# Western Heart — Character Model Inventory
**Date:** 2026-10-14
**Purpose:** Every character model downloaded for Western Heart that comes from another game, and whether it has a WH proprietary name yet. Owner will create proprietary versions/names for the unnamed ones.
**Sources scanned:** `mhvnsnt/western-heart` repo (full 46,241-file tree via GitHub API, HEAD @ 2026-10-14), `~/workspace/game-reverse-engineering/` (all lanes), `~/workspace/wwe-wrestler-models/`, `~/workspace/western-heart-vf5/`, `~/workspace/teardowns/`, other `~/workspace` model dirs.
**Rule:** inventory only — nothing modified, moved, or renamed.

## SUMMARY
| | Count |
|---|---|
| Distinct character entries inventoried | **198** |
| **LACK a WH proprietary name** | **185** (187 incl. 2 VF5 R.E.V.O. fighters not yet pulled) |
| Already have a WH proprietary name | 13 |
| Raw character-part groups (not whole characters, no WH names) | 4 groups |

**WH names already assigned (owner):** Pantera, Demonio, Phantom, Diablo, Skull, SAM-∪R-Λ1, Rin, Byou, Tou, Sha, Kai, Jin, Retsu, Zen, Gyou, Saku Ra, The Trader, The Assembled Soul, Zui, Bannon. (Per repo `ROSTER.md`.)

---

## TABLE A — NO WH PROPRIETARY NAME YET (owner action list)

### A1. Tekken 7 / Tekken 8 (modding-community pulls — local lane)
Location: `~/workspace/game-reverse-engineering/tekken7/models/`

| # | Original character | Source game | File(s) | Size | WH name |
|---|---|---|---|---|---|
| 1 | Steve Fox | Tekken 7 | `steve-fox-alt/5BDNEGLGFKGEV8VMHDP75GV0M.fbx` | 1,038,112 B | NO |
| 2 | Asuka Kazama | Tekken 7 | `asuka-alt/1L4OIS1UE1EVR6XXD54H6QH96.fbx` | 1,188,400 B | NO |
| 3 | Eddy Gordo | Tekken 7 | `eddy-gordo-capoeira/ZDZX8I1VLPXSATTXMICG95PUB.fbx` | 1,117,520 B | NO |
| 4 | Ling Xiaoyu (pink dress alt) | Tekken 7 | `xiaoyu-pink-dress/5Y7WAAMB6NEG27I43XTFO9HK8.fbx` | 1,899,744 B | NO |
| 5 | Armor King (battle cloth) | Tekken 8 | `king-variants/t8-armor-king-battle-cloth-whitemagesunny/Raw Files/Armor King Battle Cloth.fbx` + `Armor King Battle Cloth Head No Acc.fbx` | 8,926,476 + 3,661,484 B | NO |

### A2. WWF No Mercy — named wrestler models (whole characters)
Locations: repo `teardown/wwf-no-mercy/re-docs/assets/3d Assets/characters/` (mirrored at `~/workspace/game-reverse-engineering/wwf-no-mercy/re-docs/...`)

| # | Original character | Source game | File(s) | Size | WH name |
|---|---|---|---|---|---|
| 6 | Kevin Nash | WWF No Mercy (N64) | `kevin_nash/kevin_nash_1.glb` | 129,952 B | NO |
| 7 | Kurt Angle | WWF No Mercy (N64) | `kurt_angle/kurt_angle_1.glb` | 138,352 B | NO |
| 8 | Rhino | WWF No Mercy (N64) | `rhino/rhyno_1.glb` | 136,296 B | NO |
| 9 | Rob Van Dam | WWF No Mercy (N64) | `rob_van_dam/rob_van_dam_1.glb` | 137,220 B | NO |
| 10 | Scott Hall | WWF No Mercy (N64) | `scot_hall/scott_hall_1.glb` | 137,896 B | NO |
| 11 | Shawn Michaels | WWF No Mercy (N64) | `shawn_michaels/shawn_michaels_1.glb`, `shawn_michaels_2.glb` | 139,472 / 138,788 B | NO |
| 12 | Stephanie McMahon | WWF No Mercy (N64) | `stephanie_mcmahon/stephanie_mcmahon_1.glb` | 140,580 B | NO |
| 13 | Steve Austin | WWF No Mercy (N64) | `steve_austin/steve_austin_1.glb` | 135,404 B | NO |
| 14 | The Rock | WWF No Mercy (N64) | `the_rock/the_rock_1.glb`, `the_rock_2.glb`, `the_rock_bald.glb` | 138,924 / 132,020 / 137,664 B | NO |
| 15 | Triple H | WWF No Mercy (N64) | `triple_h/triple_h_1.glb` | 138,572 B | NO |

### A3. Virtua Fighter 5 (all 19 fighters — NO WH names, confirmed by `game-reverse-engineering/RENAME-MAP.md`)
Location: `~/workspace/game-reverse-engineering/virtua-fighter-5/models/<fighter>/` (full model data in TeraBox release `vf5-ps3-v1`; locally only 3 of 19 dirs populated, 16 are empty placeholders)

| # | Original character | Sega code | Style | Local status | WH name |
|---|---|---|---|---|---|
| 16 | Akira Yuki | aki | Bajiquan | populated — 63 MB (`akiitm*_{obj,tex}.bin`) | NO |
| 17 | Akira Yuki (alt variant) | akixx | Bajiquan | populated — 4.2 MB | NO |
| 18 | Pai Chan | pai | Ensei-Ken | populated — 70 MB | NO |
| 19 | Lau Chan | lau | Koen-Ken | placeholder (empty) | NO |
| 20 | Wolf Hawkfield | wol | Pro Wrestling | placeholder (empty) | NO |
| 21 | Jeffry McWild | jef | Pancratium | placeholder (empty) | NO |
| 22 | Kage-Maru | kag | Hagakure-ryu Jujutsu | placeholder (empty) | NO |
| 23 | Sarah Bryant | sar | Martial Arts | placeholder (empty) | NO |
| 24 | Jacky Bryant | jak | Jeet Kune Do | placeholder (empty) | NO |
| 25 | Shun Di | shu | Drunken Kung Fu | placeholder (empty) | NO |
| 26 | Lion Rafale | lio | Praying Mantis Kung Fu | placeholder (empty) | NO |
| 27 | Aoi Umenokouji | aoi | Aiki-Jujutsu | placeholder (empty) | NO |
| 28 | Lei-Fei | lei | Shaolin Kung Fu | placeholder (empty) | NO |
| 29 | Vanessa Lewis | van | Vale Tudo | placeholder (empty) | NO |
| 30 | Brad Burns | bra | Kickboxing | placeholder (empty) | NO |
| 31 | Goh Hinogami | goh | Judo | placeholder (empty) | NO |
| 32 | Eileen | mon | Monkey Kung Fu | placeholder (empty) | NO |
| 33 | El Blaze | msk | Lucha Libre | placeholder (empty) | NO |
| 34 | Dural (boss) | dur | — | placeholder (empty) | NO |
| — | Jean Kujo | — | Karate | **not yet pulled** (R.E.V.O. only) | NO |
| — | Taka-Arashi | — | Sumo | **not yet pulled** (R.E.V.O. only) | NO |

### A4. Urban Reign — 72 character slots (unnamed at extraction level)
Location: repo `teardown/urban-reign/models/char001/` … `char072/` — 216 `.obj` files total (3 per char: `charNNN_normals.obj`, `charNNN_pos_infl0.obj`, `charNNN_uv.obj`), **19,770,154 B total**. All **NO** WH name. (Lane notes: Tekken guests Paul Phoenix / Marshall Law are among these slots; slot→name mapping not yet established.)

| # | Original character | Source game | Files | Size | WH name |
|---|---|---|---|---|---|
| 35–106 | char001 … char072 (72 fighters, names TBD) | Urban Reign (PS2) | `teardown/urban-reign/models/charNNN/*.obj` (3 files each) | ~19.8 MB total | NO |

### A5. WWE WrestleMania XIX — 78 populated wrestler slots (unnamed at slot level)
Location: repo `teardown/wmxix/wrestlers/000/` … `077/` — 126 `.obj` files (slot dirs `NNN/NNN_M.obj`), per `~/workspace/wwe-wrestler-models/README.md`: "126 wrestler models from all 111 character slots on the disc (78 populated slots, some with variants)". Mirrored at `~/workspace/wwe-wrestler-models/wmxix/wrestlers/` and `~/workspace/game-reverse-engineering/wwe-wrestlemania-xix/objs/`. All **NO** WH name.

| # | Original character | Source game | Files | Size | WH name |
|---|---|---|---|---|---|
| 107–184 | wrestler slots 000 … 077 (78 wrestlers, names TBD) | WWE WrestleMania XIX (GCN) | `teardown/wmxix/wrestlers/NNN/NNN_M.obj` (126 files) | — | NO |

### A6. WWF No Mercy — raw character parts (not whole characters; no WH names)
| Group | Location | Files | WH name |
|---|---|---|---|
| CAW body parts (220) | repo `customization/parts/no-mercy/body_parts/model_*.obj` | 220 `.obj` (~1–2 KB each) | NO |
| Faces / hair (48) | repo `teardown/wwf-no-mercy/models/face/` | 48 `.obj` | NO |
| Attire meshes (2,431 unlabeled + 1 attire_part) | repo `teardown/wwf-no-mercy/models/unlabeled/` + `attire_parts/` | 2,432 `.obj` | NO |
| (mirror) | `~/workspace/wwe-wrestler-models/no-mercy/models/` — 2,700 meshes w/ `manifest.json` labels | — | NO |

### A7. Non-commercial-game character model (flagged, no WH name)
| # | Character | Source | File | Size | WH name |
|---|---|---|---|---|---|
| 185 | "Soldier" | tk-fighting-game (open-source "SHADOW STRIKERS", not a commercial game) | repo `customization/create-fighter/assets/Soldier.glb`; local `game-reverse-engineering/western-heart-assets/tk-fighting-game/assets/models/Soldier.glb` | 2,160,468 B | NO |

---

## TABLE B — ALREADY HAVE WH PROPRIETARY NAMES

| # | WH name | Source character / game | Model file(s) | Size |
|---|---|---|---|---|
| 1 | **Pantera** | King — Tekken 3/7/8 | repo `game/assets/models/pantera.glb`; `roster/pantera/pantera_rigged.glb`, `roster/pantera/tail-rig/pantera_body.glb`, `pantera_tail.glb`, `roster/pantera/attires/leomon/mane-pieces/*.obj`, `tail/pantera_tail.glb`; `lab/game/assets/pantera_leoman.glb`, `pantera_leoman_t3real.glb`; `lab/source_assets/original/pantera_leoman_original.glb`; local `game-reverse-engineering/tekken7/king/` (pantera.glb, pantera_light.glb, pantera_tiny.glb, pantera_rigged.glb, king_joined.glb, King T7/T8 fbx, arena .blends); repo `teardown/tekken7/king/` + `models/king-variants/`; `teardown/tekken3/models/king95/`; Leomon (Digimon) mane/head pieces `tekken7/king/leomon/` (attire source); `quaternius-lion.glb` (CC0 mane source, not a game) | ~7.6 MB main + variants |
| 2 | **Demonio** | Jin Kazama — Tekken 3 | repo `game/assets/models/demonio.glb`; `lab/game/assets/t3_jin.glb`, `t3_jin_t3real.glb`; `teardown/tekken3/models/jin151/` | 23.3 MB main |
| 3 | **Phantom** | Yoshimitsu — Tekken 3 | `lab/game/assets/t3_yoshimitsu.glb`, `t3_yoshimitsu_t3real.glb`; `teardown/tekken3/models/yoshimitsu103/` | — |
| 4 | **Diablo** | Heihachi Mishima — Tekken 3 | `teardown/tekken3/models/heihachi191/` | — |
| 5 | **Skull** | Bryan Fury — Tekken 3 | `lab/game/assets/t3_bryan.glb`, `t3_bryan_t3real.glb`; `teardown/tekken3/models/bryan183/` | — |
| 6 | **SAM-∪R-Λ1** | Gun Jack — Tekken 3 | `lab/game/assets/t3_gunjack.glb`, `t3_gunjack_t3real.glb`; `teardown/tekken3/models/gunjack215/` | — |
| 7 | **Sha / Saku Ra** | Ling Xiaoyu — Tekken 3 | `lab/game/assets/t3_xiaoyu.glb`, `t3_xiaoyu_t3real.glb`; `teardown/tekken3/models/xiaoyu127/` | — |
| 8 | **Rin** | Jin Kazama — Tekken 3 (Nine Souls) | same donor files as Demonio (body donor Jin TMD) | — |
| 9 | **Byou** | Lei Wulong — Tekken 3 (Nine Souls) | `teardown/tekken3/renders/king/lei_full_raw.obj`, `lei_head.obj` | — |
| 10 | **Tou** | Paul Phoenix — Tekken 3 (Nine Souls) | design mapping only; no separate model file | — |
| 11 | **Kai** | Eddy Gordo — Tekken 3 (Nine Souls) | design mapping only; no separate model file | — |
| 12 | **Retsu / Zen / Gyou / Jin** | Bryan / Julia / Hwoarang / Yoshimitsu — Tekken 3 (Nine Souls) | covered by donor files above | — |
| 13 | **Zui** | (import) | repo `roster/zui/imports/base_v1.glb` | 23,311,408 B |
| — | **Bannon** | (mask) | `lab/game/attire/bannon_mask/bannon_mask.glb`; `lab/source_assets/original/bannon_mask_original.glb` | 2,655,024 / 23,340,972 B |
| — | **The Trader / The Assembled Soul** | Mokujin / True Ogre (design space) | no model files yet | — |

**Name-source of truth:** repo `ROSTER.md` (Nine Souls + owner-designed characters). Rename tracking: `~/workspace/game-reverse-engineering/RENAME-MAP.md` (VF5 rows all "no"; delete file when renames complete, per owner law).

---

## EXCLUDED (not character models)
- `lab/game/assets/t3_stage_l.glb` — Tekken 3 stage geometry, not a character.
- `teardown/wwf-no-mercy/re-docs/assets/3d Assets/environments/*.glb` — menu scenes.
- `teardown/wwf-no-mercy/models/{arena,backstage,lobby,stage}/` + `weapon/` — environments/props.
- `teardown/wmxix/arenas/` (40) — arenas.
- `teardown/urban-reign` stage files / `teardown/tekken3/stages/` — stages.
- `assets/free-pull-1/quaternius/` — animation libraries (FBX/glTF), no character meshes.
- `assets/free-pull-1/ambientcg/` — PBR texture packs (.blend), no characters.
- `western-heart-assets/{kenney,cmu-mocap}` — particles/audio/mocap BVH, no character models.
- `customization/parts/wmxix/` — .ymg accessory parts (not standard model files; CAW accessories).
- `customization/parts/doa/` — docs only, no model files present.
- `~/workspace/agent-ops/worktrees/wrestling-teardown/` — git worktree duplicates of repo teardown files (not separate models).
- `~/workspace/teardowns/` — docs only (beat-em-up teardown notes, not WH character models).
