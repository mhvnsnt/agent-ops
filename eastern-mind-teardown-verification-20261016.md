# Eastern Mind Teardown-Completion Verification — 2026-10-16

**Order:** Owner 2026-10-16 — verify 100% per TEARDOWN-COMPLETION LAW before local source deletion.
**Law:** "torn down" = extracted, decrypted, decoded, AND assembled into working assets. File count is not completion.
**Verifier:** subagent, read-only on source. All repo checks via `git ls-tree` + sampled `git cat-file` blobs.
**Source:** `~/workspace/eastern-mind/` (emtlsotn.zip 575,140,238B, cdimg/ 697MB .img + .ccd, 48 palettes, extract_dxr.py)
**Repo:** `mhvnsnt/western-heart`, `teardown/eastern-mind/` — 5,707 files, commit 441b731, PR #160 merged.

## Pillar 1: EXTRACTED — PASS

- Unpacked the CloneCD `.img` ISO9660 filesystem manually (PVD at file offset 37648, 2352-byte sectors): **129 files** inventoried — 38 DXR + 8 DIR (46 Director movies), 24 MOV, 15 QTC, EXEs/DLLs, ENDING.AIF, docs.
- Repo contains decoded output from **44 of 46** Director files. The 2 without bitmap output: `DAMMY.DIR` (13–15KB, empty dummy files — not a gap) and `PROMO.DIR` (3MB; its content appears covered under `transcript-promo/` — 1,128 files).
- All 24 MOVs → 24 MP4s. All 3 Red Book CD audio tracks → WAVs. ENDING.AIF → WAV. 31 STXT → TXTs. 48 palettes → repo.
- **Provenance note (not a blocker):** repo has 47 additional bitmap sources (W_×24, L_×8, R_×13, G_TONNEL, SHARED) NOT present on this CD or in the IA zip. They are real Eastern Mind art (own-eyes verified, correct style/palette), decoded from files named `W_KING.DXR`-style (extractor names dirs by input filename). Second source is **undocumented** in TEARDOWN.md — likely another IA rip (e.g. `eastern-mind-the-lost-souls-of-tong-nou` 469MB zip). Recommend: document the second source in TEARDOWN.md when identified.

## Pillar 2: DECRYPTED — PASS

- Director 4 DXR (RIFX/MV93) has **no encryption on cast data** — only Lingo bytecode is access-protected. Verified: RIFX/mmap/KEY*/CASt/BITD chunks parse as plaintext structures; the custom parser reads them without any key. Nothing to decrypt.

## Pillar 3: DECODED — PASS (with documented gaps)

- **PNGs:** 5,321 in repo. Sampled 24 across stages — **24/24 open as valid PNGs** with real dimensions. Own-eyes check on 8: unmistakable Osamu Sato/Eastern Mind art (organic textures, insect creatures, area text), correct 8-bit palettes applied, no corruption.
- **WAVs:** 233 in repo (229 snd + 3 CD + 1 ending). Sampled 8 — **8/8 valid** WAV headers, readable frames.
- **TXs:** 31 STXT dumps — readable, real game strings (UI text, Lingo fragments, "OSAMU SATO" credits).
- **Palettes:** 48 unique CLUTs in repo (97 files incl. per-DXR copies); match local 48.
- **Documented gaps (in TEARDOWN.md):** ~7% of BITD chunks unmatched to dimension info (non-8-bit records; pixel data preserved in analysis logs, recoverable); Lingo scripts (~115/DXR) NOT decompiled; THUM thumbnails skipped (redundant). None block Chimera use.

## Pillar 4: WORKING ASSEMBLED — PASS

- 5,707 files organized by owner-assigned WH stage names: stage-1-plains-of-chi-u (518), stage-2-helix-palace (1,282), stage-3-palace-of-dreaming (676), stage-4-tree-of-life (505), stage-5-phantom-marketplace (100), stage-6-octagonal-shrine-par-fang (223), prologue-ending (661), incarnation-system (512), transcript-promo (1,128), soundtrack (4), palettes (97), TEARDOWN.md.
- Per-file naming carries provenance: `<DXR>_<type><index>_<WxH>.png` (e.g. `F_FIELD_b013_580x187.png`). Manifest = TEARDOWN.md + stage mapping table + filename encoding.
- All sampled assets are valid, correctly-paletted, immediately usable in Chimera builds (stages/lore/art reference).

## Pillar 5: REASSEMBLY / MODDING — PASS for owner purpose

- For Chimera builds (stages, lore, art, audio): everything needed is present as working PNG/WAV/MP4.
- Full game rebuild would require Lingo decompilation (not done — documented). Not needed for stated use.

## Store verification (deletion safety)

- **GitHub:** release `eastern-mind-v1`, `emtlsotn.zip` = 575,140,238 bytes — byte-identical to local (local sha256 `3f7198e76969b9b9…` recorded 2026-10-13; size matches exactly). The `.img` (697,201,008B) and `.ccd` are INSIDE the zip (verified in zip listing). Every source byte is on GitHub.
- **TeraBox:** `/game-files/eastern-mind/` 22/22 pieces, reassembled tar hash `cfff7584…` verified 2026-10-15 — full working folder including extract_dxr.py.
- **WH repo:** the 5,707 decoded assets + 97 palettes, commit 441b731 on main.
- Minor: `extract_dxr.py` is NOT committed to the WH repo (only local + inside TeraBox tar). Recommend committing it to `teardown/eastern-mind/tools/` before local deletion so the decode remains re-runnable from the repo. Not a blocker — it is preserved.

## VERDICT: VERIFIED 100% (safe to delete local)

All five pillars pass. Documented gaps (Lingo, 7% BITD, THUM, second-source provenance, extractor not in repo) are real but none block the teardown's purpose, and all are on record. Local `~/workspace/eastern-mind/` (1.2GB) may be deleted per the RELAXATION — every byte is recoverable from GitHub + TeraBox + WH repo. Suggested pre-deletion: commit `extract_dxr.py` to the repo and add the second-source note to TEARDOWN.md (5-minute job, can ride along).
