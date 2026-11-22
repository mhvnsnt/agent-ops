#!/bin/bash
# disk-space-guardian 2026-10-14 ~22:10 EDT run — upload staging-ep01-loti tar parts
# (already split at 1000M by a previous run) to GitHub release. Size-verify each
# part via gh api, then delete the local staging dir ONLY after all parts verify.
set -u
STAGE="$HOME/workspace/agent-ops/staging-ep01-loti"
REPO="mhvnsnt/google-drive-repo"
TAG="ep01-loti-staging-2026-10-14"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
ts() { date -u +%FT%TZ; }

gh release create "$TAG" --repo "$REPO" --title "EP01 LOTI-swap staging 2026-10-14" \
  --notes "staging-ep01-loti tar parts (ep01-loti-swap.tar split 1000M). Uploaded by disk-space-guardian 2026-10-14." 2>/dev/null || true

PARTS="part_ab part_ac part_ad part_ae"
for p in $PARTS; do
  f="$STAGE/ep01-loti-swap.tar.$p"
  [ -f "$f" ] || { echo "$(ts) [guardian] $p MISSING locally — skipping" >> "$LOG"; continue; }
  sz=$(stat -c%s "$f")
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"ep01-loti-swap.tar.$p\") | .size" 2>/dev/null)
  if [ "$remote_sz" == "$sz" ]; then
    echo "$(ts) [guardian] $p already on release, size-verified ($sz) — skipping upload" >> "$LOG"
    continue
  fi
  ok=0
  for attempt in 1 2 3 4 5; do
    if timeout 1800 gh release upload "$TAG" "$f" --repo "$REPO" --clobber >/tmp/loti_$p-up.log 2>&1; then
      ok=1; break
    fi
    echo "$(ts) [guardian] $p upload attempt $attempt failed, retrying" >> "$LOG"
    sleep $((attempt*20))
  done
  if [ $ok -eq 0 ]; then
    echo "$(ts) [guardian] $p upload FAILED after 5 attempts — leaving for next run" >> "$LOG"
    exit 1
  fi
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"ep01-loti-swap.tar.$p\") | .size" 2>/dev/null)
  if [ "$remote_sz" == "$sz" ]; then
    echo "$(ts) [guardian] $p verified on GitHub release ($sz bytes)" >> "$LOG"
  else
    echo "$(ts) [guardian] $p SIZE MISMATCH local=$sz remote=$remote_sz — leaving for next run" >> "$LOG"
    exit 2
  fi
done

# final gate: all 4 parts verified -> delete local staging
n=$(gh api "repos/$REPO/releases/tags/$TAG" --jq '[.assets[] | select(.name|test("ep01-loti-swap.tar.part_"))] | length' 2>/dev/null)
if [ "$n" == "4" ]; then
  rm -rf "$STAGE"
  echo "$(ts) [guardian] ALL 4 staging-ep01-loti parts size-verified on release — local staging deleted (3.7G freed)" >> "$LOG"
  echo "DONE-loti-staging"
else
  echo "$(ts) [guardian] only $n/4 parts on release — NOT deleting local" >> "$LOG"
  exit 3
fi
