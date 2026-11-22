#!/usr/bin/env bash
# Guardian mirror pass 2026-10-20 07:44 CDT.
# Mirrors IDLE (no live writers, 6-25h since last write) github-tier bulk to
# mhvnsnt/clouddog-storage release clouddog-20261020. Mirroring never deletes;
# the clear decision happens on a later guardian pass after independent re-verify
# and a fresh idleness check (NO-SWEEP-INFLIGHT / ONE-STORE RULE preserved).
set -u
REPO=mhvnsnt/clouddog-storage
TAG=clouddog-20261020
LOG=~/workspace/agent-ops/disk-cleanup-log.md
MAN=~/workspace/agent-ops/guardian-mirror-20261020-0744.SHA256
STAGE=~/workspace/agent-ops/.guardian-mirror-20261020-0744
mkdir -p "$STAGE"
: > "$MAN"

upload() { # $1=local path, $2=asset name
  local f="$1" a="$2"
  [ -f "$f" ] || { echo "$(date '+%F %T %Z') mirror-SKIP missing $f" >>"$LOG"; return 1; }
  sha256sum "$f" >> "$MAN"
  for i in 1 2 3; do
    if gh release upload "$TAG" "$f#$a" --repo "$REPO" --clobber >/dev/null 2>&1; then
      echo "$(date '+%F %T %Z') mirror-ok $a <- $f ($(du -h "$f" | cut -f1))" >>"$LOG"
      return 0
    fi
    sleep 30
  done
  echo "$(date '+%F %T %Z') mirror-FAILED $a <- $f" >>"$LOG"
  return 1
}

echo "$(date '+%F %T %Z') guardian-mirror-20261020-0744 START" >>"$LOG"

# Package dir payloads (keeps the STAGE sacred-protected? no: stage is transient; manifest is the sacred record)
tar -cf "$STAGE/wm-chunks.tar" -C ~/workspace/viggle-inputs wm-chunks
tar -cf "$STAGE/autorig-foreign.tar" -C ~/workspace/autorig-work foreign

# sunra-rig (718M, last write 2026-10-19 06:25, no live writers)
upload ~/workspace/sunra-rig/sun-ra-rigged.blend    sunra-rig-sun-ra-rigged.blend
upload ~/workspace/sunra-rig/sun-ra-rigged-v2.blend sunra-rig-sun-ra-rigged-v2.blend
upload ~/workspace/sunra-rig/sun-ra-rigged-v3.blend sunra-rig-sun-ra-rigged-v3.blend
upload ~/workspace/sunra-rig/sun-ra-anim.blend      sunra-rig-sun-ra-anim.blend

# twerk-test (last write 2026-10-19 21:11, no live writers)
if cmp -s ~/workspace/twerk-test/star_twerk.blend ~/workspace/twerk-test/star_twerk.blend1; then
  echo "$(date '+%F %T %Z') twerk-test: star_twerk.blend1 byte-identical to star_twerk.blend (single store covers both)" >>"$LOG"
fi
upload ~/workspace/twerk-test/star_twerk.blend     twerk-test-star_twerk.blend

# packaged dirs
upload "$STAGE/wm-chunks.tar"          viggle-inputs-wm-chunks.tar
upload "$STAGE/autorig-foreign.tar"    autorig-work-foreign.tar

rm -rf "$STAGE"
echo "$(date '+%F %T %Z') guardian-mirror-20261020-0744 DONE" >>"$LOG"
