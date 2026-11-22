# TeraBox Browser Task Spec — WMXIX lane (prepared 2026-10-15 ~12:30 EDT)
**For:** parent agent to delegate as a live browser task
**Account:** fmmg.mars@gmail.com (Google sign-in authorized by owner 2026-10-15 ~12:00 EDT)
**Session:** should already be active in the live browser (verified working 2026-10-15 morning)

## Part 1 — VERIFY (do not re-upload)
The local staging tarballs for 1A/1D were uploaded and deleted per the storing/moving law.
Confirm these exist in TeraBox with the exact byte counts:

| File | TeraBox path | Expected bytes |
|---|---|---|
| teardown-batch-b.tar.gz | /western-heart/teardown/ | 769,703,936 |
| wrestling-models.tar.gz | /western-heart/wrestling/ | 1,468,416 |

If either is missing or byte-count mismatches, report it — do NOT re-upload (source is gone from disk; re-stage from GitHub if needed).

## Part 2 — TASK 2D: WMXIX ISO → TeraBox
**GitHub release:** https://github.com/mhvnsnt/western-heart/releases/tag/wmxix-iso-v1
**Assets (all verified present):**
- wmxix-500m.part_00 — 524,288,000 bytes
- wmxix-500m.part_aa — 524,288,000 bytes
- wmxix-500m.part_ab — 524,288,000 bytes
- wmxix-500m.part_ac — 411,402,240 bytes
- **Total:** 1,984,266,240 bytes (~1.98 GB)

**TeraBox destination:** /western-heart/games/wmxix/
**Steps:** Download all 4 from the release page → upload to /western-heart/games/wmxix/ → verify each byte count in the TeraBox UI.
**Note:** The local ISO symlink is broken — GitHub release is the only source. Do not look for it on disk.

## Part 3 — CAW.gci (separate browser task, already launched)
Do NOT duplicate. When it lands, hand the .gci file to the wrestling-teardown lane for byte-layout analysis against `wwe-wrestlemania-xix/docs/CAW-EDIT-DATA-WMXIX.md`.
