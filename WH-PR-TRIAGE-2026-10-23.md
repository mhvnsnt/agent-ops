# WESTERN-HEART PR TRIAGE — 2026-10-23

**Snapshot:** 2026-10-23 ~15:35 CDT (20:35 UTC). Read-only triage — nothing merged, pushed, or commented by this run.
**Repo:** mhvnsnt/western-heart. **Open PRs at snapshot: 50** (audit counted 112; the idle merge lane has landed ~62 since).
**⚠️ The merge lane is LIVE:** PR #833 merged at 20:31 UTC *during* this triage. Counts below are snapshot-accurate; the lane may have landed more since.

## BUCKET COUNTS

| Bucket | Count | PRs |
|---|---|---|
| MERGE-READY | 4 | #825, #812, #831, #821 |
| FIXABLE | 29 | #833, #834, #832, #718, #442, #822, #744, #741, #734, #723, #721, #720, #719, #717, #716, #715, #713, #704, #703, #711, #710, #709, #701, #685, #644, #449, #393, #498, #499 |
| CONFLICT | 9 | #826, #806, #714, #712, #706, #678, #668, #665, #497 |
| OWNER-DECISION | 4 | #377, #722, #446, #182 |
| CLOSE-CANDIDATE | 4 | #464, #660, #636, #206 |
| WATCH | 0 | — (all phase stacks resolved today; see Urban Reign) |

Rule notes: #833 was MERGE-READY/FIXABLE at snapshot but **merged by the lane at 20:31 UTC** — it validates the triage criteria (its latest instruction-gate run at 20:25 was success; the lane merged it 6 min later). #377 stays open as evidence per owner — never merge/close. #722's title/body carries an explicit MERGE FREEZE — never merge while the freeze stands.

---

## MERGE-READY (4)

Mergeable, checks acceptable, no unexplained deletions. Merge-commit only; verify payload on main after.

| PR | Title | Mergeable / state | Checks | +/-/files | Blocker |
|---|---|---|---|---|---|
| [#825](https://github.com/mhvnsnt/western-heart/pull/825) | Rig and wire Buffalo Bill (Marshall Law bank) + re-rig Thor | True / clean | 6/6 pass, gate success | +100/-3, 8 | none |
| [#812](https://github.com/mhvnsnt/western-heart/pull/812) | Input resolver V2: deterministic Tekken input (fixes neutral …) | True / clean | 6/6 pass, gate success | +14630/-3, 9 | none |
| [#831](https://github.com/mhvnsnt/western-heart/pull/831) | Teardown coverage audit: COVERAGE.md + coverage.json | True / unstable | gate success; guard + deletion-guard **in_progress at snapshot** | +191/-0, 4 | wait for / re-check the 2 in-progress runs |
| [#821](https://github.com/mhvnsnt/western-heart/pull/821) | t122u: fix untappable main menu on phone + Playwright touch | True / unstable | gate success; menu-touch-e2e, guard, deletion-guard **in_progress at snapshot** | +107/-0, 11 | wait for / re-check the 3 in-progress runs |

## FIXABLE (29)

One concrete fix each — no owner input needed. "Rebase" below = merge main into the branch (never rebase/force-push shared branches per lane rules), keep both sides, then re-run checks.

| PR | Title | State | Exact fix |
|---|---|---|---|
| [#833](https://github.com/mhvnsnt/western-heart/pull/833) | TTT2 surgical extraction pipeline (Law/Lars lane) | True / unstable | **LANDED DURING TRIAGE (20:31 UTC).** At snapshot: gate had success (20:25) + stale failure (20:23) — nothing to fix, just needed the merge. |
| [#834](https://github.com/mhvnsnt/western-heart/pull/834) | ci: ui_sources gate, no unsourced menu changes | True / unstable | **Body fix only:** gate 20:24 fails "Proof ref is not a file, commit, tag, release or branch of this repo: screen-daily / legacy-unsourced / screen-*". Replace with real paths/branches. All other checks pass. |
| [#832](https://github.com/mhvnsnt/western-heart/pull/832) | Submenu: versus setup rebuilt from Tekken 7 GAME OPTION | True / unstable | **Body fix only:** gate 20:36 fails "'Method actually used' differs from 'Method the owner specified' but Deviations says none." Align the method section or add the deviation with owner approval link. |
| [#718](https://github.com/mhvnsnt/western-heart/pull/718) | Worker 72: T5/T6/TTT2/T7 teardown completion report | True / unstable | **Body fix only:** gate 00:56 fails "Proof path not in this PR's diff or the repo: ttt2-7z-v1 / tekken6-ps3-full-v1 / tekken5-iso-v1 / tekken5-disc-v1 / worker72/t5-t6-ttt2-teardown-completion" — these are release names, not paths. Repoint proofs at real paths or release links. |
| [#442](https://github.com/mhvnsnt/western-heart/pull/442) | Urban Reign phase 2: native .gyu motion conversion | True / unstable | **Body fix + base decision:** gate fails on 5 missing sections (Self-check, Proof, Deviations, Method specified, Method used). **Payload verified NOT on main** (3/3 sample paths 404). Native .gyu sources exist on main under teardown/urban-reign/motion/ but the converted banks (game/assets/anim/ur-general-*/) do not. Lane must decide: retarget base to main, or confirm phase-6 AFS bank supersedes it. See Urban Reign section. |
| [#822](https://github.com/mhvnsnt/western-heart/pull/822) | WORKLOG: merge steward pass 2026-10-23 | dirty / gate success | Trivial: merge main in (11+/0, 1 file), checks already green. |
| [#744](https://github.com/mhvnsnt/western-heart/pull/744) | Worker 84: Gyou spirit body archive (Tripo fiery humanoid) | dirty / gate failure | Rebase (110+/0, 5 files) + gate re-run (post-#828 body fix). |
| [#741](https://github.com/mhvnsnt/western-heart/pull/741) | Worker 83: Nine Souls character-select redesign | dirty / gate failure | Rebase (567+/8, 10 files) + gate re-run. |
| [#734](https://github.com/mhvnsnt/western-heart/pull/734) | docs: lock Kuma replacement display name as GASHADOKURO | dirty / gate failure | Rebase (10+/3, 2 files) + gate re-run. |
| [#723](https://github.com/mhvnsnt/western-heart/pull/723) | Worker 77: SCIMITAR ATTIRE 1 ARCHIVE + SPEC | dirty / gate failure | Rebase (47+/0, 4 files) + gate re-run. |
| [#721](https://github.com/mhvnsnt/western-heart/pull/721) | archive(yukihyo): Attire 3 Tiger King source model | dirty / gate failure | Rebase (1+/0, 2 files) + gate re-run. |
| [#720](https://github.com/mhvnsnt/western-heart/pull/720) | archive(bruno): Attire 1 + Attire 2 source models | dirty / gate failure | Rebase (113+/1, 6 files) + gate re-run. |
| [#719](https://github.com/mhvnsnt/western-heart/pull/719) | Dio Attire 1 + Million Eyes Demon transformation Tripo archive | dirty / gate failure | Rebase (82+/0, 6 files) + gate re-run. |
| [#717](https://github.com/mhvnsnt/western-heart/pull/717) | archive(sweep): tpose-delivery proof renders + sweep record | dirty / gate failure | Rebase (105+/0, 13 files) + gate re-run. |
| [#716](https://github.com/mhvnsnt/western-heart/pull/716) | archive(kuma-replacement): Attire 1 Tripo source model | dirty / gate failure | Rebase (68+/0, 5 files) + gate re-run. |
| [#715](https://github.com/mhvnsnt/western-heart/pull/715) | archive+eyeglow(negativo): Tripo A1/A2 + CornerStone A1 | dirty / gate failure | Rebase (261+/14, 16 files) + gate re-run. |
| [#713](https://github.com/mhvnsnt/western-heart/pull/713) | VF5 motion pipeline: Dural stance for Zen (worker 60) | dirty / gate failure | Rebase (11+/1, 4 files) + gate re-run. |
| [#704](https://github.com/mhvnsnt/western-heart/pull/704) | VF5 full integration — worker 57 re-dispatch | dirty / gate failure | Rebase (174+/0, 3 files) + gate re-run. |
| [#703](https://github.com/mhvnsnt/western-heart/pull/703) | archive(buffalo-bill,theory): Buffalo Bill A1/A2 + Theory A1 | dirty / gate failure | Rebase (164+/0, 20 files) + gate re-run. |
| [#711](https://github.com/mhvnsnt/western-heart/pull/711) | Worker 66: in-suite hand-tooling with headless Blender | dirty / gate failure | Rebase (1452+/1, 11 files) + gate re-run. |
| [#710](https://github.com/mhvnsnt/western-heart/pull/710) | worker65: WWE CAW drives the creation suite | dirty / gate failure | Rebase (505+/7, 5 files) + gate re-run. |
| [#709](https://github.com/mhvnsnt/western-heart/pull/709) | Clothing remove/change system + labeling standard | dirty / gate failure | Rebase (738+/3, 16 files) + gate re-run. |
| [#701](https://github.com/mhvnsnt/western-heart/pull/701) | FIGHT-LOOP CRASH REPAIR (worker 54): restore clobbered hitfx | dirty / **gate latest success (21:42)** | Rebase only (353+/49, 5 files); gate already green on latest run. High value — crash repair. |
| [#685](https://github.com/mhvnsnt/western-heart/pull/685) | Worker 29: Training mode depth + replays | dirty / no checks ran | Rebase (1959+/13, 21 files); push to trigger checks. |
| [#644](https://github.com/mhvnsnt/western-heart/pull/644) | Worker 20: HEART AND MIND WITHIN phase 1 | dirty / no checks ran | Rebase (2306+/189, 23 files); push to trigger checks. |
| [#449](https://github.com/mhvnsnt/western-heart/pull/449) | CornerStone Attire 1: owner's Tripo model wired | dirty / no checks ran | Rebase (2203+/12, 10 files); push to trigger checks. |
| [#393](https://github.com/mhvnsnt/western-heart/pull/393) | Pose isolation fix: own-stance idle/walk, Chest->Spine2 | unknown / no checks ran | Branch valid; mergeable never computed. Rebase/merge main in (1030+/345, 17 files) to trigger mergeable + checks. |
| [#498](https://github.com/mhvnsnt/western-heart/pull/498) | Re-derive Pantera skin weights via k-NN from steve-fox donor | dirty / gate failure | **Body semantic fix:** gate 04:41 fails "'Method actually used' differs from 'Method the owner specified' but Deviations says none." Align method sections or add deviation w/ approval link; then rebase (438+/0, 3 files). |
| [#499](https://github.com/mhvnsnt/western-heart/pull/499) | W3c AKI CORRECTIVE: true clips (base: feat/aki-fk-ik-rock-20261021) | True / unstable / gate failure | **Body format fix:** gate 04:36 fails on 4 missing sections — Self-check, Proof, Deviations, Owner instruction (verbatim quote). Add them. Base is the live AKI feature branch, mergeable. |

Note on the mass instruction-gate failures: PR #828 ("Instruction gate: use the PR's current body, not the stale event", merged 20:09 UTC) fixed the gate to read the PR's current body. Gate failures from **before** 20:09 UTC were likely stale-body false failures — a re-run is the fix, not a body rewrite. Failures **after** 20:09 (#832 at 20:36, #834 at 20:24) are real semantic issues with exact causes named above.

---

## CONFLICT (9)

Needs a dedicated conflict lane: merge main in, keep BOTH sides, never drop either side's work, then merge when green.

| PR | Title | +/-/files | Overlapping areas / why it's not trivial |
|---|---|---|---|
| [#826](https://github.com/mhvnsnt/western-heart/pull/826) | T7 character select rebuild: 2-row grid, 1P/2P cursors | +1232/-352, 10 | 352 deletions in select UI the lane touched TODAY (#830 select phone fix merged 20:18, #821/#832 open). Gate also fails (deviation approval links). Real overlap. |
| [#806](https://github.com/mhvnsnt/western-heart/pull/806) | Law full pull for Buffalo Bill: anim bank + moveset + stance | +148135/-39, 40 | 148k-addition Law bank pull; zero checks have ever run. Needs lane to run gates + resolve vs main. |
| [#714](https://github.com/mhvnsnt/western-heart/pull/714) | worker68: CORNERSTONE moveset — Yamazaki 3D KOF + Rock + Togashi | +5691/-585, 15 | 585 deletions unexplained at triage; moveset area overlaps #678 library work. |
| [#712](https://github.com/mhvnsnt/western-heart/pull/712) | Worker 61: owner-repo mining — animations, customization parts | +5059/-6, 138 | 138 files across repo-mining surface; broad conflict footprint. |
| [#706](https://github.com/mhvnsnt/western-heart/pull/706) | w59: Ashlane->DOA claimed-map lock + DOA4/KOF3D federation | +12315/-1359, 34 | 1,359 deletions need per-line justification vs today's merges. |
| [#678](https://github.com/mhvnsnt/western-heart/pull/678) | Moveset Library System: central 9,420-move library | +453807/-0, 21 | 453k-addition library; gate now green on latest run (20:57) but branch is dirty. Dedicated lane to rebase the giant payload. |
| [#668](https://github.com/mhvnsnt/western-heart/pull/668) | Worker 24: TTT2 team battle in versus (v2) | +922/-17, 11 | Overlaps versus-submenu area (#832) and select area touched today. Keeps #660 as the closed duplicate (see below). |
| [#665](https://github.com/mhvnsnt/western-heart/pull/665) | Eastern Mind assets incorporated + generative AI canon pass | +1830/-7, 25 | 25 files; instruction-gate failed 3x (body issues) + dirty. Canon-sensitive content — lane must fix body AND conflicts. |
| [#497](https://github.com/mhvnsnt/western-heart/pull/497) | T3 bank facing: fix the backwards bake at the source | +681/-501, 162 | **Regression risk:** conflicts against the merged #508 feet fix (Doc Frank feet). Lane must keep BOTH the facing fix and #508's correction. Gate is green (success) — conflict is the only blocker. |

---

## OWNER-DECISION (4)

Concrete questions for the owner — no lane action until answered.

| PR | Title | Question for the owner |
|---|---|---|
| [#377](https://github.com/mhvnsnt/western-heart/pull/377) | [DO NOT MERGE - tool fails rig] Wire Keemap into anim-retarg | **Stays open as evidence per your standing order** — mergeable, gate green, 22k additions. No action; listed here so no lane touches it. Confirm: keep open indefinitely as evidence, or is there a close condition? |
| [#722](https://github.com/mhvnsnt/western-heart/pull/722) | Worker 75: SmutBase intake repair (MERGE FREEZE, do NOT merge) | Title AND body say **"MERGE FREEZE: merge-ready, do NOT merge."** Respected — no lane will merge it. Question: is the freeze still in effect, or lifted? If lifted, it becomes MERGE-READY (gate needs one re-run; 278+/0, all other checks pass). |
| [#446](https://github.com/mhvnsnt/western-heart/pull/446) | Tekken 6 PSP SOLVED: 76/76 adler-exact | **597,293 additions / 3,765 files** in one PR; mergeable never computed, zero checks ran. Question: land this as one giant merge commit, or split it (e.g. tools → release, traces → release, docs → PR)? A 597k-addition merge will swamp git history and CI. |
| [#182](https://github.com/mhvnsnt/western-heart/pull/182) | RESEARCH (do not merge): rig auto-fix survey | Draft, marked do-not-merge, branch diff is 5M deletions vs current main (ancient fork). Question: close it as dead research, or keep open as a reference document? |

---

## CLOSE-CANDIDATE (4)

| PR | Title | Why |
|---|---|---|
| [#464](https://github.com/mhvnsnt/western-heart/pull/464) | Urban Reign phase 3: textures + general-pool assignment | **Empty diff: +0/-0, 0 files** vs its base (ur-phase3-textures == ur-phase2-motion tip). Payload already flowed up the chain and landed via #820. Nothing to merge. |
| [#660](https://github.com/mhvnsnt/western-heart/pull/660) | Worker 24: TTT2 team battle in versus | **Superseded by #668** (v2, created 19 min later, same worker/topic). No checks ever ran on #660. |
| [#636](https://github.com/mhvnsnt/western-heart/pull/636) | T-pose urgent batch: Mirko render | Single proof PNG, superseded by later t-pose deliveries (#717 archive, #722 freeze PR). No code. |
| [#206](https://github.com/mhvnsnt/western-heart/pull/206) | Research: 3D pipeline 2026 | **Empty diff: +0/-0, 0 files** vs main. Nothing to merge. |

---

## URBAN REIGN PHASE STACK — current state (verified this run)

- **#784** (old tip, was CONFLICTING): **merged 19:31 UTC** via merge commit 61d8e2fd — but its recorded diff vs its merge base showed 100 files as *removed* (AGENTS.md, CANON.md, .github/workflows, instruction gate, …). Investigated: main is intact — AGENTS.md last touched by #707 at 19:56 UTC, instruction-gate.yml last touched 04:33 UTC, all return 200 on main. The merge did not wipe main's files.
- **#506 / #518 / #548**: all merged 16:09 UTC branch-to-branch (phase4→phase3, phase5→phase4, phase6→phase5).
- **#820** ("RESOLVED: Urban Reign phases 3-6 stack tip → main (conflict-resolved)", branch ur-phase6-bank-completion-resolved-20261023): **merged 19:31 UTC**, merge commit 2a6b5b21. Spot-checked 6/6 sampled files **blob-identical on main**. This is the real UR landing: 200+ files (game/assets/movesets/ur-*.json, teardown/urban-reign/**, textured models/textures).
- **#464** (phase 3 stacked PR): empty diff — close candidate.
- **#442** (phase 2, native .gyu motion conversion): **STILL OPEN and its payload is NOT on main** (3/3 sampled paths 404). The native .gyu sources exist on main (teardown/urban-reign/motion/*.gyu), but phase 2's converted banks (game/assets/anim/ur-general-*/clips.json, rows.pack.json, skeleton.json — 83 files, +13,415) are absent. Either the #820 resolution deliberately dropped them (phase-6 AFS bank supersedes?) or they fell out. **UR lane decision needed** — flagged in FIXABLE with the exact gate body fix.
- Net: phases 3–6 are on main; phase 2's converted output is the one open gap.

## #497 / #498 / #499 — current states (verified this run)

- **#497** (T3 bank facing fix): mergeable=false/dirty, **instruction-gate SUCCESS**, +681/-501 over **162 files**. → CONFLICT. Dedicated lane must rebase keeping both this fix and the merged #508 feet fix (regression risk named in prior triage confirmed by the conflict).
- **#498** (Pantera k-NN skin weights): mergeable=false/dirty, gate FAILURE — exact cause from annotations: *"'Method actually used' differs from 'Method the owner specified' but Deviations says none."* → FIXABLE: fix the body (align method or add deviation + approval link), then rebase (438+/0, 3 files).
- **#499** (W3c AKI true clips → base feat/aki-fk-ik-rock-20261021): mergeable=true/unstable, gate FAILURE — exact cause: 4 missing body sections (Self-check, Proof, Deviations, Owner instruction verbatim quote). → FIXABLE: add the sections; no conflict.

## FALSE-DONE SPOT CHECK (5 recently merged PRs, contents API vs main)

| PR | Merge commit | Sampled files blob-identical on main | Verdict |
|---|---|---|---|
| #820 Urban Reign tip (resolved) | 2a6b5b21 | 6/6 | REAL DONE |
| #828 Instruction gate live-body fix | ea9873e8 | 2/2 | REAL DONE |
| #829 tekken6 DINF tools restore | f8c9d0ec | 3/3 | REAL DONE |
| #830 select phone layout fix | 13aa3168 | 3/4 | REAL DONE — 1 SHA mismatch on docs/WORKLOG.md, expected: WORKLOG.md is append-only and later merges moved it after #830 landed |
| #784 Urban Reign tip (old) | 61d8e2fd | n/a (diff recorded as removals vs old base) | Investigated — main intact (see Urban Reign section). The effective payload landed via #820. |

No false "done" found. One genuine gap found instead: **#442's phase-2 converted motion banks are not on main** (open PR, not a false merge claim).

---

## TOP 10 MERGE-READY / NEXT-UP, ranked by value

1. **#812 — Input resolver V2** — clean, 6/6 green. Deterministic Tekken input, fixes neutral-input bugs. Core fight-loop value.
2. **#825 — Rig and wire Buffalo Bill (Marshall Law bank) + re-rig Thor** — clean, 6/6 green. Fighter rigging is the owner's top priority class.
3. **#831 — Teardown coverage audit** — gate green, 2 checks in-progress at snapshot. Tiny docs payload; unblocks coverage tracking.
4. **#821 — t122u phone menu touch fix** — gate green, 3 checks in-progress at snapshot. Phone playability.
5. **#701 — FIGHT-LOOP CRASH REPAIR** — gate already green on latest run; needs only a rebase (353+/49, 5 files). Crash repair = high value.
6. **#442 — UR phase 2 motion conversion** — the one verified gap in the UR stack on main; body-section fix + base decision, then mergeable.
7. **#832 — versus setup submenu rebuild** — mergeable, one body semantic fix (method/deviation alignment), then green.
8. **#718 — T5/T6/TTT2/T7 teardown completion report** — mergeable, one body fix (proof refs are release names, repoint to paths).
9. **#834 — ui_sources gate** — CI infra enforcing the owner's no-unsourced-menus law; one body fix (bad proof refs).
10. **#497 — T3 bank facing fix** — gate green; needs the dedicated conflict lane vs #508 (keep both). Ranked 10th only because it needs the most careful lane, not because it lacks value.

**Also of note:** #833 (TTT2 surgical extraction) was in this list at snapshot and **the live merge lane landed it at 20:31 UTC** — the lane is working through MERGE-READY/FIXABLE in real time.

---
*Method: REST API (api.github.com) — PR list + per-PR detail + commit check-runs + check-run annotations + contents API on main. GraphQL was 502ing at triage time; all data above is from REST. Snapshot ~20:35 UTC 2026-10-23.*
