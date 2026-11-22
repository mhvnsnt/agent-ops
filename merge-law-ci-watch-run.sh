#!/bin/bash
# merge-law-ci-watch batch run — Sat 2026-10-17
# Checks each listed PR; merges ONLY when state=OPEN and mergeStateStatus=CLEAN.
# Never squash/rebase. Never touch Bannon #78.
LOG="$HOME/workspace/agent-ops/merge-law-ci-watch-run-20261017.log"
: > "$LOG"
merged=0
blocked=0
already=0
errors=0

PRS=(
# MERGE-LAW PRs
"mhvnsnt/agent-ops 27"
"mhvnsnt/Bannon 83"
"mhvnsnt/Physics-sandbox-playground- 4"
"mhvnsnt/game-reverse-engineering 6"
"mhvnsnt/money-machine-hq 29"
"mhvnsnt/AshLanev2 46"
"mhvnsnt/Brutal-Fist 32"
"mhvnsnt/wrestling-game 6"
"mhvnsnt/Bannon 87"
"mhvnsnt/wrestling-game 9"
"mhvnsnt/Bannon 88"
"mhvnsnt/wrestling-game 10"
"mhvnsnt/AshLanev2 48"
"mhvnsnt/Brutal-Fist 35"
"mhvnsnt/TRIPPEDD-Production-studios- 272"
"mhvnsnt/Physics-sandbox-playground- 5"
"mhvnsnt/game-reverse-engineering 11"
"mhvnsnt/money-machine-hq 31"
"mhvnsnt/ConcreteDragon 59"
"mhvnsnt/western-heart 234"
"mhvnsnt/western-heart 237"
"mhvnsnt/western-heart 238"
# ANTI-CLOBBER LAW PRs
"mhvnsnt/agent-ops 31"
"mhvnsnt/agent-ops 32"
"mhvnsnt/AshLane-prototype 6"
"mhvnsnt/atlas 13"
"mhvnsnt/BioMechania 26"
"mhvnsnt/bolt.diy-M 2"
"mhvnsnt/ConcreteDragon 61"
"mhvnsnt/Forge3D 11"
"mhvnsnt/GAME-Emulator 4"
"mhvnsnt/Lyra 3"
"mhvnsnt/M-Hero-Simulator- 7"
"mhvnsnt/M-OS-Daywalker 3"
"mhvnsnt/M-OS-Daywalker-private 3"
"mhvnsnt/M.-Engine- 21"
"mhvnsnt/M_Unity_FreeflowCombat 3"
"mhvnsnt/Mochiichao-Diamond-Version-2d- 3"
"mhvnsnt/Moneymachine 3"
"mhvnsnt/Moneymachine-private 3"
"mhvnsnt/Neon-App-Builder 3"
"mhvnsnt/NightSkyEngine 3"
"mhvnsnt/Physics-sandbox-playground- 7"
"mhvnsnt/physics-playground-pwa 20"
"mhvnsnt/QuantumBlur 3"
"mhvnsnt/SMOKE-MIRROR-S- 6"
"mhvnsnt/SchwarzerblitzEngine 3"
"mhvnsnt/TRIPPEDD-Animation-Studio 8"
"mhvnsnt/TRIPPEDD-Production-studios- 274"
"mhvnsnt/Tekken3Recompiled-private 3"
"mhvnsnt/URBAN-MAYHEM- 9"
"mhvnsnt/Wrestli6game-3 5"
"mhvnsnt/animation-research-library 9"
"mhvnsnt/blend-physics-playground 10"
"mhvnsnt/box-orphans 2"
"mhvnsnt/box-storage 3"
"mhvnsnt/brutalfist11 4"
"mhvnsnt/brutalfistgrokversion 4"
"mhvnsnt/brutalfistgrokversion12 5"
"mhvnsnt/brutalfistgrokversion9 4"
"mhvnsnt/brutalfistgrokversioneight 6"
"mhvnsnt/brutalfistgrokversionfive 4"
"mhvnsnt/brutalfistgrokversionfour 4"
"mhvnsnt/brutalfistgrokversionseven 4"
"mhvnsnt/brutalfistgrokversionsix 4"
"mhvnsnt/brutalfistgrokversionten 42"
"mhvnsnt/brutalfistgrokversiontenpointfive 4"
"mhvnsnt/brutalfistgrokversionthree 4"
"mhvnsnt/brutalfistgrokversiontwo 4"
"mhvnsnt/cape-jones 105"
"mhvnsnt/chimera-emulator-hub 7"
"mhvnsnt/chimera-rom-nomercy 3"
"mhvnsnt/chimera-roms 5"
"mhvnsnt/cn-gigaleak-cow-and-chicken 4"
"mhvnsnt/cn-gigaleak-dexters-lab 3"
"mhvnsnt/cn-gigaleak-duck-dodgers 3"
"mhvnsnt/cn-gigaleak-fosters-home 3"
"mhvnsnt/cn-gigaleak-grim-adventures 4"
"mhvnsnt/cn-gigaleak-gumball 4"
"mhvnsnt/cn-gigaleak-johnny-bravo 5"
"mhvnsnt/cn-gigaleak-johnny-test 3"
"mhvnsnt/cn-gigaleak-kids-next-door 3"
"mhvnsnt/cn-gigaleak-looney-tunes 5"
"mhvnsnt/cn-gigaleak-mgm-shorts 3"
"mhvnsnt/cn-gigaleak-my-gym-partner 4"
"mhvnsnt/cn-gigaleak-pink-panther 4"
"mhvnsnt/cn-gigaleak-powerpuff-girls 4"
"mhvnsnt/cn-gigaleak-robot-chicken 4"
"mhvnsnt/cn-gigaleak-scooby-doo-mystery-inc 4"
"mhvnsnt/cn-gigaleak-space-ghost 4"
"mhvnsnt/cn-gigaleak-teen-titans 3"
"mhvnsnt/cn-gigaleak-wabbit 3"
"mhvnsnt/code-doctor 3"
"mhvnsnt/dispossessory-case 4"
"mhvnsnt/drive-storage 20"
"mhvnsnt/font-wizard 16"
"mhvnsnt/game-reverse-engineering 13"
"mhvnsnt/google-drive-repo 6"
"mhvnsnt/homefront 3"
"mhvnsnt/money-machine-hq 33"
"mhvnsnt/mystery-coast-ghosted 10"
"mhvnsnt/os-harvest 3"
"mhvnsnt/pocket-studio 6"
"mhvnsnt/ragdoll-wrestler 8"
"mhvnsnt/steal-like-artist-archive 3"
"mhvnsnt/texture-customizer 3"
"mhvnsnt/theyard 5"
"mhvnsnt/western-heart 235"
"mhvnsnt/wizard-gang-storage 5"
"mhvnsnt/wizard-gang-voice-pipe 6"
"mhvnsnt/wrestling-game 12"
"mhvnsnt/wwe-wrestler-models 5"
# CLOBBER RECOVERY PRs
"mhvnsnt/God-Molecule-Show-Studio 31"
)

for entry in "${PRS[@]}"; do
  repo="${entry% *}"
  num="${entry##* }"
  status=$(gh pr view "$num" --repo "$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>/dev/null)
  if [ -z "$status" ]; then
    echo "ERROR $repo #$num (view failed)" | tee -a "$LOG"
    errors=$((errors+1))
    sleep 1
    continue
  fi
  state="${status% *}"
  ms="${status##* }"
  if [ "$state" = "MERGED" ] || [ "$state" = "CLOSED" ]; then
    echo "DONE  $repo #$num ($state)" >> "$LOG"
    already=$((already+1))
  elif [ "$state" = "OPEN" ] && [ "$ms" = "CLEAN" ]; then
    out=$(gh pr merge "$num" --repo "$repo" --merge 2>&1)
    echo "MERGED $repo #$num :: $out" | tee -a "$LOG"
    merged=$((merged+1))
    sleep 2
  else
    echo "BLOCKED $repo #$num ($state $ms)" | tee -a "$LOG"
    blocked=$((blocked+1))
  fi
  sleep 1
done

echo "" | tee -a "$LOG"
echo "SUMMARY merged=$merged blocked=$blocked already_done=$already errors=$errors" | tee -a "$LOG"
