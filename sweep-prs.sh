#!/bin/bash
# Check each PR: merge only if state=OPEN and mergeStateStatus=CLEAN
out="sweep-results-$(date -u +%Y%m%dT%H%M%SZ).log"
> "$out"
merged=0; left=0
while read -r repo pr; do
  [ -z "$repo" ] && continue
  st=$(gh pr view "$pr" --repo "$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>/dev/null)
  echo "$repo #$pr => $st" | tee -a "$out"
  if [ "$st" = "OPEN CLEAN" ]; then
    echo "  MERGING $repo #$pr" | tee -a "$out"
    if gh pr merge "$pr" --repo "$repo" --merge >> "$out" 2>&1; then
      echo "  MERGED" | tee -a "$out"; merged=$((merged+1))
    else
      echo "  MERGE-FAILED" | tee -a "$out"; left=$((left+1))
    fi
  else
    left=$((left+1))
  fi
  sleep 1
done < pr-sweep-list.txt
echo "=== merged=$merged left_open=$left" | tee -a "$out"
