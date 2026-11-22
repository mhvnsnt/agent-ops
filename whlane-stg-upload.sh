#!/bin/bash
# whlane-stg-upload.sh — finish the stalled CloudDog mirror of
# whwork-creation-suite-playable-20261020.tar parts (aa..ay) into draft release
# 418094497 on mhvnsnt/clouddog-storage. Verify-then-delete per part.
# Started 2026-10-21 by the Wizard Gang side-chat disk cleanup turn.
set -u
DIR="$HOME/workspace/.whlane-stg-creation-suite-playable"
RID=418094497
REPO=mhvnsnt/clouddog-storage
LOG="$HOME/workspace/agent-ops/whlane-stg-upload.log"
CLEANLOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"

log(){ echo "[$(date '+%F %T %Z')] $*" >> "$LOG"; }

for f in "$DIR"/whwork-creation-suite-playable-20261020.tar.part-*; do
  [ -f "$f" ] || continue
  name=$(basename "$f")
  local_sha=$(sha256sum "$f" | cut -d' ' -f1)
  local_size=$(stat -c%s "$f")
  remote=$(gh api "repos/$REPO/releases/$RID/assets?per_page=100" --jq ".[] | select(.name==\"$name\") | \"\(.size) \(.digest)\"" 2>/dev/null)
  if [ -n "$remote" ]; then
    rsize=$(echo "$remote" | cut -d' ' -f1)
    rdigest=$(echo "$remote" | cut -d' ' -f2)
    if [ "$rsize" = "$local_size" ] && [ "$rdigest" = "sha256:$local_sha" ]; then
      rm -f "$f"
      log "VERIFIED-EXISTING $name size=$local_size sha=$local_sha -> local deleted"
      echo "- $(date '+%F %T %Z') whlane-stg clear: $name ($local_size B) already verified on clouddog-storage draft release whwork-creation-suite-playable-20261020 (digest matched local sha256) -> local part deleted. Pull-back: gh api repos/$REPO/releases/$RID/assets + download. [side-chat cleanup lane]" >> "$CLEANLOG"
      continue
    else
      log "MISMATCH $name local=$local_size/$local_sha remote=$remote -> KEPT"
      continue
    fi
  fi
  log "UPLOADING $name size=$local_size sha=$local_sha"
  if gh api "https://uploads.github.com/repos/$REPO/releases/$RID/assets?name=$name" -X POST -H "Content-Type: application/octet-stream" --input "$f" > /dev/null 2>>"$LOG"; then
    remote=$(gh api "repos/$REPO/releases/$RID/assets?per_page=100" --jq ".[] | select(.name==\"$name\") | \"\(.size) \(.digest)\"" 2>/dev/null)
    rsize=$(echo "$remote" | cut -d' ' -f1)
    rdigest=$(echo "$remote" | cut -d' ' -f2)
    if [ "$rsize" = "$local_size" ] && [ "$rdigest" = "sha256:$local_sha" ]; then
      rm -f "$f"
      log "UPLOADED+VERIFIED $name -> local deleted"
      echo "- $(date '+%F %T %Z') whlane-stg clear: $name ($local_size B) uploaded to clouddog-storage draft release whwork-creation-suite-playable-20261020, API digest verified == local sha256 -> local part deleted. Pull-back: gh release download whwork-creation-suite-playable-20261020 -R $REPO (draft) or assets API on release $RID. [side-chat cleanup lane]" >> "$CLEANLOG"
    else
      log "POST-UPLOAD VERIFY FAILED $name remote=$remote -> KEPT"
    fi
  else
    log "UPLOAD FAILED $name -> KEPT, will not retry in this run"
  fi
done
log "RUN COMPLETE. Remaining local parts: $(ls "$DIR" 2>/dev/null | wc -l)"
df -h /home/hatch | tail -1 >> "$LOG"
