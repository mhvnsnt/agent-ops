#!/usr/bin/env python3
"""Restore 3 checkpoint files zeroed by the 2026-11-20 09:37 EST watchdog
heartbeat attempt during a disk-quota write flicker (child-process writes
returning EPERM). Source: .supervisor-last.json (2026-11-17 snapshot, full
content). Retries writes until the flicker passes, then verifies by re-read.
Run: python3 restore-3-ckpt.py  (background; exits 0 only if all 3 verify)
"""
import json, os, ast, sys, time
from datetime import datetime, timezone

CKPT = "/home/hatch/workspace/agent-ops/checkpoints"
SNAP = "/home/hatch/workspace/agent-ops/.supervisor-last.json"

NOTES = {
 "charfix-worker-batch3.json": "[worker-watchdog 2026-11-20 09:41 EST] RECOVERED after 09:37 EST heartbeat attempt zeroed this file during a disk-quota write flicker (child-process writes returning EPERM). Restored from .supervisor-last.json snapshot (2026-11-17 03:32, full content incl. notes) + timestamps bumped to now. Parent hold re-verified same tick: game-sweep/AshLanev2 absent, no CHARFIX_STATUS.md/_charfix_viewer.html. Heartbeat only; attempts unchanged.",
 "concrete-dragon-improve-loop.json": "[worker-watchdog 2026-11-20 09:41 EST] RECOVERED after 09:37 EST heartbeat attempt zeroed this file during a disk-quota write flicker (child-process writes returning EPERM). Restored from .supervisor-last.json snapshot (2026-11-17 03:32, full content incl. notes) + timestamps bumped to now. Owner pause on ALL Concrete Dragon work re-verified same tick (no lift in 2026-11-20 log). Heartbeat only; attempts stay 20.",
 "gap-closure-w4d-dolphin-route3.json": "[worker-watchdog 2026-11-20 09:41 EST] RECOVERED after 09:37 EST heartbeat attempt zeroed this file during a disk-quota write flicker (child-process writes returning EPERM). Restored from .supervisor-last.json snapshot (2026-11-17 03:32, full content incl. notes) + timestamps bumped to now. QUEUED brief only - do not start. Heartbeat only; attempts unchanged.",
}

def build(fname, e):
    d = {k: v for k, v in e.items() if not k.startswith("_")}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
    newnote = NOTES[fname]
    old_notes = d.get("notes", "")
    # gap-closure notes is a LIST in the Nov 17 snapshot; ckpt schema wants str.
    # Join it (preserves every entry, matches the string form the file had on
    # Nov 20). Never print the value in errors - it is ~30KB.
    if isinstance(old_notes, list):
        if fname == "gap-closure-w4d-dolphin-route3.json" and "note" not in d and old_notes:
            d["note"] = old_notes[0]
        old_notes = " | ".join(str(x) for x in old_notes)
    elif fname == "gap-closure-w4d-dolphin-route3.json" and "note" not in d:
        try:
            lst = ast.literal_eval(old_notes)
            if isinstance(lst, list) and lst:
                d["note"] = lst[0]
        except Exception as ex:
            print(fname, "note rebuild failed:", type(ex).__name__, flush=True)
    d["updated_at"] = now
    if "heartbeat" in d:
        d["heartbeat"] = now
    if "last_heartbeat" in d:
        d["last_heartbeat"] = now
    d["notes"] = newnote + " | " + old_notes
    return d

def verify(fname, d):
    full = os.path.join(CKPT, fname)
    got = json.load(open(full, encoding="utf-8"))
    assert got.get("status") == d["status"], "status mismatch"
    assert got.get("task") == d["task"], "task mismatch"
    assert len(got.get("resume_brief") or "") >= 50, "brief too short"
    assert got.get("watchdog") is True, "watchdog flag lost"
    assert len(str(got.get("notes") or "")) >= len(str(d.get("notes") or "")) - 5, "notes truncated"
    return os.path.getsize(full)

def main():
    snap = json.load(open(SNAP, encoding="utf-8"))
    by_file = {e["_file"]: e for e in snap if "_file" in e}
    pending = list(NOTES.keys())
    for attempt in range(1, 61):
        still = []
        for fname in pending:
            try:
                d = build(fname, by_file[os.path.join(CKPT, fname)])
                tmp = os.path.join(CKPT, fname + ".restore-tmp")
                with open(tmp, "w", encoding="utf-8") as fh:
                    json.dump(d, fh, indent=1, ensure_ascii=False)
                    fh.write("\n")
                    fh.flush()
                    os.fsync(fh.fileno())
                os.replace(tmp, os.path.join(CKPT, fname))
                size = verify(fname, d)
                print(f"[{attempt}] RESTORED {fname} bytes={size} updated_at={d['updated_at']}", flush=True)
            except Exception as ex:
                print(f"[{attempt}] {fname} FAILED: {type(ex).__name__}: {ex}", flush=True)
                still.append(fname)
        pending = still
        if not pending:
            print("ALL THREE RESTORED AND VERIFIED", flush=True)
            return 0
        time.sleep(15)
    print("GAVE UP after 60 attempts; still pending:", pending, flush=True)
    return 1

if __name__ == "__main__":
    sys.exit(main())
