#!/bin/bash
# guardian-pullback-chain-20261111.sh — disk-space-guardian 2026-11-11 ~14:00 CST
# Sequential pull-back verify + stage-clear for the remaining _repo-staging-20261110/stage items.
# Per item: run its pullback.sh (downloads release parts, sha256 vs release SHA256SUMS, deletes
# downloads as it goes); then verify LOCAL stage parts vs SHA256SUMS; only if BOTH pass,
# log the clear to disk-cleanup-log.md and rm -rf the stage dir + its pullback dir.
# SCOPE: stage dirs ONLY — live source dirs (e.g. _afro-refit-20261110) are NEVER touched by this chain.
# On any failure for an item: log it, skip the delete, continue to the next item.
# Logging uses shell builtins (echo >>) — child-process file writes flicker with
# "Operation not permitted" under the quota wall (TOOLS.md 2026-11-11 ~13:50 CT).
set -u
STAGE=/home/hatch/workspace/_repo-staging-20261110/stage
LOG=/home/hatch/workspace/agent-ops/disk-cleanup-log.md
CHAINLOG=/home/hatch/workspace/agent-ops/guardian-pullback-chain-20261111.log
# name:tag:tarsha (tar sha256 from each item's MANIFEST)
ITEMS="gnmcomposite-20261109:gnmcomposite-20261109-20261110
v3face-pull-20261110:v3face-pull-20261110-20261110
afro-v2-proof:afro-v2-proof-20261110
adri-lifecut-v1:adri-lifecut-v1-20261110
roster-wireup-20261109:roster-wireup-20261109-20261110
collision-20261109:collision-20261109-20261110
gnmface-20261109:gnmface-20261109-20261110"
echo "CHAIN START $(date -u +%FT%TZ) df: $(df -h /home/hatch | tail -1)" >> "$CHAINLOG"
echo "$ITEMS" | while IFS=: read -r NAME TAG; do
  [ -n "$NAME" ] || continue
  echo "ITEM $NAME tag=$TAG start $(date -u +%T)" >> "$CHAINLOG"
  if [ ! -d "$STAGE/$NAME" ]; then echo "ITEM $NAME SKIP already-gone" >> "$CHAINLOG"; continue; fi
  # 1. release-side pull-back (idempotent; writes pullback.done on success)
  bash "$STAGE/${NAME}-pullback/pullback.sh" >> "$CHAINLOG" 2>&1
  if [ ! -f "$STAGE/${NAME}-pullback/pullback.done" ]; then
    echo "ITEM $NAME FAIL pullback not verified — NOT cleared" >> "$CHAINLOG"
    continue
  fi
  # 2. local-side sha check of the stage parts
  if ! (cd "$STAGE/$NAME" && sha256sum -c "SHA256SUMS-${NAME}.txt" >> "$CHAINLOG" 2>&1); then
    echo "ITEM $NAME FAIL local sha mismatch — NOT cleared" >> "$CHAINLOG"
    continue
  fi
  # 3. record + clear (stage dir + pullback dir only)
  BYTES=$(du -sb "$STAGE/$NAME" | cut -f1)
  TARSHA=$(grep -m1 '^- Tar:' "$STAGE/$NAME/MANIFEST-${NAME}.md" 2>/dev/null | grep -oE '[0-9a-f]{64}' | head -1)
  echo "- CLEARED $NAME stage (guardian-pullback-chain 2026-11-11): freed ${BYTES} B (stage tar, pull-back verified both sides vs SHA256SUMS). Backup: https://github.com/mhvnsnt/clouddog-storage/releases/tag/$TAG . Tar sha256: ${TARSHA:-see MANIFEST}. Live source dir NOT touched by this chain." >> "$LOG"
  rm -rf "$STAGE/$NAME" "$STAGE/${NAME}-pullback"
  echo "ITEM $NAME CLEARED freed=${BYTES}B df: $(df -h /home/hatch | tail -1)" >> "$CHAINLOG"
done
echo "CHAIN END $(date -u +%FT%TZ) df: $(df -h /home/hatch | tail -1)" >> "$CHAINLOG"
