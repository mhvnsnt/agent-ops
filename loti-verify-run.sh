#!/bin/bash
# LOTI lanes: download-back verify 10/10 parts -> publish -> delete locals -> log -> checkpoints done
# Resumes disk-store-ep01loti.json + disk-store-loti-final.json
set -u
CKPT1=~/workspace/agent-ops/checkpoints/disk-store-ep01loti.json
CKPT2=~/workspace/agent-ops/checkpoints/disk-store-loti-final.json
STAGE=~/workspace/.verify-staging/loti
REPO=mhvnsnt/drive-storage
TAG=ep01-loti-swap-2026-10-14
LOCALDIR=~/workspace/ep01-loti-swap
LOG=~/workspace/agent-ops/disk-cleanup-log.md
hb() { python3 -c "
import json,sys,datetime
n=sys.argv[3]
for p in sys.argv[1].split(','):
    d=json.load(open(p))
    d['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    d['notes']=n
    json.dump(d,open(p,'w'),indent=1)" "$CKPT1,$CKPT2" x "$1"; echo "HB: $1"; }

hb "2026-10-15: loti verify script started; downloading 10 parts sequentially (~0.7MB/s pipe)."
cd "$STAGE"
# sha files (fresh, authoritative) — retry on transient proxy flakes
ok=0
for attempt in 1 2 3; do
  if gh release download "$TAG" -R "$REPO" -p "parts.sha256" -p "originals.sha256" -D "$STAGE"/; then ok=1; break; fi
  echo "sha download attempt $attempt failed, retrying in 30s..."
  sleep 30
done
[ "$ok" = "1" ] || { hb "LOTI BLOCKED: sha file download failed after 3 attempts"; exit 1; }
declare -A EXPECT=( [v2.part_aa]=524288000 [v2.part_ab]=524288000 [v2.part_ac]=524288000 [v2.part_ad]=524288000 [v2.part_ae]=344107465 [p2.part_aa]=524288000 [p2.part_ab]=524288000 [p2.part_ac]=524288000 [p2.part_ad]=524288000 [p2.part_ae]=106854944 )
for f in v2.part_aa v2.part_ab v2.part_ac v2.part_ad v2.part_ae p2.part_aa p2.part_ab p2.part_ac p2.part_ad p2.part_ae; do
  if [ -f "$f" ] && [ "$(stat -c %s "$f")" = "${EXPECT[$f]}" ]; then echo "SKIP $f (complete)"; continue; fi
  echo "Downloading $f ..."
  ok=0
  for attempt in 1 2 3; do
    rm -f "$f"
    if gh release download "$TAG" -R "$REPO" -p "$f" -D "$STAGE"/; then ok=1; break; fi
    echo "download attempt $attempt failed for $f, retrying in 30s..."
    sleep 30
  done
  [ "$ok" = "1" ] || { hb "LOTI BLOCKED: download of $f failed after 3 attempts"; exit 1; }
done
hb "LOTI: 10/10 parts downloaded; verifying per-part sha256."
sha256sum -c <(grep -E "v2.part_|p2.part_" parts.sha256) || { hb "LOTI BLOCKED: part sha256 MISMATCH - NOT deleting"; exit 1; }
echo "10/10 PART HASHES OK"
hb "LOTI: parts hash-clean; verifying reassembly against originals."
V2SHA=$(cat v2.part_aa v2.part_ab v2.part_ac v2.part_ad v2.part_ae | sha256sum | cut -d' ' -f1)
P2SHA=$(cat p2.part_aa p2.part_ab p2.part_ac p2.part_ad p2.part_ae | sha256sum | cut -d' ' -f1)
V2EXP=$(grep "EP01-THE-WALK-v2.mp4" originals.sha256 | cut -d' ' -f1)
P2EXP=$(grep " p2.mp4" originals.sha256 | cut -d' ' -f1)
echo "v2 reassembled: $V2SHA"; echo "v2 expected:    $V2EXP"
echo "p2 reassembled: $P2SHA"; echo "p2 expected:    $P2EXP"
[ "$V2SHA" = "$V2EXP" ] || { hb "LOTI BLOCKED: v2 reassembly sha mismatch"; exit 1; }
[ "$P2SHA" = "$P2EXP" ] || { hb "LOTI BLOCKED: p2 reassembly sha mismatch"; exit 1; }
echo "REASSEMBLY VERIFIED: parts reproduce originals byte-identical"
# also confirm local originals still match (unchanged since split)
cd "$LOCALDIR" && sha256sum -c <(grep -E "EP01-THE-WALK-v2.mp4| p2.mp4" "$STAGE/originals.sha256") || { hb "LOTI BLOCKED: local originals changed since split"; exit 1; }
cd "$STAGE"
hb "LOTI: fully verified; updating release notes with reassembly command and publishing."
NOTES="Cold archive of workspace/ep01-loti-swap: EP01 segment-5 LOTI swap intermediates (v2 master 2.3G, p2 2.1G, seg5 pieces, qc). EP01 finished cut delivered 2026-10-14.

REASSEMBLY (verified 2026-10-15, download-back sha256 10/10 + cat|sha256 == originals):
  cat v2.part_aa v2.part_ab v2.part_ac v2.part_ad v2.part_ae > EP01-THE-WALK-v2.mp4   # sha256 $V2EXP
  cat p2.part_aa p2.part_ab p2.part_ac p2.part_ad p2.part_ae > p2.mp4                 # sha256 $P2EXP
Archived by disk-offload lane to free local disk."
gh release edit "$TAG" -R "$REPO" --notes "$NOTES" --draft=false || { hb "LOTI BLOCKED: publish failed"; exit 1; }
echo "RELEASE PUBLISHED"
# SAVE-BEFORE-DELETE satisfied. Delete local originals + stale chunks + qc + dir.
FREED=$(du -sb "$LOCALDIR" | cut -f1)
rm -rf "$LOCALDIR" "$STAGE"
DF=$(df -h /home/hatch | tail -1 | awk '{print $5}')
{
echo ""
echo "2026-10-15T$(date -u +%H:%M:%SZ) [disk-store] LOTI lanes DONE: downloaded 10 parts back from mhvnsnt/drive-storage:ep01-loti-swap-2026-10-14, sha256sum -c clean 10/10, cat-reassembly sha256 == originals.sha256 for both EP01-THE-WALK-v2.mp4 and p2.mp4, local originals unchanged. Release published with reassembly notes. DELETED ~/workspace/ep01-loti-swap/ (${FREED} bytes: originals + stale split chunks + qc). 5 small files already on ep01-renders-2026-10-14 (published). Disk now $DF."
} >> "$LOG"
python3 -c "
import json,datetime
for p in ['$CKPT1','$CKPT2']:
    d=json.load(open(p))
    d['status']='done'; d['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    d['notes']='2026-10-15: DONE. 10/10 parts download-back sha256 clean, reassembly reproduces originals byte-identical, release published with reassembly notes, ~/workspace/ep01-loti-swap/ deleted. Small files on published ep01-renders-2026-10-14.'
    json.dump(d,open(p,'w'),indent=1)"
echo "LOTI LANES COMPLETE"
