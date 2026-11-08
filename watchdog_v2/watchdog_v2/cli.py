"""CLI: `watchdog-v2 check | score | penalize`.

`check` takes the filelock before doing anything: if another watchdog is
already running, this one records the blocked duplicate (+5 — the lock
doing its job is a success, not an error) and exits 75 without scanning.
That single rule would have prevented the Oct 27-28 duplicate-writer
corruption and every duplicate-lane accident since.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import structlog
from filelock import FileLock, Timeout

from .ledger import Ledger
from .scan import scan

DEFAULT_CHECKPOINTS = Path.home() / "workspace/agent-ops/checkpoints"
DEFAULT_STATE = Path(os.environ.get(
    "WATCHDOG_V2_STATE",
    Path.home() / "workspace/agent-ops/watchdog_v2/state"))


def main(argv: list[str] | None = None) -> int:
    structlog.configure(processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ])
    parser = argparse.ArgumentParser(prog="watchdog-v2")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_check = sub.add_parser("check", help="run one read-only scan")
    p_check.add_argument("--checkpoints", type=Path, default=DEFAULT_CHECKPOINTS)
    p_check.add_argument("--state", type=Path, default=DEFAULT_STATE)
    p_check.add_argument("--disk-path", default=str(Path.home()))
    p_check.add_argument("--no-http", action="store_true")
    p_score = sub.add_parser("score", help="show the reward ledger total and level")
    p_score.add_argument("--state", type=Path, default=DEFAULT_STATE)
    p_pen = sub.add_parser("penalize",
                           help="record a false alarm against the watchdog (-25)")
    p_pen.add_argument("--state", type=Path, default=DEFAULT_STATE)
    p_pen.add_argument("detail")
    args = parser.parse_args(argv)

    ledger = Ledger(args.state / "watchdog_v2.db")
    try:
        if args.cmd == "score":
            print(json.dumps({"score": ledger.total_score(),
                              "level": ledger.level()}))
            return 0
        if args.cmd == "penalize":
            ledger.award("false_alarm", args.detail)
            print(json.dumps({"score": ledger.total_score(),
                              "level": ledger.level(),
                              "penalized": args.detail}))
            return 0
        # check
        lock = FileLock(str(args.state / "watchdog_v2.lock"), timeout=0)
        try:
            lock.acquire()
        except Timeout:
            ledger.award("duplicate_run_blocked", "filelock held by another run")
            print(json.dumps({"blocked_duplicate": True,
                              "score": ledger.total_score()}))
            return 75
        with lock:
            report = scan(args.checkpoints, ledger,
                          disk_path=args.disk_path,
                          check_http=not args.no_http)
        print(json.dumps(report, indent=1, default=str))
        return 0
    finally:
        ledger.close()


if __name__ == "__main__":
    sys.exit(main())
