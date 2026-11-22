#!/bin/bash
# merge-law-ci-watch: check each PR, merge only if OPEN and CLEAN
LIST="$HOME/workspace/agent-ops/merge-law-ci-watch-prs.txt"
REPORT="$HOME/workspace/agent-ops/merge-law-ci-watch-report.txt"
> "$REPORT"
while read -r repo num; do
  [ -z "$repo" ] && continue
  num="${num#\#}"
  status=$(gh pr view "$num" --repo "$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>&1)
  echo "$repo #$num => $status" | tee -a "$REPORT"
  if [ "$status" = "OPEN CLEAN" ]; then
    echo "  -> MERGING" | tee -a "$REPORT"
    gh pr merge "$num" --repo "$repo" --merge 2>&1 | tee -a "$REPORT"
  fi
done < "$LIST"
echo "DONE" | tee -a "$REPORT"
