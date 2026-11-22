#!/usr/bin/env bash
# merge-law-ci-watch sweep 2026-10-26
# Format: repo#pr
PRS=(
"Physics-sandbox-playground-#4"
"Physics-sandbox-playground-#5"
"Physics-sandbox-playground-#7"
"money-machine-hq#29"
"money-machine-hq#31"
"AshLanev2#46"
"AshLanev2#48"
"TRIPPEDD-Production-studios-#272"
"TRIPPEDD-Production-studios-#274"
"atlas#13"
"BioMechania#26"
"bolt.diy-M#2"
"M-OS-Daywalker-private#3"
"M.-Engine-#21"
"Moneymachine-private#3"
"physics-playground-pwa#20"
"SMOKE-MIRROR-S-#6"
"TRIPPEDD-Animation-Studio#8"
"Tekken3Recompiled-private#3"
"URBAN-MAYHEM-#9"
"animation-research-library#9"
"blend-physics-playground#10"
"box-orphans#2"
"box-storage#3"
"brutalfist11#4"
"brutalfistgrokversionten#42"
"chimera-emulator-hub#7"
"chimera-rom-nomercy#3"
"chimera-roms#5"
"cn-gigaleak-cow-and-chicken#4"
"cn-gigaleak-dexters-lab#3"
"cn-gigaleak-duck-dodgers#4"
"cn-gigaleak-fosters-home#3"
"cn-gigaleak-grim-adventures#4"
"cn-gigaleak-gumball#4"
"cn-gigaleak-johnny-bravo#5"
"cn-gigaleak-johnny-test#3"
"cn-gigaleak-kids-next-door#3"
"cn-gigaleak-looney-tunes#5"
"cn-gigaleak-mgm-shorts#3"
"cn-gigaleak-my-gym-partner#4"
"cn-gigaleak-pink-panther#4"
"cn-gigaleak-powerpuff-girls#4"
"cn-gigaleak-robot-chicken#4"
"cn-gigaleak-scooby-doo-mystery-inc#4"
"cn-gigaleak-space-ghost#4"
"cn-gigaleak-teen-titans#3"
"cn-gigaleak-wabbit#3"
"dispossessory-case#4"
"drive-storage#20"
"google-drive-repo#6"
"homefront#3"
"os-harvest#3"
"pocket-studio#6"
"steal-like-artist-archive#3"
"wizard-gang-storage#5"
"wizard-gang-voice-pipe#6"
"wwe-wrestler-models#5"
)
OUT="$HOME/workspace/agent-ops/merge-law-ci-watch-2026-10-26.log"
mkdir -p "$HOME/workspace/agent-ops"
: > "$OUT"
merged=0; open_not_clean=0; closed=0; errors=0
for item in "${PRS[@]}"; do
  repo="${item%%#*}"
  num="${item##*#}"
  status=$(gh pr view "$num" --repo "mhvnsnt/$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>/dev/null)
  if [ -z "$status" ]; then
    echo "mhvnsnt/$repo#$num: ERROR (no data)" | tee -a "$OUT"
    errors=$((errors+1))
    continue
  fi
  echo "mhvnsnt/$repo#$num: $status" | tee -a "$OUT"
  if [ "$status" = "OPEN CLEAN" ]; then
    if gh pr merge "$num" --repo "mhvnsnt/$repo" --merge 2>&1 | tee -a "$OUT"; then
      merged=$((merged+1))
    else
      echo "mhvnsnt/$repo#$num: MERGE FAILED" | tee -a "$OUT"
    fi
  elif [ "$status" = "MERGED CLEAN" ] || [ "${status%% *}" = "MERGED" ]; then
    closed=$((closed+1))
  elif [ "${status%% *}" = "CLOSED" ]; then
    closed=$((closed+1))
  else
    open_not_clean=$((open_not_clean+1))
  fi
done
echo "SUMMARY: checked=${#PRS[@]} merged=$merged open_not_clean=$open_not_clean already_closed_merged=$closed errors=$errors" | tee -a "$OUT"
