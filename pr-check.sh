#!/bin/bash
# merge-law-ci-watch checker: reads pr-check-list.txt (repo pr), prints "repo pr state mergeStateStatus"
LIST="$HOME/workspace/agent-ops/pr-check-list.txt"
while read -r repo pr; do
  [[ "$repo" == \#* || -z "$repo" ]] && continue
  out=$(gh pr view "$pr" --repo "$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>/dev/null)
  if [ -z "$out" ]; then
    echo "$repo $pr FETCH_ERROR"
  else
    echo "$repo $pr $out"
  fi
done < "$LIST"
