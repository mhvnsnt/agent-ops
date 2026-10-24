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
- Briefing landed: western-heart PR (GAME-DEV-BRIEFING.md section 11) + agent-ops PR (AGENTS.md) — fill in numbers below.

## western-heart — open PRs at briefing time (77, listed 2026-10-24 ~16:35 CDT)

| PR | Title | Branch | Last updated | Status |
|----|-------|--------|--------------|--------|
| #1008 | Root motion: apply decoded T3 clip root_t travel during attacks (fighter.js) | `feat/root-motion-20261024b` | 2026-10-24 | AWAITING CONFIRMATION |
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

## Confirmations received

None yet. Add rows as lanes confirm: `PR # / lane — confirmed, <time>, via <chat / PR comment / check-in>`.

