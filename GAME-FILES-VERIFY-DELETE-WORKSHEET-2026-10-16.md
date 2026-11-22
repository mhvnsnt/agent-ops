# Game Files Verify-and-Delete Worksheet
**Created:** 2026-10-16 ~11:35 EDT (subagent verify-and-delete pass)
**Purpose:** Track GitHub + TeraBox verification for game-reverse-engineering/ (24G) per the RELAXATION law.
**Law:** Delete ONLY when FULL folder is byte-identical on BOTH GitHub and TeraBox. No TeraBox verification = no deletion.

## Summary

| Directory | Size | GitHub Status | TeraBox Status | Active Work? | Deletable? |
|-----------|------|---------------|----------------|--------------|------------|
| tekken-tag-tournament-2/ | 5.6G | ✅ 26/26 parts on release ttt2-7z-v1 | ❓ NEEDS BROWSER CHECK | No (ckpt done) | NO — TeraBox unverified |
| tekken6-ps3/ | 4.7G | ⏳ tekken6-ps3-full-v1 (draft created, upload BLOCKED — large file uploads timing out via proxy) | ❓ NEEDS BROWSER CHECK | No | NO — not uploaded |
| tekken7/ | 3.1G | ✅ tekken7-full-v1 (published, 7 parts) | ❓ NEEDS BROWSER CHECK | No | NO — TeraBox unverified |
| tekken6/ | 1.9G | ✅ ISO byte-identical (855,638,016B) on tekken6-psp-v1 | ❓ NEEDS BROWSER CHECK | No (ckpt done) | NO — TeraBox unverified |
| street-fighter-3d-games/ | 1.9G | ⚠️ Partial (sf-ex releases exist, need per-file check) | ❓ NEEDS BROWSER CHECK | No | NO — incomplete |
| soulcalibur/ | 667M | ✅ soulcalibur2 releases exist | ❓ NEEDS BROWSER CHECK | No | NO — TeraBox unverified |
| tekken3/ | 407M | ⚠️ tekken3-ps1-v1 is DRAFT | ❓ NEEDS BROWSER CHECK | No | NO — draft + TeraBox unverified |
| tekken8/ | 225M | ✅ tekken8-full-v1 (published) | ❓ NEEDS BROWSER CHECK | No | NO — TeraBox unverified |
| virtua-fighter-5/ | 136M | ✅ vf5 releases exist | ❓ NEEDS BROWSER CHECK | No | NO — TeraBox unverified |
| Others (<150M each) | ~500M | Varies | ❓ NEEDS BROWSER CHECK | No | NO — TeraBox unverified |

**Total:** ~24G. **Deletable now:** 0 bytes (TeraBox unverified for all).

## Detailed Findings

### 1. tekken-tag-tournament-2/ (5.6G)
- **Local:** `chunks/Tekken Tag Tournament 2.7z` (5.4G) + tools + logs. Only part_12 remains locally (149M, partial).
- **GitHub:** Release `ttt2-7z-v1` has all 26 parts (part_01 through part_26, 500M each except part_26 at 256M). ✅ COMPLETE
- **TeraBox:** ❓ UNKNOWN — needs browser check of `/game-files/` or similar path.
- **Active work:** No. Checkpoints `extract-ttt2.json` and `t6-ttt2-100.json` both status=done.
- **Teardown %:** ~15-25% per inventory (reassembly in progress).
- **Action needed:** Browser task to verify TeraBox has the 26 parts or reassembled 7z.

### 2. tekken6-ps3/ (4.7G)
- **Local:** `iso/` directory with PS3_DISC.SFB, PS3_GAME/ (4.6G), manifest files.
- **GitHub:** ❌ NO RELEASE FOUND. Not on GitHub.
- **TeraBox:** ❓ UNKNOWN — needs browser check.
- **Active work:** No.
- **Action needed:** Upload to GitHub (as split release) AND TeraBox before eligible for deletion. This is a 4.7G upload job.

### 3. tekken7/ (3.1G)
- **Local:** models/, arenas/, king/, tools/, docs. Appears to be extracted/model files, not a single archive.
- **GitHub:** ❌ No full archive release. Only `tekken-models-batch-2` and `tekken-models-batch-3` (model pulls, not the full 3.1G).
- **TeraBox:** ❓ UNKNOWN — needs browser check.
- **Active work:** No.
- **Action needed:** Determine if the 3.1G is fully represented in GitHub (batches + repo files). Likely needs upload.

### 4. tekken6/ (1.9G)
- **Local:** `tekken6-psp.iso` (816MB, 855,638,016 bytes) + decrypted/, extracted/, tools/, docs/, work/.
- **GitHub:** ✅ ISO byte-identical on release `tekken6-psp-v1` (855,638,016 bytes match). Endings on `tekken6-endings-v1`.
- **TeraBox:** ❓ UNKNOWN — inventory said "going to TeraBox" at `/game-files/tekken6-psp-iso/` (17 × 50MB pieces) but not confirmed complete.
- **Active work:** No. Checkpoints done.
- **Teardown %:** ~40-45% per inventory.
- **Action needed:** Browser task to verify TeraBox has the ISO pieces. Also verify decrypted/extracted files are in western-heart repo.

### 5. street-fighter-3d-games/ (1.9G)
- **Local:** downloads/, extracted/, work/, CATALOG.md.
- **GitHub:** ⚠️ Releases exist (`sf-ex-plus-alpha-v1`, `sf-ex2-plus-v1`, `sf-ex3-v1`) but need per-file verification against local.
- **TeraBox:** ❓ UNKNOWN — needs browser check.
- **Action needed:** Map local files to releases, verify completeness.

### 6. soulcalibur/ (667M)
- **Local:** iso_extract/, TEARDOWN.md, logs.
- **GitHub:** ✅ Releases `soulcalibur2-xbox-extract-v1` and `soulcalibur2-ps2-v1` exist.
- **TeraBox:** ❓ UNKNOWN — needs browser check.
- **Action needed:** Browser verification + confirm local files match releases.

### 7. tekken3/ (407M)
- **Local:** cue file, animations/, audio/, code/.
- **GitHub:** ⚠️ Release `tekken3-ps1-v1` exists but is DRAFT (not finalized).
- **TeraBox:** ❓ UNKNOWN — needs browser check.
- **Action needed:** Finalize draft release, then browser verification.

### 8. tekken8/ (225M)
- **Local:** arenas/, models/.
- **GitHub:** ❌ No release found.
- **TeraBox:** ❓ UNKNOWN.
- **Action needed:** Upload to GitHub and TeraBox.

### 9. virtua-fighter-5/ (136M)
- **Local:** extracted/, models/, stages/.
- **GitHub:** ✅ Releases `vf5-model-library-v1` and `vf5-ps3-v1` exist.
- **TeraBox:** ❓ UNKNOWN — needs browser check.
- **Action needed:** Browser verification.

## TeraBox Browser Verification Needed

For EACH directory above, a browser task must:
1. Open TeraBox, navigate to the game-files folder
2. List contents and record file names + byte sizes
3. Compare against local inventory
4. Report: verified / missing / partial

**Estimated browser work:** 9+ directories. Each needs a folder listing check.

## Uploads Needed (not on GitHub)

These need GitHub upload BEFORE they can be considered for deletion:
- tekken6-ps3/ (4.7G) — no release
- tekken7/ (3.1G) — no full archive release
- tekken8/ (225M) — no release

## What Was NOT Deleted (and why)

**Nothing was deleted** in this pass because TeraBox verification requires browser access, which is unavailable to this subagent. Per the RELAXATION law, deletion requires BOTH stores verified. GitHub-only verification is insufficient.

## Recommendations for Parent

1. **Browser verification lane:** Spawn browser tasks to verify TeraBox contents for each of the 9 directories. This is the blocker for all deletions.
2. **GitHub upload lane:** tekken6-ps3, tekken7, tekken8 need GitHub releases created (split into parts per the 2GB asset limit).
3. **After both verified:** Re-run this pass to delete verified directories.
4. **Do NOT delete** tekken6-ps3, tekken7, tekken8 yet — they're not on GitHub at all.
