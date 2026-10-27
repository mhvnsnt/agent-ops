# MERGE-QUEUE BRIEFING — CONFIRMATIONS (2026-10-24)

Owner order 2026-10-24: before the merge queue flips on western-heart (and agent-ops),
EVERY active lane must be told first and must confirm it knows. Nothing flips until
confirmations are in.

Briefing text (plain language, no jargon): western-heart `GAME-DEV-BRIEFING.md` section 11,
agent-ops `AGENTS.md` — "MERGE QUEUE — COMING SOON". Both landed 2026-10-24 (see below).

How a lane confirms: reply "merge-queue briefing confirmed" in its chat, or drop that
line as a comment on its PR, or tell the merge coordinator at its next check-in.
Record each confirmation here with lane + PR + time.

## Status

- western-heart queue plumbing: READY (PR #742 merged the merge_group triggers, 2026-10-23).
- agent-ops queue plumbing: READY (PR #39 merged the merge_group triggers, 2026-10-23 21:23Z).
- The flip itself: NOT DONE. No branch protection changed.
- Briefing landed: western-heart PR #1010 (merged 2026-10-24T21:43:29Z, merge f9306e87; GAME-DEV-BRIEFING.md section 11) + agent-ops PR #104 (merged 2026-10-24T21:43:38Z, merge cf516322; AGENTS.md). Both verified on main: merge-tree exactly the briefing files, 0 deletions.

## western-heart — open PRs at briefing time (77, listed 2026-10-24 ~16:35 CDT)

| PR | Title | Branch | Last updated | Status |
|----|-------|--------|--------------|--------|
| #1008 | Root motion: apply decoded T3 clip root_t travel during attacks (fighter.js) | `feat/root-motion-20261024b` | 2026-10-24 | MERGED 2026-10-24T21:36:17Z (merge 3275523e) — no confirmation needed |
| #995 | docs: Create-A-Move List design with custom combos | `docs/create-a-move-list-design-20261024` | 2026-10-24 | AWAITING CONFIRMATION |
| #994 | docs: Move Matching System design | `docs/move-matching-system-20261024` | 2026-10-24 | AWAITING CONFIRMATION |
| #993 | docs: button names LP1/RP2/LK3/RK4 directive (2026-10-24) | `docs/button-names-lp1-rp2-20261024` | 2026-10-24 | AWAITING CONFIRMATION |
| #992 | docs: log 2026-10-24 DO THE WORK RIGHT, NOT FAST directive verbatim | `docs/work-right-not-fast-20261024` | 2026-10-24 | AWAITING CONFIRMATION |
| #988 | fix(anims): map every T7/T8 move to its correct T3 animation row | `fix/anim-true-mapping-20261023` | 2026-10-24 | AWAITING CONFIRMATION |
| #973 | Canon sizing: per-version height+girth, Burger Bob-sized | `feat/canon-sizing` | 2026-10-24 | AWAITING CONFIRMATION |
| #970 | Batch2 moveset pull: scimitar/slice/skull/zui/kinpo (T8 diff + SHOW-ANIMATION... | `moveset/batch2-pull` | 2026-10-24 | AWAITING CONFIRMATION |
| #968 | TTT2 take-2: surgical carve infrastructure + XDVDFS listing (Law/Lars lane) | `ttt2/take2-results-20261024` | 2026-10-24 | AWAITING CONFIRMATION |
| #966 | feat: MDickey move melding — WH-native design + prototype | `feat/move-melding-20261023` | 2026-10-24 | AWAITING CONFIRMATION |
| #964 | docs: agent handoff 2026-10-23 (pickup guide for Claude/Muse) | `docs/agent-handoff-20261023` | 2026-10-24 | AWAITING CONFIRMATION |
| #963 | feat: soft-body nextgen lane — SurRoL MPM-lite backend + Newton stages + NDG ... | `feature/softbody-nextgen-20261023` | 2026-10-24 | AWAITING CONFIRMATION |
| #962 | Full move lists + combos for every fighter: base + 魂 ACTION/KESSHOU/九魂解放/霊放/試... | `feat/full-movelist-combos` | 2026-10-24 | AWAITING CONFIRMATION |
| #961 | feat: XPBD cloth engine (game/js/fx/cloth.js) + roster-wide wiring | `feature/cloth-xpbd-20261023` | 2026-10-24 | AWAITING CONFIRMATION |
| #960 | feat: voro++ Voronoi fracture wired into arena destruction | `feat/voropp-destruction-20261023` | 2026-10-24 | AWAITING CONFIRMATION |
| #959 | FightingICE-methodology CPU AI: reaction delay, frame-data punishes, MCTS | `feat/fighting-ai-methodology-20261023` | 2026-10-24 | AWAITING CONFIRMATION |
| #957 | [FutureTech] SCRIPT + AdaHuman/GAIA integration design (research-stage) | `docs/futuretech-script-phototofighter-20261023` | 2026-10-24 | AWAITING CONFIRMATION |
| #940 | docs(research): MK Armageddon — Konquest + Kreate-A-Fighter technique research | `docs/mk-armageddon` | 2026-10-24 | AWAITING CONFIRMATION |
| #936 | Track 7: cutscenes & story mode — cinematic director, brawler camera, Yuka na... | `feat/track7-cutscenes-story` | 2026-10-24 | AWAITING CONFIRMATION |
| #931 | tools: RE toolchain install script + mocap (VM-rebuildable) | `tools/re-toolchain-setup` | 2026-10-23 | AWAITING CONFIRMATION |
| #924 | Moveset batch8 pull: bruno/docfrank/chatur/samura1/star + SHOW-ANIMATION LOCK | `moveset/batch8-pull` | 2026-10-24 | AWAITING CONFIRMATION |
| #911 | Select-card audit: Tripo-first defaults + texture-elimination guard | `fix/select-card-defaults-20261023` | 2026-10-23 | AWAITING CONFIRMATION |
| #909 | docs: RE toolchain setup 2026-10-23 | `docs/re-toolchain-2026-10-23` | 2026-10-23 | AWAITING CONFIRMATION |
| #908 | Fix universal face-weight cone bug (37 models) + CI guard | `fix/face-weight-cone-20261023` | 2026-10-23 | AWAITING CONFIRMATION |
| #887 | Batch-5 moveset pull: King Tyrant, Cyborg X, Awa Pop, Retsu, Rin (T8 diff + S... | `moveset/batch5-pull` | 2026-10-24 | AWAITING CONFIRMATION |
| #884 | docs: Wrestling Empire systems research (HMW world/match variety) | `docs/wrestling-empire` | 2026-10-23 | AWAITING CONFIRMATION |
| #883 | docs: Yakuza Kiwami brawler/city/story systems research (HMW) | `docs/yakuza-kiwami` | 2026-10-23 | AWAITING CONFIRMATION |
| #882 | docs: Nioh character-depth / mythology-structure systems research | `docs/nioh-systems` | 2026-10-23 | AWAITING CONFIRMATION |
| #881 | docs: WWE 2K22 creation-suite / animation / rig format research | `docs/wwe2k22-creation` | 2026-10-23 | AWAITING CONFIRMATION |
| #880 | docs: Gang Beasts physics technique spec (partial-ragdoll) | `docs/gang-beasts-physics` | 2026-10-23 | AWAITING CONFIRMATION |
| #879 | docs: Fire Pro Wrestling World systems research (CPU sim / creation / AI logic) | `docs/fire-pro-systems` | 2026-10-23 | AWAITING CONFIRMATION |
| #875 | rig: universal face-cone skin-weight audit + fixer (WIP) | `feat/face-cone-skin-weights` | 2026-10-24 | AWAITING CONFIRMATION |
| #863 | T7 Steam extraction #1: pakchunk0 meshes (Alisa/Lee/Bob + 35 more), textures, UI | `feat/t7-steam-extraction` | 2026-10-23 | AWAITING CONFIRMATION |
| #857 | Jules API helper + Jules taskboard claims | `grok/jules-helper` | 2026-10-23 | AWAITING CONFIRMATION |
| #850 | docs(team): TASKBOARD, limit handoff steps, free-resource playbook (builds on... | `grok/team-taskboard-free-resources-v2` | 2026-10-23 | AWAITING CONFIRMATION |
| #844 | docs: agent team protocol + multi-agent directive (user 2026-10-23) | `docs/agent-team-protocol` | 2026-10-23 | AWAITING CONFIRMATION |
| #842 | Touch controls: visible Tekken 1/2/3/4 diamond + HEAT/RAGE (phone) | `fix/touch-tekken-buttons` | 2026-10-23 | AWAITING CONFIRMATION |
| #826 | T7 character select rebuild: 2-row grid, 1P/2P cursors, stage strip, announce... | `w-t7-select-rebuild` | 2026-10-23 | AWAITING CONFIRMATION |
| #822 | WORKLOG: merge steward pass 2026-10-23 | `docs/worklog-merge-steward-20261023` | 2026-10-23 | AWAITING CONFIRMATION |
| #806 | Law full pull for Buffalo Bill: anim bank + moveset + stance/poses | `law/full-pull-2026-10-23` | 2026-10-23 | AWAITING CONFIRMATION |
| #744 | Worker 84: Gyou spirit body archive (Tripo fiery humanoid) — archive-only, no... | `archive/gyou-spirit-body-20261022` | 2026-10-23 | AWAITING CONFIRMATION |
| #741 | Worker 83: Nine Souls character-select redesign (owner directive 2026-10-22) | `worker83/nine-souls-select-redesign-20261022` | 2026-10-23 | AWAITING CONFIRMATION |
| #734 | docs: lock Kuma replacement display name as GASHADOKURO | `worker79/kuma-name-lock-gashadokuro` | 2026-10-23 | AWAITING CONFIRMATION |
| #723 | Worker 77: SCIMITAR ATTIRE 1 ARCHIVE + SPEC (user directive 2026-10-22) | `worker-77-scimitar-a1-archive` | 2026-10-23 | AWAITING CONFIRMATION |
| #722 | Worker 75: SmutBase intake repair — all 6 files open + T-pose renders (MERGE ... | `worker75-smutbase-intake-repair-20261022` | 2026-10-23 | AWAITING CONFIRMATION |
| #721 | archive(yukihyo): Attire 3 Tiger King source model (immutable original) | `w76-yukihyo-a3-archive` | 2026-10-23 | AWAITING CONFIRMATION |
| #720 | archive(bruno): Attire 1 + Attire 2 source models (immutable originals) + Mig... | `worker74-bruno-a1-archive` | 2026-10-23 | AWAITING CONFIRMATION |
| #719 | Dio Attire 1 + Million Eyes Demon transformation Tripo archive (worker 73) | `worker73-dio-a1-archive` | 2026-10-23 | AWAITING CONFIRMATION |
| #718 | Worker 72: T5/T6/TTT2/T7 teardown completion report (MERGE FREEZE — do not me... | `worker72/t5-t6-ttt2-teardown-completion` | 2026-10-23 | AWAITING CONFIRMATION |
| #717 | archive(sweep): tpose-delivery proof renders + sweep record + archive-then-cl... | `archive/negativo-cornerstone-tpose-20261022` | 2026-10-23 | AWAITING CONFIRMATION |
| #716 | archive(kuma-replacement): Attire 1 Tripo source model (immutable original) +... | `archive/kuma-replacement-a1-20261022` | 2026-10-23 | AWAITING CONFIRMATION |
| #715 | archive+eyeglow(negativo): Tripo A1/A2 + CornerStone A1 immutable originals; ... | `archive/negativo-eye-glow-20261022` | 2026-10-22 | AWAITING CONFIRMATION |
| #714 | worker68: CORNERSTONE moveset — Yamazaki 3D KOF + Rock + Toguro (YYH:DT teard... | `w68/cornerstone-moveset` | 2026-10-22 | AWAITING CONFIRMATION |
| #713 | VF5 motion pipeline: Dural stance for Zen (worker 60) | `vf5/motion-pipeline-20261022` | 2026-10-22 | AWAITING CONFIRMATION |
| #712 | Worker 61: owner-repo mining — animations, customization parts, select-screen... | `worker61-owner-repo-mining` | 2026-10-22 | AWAITING CONFIRMATION |
| #711 | Worker 66: in-suite hand-tooling with headless Blender backend (MODEL EDIT) | `w66/in-suite-mesh-edit` | 2026-10-22 | AWAITING CONFIRMATION |
| #710 | worker65: WWE CAW drives the creation suite — menu logic + 100% teardown cove... | `worker65/wwe-caw-creation-suite` | 2026-10-22 | AWAITING CONFIRMATION |
| #709 | Clothing remove/change system + labeling standard + Tsuyu frog hat (worker 64) | `w64/clothing-layer-system` | 2026-10-22 | AWAITING CONFIRMATION |
| #706 | w59: Ashlane->DOA claimed-map lock + DOA4/KOF3D federation sources + Vain Abe... | `w59-doa4-kof-movesets` | 2026-10-22 | AWAITING CONFIRMATION |
| #704 | VF5 full integration — worker 57 re-dispatch: van/wol renders + Wolf head fix | `w57/vf5-redispatch-20261022` | 2026-10-22 | AWAITING CONFIRMATION |
| #703 | archive(buffalo-bill,theory): Buffalo Bill A1/A2 + Theory A1-A4 source models... | `archive/buffalo-bill-theory-20261022` | 2026-10-23 | AWAITING CONFIRMATION |
| #685 | Worker 29: Training mode depth + replays (Gungaku lab, replay theater) | `worker29/training-replays` | 2026-10-23 | AWAITING CONFIRMATION |
| #678 | Moveset Library System: central 9,420-move library + per-fighter assembly (wo... | `w47/moveset-library-system` | 2026-10-23 | AWAITING CONFIRMATION |
| #668 | Worker 24: TTT2 team battle in versus (submenu + tag mechanics) | `worker24/ttt2-team-battle-v2` | 2026-10-23 | AWAITING CONFIRMATION |
| #665 | Eastern Mind assets incorporated + generative AI canon pass (worker 40) | `feat/eastern-mind-assets-ai-pass-20261022` | 2026-10-23 | AWAITING CONFIRMATION |
| #660 | Worker 24: TTT2 team battle in versus (submenu + tag mechanics) | `worker24/ttt2-team-battle` | 2026-10-23 | AWAITING CONFIRMATION |
| #644 | Worker 20: HEART AND MIND WITHIN phase 1 — Devil Within foundation (playable ... | `worker20/heart-mind-within-phase1` | 2026-10-23 | AWAITING CONFIRMATION |
| #636 | T-pose urgent batch: Mirko render | `tpose-urgent/mirko` | 2026-10-23 | AWAITING CONFIRMATION |
| #497 | T3 bank facing: fix the backwards bake at the source | `fix/t3-bank-facing-20261022` | 2026-10-23 | AWAITING CONFIRMATION |
| #464 | Urban Reign phase 3: textures + general-pool assignment + name mapping (state... | `ur-phase3-textures` | 2026-10-23 | AWAITING CONFIRMATION |
| #449 | CornerStone Attire 1: owner's Tripo model wired (model lane) | `feat/cornerstone-model-20261021` | 2026-10-23 | AWAITING CONFIRMATION |
| #446 | Tekken 6 PSP SOLVED: 76/76 adler-exact — root cause was per-2048 vs per-1024 ... | `teardown/tekken6-round4-ppsspp-trace` | 2026-10-23 | AWAITING CONFIRMATION |
| #442 | Urban Reign phase 2: native .gyu motion conversion (stacked on #434) | `ur-phase2-motion` | 2026-10-21 | AWAITING CONFIRMATION |
| #393 | Pose isolation fix: own-stance idle/walk, Chest->Spine2, Steve Fox shirt re-s... | `pose-isolation-fix-20261020` | 2026-10-23 | AWAITING CONFIRMATION |
| #377 | [DO NOT MERGE - tool fails rig] Wire Keemap into anim-retarget + proof run: K... | `wireup/keemap-20261020` | 2026-10-20 | AWAITING CONFIRMATION |
| #206 | Research: 3D pipeline 2026 (image-to-3D ranking, Source/XPS to GLB, T-pose re... | `3d-pipeline-doc` | 2026-10-17 | AWAITING CONFIRMATION |
| #182 | RESEARCH (do not merge): rig auto-fix survey — teardown rules + OSS tooling | `research/rig-autofix-survey` | 2026-10-15 | AWAITING CONFIRMATION |

## agent-ops — open PRs at briefing time (0)

No open PRs on mhvnsnt/agent-ops at briefing time. Any lane opening a PR after this
briefing is briefed by the AGENTS.md section on arrival; add its row here when it opens.

## Coordinator lanes (no PR of their own)

| Lane | How briefed | Status |
|------|-------------|--------|
| Merge coordinator (overnight queue-sync / push-everything wave) | agent-ops AGENTS.md briefing + this file | AWAITING CONFIRMATION |

## Scope decision + active-lane census (2026-10-26)

Owner decision 2026-10-26 ~19:10 CDT (tapped option): **"Count only active lanes"** — the flip no longer waits on every briefed lane, only on active ones. This replaces the open question in the 2026-10-24 record.

**"Active" definition (recorded, defensible):** a western-heart PR counts as active if its `updatedAt` is at or after the briefing census, **2026-10-24 21:35Z** (16:35 CDT Oct 24). `updatedAt` moves on any push, comment, or GitHub-side refresh, so it is a checkable liveness signal, not a guess about who is working. PRs opened after the briefing are active by the same test (their `updatedAt` is after the cutoff).

**Census 2026-10-26 ~19:11 CDT (00:11Z Oct 27), verified live via `gh pr list`:** 57 open western-heart PRs (down from 77 at briefing — 20 closed/merged since, incl. the Oct 25 get-it-all-done wave). 31 mergeable / 26 conflicting. **51 active, 6 inactive.** 40 PRs opened after the briefing — the active set keeps moving; the flip must be judged against the cutoff set below, or re-censused at flip time.

**Flip state verified live 2026-10-26:** western-heart `main` branch protection has `required_merge_queue: null`; agent-ops `main` has NO branch protection at all (404); no rulesets on either repo. The flip has NOT happened anywhere. Do not flip until the parent agent verifies the confirmation evidence and flips both repos together.

### Active lanes (51) — in scope, all chased 2026-10-26

| PR | Title | Branch | Last updated | Status | Confirmation |
|----|-------|--------|--------------|--------|--------------|
| #442 | Urban Reign phase 2: native .gyu motion conversion (stacked on #434) | `ur-phase2-motion` | 2026-10-26 | MERGEABLE / BLOCKED | AWAITING CONFIRMATION |
| #706 | w59: Ashlane->DOA claimed-map lock + DOA4/KOF3D federation sources + Vain Abel 200-entry wiring | `w59-doa4-kof-movesets` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #713 | VF5 motion pipeline: Dural stance for Zen (worker 60) | `vf5/motion-pipeline-20261022` | 2026-10-25 | MERGEABLE / UNSTABLE | AWAITING CONFIRMATION |
| #714 | worker68: CORNERSTONE moveset — Yamazaki 3D KOF + Rock + Toguro (YYH:DT teardown) + library banks | `w68/cornerstone-moveset` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #718 | Worker 72: T5/T6/TTT2/T7 teardown completion report (MERGE FREEZE — do not merge) | `worker72/t5-t6-ttt2-teardown-completion` | 2026-10-26 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #722 | Worker 75: SmutBase intake repair — all 6 files open + T-pose renders (MERGE FREEZE, do NOT merge) | `worker75-smutbase-intake-repair-20261022` | 2026-10-26 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #744 | Worker 84: Gyou spirit body archive (Tripo fiery humanoid) — archive-only, not wired | `archive/gyou-spirit-body-20261022` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #857 | Jules API helper + Jules taskboard claims | `grok/jules-helper` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #863 | T7 Steam extraction #1: pakchunk0 meshes (Alisa/Lee/Bob + 35 more), textures, UI | `feat/t7-steam-extraction` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #875 | rig: universal face-cone skin-weight audit + fixer (WIP) | `feat/face-cone-skin-weights` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #964 | docs: agent handoff 2026-10-23 (pickup guide for Claude/Muse) | `docs/agent-handoff-20261023` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1057 | Creation Suite: remove Mixamo Soldier, wire real templates, nested menus, universal rigs | `feature/creation-suite-mixamo-removal-20261024` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1072 | feat(music): rotation pools for every stage + mode, two Cape pools, cutscene hook, Tekken/all-games research | `feature/music-wiring-rotations-20261024` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1073 | Reconcile mega-batch + motbin wiring: one correct moveset per fighter (supersedes #1039) | `feature/reconcile-1039-1048-20261024` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1090 | [HELD FOR APPROVAL - DO NOT MERGE] Zen: VF5 Dural layer (194) + Twelve layer (5), proposed button map | `feature/zen-dural-twelve-20261024` | 2026-10-25 | MERGEABLE / BLOCKED | AWAITING CONFIRMATION |
| #1096 | Batch 1 step plans (Pantera LP1/RP2): _attackClipPlan step-plan branch + 60 string_step_plans, verified steps  | `feat/batch1-step-plans-pantera-20261024` | 2026-10-25 | MERGEABLE / UNSTABLE | AWAITING CONFIRMATION |
| #1097 | Batch 1 follow-up (Pantera LP1/RP2): Job 3 fills (row 97 VERIFIED, row 49 SOFT) + Job 4 adjudications | `feat/batch1-followup-job3-job4-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1099 | Batch 2 step plans (Pantera LK3/RK4-only strings): 27 plan keys, 1 verified step | `feat/batch2-step-plans-pantera-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1101 | Batch 3 step plans (Pantera mixed-pair strings): 49 plan keys, 10 verified steps | `feat/batch3-step-plans-pantera-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1102 | Batch 4 step plans (Pantera triples/quads/rest strings): 72 plan keys, 36 verified steps | `feat/batch4-step-plans-pantera-20261025` | 2026-10-25 | MERGEABLE / UNSTABLE | AWAITING CONFIRMATION |
| #1103 | Burger Batch 1 step plans (LP1/RP2-only strings): 88 plan keys, 15 verified steps | `feat/burger-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1104 | Burger Batch 2 step plans (LK3/RK4-only strings): 67 plan keys, 11 verified steps | `feat/burger-batch2-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1105 | Burger Batch 3 step plans (mixed-pair strings): 49 plan keys, 8 verified steps | `feat/burger-batch3-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1107 | Burger Batch 4 step plans (triples/quads/rest): 15 plan keys, 5 verified steps, BURGER COVERAGE-COMPLETE | `feat/burger-batch4-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1108 | Demonio Batch 1 step plans (LP1/RP2-only strings): 59 plan keys, 27 verified steps, 0 fills | `feat/demonio-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1110 | Demonio Batch 2 step plans (LK3/RK4-only strings): 25 plan keys, 11 verified steps, 0 fills | `feat/demonio-batch2-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1111 | Demonio Batch 3 step plans (mixed-pair strings): 87 plan keys, 19 verified steps, 0 fills | `feat/demonio-batch3-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1112 | Demonio Batch 4 step plans (triples/quads/rest): 100 plan keys, 133 verified steps, coverage COMPLETE | `feat/demonio-batch4-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1113 | Diablo Batch 1 step plans (LP1/RP2-only strings): 111 plan keys, 44 verified steps, 0 fills | `feat/diablo-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1114 | Diablo Batch 2 step plans (LK3/RK4-only strings): 21 plan keys, 9 verified steps, 0 fills | `feat/diablo-batch2-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1115 | Diablo Batch 3 step plans (mixed-pair strings): 43 plan keys, 15 verified steps, 0 fills | `feat/diablo-batch3-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1116 | Diablo Batch 4 step plans (triples/quads/rest): 42 plan keys, 110 verified steps, 0 fills — LAST diablo batch | `feat/diablo-batch4-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1117 | Kinpo Batch 1 step plans (LP1/RP2-only strings): 47 plan keys, 19 verified steps, 1 Job 3 fill | `feat/kinpo-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1118 | Kinpo Batch 2 step plans (LK3/RK4-only strings): 20 plan keys, 9 verified steps, 0 Job 3 fills | `feat/kinpo-batch2-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1119 | Kinpo Batch 3 step plans (mixed-pair strings): 48 plan keys, 2 verified steps, 0 Job 3 fills | `feat/kinpo-batch3-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1120 | Kinpo Batch 4 step plans (triples/quads + rest): 62 plan keys, 27 verified steps, 1 Job 3 fill — COVERAGE COMP | `feat/kinpo-batch4-step-plans-20261025` | 2026-10-25 | MERGEABLE / UNSTABLE | AWAITING CONFIRMATION |
| #1121 | Phantom Batch 1 step plans (LP1/RP2-only strings): 186 plan keys, 22 verified steps, 0 Job 3 fills | `feat/phantom-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1122 | Phantom Batch 2 step plans (LK3/RK4-only strings): 49 plan keys, 3 verified steps, 0 Job 3 fills | `feat/phantom-batch2-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1123 | Phantom Batch 3 step plans (mixed-pair strings): 85 plan keys, 18 verified steps, 0 Job 3 fills | `feat/phantom-batch3-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1124 | Phantom Batch 4 step plans (triples/quads/rest): 52 plan keys, 32 verified steps, coverage-complete | `feat/phantom-batch4-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1125 | Scimitar Batch 1 step plans (LP1/RP2-only strings): 21 plan keys, 16 verified steps, 0 Job 3 fills | `feat/scimitar-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1126 | Scimitar Batch 2 step plans (LK3/RK4-only strings): 18 plan keys, 9 verified steps, 0 Job 3 fills | `feat/scimitar-batch2-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1127 | Scimitar Batch 3 step plans (mixed-pair strings): 23 plan keys, 1 verified step, 0 Job 3 fills | `feat/scimitar-batch3-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1128 | Scimitar Batch 4 step plans (triples/quads/rest): 16 plan keys, 30 verified steps, 0 Job 3 fills — COVERAGE CO | `feat/scimitar-batch4-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1129 | Skull Batch 1 step plans (LP1/RP2-only strings): 91 plan keys, 32 verified steps, 0 Job 3 fills | `feat/skull-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1130 | Skull Batch 2 step plans (LK3/RK4-only strings): 29 plan keys, 8 verified steps | `feat/skull-batch2-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1131 | Skull Batch 3 step plans (mixed-pair strings): 78 plan keys, 12 verified steps | `feat/skull-batch3-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1132 | Skull Batch 4 step plans (triples/quads/rest): 130 plan keys, skull coverage COMPLETE | `feat/skull-batch4-step-plans-20261025` | 2026-10-25 | MERGEABLE / CLEAN | AWAITING CONFIRMATION |
| #1136 | Torch Batch 1 step plans (LP1/RP2-only strings): 79 plan keys, 11 verified (anna) steps, 22 BANK-BLOCKED (jin) | `feat/torch-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1139 | Zui Batch 1 step plans (LP1/RP2-only strings): 194 plan keys, 9 verified (jin) steps, 0 Job 3 fills | `feat/zui-batch1-step-plans-20261025` | 2026-10-25 | CONFLICTING / DIRTY | AWAITING CONFIRMATION |
| #1141 | Torch per-step-bank engine support: step plans resolve a step's clip from the step's own bank (BANK-BLOCKED fl | `feat/torch-per-step-bank-20261025` | 2026-10-25 | MERGEABLE / UNSTABLE | AWAITING CONFIRMATION |

### Inactive lanes (6) — OUT of scope under the owner's decision, not chased, no confirmation needed

| PR | Title | Branch | Last updated | Status |
|----|-------|--------|--------------|--------|
| #182 | RESEARCH (do not merge): rig auto-fix survey — teardown rules + OSS tooling | `research/rig-autofix-survey` | 2026-10-15 | CONFLICTING / DIRTY |
| #377 | [DO NOT MERGE - tool fails rig] Wire Keemap into anim-retarget + proof run: Keemap v0.0.9 collapses Scarlett D | `wireup/keemap-20261020` | 2026-10-20 | MERGEABLE / CLEAN |
| #826 | T7 character select rebuild: 2-row grid, 1P/2P cursors, stage strip, announcer cues | `w-t7-select-rebuild` | 2026-10-23 | CONFLICTING / DIRTY |
| #908 | Fix universal face-weight cone bug (37 models) + CI guard | `fix/face-weight-cone-20261023` | 2026-10-23 | CONFLICTING / DIRTY |
| #911 | Select-card audit: Tripo-first defaults + texture-elimination guard | `fix/select-card-defaults-20261023` | 2026-10-23 | CONFLICTING / DIRTY |
| #970 | Batch2 moveset pull: scimitar/slice/skull/zui/kinpo (T8 diff + SHOW-ANIMATION LOCK) | `moveset/batch2-pull` | 2026-10-24 | CONFLICTING / DIRTY |

Notes on the inactive set: #377 is parked forever (`[DO NOT MERGE - tool fails rig]`); #182 is a research-only PR from 2026-10-15; #826/#911/#908/#970 last moved Oct 23–24, before the briefing census, and have not moved since.

### Chase (2026-10-26)

2nd-notice comment posted to **all 51 active PRs** (2026-10-27 00:13–00:21Z, 51 posted / 0 skipped / 0 failed), pointing at `GAME-DEV-BRIEFING.md` section 11 on main and asking each lane to reply `merge-queue briefing confirmed`. Spot-verified live afterwards on #964, #744, #1101. No PR was closed, no branch touched, nothing flipped.

### Merge coordinator lane (no PR of its own)

Still AWAITING CONFIRMATION. Briefed via agent-ops AGENTS.md + this file. Evidence it is still running: agent-ops overnight queue-sync PRs #194–#200 landed 2026-10-26 (latest merge 3eedcbe, #200 at 23:44Z). It cannot confirm via a PR comment — it confirms at its next check-in.


## Confirmations received

None yet. Add rows as lanes confirm: `PR # / lane — confirmed, <time>, via <chat / PR comment / check-in>`.

Checked 2026-10-26 ~19:30 CDT: still NONE. Exact-phrase GitHub search (`merge-queue briefing confirmed`, both repos) returns 0; spot-checked comments on WH #1096, #718, #1101 (zero comments) and #442 (one unrelated sweep note). No lane has confirmed by any verifiable channel this lane can check (chat check-ins in other chats are not visible to this lane — if a lane says it confirmed in chat, the parent agent should record it here with the chat + time).

