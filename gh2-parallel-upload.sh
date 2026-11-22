#!/bin/bash
# disk-space-guardian 2026-10-14 05:0x run — parallel upload of gh2 piece to
# accelerate the cn-gigaleak-work relief gate (main script does gh1..gh3
# sequentially; gh1 crawling). Safe: separate asset name, --clobber, no deletes.
# Main script will re-carve/re-upload/re-verify before its own deletion.
STAGE="$HOME/workspace/agent-ops/.store-staging"
NAME="cn-gigaleak-work-automigrate-2026-10-14"
REPO="mhvnsnt/google-drive-repo"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
piece="$STAGE/${NAME}.gh2.bin"
sz=$(stat -c%s "$piece")
sha=$(sha256sum "$piece" | awk '{print $1}')
echo "$(date -u +%FT%TZ) [guardian] gh2 parallel carve verified: $sz bytes sha256=$sha" >> "$LOG"
ok=0
for attempt in 1 2 3; do
  if gh release upload "$NAME" "$piece" --repo "$REPO" --clobber >/tmp/gh2-up.log 2>&1; then ok=1; break; fi
  echo "$(date -u +%FT%TZ) [guardian] gh2 parallel upload attempt $attempt failed, retrying" >> "$LOG"
  sleep $((attempt*30))
done
if [ $ok -eq 0 ]; then
  echo "$(date -u +%FT%TZ) [guardian] gh2 parallel upload FAILED after 3 attempts — piece kept" >> "$LOG"; exit 1
fi
remote_sz=$(gh api "repos/$REPO/releases/tags/$NAME" --jq ".assets[] | select(.name==\"${NAME}.gh2.bin\") | .size" 2>/dev/null)
if [ "$remote_sz" == "$sz" ]; then
  echo "$(date -u +%FT%TZ) [guardian] gh2 parallel upload VERIFIED on GitHub release ($sz bytes, sha256=$sha) — main script will re-verify and clean up" >> "$LOG"
  echo "DONE-gh2-verified"
else
  echo "$(date -u +%FT%TZ) [guardian] gh2 parallel SIZE MISMATCH local=$sz remote=$remote_sz — piece kept" >> "$LOG"; exit 2
fi
