# HANDOFF — REPOS (per-repo state + landing order)

State verified 2026-10-23. Sources: `MERGE-QUEUE.md`, `CROSS-REPO-STRANDED-AUDIT-2026-10-23.md` (live `gh` API audit, classification only — nothing was merged by the audit). Fleet pattern: of 69 open PRs audited outside western-heart, only 2 are conflicting (both Bannon). The dominant failure is finished, MERGEABLE work sitting unmerged — mostly CI-blocked (GitHub Actions quota outage; resets 2026-11-01 per records). Content is done; merges are what's owed.

## Prioritized landing order (cross-repo)

1. **wrestling-game W5 Def Jam set** #14 → #15 → #16 → #17 → #18 (unblocks the never-run western-heart CATALOG wiring).
2. **No Mercy wrestlers + teardown mirror, once, in wrestling-game** (#9, #13); then close the Bannon twins #87/#92 as duplicates.
3. **GRE SF EX phases** #42 → #43 → #44 → #45.
4. **GRE SCII stack** in phase order, then Tekken 5 set, YYH set, W1 #38; deletion-guard check on GRE #10 first.
5. **Law/doc dedup** — one anti-clobber + one MERGE-IT-YOURSELF + render-orientation per repo (verified MISSING from wrestling-game, GRE, ConcreteDragon mains), plus PRs for the shared `docs/sale-status-owner-rule-2026-10-14` branch (stranded in 3 repos).
6. **ConcreteDragon** — branch-protection decision unblocks all 4 PRs; then PRs for `feature/customization-suite` (11 commits) and `content/waves-2-4`.
7. **Bannon** — rig line #77/#48, playable line #49/#41, conflict work on #39/#38 (keep both sides), close empty #22.
8. **Local-only payloads** — commit `~/workspace/wrestling-work/` (6 move FBX + 6 JSON) into wrestling-game; resolve the uncommitted local agent-ops clone edits.

## mhvnsnt/wrestling-game — 11 open / 7 merged; ALL 11 stranded, ALL mergeable (CI-blocked)

- W5 Def Jam set: #14 reconciliation, #15/#16/#17 = the 912 extracted parts (42+217+653 files), #18 microcode valid-negative. See HANDOFF-TEARDOWNS.md.
- #9 No Mercy wrestlers (13 GLBs) — verified: `models/` on main holds ONLY WMXIX. Bannon #87 is the duplicate twin.
- #13 teardown mirror (139 files, +63,917 lines). Bannon #92 is the twin.
- #10 render-orientation, #6 MERGE-IT-YOURSELF law, #11/#12 anti-clobber duplicate pair (land ONE).
- Branch-only: `docs/sale-status-owner-rule-2026-10-14`. Local-only: `~/workspace/wrestling-work/` FBX+JSON set (never committed anywhere, not a git repo).

## mhvnsnt/game-reverse-engineering — 33 open / 11 merged; ALL 33 stranded, ALL mergeable (CI-blocked)

- SF EX #42–#45, SCII 10-PR stack (tip #40 = 144 commits ahead), Tekken 5 ×7, YYH ×3, W1 census #38, research #29, tooling #9/#7 — details in HANDOFF-TEARDOWNS.md.
- #10 RE tooling pull-in (905 files) has **−2 deletions** — deletion-guard check BEFORE merging.
- #12/#13 anti-clobber duplicate pair (land one). Branch-only: `feat/re-toolchain-research-20261016` (ahead 8), `watchdog/tekken6-decrypt-callgraph-20261015` (ahead 4), sale-status docs branch.
- **ORPHAN-HISTORY WARNING:** 7 branches have NO common ancestor with main and cannot be PR'd normally: `master`, `offload-push`, `push-clean`, `tekken-pull-verify-20261013`, `watchdog/doa4-download-fix`, `watchdog/wrestling-teardown-20261013`, `feat/ymg-skinning-decoder`. Archive each tip to a release; **deletion only with the owner's per-item sign-off — never delete on your own call.**

## mhvnsnt/Bannon — 18 open / 70 merged; backlog dormant (both Bannon checkpoints = done)

- Stranded-unique (11): rig line #77 (rig-repair pipeline) + #48 (rig hardening); playable line #49 (Stick-Up v2 cinematic) + #41 (PWA-sync CI); #84, #80, #88, #83; doc-family PRs.
- CONFLICTING/DIRTY (2): #39 reality audit, #38 grapple solver (oldest substantive PR in the fleet, from Aug 4). Conflict work keeps both sides.
- Duplicates: #87 = wrestling-game #9, #92 = wrestling-game #13 (land there, close these). #89 anti-clobber partially landed (main AGENTS.md has 1 mention — verify full text before closing). #22 "Aye" = 0 files, close candidate (owner call).
- Drafts: #78 Stick Up HQ = **OWNER-EXCLUDED, do not merge**; #43/#44/#45 dormant.

## mhvnsnt/ConcreteDragon — 4 open / 56 merged; ALL blocked by branch protection on main

- #62 Quantum Jam prep — the jam is OVER (ran Sep 25–28, 2026; nothing was ever submitted). Owner decision: land the district build as ordinary repo work, or close.
- #59 render-orientation; #60/#61 anti-clobber duplicate pair.
- Branch-only: `feature/customization-suite` (11 ahead — biggest stranded CD branch), `content/waves-2-4` (4), `weight-paint-pwa` (3), + 5 more. PR them.
- Local-only: itch staging `~/workspace/concrete-dragon-itch/` untouched since Oct 9 — the blocker is the owner's manual itch.io payout setup, not code.

## mhvnsnt/cape-jones — 3 open / 207 merged; HEALTHY — 0 stranded

- All 3 open PRs are MERGEABLE + CLEAN but **OWNER-HELD**: #167 mesh-repair, #156/#157 sitting takes (the sitting choice is the owner's). Do not merge.
- 176 remote branches look alarming; sample-verified 8/8 fully contained in main (ahead_by=0) — merged-but-never-deleted hygiene debt, not stranded work.
- Local clone is dirty (~10.4k unstaged deletions, anim-stack donor files, contained on main) — lane-owned; don't touch.

## mhvnsnt/agent-ops — this repo

- #40 cross-repo stranded audit — MERGEABLE, CI unstable; merge when green. #29 owner-authored docs PR — CONFLICTING since 2026-10-21; rebase keeping both sides (no auto-merge per anti-clobber).
- The local clone at `~/workspace/agent-ops` carries uncommitted edits on branch `docs/research-conventions-20261016` — resolve (commit via PR or discard with cause), don't let them rot.

## mhvnsnt/western-heart — summary (full handoff: HANDOFF-WESTERN-HEART.md)

112 open / 607 merged PRs, 759 branches, 89 releases. Landing waves: wiring → models → movesets → rigs → canon. Owner-held: PR #377 (evidence, never merge). Playtest gate in force — see HANDOFF-WESTERN-HEART.md.

## Owner-held / do-not-merge (fleet-wide, binding)

Bannon #78 (excluded draft) · western-heart #377 (evidence) · cape-jones #156/#157 (do-not-merge) · cape-jones #167 + sitting takes (owner decision pending) · ConcreteDragon #62 (owner decision: land or close) · Bannon #22 + GRE's 7 orphan branches (owner deletion/close calls only).
