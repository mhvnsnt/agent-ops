# HANDOFF — TEARDOWNS

State verified 2026-10-23. Sources: checkpoints in `checkpoints/` (`extract-nomercy.json`, `wh-tekken6-100.json`, `tekken6-data401-decrypt.json`, `teardown-sweep-tekken6-psp.json`, `ttt2-resume-100.json`, `wh-ttt2-100.json`, `defjam-teardown.json`, `wh-defjam-100.json`, `gap-closure-w5*.json`), `CROSS-REPO-STRANDED-AUDIT-2026-10-23.md`, `MERGE-QUEUE.md`. Teardown completion means: extracted + decrypted + decoded + assembled. Anything short of that is not "done", whatever a checkpoint says.

## Tekken 6 (PSP) — mhvnsnt/western-heart `teardown/tekken6/` + game-reverse-engineering

**What exists & where:** sector cipher fully reversed bit-exact (`tekken6/tools/sector_cipher.py`); ISO preserved byte-exact at game-reverse-engineering release `tekken6-psp-v1`; EBOOT decrypted; DATA401 DINF manifest re-verified (2,169 entries, data-region byte total 384,051,200); bulk region is NOT plaintext-compressed (entropy ~7.91) — the Tekken 5 LZSS surprise does not repeat.
**Verified state:** models/partial decode work landed via sweep-lane PRs #187/#388/#413/#446 (western-heart). **Motion/move extraction DOES-NOT-EXIST.**
**Blocker (concrete):** motion data is locked behind the DATA401 DEFLATE **encode-context crack** — 20/76 studied containers byte-exact, 56 await the encode context. The crack is owned by the live teardown-sweep lane (`teardown-sweep-tekken6-psp.json`, PPSSPP/Ghidra). The separate decrypt6 lane (`wh-tekken6-decrypt6.json`) has been parked `needs_owner` since 2026-10-16 with NO concrete decision ever recorded — per pipeline v2 this must be restated as a concrete decision or folded into the sweep lane. Do not spawn a parallel crack lane.
**Ownership:** teardown-sweep lane (crack) + T6 coordinator scope (LZSS spot-tests, motion-data ID once the crack lands).

## Tekken Tag Tournament 2 (Xbox 360) — western-heart release `ttt2-7z-v1`, tools on branch `feat/ttt2-teardown-100`

**What exists & where:** all 26 archive chunks verified on release `ttt2-7z-v1` (25×524,288,000B + 1×256,424,393B = 13,363,624,393B); Phase 1 streaming listing done (inner image: 78 files / 8,402,073,168 bytes; GoD stream is a bare XDVDFS game partition, descriptor at image sector 32). Tools: `god_surgical.py`, `xdvdfs_reader.py`, `stfs_blobs.py`, `ttt2_virtual_god.py`.
**Verified state:** Phase 2 per-fighter extraction is **ACTIVE** (checkpoint `ttt2-resume-100.json`, status running, heartbeat 2026-10-23). Reassembly is parked BY DESIGN behind the resume gate: disk <70% AND no other big download running AND single coordinated lane (`ttt2-resume-100` OR `wh-ttt2-100` — the latter is superseded; use resume-100).
**Note:** `teardown-sweep-ttt2.json` still says "blocked" — stale; `ttt2-resume-100` is the live checkpoint. Priority per owner: characters + moves first.
**Ownership:** TTT2 lane (`ttt2-resume-100`).

## WWF No Mercy (N64) — western-heart `teardown/` (wrong-window set)

**Verified state:** checkpoint `extract-nomercy.json` says "done" (2026-10-13) — **that claim is false in substance.** Per the wrong-window audit (western-heart PR #505), ALL No Mercy extractors share one FileTable with the wrong window (FT 0x16C3238 / FIRST 0x1BD1B0); **everything NM-derived on western-heart main is wrong-window**: the anim bank, model bank, texture bank, 17 arena assemblies, AKI→T3 v1+v2, ANIMATION-INDEX, MOVE-DATABASE NM entries. Correct window exists only in W3c v3 (western-heart PR #499, open) + CAW/name tables.
**Queued:** true-window re-extraction + per-character rewiring — **exists nowhere, never run as a program.** It is a MERGE-QUEUE item, not a cleanup task. The 13 No Mercy wrestler GLBs in wrestling-game PR #9 are a separate payload (extraction set) — land them in wrestling-game per HANDOFF-REPOS.md; do not confuse them with fixing the wrong-window banks.
**Ownership:** unassigned program — pick up via MERGE-QUEUE.md.

## Def Jam: Fight for NY (PS2) — wrestling-game PRs #14–#18; western-heart CATALOG pending

**Verified state:** teardown checkpoints `defjam-teardown.json` / `wh-defjam-100.json` = done; gap-closure W5 complete: motion census EXACT (423=423 / 3=3 / 329=329); **912/912 parts extracted** — but "stored" means **open-PR branches only**: wrestling-game #15 (42 files), #16 (217), #17 (653), on top of #14 (reconciliation). Microcode hunt EXHAUSTED — valid negative (#18: 3,065 files, 2,486 refs, 0 definitions). Disc originals CLEAN (2,624/2,624 parse); the 767 corrupt held copies are an old extraction artifact, replaceable from disc.
**Queued:** (1) land the W5 set in order #14 → #15 → #16 → #17 → #18; (2) **converter + CATALOG.json wiring into western-heart — NEVER RUN, exists nowhere**, gated on the W5 landing. Vertex/VU converter routes closed as spec addendums (checkpoints `gap-closure-w5c/w5d/w5e` = done).
**Ownership:** W5 landing = merge queue; converter/catalog wiring = unassigned, starts only after W5 lands.

## Street Fighter EX (GRE PRs #42–#45) — game-reverse-engineering

Fresh, active program (2026-10-23), all four phase PRs MERGEABLE/CI-blocked, none on main: #42 Phase 1 PAC loader contract + EX2 model decode + census (216 files); #43 Phase 2 EX1 geometry + EX2 textures + EX3 archive; #44 Phase 3 EX1 TMD assembly + EX3 .mdl contract; #45 Phase 4 animation decode + final state. **Land in phase order.**

## SoulCalibur II (GRE PRs #26–#40) — game-reverse-engineering

10 PRs, stacked branches (each phase carries the previous phases; phase-10 tip #40 is 144 commits ahead of main): #26 model hunt (stack base), #28 VMX format cracked, #30 fighter position stream, #31 rigid placement, #32 skinning SOLVED (22 GLBs, 24 movesets), #33 motion DB crack, #34 bank track layout, #36 composition, #37 template initializer, #40 composition candidates (tip). **Land in phase order, or verify the #40 tip carries the whole stack and land the tip.**

## Tekken 5 (GRE PRs #20–#25, #27) — game-reverse-engineering

7 lane PRs, all stranded mergeable: #20 DATA0/DATA1 cipher hunt, #21 Devil Within deep-dive, #22 production architecture docs, #23 roster ground truth + name tables, #24 IPU/TIM2/Ghidra-EE tool pull-in, #25 72-file archive catalogue + maps, #27 ISO complete (MD5 verified) + extraction status. (Separate known gap: DATA0 is the only unexamined place for the T5 skull-mask question.)

## Yu Yu Hakusho (GRE PRs #35, #39, #41) — game-reverse-engineering

#35 Dark Tournament census; #39 RESOURCE.PAK resource unpacker + Toguro teardown; #41 MDL→GLB (47-bone) + 4-PAK reconciliation. All stranded mergeable. Note for Western Heart: the YYH ANI encoding is cracked+proven in the WH gap-closure work (195 clips / 3,039 keys, handedness unverified in-engine) — that lives in the WH lane records, not these PRs.

## Cross-cutting

- W1 WWE All Stars census = GRE PR #38 (Rock animation data located); the ISO itself is stored byte-exact at western-heart release `wwe-all-stars-ps2-v1` with pull-back proven.
- GRE PR #10 (RE tooling pull-in, 905 files) carries **−2 deletions** — run the deletion guard before any merge.
- Every item above is in `MERGE-QUEUE.md` with its landing order. If a teardown's state here disagrees with a checkpoint, the repo wins and the checkpoint is stale — fix the checkpoint in your PR.

## INCIDENT 2026-10-24 ~05:20Z — GRE #58/#57 merges wiped off main by lane ref-rewrite

**What happened:** the overnight pipeline's 04:22-04:24Z merges (#58 WWE 2K19 batch1 → 79c068d5, #57 Yakuza Kiwami hact → c2a1c8c7) were verified LANDED-VERIFIED at 04:24Z, then dropped off main. Verified own-eyes 05:20Z: `teardown/wwe2k19` 404 on main (retried — not transient); `teardown/` on main = firepro, pakchunk0, tekken7-steam, tkdata, wrestling-empire only. Both merge commits exist but are NOT in main's ancestry (compare 79c068d5...HEAD = diverged, ahead 27 / behind 15). Main HEAD = b8abadd6 (03:49:18Z) — the ref moved BACKWARD over the 04:22-04:24Z merges.
**Cause:** the GRE teardown lane is rewriting main directly tonight (their teardown stack push is in flight — #59 was merged by the pipeline onto their stacking branch teardown/wwe2k19-b1 @2ae430ef 04:30:30Z). Same failure class as western-heart #499 (lane force-push dropped a landed merge).
**Nothing lost:** payloads survive on branches — teardown/wwe2k19-b1 @2ae430ef (union tree: gang-beasts 1605 + wwe2k19 1775 + yakuza 11809 paths); teardown/yakuza-kiwami-hact @79c068d5 (wwe2k19 batch1 + yakuza hact). REOPENED in MERGE-QUEUE.md. Pipeline stood down per CHECK-BEFORE-START — the lane owns the stack merge to main; an API merge now would be dropped again or collide.
**Rule for future runs:** on repos where a lane is force-pushing main, LANDED-VERIFIED requires re-checking the ref AFTER the lane's push window closes.
**Concrete owner question:** does the GRE teardown lane get to keep force-pushing main, or must it merge via PRs/API like everyone else?
**Also lane-owned in-flight:** GRE #55 "Yakuza Kiwami b1 (battle, boot, motion PARs)" — OPEN, mergeable=false/dirty, +828,709/-0, 19 commits. Same lane; stand down.
