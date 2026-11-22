#!/bin/bash
check() {
  repo="$1"; n="$2"
  out=$(gh pr view "$n" --repo "mhvnsnt/$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>&1)
  echo "$repo #$n: $out"
}
check cn-gigaleak-mgm-shorts 3
check cn-gigaleak-my-gym-partner 4
check cn-gigaleak-pink-panther 4
check cn-gigaleak-powerpuff-girls 4
check cn-gigaleak-robot-chicken 4
check cn-gigaleak-scooby-doo-mystery-inc 4
check cn-gigaleak-space-ghost 4
check cn-gigaleak-teen-titans 3
check cn-gigaleak-wabbit 3
check dispossessory-case 4
check drive-storage 20
check google-drive-repo 6
check homefront 3
check os-harvest 3
check pocket-studio 6
check steal-like-artist-archive 3
check wizard-gang-storage 5
check wizard-gang-voice-pipe 6
check wwe-wrestler-models 5
