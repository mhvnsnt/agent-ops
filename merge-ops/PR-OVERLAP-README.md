# Merge serialization — research + recommendations (friction task C, 2026-10-22)

**Problem:** merge-order hazards with the PR pile-up. 2026-10-22: western-heart
PR #497 carried old geometry while PR #508's fix ("feet point forward on all Doc
Frank models") merged first — the #497 lane had to rebase preserving #508's fix,
and an in-flight A4 rig was built on pre-#508 geometry. Cluster 03 (2026-10-19)
covered CI minutes + self-hosted runners; it did NOT cover merge ordering.

## Verdicts (all verified against live sources 2026-10-22)

| Candidate | License / cost | Verdict |
|---|---|---|
| **GitHub native merge queue** | $0 — available in any public org repo; Actions minutes free on public repos | **RECOMMEND as pilot** — true serialization via `merge_group` (each PR CI-tested against base + everything queued ahead). Fixes the #497/#508 class: a PR built on old main gets re-validated against current main before landing. Requirements: branch protection "Require merge queue" + required checks; CI workflows must add `merge_group` as a trigger or the queue stalls. Merge method MUST be "merge" (never squash/rebase — owner law). **Needs OWNER APPROVAL** — enabling changes repo behavior; pilot on 1–2 busy repos (e.g. western-heart) first, kill it if it slows lanes. |
| **Kodiak** (chdsbd/kodiak) | **AGPL-3.0** (verified via live `gh api` license call — NOT MIT as commonly assumed); hosted SaaS, paid seats optional | **SKIP for ordering** — label-gated automerge only; it merges green PRs independently and does NOT serialize, so it cannot fix the hazard class we hit. |
| **bors-ng** | **Apache-2.0** (verified) — free/open-source | **SKIP** — strongest serialization (staging-batch + bisect) but setup tax is far too heavy: separate app, `staging`/`trying` branches, CI reconfigured to report Statuses, comment-driven `bors r+` workflow fights the lane-merge flow. |
| **Mergify** | Free for open-source/public repos (pricing page crawled 2026-10-21); paid tiers per active contributor | **CONDITIONAL** — merge queue with batching + `Depends-On` chains (even cross-repo: "merge #508 before #497" declared explicitly), works WITHOUT touching CI. Only after a native-queue pilot proves the concept; confirm free-tier limits for a 135-repo org first. Third-party app on the merge path = vendor dependency. |

## Wired now (no approval needed)

`merge-ops/pr-overlap.sh` — read-only `gh` calls: lists open PRs (number, title,
branch, mergeable/mergeStateStatus, file list), computes pairwise file overlaps,
flags CONFLICTING pairs and suggests merge order (older first, then rebase).
Run before merge batches or wire into the merge-review lane brief. It makes the
hazard visible; enforcement follows via the merge-queue pilot.

Live-tested 2026-10-22 against `mhvnsnt/agent-ops`: correctly listed 17 open PRs
and flagged real overlaps (e.g. CLAIMS.md shared by PRs #9/#10/#11/#24, several
already CONFLICTING).

Sources: docs.github.com merge-queue docs (managing-a-merge-queue,
merging-a-pull-request-with-a-merge-queue, managing-auto-merge),
kodiakhq.com/docs, bors.tech/documentation, mergify.com/pricing +
/product/merge-queue + /compare/github-merge-queue (crawled Oct 2026).
