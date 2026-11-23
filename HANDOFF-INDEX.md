# HANDOFF INDEX — fleet state, one place, no "missing"

State verified 2026-10-23. Sources: `MERGE-QUEUE.md` (this repo), `CROSS-REPO-STRANDED-AUDIT-2026-10-23.md` (this repo), teardown checkpoints in `checkpoints/`, cron job `overnight-idle-pipeline` v2 body. Anything a lane claimed that is not verified on a repo's main is labeled CLAIM in these docs. **If you are about to say something is missing, check here first — then check the MERGE QUEUE. Do not route state questions through the owner.**

## The documents

| Doc | Covers |
|---|---|
| `HANDOFF-WESTERN-HEART.md` | The game (mhvnsnt/western-heart): verified state on main, landing waves, in-flight lanes, playtest gate, engine lock |
| `HANDOFF-TEARDOWNS.md` | Every game teardown: T6, TTT2, No Mercy, Def Jam, SF EX, SCII, Tekken 5, YYH — what exists, where, what is blocked and on what |
| `HANDOFF-REPOS.md` | Per-repo state + landing order for every fleet repo, owner-held list, orphan-branch warning |
| `HANDOFF-CANON.md` | Where canon lives now, the 4 fighters with canon on main, the commit-the-day-it's-recorded rule, the truly-blank process |
| `MERGE-QUEUE.md` | THE queue: every built-but-not-landed item across all repos, with state (OPEN-PR / BRANCH-ONLY / LOCAL-ONLY / BLOCKED / LANDED-VERIFIED) |

## Fleet operating rules (overnight pipeline v2 — binding on every agent)

1. **DONE MEANS VERIFIED ON MAIN.** A piece of work is done only when its payload is confirmed present on its repo's main branch (contents API / git tree check), by the agent reporting it. A lane report, checkpoint status, heartbeat, or PR title is not proof. If you cannot verify it on main, it is not done — it belongs in the MERGE QUEUE with its real state. Never write "done", "merged", or "complete" for anything you did not verify on main yourself.
2. **QUEUE-FIRST.** Finish before starting. Every work session works the MERGE QUEUE before any new intake: merge what's mergeable, fix what's fixable, PR what's branch-only, push what's local-only. New pulls/builds are last, and anything new enters the queue the same session until it is LANDED-VERIFIED.
3. **PROGRESS = ARTIFACTS, NOT HEARTBEATS.** A checkpoint whose `updated_at` advances but which produced no new commits, files, or PR activity in 24h is STALLED, not running. Mark it stalled in the queue with what its core path is blocked on. (Failure this prevents: Tekken 6 decrypt6 sat "needs_owner" from 2026-10-16 with heartbeats flowing and zero core-path progress.)
4. **CONFLICTS KEEP BOTH SIDES.** Resolving a merge conflict by dropping either side's work is a clobber — forbidden. Merge commits only; never rebase, squash, or force-push.
5. **BLOCKERS ARE CONCRETE DECISIONS.** A blocker that needs the owner is stated as a specific question/decision, never a bare "needs owner" label. Items blocked >72h get flagged by name with their blocker.
6. **OWNER-HELD / DO-NOT-MERGE** (never merge without the owner's explicit word): Bannon PR #78 (draft, excluded), western-heart PR #377 (stays open as evidence), cape-jones PRs #156/#157 (do-not-merge), cape-jones #167 + sitting-takes PRs (owner-held decision).
7. **REPO LAW:** no repo is ever deleted; nothing gets deleted without the owner's explicit per-item sign-off. Orphan-history branches are archived, never deleted on an agent's own call.
8. **CANON RULE:** game canon, notes, and development decisions are committed to the repos the day they are recorded. Assistant memory files are a working copy, never the only home. See `HANDOFF-CANON.md`.
9. **VERIFY-DONE SWEEP:** past "done/merged" claims get re-verified against main on rotation; failures are reopened into the queue. The reopened false claims are listed at the bottom of `MERGE-QUEUE.md`.

## Picking up any workstream cold

1. Read this index, then the handoff doc for your workstream.
2. Read your items in `MERGE-QUEUE.md` — that is your work list, in landing order.
3. Verify current state yourself before acting: `gh pr view`, contents API, `git log`. Handoff docs are a map, not proof; the repos win any disagreement.
4. Work branch → PR → merge (merge commit), then verify the payload on main and mark the queue item LANDED-VERIFIED with the merge sha.
5. If you finish or stall, update the queue and the relevant handoff doc in the same PR. The next agent should never have to ask anyone where things stand.

## 2026-11-23 addendum (Lane D handoff refresh — verified live)

- **Queue: 155 open at the 2026-11-23T15:44Z overnight-pipeline run** (WH 45 + Bannon 67 + PPWA 26 + CJ 1 + PA3D 2 + GRE 4 + DG 3 + PA2D 0 + WG 2 + CD 2 + AO 1 + wrestling 2; wizard-gang-storage #4/#5 not counted in the 155 by convention). Live recount later the same day: Bannon 65 (fold-lane #456/#457 landed on `muse/web-upgrade` after the run), CJ 2 (#429 + new #445) — total 154 on the same convention.
- **CORRECTION — Bannon #78 is NOT a draft anymore.** It MERGED 2026-11-19T14:16Z despite the do-not-merge exclusion. The exclusion list above (§6) is wrong on #78: the open question is now stays-or-reverted, and that is still the owner's call. Do not re-litigate it in a lane, and do not cite #78 as "do not merge" — it is already merged.
- **Owner-held / do-not-merge, current 2026-11-23:** western-heart #377 (evidence) · cape-jones #156/#157 (do-not-merge) · cape-jones #167 + sitting takes (owner decision pending) · cape-jones #429 (AnimLab verdict, owner-held) · western-heart #1820/#1835 (CLEAN but owner-held) · western-heart #1834/#1840/#1842 (UNSTABLE, held) · western-heart #1836–#1839 (BLOCKED, held) · Bannon #424 (sync web-upgrade → main, head e094389, mergeability UNKNOWN) · pokemon-arena-3d #7/#8 (do-not-merge bodies) · dream-girl #89 (draft, do-not-merge) · physics-playground #290/#293/#294 (owner-held) · game-reverse-engineering #99 (owner-held).
- **Repo HANDOFF.md files (owner order 2026-11-22) are on main in all 17 fleet repos** and were refreshed 2026-11-23 by Lane D of the get-it-all-into-the-repos sweep. Each repo's HANDOFF.md is its pickup doc; this index + `MERGE-QUEUE.md` stay the fleet-wide map. Handoff docs are a map, not proof; the repos win any disagreement.
