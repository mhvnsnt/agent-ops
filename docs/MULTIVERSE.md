# MULTIVERSE — one universe, many games

Owner direction (2026-10-14): **all of the owner's games are ONE multiverse**,
in the spirit of the MDickie universe — shared parts, shared skeleton, shared
creation suite, shared wearables — with each title keeping its own reference
games, tone, and per-game systems.

This doc lives in `mhvnsnt/agent-ops` so every agent can find the map without
cloning every game repo. Update it when a shared part lands or a game's
reference set changes. Claim related work in [CLAIMS.md](../CLAIMS.md).

---

## Games at a glance

| Game | Repo | Primary references | Canon distance from Bannon | Live / Lab |
|---|---|---|---|---|
| **Bannon** | [`mhvnsnt/Bannon`](https://github.com/mhvnsnt/Bannon) | WWE games we have (2K CAW/moveset lineage, Off The Top Rope books, MDickie wrestling sims, Neckbreaker / Visceral Pro Wrestling ragdoll notes) | **Canon center** | [bannon.pages.dev](https://bannon.pages.dev); UE5 under `unreal/`; legacy Three.js arena |
| **AshLane (v2)** | [`mhvnsnt/AshLanev2`](https://github.com/mhvnsnt/AshLanev2) | **Urban Reign** (street-lane brawler feel); Kenney City Kit CC0 shells | Close — shared cast / Bannon can appear | [ashlane-1aa.pages.dev](https://ashlane-1aa.pages.dev); TanStack Start + Three.js mobile |
| **Brutal-Fist** | [`mhvnsnt/brutalfistgrokversionten`](https://github.com/mhvnsnt/brutalfistgrokversionten) | **Tekken**, **Def Jam**, and similar 3D fighters. **No psychedelic elements** — AshLane/Tekken-style fighting without Urban Reign rain or Tong-Nou surrealism | Close — shared roster DNA, Bannon model as quality bar | [brutalfist.pages.dev](https://brutalfist.pages.dev) |
| **western-heart** | [`mhvnsnt/western-heart`](https://github.com/mhvnsnt/western-heart) | **Tekken base** (T3 engine/importers; T6/TTT2 in progress) **plus** pieces from all teardown games: Urban Reign, Def Jam, WWE No Mercy / WM19, Eastern Mind / Tong-Nou fiction | **Furthest from Bannon canon**, but **linked** — Bannon can appear playable; mask is universal | Godot Lab 1v1 (`lab/`); private, never published as those titles |

Study / teardown material is for understanding and licensed recombination only.
Western Heart and the other originals remain the owner's work.

---

## Shared parts (use these; do not fork silently)

| Shared part | Canonical home | What agents must do |
|---|---|---|
| **Canonical skeleton + retarget maps** | western-heart Lab (`lab/`, `wh_canonical_*` rigs); retarget into each game's runtime | Retarget Tekken / Mixamo / Tripo / WWE-style clips onto the shared skeleton; do not invent a second "canonical" bone set |
| **Creation suite** | western-heart [`packages/creation-suite`](https://github.com/mhvnsnt/western-heart/tree/main/packages/creation-suite) (`@mhvnsnt/creation-suite`); design in [`docs/creation-suite/DESIGN.md`](https://github.com/mhvnsnt/western-heart/blob/main/docs/creation-suite/DESIGN.md) | DNA v2 (superset of Bannon `docs/DNA_SCHEMA.md` + `bannon_customizer.js`); body sliders + size-adaptive jiggle; attire slots; WWE-style moveset from Bannon `assets/moves/moveset_schema.json` next. Wire into every game under its suite name (Create a Wrestler / Fighter / Brawler) |
| **Bannon mask (universal wearable)** | western-heart [`docs/attire/BANNON_MASK.md`](https://github.com/mhvnsnt/western-heart/blob/main/docs/attire/BANNON_MASK.md) + `lab/game/attire/bannon_mask/` | Equip in **all** games' character customization; bind/skin to head bone (or aliases); per-body-type fit offsets from the manifest presets |
| **Rig / mesh audits** | Brutal-Fist bone-integrity CI (e.g. PR #34/#38 pattern); western-heart mask follow-check (`lab/tools/mask_fit.py`); Bannon UniRig / skinqa gate | Run before merge of new Tripo/Drive models; catch broken bind poses, pixelated meshes, wrong facing |
| **Tripo intake pipeline** | Owner models mostly from **Tripo 3D**; intake + gate owned with Brutal-Fist model audit / Drive sync patterns (Bannon `tools/drive_sync`) | Assume no authored blend shapes or extra bones; procedural morphs + generated spring bones (creation-suite) |

Secondary physics (glute / thigh / chest / belly jiggle, hair/cloth chains) is part of the shared creation suite and scales with measured body size — not a per-game reinvention.

---

## Per-game parts

What stays **local** to each title (engine, fiction, stages, exclusive systems).
Filled from each repo's README / design docs (2026-10-14).

### Bannon (`mhvnsnt/Bannon`)

| Area | Per-game |
|---|---|
| Fantasy / fiction | Off The Top Rope books; wrestling promotion sim |
| Engine | UE5 C++ primary (`unreal/`); legacy Three.js single-file arena |
| Creation naming | **Create a Wrestler** |
| Own systems | DNA schema v1 + customizer hub; moveset_schema (WWE-2K Create-a-Moveset data); attire catalogues under `assets/customizer/`; active ragdoll / Neckbreaker-inspired physics notes |
| Stages | Wrestling rings / arenas (canon arena ledger in sibling fighters) |
| Deployment | Cloudflare Pages PWA; Android WebView package noted in README |

### AshLane v2 (`mhvnsnt/AshLanev2`)

| Area | Per-game |
|---|---|
| Fantasy / fiction | One walkable city lane; district jobs; named street fighters (`src/game3d/ward.ts`, `roster.ts`) |
| Engine | TanStack Start + Three.js; **not** C++ / Godot rewrite |
| Reference feel | Urban Reign street brawler |
| Creation naming | **Create a Brawler** |
| Own systems | Campaign save `ashlane-campaign-v2`; Kenney City Kit CC0 buildings; ring/cage/subway/crane/back-room interiors in `sim.ts` |
| Hard rules | No Schwarzerblitz / OpenBOR / GPL game asset copies; MIT/BSD/Apache/CC0 only; do not retarget foreign skeletons onto lane fighters (T-pose bug) |
| Deployment | Cloudflare Pages (`ashlane-1aa`); Vercel-oriented app builder shell |

### Brutal-Fist (`mhvnsnt/brutalfistgrokversionten`)

| Area | Per-game |
|---|---|
| Fantasy / fiction | Straight 3D fighter — **no** Tong-Nou / psychedelic layer |
| Engine | App-builder stack (TanStack / Vite / Three.js path in repo) |
| Reference feel | Tekken (movement, walls, juggles, okizeme — see `docs/TEKKEN-INSPIRATION.md`) + Def Jam / similar |
| Creation naming | **Create a Fighter** |
| Own systems | Roster + arena ledger (`docs/CANON_ARENA_STAGE_ROSTER_LEDGER.md`); animation intake docs; airborne dive / grapple maps; Bannon model as mesh/rig quality bar |
| Deployment | Cloudflare Pages (`brutalfist.pages.dev`) |

### western-heart (`mhvnsnt/western-heart`)

| Area | Per-game |
|---|---|
| Fantasy / fiction | Fighting trial inside Tong-Nou (Eastern Mind); nine souls; reincarnation rounds; Force Claiming — "lost multiverse bastard child" (`MISSION.md`, `DESIGN.md`) |
| Engine | Godot 4 Lab; Tekken 3–derived fighting core from teardown |
| Reference base | Tekken 3 (+ T6/TTT2 importers); Urban Reign, Def Jam, WWE No Mercy/WM19 teardown pieces as library entries |
| Creation naming | **Create a Fighter** (shared suite ships here first) |
| Own systems | Chimera architecture docs; Lab 1v1 (Leo-Man Pantera vs King); attire.gd + mask; teardown under `teardown/`; moveset-library |
| Multiverse link | Furthest fiction from Bannon, but Bannon is allowed as a playable guest with Tekken-style inputs + retargeted WH moves; mask already Lab-wired |
| Publishing | Private study build — do not ship as Tekken / WWE / etc. |

---

## Cross-game rules (owner)

1. **One multiverse** — shared skeleton, creation suite, mask, audits, Tripo intake.
2. **Playtest against the right references:** Bannon ↔ WWE; AshLane ↔ Urban Reign; Brutal-Fist ↔ Tekken + Def Jam (+ similar); western-heart ↔ Tekken base + all its teardown games.
3. **Push each piece** as small incremental PRs; claim in CLAIMS.md before starting.
4. **No deletion of owner work** — store safely (backup branches / box-storage) before freeing disk.
5. **Proof** for multiverse tasks: clips of Bannon fighting in western-heart; mask equipped on characters in each game.

---

## Active follow-ups (Repo Co Dev)

See CLAIMS.md row for this workstream:

1. Put the fixed Bannon model/skeleton/rig into western-heart, playable, Tekken-style movesets + retargeted WH animations.
2. Add the Bannon mask GLB as an equippable wearable in **all** games (head bind + per-body fit).
3. Keep this MULTIVERSE.md current as shared parts land.

*Last updated: 2026-10-14 CT.*
