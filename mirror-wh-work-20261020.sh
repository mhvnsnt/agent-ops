#!/bin/bash
# Mirror lane: wh-work-mirror-20261020 (disk-space-guardian 2026-10-20 ~03:45 CDT)
# For each cold work dir: tar -> split 100MB -> gh release upload (delete-as-you-go)
# -> full re-download stream-verify (sha256, no disk) -> rm -rf source -> log.
# NEVER touches: in-flight dirs, .DO_NOT_DELETE, repos, tools/, tekken5, staging-mocapsit,
# sp-scratch, meshrepair-scratch, _sf-scratch, deathfang-yamazaki, viggle-inputs, wt-mocapsit.
set -u
REPO="mhvnsnt/clouddog-storage"
TAG="wh-work-mirror-20261020"
WORK="$HOME/workspace/agent-ops/.mirror-ww"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
mkdir -p "$WORK"
log(){ echo "[$(date '+%F %T %Z')] MIRROR-WW: $*" | tee -a "$LOG"; }
free_mb(){ df -m /home/hatch | tail -1 | awk '{print $4}'; }

DIRS=(
  "$HOME/workspace/_wh-work/moveset-cluster-b-t7"
  "$HOME/workspace/_wh-work/moveset-cluster-c-sf"
  "$HOME/workspace/_wh-work/moveset-cluster-d-kof"
  "$HOME/workspace/_wh-work/moveset-cluster-a-t8"
  "$HOME/workspace/_wh-work/anim-targeting-fix"
  "$HOME/workspace/_wh-work/sf-moves"
  "$HOME/workspace/_wh-work/sf-teardown-pr2"
  "$HOME/workspace/wt-stream4-parity"
  "$HOME/workspace/star-rig-work"
  "$HOME/workspace/wh-teardown-integration"
)

if ! gh release view "$TAG" --repo "$REPO" >/dev/null 2>&1; then
  gh release create "$TAG" --repo "$REPO" --title "WH work mirror 2026-10-20" \
    --notes "Disk-guardian workdir mirror 2026-10-20 (ONE-STORE RULE): cold _wh-work + work dirs, tar split into <=100MB parts. Pull-back: gh release download $TAG --repo $REPO --pattern '<item>.tar.part-*' --dir <dest>; cat <item>.tar.part-* > <item>.tar; tar -xf <item>.tar" \
    || { log "FATAL: cannot create release"; exit 1; }
  log "created release $TAG"
fi

asset_id(){
  gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"$1\") | .id" 2>/dev/null
}
asset_size(){
  gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"$1\") | .size" 2>/dev/null
}

for D in "${DIRS[@]}"; do
  [ -d "$D" ] || { log "skip (gone): $D"; continue; }
  if find "$D" -maxdepth 2 -name '.DO_NOT_DELETE*' 2>/dev/null | grep -q .; then
    log "skip (DO_NOT_DELETE): $D"; continue
  fi
  ITEM="$(basename "$D").tar"
  NEWEST=$(find "$D" -type f -printf '%T@\n' 2>/dev/null | sort -rn | head -1 | cut -d. -f1)
  NOW=$(date +%s)
  if [ $(( NOW - NEWEST )) -lt 3600 ]; then
    log "skip (written <60min ago, possibly in-flight): $D"; continue
  fi
  if [ "$(free_mb)" -lt 2500 ]; then
    log "STOP: <2.5G free, halting lane"; break
  fi
  log "START $D -> $ITEM"
  PDIR="$WORK/$ITEM.d"; rm -rf "$PDIR"; mkdir -p "$PDIR"
  # tar, split into 100MB parts, then sha256 the reassembled stream (race-free)
  tar -cf - -C "$(dirname "$D")" "$(basename "$D")" \
    | split -b 100M -d - "$PDIR/$ITEM.part-"
  TSHA=$(cat "$PDIR"/$ITEM.part-* | sha256sum | awk '{print $1}')
  PSUM=$(du -cb "$PDIR"/$ITEM.part-* 2>/dev/null | tail -1 | awk '{print $1}')
  DSZ=$(du -sb "$D" 2>/dev/null | awk '{print $1}')
  if [ -z "$PSUM" ] || [ "$PSUM" -lt 1000 ] || [ "$PSUM" -lt $(( DSZ / 2 )) ]; then
    log "FAIL: tar/split sanity (parts=$PSUM B, dir=$DSZ B) — dir kept"; rm -rf "$PDIR"; continue
  fi
  log "$ITEM tar sha256=$TSHA"
  echo "$TSHA  $ITEM" > "$PDIR/MANIFEST.txt"
  FAIL=0
  for P in "$PDIR"/$ITEM.part-*; do
    PN=$(basename "$P"); LSZ=$(stat -c%s "$P")
    RSZ=$(asset_size "$PN")
    if [ -n "$RSZ" ] && [ "$RSZ" = "$LSZ" ]; then
      log "$PN already on store ($LSZ B), skip upload"
    else
      for ATT in 1 2 3; do
        if gh release upload "$TAG" "$P" --repo "$REPO" --clobber >/dev/null 2>&1; then break; fi
        log "$PN upload attempt $ATT failed, retrying"; sleep 10
      done
      RSZ=$(asset_size "$PN")
      if [ -z "$RSZ" ] || [ "$RSZ" != "$LSZ" ]; then
        log "FAIL: $PN size mismatch (local $LSZ, store $RSZ)"; FAIL=1; break
      fi
    fi
    sha256sum "$P" | awk -v n="$PN" '{print $1"  "n}' >> "$PDIR/MANIFEST.txt"
    rm -f "$P"   # delete-as-you-go: disk falls DURING the upload
    log "$PN uploaded+verified ($LSZ B), local part deleted"
  done
  if [ "$FAIL" = "1" ]; then log "ABORT $ITEM (part failure), local dir kept"; continue; fi
  # upload manifest
  gh release upload "$TAG" "$PDIR/MANIFEST.txt" --repo "$REPO" --clobber >/dev/null 2>&1
  # FULL re-download verify: stream all parts, hash, compare (no disk)
  log "$ITEM: full re-download verify (streamed)..."
  VFY=$( { for PN in $(tail -n +2 "$PDIR/MANIFEST.txt" | awk '{print $2}' | sort); do
            AID=$(asset_id "$PN")
            [ -n "$AID" ] || { echo "MISSING_ASSET_ID"; break; }
            gh api "repos/$REPO/releases/assets/$AID" -H "Accept: application/octet-stream"
          done; } | sha256sum | awk '{print $1}' )
  if [ "$VFY" != "$TSHA" ]; then
    log "FAIL: $ITEM re-download sha256 mismatch (got $VFY, want $TSHA) — local dir KEPT"; continue
  fi
  log "$ITEM VERIFIED 100% on $REPO@$TAG (sha256 match)"
  # final active-write re-check before delete
  NEWEST2=$(find "$D" -type f -printf '%T@\n' 2>/dev/null | sort -rn | head -1 | cut -d. -f1)
  if [ $(( $(date +%s) - NEWEST2 )) -lt 3600 ]; then
    log "skip delete (dir written during mirror, in-flight): $D"; continue
  fi
  rm -rf "$D" "$PDIR"
  sync
  log "CLEARED $D (verified on $REPO release $TAG as $ITEM, $(free_mb)MB free now)"
done
log "lane done"
