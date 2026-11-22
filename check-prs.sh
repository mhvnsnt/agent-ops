#!/bin/bash
# Checks each PR in $1 (repo pr lines), outputs "repo pr state status"
check_one() {
  local repo="$1" pr="$2"
  local out
  out=$(gh pr view "$pr" --repo "$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>/dev/null)
  if [ -z "$out" ]; then
    echo "$repo $pr ERROR"
  else
    echo "$repo $pr $out"
  fi
}
export -f check_one
cat "$1" | xargs -P 12 -n 2 bash -c 'check_one "$0" "$1"'
