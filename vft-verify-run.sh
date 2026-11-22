#!/bin/bash
# VFT lane: download-back verify -> publish -> delete -> log -> checkpoint done
# Resume of disk-store-fontstools.json (fonts part already DONE per log).
set -u
CKPT=~/workspace/agent-ops/checkpoints/disk-store-fontstools.json
STAGE=~/workspace/.verify-staging/vft
REPO=mhvnsnt/video-fix-tools
TAG=vft-archive-2026-10-15
LOCALDIR=~/workspace/video-fix-tools
LOG=~/workspace/agent-ops/disk-cleanup-log.md
hb() { python3 -c "
import json,sys,datetime
p=sys.argv[1]; d=json.load(open(p))
d['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
d['notes']=sys.argv[2]
json.dump(d,open(p,'w'),indent=1)" "$CKPT" "$1"; echo "HB: $1"; }

hb "2026-10-15: vft verify script started; single-stream pipe ~0.7MB/s, downloading aa-ad sequentially."
cd "$STAGE"
for p in aa ab ac ad; do
  f="vft-archive-2026-10-15.tar.part_$p"
  if [ -f "$f" ] && [ "$(stat -c %s "$f")" = "524288000" ]; then echo "SKIP $f (complete)"; continue; fi
  echo "Downloading $f ..."
  ok=0
  for attempt in 1 2 3; do
    rm -f "$f"
    if gh release download "$TAG" -R "$REPO" -p "$f" -D "$STAGE"/; then ok=1; break; fi
    echo "download attempt $attempt failed for $f, retrying in 30s..."
    sleep 30
  done
  [ "$ok" = "1" ] || { hb "VFT BLOCKED: download of $f failed after 3 attempts"; exit 1; }
done
hb "VFT: all 5 parts downloaded; running sha256sum -c."
sha256sum -c SHA256SUMS || { hb "VFT BLOCKED: part sha256 MISMATCH - NOT deleting"; exit 1; }
echo "PART HASHES OK"
hb "VFT: 5/5 part hashes match; extracting tar and diffing vs local tree."
mkdir -p "$STAGE/extract"
cat vft-archive-2026-10-15.tar.part_* | tar -xf - -C "$STAGE/extract" || { hb "VFT BLOCKED: tar extract failed"; exit 1; }
TOP=$(ls "$STAGE/extract")
echo "Tar top level: $TOP"
if [ "$(ls "$STAGE/extract" | wc -l)" != "1" ]; then hb "VFT BLOCKED: tar has >1 top-level entry: $TOP"; exit 1; fi
diff -r -q "$STAGE/extract/$TOP" "$LOCALDIR" > "$STAGE/diff.out" 2>&1
if [ -s "$STAGE/diff.out" ]; then echo "DIFF FOUND:"; head -20 "$STAGE/diff.out"; hb "VFT BLOCKED: extracted tar differs from local tree - NOT deleting"; exit 1; fi
echo "TREE DIFF CLEAN"
# confirm .git history present in archive
[ -d "$STAGE/extract/$TOP/.git" ] || { hb "VFT BLOCKED: no .git in archive"; exit 1; }
cd "$STAGE/extract/$TOP" && git log --oneline -1 && cd "$STAGE"
hb "VFT: archive byte-identical to local tree incl .git; publishing release."
gh release edit "$TAG" -R "$REPO" --draft=false || { hb "VFT BLOCKED: publish failed"; exit 1; }
echo "RELEASE PUBLISHED"
# SAVE-BEFORE-DELETE satisfied: verified backup on GitHub. Delete locals.
FREED=$(du -sb "$LOCALDIR" | cut -f1)
rm -rf "$LOCALDIR"
BFREED=$(du -sb ~/workspace/agent-ops/bundle-staging/vft-backup-2026-10-15.bundle 2>/dev/null | cut -f1 || echo 0)
rm -f ~/workspace/agent-ops/bundle-staging/vft-backup-2026-10-15.bundle ~/workspace/agent-ops/bundle-staging/vft-backup-2026-10-15.bundle.sha256
rm -rf "$STAGE"
# delete dead vft-backup draft (bundle asset never uploaded; superseded by archive)
gh release delete vft-backup-2026-10-15 -R "$REPO" --yes 2>/dev/null || true
gh release delete-asset vft-backup-2026-10-15 vft-backup-2026-10-15.bundle.sha256 -R "$REPO" --yes 2>/dev/null || true
DF=$(df -h /home/hatch | tail -1 | awk '{print $5}')
{
echo ""
echo "2026-10-15T$(date -u +%H:%M:%SZ) [disk-store] VFT lane DONE: downloaded 5 tar parts back from mhvnsnt/video-fix-tools:vft-archive-2026-10-15, sha256sum -c clean 5/5, extracted tar diff -r -q vs local tree CLEAN (incl .git, HEAD 2d0e36d). Release published (not draft). DELETED ~/workspace/video-fix-tools (${FREED} bytes), redundant git bundle staging (${BFREED} bytes), dead vft-backup draft. Disk now $DF."
} >> "$LOG"
python3 -c "
import json,datetime
p='$CKPT'; d=json.load(open(p))
d['status']='done'; d['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
d['notes']='2026-10-15: DONE. 5/5 parts download-back sha256 clean, extract+diff -r clean incl .git, release published, local video-fix-tools + bundle staging deleted, dead vft-backup draft removed. Fonts were already done (pushed to mhvnsnt/font-wizard @0ddfce55).'
json.dump(d,open(p,'w'),indent=1)"
echo "VFT LANE COMPLETE"
