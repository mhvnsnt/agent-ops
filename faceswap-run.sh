#!/bin/bash
# FaceFusion CPU batch: 12 Kiko music video clips with Muta reference faces
# Launched by worker-watchdog 2026-10-12. Logs to ~/workspace/agent-ops/faceswap.log
set -u
FF="$HOME/workspace/video-fix-tools/character-replace/facefusion"
VID="$HOME/workspace/trippedd-studio/production/WIZARD_GANG_EP01/video"
REFS="$HOME/workspace/voice-clone-work/kiko/muta-refs"
OUT="$VID/faceswap"
mkdir -p "$OUT"
declare -A MAP=(
  [pier-8s]="muta-1.jpg"
  [cont-1]="muta-3.jpg"
  [cont-2]="muta-white-1.jpg"
  [cont-3]="muta-1.jpg"
  [cont-4]="muta-white-2.jpg"
  [cont-5]="muta-2.jpg"
  [cont-6]="muta-white-5.jpg"
  [cont-7]="muta-1.jpg"
  [cont-8]="muta-white-7.jpg"
  [cont-9]="muta-3.jpg"
  [cont-10]="muta-white-1.jpg"
  [cont-11]="muta-1.jpg"
)
ORDER="pier-8s cont-1 cont-2 cont-3 cont-4 cont-5 cont-6 cont-7 cont-8 cont-9 cont-10 cont-11"
for clip in $ORDER; do
  target=$(ls "$VID"/media-generation-kiko-"$clip"-*.mp4 2>/dev/null | head -1)
  [ -z "$target" ] && { echo "$(date -u +%FT%TZ) $clip SKIP: source clip missing"; continue; }
  src="$REFS/${MAP[$clip]}"
  out="$OUT/${clip}-faceswap.mp4"
  if [ -s "$out" ]; then
    echo "$(date -u +%FT%TZ) $clip SKIP: output exists ($out)"
    continue
  fi
  echo "$(date -u +%FT%TZ) $clip START (src=${MAP[$clip]})"
  cd "$FF" && python3 facefusion.py headless-run \
    --processors face_swapper \
    --execution-providers cpu --execution-thread-count 8 \
    --temp-frame-format jpeg \
    --output-video-encoder libx264 --output-video-preset veryfast \
    -s "$src" -t "$target" -o "$out" >> "$HOME/workspace/agent-ops/faceswap.log" 2>&1
  rc=$?
  echo "$(date -u +%FT%TZ) $clip DONE rc=$rc out=$out"
done
echo "$(date -u +%FT%TZ) BATCH COMPLETE"
