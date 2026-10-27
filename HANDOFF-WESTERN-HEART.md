# HANDOFF — WESTERN HEART (mhvnsnt/western-heart)


## OBSOLETE-ORIGINALS RULE (owner, 2026-10-23 — binding)

A source-game character whose moveset and identity were given to a proprietary character of this universe is **OBSOLETE IN CANON**: not a character here — no canon file, no story, no roster entry. Only the proprietary successor exists. Authority: mhvnsnt/western-heart `docs/OBSOLETE-ORIGINALS-RULE.md` (on main since 2026-10-23, PR #766).

**Character select + attire ladder** (owner's verbatim order, same day): obsolete originals **never appear on the character select list** — not selectable, not listed, not counted as fighters. Their models wire **only as laddered attires of their successor, late in the ladder (slots 5+)**, behind the successor's own attires. The ladder front is fixed: the character's Tripo 3D models first (slots 1-5), then the owner's proprietary reskins. Original-game attires/reskins ladder behind those, never in front.

Existing text about originals is KEPT (never deleted) with the obsolete notice at the top of the file/section. Base-name mentions inside a successor's file are scaffolding references, not identities. Mapping (original -> successor): Blanka->CHARGER, Zangief->KRONOS, Vega->KORESHI, Iori->DEATHFANG, Kuma->GASHADOKURO, Panda->AOTSUKI, Baek->KEVIN, Zafina->MARIPOSA, Lili->SILVERTONGUE, Jin->DEMONIO, Armor King->YUKIHYO; base-only (never had roster entries): Xiaoyu/Christie->STAR, Nina->AWA POP, Asuka->KINPO, Bryan->SKULL, Bob->BURGER, Heihachi->DIABLO, King->PANTERA, Yoshimitsu->PHANTOM, Lei->RAVE, Dragunov->SLICE, Ganryu->THOR, Mokujin->DXMMII.

State verified 2026-10-23. Sources: main-branch tree + `game/js/assets.js` checks by the main agent, merged census doc `docs/ROSTER-COUNT-CANON-2026-10-21.md` (PR #484), `MERGE-QUEUE.md`. Live site: https://mhvnsnt.github.io/western-heart/

## What exists & where

- Game code: `game/` (JS frontend, `game/js/assets.js` holds `MODEL_URLS`). Models live in `game/assets/models/` — NOT in `roster/`. Roster content (canon, attires, sources) lives in `roster/<fighter>/`. Movesets: `game/assets/movesets/*.json`. Teardowns: `teardown/` in-repo.
- Catch-up audit (in flight): `docs/CATCHUP-AUDIT-2026-10-23.md` + `docs/catchup-audit-2026-10-23.json` — the per-fighter gap map; when it merges, its items enter `MERGE-QUEUE.md`.

## Verified state (on main, 2026-10-23)

- **Roster:** 67 fighter dirs in `roster/` (includes duplicate-name dirs: rave + kiko-tanaka, jin + jin-eastern-mind, purple-rain + purplerain, saku-ra + sakura; plus a non-fighter `props` dir). Census (PR #484): 59 roster entries / 50 distinct fighters.
- **Canon:** only **4 of 67 dirs** have a canon/bio file: `buffalo-bill/CANON.md`, `dorowani/VOICE-CANON.md`, `gyou/CANON.md`, `zen/CANON.md`. The rest of the recorded canon exists in assistant memory files only — that is the gap the canon lanes (below) are closing. See `HANDOFF-CANON.md`.
- **Models:** `MODEL_URLS` in `game/js/assets.js` has **107 keys; 106 resolve to files that exist on main; exactly 1 is broken**: `ryuji-rock` → `../roster/ryuji-rock/attires/attire1/model.glb` (missing). Models mostly live in `game/assets/models/`; Cyborg X and Cape Jones models both exist there (same person — do not report either as model-less).
- **CornerStone (ryuji-rock) — the pattern case:** the owner's Tripo pull `20c1fd2e-40d0-4500-9be6-50f6494ab5e1` IS archived on main at `roster/ryuji-rock/attires/attire1/source/cornerstone-a1.glb` (18,872,720B, manifest in the same dir). It was never copied to the wired path, never rigged, and has no `roster-full.js` entry — the fighter is unselectable while his model sits in the repo. His moveset IS live (22 moves). This is landing wave 1, item 1.
- **Movesets:** census: 58 per-id files / 55 loader-listed. `game/assets/movesets/` holds 123 paths incl. `index.json` and non-roster extras. Fighters with moveset files but NO `MODEL_URLS` key include: dio, koreshi, bruno, chordz, lili, blanka, iori.
- **Attires:** census: 108 rows — 94 wired / 13 not wired / 1 broken. Tripo pulls: 66 distinct — 53 wired / 5 staged / 8 pulled-not-wired.
- **Backlog:** 112 open PRs / 759 remote branches / 89 releases at audit time. Most open PRs are mergeable-but-unmerged (fleet-wide Actions quota outage; resets 2026-11-01 per records).

## Queued / next (landing waves, in order — see MERGE-QUEUE.md)

1. **Wiring/path fixes** — CornerStone first (copy source GLB to the wired path, rig per the auto-rig rule, add roster-full entry).
2. **Models** — unwired Tripo pulls + missing `MODEL_URLS` keys.
3. **Movesets** — loader-list the unlisted files; fill fighters with movesets but no model key.
4. **Rigs** — the needs-rig list (27 fighters per the sibling audit — CLAIM until the catch-up audit verifies per fighter).
5. **Canon** — per-fighter CANON.md from recorded material only (see HANDOFF-CANON.md).

Held/problem PRs: #497 (CONFLICTING — merging as-is REGRESSES the #508 feet fix; rebase preserving #508), #498 (gate semantic fail — lane must correct its deviations declaration), #499 (AKI corrective; all 11 clips fail gate on true data; awaits FK→T3 IK follow-on), #462 (merge when CLEAN). #377 stays OPEN as evidence — do not merge.

## In-flight lanes (state as of 2026-10-23 — verify before assuming)

- **Zen originals restore** — adds `roster/zen/{spirit,tentacle,oversoul}/model-rigged-original.glb` (exact pre-compression bytes from merge 74678121) alongside the compressed in-game files, which stay as the wired versions per owner decision 2026-10-23. PR + merge in flight.
- **Bios harvest batch 1** — writes `roster/<dir>/CANON.md` for 25 fighters from owner-recorded material only; zero-material fighters get NO file and go on a truly-blank list for the owner to dictate.
- **Canon archive push** — compiles all recorded game canon/notes/dev records into `docs/canon-archive/` (CANON-MASTER.md + DEV-NOTES-ARCHIVE.md), game material only.
- **Catch-up audit** — per-fighter gap table with a verified payload location for every gap (on-main-wrong-path / branch / PR / release / local / claim-only / does-not-exist).

## Blockers (concrete)

- **Playtest gate (owner, 2026-10-23):** the owner has NOT retested and will test only after this catch-up lands. His 2026-10-21 verdict stands until cleared: "unplayable" (characters slide on their own; select screen persists into the fight; fighters freeze in T-pose while the timer counts; fighters fall halfway through the ground; stage-select dead-end on phone). Rule: nothing is called playable until the landing waves are merged AND verified on main AND a main-agent harness playtest (fight + customization) passes. Only then does the owner get asked to test.
- PR #497/#498: owning lanes must fix (above) — not owner decisions.

## Ownership

- Backlog/merge order: `MERGE-QUEUE.md` + the merge-law-ci-watch. Playtest triage + stage-select build: sibling Western Heart session (do not duplicate). Teardown-derived inputs: `HANDOFF-TEARDOWNS.md`.

## Engine lock

**GODOT 4.7.2** (owner-delegated pick, 2026-10-21). Mobile (Vulkan) renderer, Compatibility fallback, GLB native import, deterministic fixed-step sim core separated from presentation, direct APK export. Unity 6.3 LTS is the standing fallback. First build step: 2-fighter vertical slice on a real mid-range phone. The current web build (gh-pages) is the shipping prototype the playtest gate applies to.

## 2026-10-24 ~05:20Z verify-sweep (overnight pipeline)

- **#979 "cape-jones-fight" — VERIFIED on main.** Live merge lane merged 7559a534 at 05:07:21Z. Merge-tree gate: ahead_by=9, behind=0 vs parent1 d60f354f; exactly the 11 intended files (WORKLOG.md, docs/decisions/2026-10-23-cape-jones-fight-wiring.md, 3 proof pngs, portraits-manifest.json, owner-models.json, assets.js, attires.js, ATTIRE-SLOTS.md, roster/cyborg-x/attires/attire1/model-rigged.glb); 0 deletions. Cyborg X Attire 1 = Cape Jones canonical wiring is on main.
- **#987 soul-variants-wave3 — VERIFIED on main.** Merge 67631439 vs parent1 acfd05a3 = exactly 1 modified file: game/data/soul-variants.json; 0 deletions.
- **#989 dev-notes** — tail entry (Vain Abel A1 / rig wave 2 / moveset wave 3) intact on main, 41,512B — survived the lane's subsequent merges.
- WH live merge lane ACTIVE tonight (merged #979 05:07Z; #984/#985/#986/#988 iterating). Pipeline stood down per CHECK-BEFORE-START.

## Deploy state (2026-10-26/27 — verified)

- **Split hosting approved (owner, 2026-10-26 19:10 CDT):** Pages shell + GLBs on Cloudflare R2. Nothing is cut from the game, only from the deploy. Doc on WH main: `docs/DEPLOY-SPLIT-2026-10-26.md` (PR #1151, merge bce9feba, blob sha 08565ccb, 810B). R2 signup still owner-only (card rules); itch.io account/payout setup still owner-only.
- **Live site frozen on Oct 24 build:** deploy set 5,969 MB vs 1 GB Pages limit.
- **Netlify credits exhausted (verified extraction 2026-10-27 00:44 UTC, claim 408b1ac0):** 75% of 300 credits used by Sun 8:47 AM CT, all 300 by 11:21 AM CT. Production deploys and Agent Runners paused; live sites stay up on 30 operational credits; if those run out the sites suspend until credits come back or the billing cycle resets November 23. Offered fix is upgrading to a Personal plan (1,000 credits/mo, no price in the email) — owner's call. With Pages also failing its deploy on size, Netlify is off the table as a deploy fallback unless upgraded.
- WH deploy-split doc was NOT amended with the Netlify note — no verbatim owner instruction on file for that edit; the split decision itself is landed (above).
