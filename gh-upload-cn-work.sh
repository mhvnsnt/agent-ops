#!/bin/bash
# disk-space-guardian 2026-10-14 03:01 run — upload remaining 46 chunks of
# cn-gigaleak-work-automigrate-2026-10-14.tar to GitHub release (Drive full).
# Bytes [5242880000, 10160814080) split into 3 x 1639311360-byte pieces.
set -u
STAGE="$HOME/workspace/agent-ops/.store-staging"
TAR="$STAGE/store_cn-gigaleak-work-automigrate-2026-10-14.tar"
NAME="cn-gigaleak-work-automigrate-2026-10-14"
REPO="mhvnsnt/google-drive-repo"
TAG="$NAME"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
PIECE_BYTES=1639311360
SKIPS="5242880000 6882191360 8521502720"
i=0
for skip in $SKIPS; do
  i=$((i+1))
  piece="$STAGE/${NAME}.gh${i}.bin"
  dd if="$TAR" of="$piece" bs=1M iflag=skip_bytes,count_bytes skip="$skip" count="$PIECE_BYTES" status=none
  sz=$(stat -c%s "$piece")
  sha=$(sha256sum "$piece" | awk '{print $1}')
  echo "$(date -u +%FT%TZ) [guardian] piece gh$i carved: $sz bytes sha256=$sha (tar offset $skip)" >> "$LOG"
  if [ "$sz" != "$PIECE_BYTES" ]; then
    echo "$(date -u +%FT%TZ) [guardian] gh$i CARVE SIZE WRONG: $sz != $PIECE_BYTES" >> "$LOG"; exit 1
  fi
  ok=0
  for attempt in 1 2 3 4 5; do
    out=$(gh release upload "$TAG" "$piece" --repo "$REPO" --clobber 2>&1)
    rc=$?
    echo "$out" | tail -2
    if [ $rc -eq 0 ]; then ok=1; break; fi
    echo "$(date -u +%FT%TZ) [guardian] gh$i upload attempt $attempt failed (rc=$rc), retrying" >> "$LOG"
    sleep $((attempt*20))
  done
  if [ $ok -eq 0 ]; then
    echo "$(date -u +%FT%TZ) [guardian] gh$i FAILED after 5 attempts — piece kept at $piece" >> "$LOG"; exit 1
  fi
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"${NAME}.gh${i}.bin\") | .size" 2>/dev/null)
  if [ "$remote_sz" != "$sz" ]; then
    echo "$(date -u +%FT%TZ) [guardian] gh$i SIZE MISMATCH local=$sz remote=$remote_sz — piece kept" >> "$LOG"; exit 2
  fi
  echo "$(date -u +%FT%TZ) [guardian] gh$i verified on GitHub release ($sz bytes, sha256=$sha)" >> "$LOG"
  rm -f "$piece"
done
echo "$(date -u +%FT%TZ) [guardian] all 3 GitHub pieces uploaded and size-verified" >> "$LOG"
echo "DONE-ALL-3-PIECES"
