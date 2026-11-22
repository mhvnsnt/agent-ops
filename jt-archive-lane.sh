#!/bin/bash
# jt-parody-work offload lane (disk-space-guardian 2026-10-18).
# Splits ~/workspace/jt-parody-work into 100M tar chunks, uploads each to
# mhvnsnt/johnny-test-parody release guardian-jt-archive-20261018,
# verifies byte-exact via gh api, then deletes the local chunk (DELETE-AS-YOU-GO).
# Resumable: skips chunks already present on the release with matching size.
# Progress manifest: ~/workspace/agent-ops/jt-archive-manifest.json (SACRED - never delete).
set -u
REPO="mhvnsnt/johnny-test-parody"
TAG="guardian-jt-archive-20261018"
SRC="$HOME/workspace/jt-parody-work"
WORK="$HOME/workspace/agent-ops/jt-archive"
MANIFEST="$HOME/workspace/agent-ops/jt-archive-manifest.json"
mkdir -p "$WORK"
LOG="$WORK/lane.log"

log(){ echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }

cd "$SRC" || exit 1

# Phase 1: tar + split (idempotent — skip if chunks already exist)
if ! ls "$WORK"/jt-tree.tar.100m-* >/dev/null 2>&1; then
  log "creating tar split..."
  tar -cf - . | split -b 100M - "$WORK/jt-tree.tar.100m-"
  log "tar split done: $(ls "$WORK"/jt-tree.tar.100m-* | wc -l) chunks"
fi

# Phase 2: upload each chunk with verify + delete-as-you-go
for f in "$WORK"/jt-tree.tar.100m-*; do
  [ -f "$f" ] || continue
  name="$(basename "$f")"
  size="$(stat -c %s "$f")"
  sha="$(sha256sum "$f" | cut -d' ' -f1)"

  # Skip if already on release with matching size
  remote_size="$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"$name\") | .size" 2>/dev/null | head -1)"
  if [ -n "$remote_size" ]; then
    if [ "$remote_size" = "$size" ]; then
      log "$name already on release (size $size OK) - deleting local"
      rm -f "$f"
      continue
    else
      log "WARN $name size mismatch remote=$remote_size local=$size - re-uploading"
    fi
  fi

  # Upload with retries
  attempt=0
  while [ $attempt -lt 4 ]; do
    attempt=$((attempt+1))
    if gh release upload "$TAG" "$f" --repo "$REPO" --clobber >/dev/null 2>&1; then
      break
    fi
    log "$name upload attempt $attempt failed - backing off"
    sleep $((attempt*30))
  done

  # Verify byte-exact, then delete local
  rsize="$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"$name\") | .size" 2>/dev/null | head -1)"
  if [ "$rsize" = "$size" ]; then
    log "$name VERIFIED ($size bytes, sha256 $sha) - deleting local chunk"
    rm -f "$f"
    # Sacred progress manifest entry
    python3 - "$MANIFEST" "$name" "$size" "$sha" <<'PYEOF'
import json,sys,os
mp, nm, sz, sh = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
d = {"source": os.path.expanduser("~/workspace/jt-parody-work"), "release": "mhvnsnt/johnny-test-parody@guardian-jt-archive-20261018", "chunks": {}}
if os.path.exists(mp):
    d = json.load(open(mp))
d["chunks"][nm] = {"size": sz, "sha256": sh}
json.dump(d, open(mp,"w"), indent=1)
PYEOF
  else
    log "ERROR $name verify failed (local=$size remote=${rsize:-missing}) - leaving local, will retry next pass"
  fi
done

remaining=$(ls "$WORK"/jt-tree.tar.100m-* 2>/dev/null | wc -l)
log "lane pass complete. remaining chunks: $remaining"
if [ "$remaining" -eq 0 ]; then
  total=$(gh api "repos/$REPO/releases/tags/$TAG" --jq '[.assets[].size] | add' 2>/dev/null)
  log "ALL CHUNKS UPLOADED. release total bytes: $total"
  log "NEXT: verify SHA256SUMS, then guardian may clear $SRC per ONE-STORE RULE (log pull-back first)"
fi
