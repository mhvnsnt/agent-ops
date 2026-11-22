# Western Heart PR conflict resolution — 2026-10-20
Lane: forward-merge origin/main into each CONFLICTING PR branch, keep both sides, push, no merges.
PRs in scope: #359 #357 #355 #345 #338 #337 #325 (all CONFLICTING/DIRTY, non-draft, owner-authored — none skipped).
PR #363 (Cluster C) is also CONFLICTING but NOT in this lane's scope.

## PR #359 — RESOLVED by sibling lane (not by this lane)
- Branch moveset-cluster-b-t7 was at 74efb3fb (CONFLICTING) when this lane started.
- This lane computed a full keep-both-sides resolution (10 moveset JSONs unioned: T7 branch moves + T3 main moves, same-key collisions kept as '<key>'/'<key>__main'; movesets.js auto-merged; 0 deletions) and built the merge commit server-side via the git-database API (tree a644bd39, commit 1f281dee, parents 74efb3fb+c9655c33).
- Before pushing, the branch moved to 71fe2ffe: sibling lane had pushed its own forward-merge ("Merge origin/main into moveset-cluster-b-t7 (forward-merge, PR #359)", parents 74efb3fb+caa33fc2). This lane did NOT push (would have duplicated/raced).
- Verified sibling's result keep-both-sides: bruno.json has 296 moves (matches this lane's union count), t7_base AND t3_bank metadata both present.
- PR #359 now MERGEABLE/CLEAN. Resolution only; left for merge-law-ci-watch to merge.

## PR #357 — already MERGED (no action)
## PR #355 — already MERGED (no action)
## PR #325 — already MERGED (no action)
(All three show state=MERGED; mergeable UNKNOWN because closed. Nothing for this lane to do.)

## PR #345 — RESOLVED + PUSHED by this lane
- Branch stream3/arena-pull-20261019 (was af5c9960, CONFLICTING) forward-merged with origin/main (bbe1bce2) via server-side merge commit 5361bfaf (git-database API: blobs + tree + commit + ref update, fast-forward only).
- 4 conflicted files, both sides kept, zero deletions: main.js / roster-full.js / styles.css clean textual merges; stages.js buildNoMercy keeps BOTH geometry paths (branch GLB + main OBJ fallback), STAGE_TIERS keeps both 'WWF NO MERCY' and 'WRESTLING'.
- PR #345 now MERGEABLE/UNSTABLE (CI pending — merge-law-ci-watch's domain). Comment posted on PR. Not merged by this lane.

## PR #337 — already MERGED (no action)
- Branch burger/kusaregedo-kit-20261019 tip 34871531 is fully contained in main; bbe1bce2 is the merge commit ("Merge pull request #337"), merged 2026-10-20T18:03:57Z. Nothing for this lane to resolve.

## PR #338 — RESOLVED + PUSHED by this lane
- Branch stream6/combat-100-20261019 (was 1a0aec84, CONFLICTING) forward-merged with origin/main (559fddde) via server-side merge commit 4cc6b41b (git-database API: 56 blobs + tree + commit + ref update, fast-forward only, tip verified before push).
- 56 conflicted files, both sides kept, zero deletions: 49 moveset JSONs unioned (branch combat moves + main additions; same-key collisions as '<key>'/'<key>__main'); fighter.js kept branch cainelias mapping + main intake block; input.js kept branch tekken limb input + main TRANSFORM touch input; movesets.js kept branch cainelias id + main fighter list; index.html/game.js/main.js/styles.css clean textual merges.
- PR #338 now MERGEABLE/UNSTABLE (CI pending — merge-law-ci-watch's domain). Comment posted on PR. Not merged by this lane.

## SUMMARY
| PR | Result |
|----|--------|
| #359 | Resolved by sibling lane (verified keep-both-sides); MERGEABLE/CLEAN |
| #357 | Already MERGED — no action |
| #355 | Already MERGED — no action |
| #345 | Resolved+pushed by this lane (5361bfaf); MERGEABLE/UNSTABLE |
| #338 | Resolved+pushed by this lane (4cc6b41b); MERGEABLE/UNSTABLE |
| #337 | Already MERGED — no action |
| #325 | Already MERGED — no action |

No PRs merged by this lane (resolution only, per task). No DRAFTs, no owner-excluded PRs in scope. PR #363 (Cluster C, CONFLICTING) was not in this lane's assigned scope.
