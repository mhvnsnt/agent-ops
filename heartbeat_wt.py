#!/usr/bin/env python3
"""Heartbeat helper for wrestling-game-teardown checkpoint."""
import json, datetime, os, sys
p = os.path.expanduser('~/workspace/agent-ops/checkpoints/wrestling-game-teardown.json')
d = json.load(open(p))
if len(sys.argv) > 1:
    d['notes'].append(sys.argv[1])
d['updated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
tmp = p + '.tmp'
json.dump(d, open(tmp, 'w'), indent=1)
os.rename(tmp, p)
print('heartbeat ok', d['updated_at'])
