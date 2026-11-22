#!/bin/bash
out=~/workspace/agent-ops/mergewatch-results-2026-10-27.txt
: > "$out"
while read repo n; do
  r=$(gh pr view "$n" --repo "mhvnsnt/$repo" --json mergeStateStatus,state --jq '"\(.state) \(.mergeStateStatus)"' 2>&1)
  echo "$repo #$n : $r" >> "$out"
done < ~/workspace/agent-ops/mergewatch-list.txt
echo "CHECK-DONE $(date -u +%FT%TZ)" >> "$out"
