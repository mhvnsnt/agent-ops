# HANDOFF — WESTERN HEART (mhvnsnt/western-heart)

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
