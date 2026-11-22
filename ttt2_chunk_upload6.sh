#!/bin/bash
# TTT2 chunk upload resume — chunks 16-26, 500MB each
# Extract one chunk at a time with dd, upload via gh, verify size, delete local.
# Stored in workspace (survives /tmp wipes from daemon restarts).
set -u
cd ~/workspace/game-reverse-engineering/tekken-tag-tournament-2/
SRC="Tekken Tag Tournament 2.7z"
REPO="mhvnsnt/western-heart"
TAG="ttt2-7z-v1"
LOG="ttt2-chunk-upload.log"
FULL=524288000

log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }

remote_size() {
  gh release view "$TAG" --repo "$REPO" --json assets \
    -q ".assets[] | select(.name==\"$1\") | .size" 2>/dev/null
}

upload_chunk() {
  local f="$1" expected="$2"
  local attempt=0
  while [ $attempt -lt 5 ]; do
    attempt=$((attempt+1))
    log "Uploading $f ($expected bytes) — attempt $attempt/5"
    if gh release upload "$TAG" "$f" --repo "$REPO" --clobber >>"$LOG" 2>&1; then
      local rs
      rs=$(remote_size "$f")
      if [ "$rs" = "$expected" ]; then
        log "VERIFIED $f ($rs bytes), deleting local"
        rm -f "$f"
        return 0
      fi
      log "Upload seemed OK but size mismatch: local=$expected remote=$rs — retrying"
    else
      log "gh release upload failed (attempt $attempt) — retrying"
    fi
    sleep 10
  done
  log "FAILED $f after 5 attempts — aborting"
  return 1
}

for n in $(seq 16 26); do
  nn=$(printf "%02d" $n)
  f="ttt2-500m.part_$nn"
  if [ "$n" -lt 26 ]; then
    count=500
    expected=$FULL
  else
    count=245
    expected=256424393
  fi
  # skip if already verified on release
  rs=$(remote_size "$f")
  if [ "$rs" = "$expected" ]; then
    log "$f already verified on release ($rs) — skipping"
    rm -f "$f"
    continue
  fi
  # reuse local chunk if it exists with correct size
  if [ -f "$f" ]; then
    sz=$(stat -c%s "$f")
    if [ "$sz" = "$expected" ]; then
      log "Reusing existing local $f ($sz bytes)"
    else
      log "Local $f wrong size ($sz) — re-extracting"
      rm -f "$f"
    fi
  fi
  if [ ! -f "$f" ]; then
    skip=$(( (n-1)*500 ))
    log "Extracting chunk $n/26: $f (skip=${skip}M count=${count}M)"
    dd if="$SRC" of="$f" bs=1M skip="$skip" count="$count" status=none 2>>"$LOG"
    sz=$(stat -c%s "$f")
    if [ "$sz" != "$expected" ]; then
      log "ERROR: extracted $f size $sz != expected $expected — aborting"
      exit 1
    fi
  fi
  upload_chunk "$f" "$expected" || exit 1
done

log "ALL 26 CHUNKS VERIFIED ON RELEASE"
