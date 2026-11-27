# HANDOFF — REPOS (per-repo state + landing order)

State verified 2026-10-23. Sources: `MERGE-QUEUE.md`, `CROSS-REPO-STRANDED-AUDIT-2026-10-23.md` (live `gh` API audit, classification only — nothing was merged by the audit). Fleet pattern: of 69 open PRs audited outside western-heart, only 2 are conflicting (both Bannon). The dominant failure is finished, MERGEABLE work sitting unmerged — mostly CI-blocked (GitHub Actions quota outage; resets 2026-11-01 per records). Content is done; merges are what's owed.

## 2026-11-27 — repo/CI state (overnight pipeline 16:50Z, verified via gh API)
- **mhvnsnt/wizard-gang is GONE (404)** — repo GET + pulls list both 404. Wizard Gang work lives on **wizard-gang-storage** (open PRs #4/#5/#8) and **wizard-gang-voice-pipe** (open PRs #5/#6/#10). Do not queue anything under `wizard-gang` until the owner says whether the repo was deleted/renamed on purpose.
- **Multi-repo CI fast-fail (infra, not PR content):** Bannon (all workflows fail in ~1–2s, logs 404 BlobNotFound, since ≥Nov 25), dream-girl `ci` (validate job fails in ~3s, same BlobNotFound logs, failing since Nov 23), wizard-gang-storage + wizard-gang-voice-pipe `no-deletion-guard` (failing since Oct 17). Doc-only PRs on these repos cannot turn green until the workflows themselves are diagnosed. Do NOT merge Bannon/DG/WG PRs on this run's authority while CI is dead.
- **Dead self-hosted runner (oracle-ppp OFFLINE):** game-reverse-engineering + wrestling-game `no-deletion-guard` jobs sit QUEUED on labels=self-hosted,linux; physics-playground-pwa CI queued since Nov 26 18:25Z. PRs affected: GRE #101, wrestling #25, PPWA #304/#305/#306 — all PENDING, merge blocked until a runner returns.
- **Token limit (known):** this PAT gets 403 on REST check-runs for Bannon/PPWA/DG/GRE/wrestling/WG repos. Workaround that works: GraphQL `statusCheckRollup.state` (top-level state readable; individual check names 403) + Actions-runs API for job detail. WH + CJ + AO check-runs read fine via REST.
- WH #1864/#1865: only `speed-quality` in_progress (started 16:42:10Z) — merge when green, next run.

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

## 2026-11-23 addendum (Lane D handoff refresh — verified live, supersedes the Oct-23 counts above)

Open-PR counts below were re-counted live 2026-11-23; the Oct-23 numbers above are stale — do not use them. (Queue convention: wizard-gang-storage #4/#5 are NOT counted in the fleet total.)

| Repo | Open now | What changed since Oct 23 |
|---|---|---|
| western-heart | 45 | Landing waves through #1849 (main tip 72fead43); #911 merged; held: #1820/#1835 clean-but-owner-held, #1834/#1840/#1842 unstable, #1836–#1839 blocked |
| Bannon | 65 | Main tip 4f02c16 (#427 mocap kit follow-up). **#309/#310/#311 MERGED 2026-11-22 — the "conflicting" line above is WRONG.** Fold lane active on `muse/web-upgrade` (tip e094389): #447/#451/#454/#455/#456/#457 landed there; #424 sync-to-main OPEN, head e094389, mergeability UNKNOWN. #78 MERGED 2026-11-19 despite exclusion — stays-or-revert is the owner's call |
| physics-playground-pwa | 26 | #296/#298/#299/#300/#301 landed (tip 6da2bf7); R7 V3 PARTIAL landed (#287); #294/#290/#293 owner-held |
| cape-jones | 2 | #430–#444 landed (tip f0ece39); open #429 (owner-held) + #445 (Brotherman rig docs) |
| pokemon-arena-3d | 2 | #10 Switch 132 models landed (tip 75d2853); open #7/#8 do-not-merge |
| game-reverse-engineering | 4 | #98 (this repo's HANDOFF.md) merged; open #84/#96/#97 + #99 God Within Urban Reign Redux v0.5 manifest (owner-held) |
| dream-girl | 3 | #93 (HANDOFF.md) merged (tip 369123b); open #9/#89/#91; CUT 001R v3 staged on branch `tools/production-line-v4` (tip 7bd5ac7), NOT merged |
| pokemon-arena-2d | 0 | QUEUE CLEAR — #1/#2/#4/#5/#7 all merged 2026-11-22 |
| wizard-gang-voice-pipe | 2 | #7 + #8 (HANDOFF.md) merged (tip 8030efc); open #5/#6 |
| wizard-gang-storage | 2 | #7 (HANDOFF.md) merged (tip 2881630); open #4/#5 |
| ConcreteDragon | 2 | #75 (HANDOFF.md) merged (tip 3b31785); open #71/#74 |
| ConcreteDragon2 | 1 | #13 (HANDOFF.md) merged (tip ce6023a); open #12 |
| wrestling-game | 2 | #24 (HANDOFF.md) merged (tip 9dd4c61); open #22/#23 |
| money-machine-hq | 4 | #38 (HANDOFF.md) merged; Nov 23 daily sweep 73b4d53; open #12/#29/#36/#37 |
| code-doctor | 1 | #6 (HANDOFF.md) merged (tip c090f7c); open #5 |
| Moneymachine-private | 1 | #4 (HANDOFF.md) merged (tip dce4c78); open #3 |
| agent-ops | 1 | Syncs #1040–#1047 landed (tip 0e14200); open #952, CONFLICTING |

Fleet total on the queue convention: **154 open** (155 at the 15:44Z pipeline run; Bannon −2, CJ +1 after it).

## 2026-11-27 20:14Z addendum (overnight pipeline live sweep — supersedes the Nov-23 counts for the swept repos)
Live `gh` sweep 20:14–20:25Z, 15 repos, 86 open total: western-heart 35 (tip 7c65f7d) · Bannon 3 (tip 19f70c1) · cape-jones 1 (tip ffc5b0d) · physics-playground-pwa 28 (tip e56e317) · dream-girl 3 (tip 3ec5afc) · pokemon-arena-3d 2 (tip f238c06) · game-reverse-engineering 2 (tip f40f0c0) · wizard-gang-storage 3 (tip 2881630) · wizard-gang-voice-pipe 3 (tip 6093e88) · wrestling-game 1 (tip c9ff241) · blend-physics-playground 4 (tip 25a255a) · pokemon-arena-2d 1 (tip 1263ba2) · ConcreteDragon 0 (tip b7ffff1) · ConcreteDragon2 0 (tip 7667399) · agent-ops 0 (tip d40aec2). Bannon: Real ordered "merge everything the clean way, first things first" — round 1 (#592/#595) + round 2 (#597/#599/#601/#604/#605/#606/#607/#609/#610/#612/#614/#616/#620) all landed on main; HELD only #596 (APEX STEER question + video proof + missing tests), #600 (WIP, content landed via Stage 5), #382 (TNA draft, revive-or-drop his call). Bannon CI still dead (5 runs 20:17:46Z all failure) — merges were judgement merges on file verification, recorded not endorsed by the pipeline. money-machine-hq / code-doctor / Moneymachine-private not swept this run (Nov-23 counts carried: 4 / 1 / 1).
