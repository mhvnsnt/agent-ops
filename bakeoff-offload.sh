#!/bin/bash
# Guardian DELETE-AS-YOU-GO: upload remaining bakeoff blends to the lane's own
# release (mhvnsnt/cape-jones weight-bakeoff-20261017), verify name+size via the
# API, then delete local. One file at a time so disk falls DURING the upload.
set -u
REPO="mhvnsnt/cape-jones"
TAG="weight-bakeoff-20261017"
DIR="$HOME/workspace/weight-bakeoff-scratch/blends"
LOG="$HOME/workspace/agent-ops/bakeoff-offload.log"
FILES="W8.blend W7.blend W3.blend W2.blend W7b.blend"  # small first
{
echo "=== bakeoff offload started $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
for f in $FILES; do
  p="$DIR/$f"
  [ -f "$p" ] || { echo "SKIP (missing): $f"; continue; }
  sz=$(stat -c %s "$p")
  echo "upload: $f ($sz bytes)..."
  if ! gh release upload "$TAG" "$p" --repo "$REPO" >>"$LOG" 2>&1; then
    echo "UPLOAD FAIL: $f (leaving local, continuing)"; continue
  fi
  rsz=$(gh release view "$TAG" --repo "$REPO" --json assets -q ".assets[] | select(.name==\"$f\") | .size" 2>/dev/null)
  if [ "$rsz" = "$sz" ]; then
    rm -f "$p"
    echo "VERIFIED+DELETED: $f ($sz bytes) -> $REPO releases/$TAG"
  else
    echo "VERIFY FAIL: $f local=$sz remote=${rsz:-none} (leaving local)"
  fi
done
echo "=== bakeoff offload ended $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
} >>"$LOG" 2>&1
