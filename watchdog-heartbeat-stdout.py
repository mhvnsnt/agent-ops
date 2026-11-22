"""Print the heartbeated checkpoint JSON for ONE file to stdout (no file writes).
Caller captures stdout and writes it with a shell builtin (TOOLS.md workaround
for the intermittent child-process file-write block)."""
import json, os, sys, datetime
d = "/home/hatch/workspace/agent-ops/checkpoints"
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
n = sys.argv[1]
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
print(json.dumps(j, indent=1))
