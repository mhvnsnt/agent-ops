#!/bin/bash
# watchdog 2026-10-14 03:25 run — offload triple-xxx + attire-pull-rest to GitHub
# releases (Drive full), size-verify, then delete staging + local sources.
set -u
STAGE="$HOME/workspace/agent-ops/.store-staging"
REPO="mhvnsnt/google-drive-repo"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"

upload_one() {
  local name="$1" tag="$2" tar="$3" expect_sz="$4"
  local piece; piece="$(basename "$tar")"
  local ok=0
  for attempt in 1 2 3 4 5; do
    out=$(gh release upload "$tag" "$tar" --repo "$REPO" --clobber 2>&1)
    rc=$?
    echo "$out" | tail -2
    if [ $rc -eq 0 ]; then ok=1; break; fi
    echo "$(date -u +%FT%TZ) [watchdog] $name upload attempt $attempt failed (rc=$rc), retrying" >> "$LOG"
    sleep $((attempt*20))
  done
  if [ $ok -eq 0 ]; then
    echo "$(date -u +%FT%TZ) [watchdog] $name FAILED after 5 attempts — NOT deleted" >> "$LOG"
    return 1
  fi
  remote_sz=$(gh api "repos/$REPO/releases/tags/$tag" --jq ".assets[] | select(.name==\"$piece\") | .size" 2>/dev/null)
  if [ "$remote_sz" != "$expect_sz" ]; then
    echo "$(date -u +%FT%TZ) [watchdog] $name SIZE MISMATCH local=$expect_sz remote=$remote_sz — NOT deleted" >> "$LOG"
    return 2
  fi
  echo "$(date -u +%FT%TZ) [watchdog] $name verified on GitHub release $tag ($expect_sz bytes)" >> "$LOG"
  return 0
}

T1_SZ=182784000; T2_SZ=506757120

upload_one triple-xxx triple-xxx-automigrate-2026-10-14 "$STAGE/triple-xxx-automigrate-2026-10-14.tar" "$T1_SZ" && \
upload_one attire-pull-rest attire-pull-rest-automigrate-2026-10-14 "$STAGE/attire-pull-rest-automigrate-2026-10-14.tar" "$T2_SZ"
rc=$?

if [ $rc -eq 0 ]; then
  # Manifest entries
  python3 - "$STAGE" >> "$LOG" <<'PYEOF'
import json, os, sys
stage = sys.argv[1]
mp = os.path.expanduser('~/workspace/agent-ops/STORAGE-MANIFEST.json')
d = json.load(open(mp)) if os.path.exists(mp) else {}
d['triple-xxx-automigrate-2026-10-14'] = {
  'bytes': 182784000, 'sha256': '29fb777bbd31c8f2fb85320cbed59b91649865c9f80ae1611e2c5a1100517d24',
  'store': 'github-release', 'repo': 'mhvnsnt/google-drive-repo',
  'tag': 'triple-xxx-automigrate-2026-10-14', 'asset': 'triple-xxx-automigrate-2026-10-14.tar',
  'source': '~/workspace/triple-xxx', 'uploaded': '2026-10-14T07:35:00Z', 'by': 'worker-watchdog'}
d['attire-pull-rest-automigrate-2026-10-14'] = {
  'bytes': 506757120, 'sha256': 'bafc8601d4d74c914461c3ec1cf90840bc0c175941c9c50fec1ea9eb239d1b94',
  'store': 'github-release', 'repo': 'mhvnsnt/google-drive-repo',
  'tag': 'attire-pull-rest-automigrate-2026-10-14', 'asset': 'attire-pull-rest-automigrate-2026-10-14.tar',
  'source': '~/workspace/attire-pull', 'uploaded': '2026-10-14T07:35:00Z', 'by': 'worker-watchdog',
  'note': 'remainder after cain+edwin (pablo/props/sensei/tarzanian/wreck + push_attires.py + robust_push.py)'}
json.dump(d, open(mp, 'w'), indent=2)
print('[watchdog] manifest updated: triple-xxx + attire-pull-rest entries added')
PYEOF
  rm -f "$STAGE/triple-xxx-automigrate-2026-10-14.tar" "$STAGE/attire-pull-rest-automigrate-2026-10-14.tar"
  rm -rf "$HOME/workspace/triple-xxx" "$HOME/workspace/attire-pull"
  echo "$(date -u +%FT%TZ) [watchdog] deleted staging tars + ~/workspace/triple-xxx (175M) + ~/workspace/attire-pull (484M); ~659M freed" >> "$LOG"
  echo "DONE-ALL-VERIFIED-DELETED"
else
  echo "UPLOADS-NOT-VERIFIED — nothing deleted"
fi
