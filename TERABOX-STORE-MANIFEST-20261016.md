# TeraBox Store Manifest — 2026-10-16 Store-Everything Campaign

**Purpose:** Everything on local disk → 100% on TeraBox (and GitHub), then local deletes per the relaxed game-files law.
**Browser lane:** ~~upload via TeraBox web (file-grant limit ~225MB per batch, serialized)~~ SUPERSEDED 2026-10-16 — use the API path `~/workspace/tools/terabox-uploader/tbupload.py upload <file> <remotedir>` (4MB chunks, auto-verify, no size cap). See `~/workspace/agent-ops/TERABOX-SESSION-KEEPER.md`.

## ✅ ALREADY ON TERABOX (verified)

| Item | TeraBox path | Verified |
|---|---|---|
| Tekken 6 PSP ISO (855,638,016B) | `/game-files/tekken6-psp-iso/` | 17/17, 2026-10-15 |
| SF EX3 bin (701,813,280B, sha256 059a9516…) | `/game-files/sfex3-usa-bin/` | 14/14, 2026-10-15 |
| Eastern Mind (full) | `/game-files/eastern-mind/` | 22/22, 2026-10-15 |
| WMXIX teardown (26.8MB) | `/western-heart/wmxix-teardown/` | 1/1, 2026-10-15 |
| models-batch-a (1.1GB) | `/western-heart/models/` | 22 parts, 2026-10-14 |
| teardown-batch-c (1.2GB) | `/western-heart/teardown/` | 24 parts, 2026-10-14 |
| AT 2015 (630 files) | `/CN-Gigaleak/adventure-time/` | 75 parts, 2026-10-14 |
| Fosters (159 parts) | `/CN-Gigaleak/fosters/` | 159/159, 2026-10-14 |
| Scooby-Doo | `/CN-Gigaleak/scooby-doo/` | verified, 2026-10-14 |
| Teen Titans (702MB) | `/CN-Gigaleak/teen-titans/` | 29 parts, 2026-10-14 |
| Space Ghost (452MB) | `/CN-Gigaleak/space-ghost/` | 19 parts, 2026-10-14 |
| PPG (15/17 parts) | `/CN-Gigaleak/powerpuff-girls/` | partial, 2026-10-14 |

## 🔄 STAGED FOR TERABOX (browser lane: upload now)

**game-reverse-engineering → `/western-heart/teardowns/`** (prepared 2026-10-16 11:29 EDT)
- Staging: `~/workspace/terabox-staging/game-re/` (hard links, zero extra disk)
- 25 batches (batch-001 … batch-025, ~225MB each) — ALL PENDING
- 9 oversized files (split to ~200MB chunks) — ALL PENDING:
  - `Street Fighter EX Plus Alpha.7z` (252M, 2 chunks)
  - `tekken7/arenas/mishima-dojo-full-8_10_21.rar` (257M, 2 chunks)
  - `tekken6/work/decrypt3/bulk_decrypted.bin` (366M, 2 chunks)
  - `Street Fighter EX Plus Alpha.bin` (504M, 3 chunks)
  - `soulcalibur/xbox-extract/root.olk` (662M, 4 chunks)
  - `Street Fighter EX3 (USA).bin` (669M, 4 chunks) — NOTE: local deleted 2026-10-16 after GH verify; TeraBox copy already exists at `/game-files/sfex3-usa-bin/`
  - `tekken6/tekken6-psp.iso` (816M, 5 chunks) — NOTE: TeraBox copy already exists at `/game-files/tekken6-psp-iso/`
  - `tekken6-ps3/iso/PS3_GAME/USRDIR/TEKKEN.psarc` (4.6G, 24 chunks)
  - `tekken-tag-tournament-2/chunks/Tekken Tag Tournament 2.7z` (5.5G, 28 chunks)
- Plan: `~/workspace/terabox-staging/game-re/BATCH-PLAN.json`
- **After ALL verify byte-identical: delete staging links AND source tree** (except active T6 work — see below)

## ⏳ NEEDS TERABOX (not yet uploaded)

| Item | Size | GitHub status | TeraBox dest (suggested) |
|---|---|---|---|
| TEKKEN.psarc | 4.5G | Uploading to `game-binaries-20261016` | `/game-files/tekken6-ps3/` |
| root.olk (SCII Xbox) | 662M | Uploading to `game-binaries-20261016` | `/game-files/soulcalibur2-xbox/` |
| mishima-dojo rar (T7) | 257M | Uploading to `game-binaries-20261016` | `/game-files/tekken7-arena/` |
| EX Plus Alpha 7z | 252M | Uploading to `sf-ex-plus-alpha-v1` | `/game-files/sfex-plus-alpha/` |
| EX Plus Alpha bin (extracted) | 504M | On `sf-ex-plus-alpha-v1` ✅ | `/game-files/sfex-plus-alpha/` |
| EX2 Plus 7z | 198M | On `sf-ex2-plus-v1` ✅ | `/game-files/sfex2/` |
| Def Jam ISO (incomplete) | 1.4G/4.7G | Not on GH | `/game-files/defjam-ffny/` (after download completes) |
| WMXIX ISO parts (1.9G) | 1.9G | On `wmxix-iso-v1`? verify | `/game-files/wmxix-iso/` |

## 🚫 DO NOT DELETE (protected)

- `game-reverse-engineering/tekken6/` — ACTIVE T6 recon (side chat) + decrypt lanes
- `~/workspace/hero-parts-pull/` (8.3G) — TorBox extraction in-flight
- `~/workspace/cn-pull-bigend/` (6.6G) — AT.zip download in-flight
- `~/workspace/cn-pull-smallend/` (4.6G) — in-flight
- `~/workspace/wmxix-iso/` (1.6G) — Dolphin agent actively using
- `~/workspace/terabox-staging/def-jam/` — Def Jam ISO resume in-flight
- `~/workspace/dxmmii-limbs/` (2.3G) — active character work
- `~/workspace/your_files/` (859M) — owner personal
- `~/workspace/ep01-chronomap/` — NEVER touch (owner raw footage)
- `~/workspace/tools/` — active tools

## 🗑️ DELETED 2026-10-16 (verified both stores)

- SF EX3 bin (701MB) — GH `sf-ex3-v1` + TeraBox `/game-files/sfex3-usa-bin/`, sha256 059a9516… triple-verified. Idle queue #2.
