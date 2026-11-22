#!/bin/bash
# disk-space-guardian 2026-10-14 run — upload wg-video-intermediates chunks 00-06
# to the (empty) GitHub release, 200MB chunks; per-chunk verify + DELETE local
# chunk to keep disk flat (the 1.31G single-file uploads kept stalling).
# tar sha256: e633930902ffc74d8473c8582bd588e6c84977cd0ceb4968673d9a260b6a31f2
# After ALL 7 chunks size+digest-verify: DELETE the staging tar
# gh_wg-video-intermediates.tar as well. Safe: --clobber, no other local deletes.
# Logs to disk-cleanup-log.md.
set -u
STAGE="$HOME/workspace/agent-ops/.store-staging/wgsplit"
TAR="$HOME/workspace/agent-ops/.store-staging/gh_wg-video-intermediates.tar"
REPO="mhvnsnt/google-drive-repo"
TAG="wg-video-intermediates-automigrate-2026-10-14"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
ts() { date -u +%FT%TZ; }

for i in 00 01 02 03 04 05 06; do
  f="$STAGE/wgchunk_$i"
  [ -f "$f" ] || { echo "$(ts) [guardian] wgchunk_$i MISSING locally — skipping" >> "$LOG"; continue; }
  sz=$(stat -c%s "$f")
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"wgchunk_$i\") | .size" 2>/dev/null)
  if [ "$remote_sz" == "$sz" ]; then
    echo "$(ts) [guardian] wgchunk_$i already on release, size-verified ($sz) — deleting local chunk" >> "$LOG"
    rm -f "$f" && echo "$(ts) [guardian] wgchunk_$i local deleted" >> "$LOG"
    continue
  fi
  ok=0
  for attempt in 1 2 3 4 5; do
    if timeout 1800 gh release upload "$TAG" "$f" --repo "$REPO" --clobber >/tmp/wgchunk_$i-up.log 2>&1; then
      ok=1; break
    fi
    echo "$(ts) [guardian] wgchunk_$i upload attempt $attempt failed, retrying" >> "$LOG"
    sleep $((attempt*20))
  done
  if [ $ok -eq 0 ]; then
    echo "$(ts) [guardian] wgchunk_$i upload FAILED after 5 attempts — leaving for next run" >> "$LOG"
    exit 1
  fi
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"wgchunk_$i\") | .size" 2>/dev/null)
  local_dig=$(sha256sum "$f" | cut -d' ' -f1)
  remote_dig=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"wgchunk_$i\") | .digest" 2>/dev/null | sed 's/^sha256://')
  if [ "$remote_sz" == "$sz" ] && [ "$remote_dig" == "$local_dig" ]; then
    echo "$(ts) [guardian] wgchunk_$i verified on GitHub release ($sz bytes, digest ✓) — deleting local chunk" >> "$LOG"
    rm -f "$f"
  else
    echo "$(ts) [guardian] wgchunk_$i VERIFY FAIL local=$sz remote=$remote_sz — leaving for next run" >> "$LOG"
    exit 2
  fi
done
# All chunks verified: delete the staging tar too (content fully on release).
remaining=$(ls "$STAGE"/wgchunk_* 2>/dev/null | wc -l)
if [ "$remaining" -eq 0 ] && [ -f "$TAR" ]; then
  rm -f "$TAR"
  echo "$(ts) [guardian] ALL wg chunks 00-06 uploaded + size-verified; staging tar deleted — 2.6G total relief" >> "$LOG"
fi
echo "DONE-wg-chunks"
