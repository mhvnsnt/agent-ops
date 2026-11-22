#!/bin/bash
# Overnight pipeline delta sweep — 2026-11-20 16:14Z run
# Baseline: 13:44Z run. Fetches main tips + open PR lists for all 17 repos,
# then commit-status for the candidate PR heads carried from the baseline.
set -u
OUT=~/workspace/agent-ops/overnight-sweep-20261120-1614
mkdir -p "$OUT"
REPOS="western-heart cape-jones game-reverse-engineering Bannon ConcreteDragon ConcreteDragon2 wrestling-game pokemon-arena-3d pokemon-arena-2d dream-girl M.-Engine- money-machine-hq physics-playground-pwa TRIPPEDD-Production-studios- TRIPPEDD-Animation-Studio Wrestli6game-3 agent-ops"
: > "$OUT/tips.txt"
: > "$OUT/open_counts.txt"
for r in $REPOS; do
  sha=$(gh api "repos/mhvnsnt/$r/commits/main" --jq '.sha' 2>"$OUT/err-$r.txt" | cut -c1-7)
  echo "$r $sha" >> "$OUT/tips.txt"
  gh api "repos/mhvnsnt/$r/pulls?state=open&per_page=100" --jq '.[] | [.number, .draft, .mergeable, (.head.sha | .[0:7]), (.created_at | .[0:10]), (.title | .[0:80])] | @tsv' 2>>"$OUT/err-$r.txt" > "$OUT/prs-$r.tsv"
  echo "$r $(wc -l < "$OUT/prs-$r.tsv")" >> "$OUT/open_counts.txt"
done
# Candidate heads from 13:44Z baseline (repo:pr:head7)
CANDS="western-heart:1778:796df7c western-heart:1777:ddf19a5 western-heart:1714:c6d4234 western-heart:1696:c675e6c Bannon:150:8f68e07 Bannon:151:e43f23f Bannon:152:0f6ed99 Bannon:153:1c17f1b Bannon:154:d7a4ab4 Bannon:155:aef354c Bannon:156:8246fc1 Bannon:157:28a457e Bannon:158:ec3f221 Bannon:159:ff10c83 Bannon:160:050d073 Bannon:161:730ecba Bannon:162:28ac28a Bannon:163:625042d game-reverse-engineering:84:caeddb0 game-reverse-engineering:96:2102b48 M.-Engine-:25:8b7748a dream-girl:91:aead7a8 physics-playground-pwa:246:be206f5 pokemon-arena-2d:1:0f49580 pokemon-arena-2d:2:59cef62"
: > "$OUT/cand_status.txt"
for c in $CANDS; do
  r="${c%%:*}"; rest="${c#*:}"; n="${rest%%:*}"; h="${rest##*:}"
  st=$(gh api "repos/mhvnsnt/$r/commits/$h/status" --jq '{state: .state, n: (.statuses | length), ctx: [.statuses[].context]}' 2>/dev/null | tr -d '\n ')
  echo "$r #$n $h $st" >> "$OUT/cand_status.txt"
done
# AO #962 (13:44Z queue-sync PR): state + merged?
gh api repos/mhvnsnt/agent-ops/pulls/962 --jq '{state, merged, mergeable, head: .head.sha[0:7], title}' > "$OUT/ao962.json" 2>&1
# WH newest open PRs (anything above #1778)
echo "--- tips ---"; cat "$OUT/tips.txt"
echo "--- open counts ---"; cat "$OUT/open_counts.txt"
echo "--- cand status ---"; cat "$OUT/cand_status.txt"
echo "--- ao962 ---"; cat "$OUT/ao962.json"
echo "--- errors ---"; grep -l . "$OUT"/err-*.txt 2>/dev/null | head; cat "$OUT"/err-*.txt 2>/dev/null | head -20
