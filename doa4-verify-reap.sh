#!/bin/bash
# doa4-extracted verify+reap — ONE-STORE RULE lane for ~/workspace/doa4-bass/extracted/ (3.0G)
# Verifies the 6 release parts on mhvnsnt/western-heart@doa4-mirror-20261017 are
# byte-identical to a fresh re-stream of the local tree (per-part sha256, one part
# on disk at a time, delete-as-you-go). On full match: queue-log, delete, log.
# NEVER holds more than one 500M part (~0.5% disk). Aborts safe on any mismatch.
set -u
SRC="$HOME/workspace/doa4-bass/extracted"
WORK="$HOME/workspace/agent-ops/doa4-verify"
PARTS="$WORK/parts"
LOG="$WORK/verify.log"
RESULT="$WORK/RESULT.txt"
REPO="mhvnsnt/western-heart"
TAG="doa4-mirror-20261017"
PREFIX="doa4-mirror-extracted-20261017.tar"
CHUNK=524288000
mkdir -p "$PARTS"
exec >>"$LOG" 2>&1
echo "=== doa4-extracted verify+reap started $(date -u '+%F %T UTC') ==="
fail() { echo "ABORT: $1"; echo "ABORT: $1" > "$RESULT"; exit 1; }

[ -d "$SRC" ] || fail "source dir missing: $SRC"

# Gate 0: no file under extracted/ newer than the original tar creation (~13:00 CDT 2026-10-17).
# If anything changed, a re-stream would differ -> verification meaningless -> abort.
if find "$SRC" -newermt "2026-10-17 13:05:00 -0500" -print -quit 2>/dev/null | grep -q .; then
  fail "files under extracted/ modified after original tar creation; re-stream would differ"
fi
echo "Gate 0 OK: tree untouched since original tar"

# Gate 1: no live process working inside doa4-bass
if ls -l /proc/[0-9]*/cwd 2>/dev/null | grep -q 'doa4-bass'; then
  fail "live process has cwd inside doa4-bass"
fi
echo "Gate 1 OK: no live process in doa4-bass"

# Step 1: re-stream tar locally, sha256 each 500M chunk (never stored)
echo "Step 1: re-streaming tar and hashing chunks..."
tar -cf - -C "$HOME/workspace/doa4-bass" extracted 2>/dev/null | python3 -c "
import sys, hashlib
i = 0
while True:
    data = sys.stdin.buffer.read($CHUNK)
    if not data: break
    open('$WORK/chunk-' + str(i) + '.sha256','w').write(hashlib.sha256(data).hexdigest() + '  chunk-' + str(i) + chr(10))
    print('chunk', i, 'bytes', len(data), 'sha256', hashlib.sha256(data).hexdigest(), flush=True)
    i += 1
print('TOTAL_CHUNKS', i)
" || fail "tar re-stream failed"
NCHUNKS=$(ls "$WORK"/chunk-*.sha256 2>/dev/null | wc -l)
[ "$NCHUNKS" = "6" ] || fail "expected 6 chunks, got $NCHUNKS"
echo "Step 1 OK: 6 local chunk hashes recorded"

# Step 2: download each release part (one at a time), hash, compare, delete
for i in 0 1 2 3 4 5; do
  name="${PREFIX}.part-0${i}"
  echo "Step 2: downloading $name ..."
  gh release download "$TAG" -R "$REPO" -p "$name" -D "$PARTS" --clobber \
    || fail "download failed for $name"
  got=$(sha256sum "$PARTS/$name" | awk '{print $1}')
  want=$(awk '{print $1}' "$WORK/chunk-$i.sha256")
  echo "  part-$i downloaded sha256=$got"
  echo "  part-$i local      sha256=$want"
  rm -f "$PARTS/$name"
  [ "$got" = "$want" ] || fail "HASH MISMATCH on part-0$i (downloaded != local re-stream)"
  echo "  part-0$i MATCH, deleted local copy"
done
echo "Step 2 OK: all 6 parts byte-identical"

# Gate 2 (re-check right before delete): still no live process, still untouched
if ls -l /proc/[0-9]*/cwd 2>/dev/null | grep -q 'doa4-bass'; then
  fail "live process entered doa4-bass during verification; NOT deleting"
fi
if find "$SRC" -newermt "2026-10-17 13:05:00 -0500" -print -quit 2>/dev/null | grep -q .; then
  fail "tree modified during verification; NOT deleting"
fi

# Step 3: ONE-STORE RULE condition 3 — log continuation to TEARDOWN-IDLE-QUEUE BEFORE deleting
cat >> "$HOME/workspace/agent-ops/TEARDOWN-IDLE-QUEUE.md" <<'EOF'

## 2026-10-17 — DOA4 extracted/ source cleared per ONE-STORE RULE (disk-space-guardian)
- `~/workspace/doa4-bass/extracted/` (3.0G) verified BYTE-IDENTICAL on GitHub
  (mhvnsnt/western-heart release doa4-mirror-20261017, 6 parts, per-part sha256 match)
  and cleared from local disk. Pull-back:
  `gh release download doa4-mirror-20261017 -R mhvnsnt/western-heart -p 'doa4-mirror-extracted-20261017.tar.part-*'`
  then `cat doa4-mirror-extracted-20261017.tar.part-* | tar -xf -`.
- Teardown NOT 100% per TEARDOWN-COMPLETION LAW — remaining: 6 encrypted AFS archives
  (chrone/chrtwo/chrthree/anm/mot/stg, 2.4GB) need header keystream algorithm
  (see western-heart/teardown/dead-or-alive-4/ENCRYPTION-ANALYSIS.md; S-box at 0x822f06d0).
  Xenia memory dump or full RE still pending. Resume in idle time.
EOF
echo "Step 3 OK: TEARDOWN-IDLE-QUEUE entry written"

# Step 4: delete + log
SIZE=$(du -sh "$SRC" | cut -f1)
rm -rf "$SRC"
echo "DELETED $SRC ($SIZE)"
DF=$(df -h /home/hatch | tail -1 | awk '{print $5}')
cat >> "$HOME/workspace/agent-ops/disk-cleanup-log.md" <<EOF
- [$(date '+%F %T %Z')] ONE-STORE-RULE REAP doa4-bass/extracted/ ($SIZE) — byte-identical on github:mhvnsnt/western-heart@doa4-mirror-20261017 (6/6 parts sha256-verified vs local re-stream); no active teardown work; continuation logged to TEARDOWN-IDLE-QUEUE.md. Pull-back: gh release download $TAG -R $REPO -p '${PREFIX}.part-*'. Disk now $DF.
EOF
echo "DONE: deleted $SRC, disk $DF"
echo "DONE $(date -u '+%F %T UTC') disk=$DF" > "$RESULT"
