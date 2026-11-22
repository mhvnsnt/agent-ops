import json, glob, os
from datetime import datetime, timezone
rows=[]
malformed=[]
unparseable=[]
for f in sorted(glob.glob(os.path.expanduser('~/workspace/agent-ops/checkpoints/*.json'))):
    try:
        d=json.load(open(f))
    except Exception as e:
        unparseable.append((f,str(e))); continue
    if d.get('watchdog') not in (True,'True'):
        continue
    if d.get('status')=='cancelled':
        continue
    name=os.path.basename(f)
    task=d.get('task') or ''
    repo=d.get('repo') or ''
    rb=d.get('resume_brief') or ''
    status=str(d.get('status') or '')
    bad=[]
    if not task: bad.append('task')
    if not repo: bad.append('repo')
    if len(rb)<50: bad.append('resume_brief<50')
    if bad: malformed.append((name,status,bad))
    rows.append((d.get('updated_at') or '', name, status, d.get('attempts'), task[:120]))
rows.sort()
print(f"managed={len(rows)} malformed={len(malformed)} unparseable={len(unparseable)}")
print("MALFORMED:")
for m in malformed: print(m)
print("UNPARSEABLE:")
for u in unparseable: print(u)
print("NON-DONE/COMPLETE (oldest first):")
for r in rows:
    if r[2].lower() not in ('done','complete'):
        print(r)
print("NEWEST 10 overall:")
for r in rows[-10:]: print(r)
now=datetime.now(timezone.utc)
print("now_utc", now.isoformat())
