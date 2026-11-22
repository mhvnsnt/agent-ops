#!/bin/bash
# Parallel download of TTT2 parts from GitHub Release
cd ~/workspace/game-reverse-engineering/tekken-tag-tournament-2/ttt2-parts/
BASE="https://github.com/mhvnsnt/western-heart/releases/download/ttt2-7z-v1"

download_part() {
  local n=$1
  local nn=$(printf "%02d" $n)
  local f="ttt2-500m.part_$nn"
  if [ "$n" -lt 26 ]; then
    expected=524288000
  else
    expected=256424393
  fi
  # skip if already correct
  if [ -f "$f" ]; then
    sz=$(stat -c%s "$f" 2>/dev/null)
    if [ "$sz" = "$expected" ]; then
      echo "$(date -u +%T) $f already done, skipping"
      return 0
    fi
    rm -f "$f"
  fi
  echo "$(date -u +%T) Downloading $f..."
  for attempt in 1 2 3; do
    if curl -sL --retry 3 -o "$f" "$BASE/$f"; then
      sz=$(stat -c%s "$f" 2>/dev/null)
      if [ "$sz" = "$expected" ]; then
        echo "$(date -u +%T) DONE $f ($sz bytes)"
        return 0
      fi
      echo "$(date -u +%T) $f size mismatch ($sz != $expected), retry $attempt"
      rm -f "$f"
    else
      echo "$(date -u +%T) $f curl failed, retry $attempt"
    fi
    sleep 5
  done
  echo "$(date -u +%T) FAILED $f after 3 attempts"
  return 1
}

# Download 6 at a time
for n in $(seq 1 26); do
  download_part $n &
  # limit parallelism
  while [ $(jobs -r | wc -l) -ge 6 ]; do sleep 5; done
done
wait
echo "$(date -u +%T) ALL DOWNLOADS COMPLETE"
ls -1 ttt2-500m.part_* | wc -l
