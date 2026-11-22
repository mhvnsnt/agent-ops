# Deletion inventory — `feat/re-toolchain-research-20261016` split (2026-10-23)

The add-only split PR **mhvnsnt/game-reverse-engineering #49** (merged 2026-10-23T19:30:47Z, merge `71ac66e300de51f4618741661f17f622a0463659`, LANDED-VERIFIED on main) deliberately EXCLUDED every deletion on the source branch. This file inventories all of them so the owner can decide their fate. **Nothing here is deleted from main — all 478 files still exist on main, verified 2026-10-23 against main's full file tree.**

Prior PR #8 ("Console homebrew/RE toolchain research 2026 + install scripts") was CLOSED unmerged for carrying these deletions. The source branch `feat/re-toolchain-research-20261016` was NOT modified or deleted — left intact for the owning lane at `8c27b87750be3f19e96b77da0b1723f4c1b4241a`.

## The deleting commit

- Commit `b54792a` (2026-10-17T01:20:59Z) — "disk-clear 2026-10-16: data moved to GitHub releases + law update"
- Lane's claim: "Cleared folders (now on releases): tekken-tag-tournament-2, soulcalibur, tekken6 (ISO+recon), tekken7, tekken8, tekken3, virtua-fighter-5, street-fighter EX Plus Alpha, wwf-no-mercy, wwe2k, western-heart-assets — See TEARDOWN-IDLE-QUEUE.md #3-12 and disk-cleanup-log.md for backup locations"
- **Unverified:** whether the claimed GitHub release backups actually exist, are byte-identical, and are retrievable. Per the ONE-STORE RULE, no deletion lands until the backup is verified 100% on a store AND surfaced. That verification has NOT been done for these files.

## Scope corrections (read both)

1. The MERGE-QUEUE.md entry for this branch listed only the soulcalibur/* and tekken-tag-tournament-2/* deletions (~14 files). The real deletion set is **478 files**.
2. An earlier draft of this inventory said 289 — that came from a truncated GitHub compare-API response. The complete list below was re-derived from a full local `git diff` (526 files: 482 D / 41 A / 2 M / 1 R) intersected against current main's full 2,414-path file tree. 478 of the 482 deleted paths still exist on main (4 were already reorganized away by other lanes — listed separately, not pending).

## Group 1 — soulcalibur/ (7 files)

Xbox Soulcalibur II teardown work (the XISO was fully torn down 2026-10-14: OLK format RE'd, 1,097 files/664MB extracted; release `soulcalibur2-xbox-extract-v1`).

| Path | What it is |
|---|---|
| `soulcalibur/TEARDOWN.md` | Soulcalibur teardown doc (73 lines) |
| `soulcalibur/XBOX-EXTRACTION-REPORT.md` | Xbox extraction report (109 lines) |
| `soulcalibur/xbox-extract/Olk_extract.py` | OLK archive extractor (83 lines) |
| `soulcalibur/xbox-extract/olk_extract.py` | Case-variant duplicate of the OLK extractor (83 lines) |
| `soulcalibur/xbox-extract/dl_olk.py` | OLK download helper (74 lines) |
| `soulcalibur/xbox-extract/XBOX-EXTRACTION-REPORT.md` | Copy of the extraction report inside xbox-extract/ (109 lines) |
| `soulcalibur/xbox-extract/signed_url.txt` | Signed download URL (1 line) |

## Group 2 — tekken-tag-tournament-2/ (7 files)

TTT2 surgical-extraction tooling (the lane built these so the 26 release chunks could be extracted without a 27GB disk peak).

| Path | What it is |
|---|---|
| `tekken-tag-tournament-2/HEADER-LISTING.txt` | Archive header listing (80 lines) |
| `tekken-tag-tournament-2/tools/god_surgical.py` | GoD surgical extraction tool (191 lines) |
| `tekken-tag-tournament-2/tools/stfs_blobs.py` | STFS blob tool (114 lines) |
| `tekken-tag-tournament-2/tools/xdvdfs_reader.py` | XDVDFS reader (146 lines) |
| `tekken-tag-tournament-2/tools/__pycache__/god_surgical.cpython-312.pyc` | Bytecode cache (regenerable) |
| `tekken-tag-tournament-2/tools/__pycache__/stfs_blobs.cpython-312.pyc` | Bytecode cache (regenerable) |
| `tekken-tag-tournament-2/tools/__pycache__/xdvdfs_reader.cpython-312.pyc` | Bytecode cache (regenerable) |

## Group 3 — tekken3/ (353 files)

Working files of the completed Tekken 3 teardown (scoreboard 100% ✅: 7 fighters, 15 stages, 8,556 textures, pose solved, 3,247 moves).

- `tekken3/animations/` (8) — `divmot03_king.bin`, `divmot04_yoshimitsu.bin`, `divmot07_xiaoyu.bin`, `divmot09_jin.bin`, `divmot12_bryan.bin`, `divmot13_heihachi.bin`, `divmot16_gunjack.bin`, `divmot99_common.bin` — animation binaries
- `tekken3/bns-table.pkl` — BNS table pickle
- `tekken3/docs/` (5) — `3DMK-MODEL-MAPPING.md`, `BNS-ORGANIZATION-PATTERN.md`, `REVERSE-ENGINEERING-PLAYBOOK.md`, `TEKKEN3-ARCHITECTURE.md`, `TEKKEN3-RIG-LESSONS.md` — reverse-engineering documentation
- `tekken3/model-inventory.csv` / `tekken3/model-inventory.json` — model inventory (the JSON is ~295k lines)
- `tekken3/models/` (30) — per-fighter model dirs: bryan183, gunjack215, heihachi191, jin151, king95, xiaoyu127, yoshimitsu103 — each with `.kmd`, `_parts.obj`, `_parts_montage.png`, `_renderdata.pkl` (+ king95 stance pose JSONs)
- `tekken3/movesets/` (15) — `MOVESET-SUMMARY.md` + per-fighter `moveset_<name>.csv` / `moveset_<name>.json` (7 fighters)
- `tekken3/renders/` (219) — render outputs: `king/lei_full_front.png`, `king/lei_full_raw.obj`, `king/lei_head.obj`, `king/lei_head_front.png`, `king/pose-check/` (6 files: yup/skeleton/stance75), `king/textures/king_adj_*.png` (3), `king/textures/king_block/king_tex_*.png` (49), `king/textures/real_king/king95_*.png` (59), `king/textures/tim_*.png` (98)
- `tekken3/tim-inventory.json` — TIM texture inventory
- `tekken3/tim-output/` (63) — `inventory.json` + 31 TIM texture pairs (`.tim` + `.p000.png` renders)
- `tekken3/tools/local/` (9) — `extract_fighter.py`, `kmd_parse.py`, `moveset_extract.py`, `pose_assemble.py`, `pose_sample_analytic.py`, `tim_extract.py`, `usa_motion.py`, `usa_tables.py`, `validate_usa_spline.py` — the Tekken 3 RE tool scripts

## Group 4 — tekken6/ (18 files) — ACTIVE lane, highest risk

The Tekken 6 PSP decrypt lane's working files. The decrypt6 core path is parked (needs_owner) but the lane's docs just landed via #47 and TEARDOWN-STATUS.md references these paths (e.g. the T6 unblock path cites `tools/k1k2_extract.py` for the sector-cipher validation).

| Path | What it is |
|---|---|
| `tekken6/PPSSPP-LIVE-RUN-GUIDE.md` | PPSSPP live-dump guide (cited in TEARDOWN-STATUS.md unblock path) |
| `tekken6/TEARDOWN.md` | Tekken 6 teardown doc |
| `tekken6/decrypted/EBOOT.DECRYPTED.ELF` | Decrypted EBOOT (4.0MB KIRK-decrypted ELF) |
| `tekken6/docs/K1K2-CALL-SITE-ANALYSIS.md` | K1/K2 call-site analysis doc |
| `tekken6/extracted/DATA401.IDX` | Extracted DATA401 index |
| `tekken6/extracted/DINF_400.BIN` | Extracted DINF_400.BIN |
| `tekken6/tools/SECTOR-CIPHER-REVERSED.md` | Sector-cipher reversal notes |
| `tekken6/tools/k1k2_extract.py` | K1/K2 extraction tool (referenced by TEARDOWN-STATUS.md) |
| `tekken6/tools/mips_dis.py` | MIPS disassembler helper |
| `tekken6/tools/sector_cipher.py` | Sector cipher tool |
| `tekken6/tools/uc_cipher_validate.py` / `uc_cipher_validate2.py` | Unicorn cipher validation scripts |
| `tekken6/tools/uc_keyextract.py` / `tekken6/tools/unicorn_keyextract_test.py` | Key-extraction scripts |
| `tekken6/tools/sdl_noaudio.c` / `sdl_noaudio.so` | SDL no-audio shim (build artifact) |
| `tekken6/tools/__pycache__/*.pyc` (2) | Bytecode caches (regenerable) |

## Group 5 — tekken7/ (71 files)

Tekken 7 (King) lane work — feeds the western-heart Pantera/Leopard King lanes.

- `tekken7/TEKKEN7-ROSTER-MAPPING.md` — roster mapping doc
- `tekken7/arenas/mishima-dojo-map-2_17_24.rar` — Mishima Dojo arena map archive
- `tekken7/king/` (63) — King model: `.fbx` + `.jpg`, `Animate3D.exe`, `License.txt`, `default-grey.jpg`, full PBR texture set (`King_*_D/N/S.png` — diffuse/normal/specular), `views/` (4 renders)
- `tekken7/models/` (5) — `asuka-kazama/asuka-t7-fbx.zip`, `eddy-gordo/eddy-t7-fbx.zip`, `steve-fox/steve-fox-t7-fbx.zip`, `xiaoyu-t8/xiaoyu-t8-phoenix-dress.rar`, `xiaoyu/xiaoyu-t7-fbx.zip`
- `tekken7/tools/umodel_linux` — umodel binary
- NOTE: the branch also renames `tekken7/models/heihachi-mishima/browser-download-20261013T031523.250420183Z-1-1600860987_heihachi_mishima.rar` → `tekken6-ps3/iso/PS3_GAME/USRDIR/EBOOT.BIN` (similarity R055); the old path still exists on main.

## Group 6 — tekken8/ (3 files)

- `tekken8/models/gdrive-dl.sh` — Google Drive download helper
- `tekken8/models/sfmlab-tekken8-asuka_SFM.rar` — Asuka model archive
- `tekken8/models/t8-yoshimitsu-s1-blender.7z` — Yoshimitsu model archive

## Group 7 — wwf-no-mercy/ (19 files)

WWF No Mercy RE work (5,787 anims / 3,570 models / 5,029 textures per the scoreboard; the full teardown folder is slated for Western Heart per owner directive 2026-10-17).

- `wwf-no-mercy/WWF-No-Mercy.zip` — game archive
- `wwf-no-mercy/nm.torrent` — torrent file
- `wwf-no-mercy/docs/` (11) — `ANIMATION-ISOLATION.md`, `CAW-EDIT-DATA.md`, `CAW-SAVE-RECORD-STATUS.md`, `CHARACTER-DATA.md`, `NOMERCY-TEARDOWN.md`, `TEXT-CODE-DICTIONARY.md`, `TOKI2-SEMANTICS.md`, `caw-categories.json`, `caw-name-table.json`, `wrestler-id-table.json`
- `wwf-no-mercy/tools/` (7) — `analyze_nomercy.py`, `anim_extract.py`, `caw_parse.py`, `extract_all_anims.py`, `extract_all_models.py`, `extract_textures.py`, `lzss.py`

## Already gone from main (4 — NOT pending, no action needed)

These 4 paths were deleted on the branch but other lanes already reorganized them off main (e.g. PR #10's deletion-guard check: wwf-no-mercy/re-docs + recomp were 0-byte dead gitlinks superseded by real docs/ + tools/ dirs):

- `tekken3/tools/tekken3recompiled`
- `tekken7/tekkenmods-docs`
- `wwf-no-mercy/re-docs`
- `wwf-no-mercy/recomp`

## Stranded ADDITIONS not in the split's scope (follow-up candidates)

The branch also ADDS 30 files under `tekken6-ps3/` (commit 8c27b87 "TEARDOWN-STATUS sync 2026-10-18 + quickbms tool for tekken6-ps3") that are NOT on main and were NOT included in PR #49 (the split's scope was docs/toolchains/* + AGENTS.md/TEARDOWN-STATUS.md). They are pure additions (zero deletions), so a follow-up add-only PR is safe whenever the owner wants them:

- `tekken6-ps3/docs/` — `BIN_E7-PROBE.md`, `CHARACTER-ASSET-MAP.md`, `COM-FINGERPRINT.md`, `COMMUNITY-TOOLS.md`
- `tekken6-ps3/iso/` — PS3 ISO structure (`PS3_DISC.SFB`, `PS3_GAME/...`, `_manifest_sha256.txt`, `_missed.txt`)
- `tekken6-ps3/*.py`, `*.json`, `*.torrent`, `wave1_manifest.txt` — `t6dl.py`, `tb.py`, `iso_list.py`, `iso_stream_extract.py`, `par_extract.py`, `probe_dir.py`, `probe_psarc.py`, `t6ps3.torrent`, `dl_status.json`, `par_status.json`
- `tekken6-ps3/tools/` — `arc`, `quickbms`, `t6framedatatool`, `tekken5-tools`

## Full path list (478 files still on main)

```
soulcalibur/TEARDOWN.md
soulcalibur/XBOX-EXTRACTION-REPORT.md
soulcalibur/xbox-extract/Olk_extract.py
soulcalibur/xbox-extract/XBOX-EXTRACTION-REPORT.md
soulcalibur/xbox-extract/dl_olk.py
soulcalibur/xbox-extract/olk_extract.py
soulcalibur/xbox-extract/signed_url.txt
tekken-tag-tournament-2/HEADER-LISTING.txt
tekken-tag-tournament-2/tools/__pycache__/god_surgical.cpython-312.pyc
tekken-tag-tournament-2/tools/__pycache__/stfs_blobs.cpython-312.pyc
tekken-tag-tournament-2/tools/__pycache__/xdvdfs_reader.cpython-312.pyc
tekken-tag-tournament-2/tools/god_surgical.py
tekken-tag-tournament-2/tools/stfs_blobs.py
tekken-tag-tournament-2/tools/xdvdfs_reader.py
tekken3/animations/divmot03_king.bin
tekken3/animations/divmot04_yoshimitsu.bin
tekken3/animations/divmot07_xiaoyu.bin
tekken3/animations/divmot09_jin.bin
tekken3/animations/divmot12_bryan.bin
tekken3/animations/divmot13_heihachi.bin
tekken3/animations/divmot16_gunjack.bin
tekken3/animations/divmot99_common.bin
tekken3/bns-table.pkl
tekken3/docs/3DMK-MODEL-MAPPING.md
tekken3/docs/BNS-ORGANIZATION-PATTERN.md
tekken3/docs/REVERSE-ENGINEERING-PLAYBOOK.md
tekken3/docs/TEKKEN3-ARCHITECTURE.md
tekken3/docs/TEKKEN3-RIG-LESSONS.md
tekken3/model-inventory.csv
tekken3/model-inventory.json
tekken3/models/bryan183/bryan.kmd
tekken3/models/bryan183/bryan_parts.obj
tekken3/models/bryan183/bryan_parts_montage.png
tekken3/models/bryan183/bryan_renderdata.pkl
tekken3/models/gunjack215/gunjack.kmd
tekken3/models/gunjack215/gunjack_parts.obj
tekken3/models/gunjack215/gunjack_parts_montage.png
tekken3/models/gunjack215/gunjack_renderdata.pkl
tekken3/models/heihachi191/heihachi.kmd
tekken3/models/heihachi191/heihachi_parts.obj
tekken3/models/heihachi191/heihachi_parts_montage.png
tekken3/models/heihachi191/heihachi_renderdata.pkl
tekken3/models/jin151/jin.kmd
tekken3/models/jin151/jin_parts.obj
tekken3/models/jin151/jin_parts_montage.png
tekken3/models/jin151/jin_renderdata.pkl
tekken3/models/king95/king95.kmd
tekken3/models/king95/king95_parts.obj
tekken3/models/king95/king95_parts_montage.png
tekken3/models/king95/king95_renderdata.pkl
tekken3/models/king95/king95_stance0_pose.json
tekken3/models/king95/king95_stance2_pose.json
tekken3/models/xiaoyu127/xiaoyu.kmd
tekken3/models/xiaoyu127/xiaoyu_parts.obj
tekken3/models/xiaoyu127/xiaoyu_parts_montage.png
tekken3/models/xiaoyu127/xiaoyu_renderdata.pkl
tekken3/models/yoshimitsu103/yoshimitsu.kmd
tekken3/models/yoshimitsu103/yoshimitsu_parts.obj
tekken3/models/yoshimitsu103/yoshimitsu_parts_montage.png
tekken3/models/yoshimitsu103/yoshimitsu_renderdata.pkl
tekken3/movesets/MOVESET-SUMMARY.md
tekken3/movesets/moveset_bryan.csv
tekken3/movesets/moveset_bryan.json
tekken3/movesets/moveset_gunjack.csv
tekken3/movesets/moveset_gunjack.json
tekken3/movesets/moveset_heihachi.csv
tekken3/movesets/moveset_heihachi.json
tekken3/movesets/moveset_jin.csv
tekken3/movesets/moveset_jin.json
tekken3/movesets/moveset_king.csv
tekken3/movesets/moveset_king.json
tekken3/movesets/moveset_xiaoyu.csv
tekken3/movesets/moveset_xiaoyu.json
tekken3/movesets/moveset_yoshimitsu.csv
tekken3/movesets/moveset_yoshimitsu.json
tekken3/renders/king/lei_full_front.png
tekken3/renders/king/lei_full_raw.obj
tekken3/renders/king/lei_head.obj
tekken3/renders/king/lei_head_front.png
tekken3/renders/king/textures/king_adj_00_10244144.png
tekken3/renders/king/textures/king_adj_01_10250740.png
tekken3/renders/king/textures/king_adj_02_10250804.png
tekken3/renders/king/textures/king_block/king_tex_6110.png
tekken3/renders/king/textures/king_block/king_tex_6111.png
tekken3/renders/king/textures/king_block/king_tex_6112.png
tekken3/renders/king/textures/king_block/king_tex_6113.png
tekken3/renders/king/textures/king_block/king_tex_6114.png
tekken3/renders/king/textures/king_block/king_tex_6115.png
tekken3/renders/king/textures/king_block/king_tex_6116.png
tekken3/renders/king/textures/king_block/king_tex_6117.png
tekken3/renders/king/textures/king_block/king_tex_6118.png
tekken3/renders/king/textures/king_block/king_tex_6119.png
tekken3/renders/king/textures/king_block/king_tex_6120.png
tekken3/renders/king/textures/king_block/king_tex_6121.png
tekken3/renders/king/textures/king_block/king_tex_6122.png
tekken3/renders/king/textures/king_block/king_tex_6123.png
tekken3/renders/king/textures/king_block/king_tex_6124.png
tekken3/renders/king/textures/king_block/king_tex_6125.png
tekken3/renders/king/textures/king_block/king_tex_6126.png
tekken3/renders/king/textures/king_block/king_tex_6127.png
tekken3/renders/king/textures/king_block/king_tex_6128.png
tekken3/renders/king/textures/king_block/king_tex_6129.png
tekken3/renders/king/textures/king_block/king_tex_6130.png
tekken3/renders/king/textures/king_block/king_tex_6131.png
tekken3/renders/king/textures/king_block/king_tex_6132.png
tekken3/renders/king/textures/king_block/king_tex_6133.png
tekken3/renders/king/textures/king_block/king_tex_6134.png
tekken3/renders/king/textures/king_block/king_tex_6135.png
tekken3/renders/king/textures/king_block/king_tex_6136.png
tekken3/renders/king/textures/king_block/king_tex_6137.png
tekken3/renders/king/textures/king_block/king_tex_6138.png
tekken3/renders/king/textures/king_block/king_tex_6139.png
tekken3/renders/king/textures/king_block/king_tex_6140.png
tekken3/renders/king/textures/king_block/king_tex_6141.png
tekken3/renders/king/textures/king_block/king_tex_6142.png
tekken3/renders/king/textures/king_block/king_tex_6143.png
tekken3/renders/king/textures/king_block/king_tex_6144.png
tekken3/renders/king/textures/king_block/king_tex_6145.png
tekken3/renders/king/textures/king_block/king_tex_6146.png
tekken3/renders/king/textures/king_block/king_tex_6147.png
tekken3/renders/king/textures/king_block/king_tex_6148.png
tekken3/renders/king/textures/king_block/king_tex_6149.png
tekken3/renders/king/textures/king_block/king_tex_6150.png
tekken3/renders/king/textures/king_block/king_tex_6151.png
tekken3/renders/king/textures/king_block/king_tex_6152.png
tekken3/renders/king/textures/king_block/king_tex_6153.png
tekken3/renders/king/textures/king_block/king_tex_6154.png
tekken3/renders/king/textures/king_block/king_tex_6155.png
tekken3/renders/king/textures/king_block/king_tex_6156.png
tekken3/renders/king/textures/king_block/king_tex_6157.png
tekken3/renders/king/textures/king_block/king_tex_6158.png
tekken3/renders/king/textures/real_king/king95_6213.png
tekken3/renders/king/textures/real_king/king95_6214.png
tekken3/renders/king/textures/real_king/king95_6215.png
tekken3/renders/king/textures/real_king/king95_6216.png
tekken3/renders/king/textures/real_king/king95_6217.png
tekken3/renders/king/textures/real_king/king95_6218.png
tekken3/renders/king/textures/real_king/king95_6219.png
tekken3/renders/king/textures/real_king/king95_6220.png
tekken3/renders/king/textures/real_king/king95_6221.png
tekken3/renders/king/textures/real_king/king95_6222.png
tekken3/renders/king/textures/real_king/king95_6223.png
tekken3/renders/king/textures/real_king/king95_6224.png
tekken3/renders/king/textures/real_king/king95_6225.png
tekken3/renders/king/textures/real_king/king95_6226.png
tekken3/renders/king/textures/real_king/king95_6227.png
tekken3/renders/king/textures/real_king/king95_6228.png
tekken3/renders/king/textures/real_king/king95_6229.png
tekken3/renders/king/textures/real_king/king95_6230.png
tekken3/renders/king/textures/real_king/king95_6231.png
tekken3/renders/king/textures/real_king/king95_6232.png
tekken3/renders/king/textures/real_king/king95_6233.png
tekken3/renders/king/textures/real_king/king95_6234.png
tekken3/renders/king/textures/real_king/king95_6235.png
tekken3/renders/king/textures/real_king/king95_6236.png
tekken3/renders/king/textures/real_king/king95_6237.png
tekken3/renders/king/textures/real_king/king95_6238.png
tekken3/renders/king/textures/real_king/king95_6239.png
tekken3/renders/king/textures/real_king/king95_6240.png
tekken3/renders/king/textures/real_king/king95_6241.png
tekken3/renders/king/textures/real_king/king95_6242.png
tekken3/renders/king/textures/real_king/king95_6243.png
tekken3/renders/king/textures/real_king/king95_6244.png
tekken3/renders/king/textures/real_king/king95_6245.png
tekken3/renders/king/textures/real_king/king95_6246.png
tekken3/renders/king/textures/real_king/king95_6247.png
tekken3/renders/king/textures/real_king/king95_6248.png
tekken3/renders/king/textures/real_king/king95_6249.png
tekken3/renders/king/textures/real_king/king95_6250.png
tekken3/renders/king/textures/real_king/king95_6251.png
tekken3/renders/king/textures/real_king/king95_6252.png
tekken3/renders/king/textures/real_king/king95_6253.png
tekken3/renders/king/textures/real_king/king95_6254.png
tekken3/renders/king/textures/real_king/king95_6255.png
tekken3/renders/king/textures/real_king/king95_6256.png
tekken3/renders/king/textures/real_king/king95_6257.png
tekken3/renders/king/textures/real_king/king95_6258.png
tekken3/renders/king/textures/real_king/king95_6259.png
tekken3/renders/king/textures/real_king/king95_6260.png
tekken3/renders/king/textures/real_king/king95_6261.png
tekken3/renders/king/textures/real_king/king95_6262.png
tekken3/renders/king/textures/real_king/king95_6263.png
tekken3/renders/king/textures/real_king/king95_6264.png
tekken3/renders/king/textures/real_king/king95_6265.png
tekken3/renders/king/textures/real_king/king95_6266.png
tekken3/renders/king/textures/real_king/king95_6267.png
tekken3/renders/king/textures/real_king/king95_6268.png
tekken3/renders/king/textures/real_king/king95_6269.png
tekken3/renders/king/textures/real_king/king95_6270.png
tekken3/renders/king/textures/real_king/king95_6271.png
tekken3/renders/king/textures/tim_6061_64x88.png
tekken3/renders/king/textures/tim_6062_128x64.png
tekken3/renders/king/textures/tim_6063_128x128.png
tekken3/renders/king/textures/tim_6064_64x128.png
tekken3/renders/king/textures/tim_6065_128x128.png
tekken3/renders/king/textures/tim_6066_64x128.png
tekken3/renders/king/textures/tim_6067_128x32.png
tekken3/renders/king/textures/tim_6068_128x64.png
tekken3/renders/king/textures/tim_6069_64x128.png
tekken3/renders/king/textures/tim_6070_64x128.png
tekken3/renders/king/textures/tim_6071_64x128.png
tekken3/renders/king/textures/tim_6072_64x128.png
tekken3/renders/king/textures/tim_6073_64x112.png
tekken3/renders/king/textures/tim_6074_64x128.png
tekken3/renders/king/textures/tim_6075_128x64.png
tekken3/renders/king/textures/tim_6076_64x128.png
tekken3/renders/king/textures/tim_6077_64x128.png
tekken3/renders/king/textures/tim_6078_64x88.png
tekken3/renders/king/textures/tim_6079_128x40.png
tekken3/renders/king/textures/tim_6080_128x128.png
tekken3/renders/king/textures/tim_6081_128x128.png
tekken3/renders/king/textures/tim_6082_128x128.png
tekken3/renders/king/textures/tim_6083_128x128.png
tekken3/renders/king/textures/tim_6084_128x128.png
tekken3/renders/king/textures/tim_6085_128x128.png
tekken3/renders/king/textures/tim_6086_128x128.png
tekken3/renders/king/textures/tim_6087_128x128.png
tekken3/renders/king/textures/tim_6088_128x128.png
tekken3/renders/king/textures/tim_6089_128x128.png
tekken3/renders/king/textures/tim_6090_128x128.png
tekken3/renders/king/textures/tim_6091_128x128.png
tekken3/renders/king/textures/tim_6092_128x128.png
tekken3/renders/king/textures/tim_6093_128x128.png
tekken3/renders/king/textures/tim_6094_128x128.png
tekken3/renders/king/textures/tim_6095_128x128.png
tekken3/renders/king/textures/tim_6096_128x128.png
tekken3/renders/king/textures/tim_6097_128x128.png
tekken3/renders/king/textures/tim_6098_128x128.png
tekken3/renders/king/textures/tim_6099_128x128.png
tekken3/renders/king/textures/tim_6100_128x128.png
tekken3/renders/king/textures/tim_6101_128x128.png
tekken3/renders/king/textures/tim_6102_128x128.png
tekken3/renders/king/textures/tim_6103_128x128.png
tekken3/renders/king/textures/tim_6104_128x128.png
tekken3/renders/king/textures/tim_6105_128x128.png
tekken3/renders/king/textures/tim_6106_128x128.png
tekken3/renders/king/textures/tim_6107_128x128.png
tekken3/renders/king/textures/tim_6108_128x128.png
tekken3/renders/king/textures/tim_6109_128x128.png
tekken3/renders/king/textures/tim_6110_64x128.png
tekken3/renders/king/textures/tim_6111_128x128.png
tekken3/renders/king/textures/tim_6112_64x128.png
tekken3/renders/king/textures/tim_6113_64x128.png
tekken3/renders/king/textures/tim_6114_64x128.png
tekken3/renders/king/textures/tim_6115_128x64.png
tekken3/renders/king/textures/tim_6116_64x128.png
tekken3/renders/king/textures/tim_6117_128x64.png
tekken3/renders/king/textures/tim_6118_128x128.png
tekken3/renders/king/textures/tim_6119_128x64.png
tekken3/renders/king/textures/tim_6120_128x128.png
tekken3/renders/king/textures/tim_6121_128x64.png
tekken3/renders/king/textures/tim_6122_128x128.png
tekken3/renders/king/textures/tim_6123_128x128.png
tekken3/renders/king/textures/tim_6124_128x128.png
tekken3/renders/king/textures/tim_6125_64x128.png
tekken3/renders/king/textures/tim_6126_128x128.png
tekken3/renders/king/textures/tim_6127_64x128.png
tekken3/renders/king/textures/tim_6128_64x128.png
tekken3/renders/king/textures/tim_6129_128x128.png
tekken3/renders/king/textures/tim_6130_128x128.png
tekken3/renders/king/textures/tim_6131_128x128.png
tekken3/renders/king/textures/tim_6132_128x128.png
tekken3/renders/king/textures/tim_6133_128x128.png
tekken3/renders/king/textures/tim_6134_128x128.png
tekken3/renders/king/textures/tim_6135_128x128.png
tekken3/renders/king/textures/tim_6136_128x128.png
tekken3/renders/king/textures/tim_6137_128x128.png
tekken3/renders/king/textures/tim_6138_128x128.png
tekken3/renders/king/textures/tim_6139_128x128.png
tekken3/renders/king/textures/tim_6140_128x128.png
tekken3/renders/king/textures/tim_6141_128x128.png
tekken3/renders/king/textures/tim_6142_128x128.png
tekken3/renders/king/textures/tim_6143_128x128.png
tekken3/renders/king/textures/tim_6144_128x128.png
tekken3/renders/king/textures/tim_6145_128x128.png
tekken3/renders/king/textures/tim_6146_128x128.png
tekken3/renders/king/textures/tim_6147_128x128.png
tekken3/renders/king/textures/tim_6148_128x128.png
tekken3/renders/king/textures/tim_6149_128x128.png
tekken3/renders/king/textures/tim_6150_128x128.png
tekken3/renders/king/textures/tim_6151_128x128.png
tekken3/renders/king/textures/tim_6152_128x128.png
tekken3/renders/king/textures/tim_6153_128x128.png
tekken3/renders/king/textures/tim_6154_128x128.png
tekken3/renders/king/textures/tim_6155_128x128.png
tekken3/renders/king/textures/tim_6156_128x128.png
tekken3/renders/king/textures/tim_6157_128x128.png
tekken3/renders/king/textures/tim_6158_128x128.png
tekken3/renders/pose-check/king_f75_yup.png
tekken3/renders/pose-check/king_skeleton.png
tekken3/renders/pose-check/king_skeleton_2d.png
tekken3/renders/pose-check/king_stance75.json
tekken3/renders/pose-check/king_stance75.obj
tekken3/renders/pose-check/king_stance75_verts.png
tekken3/tim-inventory.json
tekken3/tim-output/inventory.json
tekken3/tim-output/tim_0000_off_000123B4.p000.png
tekken3/tim-output/tim_0000_off_000123B4.tim
tekken3/tim-output/tim_0001_off_000125F4.p000.png
tekken3/tim-output/tim_0001_off_000125F4.tim
tekken3/tim-output/tim_0002_off_00012834.p000.png
tekken3/tim-output/tim_0002_off_00012834.tim
tekken3/tim-output/tim_0003_off_00012A74.p000.png
tekken3/tim-output/tim_0003_off_00012A74.tim
tekken3/tim-output/tim_0004_off_00012CB4.p000.png
tekken3/tim-output/tim_0004_off_00012CB4.tim
tekken3/tim-output/tim_0005_off_00012EF4.p000.png
tekken3/tim-output/tim_0005_off_00012EF4.tim
tekken3/tim-output/tim_0006_off_00013134.p000.png
tekken3/tim-output/tim_0006_off_00013134.tim
tekken3/tim-output/tim_0007_off_00013374.p000.png
tekken3/tim-output/tim_0007_off_00013374.tim
tekken3/tim-output/tim_0008_off_000135B4.p000.png
tekken3/tim-output/tim_0008_off_000135B4.tim
tekken3/tim-output/tim_0009_off_000137F4.p000.png
tekken3/tim-output/tim_0009_off_000137F4.tim
tekken3/tim-output/tim_0010_off_00013A34.p000.png
tekken3/tim-output/tim_0010_off_00013A34.tim
tekken3/tim-output/tim_0011_off_00013C74.p000.png
tekken3/tim-output/tim_0011_off_00013C74.tim
tekken3/tim-output/tim_0012_off_00013EB4.p000.png
tekken3/tim-output/tim_0012_off_00013EB4.tim
tekken3/tim-output/tim_0013_off_000140F4.p000.png
tekken3/tim-output/tim_0013_off_000140F4.tim
tekken3/tim-output/tim_0014_off_00014334.p000.png
tekken3/tim-output/tim_0014_off_00014334.tim
tekken3/tim-output/tim_0015_off_00014574.p000.png
tekken3/tim-output/tim_0015_off_00014574.tim
tekken3/tim-output/tim_0016_off_000147B4.p000.png
tekken3/tim-output/tim_0016_off_000147B4.tim
tekken3/tim-output/tim_0017_off_000149F4.p000.png
tekken3/tim-output/tim_0017_off_000149F4.tim
tekken3/tim-output/tim_0018_off_00014C34.p000.png
tekken3/tim-output/tim_0018_off_00014C34.tim
tekken3/tim-output/tim_0019_off_00014E74.p000.png
tekken3/tim-output/tim_0019_off_00014E74.tim
tekken3/tim-output/tim_0020_off_000150B4.p000.png
tekken3/tim-output/tim_0020_off_000150B4.tim
tekken3/tim-output/tim_0021_off_000152F4.p000.png
tekken3/tim-output/tim_0021_off_000152F4.tim
tekken3/tim-output/tim_0022_off_00015534.p000.png
tekken3/tim-output/tim_0022_off_00015534.tim
tekken3/tim-output/tim_0023_off_00015774.p000.png
tekken3/tim-output/tim_0023_off_00015774.tim
tekken3/tim-output/tim_0024_off_000159B4.p000.png
tekken3/tim-output/tim_0024_off_000159B4.tim
tekken3/tim-output/tim_0025_off_00015BF4.p000.png
tekken3/tim-output/tim_0025_off_00015BF4.tim
tekken3/tim-output/tim_0026_off_00015E34.p000.png
tekken3/tim-output/tim_0026_off_00015E34.tim
tekken3/tim-output/tim_0027_off_00016074.p000.png
tekken3/tim-output/tim_0027_off_00016074.tim
tekken3/tim-output/tim_0028_off_000162B4.p000.png
tekken3/tim-output/tim_0028_off_000162B4.tim
tekken3/tim-output/tim_0029_off_000164F4.p000.png
tekken3/tim-output/tim_0029_off_000164F4.tim
tekken3/tim-output/tim_0030_off_00016734.p000.png
tekken3/tim-output/tim_0030_off_00016734.tim
tekken3/tools/local/extract_fighter.py
tekken3/tools/local/kmd_parse.py
tekken3/tools/local/moveset_extract.py
tekken3/tools/local/pose_assemble.py
tekken3/tools/local/pose_sample_analytic.py
tekken3/tools/local/tim_extract.py
tekken3/tools/local/usa_motion.py
tekken3/tools/local/usa_tables.py
tekken3/tools/local/validate_usa_spline.py
tekken6/PPSSPP-LIVE-RUN-GUIDE.md
tekken6/TEARDOWN.md
tekken6/decrypted/EBOOT.DECRYPTED.ELF
tekken6/docs/K1K2-CALL-SITE-ANALYSIS.md
tekken6/extracted/DATA401.IDX
tekken6/extracted/DINF_400.BIN
tekken6/tools/SECTOR-CIPHER-REVERSED.md
tekken6/tools/__pycache__/k1k2_extract.cpython-312.pyc
tekken6/tools/__pycache__/sector_cipher.cpython-312.pyc
tekken6/tools/k1k2_extract.py
tekken6/tools/mips_dis.py
tekken6/tools/sdl_noaudio.c
tekken6/tools/sdl_noaudio.so
tekken6/tools/sector_cipher.py
tekken6/tools/uc_cipher_validate.py
tekken6/tools/uc_cipher_validate2.py
tekken6/tools/uc_keyextract.py
tekken6/tools/unicorn_keyextract_test.py
tekken7/TEKKEN7-ROSTER-MAPPING.md
tekken7/arenas/mishima-dojo-map-2_17_24.rar
tekken7/king/5PMH7G85GYN7P71W3BD1V0249.fbx
tekken7/king/5PMH7G85GYN7P71W3BD1V0249.jpg
tekken7/king/Animate3D.exe
tekken7/king/King_ArmBelt_D.png
tekken7/king/King_ArmBelt_N.png
tekken7/king/King_ArmBelt_S.png
tekken7/king/King_ArmProtectors_D.png
tekken7/king/King_ArmProtectors_N.png
tekken7/king/King_ArmProtectors_S.png
tekken7/king/King_Arms_D.png
tekken7/king/King_Arms_N.png
tekken7/king/King_Arms_S.png
tekken7/king/King_BootProtector1_D.png
tekken7/king/King_BootProtector1_N.png
tekken7/king/King_BootProtector1_S.png
tekken7/king/King_BootProtector2_D.png
tekken7/king/King_BootProtector2_N.png
tekken7/king/King_BootProtector2_S.png
tekken7/king/King_Buckles_D.png
tekken7/king/King_Buckles_N.png
tekken7/king/King_Buckles_S.png
tekken7/king/King_DefaultHead_D.png
tekken7/king/King_DefaultHead_N.png
tekken7/king/King_DefaultHead_S.png
tekken7/king/King_Eye_D.png
tekken7/king/King_Eye_N.png
tekken7/king/King_Eye_S.png
tekken7/king/King_Eyehole_D.png
tekken7/king/King_Eyehole_N.png
tekken7/king/King_Eyehole_S.png
tekken7/king/King_FootAcc_D.png
tekken7/king/King_FootAcc_N.png
tekken7/king/King_FootAcc_S.png
tekken7/king/King_Hand_D.png
tekken7/king/King_Hand_N.png
tekken7/king/King_Hand_S.png
tekken7/king/King_MaskFur1_D.png
tekken7/king/King_MaskFur1_N.png
tekken7/king/King_MaskFur1_S.png
tekken7/king/King_Neck_D.png
tekken7/king/King_Neck_N.png
tekken7/king/King_Neck_S.png
tekken7/king/King_PantsLogo_D.png
tekken7/king/King_PantsLogo_N.png
tekken7/king/King_PantsLogo_S.png
tekken7/king/King_PantsLower_D.png
tekken7/king/King_PantsLower_N.png
tekken7/king/King_PantsLower_S.png
tekken7/king/King_PantsUpper_D.png
tekken7/king/King_PantsUpper_N.png
tekken7/king/King_PantsUpper_S.png
tekken7/king/King_Teeth_D.png
tekken7/king/King_Teeth_N.png
tekken7/king/King_Teeth_S.png
tekken7/king/King_Torso_D.png
tekken7/king/King_Torso_N.png
tekken7/king/King_Torso_S.png
tekken7/king/License.txt
tekken7/king/default-grey.jpg
tekken7/king/views/king_back.png
tekken7/king/views/king_front.png
tekken7/king/views/king_left.png
tekken7/king/views/king_right.png
tekken7/models/asuka-kazama/asuka-t7-fbx.zip
tekken7/models/eddy-gordo/eddy-t7-fbx.zip
tekken7/models/steve-fox/steve-fox-t7-fbx.zip
tekken7/models/xiaoyu-t8/xiaoyu-t8-phoenix-dress.rar
tekken7/models/xiaoyu/xiaoyu-t7-fbx.zip
tekken7/tools/umodel_linux
tekken8/models/gdrive-dl.sh
tekken8/models/sfmlab-tekken8-asuka_SFM.rar
tekken8/models/t8-yoshimitsu-s1-blender.7z
wwf-no-mercy/WWF-No-Mercy.zip
wwf-no-mercy/docs/ANIMATION-ISOLATION.md
wwf-no-mercy/docs/CAW-EDIT-DATA.md
wwf-no-mercy/docs/CAW-SAVE-RECORD-STATUS.md
wwf-no-mercy/docs/CHARACTER-DATA.md
wwf-no-mercy/docs/NOMERCY-TEARDOWN.md
wwf-no-mercy/docs/TEXT-CODE-DICTIONARY.md
wwf-no-mercy/docs/TOKI2-SEMANTICS.md
wwf-no-mercy/docs/caw-categories.json
wwf-no-mercy/docs/caw-name-table.json
wwf-no-mercy/docs/wrestler-id-table.json
wwf-no-mercy/nm.torrent
wwf-no-mercy/tools/analyze_nomercy.py
wwf-no-mercy/tools/anim_extract.py
wwf-no-mercy/tools/caw_parse.py
wwf-no-mercy/tools/extract_all_anims.py
wwf-no-mercy/tools/extract_all_models.py
wwf-no-mercy/tools/extract_textures.py
wwf-no-mercy/tools/lzss.py
```

## Owner decisions needed

For each group: do the claimed GitHub release backups from `b54792a` exist, byte-identical and retrievable (per TEARDOWN-IDLE-QUEUE.md #3-12 / disk-cleanup-log.md)? If yes and surfaced, the deletions can be re-proposed in a separate PR. If not, these files stay on main.

1. tekken6/ (18 files) — ACTIVE lane working files; the T6 unblock path in TEARDOWN-STATUS.md cites `tools/k1k2_extract.py`. Recommend: KEEP until decrypt6 resolves.
2. tekken3/ (353 files) — completed teardown's working files (docs/models/movesets/renders/tools). Recommend: KEEP (or verify release backup first).
3. wwf-no-mercy/ (19 files) — teardown slated for Western Heart. Recommend: KEEP.
4. tekken7/ (71 files) — King/Pantera lane inputs. Recommend: KEEP.
5. soulcalibur/ (7), tekken-tag-tournament-2/ (7), tekken8/ (3) — teardown done/released or parked; verify backups, then decide.
6. tekken6-ps3/ stranded additions (30 files) — land as a follow-up add-only PR, or leave on the branch?
