#!/bin/bash
# Watchdog keepalive: heartbeat the 3 disk-store checkpoints every 8 min
# while either verify script is still running. Updates updated_at only,
# never touches status/notes (the verify scripts own those).
set -u
CKPTS=~/workspace/agent-ops/checkpoints/disk-store-ep01loti.json,~/workspace/agent-ops/checkpoints/disk-store-loti-final.json,~/workspace/agent-ops/checkpoints/disk-store-fontstools.json
while pgrep -f "vft-verify-run.sh" >/dev/null || pgrep -f "loti-verify-run.sh" >/dev/null; do
  NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  python3 -c "
import json,sys,datetime
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for p in sys.argv[1].split(','):
    try:
        d=json.load(open(p)); d['updated_at']=now; json.dump(d,open(p,'w'),indent=1)
    except Exception as e: print('HB-ERR',p,e)
" "$CKPTS"
  echo "keepalive heartbeat $NOW"
  sleep 480
done
echo "keepalive: no verify script running, exiting"
