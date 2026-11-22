# FIGHTER MODEL CENSUS — 2026-10-16

**Owner order:** "where are they and why aren't you rendering them" — full inventory of every fighter/character model on disk or in our repos/releases.

**Method:** Every entry verified against disk (`~/workspace/`) or GitHub API. No guessing. Wrestling-earmarked models are listed separately per the 2026-10-13 separation rule.

---

## SUMMARY TABLE

| Game | Fighters w/ models | WH-named | Unnamed | T-pose rendered | Notes |
|---|---|---|---|---|---|
| Tekken 3 | 7 | 7 | 0 | 0 | All named; TMD extractions in WH repo |
| Tekken 7 (rigmodels) | 20+ | 16 | 4 | 0 | FBX zips on disk; see detail |
| Tekken 8 | 2 | 2 | 0 | 0 | Asuka T8, Xiaoyu T8 (rar) |
| Tekken 6 (PSP) | 0 | 0 | 0 | 0 | Bulk decrypt in progress — no models yet |
| TTT2 | 0 | 0 | 0 | 0 | Reassembly 11/26 — no models yet |
| Virtua Fighter 5 | 19 | 2 | 17 | 0 | .farc in release tars; needs 3ds Max Windows |
| Urban Reign | 72 | 0 | 72 | 0 | Coded char001–072; geometry decode blocked |
| Street Fighter | 1 (Rashid ×3) | 0 | 1 | 0 | SFV not acquired; EX = bins only |
| SoulCalibur II | 0 | 0 | 0 | 0 | **24 movesets mapped, ZERO 3D models** |
| Dead or Alive | 0 | 0 | 0 | 0 | **Bass NOT in hand**; DOA4 ISO reassembling |
| **WH-usable total** | **~121** | **27** | **~94** | **2** | Pantera + Zui only |
| Def Jam FFNY | 78 sets | 0 | 78 | 0 | Wrestling-earmarked |
| WWF No Mercy | 3,570 | 0 | — | 0 | Wrestling-earmarked |
| WMXIX | 126 OBJs | 0 | 126 | 0 | Wrestling-earmarked; full-body blocked |
| WWE 2K models | 2,826 | 0 | — | 0 | Wrestling-earmarked |

---

## TEKKEN 7 — rigmodels batch (on disk)

**Location:** `~/workspace/game-reverse-engineering/tekken7/models/`
**Format:** FBX inside zips (1 FBX each, zip-integrity verified 2026-10-14)

| Dir | Character | Polys | WH name | T-pose |
|---|---|---|---|---|
| negan/ | Negan | 30,338 | N3GΔTIV0 | ❌ |
| lili/ | Lili | 40,448 | — | ❌ |
| ganryu/ | Ganryu | 5,168 / 5,276 | Thor | ❌ |
| xiaoyu/ | Xiaoyu | 35,355 | Saku Ra | ❌ |
| xiaoyu-pink-dress/ | Xiaoyu alt | — | Saku Ra alt | ❌ |
| xiaoyu-t8/ | Xiaoyu T8 | rar | Saku Ra alt | ❌ |
| zafina/ | Zafina (T6 Butterfly) | 38,002 | — | ❌ |
| josie/ | Josie | 25,805 | Waterfall | ❌ |
| julia/ | Julia | 27,570 | Nightwolf | ❌ |
| nina/ | Nina | 8,124 | Awa Pop | ❌ |
| lei/ | Lei Wulong | 19,372 | Rave | ❌ |
| bryan/ | Bryan | 7,650 | Skull | ❌ |
| yoshimitsu/ | Yoshimitsu | 5,410 | Phantom | ❌ |
| baek/ | Baek | 5,370 | — | ❌ |
| lee/ | Lee | 6,413 | Purple Rain | ❌ |
| mokujin/ | Mokujin | 6,934 | DXMMII | ❌ |
| steve-fox/ | Steve Fox | — | Zui | ✅ |
| steve-fox-alt/ | Steve Fox alt | FBX | Zui alt | ❌ |
| asuka-kazama/ | Asuka | — | Kinpo | ❌ |
| asuka-alt/ | Asuka alt | FBX | Kinpo alt | ❌ |
| eddy-gordo/ | Eddy | — | King Tyrant | ❌ |
| eddy-gordo-capoeira/ | Eddy alt | textures | King Tyrant alt | ❌ |
| heihachi-mishima/ | Heihachi | rar | Diablo | ❌ |
| gun-jack/ | Gun Jack | 3 zips | SAM-UR-A1 | ❌ |
| dr-bosconovitch/ | Dr. Bosconovitch | rar (XPS) | Doc Frank | ❌ |
| king-variants/ | King ×6 | mixed | Pantera/Yukihyō alts | ✅ (Pantera) |
| unsorted-rigmodels/ | 3 unsorted | FBX zips | — | ❌ |

**Missing from rigmodels (pending next reset):** Kunimitsu, Michelle, Law, Anna, Christie, Kuma, Jin, Kazuya, Jun, Bruce, Armor King, Panda, Paul, **Lars** (needed for Chordz — NOT in hand)

## TEKKEN 3 (WH repo)

**Location:** `western-heart/teardown/tekken3/models/` (GitHub)
7 fighters, all WH-named: King95→Pantera, Jin151→Demonio, Yoshimitsu103→Phantom, Heihachi191→Diablo, Bryan183→Skull, GunJack215→SAM-UR-A1, Xiaoyu127→Saku Ra. T-pose: none.

## VIRTUA FIGHTER 5 (19 fighters)

**Location:** GitHub Release `vf5-model-library-v1` (mhvnsnt/western-heart) — `vf5-models-a.tar` (394MB) + `vf5-models-b.tar` (386MB). NOT extracted locally.
**Format:** `.farc` body archives — **conversion BLOCKED on Linux, needs 3ds Max Windows** (owner: "Get the software").

| Fighter | Code | WH name | T-pose |
|---|---|---|---|
| Akira Yuki (+alt) | aki/akixx | — | ❌ |
| Pai Chan | pai | — | ❌ |
| Lau Chan | lau | — | ❌ |
| Wolf Hawkfield | wol | — | ❌ |
| Jeffry McWild | jef | — | ❌ |
| Kage-Maru | kag | — | ❌ |
| Sarah Bryant | sar | — | ❌ |
| Jacky Bryant | jak | — | ❌ |
| Shun Di | shu | — | ❌ |
| Lion Rafale | lio | — | ❌ |
| Aoi Umenokouji | aoi | — | ❌ |
| Lei-Fei | lei | — | ❌ |
| Vanessa Lewis | van | — | ❌ |
| Brad Burns | bra | **Realizzt** | ❌ |
| Goh Hinogami | goh | **Kutz** | ❌ |
| Eileen | mon | — | ❌ |
| El Blaze | msk | — | ❌ |
| Dural | dur | — | ❌ |

## URBAN REIGN (72 fighters)

**Location:** `western-heart/teardown/urban-reign/models/char001`–`char072` (GitHub)
**Status:** All coded, ROSTER.json has stats but **zero names**. Geometry decode **BLOCKED** (checkpoint `ur-geometry-decode.json` needs_owner — skeleton not in char PPKs; owner directed "all and both" leads: .gyu motion files + stage PPKs, re-arm pending).
**WH names:** 0/72. **T-pose:** 0/72.

## STREET FIGHTER

- **Rashid (SFV)** — 3 variants (default XPS 48,708v, Air Man XPS, SFM CC0) in `western-heart/teardown/street-fighter-5/models/rashid/`. WH name: none. T-pose: none.
- **SFV full game:** NOT acquired (FitGirl/CODEX blocked by browser policy; Archive.org dark). Checkpoint `sfv-pull-teardown.json` needs_owner.
- **EX series:** EX2 Plus complete (PR #87), EX3/EX+Alpha = bins only on releases. No extracted models.

## SOULCALIBUR II — ⚠️ MODELS GAP

**24 movesets mapped** (`teardown/soulcalibur-2/CHARACTER-MAP.md`: Mitsurugi, Seong Mi-na, Taki, Maxi, Voldo, Sophitia, Ivy, Kilik, Xianghua, Yoshimitsu, Nightmare, Astaroth, Cervantes, Raphael, Talim, Cassandra, Necrid, Yun-seong, Link, Heihachi, Spawn + 3 unidentified).
**3D models extracted: ZERO.** No fighter geometry in hand. WH rename: all pending.

## DEAD OR ALIVE — ⚠️ MODELS GAP

- **Bass Armstrong:** **NOT IN HAND** (confirmed in `teardown/BASS-ARMSTRONG.md`). Path: DOA4 teardown (ISO reassembly in progress) or DeviantArt XNALARA hunt.
- **DOA4:** ISO 30/30 chunks on release `doa4-iso-v1`; reassembly scripts ready; download gated behind TTT2.
- **DOA6:** mechanics docs only, binaries never acquired.

## TEKKEN 6 / TTT2

- **T6:** Sector cipher + K1/K2 reversed; DATA401 bulk decrypt verified (decrypt2). **No character models extracted yet.** Recon in "Western Heart recon" side chat.
- **TTT2:** 26/26 chunks on release `ttt2-7z-v1`; reassembly at 11/26. **No character models yet.**

## WRESTLING-EARMARKED (not WH — separation rule 2026-10-13)

- **Def Jam FFNY:** 78 fighter sets (coded V2IP_001A–V2IP_999A), `wrestling-game/teardown/def-jam-fight-for-ny/models/fighters/` (234 entries). CAW parts → WH Create Fighter (22,360 parts indexed).
- **WWF No Mercy:** 3,570 models, `western-heart/teardown/wwf-no-mercy/models/`.
- **WMXIX:** 126 wrestler OBJs (mod repo). Full-body assembly blocked (limb.ymg hunt).
- **WWE 2K:** 2,826 models in `mhvnsnt/wwe-wrestler-models` (migration pending).

---

## OWNER-NAMED CHARACTERS — FIND/CONFIRM

| Name | Owner said | Status |
|---|---|---|
| Samir | "Samir from some games" | ❌ **NOT FOUND** anywhere — no file, no doc, no inventory mentions Samir. Needs owner clarification (which game?) |
| Bass (DOA) | Bass Armstrong | ❌ **NOT IN HAND** — confirmed. Path: DOA4 teardown or XNALARA hunt |
| Zangief | Street Fighter | ❌ **NOT IN HAND** — only SF model is Rashid |
| Bear | (Kuma?) | ❌ **NOT IN HAND** — Kuma on rigmodels next-reset list, never pulled |
| Bryden (?) | "from goddamn you know that fight game" | ❌ **NOT FOUND** — no match in any inventory. Needs owner clarification |
| Hugo | SF, "based off Vader the wrestler" | ❌ **NOT IN HAND** — only SF model is Rashid. Hugo is SFIII/2nd Impact — no source in hand |
| Lars → Chordz | Tekken | ❌ **MODEL NOT IN HAND** — rigmodels next reset |

## BIGGEST GAPS (models in hand, no renders, no names)

1. **Urban Reign 72** — biggest unnamed pool, but geometry decode blocked. Can't render until decode lands.
2. **VF5 17 unnamed** — models exist in release tars but .farc needs 3ds Max Windows. Can't render until converted.
3. **T7 unnamed 4** — Lili, Baek, Zafina, + Lars missing. **These CAN render now** (FBX on disk, Blender fixed via xvfb-run).
4. **SCII 24** — movesets but zero models. Needs model extraction lane.
5. **DOA entire** — Bass + roster. Needs DOA4 teardown or XNALARA hunt.
6. **T-pose renders: 2/121** — only Pantera and Zui. Everything else unrendered.

## RENDER-READY NOW (no blockers)

These have 3D files on disk/in repo TODAY and could go through T-pose renders immediately:
- T7: Lili, Baek, Zafina, Negan, Ganryu, Josie, Julia, Nina, Lei, Bryan, Yoshimitsu, Lee, Mokujin, Xiaoyu (+alts), Steve Fox (+alt), Asuka (+alt), Eddy (+alt), Heihachi, Gun Jack, Dr. Bosconovitch
- T3: all 7 (TMD extractions)
- T8: Asuka T8, Xiaoyu T8
- Rashid ×3
- **Blocked from rendering:** VF5 19 (.farc), UR 72 (geometry), T6/TTT2 (no models yet), SCII (no models), DOA (no models)
