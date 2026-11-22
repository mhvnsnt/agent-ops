#!/bin/bash
# disk-space-guardian 2026-10-14 — upload EP01 finished master to GitHub release
# in 200MB chunks. DIGEST GATE (not just size): for each chunk, upload, then
# download the release asset back and sha256-compare to the local chunk. Only
# then is the local chunk deleted and its digest recorded.
#
# MASTER DELETION GATE: local master is deleted ONLY after ALL 12 chunks pass
# download-back digest verification (recorded in CHUNK-DIGESTS.txt). Since the
# chunks were carved as an exact partition of the master (concat sha256 ==
# MASTER-SHA256.txt, verified at carve time), 12/12 digest-verified chunks ==
# byte-exact master on the release.
#
# Safe: --clobber, no other deletes. Chunk list is fixed 00..11.
set -u
STAGE="$HOME/workspace/agent-ops/.store-staging/ep01fixedsplit"
REPO="mhvnsnt/google-drive-repo"
TAG="ep01-fixed-master-2026-10-14"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
DIGESTS="$STAGE/CHUNK-DIGESTS.txt"
ts() { date -u +%FT%TZ; }

verify_chunk() { # $1 = chunk index (00..11)
  local i="$1" f="$STAGE/ep01fchunk_$i" remote_sz remote_dig
  [ -f "$f" ] || { echo "$(ts) [guardian] ep01fchunk_$i missing locally — checking release state"; }
  if [ -f "$f" ]; then
    local sz local_dig
    sz=$(stat -c%s "$f")
    local_dig=$(sha256sum "$f" | awk '{print $1}')
    remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"ep01fchunk_$i\") | .size" 2>/dev/null)
    if [ "$remote_sz" == "$sz" ]; then
      # size match — do digest verify by downloading back
      echo "$(ts) [guardian] ep01fchunk_$i size-verified ($sz), downloading back for digest check" >> "$LOG"
      if gh release download "$TAG" --repo "$REPO" -p "ep01fchunk_$i" --clobber -O "/tmp/ep01fchunk_$i.verify" >/dev/null 2>&1; then
        remote_dig=$(sha256sum "/tmp/ep01fchunk_$i.verify" | awk '{print $1}')
        rm -f "/tmp/ep01fchunk_$i.verify"
        if [ "$remote_dig" == "$local_dig" ]; then
          echo "$(ts) [guardian] ep01fchunk_$i DIGEST-VERIFIED ($local_dig) — deleting local chunk" >> "$LOG"
          echo "$i $local_dig $sz" >> "$DIGESTS"
          rm -f "$f"
          return 0
        else
          echo "$(ts) [guardian] ep01fchunk_$i DIGEST MISMATCH (local $local_dig vs remote $remote_dig) — re-uploading" >> "$LOG"
        fi
      else
        echo "$(ts) [guardian] ep01fchunk_$i download-back failed — retrying upload" >> "$LOG"
      fi
    fi
    local ok=0
    for attempt in 1 2 3 4 5; do
      if timeout 1800 gh release upload "$TAG" "$f" --repo "$REPO" --clobber >/tmp/ep01fchunk_$i-up.log 2>&1; then
        ok=1; break
      fi
      echo "$(ts) [guardian] ep01fchunk_$i upload attempt $attempt failed, retrying" >> "$LOG"
      sleep $((attempt*20))
    done
    if [ $ok -eq 0 ]; then
      echo "$(ts) [guardian] ep01fchunk_$i upload FAILED after 5 attempts — leaving for next run" >> "$LOG"
      return 1
    fi
    # download-back digest verify
    if gh release download "$TAG" --repo "$REPO" -p "ep01fchunk_$i" --clobber -O "/tmp/ep01fchunk_$i.verify" >/dev/null 2>&1; then
      remote_dig=$(sha256sum "/tmp/ep01fchunk_$i.verify" | awk '{print $1}')
      rm -f "/tmp/ep01fchunk_$i.verify"
      if [ "$remote_dig" == "$local_dig" ]; then
        echo "$(ts) [guardian] ep01fchunk_$i uploaded + DIGEST-VERIFIED ($local_dig) — deleting local chunk" >> "$LOG"
        echo "$i $local_dig $sz" >> "$DIGESTS"
        rm -f "$f"
        return 0
      else
        echo "$(ts) [guardian] ep01fchunk_$i DIGEST MISMATCH after upload (local $local_dig vs remote $remote_dig) — leaving for next run" >> "$LOG"
        return 1
      fi
    else
      echo "$(ts) [guardian] ep01fchunk_$i download-back failed after upload — leaving for next run" >> "$LOG"
      return 1
    fi
  else
    # local chunk already gone (verified in earlier pass) — confirm it exists on release
    remote_sz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"ep01fchunk_$i\") | .size" 2>/dev/null)
    if [ -n "$remote_sz" ] && [ "$remote_sz" != "null" ]; then
      if ! grep -q "^$i " "$DIGESTS" 2>/dev/null; then
        echo "$(ts) [guardian] ep01fchunk_$i already gone locally but on release ($remote_sz bytes) — no digest record; leaving gate open" >> "$LOG"
      fi
      return 0
    else
      echo "$(ts) [guardian] ep01fchunk_$i missing BOTH locally and on release — PROBLEM, leaving for next run" >> "$LOG"
      return 1
    fi
  fi
}

touch "$DIGESTS"
for i in 00 01 02 03 04 05 06 07 08 09 10 11; do
  verify_chunk "$i" || exit 1
done
echo "$(ts) [guardian] ALL ep01 chunks processed — gate state in $DIGESTS" >> "$LOG"
