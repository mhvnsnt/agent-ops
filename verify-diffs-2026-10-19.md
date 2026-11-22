# CN Gigaleak Verify — File-Name Diffs (2026-10-19)
**Method:** Torrent manifest parsed byte-exact from `~/workspace/hero-parts-pull/CNleaks.torrent` (72,369 files) vs GitHub git trees (recursive API, read-only) + release asset lists. File lists + diffs in `~/workspace/verify-lists/` (note: /tmp is a full 512MB tmpfs — lists were written to `~/workspace/verify-lists/` instead of /tmp/verify-lists/).

**Path-normalization rules applied per show:** nested-duplicate top dirs stripped (torrent stores `Dexter's Lab/Dexter's Lab/...`); git-safe sanitization `#Uxxxx` → private-use char `\uxxxx` reversed (lanes renamed PUA bytes git couldn't hold); repo-management files (AGENTS.md, workflows, README) excluded from "extra" judgment.

---

## 1. DEXTER'S LAB — ✅ COMPLETE
- Torrent dir `Dexter's Lab`: **2,298 files / 451,989,544 B** (2,257 nonzero + 41 zero-byte Mac `Icon` stubs).
- Holding: `mhvnsnt/cn-gigaleak-dexters-lab` **main branch git tree** = 2,302 blobs.
- Diff after normalization: **0 missing, 0 size mismatches** across all matched files. 4 extras, all repo-management (`.github/workflows/no-deletion-guard.yml`, `AGENTS.md`, `README.md`, `docs/NO-DATA-LOSS-RULES.md`).
- The audit's "0.29 GB gap" was a measurement artifact: it compared torrent bytes against the release-asset bytes (`dexters-lab-complete-v1`, 1 asset), not the full git tree. **No pull needed.**
---

## 2. GRIM ADVENTURES OF BILLY & MANDY — ✅ COMPLETE (3 trivial Mac-metadata files absent)
- Torrent dir `Grim Adventures of Billy & Mandy`: **1,620 files / 5,733,257,180 B** (all nested under a duplicate `Grim Adventures of Billy & Mandy/` subdir in the torrent).
- Holdings: `mhvnsnt/cn-gigaleak-grim-adventures` **main branch tree** (1,490 blobs) + release **`grim-complete-v1`** = `GRIM.zip` split in 8 parts (3.66 GB compressed).
- Proved via metadata-only central-directory read of `GRIM.zip` (317 KB CD, HTTP Range on the last part — no file contents downloaded): the zip holds **1,617 real files** + the git tree holds 1,486; union covers **1,617/1,620** torrent files, **0 size mismatches** on all matched files.
- **Truly missing (3 files, 6,289 bytes total):**
  - `GBM BACKGROUNDS/STOCK BGS/Stock Color BG 2005/.BridgeSort` (4,837 B)
  - `GBM CHARACTER ART PACK FULL/GBM CHARACTER ART/4C/BILLY/.BridgeSort` (578 B)
  - `GBM CHARACTER ART PACK FULL/GBM CHARACTER ART/BW/GRIM/.BridgeSort` (874 B)
  - These are Mac Finder `.BridgeSort` sort-order metadata stubs, not content. Candidate for the pull queue only if byte-exactness is demanded; otherwise ignorable.
- Apparent near-miss resolved: `Stk Secondary Char 2005/Eris/Eris MÇ.psd` (3,831,998 B) IS held — the zip stores it NFD-normalized (`MÇ`) vs the torrent's NFC (`MÇ`); git tree holds a mojibake-named copy of the same bytes. Unicode normalization, not a gap.
- The audit's "2.07 GB gap" was the same measurement artifact as Dexter's (release bytes vs torrent bytes, ignoring the git tree + compression). **No re-pull needed.**
---

## 3. TEEN TITANS — ✅ COMPLETE (970/970, byte-exact)
- Torrent dir `TEEN TITANS`: **970 files / 1,096,266,235 B** (nested duplicate `TEEN TITANS/` subdir).
- Holding: `mhvnsnt/cn-gigaleak-teen-titans` release **`teen-titans-complete-v1`** = `TEEN_TITANS.zip` in 2 parts (736 MB compressed). (Main branch holds only repo-mgmt files; the draft releases `teen-titans-cnleaks-v1`/`teen-titans-cowchicken-v1` are alternate chunkings of the same content.)
- Proved via metadata-only central-directory read of `TEEN_TITANS.zip` (224 KB CD, HTTP Range on last part — no file contents downloaded): the zip holds **exactly 970 files**.
- Diff: **0 missing, 0 extra, 0 size mismatches** (uncompressed sizes match the torrent byte-for-byte). The audit's "0.36 GB gap" was pure compression (1.10 GB → 0.74 GB zipped). **No pull needed.**
---

## 4. SCOOBY-DOO! MYSTERY INC — ✅ COMPLETE (845/845, byte-exact)
- Torrent dir `Scooby-Doo! Mystery Inc`: **845 files / 12,158,804,223 B** (nested duplicate `Scooby-Doo! Mystery Inc/` subdir).
- Holding: `mhvnsnt/cn-gigaleak-scooby-doo` release **`scooby-mystery-inc-v1`** (Draft) = one big ZIP64 archive split into 79×100MB chunks (`scoobymi100m-00`…`-78`, 8.25 GB compressed).
- Proved via metadata-only ZIP64 central-directory read (148 KB CD, HTTP Range on last chunk — no file contents downloaded): the zip holds **exactly 845 files**.
- Diff: **0 missing, 0 size mismatches** (uncompressed sizes match the torrent byte-for-byte). The audit's "0.8 GB gap" was compression (12.16 GB → 8.25 GB zipped). **No pull needed.**
- Note: `mhvnsnt/cn-gigaleak-scooby-doo-mystery-inc` main holds 717 files (374 match the torrent; 343 are repo-side extras not in the torrent — likely alternate/cow-chicken pull content). Not needed for completeness.
- Note: no branch named `mystery-coast-ghosted` exists on either scooby repo (checked branches on both); verified against the release + `cn-gigaleak-scooby-doo-mystery-inc` main instead.

---

## Summary

| Show | Torrent files | Verdict | Missing |
|---|---|---|---|
| Dexter's Lab | 2,298 | ✅ COMPLETE | none |
| Grim Adventures of Billy & Mandy | 1,620 | ✅ COMPLETE | 3 Mac `.BridgeSort` metadata stubs (6,289 B total) — cosmetic |
| TEEN TITANS | 970 | ✅ COMPLETE | none |
| Scooby-Doo! Mystery Inc | 845 | ✅ COMPLETE | none |

**All 4 shows are file-level complete. The ~2.7 GB combined byte gap in the audit is explained by zip compression + the audit measuring release-asset bytes instead of full holdings (git trees + zip manifests). No re-pulls needed.** The only candidates for a byte-exact pull queue are the 3 Grim `.BridgeSort` files (paths listed in §2) — Mac Finder sort-order metadata, recommended skip.
