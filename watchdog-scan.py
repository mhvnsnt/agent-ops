import json, os, glob
from datetime import datetime, timezone
d="/home/hatch/workspace/agent-ops/checkpoints"
now=datetime.now(timezone.utc)
rows=[]; malformed=[]; total=0
for p in sorted(glob.glob(d+"/*.json")):
    try:
        with open(p) as f: j=json.load(f)
    except Exception:
        continue
    if not isinstance(j, dict) or j.get("watchdog") is not True: continue
    total+=1
    if j.get("status")=="cancelled": continue
    st=j.get("status"); upd=j.get("updated_at")
    age=None
    try:
        u=upd.replace("Z","+00:00") if isinstance(upd,str) else None
        dt=datetime.fromisoformat(u) if u else None
        if dt and dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
        age=(now-dt).total_seconds()/60 if dt else None
    except Exception: pass
    task=j.get("task"); repo=j.get("repo"); rb=j.get("resume_brief")
    valid = bool(task and repo and isinstance(rb,str) and len(rb)>=50)
    if not valid:
        malformed.append((os.path.basename(p), st, upd, task, repo, len(rb) if isinstance(rb,str) else rb))
    if st not in ("done","complete"):
        rows.append((age if age is not None else 99999999, os.path.basename(p), st, upd, j.get("attempts"), valid))
print("managed total:", total)
print("OPEN managed (not done/complete/cancelled), oldest first:")
for r in sorted(rows, reverse=True):
    print(r)
print("MALFORMED managed:")
for m in malformed: print(m)
print("counts open=", len(rows), " malformed=", len(malformed))
