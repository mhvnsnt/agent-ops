"""Heartbeat-only tick for held checkpoints: bump updated_at, append a
short notes line. Status/attempts/task/repo/resume_brief untouched.
Atomic write (temp + os.replace), all content built in memory."""
import json, os, sys, datetime
d = "/home/hatch/workspace/agent-ops/checkpoints"
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
names = sys.argv[1:]
for n in names:
    p = os.path.join(d, n)
    j = json.load(open(p))
    j["updated_at"] = now
    line = ("[worker-watchdog 2026-11-20 08:01 EST] Quiet tick, nothing resumed. "
            "Holds re-verified: charfix parent hold / CD owner pause / "
            "gap-closure-w4d-dolphin-route3 queued brief-only do-not-start. "
            "Heartbeat only; status/attempts unchanged.")
    notes = j.get("notes")
    if isinstance(notes, list):
        notes.append(line)
        j["notes"] = notes
    elif isinstance(notes, str):
        j["notes"] = notes + "\n" + line
    else:
        j["notes"] = line
    tmp = p + ".tmp-wd"
    with open(tmp, "w") as f:
        json.dump(j, f, indent=1)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, p)
    print("heartbeated", n, "->", now)
