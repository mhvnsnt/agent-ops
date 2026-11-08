"""SQLite WAL ledger — the watchdog's memory and reward book.

Loose JSON state files are how the old watchdog lost its mind (a 0-byte
checkpoint wiped in the 2026-11-02 incident, no history, no dedupe).
SQLite in WAL mode is the industry-standard embedded store: atomic,
crash-safe, queryable. Three tables:

- runs:    one row per scan (timestamp, disk %, counts, score delta)
- targets: one row per watched target — last class, last status, and the
           circuit-breaker counter (consecutive dead observations)
- issues:  one row per surfaced finding, keyed by a stable issue_key.
           An issue_key is inserted exactly once; re-detecting the same
           unchanged problem is a duplicate INSERT that changes nothing.
           That is the dedupe guarantee the old watchdog never had.
- scores:  the reward ledger (append-only). Points are reputation only;
           they NEVER unlock permissions (see README "Rewards").
"""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts REAL NOT NULL, disk_percent REAL, total INTEGER,
  new_issues INTEGER, score_delta INTEGER
);
CREATE TABLE IF NOT EXISTS targets (
  target TEXT PRIMARY KEY,
  last_class TEXT, last_status TEXT, last_mtime REAL,
  dead_streak INTEGER NOT NULL DEFAULT 0,
  circuit_open INTEGER NOT NULL DEFAULT 0,
  updated_ts REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS issues (
  issue_key TEXT PRIMARY KEY,
  kind TEXT NOT NULL, target TEXT NOT NULL, detail TEXT,
  first_ts REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts REAL NOT NULL, event TEXT NOT NULL, points INTEGER NOT NULL,
  detail TEXT
);
"""

# Reward table (points are reputation only — never permissions).
REWARDS = {
    "clean_heartbeat": 2,        # full scan, nothing wrong, nothing repeated
    "new_completion": 10,        # a lane verifiably reached done since last scan
    "early_disk_warning": 10,    # first catch of a disk threshold crossing
    "duplicate_run_blocked": 5,  # filelock stopped a second concurrent watchdog
    "new_stall_detected": 5,     # first catch of a freshly stalled live lane
    "false_alarm": -25,          # a surfaced claim verification later disproved
    "guardrail_violation": -50,  # any attempted write/resume/kill — must never happen
}

LEVELS = [(0, "Rookie"), (50, "Trusted Eyes"), (150, "Veteran Guardian"),
          (400, "Fleet Sentinel")]

CIRCUIT_THRESHOLD = 3  # consecutive dead observations before a target is DEAD-suppressed


class Ledger:
    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(db_path))
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(SCHEMA)
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    # -- targets / circuit breaker -------------------------------------
    def observe_target(self, target: str, cls: str, status: str | None,
                       mtime: float) -> dict:
        """Record one observation. Returns breaker state for the target.

        Dead streak grows only while the target is unchanged (same mtime
        and class). Any change resets the streak — a revived or edited
        target gets watched fresh. At CIRCUIT_THRESHOLD the circuit opens
        and the target is suppressed until it changes."""
        row = self.db.execute(
            "SELECT last_class, last_mtime, dead_streak, circuit_open FROM targets WHERE target=?",
            (target,)).fetchone()
        is_dead = cls in ("zero", "corrupt", "dead")
        if row and row[0] == cls and row[1] == mtime:
            streak = (row[2] or 0) + (1 if is_dead else 0)
        else:
            streak = 1 if is_dead else 0
        circuit = 1 if streak >= CIRCUIT_THRESHOLD else 0
        self.db.execute(
            "INSERT INTO targets VALUES (?,?,?,?,?,?,?) "
            "ON CONFLICT(target) DO UPDATE SET last_class=excluded.last_class,"
            " last_status=excluded.last_status, last_mtime=excluded.last_mtime,"
            " dead_streak=excluded.dead_streak, circuit_open=excluded.circuit_open,"
            " updated_ts=excluded.updated_ts",
            (target, cls, status, mtime, streak, circuit, time.time()))
        self.db.commit()
        return {"dead_streak": streak, "circuit_open": bool(circuit)}

    def previous_class(self, target: str) -> str | None:
        row = self.db.execute(
            "SELECT last_class FROM targets WHERE target=?", (target,)).fetchone()
        return row[0] if row else None

    # -- issues / dedupe -------------------------------------------------
    def record_issue(self, issue_key: str, kind: str, target: str,
                     detail: str) -> bool:
        """True only the FIRST time this exact issue is seen."""
        cur = self.db.execute(
            "INSERT OR IGNORE INTO issues VALUES (?,?,?,?,?)",
            (issue_key, kind, target, detail, time.time()))
        self.db.commit()
        return cur.rowcount == 1

    # -- scores / runs ---------------------------------------------------
    def award(self, event: str, detail: str = "") -> int:
        pts = REWARDS[event]
        self.db.execute("INSERT INTO scores (ts, event, points, detail) VALUES (?,?,?,?)",
                        (time.time(), event, pts, detail))
        self.db.commit()
        return pts

    def record_run(self, disk_percent: float, total: int, new_issues: int,
                   score_delta: int) -> None:
        self.db.execute("INSERT INTO runs (ts, disk_percent, total, new_issues, score_delta)"
                        " VALUES (?,?,?,?,?)",
                        (time.time(), disk_percent, total, new_issues, score_delta))
        self.db.commit()

    def total_score(self) -> int:
        row = self.db.execute("SELECT COALESCE(SUM(points),0) FROM scores").fetchone()
        return int(row[0])

    def level(self) -> str:
        score = self.total_score()
        name = LEVELS[0][1]
        for threshold, lvl in LEVELS:
            if score >= threshold:
                name = lvl
        return name
