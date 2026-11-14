"""The scan — registry, disk, live builds. READ-ONLY end to end.

Stack (all industry-standard OSS, composed — no framework does this
exact job off the shelf):
- filelock   single-instance guarantee (the Oct 27-28 duplicate-writer
             race is what corrupted the TTT2 spool; two watchdogs must
             never run at once)
- pydantic   checkpoint classification (models.py)
- psutil     disk usage — the standard system-metrics library
- httpx      live-build health checks
- tenacity   bounded retry with backoff for those checks (2 tries, no more)
- structlog  structured JSON logs, one event per finding
- pybreaker  circuit breaker for HTTP endpoints: 3 consecutive failures
             opens the circuit, the endpoint is reported DOWN once and
             then suppressed instead of hammered/reported every run
- SQLite WAL dedupe + circuit state for checkpoint targets (ledger.py)
"""
from __future__ import annotations

import time
from pathlib import Path

import httpx
import psutil
import pybreaker
import structlog
from tenacity import retry, stop_after_attempt, wait_fixed

from .ledger import Ledger
from .models import CheckpointClass, classify_file

log = structlog.get_logger("watchdog_v2")

LIVE_BUILDS = {
    "western-heart": "https://mhvnsnt.github.io/western-heart/",
    "physique-lab": "https://physics-playground-pwa.pages.dev/",
    "mochichao-crystal": "https://mochiichao.pages.dev/",
}

DISK_WARN = 80.0
DISK_SURFACE = 85.0


def _sanitize_proxy_env() -> None:
    """This host's no_proxy contains bare IPv6 literals (::1, [::1]) that
    crash httpx's URL parser (httpx.InvalidURL: Invalid port ':1]') —
    documented in TOOLS.md 2026-10-06. Without this, every health check
    returns None and the watchdog reports all live builds DOWN: a false
    alarm factory. Strip only the '::' tokens, keep the proxy itself."""
    import os
    for key in ("no_proxy", "NO_PROXY"):
        raw = os.environ.get(key)
        if raw:
            kept = [t for t in raw.split(",") if "::" not in t]
            os.environ[key] = ",".join(kept)


@retry(stop=stop_after_attempt(2), wait=wait_fixed(2), reraise=True)
def _fetch_status(url: str) -> int:
    _sanitize_proxy_env()
    with httpx.Client(timeout=15.0, follow_redirects=True) as client:
        return client.get(url).status_code


class BuildBreaker:
    """One pybreaker per live build, state kept across runs in-process;
    cross-run suppression comes from the ledger's issue dedupe."""

    def __init__(self) -> None:
        self._breakers = {
            name: pybreaker.CircuitBreaker(fail_max=3, reset_timeout=3600, name=name)
            for name in LIVE_BUILDS
        }

    def check(self, name: str, url: str) -> int | None:
        try:
            return self._breakers[name].call(_fetch_status, url)
        except Exception:
            return None


def scan(checkpoints_dir: Path, ledger: Ledger, *, disk_path: str,
         check_http: bool = True, now: float | None = None) -> dict:
    """Run one full read-only scan. Returns the report dict; every
    surface-worthy finding in report['new_issues'] is NEW (the ledger
    guarantees an unchanged problem is never reported twice)."""
    now = now if now is not None else time.time()
    report: dict = {"ts": now, "new_issues": [], "counts": {}, "score_delta": 0}

    def surface(kind: str, target: str, detail: str, reward: str | None) -> None:
        key = f"{kind}:{target}:{detail.split(',')[0]}"
        if ledger.record_issue(key, kind, target, detail):
            report["new_issues"].append(
                {"kind": kind, "target": target, "detail": detail})
            log.info("issue", kind=kind, target=target, detail=detail)
            if reward:
                report["score_delta"] += ledger.award(reward, f"{target}: {detail}")

    # ---- checkpoint registry -------------------------------------------
    counts: dict[str, int] = {}
    active_watch: list[str] = []
    # Skip dot-prefixed files: the lanes' atomic-write temps (.tmp.*.json,
    # .gitkeep) are write debris, not checkpoints. v2.0 counted them and
    # surfaced two 0-byte temps as corrupt_checkpoint on 2026-11-11 —
    # a false alarm, verified own-eyes (no checkpoint data was lost).
    all_json = sorted(checkpoints_dir.glob("*.json"))
    skipped_temp = [p for p in all_json if p.name.startswith(".")]
    files = [p for p in all_json if not p.name.startswith(".")]
    for path in files:
        cls, cp, detail = classify_file(path, now=now)
        counts[cls.value] = counts.get(cls.value, 0) + 1
        prev = ledger.previous_class(path.name)
        state = ledger.observe_target(
            path.name, cls.value, (cp.status if cp else None), path.stat().st_mtime)
        if cls in (CheckpointClass.ACTIVE, CheckpointClass.STALE,
                   CheckpointClass.NEEDS_OWNER):
            active_watch.append(path.name)
        # New completion: was not done last scan, is done now, and the file
        # is fresh enough to be news (not a first-scan discovery of old work).
        age_h = (now - path.stat().st_mtime) / 3600.0
        if cls == CheckpointClass.DONE and prev is not None and prev != "done" and age_h < 48:
            surface("completion", path.name, detail, "new_completion")
        if cls == CheckpointClass.STALE:
            surface("stall", path.name, detail, "new_stall_detected")
        if cls in (CheckpointClass.ZERO, CheckpointClass.CORRUPT) \
                and not state["circuit_open"]:
            surface("corrupt_checkpoint", path.name, detail, None)
        # cls == DEAD: old zero/corrupt — logged in counts, never surfaced.
    report["counts"] = counts
    report["total_checkpoints"] = len(files)
    report["skipped_temp_files"] = len(skipped_temp)
    report["active_watch"] = sorted(active_watch)

    # ---- disk ------------------------------------------------------------
    disk = psutil.disk_usage(disk_path)
    report["disk_percent"] = disk.percent
    # Disk trend: which way the number is heading since the last run,
    # so a slow climb (66% -> 81% over two days in Nov 2026) is visible
    # before it trips a threshold, not only after.
    prev_disk = ledger.last_disk_percent()
    if prev_disk is None:
        report["disk_delta"] = None
        report["disk_trend"] = "unknown"
    else:
        delta = round(disk.percent - prev_disk, 1)
        report["disk_delta"] = delta
        report["disk_trend"] = "rising" if delta >= 1 else (
            "falling" if delta <= -1 else "flat")
    if disk.percent >= DISK_SURFACE:
        surface("disk_high", disk_path, f"{disk.percent:.0f}% used", "early_disk_warning")
    elif disk.percent >= DISK_WARN:
        surface("disk_warn", disk_path, f"{disk.percent:.0f}% used", "early_disk_warning")

    # ---- live builds -------------------------------------------------------
    builds: dict[str, int | None] = {}
    if check_http:
        breaker = BuildBreaker()
        for name, url in LIVE_BUILDS.items():
            status = breaker.check(name, url)
            builds[name] = status
            if status != 200:
                surface("build_down", name, f"{url} -> {status}", None)
    report["live_builds"] = builds

    if not report["new_issues"]:
        report["score_delta"] += ledger.award("clean_heartbeat", "scan clean")
    ledger.record_run(disk.percent, len(files), len(report["new_issues"]),
                      report["score_delta"])
    report["score_total"] = ledger.total_score()
    report["level"] = ledger.level()
    return report
