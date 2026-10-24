# CLAIMS (prevents collisions)

Protocol:
1. **Before starting**, append a line to the table below and push it (branch plus PR, or include it in your first work PR): agent, task, branch, start time (CT).
2. Check the table first. If someone else holds the task or the files, pick another task or coordinate in TAG-TEAM.md.
3. When you're done, set the status to `done` with a PR link, or `released`.
4. Temp files must be unique per agent and job, e.g. `/tmp/<agent>-<task>-$(date +%s)-body.md`. **Never use a shared `/tmp/body.md`.** Same for scratch dirs and clones.

| Agent | Task | Branch | Started (CT) | Status |
|---|---|---|---|---|
| Grok Bot | TAG-TEAM board + process docs | docs/tag-team-board | 2026-10-14 15:20 | done |
| Grok Bot | Goodville postmortem / cutouts / timeline | (see TAG-TEAM #6) | 2026-10-14 | active |
| Grok Bot | CI fixes (TAG-TEAM #7) | per repo | 2026-10-14 | active |
| Grok Bot | Fiverr gig 1 (browser) | n/a | 2026-10-14 | active |
| Repo Co Dev | AshLanev2 PR #38 + #42 (crash fix / visual tests) | ashlanev2/pr-38-42 | 2026-10-14 15:23 | active |
| Repo Co Dev | western-heart Godot Lab 1v1 + T6/TTT2 importers | western-heart/lab-1v1 | 2026-10-14 15:23 | active |
| Repo Co Dev | Shared creation suite + jiggle physics (western-heart docs/creation-suite) | western-heart/creation-suite | 2026-10-14 15:23 | active |
| Repo Co Dev | Brutal-Fist all-character model audit + Tripo intake pipeline | brutalfist/model-audit-tripo | 2026-10-14 15:23 | active |
| Repo Co Dev | Cloudflare Pages deploys (bannon / brutalfist / ashlane-1aa) | cf-pages-deploys | 2026-10-14 15:23 | active |
| Repo Co Dev | Playtest + gameplay/animation fixes: AshLane, western-heart Lab, Brutal-Fist (not Kobra models) | playtest/2026-10-14 | 2026-10-14 15:58 | active |
| Grok Bot | western-heart per-character height/scale metadata applied at runtime (owner rule c); data file + loader only, no Lab engine edits beyond a scale hook | grok/wh-height-scale | 2026-10-14 16:45 | PR western-heart #120 (open, waits on owner OK of T7/T8 heights) |
| Grok Bot | western-heart menu/UI/HUD system (title, modes, char select, VS, HUD, pause, results); no physics / creation-suite physics / model-wiring files | grok/wh-menu-ui | 2026-10-14 16:57 | active |
| Muse | western-heart public collection (TAG-TEAM #18); handoff docs/handoffs/MUSE_FAN_ASSETS_HANDOFF.md | muse/wh-public-collection | 2026-10-14 18:38 | done — 3 PRs merged (#139 stubs, #143 frame data, #145 catalog+refs) |
| Muse | western-heart Pantera entrance/promo kit video v1 (first WH kit video); checkpoint wh-pantera-entrance-v1.json | muse/wh-pantera-entrance-v1 | 2026-10-14 21:40 | active |
| Muse (rig-pipeline) | western-heart universal rig-repair pipeline (TRACK 3): ingest/detect/transfer fixes + refit + separate + armpit + weldcap + gate + proof + orchestrator; 4 small PRs | rig-repair/pipeline-1, rig-repair/refit-2, rig-repair/separate-armpit-3, rig-repair/orchestrator-4 | 2026-10-15 02:50 | done — PRs #164, #165, #166, #168 (open) |
| Muse (kaggle-render-coord) | western-heart Pantera entrance video GPU render on Kaggle T4 (marsfmmg): repair Pantera via rig-pipeline PR branches #164-168 (no merge), Kaggle session/quota recon, 1500f chunked render, assemble+proof, update PR #169; checkpoint wh-pantera-kaggle-render.json | muse/wh-pantera-entrance-v1 (render lane) | 2026-10-15 11:05 | active |
| Grok Bot | western-heart merge steward / integration ONLY (merge clean+green PRs, union-merge integration PRs for doc-only conflicts, PR comments on blockers). No feature work | integrate/pr*-20261023 | 2026-10-23 13:40 CT | active |
| Grok Bot | Cape Jones x Western Heart tie-in: shared cast manifest, show-anim index (new dirs only), Cape house stage spec, TV portal doc, cape-jones proof render, handoff docs. NEW files only under `shared/cast/`, `anims/show/`, `stages/cape-house/`, `docs/HANDOFF-CAPE-JONES-X-WESTERN-HEART.md`, `docs/story/TV-PORTAL.md` in both repos; no edits to Claude/Muse files, movesets, game/js, lab/ | grok/cape-x-wh (both repos) | 2026-10-23 13:47 | active |
| Grok Bot | western-heart ANIMATION GATE (t117u): NEW `game/js/anim-gate.js`, `game/data/crossover.json`, `test/anim-gate.test.mjs`; ONE guarded hook line-block in `game/js/t3anims.js` createT3Actions only. Cape Jones = Alisa slot (t118u): additive mapping file only; char select files NOT edited without menu-lane OK. Show-slot retarget + moving proof. Avoids input-resolver/teardown/menu files. | grok/wh-anim-gate | 2026-10-23 14:20 | done (wh#811 merged 8bf6439; cape-jones#222 merged ce68b20) |
| Grok Bot | cape-jones PR CI workflow (t118u): NEW `.github/workflows/cast-ci.yml` | grok/cape-x-wh | 2026-10-23 14:20 | done (wh#811 merged 8bf6439; cape-jones#222 merged ce68b20) |
| Grok Bot | Cape Jones replaces Alisa (t118u #4/t121u): NEW `game/data/cape-alisa-binding.json`, `tools/cape/build_cape_alisa_binding.py`, proof png. NO edits to char select (menu/teardown lane: please surface binding in select bio when you next touch it) or fighter.js MOVESET_MAP | grok/cape-alisa-binding | 2026-10-23 14:25 CT | active |
| Grok Bot | western-heart asset pipeline 2026 (owner t124u): docs/tech/ASSET-PIPELINE-2026.md, tools/assets/**, tools/deploy/build_pages.py (--runtime-cache slim mode, additive), game/sw.js, game/sw-register.js, game/js/asset-preload.js. NOT touching index.html (PR #821), input.js/movesets.js (#812), select-screen.js, Cape/Alisa, anim gate. | grok/asset-pipeline-2026 | 2026-10-23 15:05 | active |
| Grok Bot (executor, teardown-integration) | western-heart: menu touch fix + e2e (PR #821), input resolver (PR #812), select-screen phone layout (game/select.css only), teardown coverage audit (docs/teardown-coverage/**), menu rebuild under namespaced paths w/ Legacy toggle, OWNER-COMPLAINTS.md, ui_sources CI gate, ROSTER-REPLACEMENT-MAP. NOT touching asset-pipeline files (sw.js, asset-preload.js, tools/assets, build_pages.py), loader files, Cape/Alisa, anim gate. | fix/menu-touch-t122u, fix/input-determinism-v2, fix/select-phone-layout, + per batch | 2026-10-23 15:04 | active |
| Repo Co Dev | Add Oct 23 owner rules (disk offload + merge rule) to western-heart + agent-ops docs; clean up Repo Co Dev's own finished /workspace clones | repo-co-dev/owner-rules-20261023 | 2026-10-23 15:55 | active |
| Grok Bot (T7/T8 integration) | western-heart: T8 frame data (docs/t7t8-reference/frame-data-t8-full, 41 JSON) -> game/data hit/guard/CH/throw-break tables + fighter.js lookup hook (additive, no moveset edits) | grok/t8-frame-tables | 2026-10-23 16:30 | starting |
| Grok Bot (T7/T8 integration) | western-heart: T7 Mishima Dojo stage (private-gated GLB) | stages/t7-mishima-dojo | 2026-10-23 16:30 | PR western-heart #855 + private game-reverse-engineering #50 |
| DoggByte (FutureTech subagent) | western-heart: SCRIPT + AdaHuman/GAIA integration design (research-stage; 2 design docs + tools/script-adapter + tools/photo-to-fighter, 38 tests pass) | docs/futuretech-script-phototofighter-20261023 | 2026-10-23 19:30 | PR western-heart #957 |
| Muse (DoggByte subagent) | western-heart: make Cape Jones playable on Alisa's select slot — rig QA on cape-jones.glb, stage roster/cyborg-x/attires/attire1/model-rigged.glb, MODEL_URLS + attire wiring, proof frames (select + fight) | muse/cape-jones-fight | 2026-10-23 20:45 CT | active |
| DoggByte (merge-tree-guard) | western-heart merge-time guard: NEW `.github/workflows/merge-tree-guard.yml` + `.github/scripts/merge_tree_guard.py` + `test_merge_tree_guard.py`; catches fake stale-tree merges (PR #974 pattern). No other files touched | muse/merge-tree-guard | 2026-10-23 22:05 CT | active |
| Repo Co Dev | Bannon playable in western-heart + Bannon mask in all games + MULTIVERSE.md | docs/multiverse-map | 2026-10-14 17:04 | active |
