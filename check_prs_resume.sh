#!/bin/bash
check() {
  repo="$1"; n="$2"
  out=$(gh pr view "$n" --repo "mhvnsnt/$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>&1)
  echo "$repo #$n: $out"
}
check URBAN-MAYHEM- 9
check animation-research-library 9
check blend-physics-playground 10
check box-orphans 2
check box-storage 3
check brutalfist11 4
check brutalfistgrokversionten 42
check chimera-emulator-hub 7
check chimera-rom-nomercy 3
check chimera-roms 5
check cn-gigaleak-cow-and-chicken 4
check cn-gigaleak-dexters-lab 3
check cn-gigaleak-duck-dodgers 4
check cn-gigaleak-fosters-home 3
check cn-gigaleak-grim-adventures 4
check cn-gigaleak-gumball 4
check cn-gigaleak-johnny-bravo 5
check cn-gigaleak-johnny-test 3
check cn-gigaleak-kids-next-door 3
check cn-gigaleak-looney-tunes 5
