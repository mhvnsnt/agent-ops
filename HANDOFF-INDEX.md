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
