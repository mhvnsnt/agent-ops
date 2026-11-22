#!/bin/bash
# disk-space-guardian 2026-10-14 run — upload ep01-loti-swap tar parts to GitHub release.
# Drive chunked upload path died twice (0 chunks uploaded); GitHub release path is proven.
REPO="mhvnsnt/google-drive-repo"
TAG="ep01-loti-staging-2026-10-14"
STAGE="$HOME/workspace/agent-ops/.store-staging"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
ts() { date -u +%FT%TZ; }

for p in aa ab ac ad ae; do
  f="$STAGE/loti-stage-part_$p"
  [ -f "$f" ] || { echo "$(ts) [guardian] part_$p MISSING locally" >> "$LOG"; exit 3; }
  sz=$(stat -c%s "$f")
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"loti-stage-part_$p\") | .size" 2>/dev/null)
  if [ "$remote_sz" == "$sz" ]; then
    echo "$(ts) [guardian] loti-stage-part_$p already on release, size-verified — skipping" >> "$LOG"
    continue
  fi
  ok=0
  for attempt in 1 2 3 4 5; do
    if timeout 1800 gh release upload "$TAG" "$f" --repo "$REPO" --clobber >>/tmp/loti_stage_$p.log 2>&1; then ok=1; break; fi
    echo "$(ts) [guardian] loti-stage-part_$p upload attempt $attempt failed, retrying" >> "$LOG"
    sleep $((attempt*20))
  done
  if [ $ok -eq 0 ]; then
    echo "$(ts) [guardian] loti-stage-part_$p FAILED after 5 attempts — leaving for next run" >> "$LOG"
    exit 1
  fi
  remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"loti-stage-part_$p\") | .size" 2>/dev/null)
  if [ "$remote_sz" == "$sz" ]; then
    echo "$(ts) [guardian] loti-stage-part_$p size-verified on GitHub release ($sz bytes)" >> "$LOG"
  else
    echo "$(ts) [guardian] loti-stage-part_$p SIZE MISMATCH local=$sz remote=$remote_sz" >> "$LOG"
    exit 2
  fi
done

n=$(gh api "repos/$REPO/releases/tags/$TAG" --jq '[.assets[] | select(.name|test("loti-stage-part_"))] | length' 2>/dev/null)
if [ "$n" == "5" ]; then
  echo "$(ts) [guardian] ALL 5 loti-stage parts verified on release $TAG" >> "$LOG"
  echo "ALL_PARTS_DONE"
else
  echo "$(ts) [guardian] only $n/5 parts on release — NOT deleting local" >> "$LOG"
  exit 4
fi
