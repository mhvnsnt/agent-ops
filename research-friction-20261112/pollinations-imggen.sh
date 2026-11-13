#!/usr/bin/env bash
# pollinations-imggen.sh — free, no-key image generation via Pollinations.ai
# Proven live 2026-11-12 (friction-research pass): anonymous text-to-image
# and flux image-to-image both return real JPEGs from this VM in ~5-6 s.
#
#   Text-to-image:
#     ./pollinations-imggen.sh --prompt "a cute anime black cat on a pink cushion" \
#         --out cat.png --width 512 --height 512 --seed 7
#   Image-to-image (reference image must be a PUBLIC URL, e.g. a GitHub raw URL):
#     ./pollinations-imggen.sh --prompt "make it a white cat with a red bow" \
#         --image "https://raw.githubusercontent.com/.../ref.png" --out cat2.png
#
# Limits (verified 2026-11-12, see research-friction-20261112/01-free-headless-imagegen.md):
#   - Anonymous tier: ~1 image per 40 s (402s in between). This script paces
#     itself (45 s between calls in one process) and retries 429/5xx.
#   - Anonymous tier serves the Sana model even when model=flux is requested
#     (EXIF manufacturer=sana on the returned JPEG). Quality is still good
#     for anime/cartoon work; do not expect FLUX-pro fidelity.
#   - Anonymous images carry a "pollinations.ai" watermark bottom-right
#     (nologo=true is ignored on the anonymous tier).
#   - model=kontext (the FLUX.1 Kontext edit model) is NOT on the anonymous
#     tier: HTTP 403 "isn't part of the Classic API. Use it with a pollen
#     key". A free account key at https://enter.pollinations.ai unlocks it
#     (signup step, no card stated). Pass it as POLLINATIONS_KEY env var and
#     this script switches to the gen.pollinations.ai endpoint.
#   - Pollinations has its own content filter; spicy/NSFW prompts will be
#     refused. Do not use for Valerie back/ass versions — those stay blocked
#     until a valid route exists.
#   - No signup, no key, no card for the anonymous path. Stdlib only
#     (curl + file + sha256sum).
set -u
PROMPT=""; OUT=""; WIDTH=1024; HEIGHT=1024; SEED=""; MODEL="flux"
IMAGE_URL=""; NOLOGO="true"; MAX_ATTEMPTS=5
while [ $# -gt 0 ]; do
  case "$1" in
    --prompt) PROMPT="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --width) WIDTH="$2"; shift 2;;
    --height) HEIGHT="$2"; shift 2;;
    --seed) SEED="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --image) IMAGE_URL="$2"; shift 2;;
    --nologo) NOLOGO="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$PROMPT" ] && [ -n "$OUT" ] || { echo "usage: $0 --prompt P --out FILE [--width W --height H --seed N --model flux --image URL]" >&2; exit 2; }
command -v curl >/dev/null || { echo "curl required" >&2; exit 1; }

urlencode() { python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$1"; }
ENC_PROMPT=$(urlencode "$PROMPT")
if [ -n "${POLLINATIONS_KEY:-}" ]; then
  BASE="https://gen.pollinations.ai/image/${ENC_PROMPT}"
  AUTH=(-H "Authorization: Bearer $POLLINATIONS_KEY")
else
  BASE="https://image.pollinations.ai/prompt/${ENC_PROMPT}"
  AUTH=()
fi
Q="width=${WIDTH}&height=${HEIGHT}&model=${MODEL}&nologo=${NOLOGO}"
[ -n "$SEED" ] && Q="${Q}&seed=${SEED}"
[ -n "$IMAGE_URL" ] && Q="${Q}&image=$(urlencode "$IMAGE_URL")"
URL="${BASE}?${Q}"

attempt=1
while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
  # Anonymous pacing: one image per ~40 s. Only sleep on retries and when
  # a previous call happened recently in this process.
  if [ "$attempt" -gt 1 ]; then sleep 45; fi
  HTTP=$(curl -sS -L --max-time 240 -o "$OUT.tmp" -w "%{http_code}" "${AUTH[@]}" "$URL") || HTTP="000"
  if [ "$HTTP" = "200" ] && file "$OUT.tmp" | grep -qiE "image data|JPEG|PNG"; then
    mv "$OUT.tmp" "$OUT"
    echo "OK $OUT $(stat -c%s "$OUT") bytes sha256=$(sha256sum "$OUT" | cut -d' ' -f1)"
    file "$OUT"
    exit 0
  fi
  echo "attempt $attempt: HTTP $HTTP — $(head -c 200 "$OUT.tmp" 2>/dev/null)" >&2
  rm -f "$OUT.tmp"
  attempt=$((attempt + 1))
done
echo "FAILED after $MAX_ATTEMPTS attempts" >&2
exit 1
