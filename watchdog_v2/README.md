# Watchdog v2 — read-only lane-registry guardian

Owner order 2026-11-07: give the watchdog a new target and new rewards,
make sure it can't break anything, evaluate the old one, and build the
replacement from industry-standard full-stack parts — no hand-tooled
homebrew.

## Evaluation of the old watchdog (wh-overnight-watchdog, prompt-only)

**What it did right (Oct 29–30, TTT2 pull lane):** caught the dead pull
worker three times, relaunched it resume-capable, verified it alive each
time. Real catches, real value.

**How it failed (Nov 2–7):**
1. **Single point of failure as a target.** One checkpoint file. When that
   file was zeroed in the 2026-11-02 wipe (same incident as MEMORY.md) and
   the driver script was archived with tools/, the watchdog had nothing —
   but kept firing every 3 hours for **8 days** on the corpse.
2. **No validation.** A 0-byte file was "unparseable, needs owner decision"
   every run instead of a classified, breakered state.
3. **No circuit breaker, no dedupe.** It re-surfaced the same two owner
   questions run after run; identical findings alternated between silent
   "success" and "failed" runs with no memory of having reported them.
4. **No lock.** Nothing stopped two watchdog runs (or a watchdog and a
   lane) from acting at once — the same duplicate-writer pattern that
   corrupted the TTT2 spool on Oct 27–28.
5. **Unsafe authority.** Its instructions let it *resume lanes*. A
   prompt-only agent with launch authority and no state is how dumb
   bullshit happens. v2 removes the authority entirely.

## The new target

Not one lane — **the whole fleet's vital signs**, every 3 hours:

1. **The checkpoint registry** (`~/workspace/agent-ops/checkpoints/*.json`,
   1,230 files at build time): every file classified live/stale/done/
   needs-owner/zero/corrupt/dead. Watched closely: anything touched in
   the last 24h plus the pinned active lanes.
2. **Disk** on the workspace volume (warn at 80%, surface at 85%).
3. **The live builds** — Western Heart (GitHub Pages), Physique Lab
   (Cloudflare Pages), Mochiichao Crystal (Cloudflare Pages): HTTP 200
   or it's news, once.

## The stack (composed OSS libraries — the research verdict)

No maintained framework does checkpoint-validation + disk/process + HTTP
+ dedupe + dead-target suppression in one box, so v2 composes the
standard libraries real SRE tooling is built from:

| Concern | Library | Replaces (homebrew) |
|---|---|---|
| Single-instance lock | `filelock` | nothing — old watchdog had no lock |
| Checkpoint schema/classification | `pydantic` v2 | ad-hoc `json.load` + hope |
| Disk/process metrics | `psutil` | shelling out to `df` and eyeballing |
| HTTP health checks | `httpx` | curl in a prompt |
| Bounded retry/backoff | `tenacity` (2 attempts max) | retry-until-whatever |
| Circuit breaker (HTTP) | `pybreaker` (3 fails → open, 1h reset) | re-reporting a dead target forever |
| Structured logging | `structlog` (JSON events) | prose run reports nobody can query |
| State, dedupe, breaker state, rewards | **SQLite (WAL mode)** | loose JSON files — the thing that got wiped |

Dead-man's-switch pattern (healthchecks.io style) is adopted as a rule,
not a service: **silence is the healthy state.** The watchdog speaks only
on a *new* finding; the ledger proves it ran (runs table) even when it
says nothing.

## Guardrails — why it can't fuck anything up

- **Read-only by construction.** The package contains no code path that
  writes outside its own `state/` directory, and no resume/kill/delete/
  launch capability at all. Surfacing a problem is its only power.
- **Dedupe by issue key.** An unchanged problem is inserted into the
  ledger once (`INSERT OR IGNORE`) and never surfaces twice.
- **Circuit breaker per target.** 3 consecutive unchanged dead
  observations → target suppressed until its file actually changes.
- **Old dead is not news.** Zero/corrupt files older than 72h classify as
  DEAD (counted, never alarmed) — the ttt2-resume-100 corpse is the
  canonical example.
- **Temp debris is not a checkpoint (v2.1).** Dot-prefixed files
  (`.tmp.*.json` atomic-write leftovers, `.gitkeep`) are skipped before
  classification and counted in `skipped_temp_files`. v2.0 flagged two
  0-byte temps as corrupt on 2026-11-11 — a false alarm; nothing was lost.

## Disk trend (v2.1)

The report carries `disk_percent`, `disk_delta` (points since the last
run), and `disk_trend` (`rising` / `falling` / `flat`, ±1 point). A slow
climb is visible before it trips the 80%/85% thresholds — disk went
66% → 81% over two days in Nov 2026 while the number alone looked fine
run to run.
- **Lock or exit.** A second concurrent run exits 75 immediately.
- **Bounded everything.** 2 HTTP attempts, 15s timeouts, one pass over
  the registry, no recursion into lane workdirs.

## Rewards (new)

The ledger keeps score. Points are **reputation only — they never unlock
permissions, ever.** Authority changes are the owner's call, in words.

| Event | Points |
|---|---|
| Clean heartbeat scan | +2 |
| New verified completion detected | +10 |
| First catch of a disk threshold crossing | +10 |
| First catch of a fresh stall | +5 |
| Duplicate run blocked by the lock | +5 |
| False alarm (lead/owner marks via `penalize`) | −25 |
| Guardrail violation (any attempted write/resume/kill) | −50 |

Levels: 0 Rookie · 50 Trusted Eyes · 150 Veteran Guardian · 400 Fleet Sentinel.
Check anytime: `watchdog-v2 score`.

## Run it

```bash
cd watchdog_v2 && pip install -e .        # or use a venv
watchdog-v2 check                          # one full read-only scan, JSON out
watchdog-v2 check --no-http                # registry + disk only
watchdog-v2 score                          # reward total + level
watchdog-v2 penalize "claimed X, verification showed Y"   # false alarm, −25
pytest tests -q                            # each test maps to a real old failure
```

The `wh-overnight-watchdog` cron (every 3h, delivery to the Western Heart
side chat) runs `check` and surfaces only `new_issues`. State lives in
`watchdog_v2/state/` (gitignored; the ledger is a local operational
record, backed by the repo's code + this README).
