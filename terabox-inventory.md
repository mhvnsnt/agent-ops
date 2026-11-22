# TeraBox Master Backup Inventory
**Owner directive 2026-10-13. TeraBox Premium 5TB (trial expires 2026-10-20 — remind owner by 2026-10-18).**
**Structure: `/western-heart/<category>/<item>/`**
**Staging worker:** terabox-staging-prep, 2026-10-13/14. All local tarballs `gzip -t` verified.

## STAGED TARBALLS (~/workspace/terabox-staging/) — status: STAGED, pending browser upload
| File | Size (bytes) | Entries | TeraBox Path | Contents |
|------|--------------|---------|--------------|----------|
| teardown-batch-b.tar.gz | 734MB (769,703,936) | 42,320 | /western-heart/teardown/ | Full western-heart/teardown/ repo dir: urban-reign, tekken3, models, wwf-no-mercy, wmxix, tekken7, vf5, tekken6, ttt2, + docs. **REBUILT 2026-10-14 — original file was corrupt (truncated gzip).** |
| teardown-batch-c.tar.gz | 1.2GB (~1.29GB) | 1,701 | /western-heart/teardown/ | Wrestling-lane outputs NOT in batch-b: game-re wwe2k, wwe2k14, wwf-no-mercy, urban-reign docs + worktree analysis (tekken7 roster-mapping/tools, tekken3 inventories/renders, no-mercy docs). Excludes in-flight `wwe2k/wwe2k14.rar` (lane writing it at staging time). |
| models-batch-a.tar.gz | 1.1GB (~1.18GB) | 1,011 | /western-heart/models/ | tekken7/models/king-variants (2.1GB), street-fighter-5/models/rashid (247MB), models/pharaohillusion (506MB) |
| wrestling-models.tar.gz | 1.4MB (~1.47MB) | 5,633 | /western-heart/wrestling/ | wwe-wrestler-models repo @ bfde439: 2,700+ No Mercy OBJs, 126 WMXIX wrestlers, tools, MANIFEST.txt |
| western-heart-docs.tar.gz | 54MB (55,869,711) | 4,616 | /western-heart/docs/ | CANON, MISSION, CHIMERA-ARCHITECTURE, ROSTER, roster/pantera (tail-rig GLBs, P2 attire pack), moveset-lib, customization |

**Staged total: ~3.1GB (5 files)**

## GITHUB RELEASE → TERABOX (download from GitHub, upload to TeraBox) — status: PENDING
Byte counts verified via `gh release view` 2026-10-13. Release page: `https://github.com/mhvnsnt/western-heart/releases/tag/<tag>`. Per-asset URL: `https://github.com/mhvnsnt/western-heart/releases/download/<tag>/<asset>`.
| Release tag | Assets | Bytes | TeraBox Path |
|-------------|--------|-------|--------------|
| ttt2-7z-v1 | 26 (`ttt2-500m.part_01`–`26`) | 13,363,624,393 (~13.36GB) | /western-heart/games/tekken-tag-tournament-2/ |
| urban-reign-iso-v1 | 9 | 4,297,261,056 (~4.30GB) | /western-heart/games/urban-reign/ |
| vf5-ps3-v1 | ~89 | ~4,946,862,305 (~4.95GB) | /western-heart/games/vf5/ |
| wmxix-iso-v1 | 4 | 1,984,266,240 (~1.98GB) | /western-heart/games/wmxix/ |
| soulcalibur2-ps2-v1 | 1 (`Soulcalibur-II.iso`) | 1,376,845,824 (~1.38GB) | /western-heart/games/soulcalibur-2/ |
| tekken6-psp-v1 | 1 (`tekken6-psp.iso`) | 855,638,016 (~0.86GB) | /western-heart/games/tekken-6/ |
| eastern-mind-v1 | 1 (`emtlsotn.zip`) | 575,140,238 (~0.58GB) | /western-heart/games/eastern-mind/ |
| king-variants-2026-10-13 | 6 | 566,607,338 (~0.57GB) | /western-heart/models/king-variants/ |
| rashid-models-20261013 | 3 | 57,634,970 (~0.06GB) | /western-heart/models/rashid/ |

**GitHub→TeraBox total: ~27.9GB (excludes in-progress doa4-iso-v1 ~7.47GB)**
**Grand total (staged + GitHub): ~31GB**

## OTHER WESTERN-HEART RELEASES (not in current browser spec — available later)
| Release tag | Notes |
|-------------|-------|
| pharaohillusion-2026-10-13 | Latest release; overlaps models-batch-a tarball |
| tekken-models-batch-2 | ~3.1GB, 14 assets |
| tekken-models-batch-3 | ~0.76GB, 23 assets |
| tekken6-endings-v1 | 46 files, ~0.34GB |
| tekken3-ps1-v1 | Draft |
| no-mercy-n64-v1 | ~32MB |
| doa4-iso-v1 | 30 assets ~7.47GB — was IN PROGRESS; verify complete before queueing |

## KNOWN ISSUES / FLAGS
- **teardown-batch-b was corrupt** (truncated gzip, `gzip -t` failed). Rebuilt from `~/workspace/western-heart/teardown/` 2026-10-14 — new file 734MB, integrity verified. Never upload the old 352MB file (already replaced in staging).
- **WMXIX ISO not on local disk** — symlink `game-reverse-engineering/wwe-wrestlemania-xix/WWE Wrestlemania XIX (USA).iso` is broken. GitHub release `wmxix-iso-v1` is the only source.
- **Def Jam FFNY ISO is 109MB** (`~/workspace/defjam-work/iso/SLUS_210.04.Def Jam - Fight for NY.iso`) — far too small for a real PS2 ISO; likely partial/dummy. NOT staged. Needs coordinator decision.
- **wwe2k14.rar in-flight** — wrestling-game-teardown lane was actively writing it during staging (growing 243→273MB). Excluded from batch-c; stage as `teardown-batch-c2` follow-up once the lane finishes.
- **Disk was 92–98% during staging** (disk-space-guardian cron was cleaning concurrently). Tarballs built successfully; disk back to ~94% after compression cleanup.

## STATUS
- [x] Staging: all 5 tarballs built, integrity-verified (2026-10-14)
- [x] BROWSER-TASKS.md written: ~/workspace/terabox-staging/BROWSER-TASKS.md
- [ ] Browser uploads: Section 1 (5 tarballs, ~3.1GB) + Section 2 (9 releases, ~27.9GB) — pending parent delegation
- [ ] Verification: TeraBox byte counts vs this doc after each upload
