#!/bin/bash
check_one() {
  repo="$1"; pr="$2"
  st=$(gh pr view "$pr" --repo "mhvnsnt/$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>&1)
  if [ "$st" = "OPEN CLEAN" ]; then
    mg=$(gh pr merge "$pr" --repo "mhvnsnt/$repo" --merge 2>&1)
    echo "MERGED: $repo #$pr :: $mg"
  else
    echo "SKIP: $repo #$pr :: $st"
  fi
}
export -f check_one
cat <<'LIST' | xargs -P 6 -n 2 bash -c 'check_one "$@"' _
cn-gigaleak-grim-adventures 4
cn-gigaleak-gumball 4
cn-gigaleak-johnny-bravo 5
cn-gigaleak-johnny-test 3
cn-gigaleak-kids-next-door 3
cn-gigaleak-looney-tunes 5
cn-gigaleak-mgm-shorts 3
cn-gigaleak-my-gym-partner 4
cn-gigaleak-pink-panther 4
cn-gigaleak-powerpuff-girls 4
cn-gigaleak-robot-chicken 4
cn-gigaleak-scooby-doo-mystery-inc 4
cn-gigaleak-space-ghost 4
cn-gigaleak-teen-titans 3
cn-gigaleak-wabbit 3
dispossessory-case 4
drive-storage 20
google-drive-repo 6
homefront 3
os-harvest 3
pocket-studio 6
steal-like-artist-archive 3
wizard-gang-storage 5
wizard-gang-voice-pipe 6
wwe-wrestler-models 5
LIST
