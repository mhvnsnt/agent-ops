#!/usr/bin/env python3
"""Resilient GitHub release uploader — retries through proxy flaps until all parts are up.
DURABLE LOCATION: ~/workspace/agent-ops/at-upload-resilient.py
NEVER store in /tmp — VM restarts wipe /tmp (NO-TEMP-STORAGE LAW, owner 2026-11-21).
Log lives alongside: ~/workspace/agent-ops/at-upload-resilient.log
"""
import subprocess, time, sys, os

REPO = "mhvnsnt/cn-gigaleak-adventure-time"
TAG = "at-cnzip-20261015"
WORKDIR = "/home/hatch/workspace/cn-pull-bigend/work-at"
LOG = "/home/hatch/workspace/agent-ops/at-upload-resilient.log"

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def uploaded_parts():
    r = subprocess.run(
        ["gh", "release", "view", TAG, "--repo", REPO, "--json", "assets", "--jq", ".assets[].name"],
        capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return None
    return set(r.stdout.strip().split("\n")) if r.stdout.strip() else set()

def main():
    parts = sorted(f for f in os.listdir(WORKDIR) if f.startswith("at-cnzip-000.part_"))
    log(f"Found {len(parts)} parts to check")
    consecutive_failures = 0
    while True:
        up = uploaded_parts()
        if up is None:
            log("Cannot reach GitHub API (proxy down?), waiting 60s...")
            time.sleep(60)
            continue
        remaining = [p for p in parts if p not in up]
        if not remaining:
            log(f"ALL {len(parts)} PARTS UPLOADED. Done.")
            return 0
        log(f"{len(remaining)} parts remaining: {remaining[0]}...")
        p = remaining[0]
        r = subprocess.run(
            ["gh", "release", "upload", TAG, os.path.join(WORKDIR, p), "--repo", REPO],
            capture_output=True, text=True, timeout=900)
        if r.returncode == 0:
            log(f"UPLOADED {p}")
            consecutive_failures = 0
        else:
            err = (r.stderr or r.stdout or "")[:200]
            log(f"FAILED {p}: {err}")
            consecutive_failures += 1
            wait = min(60 * consecutive_failures, 300)
            log(f"Waiting {wait}s before retry...")
            time.sleep(wait)

if __name__ == "__main__":
    sys.exit(main())
