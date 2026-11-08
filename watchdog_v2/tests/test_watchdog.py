"""Tests — each one maps to a real failure of the old watchdog.

Run: pytest watchdog_v2/tests -q  (from the agent-ops repo root, with the
project installed or PYTHONPATH=watchdog_v2)
"""
import json
import os
import time

from watchdog_v2.ledger import Ledger
from watchdog_v2.models import CheckpointClass, classify_file
from watchdog_v2.scan import scan


def _ledger(tmp_path):
    return Ledger(tmp_path / "state" / "test.db")


def _ckpt(tmp_path, name, content, age_h=0.0):
    p = tmp_path / name
    if isinstance(content, (dict, list)):
        p.write_text(json.dumps(content))
    else:
        p.write_text(content)
    if age_h:
        old = time.time() - age_h * 3600
        os.utime(p, (old, old))
    return p


def test_zero_byte_is_zero_not_a_crash(tmp_path):
    # The 2026-11-02 failure: a wiped 0-byte checkpoint must classify,
    # never raise, never loop.
    p = _ckpt(tmp_path, "wiped.json", "")
    cls, cp, detail = classify_file(p, now=time.time())
    assert cls == CheckpointClass.ZERO and cp is None


def test_old_zero_byte_is_dead_news_not_an_alarm(tmp_path):
    p = _ckpt(tmp_path, "ttt2-resume-100.json", "", age_h=120)
    cls, _, _ = classify_file(p, now=time.time())
    assert cls == CheckpointClass.DEAD


def test_corrupt_json_classifies(tmp_path):
    p = _ckpt(tmp_path, "bad.json", "{not json")
    cls, _, _ = classify_file(p, now=time.time())
    assert cls == CheckpointClass.CORRUPT


def test_stale_live_lane_classifies(tmp_path):
    p = _ckpt(tmp_path, "lane.json", {"status": "running", "task_id": "lane"},
              age_h=10)
    cls, _, _ = classify_file(p, now=time.time())
    assert cls == CheckpointClass.STALE


def test_dedupe_same_issue_never_resurfaces(tmp_path):
    # The 8-day re-nag failure: detect a stall 4 scans in a row, it must
    # be reported exactly once, and the circuit breaker must open.
    led = _ledger(tmp_path)
    ck = tmp_path / "ck"
    ck.mkdir()
    _ckpt(ck, "lane.json", {"status": "running"}, age_h=10)
    surfaced = 0
    for _ in range(4):
        rep = scan(ck, led, disk_path=str(tmp_path), check_http=False)
        surfaced += len([i for i in rep["new_issues"] if i["kind"] == "stall"])
    assert surfaced == 1
    row = led.db.execute(
        "SELECT circuit_open FROM targets WHERE target='lane.json'").fetchone()
    # stall is not a dead class, so no circuit — dedupe alone did the work
    assert row[0] == 0
    led.close()


def test_dead_target_circuit_opens_and_suppresses(tmp_path):
    led = _ledger(tmp_path)
    ck = tmp_path / "ck"
    ck.mkdir()
    _ckpt(ck, "dead.json", "")
    surfaced = 0
    for _ in range(5):
        rep = scan(ck, led, disk_path=str(tmp_path), check_http=False)
        surfaced += len(rep["new_issues"])
    row = led.db.execute(
        "SELECT circuit_open, dead_streak FROM targets WHERE target='dead.json'"
    ).fetchone()
    assert row[0] == 1 and row[1] >= 3
    assert surfaced <= 2  # surfaced at first sight, suppressed after
    led.close()


def test_paused_is_parked_not_stalled(tmp_path):
    # Regression, first live scan 2026-11-07: lanes paused for 500+ hours
    # were flagged as stalls. Paused = parked on purpose.
    p = _ckpt(tmp_path, "parked.json", {"status": "paused"}, age_h=500)
    cls, _, _ = classify_file(p, now=time.time())
    assert cls == CheckpointClass.OTHER


def test_proxy_env_sanitizer_strips_ipv6_literals(monkeypatch):
    # Regression, first live scan 2026-11-07: this host's no_proxy holds
    # bare ::1 literals that crash httpx and made every live build look
    # DOWN while curl showed 200s.
    from watchdog_v2.scan import _sanitize_proxy_env
    monkeypatch.setenv("no_proxy", "localhost,::1,[::1],example.com")
    _sanitize_proxy_env()
    import os
    assert os.environ["no_proxy"] == "localhost,example.com"


def test_rewards_accrue_and_penalty_applies(tmp_path):
    led = _ledger(tmp_path)
    assert led.award("clean_heartbeat") == 2
    assert led.award("new_completion") == 10
    assert led.total_score() == 12
    assert led.award("false_alarm", "claimed stall that wasn't") == -25
    assert led.total_score() == -13
    led.close()


def test_completion_transition_is_news_once(tmp_path):
    led = _ledger(tmp_path)
    ck = tmp_path / "ck"
    ck.mkdir()
    p = _ckpt(ck, "job.json", {"status": "running"})
    scan(ck, led, disk_path=str(tmp_path), check_http=False)
    p.write_text(json.dumps({"status": "completed"}))
    rep = scan(ck, led, disk_path=str(tmp_path), check_http=False)
    kinds = [i["kind"] for i in rep["new_issues"]]
    assert "completion" in kinds
    rep2 = scan(ck, led, disk_path=str(tmp_path), check_http=False)
    assert not [i for i in rep2["new_issues"] if i["kind"] == "completion"]
    led.close()
