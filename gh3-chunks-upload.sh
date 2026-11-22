#!/bin/bash
# disk-space-guardian 2026-10-14 ~10:15 EDT run — upload gh3 chunks 01-07 to the
# GitHub release (200MB chunks; the 1.6G single-file uploads kept stalling).
# Chunks verified: cat gh3chunk_* | sha256sum = 44b26bc317816788dcf841150231384e89e8a5e6d4dc28b62cd3db743b2e7811
# (matches carved gh3.bin). gh3chunk_00 already on release, hash-verified.
# Safe: --clobber, no local deletes. Logs to disk-cleanup-log.md.
# DELETION GATE (unchanged): delete .store-staging tar + gh3.bin + gh3split/
# ONLY after all 8 gh3 chunks size-verify on the release.
set -u
STAGE="$HOME/workspace/agent-ops/.store-staging/gh3split"
REPO="mhvnsnt/google-drive-repo"
TAG="cn-gigaleak-work-automigrate-2026-10-14"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
ts() { date -u +%FT%TZ; }

for i in 01 02 03 04 05 06 07; do
  f="$STAGE/gh3chunk_$i"
  [ -f "$f" ] || { echo "$(ts) [guardian] gh3chunk_$i MISSING locally — skipping" >> "$LOG"; continue; }
  sz=$(stat -c%s "$f")
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"gh3chunk_$i\") | .size" 2>/dev/null)
  if [ "$remote_sz" == "$sz" ]; then
    echo "$(ts) [guardian] gh3chunk_$i already on release, size-verified ($sz) — skipping upload" >> "$LOG"
    continue
  fi
  ok=0
  for attempt in 1 2 3 4 5; do
    if timeout 1800 gh release upload "$TAG" "$f" --repo "$REPO" --clobber >/tmp/gh3chunk_$i-up.log 2>&1; then
      ok=1; break
    fi
    echo "$(ts) [guardian] gh3chunk_$i upload attempt $attempt failed, retrying" >> "$LOG"
    sleep $((attempt*20))
  done
  if [ $ok -eq 0 ]; then
    echo "$(ts) [guardian] gh3chunk_$i upload FAILED after 5 attempts — leaving for next run" >> "$LOG"
    exit 1
  fi
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"gh3chunk_$i\") | .size" 2>/dev/null)
  if [ "$remote_sz" == "$sz" ]; then
    echo "$(ts) [guardian] gh3chunk_$i verified on GitHub release ($sz bytes)" >> "$LOG"
  else
    echo "$(ts) [guardian] gh3chunk_$i SIZE MISMATCH local=$sz remote=$remote_sz — leaving for next run" >> "$LOG"
    exit 2
  fi
done
echo "$(ts) [guardian] ALL gh3 chunks 01-07 uploaded + size-verified — gate ready for next run" >> "$LOG"
echo "DONE-gh3-chunks"
