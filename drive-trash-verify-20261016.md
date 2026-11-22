# Google Drive Trash Verification — 2026-10-16

**Verdict: DO NOT EMPTY.** 17 of 25 trashed items have NO verified safe copy elsewhere.
Trash holds ~2.5GB. Emptying would permanently destroy unique parts of Drive-only
split archives with no recovery path.

## Method
- Listed all trashed files via Drive API (`q=trashed=true`): 25 items, complete (no nextPageToken).
- Cross-checked each against: Drive live (non-trashed) files, STORAGE-MANIFEST.json
  (`~/workspace/agent-ops/STORAGE-MANIFEST.json`), GitHub releases (byte-exact size
  match required), local `~/workspace` copies.

## Key finding
The `-automigrate-2026-10-14` files are split-archive parts (100MB each). Each set
needs ALL parts to reassemble. The trashed parts are the ONLY copies of those
specific parts — no live Drive duplicates exist. Deleting them destroys the archive.

## SAFE (3 items — byte-identical copy verified elsewhere)

| Item | Size | Safe copy |
|---|---|---|
| steal-like-artist-packs2-automigrate-2026-10-14.part_002 | 100MB | GitHub `mhvnsnt/google-drive-repo` @ `steal-like-artist-packs2-automigrate-2026-10-14`, asset `gh_steal-like-artist-packs2.tar` (936,069,120 bytes = manifest bytes) |
| triple-xxx-automigrate-2026-10-14.part_000 | 100MB | GitHub `mhvnsnt/google-drive-repo` @ `triple-xxx-automigrate-2026-10-14`, asset `triple-xxx-automigrate-2026-10-14.tar` (182,784,000 bytes = manifest bytes) |
| Gumball_Bible.pdf | 109.9MB | GitHub `mhvnsnt/cn-gigaleak-gumball` @ `gumball-bibles-v1`, `Gumball_Bible.pdf` (109,925,672 bytes, exact) |

## UNSAFE (17 items — DO NOT DELETE)

**Drive-only split-archive parts (unique, irreplaceable):**

| Item | Size | Why unsafe |
|---|---|---|
| card-audit-models-automigrate-2026-10-14.part_000 | 100MB | Drive-only 5-part set; parts 000+002 trashed. Local `~/workspace/card-audit` is 12K stub (models gone). |
| card-audit-models-automigrate-2026-10-14.part_002 | 100MB | Same set. |
| wg-ep01-dialogue-v7-automigrate-2026-10-14.part_000 | 100MB | Drive-only 2-part set; part_000 trashed. (Superseded by v9, but v7 file itself exists only here.) |
| promo-work-automigrate-2026-10-14.part_000 | 100MB | Drive-only 2-part set; part_000 trashed. Not found locally. |
| bannon-teardown-drive2-automigrate-2026-10-14.part_000 | 100MB | Drive-only 2-part set; part_000 trashed. Local `bannon-teardown/` is 162M vs 184.7MB archive — unverified. |
| attire-pull-cain-automigrate-2026-10-14.part_000 (id 1Oe7cBVz…) | 100MB | Drive-only 2-part set; part_000 trashed. Not found locally. |
| attire-pull-cain-automigrate-2026-10-14.part_000 (id 1NiwwkR…) | 100MB | Duplicate name, different file — also trashed. |
| sombra-negra-automigrate-2026-10-14.part_000 | 100MB | Drive-only 3-part set; part_000 trashed. Local `bannon-reskin/sombra-negra` is 208K vs 241MB archive. |
| cn-gigaleak-work-automigrate-2026-10-14.part_033 | 100MB | Drive-only; 1 of 7 trashed parts of 50-part set. GitHub coverage incomplete (gh3 in flight, deletion gate closed). |
| cn-gigaleak-work-automigrate-2026-10-14.part_038 | 100MB | Same. |
| cn-gigaleak-work-automigrate-2026-10-14.part_040 | 100MB | Same. |
| cn-gigaleak-work-automigrate-2026-10-14.part_042 | 100MB | Same. |
| cn-gigaleak-work-automigrate-2026-10-14.part_044 | 100MB | Same. |
| cn-gigaleak-work-automigrate-2026-10-14.part_046 | 100MB | Same. |
| cn-gigaleak-work-automigrate-2026-10-14.part_048 | 100MB | Same. |
| new-drive-assets-automigrate-2026-10-14.part_000 | 100MB | Drive-only 4-part set; parts 000,001,002 trashed (only 003 live). Not found locally. |
| new-drive-assets-automigrate-2026-10-14.part_001 | 100MB | Same. |
| new-drive-assets-automigrate-2026-10-14.part_002 | 100MB | Same. |

**Loose files (no byte-identical copy found):**

| Item | Size | Why unsafe |
|---|---|---|
| ppg.zip | 134.8MB | GitHub `ppg-complete-v1` has `PPGZ.zip` (134,771,574 bytes) — 6,956 bytes smaller, different name. NOT identical. |
| dexter-lab.zip | 157.7MB | GitHub `dexters-lab-complete-v1` has `Dexter.s.Lab.zip` (157,313,281 bytes) — 405KB smaller, different name. NOT identical. |
| COMPGUIDE_CHARACTERS.PDF | 2.2MB | No copy located. |
| GUMBALL_GUIDE_2012_HR_text.pdf | 5.5MB | GitHub has `GUMBALL_GUIDE_2012_HR.pdf` (60.5MB) + `.epub` — different files, not this `_text.pdf`. |

## Recommendation
1. **Do NOT empty the trash.** Per SAFE-STORAGE-FIRST law.
2. The 3 SAFE items *could* be permanently deleted individually, but leaving them
   trashed costs nothing and they restore cleanly if ever needed.
3. Open question for owner: several Drive-only archives are now UNRECOVERABLE
   even from trash-emptied state (their parts are split across live + trash).
   Consider restoring the trashed parts (un-trash) so each set is whole in one
   place, then re-evaluating.
4. Root cause TBD: why automigrate parts were trashed at all (owner action vs
   worker error) — the manifest still lists them as the canonical store.

*Verified 2026-10-16 ~09:35 EDT by subagent. Drive API + gh CLI + local fs.*
