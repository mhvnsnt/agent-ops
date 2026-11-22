#!/bin/bash
# mirror-one.sh <item-filename> — split, upload, verify, delete-local.
# Works ONLY inside /home/hatch/workspace/meshrepair-scratch/
set -u
SCRATCH=/home/hatch/workspace/meshrepair-scratch
REPO=mhvnsnt/clouddog-storage
TAG=scratch-mirror-20261020
LOG=/home/hatch/workspace/agent-ops/disk-cleanup-log.md

cd "$SCRATCH" || { echo "FATAL: cannot cd to $SCRATCH"; exit 1; }
ITEM="$1"
[ -f "$ITEM" ] || { echo "FATAL: $ITEM is not a file"; exit 1; }

SIZE=$(stat -c %s "$ITEM")
echo "=== ITEM $ITEM size=$SIZE ==="

split -b 100M "$ITEM" "$ITEM.part-" || { echo "FATAL: split failed for $ITEM"; exit 1; }
PARTS=$(ls "$ITEM.part-"* 2>/dev/null)
N=$(echo "$PARTS" | wc -l)
echo "split into $N parts"

fail=0
for P in $PARTS; do
  PSIZE=$(stat -c %s "$P")
  OK=0
  for ATT in 1 2 3; do
    echo "--- uploading $P (attempt $ATT) ---"
    if gh release upload "$TAG" "$P" --repo "$REPO" --clobber; then
      RSIZE=$(gh api "repos/$REPO/releases/tags/$TAG" --jq '.assets[] | [.name, .size] | @tsv' 2>/dev/null | awk -F'\t' -v n="$P" '$1==n {print $2}')
      echo "local=$PSIZE remote=$RSIZE"
      if [ "$RSIZE" = "$PSIZE" ]; then
        echo "VERIFIED $P ($PSIZE bytes)"
        OK=1
        break
      else
        echo "SIZE MISMATCH for $P (local $PSIZE vs remote $RSIZE) — re-uploading"
      fi
    else
      echo "UPLOAD FAILED for $P attempt $ATT"
    fi
    [ "$ATT" = "1" ] && sleep 30
    [ "$ATT" = "2" ] && sleep 90
  done
  if [ "$OK" = "1" ]; then
    rm -f "$P" && echo "DELETED local part $P"
  else
    echo "FAILED: $P could not verify after 3 attempts — LEAVING LOCAL"
    fail=1
  fi
done

if [ "$fail" = "0" ]; then
  echo "ALL PARTS VERIFIED for $ITEM — deleting original $SIZE bytes"
  rm -f "$ITEM" && echo "DELETED original $ITEM"
  echo "2026-10-20: mirrored $ITEM ($SIZE bytes, $N parts: $(echo $PARTS | tr ' ' ',')) to mhvnsnt/clouddog-storage release scratch-mirror-20261020; deleted local $ITEM. Pull-back: gh release download scratch-mirror-20261020 --repo mhvnsnt/clouddog-storage --pattern '$ITEM.part-*' --dir <dest> && cat $ITEM.part-* > $ITEM" >> "$LOG"
else
  echo "SOME PARTS FAILED for $ITEM — original $ITEM LEFT IN PLACE"
  echo "2026-10-20: mirror of $ITEM FAILED part verification; original left in place. See run log." >> "$LOG"
  exit 2
fi
