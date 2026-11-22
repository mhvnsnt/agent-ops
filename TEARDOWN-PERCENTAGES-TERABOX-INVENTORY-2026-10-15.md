# TEARDOWN COMPLETION + TERABOX INVENTORY
**Created:** 2026-10-15 ~18:25 EDT (owner request)
**Purpose:** Handoff for ANY agent/repo picking up teardown work. Records per-game completion %, what's IN TeraBox, what's NOT, and what remains to hit 100%.
**Rule:** Check the repos for the full accurate percentage — these numbers are from the 2026-10-15 audit + MEMORY.md. Verify before trusting.

---

## GAMES MOVING TO TERABOX RIGHT NOW (upload in progress 2026-10-15)

### 1. TEKKEN 6 (PSP) — ~40% teardown
**Going to TeraBox:** `/game-files/tekken6-psp-iso/` — full ISO, 816MB (17 × 50MB pieces)
- SHA256: `b5e52660…` (full hash in `~/workspace/terabox-staging/blitz-20261015/UPLOAD-MANIFEST.md`)
- Reassemble: `cat t6-psp-iso.part_* > tekken6-psp.iso`

**What's done:**
- ISO verified byte-exact vs GitHub release `tekken6-psp-v1`
- 46 ending videos extracted (337MB, all characters) — on GitHub release `tekken6-endings-v1`
- EBOOT.BIN decrypted (no live run needed) — `decrypted/EBOOT.DECRYPTED.ELF`
- Sector cipher FULLY reversed (Python model at `tekken6/tools/sector_cipher.py`)
- DINF_400.BIN decrypted (PR #162)
- TEARDOWN.md documents structure

**What's NOT done (to reach 100%):**
- Models/textures still encrypted — DATA401 bulk scheme UNKNOWN
- Character models NOT extracted (0%)
- Moves/animations NOT extracted (0%)
- Live-dump path blocked (PPSSPP headless needs build — checkpoint `t6-live-dump.json` needs_owner)
- **Repos to check:** `western-heart/teardown/tekken6/`

### 2. STREET FIGHTER EX3 (USA, PS2) — ~5% (bin only)
**Going to TeraBox:** `/game-files/sfex3-usa-bin/` — full PS2 bin, 669MB (14 × 50MB pieces)
- SHA256: `059a9516…` (full hash in manifest)

**What's done:**
- Bin acquired, integrity check needed (was reported 329KB short at one point — VERIFY before use)
- EX2 Plus is COMPLETE (separate game, PR #87, release `sf-ex2-plus-v1`)

**What's NOT done (to reach 100%):**
- EX3 extraction NOT started
- Models, moves, stages: 0%
- **Repos to check:** `western-heart/teardown/street-fighter-3d-games/`
- **Related:** EX Plus Alpha bin (528MB, release `sf-ex-plus-alpha-v1`), SFIV PC (4.18GB), SFxT PS3 (12.99GB), USFIV PS3 (16.61GB) — all cataloged, NOT yet in TeraBox

### 3. EASTERN MIND — 100% ✅
**Going to TeraBox:** `/game-files/eastern-mind/` — 1.07GB (22 × 50MB pieces)
- SHA256: `cfff7584…` (full hash in manifest)

**What's done:**
- COMPLETE — PR #160 merged to western-heart main
- Zip verified (575MB, 845 files) + on GitHub release `eastern-mind-v1`
- 5,707 files organized by WH stage
- Extraction into WH done

**What's NOT done:** Nothing. This is the universe bible — reference only.

### 4. WRESTLEMANIA XIX TEARDOWN — ~80%+
**Going to TeraBox:** `/western-heart/wmxix-teardown/` — 28MB tarball (1 file)
- `wmxix-teardown-full.tar.gz`

**What's done:**
- ISO MD5-verified (c13c47a5ed24a675545c99a15e44529d)
- FST mapped (5,016 entries, 4,222 files)
- YOBJ/YANM/YCG/.atr formats decoded (70-bone skeleton, 170 YANM→JSON anims)
- 126 wrestler OBJs, 43 arenas, 2,690 CAW parts cataloged
- **YOBJ SKINNING SOLVED** (2026-10-15) — batch idx = bone index, s16 triplets, scale 1/64
- Mobile testbed LIVE at https://mhvnsnt.github.io/wrestlemania-xix-mod/testbed/
- Real GameCube controls wired from Prima guide

**What's NOT done (to reach 100%):**
- Full-body assembly (limb.ymg geometry location unknown)
- CAW.gci save format (needs real .gci dump — Dolphin route pending)
- ECD identity / base-ID generation
- Revenge Mode arena designs doc
- Arena face indices
- **Repos:** teardown lives in `western-heart/teardown/wmxix/` + `teardown/wwe-wrestlemania-xix/` (canonical) AND mirrored to `mhvnsnt/wrestlemania-xix-mod`

---

## OTHER GAMES — COMPLETION STATUS (not yet in TeraBox)

| Game | % | In TeraBox? | What's missing to 100% |
|------|---|-------------|----------------------|
| Tekken 3 | **100%** ✅ | No | Done. 8,556 TIMs, all fighters/stages, 3,247 moves |
| WWF No Mercy | **100%** ✅ | No | Done. 5,787 anims, 3,570 models, 17 arenas |
| VF5 (PS3) | **100% extraction** ✅ | No (GitHub release `vf5-model-library-v1`) | WH conversion blocked (needs 3ds Max Windows) |
| Def Jam FFNY | **Teardown complete** ✅ | No (ISO re-downloading) | .o = proprietary EAGL (converter = multi-day RE) |
| Urban Reign | **~95%+** | No | Geometry decode: bone-translation hunt open (.gyu + stage PPKs) |
| WWE 2K19 anims | **Packs only** | No | No base models. 2K19 pull (51GB) pending owner call |
| Soulcalibur II | **~60%** | No | PS2 FS RE needs owner call |
| TTT2 | **~15%** | No | Reassembly in progress (11/26 chunks). Characters+moves first |
| DOA4 | **ISO 100%, teardown 0%** | No | Teardown not started. Prep done, gated behind TTT2 |
| DOA6/SCVI | **10%** | No | Mechanics docs only. Binaries never acquired |
| SFV | **0%** | No | Not acquired. Steam purchase or owner-supplied copy needed |

---

## TERABOX SPACE (as of 2026-10-15)
- **Total:** 5TB (30GB permanent + 4TB trial expiring 2026-10-21 + ~1TB gift expiring 2026-11-11)
- **Used:** 23.8GB / 5120GB
- **Trial reminder:** Cron fires 2026-10-19 09:00 EDT — owner upgrades to paid ($9.99/mo or $99.99/yr)

## FOLDER MAP
```
/game-files/              ← ISOs, bins, game archives
  /tekken6-psp-iso/       ← T6 ISO (uploading 2026-10-15)
  /sfex3-usa-bin/         ← EX3 bin (uploading 2026-10-15)
  /eastern-mind/          ← Eastern Mind (uploading 2026-10-15)
/western-heart/           ← WH-related
  /wmxix-teardown/        ← WMXIX teardown tarball (uploading 2026-10-15)
/CN-Gigaleak/             ← CN show files (existing)
```

## NOTES FOR NEXT AGENT
1. **Percentages are estimates** — verify against the repos before planning work
2. **Game files law:** nothing deletes from local disk until TeraBox-verified AND owner confirms
3. **T6 ISO is irreplaceable** — took owner a full day to collect, was deleted once already
4. **Reassembly:** `cat <name>.part_* > <original>` then `sha256sum -c`
5. **Next TeraBox batch** (after current completes): VF5 (from GitHub), Def Jam ISO (when download finishes), EP01 LOTI v2 (5.4GB), home-hatch backup (6 files)
