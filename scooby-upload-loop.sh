#!/bin/bash
# Uploads the 34 missing scooby files as release assets (extract -> upload -> delete, one at a time).
set -uo pipefail
REPO=mhvnsnt/cn-gigaleak-scooby-doo-mystery-inc
TAG=scooby-complete-v1
ZIP="$HOME/workspace/cn-gigaleak-raw/scooby/Scooby-Doo! Mystery Inc.zip"
STAGE="$HOME/workspace/agent-ops/scooby-staging"
LOG="$HOME/workspace/agent-ops/scooby-upload.log"
mkdir -p "$STAGE"
exec >>"$LOG" 2>&1
echo "=== run started $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
python3 - "$ZIP" "$STAGE" <<'PYEOF'
import zipfile, os, json, urllib.request, re, sys
zip_path, stage = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(zip_path)
def gh(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/vnd.github+json'})))
tree = gh('https://api.github.com/repos/mhvnsnt/cn-gigaleak-scooby-doo-mystery-inc/git/trees/c85faf5fa1ad8b7220e1564c21f34a0b264db38f?recursive=1')
tb=set(os.path.basename(e['path']) for e in tree['tree'] if e['type']=='blob')
rels=gh('https://api.github.com/repos/mhvnsnt/cn-gigaleak-scooby-doo-mystery-inc/releases')
assets=set()
for r in rels:
    for a in r.get('assets',[]):
        n=a['name']; m=re.match(r'^(.*)\.part_[a-z]{2}$',n)
        assets.add(m.group(1) if m else n)
covered=tb|assets
jobs=[]
from collections import Counter
cands=[]
for i in z.infolist():
    if i.is_dir(): continue
    n=i.filename; p='Scooby-Doo! Mystery Inc/'
    if n.startswith(p): n=n[len(p):]
    b=os.path.basename(n)
    if '/._' in n or b.startswith('._') or b=='.DS_Store': continue
    if b not in covered: cands.append((i.filename,n,b))
cnt=Counter(b for _,_,b in cands)
for zf,rel,b in cands:
    out=b
    if cnt[b]>1:
        parent=os.path.basename(os.path.dirname(rel)).replace(' ','_')
        out=f"{parent}__{b}"
    jobs.append((zf,out))
with open(os.path.join(stage,'jobs.json'),'w') as f: json.dump(jobs,f)
print('jobs:',len(jobs))
PYEOF
if [ ! -s "$STAGE/jobs.json" ]; then echo "no jobs; exiting"; exit 0; fi
python3 - "$STAGE" "$REPO" "$TAG" <<'PYEOF'
import json, os, subprocess, sys
stage, repo, tag = sys.argv[1], sys.argv[2], sys.argv[3]
done_file = os.path.join(stage,'done.txt')
done = set(open(done_file).read().split()) if os.path.exists(done_file) else set()
jobs = json.load(open(os.path.join(stage,'jobs.json')))
for zf, out in jobs:
    if out in done:
        print(f"SKIP (already done): {out}", flush=True); continue
    print(f"extract+upload: {out}", flush=True)
    # extract via python one-liner
    r = subprocess.run(['python3','-c',
        "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); data=z.read(sys.argv[2]); open(sys.argv[3],'wb').write(data)",
        os.path.expanduser('~/workspace/cn-gigaleak-raw/scooby/Scooby-Doo! Mystery Inc.zip'), zf, os.path.join(stage,out)])
    if r.returncode != 0: print(f"EXTRACT FAIL: {out}", flush=True); break
    r = subprocess.run(['gh','release','upload',tag,os.path.join(stage,out),'--repo',repo,'--clobber'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"UPLOAD FAIL: {out}\n{r.stderr}", flush=True); break
    print(f"OK: {out}", flush=True)
    os.remove(os.path.join(stage,out))
    with open(done_file,'a') as f: f.write(out+'\n')
print("loop finished pass")
PYEOF
echo "=== run ended $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
