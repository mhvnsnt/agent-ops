#!/bin/bash
# disk-space-guardian: complete the urban-reign safe-storage backup.
# Strict verification before ANY deletion:
#   1. upload loop finished (log shows DONE)
#   2. release urban-reign-iso-v1 has all 3 part assets with EXACT byte sizes
#   3. re-downloaded part_ac sha256 matches local part_ac (upload-path integrity)
#   4. local parts reassemble to the known-good ISO sha256
# Only then: delete the ISO + 3 parts (8.3G). All actions logged.
REPO="mhvnsnt/western-heart"
TAG="urban-reign-iso-v1"
DIR="$HOME/workspace/game-reverse-engineering/urban-reign"
LOG="$HOME/workspace/agent-ops/urban-reign-upload.log"
ISO="$DIR/Urban Reign (USA).iso"
PA="$DIR/urban-reign-usa.iso.part_aa"
PB="$DIR/urban-reign-usa.iso.part_ab"
PC="$DIR/urban-reign-usa.iso.part_ac"
SA=1992294400; SB=1992294400; SC=156336128
ISO_SHA="c22209eefcdc4275a75dc3656b4abf5807940155236916271e19455d302a8ec2"
MARK="$HOME/workspace/agent-ops/urban-reign-cleanup.done"
CLEANLOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"

log(){ echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }

log "finalize: waiting for upload loop to finish"
deadline=$(( $(date +%s) + 10800 ))
while ! grep -q "=== DONE ===" "$LOG" 2>/dev/null; do
  [ $(date +%s) -gt $deadline ] && { log "finalize TIMEOUT waiting for upload loop"; exit 1; }
  sleep 60
done
log "finalize: upload loop reports DONE"

# 2. release assets present with exact sizes
deadline=$(( $(date +%s) + 1800 ))
while :; do
  info=$(gh api "repos/$REPO/releases/tags/$TAG" --jq '.assets | map("\(.name) \(.size)") | join(";")' 2>/dev/null)
  ok=true
  echo "$info" | grep -q "urban-reign-usa.iso.part_aa $SA" || ok=false
  echo "$info" | grep -q "urban-reign-usa.iso.part_ab $SB" || ok=false
  echo "$info" | grep -q "urban-reign-usa.iso.part_ac $SC" || ok=false
  $ok && break
  [ $(date +%s) -gt $deadline ] && { log "finalize TIMEOUT waiting for release assets: $info"; exit 1; }
  sleep 60
done
log "finalize: all 3 release assets present with exact sizes"

# 3. re-download smallest part, compare sha256 (upload-path integrity)
mkdir -p /tmp/ur-verify
rm -f /tmp/ur-verify/urban-reign-usa.iso.part_ac
if ! gh release download "$TAG" -p "urban-reign-usa.iso.part_ac" -D /tmp/ur-verify --repo "$REPO" >>"$LOG" 2>&1; then
  log "finalize: FAILED to re-download part_ac for verification"; exit 1
fi
h_down=$(sha256sum /tmp/ur-verify/urban-reign-usa.iso.part_ac | cut -d' ' -f1)
h_local=$(sha256sum "$PC" | cut -d' ' -f1)
if [ "$h_down" != "$h_local" ]; then
  log "finalize: part_ac sha256 MISMATCH down=$h_down local=$h_local - NOT deleting"; exit 1
fi
log "finalize: part_ac re-download sha256 matches ($h_down)"
rm -rf /tmp/ur-verify

# 4. local parts reassemble to known-good ISO sha256
h_re=$(cat "$PA" "$PB" "$PC" | sha256sum | cut -d' ' -f1)
if [ "$h_re" != "$ISO_SHA" ]; then
  log "finalize: reassembled-parts sha256 MISMATCH $h_re != $ISO_SHA - NOT deleting"; exit 1
fi
log "finalize: parts reassemble to verified ISO sha256"

# ALL CHECKS PASSED — delete local ISO + parts
rm -v "$ISO" "$PA" "$PB" "$PC" >>"$LOG" 2>&1
log "finalize: DELETED local ISO + 3 parts (8.3G freed)"
df -h /home/hatch | tail -1 >>"$LOG"
echo "$(date -u +%FT%TZ) urban-reign local ISO+parts deleted after verified release backup" > "$MARK"
cat >> "$CLEANLOG" << EOF

### Removed (urban-reign finalize, verified):
- \`game-reverse-engineering/urban-reign/Urban Reign (USA).iso\` (4,140,924,928 B) + 3 split parts (4,140,924,928 B) = 8.3G.
- Verification: release \`urban-reign-iso-v1\` has all 3 assets byte-exact; re-downloaded part_ac sha256 matches local; parts reassemble to ISO sha256 c22209ee… (also = IA re-downloadable copy). Teardown merged (PR #23); file-structure mapping done locally. rm.
EOF
log "finalize: COMPLETE"
