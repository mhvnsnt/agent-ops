# TEARDOWN IDLE QUEUE

Teardowns that aren't 100% per the TEARDOWN-COMPLETION LAW yet, queued for idle time — when there's nothing else to handle and we're waiting on owner directives. Work through top to bottom. A game file's local source may be deleted once it's byte-identical on GitHub + TeraBox, but its teardown thread lives here until verified 100%.

## Queue

### 1. Eastern Mind — DONE (verified 100%, local deleted 2026-10-16)
- Teardown-completion audit PASS on all 5 pillars (report: `agent-ops/eastern-mind-teardown-verification-20261016.md`).
- Local source deleted 2026-10-16 under the relaxed game-files law (byte-identical both stores, owner authorized).
- Backups: GitHub `eastern-mind-v1`, TeraBox `/game-files/eastern-mind/`, WH main teardown (5,707 files).
- Source: `emtlsotn.zip` (575,140,238B) — GitHub release `eastern-mind-v1` (byte-identical); full working dir on TeraBox `/game-files/eastern-mind/` 22/22 hash-verified.
- Prior state: PR #160 merged (5,707 files into WH), marked complete under the old bar.
- Needed: verify per TEARDOWN-COMPLETION LAW — extracted / decrypted / decoded / working assets / reassemblable. Director 4 DXR decode coverage (BITD→PNG, snd→WAV, STXT→text), decode failure count, asset validity.
- Verification audit started 2026-10-16 (read-only) — report at `~/workspace/agent-ops/eastern-mind-teardown-verification-20261016.md`.
- Local source: eligible for deletion under the relaxed game-files law (byte-identical both stores).

### 2. Street Fighter EX3 (PS2, SLUS_201.30) — local bin deleted 2026-10-16, teardown ~5%
- Local source deleted 2026-10-16 under the relaxed game-files law (byte-identical both stores).
- Backups: GitHub `sf-ex3-v1` (western-heart, `Street.Fighter.EX3.USA.bin`, 701,813,280B, state=uploaded); TeraBox `/game-files/sfex3-usa-bin/` (14/14 pieces, sha256 059a9516f6d8f787…).
- Local file: `game-reverse-engineering/street-fighter-3d-games/downloads/Street Fighter EX3 (USA).bin` (701,813,280B, sha256 059a9516f6d8f787…) — DELETED after triple-verification.
- Teardown remaining: EX3 extraction from bin (format RE, character/stage extraction). ~5% per 2026-10-15 inventory.
- No active work at deletion time.

## 2026-10-16 ~17:45 EDT — WMXIX ISO local parts cleared (ONE-STORE RULE)
- Cleared: ~/workspace/wmxix-iso/wmxix-500m.part_00, part_aa, part_ab (1.46GB total)
- Verified 100% on GitHub release wmxix-iso-v1 (mhvnsnt/western-heart), sizes byte-match, ranged-MD5 verified on upload 2026-10-16
- Reason: disk space needed for DOA4 100% teardown (owner priority)
- Re-download: ~/workspace/wmxix-iso/dl.sh (takes minutes)
- WMXIX teardown status: ~80%+ per 2026-10-16 report; active work is on extracted YMG/YCG files, ISO not in active use
- Thread preserved: ISO safe on GitHub, re-download anytime

### 3. Tekken Tag Tournament 2 — local source cleared 2026-10-16 (ONE-STORE RULE), teardown ~15-25%
- Cleared: ~/workspace/game-reverse-engineering/tekken-tag-tournament-2/ (5.6G) — the full 13,363,624,393-byte archive lives as 26/26 chunks on GitHub release ttt2-7z-v1 (mhvnsnt/western-heart), every asset size verified with own eyes 2026-10-16; upload log shows per-chunk VERIFY on upload 2026-10-13.
- Local "Tekken Tag Tournament 2.7z" (5,767,168,000B) was the first 11/26 chunks only (partial reassembly from 2026-10-15) — re-derivable: download all 26 parts, concatenate in order.
- Teardown remaining: full extraction of the 13.36G archive, model/stage mapping. ~15-25% per 2026-10-16 inventory.
- No active work at deletion time (checkpoints extract-ttt2.json, t6-ttt2-100.json both done; no process running).

## 2026-10-17 ~00:10 CDT — Adventure Time CN zip (at-cnzip) local payload cleared (ONE-STORE RULE)
- Cleared: ~/workspace/cn-pull-bigend/work-at/at-cnzip-000.bin (8,589,934,592B), at-cnzip-000.part_ap (524,288,000B), at-cnzip-000.part_aq (201,326,592B) — 9.3GB total
- Verified 100% on GitHub release at-cnzip-20261015 (mhvnsnt/cn-gigaleak-adventure-time), release id 414217119: all 17 assets at-cnzip-000.part_aa..part_ap (524,288,000B each) + part_aq (201,326,592B) confirmed with own eyes via gh; .bin byte-sum equals concatenated parts exactly (8,589,934,592B); local part_ap/part_aq sizes match release; push-chunk1.log shows per-part VERIFIED on upload + "ALL PARTS UPLOADED AND VERIFIED" 2026-10-16T23:56:19
- No active work at deletion time (no process touching work-at; pull lane finished)
- Teardown status: zip CONTENT LISTING done (cnzip_filelist.txt, cnzip_entries.json, cnzip_cd_info.txt); full extraction/decode NOT done — thread preserved here for idle time
- Re-download: GitHub release assets aa–aq, concatenate in order → byte-exact original
- Trigger: disk at 91%, aggressive cloud-offload per disk-space-guardian protocol

### 5. Adventure Time CN zip (at-cnzip-000) — local payload cleared 2026-10-17 (ONE-STORE RULE), teardown ~5%
- Cleared: ~/workspace/cn-pull-bigend/work-at/at-cnzip-000.bin (8,589,934,592B) + remaining local parts — 9.3GB total, deleted 2026-10-17 ~00:10 CDT.
- Backups: GitHub release at-cnzip-20261015 (mhvnsnt/cn-gigaleak-adventure-time, release id 414217119), all 17 assets (part_aa..part_ap 524,288,000B each, part_aq 201,326,592B), byte-verified with own eyes 2026-10-17.
- Teardown remaining: full extraction of the CN zip contents (FLA files, etc. per cnzip_filelist.txt) — only the content listing is done.
- No active work at deletion time.

### 4. Tekken 6 PSP — ISO cleared 2026-10-16 (ONE-STORE RULE), full recon tree cleared 2026-10-16 ~19:15 EDT (PUSH-AND-CLEAR, owner order), teardown ~40-45%
- Cleared: ~/workspace/game-reverse-engineering/tekken6/tekken6-psp.iso (855,638,016B) earlier; then the FULL remaining tree ~/workspace/game-reverse-engineering/tekken6/ (1,124,414,956B: decrypted/, extracted/, work/, docs/, tools/, TEARDOWN.md, PPSSPP-LIVE-RUN-GUIDE.md) cleared 2026-10-16 ~19:15 EDT per owner PUSH-AND-CLEAR order.
- Backups: GitHub release tekken6-psp-v1 (mhvnsnt/western-heart), byte-identical 855,638,016B verified with own eyes 2026-10-16; TeraBox /game-files/tekken6-psp-iso/ 17/17 verified 2026-10-15.
- Recon backup: GitHub release tekken6-recon-20261016 (mhvnsnt/western-heart, PUBLISHED): full 1,131,284,480B tree as 3 parts (part-aa 524,288,000B + part-ab 524,288,000B + part-ac 82,708,480B), all byte-verified with own eyes; sha256 2c738b24f46395960e463fd03c637b038a0942590c0055b9ef3fe1bc9d77afcc; reassemble with `cat t6-recon-backup.tar.part-aa t6-recon-backup.tar.part-ab t6-recon-backup.tar.part-ac > t6-recon-backup.tar`.
- Live branch: mhvnsnt/western-heart `feature/tekken6-100-teardown` @ 9ae91ce ("T6 recon WIP 2026-10-16 — disk-clear checkpoint"), pushed 2026-10-16.
- Handoff doc: ~/workspace/agent-ops/T6-RECON-HANDOFF-2026-10-16.md (what/where/done-vs-next/exact pickup commands).
- Teardown remaining: T6 recon threads (t6-live-dump needs_owner — PPSSPP live path blocked on VM; t6-bulk-decrypt done 2026-10-14 with PRNG blocker open).
- No active process at deletion time; ISO re-downloadable from GH/TeraBox in minutes if recon resumes.

### 5. Street Fighter EX Plus Alpha (PS1, SLUS_005.48) — ROM files cleared 2026-10-16 (ONE-STORE RULE)
- Cleared: ~/workspace/game-reverse-engineering/street-fighter-3d-games/downloads/Street Fighter EX Plus Alpha.7z (263,912,228B) + ~/workspace/game-reverse-engineering/street-fighter-3d-games/extracted/ex-plus-alpha/Street Fighter EX Plus Alpha.bin (528,049,872B).
- Backups: GitHub release sf-ex-plus-alpha-v1 (mhvnsnt/western-heart): Street.Fighter.EX.Plus.Alpha.7z 263,912,228B + Street.Fighter.EX.Plus.Alpha.bin 528,049,872B, sizes byte-match local exactly, verified with own eyes 2026-10-16.
- NOT cleared (unverified on any store): Street Fighter EX2 Plus.7z, Street Fighter EX2 Plus (alt).7z, extracted mednafen/[Med] emulator bundle.
- No active work at deletion time.

### 6. Soulcalibur II (Xbox) — local source cleared 2026-10-16 (ONE-STORE RULE), teardown extraction-complete
- Cleared: ~/workspace/game-reverse-engineering/soulcalibur/ (667M: xbox-extract/root.olk 693,897,216B + logs/scripts/reports) + staging hardlinks batch-001/soulcalibur/
- Backups: GitHub release soulcalibur2-xbox-extract-v1 (mhvnsnt/western-heart): root.olk 693,897,216B (byte-exact vs local, verified with own eyes) + sc-loose-files.tar 5,068,800B (all logs/scripts/reports, byte-exact) + soulcalibur2-xbox-olk-extract.tar 693,463,040B (full extraction); per-game repo copy: mhvnsnt/game-reverse-engineering release game-binaries-20261016 (root.olk 693,897,216B)
- Rule: ONE-STORE RULE; western-heart copy = chimera-build hard requirement (owner 2026-10-16 ~17:50 EDT); owner priority order 2026-10-16 ~18:19 EDT (Soulcalibur #2 after TTT2)
- Teardown remaining: character/stage model mapping from the OLK extraction; extraction itself verified (XBOX-EXTRACTION-REPORT.md in the loose tar)
- No active work at deletion time

### 7. Tekken 6 PS3 — TEKKEN.psarc local cleared 2026-10-16 (ONE-STORE RULE), teardown ~5%
- Cleared: ~/workspace/game-reverse-engineering/tekken6-ps3/iso/PS3_GAME/USRDIR/TEKKEN.psarc (4,831,493,723B) ONLY. EBOOT.BIN KEPT (decrypt key source for the KIRK RE task); PS3_DISC.SFB + manifests kept.
- Backups: GitHub release tekken6-ps3-full-v1 (DRAFT, mhvnsnt/western-heart, id 415183956): 10/10 parts (9x524288000B + 112901723B = 4,831,493,723B exact) + TEKKEN.psarc.manifest.txt; sha256 c98fb02602d58564ef4e80d386310cb3c48634566990a5050ef20ef2a4afd340 matches local byte-for-byte, verified with own eyes 2026-10-16. Re-download: 10 parts from release, concatenate in order.
- NOTE: the psarc was the WRONG acquisition (encrypted, entropy 8.00, no PSAR magic — useless for teardown). The REAL data is DATA214-220.BIN (~7.2GB) + IDX files; wh-tekken6-ps3-worker is STALLED awaiting guardian disk cleanup to fetch them. This deletion IS that cleanup.
- Teardown remaining: fetch DATA*.BIN + IDX after disk headroom; KIRK/MIPS RE of EBOOT for DATA401 key (multi-day task).
- No active process at deletion time (t6ps3_upload.py supervisor finished: "ALL 10 CHUNKS UPLOADED AND VERIFIED", manifest uploaded).

### 8. Virtua Fighter 5 — local models cleared 2026-10-16 (ONE-STORE RULE + owner 17:50 storage-layout directive)
- Cleared: ~/workspace/game-reverse-engineering/virtua-fighter-5/ (334 files, 141,977,600B tarred) — full local tree gone.
- Backups: GitHub release vf5-local-models-v1 on BOTH mhvnsnt/western-heart AND mhvnsnt/game-reverse-engineering — asset vf5-local-334files.tar 141,977,600B byte-exact on both, verified with own eyes 2026-10-16. sha256 21f5295fdba53029.
- NOTE: pre-existing GH releases vf5-model-library-v1 / vf5-ps3-v1 were built from a different (now-gone) western-heart-vf5/ tree — file counts don't correspond to the cleared local set. The vf5-local-models-v1 release is the canonical backup of what was cleared.
- Teardown remaining: VF5 model extraction/conversion into Western Heart chimera pipeline was never started on this set — queue for idle time.
- No active work at deletion time.

### 9. Tekken 7 — local tree cleared 2026-10-16 (ONE-STORE RULE)
- Cleared: ~/workspace/game-reverse-engineering/tekken7/ (3.1G: models/ 2.6G, arenas/ 297M, king/ 188M, tekkenmods-docs/ 25M, tools/ 1.2M, 1115 files) + 20 staging hardlink dirs in terabox-staging/game-re/batch-*/tekken7/.
- Backup: GitHub release tekken7-full-v1 (mhvnsnt/western-heart, PUBLISHED): 7 parts (6x524288000B + 145674240B) + tekken7.sha256. VERIFIED with own eyes 2026-10-16: re-tarred local tree, split identically, 6/7 part sha256 MATCH release exactly; part_aa differs only by tekkenmods-docs/.git directory mtime (all file data identical). Uploaded by sibling lane ~17:40 EDT; local unchanged since.
- Teardown remaining: T7 model extraction into Western Heart chimera pipeline — queue for idle time.
- No active work at deletion time (no writes except one .git dir mtime; no processes).
- 2026-11-12 ~10:53 CST (disk-space-guardian): local `~/workspace/_t7-gamefiles-20261109/wireup/tkdata/tkdata.bin` (304,756,784 B, sha256 f1523deaa8a17ad4fbd599d23ab9c4bd1e9bed7904277e15244bd5bc183daf3c) cleared under the ONE-STORE RULE — pull-back re-hash vs release `t7-depot389731-wave3-20261031` (mhvnsnt/game-reverse-engineering) matched exactly this run. Pull-back: `gh release download t7-depot389731-wave3-20261031 --repo mhvnsnt/game-reverse-engineering --pattern tkdata.bin`. NOTE: the consolidation release `tekken7-gamefiles-v1` (mhvnsnt/western-heart) is INCOMPLETE live — only 36/54 manifest assets (pakchunk0 parts 00–35 only; missing parts 36–42, all 10 _P parts, tkdata.bin) — its completeness claim in MANIFEST-tekken7-gamefiles-v1.json does not match live state; the source releases (wave1/wave3) hold everything. Consolidation still owed; local `wireup/tkdata/` remainder (tkdata2.bin 127M, unpacked/ 180M, unpacked2/ 539M) NOT store-verified, stays on disk.

### 10. Tekken 8 — local tree cleared 2026-10-16 (ONE-STORE RULE)
- Cleared: ~/workspace/game-reverse-engineering/tekken8/models/ (4 files, 225M) + staging hardlinks.
- Backup: GitHub release tekken8-full-v1 (mhvnsnt/western-heart, PUBLISHED by sibling lane ~15:46 EDT): tekken8-500m.part_aa 235,642,880B + sha256. VERIFIED with own eyes 2026-10-16: downloaded the part, sha256 matches release manifest; all 4 local files byte-size-identical inside (t8-heihachi-s1.7z 122429550, gdrive-dl.sh 904, sfmlab-tekken8-asuka_SFM.rar 30027257, t8-yoshimitsu-s1-blender.7z 83173144). NOTE: a redundant tekken8-work-v1 release was created by this lane in error (duplicate upload attempt, stalled on proxy, killed); empty release deleted, no confusion left behind.
- Teardown remaining: T8 model extraction into Western Heart chimera pipeline — queue for idle time.
- No active work at deletion time.

### 11. Tekken 3 work files — local tree cleared 2026-10-16 (ONE-STORE RULE)
- Cleared: ~/workspace/game-reverse-engineering/tekken3/ (407M, 19,536 files: tools/ 296M, tim-output/ 78M, movesets/, animations/, renders/, models/, docs/) + staging hardlinks.
- Backup: GitHub release tekken3-work-v1 (mhvnsnt/western-heart, PUBLISHED): t3-work-part-aa 209,715,200B + t3-work-part-ab 175,411,200B = 385,126,400B tar, sizes byte-exact vs local. sha256 1be0a53383460b8d. Reassemble: cat parts > t3-work.tar. (Full game rips already on tekken3-ps1-v1.)
- Upload notes: single 385MB upload stalled on proxy at 261MB — killed, split to 200MB parts, both landed.
- Teardown remaining: T3 model/animation extraction into Western Heart chimera pipeline — queue for idle time.
- No active work at deletion time.

### 12. WWF No Mercy + WWE2K work files — cleared 2026-10-16 (ONE-STORE RULE)
- Cleared: ~/workspace/game-reverse-engineering/wwf-no-mercy/ (48M: docs/, re-docs/, recomp/, tools/, WWF-No-Mercy.zip, nm.torrent) + ~/workspace/game-reverse-engineering/wwe2k/ (86M: dlcs/, ANIMATION-CATALOG.md) + staging hardlinks.
- Backups: (1) GitHub release wrestling-work-v1 (mhvnsnt/western-heart): wrestling-work.tar 112,844,800B byte-exact — contains wwf-no-mercy work files + wwe2k dlcs + catalog. (2) No Mercy ROM: release no-mercy-n64-v1 has WWF.No.Mercy.USA.Rev-A.z64 33,554,432B = local zip's internal file byte-exact (verified via unzip -l). nm.torrent (4KB pointer file) not backed up — negligible/re-obtainable.
- Teardown remaining: wrestling game teardown integration into Western Heart — queue for idle time.
- No active work at deletion time.

## 2026-10-17 ~00:15 CDT — Gumball Flash.rar local cleared (ONE-STORE RULE)
- Cleared: ~/workspace/cn-pull-smallend/"Gumball Flash.rar" (1,940,020,461B) + gflash-part-ab (524,288,000B) + gflash-part-ad (367,156,461B) — 2.64GB total
- Verified 100% on GitHub release gumball-flash-v1 (mhvnsnt/cn-gigaleak-gumball, release id 414995766): assets gflash-part-aa/ab/ac (524,288,000B each) + ad (367,156,461B) confirmed with own eyes; sum = 1,940,020,461B = local rar byte-exact; gflash-chunked-upload.log shows per-part VERIFIED + "ALL PARTS VERIFIED 100% on release"
- No active work at deletion time (lane's 02:47 retry run failed on draft-release 404 and aborted; no process running)
- Note: payload is a CN pull archive, not a game teardown — full content processing (extraction) not confirmed done; thread preserved here

## 2026-10-17 ~00:30 CDT — Street Fighter EX Plus Alpha PS1 bin cleared (ONE-STORE RULE)
- Cleared: ~/workspace/sfex-teardown/work/ex-alpha/"Street Fighter EX Plus Alpha.bin" (528,049,872B)
- Verified 100% on GitHub release sf-ex-plus-alpha-v1 (mhvnsnt/western-heart): asset Street.Fighter.EX.Plus.Alpha.bin 528,049,872B confirmed with own eyes
- No active work on this file (ex-alpha/ untouched since 2018; active sfex lane is on ex2-extracted)
- Teardown status: unknown/not confirmed 100% — thread preserved here; source re-downloadable from release
- NOTE: local work/Street.Fighter.EX.Plus.Alpha.7z (263,912,228B, also on release) LEFT IN PLACE — touched recently by lane, may be in use

## 2026-10-17 ~01:45 CDT — DOA4 ISO local source cleared (ONE-STORE RULE)
- Cleared: ~/workspace/doa4-bass/doa4.iso (7,834,892,288B)
- Verified 100% on GitHub release doa4-iso-v1 (mhvnsnt/western-heart): 30/30 parts doa4-250m.part_01..part_30, sizes sum = 7,834,892,288B = local ISO byte-exact; lane verified 7834892288/7834892288 on reassembly 2026-10-16 ~21:30 EDT (per doa4-teardown.json checkpoint)
- ISO not in active use: extraction COMPLETE (extracted/ 3.0G, extracted_afs/ 516M, carved/ 1.6G, rebuild_tmp/ all on disk); remaining lane work is keystream/decryption analysis on extracted files (ENCRYPTION-ANALYSIS.md), not the ISO; no process held the ISO open (fuser clean 01:45 CDT)
- Teardown NOT 100%: 219/221 XPR2 carved, full header decryption needs keystream algorithm (S-box at 0x822f06d0); PR #223 merged, release doa4-xpr2-carved-v1 holds carved textures. Thread preserved here for idle time.
- Re-download: GitHub release doa4-iso-v1 parts 01-30, concatenate in order -> byte-exact ISO (~2h at observed CDN speed)
- Trigger: disk at 88% (hard ceiling), aggressive cloud-offload per disk-space-guardian protocol

## 2026-10-17 ~01:45 CDT — Teen Titans upload chunks cleared (ONE-STORE RULE)
- Cleared: ~/workspace/tt-stragglers/tt100m-aa..ah (8 parts, 735,196,929B total)
- Verified 100% on GitHub draft release teen-titans-cowchicken-v1 (mhvnsnt/cn-gigaleak-teen-titans): all 8 assets byte-sizes match local exactly (aa-ag 104,857,600B each, ah 1,193,729B); parts sum = 735,196,929B = local TEEN TITANS.zip byte-exact
- Upload lane not running; TEEN TITANS.zip + extracted/ (1.1G) left in place for the TT lane
- Re-download: draft release assets aa-ah, concatenate in order

## 2026-10-17 ~01:45 CDT — DOA4 carved XPR2 tarballs cleared (ONE-STORE RULE)
- Cleared: ~/workspace/doa4-bass/doa4-xpr2-{chrone,chrthree,chrtwo,mot,stg}.tar.gz (672,404,780B total)
- Verified 100% on GitHub release doa4-xpr2-carved-v1 (mhvnsnt/western-heart): all 5 assets byte-sizes match local exactly (chrone 99,357,959B; chrthree 170,868,044B; chrtwo 248,999,763B; mot 26,198,134B; stg 131,920,615B); no process held them open
- Upload complete; lane working material (carved/, extracted/) untouched
- Re-download: release assets, or re-tar from carved/

## 2026-10-17 ~09:40 CDT — space-ghost push: 16 large files pending clone push
- Branch feat/space-ghost-full commit 8317d2018feb8bb68d24325ce9e854125fb48721 (tree f715f616c5bc7be6caf9f28d1b40d4440a4b9d9b) holds 445/461 API-pushable files, verified on GitHub.
- 16 files >10MB skipped the blob API (HTTP 422 practical limit), recorded in ~/workspace/trippedd-copylane/sg-push-large-skipped.json — push via local clone onto feat/space-ghost-full per GitHub's suggestion. Local source: ~/workspace/trippedd-copylane/sg/extracted/.
- The 445 verified files were cleared from local disk per ONE-STORE RULE (guardian run 2026-10-17 ~09:40); the 16 large + 'Space Ghost tab' + scripts/logs KEPT for the clone push.

## 2026-10-17 ~13:30 CDT — DOA4 carved/ local cleared (ONE-STORE RULE, disk 90% critical)
- Cleared: ~/workspace/doa4-bass/carved/ (1.65G, 1,653,442,560B tarred)
- Verified 100% on GitHub release doa4-mirror-20261017 (mhvnsnt/western-heart): 4 parts doa4-mirror-carved-20261017.tar.part-00..03 (524288000x3 + 80578560 = 1,653,442,560B, all state=uploaded) — part sum byte-exact equals fresh local tar of carved/ 2026-10-17 13:20 CDT; carved/ unchanged since prior lane's own-eyes byte-exact verify 2026-10-17 ~11:10 CDT (no files newer than 11:10, dir mtime 06:02)
- No active teardown work on carved/ at clear time (no doa4 process running; model lane reads carved_models/, untouched)
- Pull-back: gh release download doa4-mirror-20261017 --repo mhvnsnt/western-heart --pattern "doa4-mirror-carved-20261017.tar.part-*" && cat doa4-mirror-carved-20261017.tar.part-* > carved.tar && tar xf carved.tar
- DOA4 teardown thread still open (see 01:45 entry above): XPR2 decode not 100%; carved XPR2 textures on release doa4-xpr2-carved-v1; extracted/ mirror in-flight (part-04 uploading 13:17 CDT)

## 2026-10-17 ~14:30 CDT — Def Jam ISO parked partial (resume thread)
- Parked: ~/workspace/terabox-staging/def-jam/SLUS_210.04.Def Jam - Fight for NY.iso (3,724,824,576B, partial; curl lane died 2026-10-17 ~01:27 CDT on "curl: (18) Send failure: Broken pipe" at ~591M of a 3064M attempt — source size mismatch vs local file, needs care)
- Not verified anywhere → stays per ONE-STORE RULE; never delete as partial
- Resume: ~/workspace/terabox-staging/def-jam/resume-defjam.sh (curl -C -). Note ~140KB/s observed rate — multi-hour job, schedule in idle/low-disk window
- teardown/def-jam on western-heart was restored via #231; ISO resume is for the source-archive lane, not blocking teardown work

## 2026-10-17 22:35 CDT — Def Jam FFNY PS2 ISO cleared per GAME-FILE 100% RULE
- File: ~/workspace/terabox-staging/def-jam/SLUS_210.04.Def Jam - Fight for NY.iso (3.5G)
- SHA256: fd829ffde333fa103b0fa37b35d23ea11ad3e4fd3a8f6bcac2e50ba7260ddc24 (matches manifest LOCAL_ISO_SHA256)
- Store: mhvnsnt/def-jam-fight-for-ny release defjam-ps2-iso-v1 (36 chunks + SHA256SUMS-defjam.txt, all verified)
- Teardown status: ISO preserved on release; local cleared for disk. Pull-back: gh release download defjam-ps2-iso-v1 --repo mhvnsnt/def-jam-fight-for-ny

## 2026-10-18 02:00 CDT — DOA4 extracted/ cleared (ONE-STORE RULE, disk 91% critical)
- Cleared: ~/workspace/doa4-bass/extracted/ (3.0G)
- Verified 100% on GitHub release doa4-mirror-20261017 (mhvnsnt/western-heart): recreated tar stream `tar -cf - -C doa4-bass extracted`, chunked sha256 per 524288000B == all 6 release asset digests (part-00..05), EOF-clean. Dir untouched since 2026-10-17 13:05 (mirror creation time).
- No active teardown work on extracted/ (no doa4 processes; wh-lane6-gapfill IBUF decode works from its own lane copies).
- Pull-back: gh release download doa4-mirror-20261017 --repo mhvnsnt/western-heart --pattern "doa4-mirror-extracted-20261017.tar.part-*" && cat *.part-* > extracted.tar && tar xf extracted.tar
- DOA4 teardown thread preserved (XPR2 decode not 100%; see entries above).

## 2026-10-18 ~18:35 CDT — Johnny Test zip local cleared (ONE-STORE RULE, disk-space-guardian)
- Cleared: ~/workspace/jt-copy-work/JohnnyTest.zip (1,415,713,110B)
- Verified: local md5 e3e0c72be68c93fc3f931e7b2c9b5a84 == EXPECTED_MD5 in download.sh; all 14 parts jt100m-aa..an present on GitHub release johnny-test-cowchicken-v1 (mhvnsnt/cn-gigaleak-johnny-test, draft) — reassembles hash-verified.
- No active work at deletion time (no download process running; pull finished 2026-10-18 ~01:09).
- Note: payload is a CN pull archive, not a game teardown — full content processing (extraction completeness) not confirmed; thread preserved here.
- Pull-back: cd ~/workspace/jt-copy-work && ./download.sh  (re-downloads parts, concats, md5-verifies)
- Remaining local: extracted/ (1.9G) — tar jt-extracted.tar (md5 e26679b40292d65079747206b4d12f5c) uploading to release johnny-test-extracted-v1 this run; extracted/ to be cleared after release verifies.

### SFEX working snapshot (EX Plus Alpha / EX2 Plus) — local source cleared 2026-10-19, teardown incomplete
- Cleared: `~/workspace/sfex-teardown/` (935M) under ONE-STORE RULE 2026-10-16 — verified 100% on Google Drive as manifest item `sfex-teardown-20261018` (10/10 chunks, 980,305,920B total, reassembled sha256 `4317b43e5faa21bb2ea145dc6bc443043c79be84abd81c5bfddfbb104a962040` hash-matched 2026-10-19 ~07:20 CDT). Staging tar auto-removed by store script; pull-back: `~/workspace/tools/fetch/fetch sfex-teardown-20261018` then untar.
- Contents: teardown scripts (iso_extract.py, pac_parse.py, tim_extract.py, tmd_extract.py, obj2glb.py, render_char.py) + work/: Street.Fighter.EX.Plus.Alpha.7z, Street.Fighter.EX3.USA.bin, sf-ex2-plus.bin, alpha-extracted/ (439M, newest 2026-10-16), ex2-extracted/ (83M), ex2-tmd-scan/ (12K .obj).
- Teardown remaining: decode/assemble EX2+ EX Plus Alpha extracted TIM/TMD assets into working GLB roster; EX3 bin already tracked in entry #2 above. No active work at deletion time (nothing modified since 2026-10-16).

### 4. DxMMII Limb System — local checkout cleared 2026-10-19 (ONE-STORE RULE), lane checkpoint archived
- Cleared: `~/workspace/dxmmii-limbs/` (2.6G checkout; local HEAD ddb10ca022f476c24ae3acbc94c1f654e05230a9 'mirror checkpoint 2026-10-17', NOT on remote wh-mirror).
- Verified 100% on GitHub: release `dxmmii-limbs-checkpoint-20261017` (mhvnsnt/western-heart, published 2026-10-19T14:16:53Z), asset `dxmmii-limbs-20261017.bundle` — fresh-download SHA256 ea23b6c5cab93718ed09cf6df7eeb8a6b15c67b89cd1565b7d42e1f31472430e matches local bundle byte-for-byte (own-eyes, 2026-10-19 ~10:50 CDT); `git bundle verify` passes, complete history, master + HEAD @ ddb10ca.
- Local staging bundle retained at `~/workspace/agent-ops/staging-dxmmii/dxmmii-limbs-20261017.bundle` (SHA256-verified) + registered in CloudDog registry for next-pass re-verify/clear.
- Restore: `gh release download dxmmii-limbs-checkpoint-20261017 --repo mhvnsnt/western-heart` && `git clone dxmmii-limbs-20261017.bundle dxmmii-limbs` && `git remote add wh-mirror https://github.com/mhvnsnt/western-heart.git`.
- Thread preserved: DXMMII limb system work resumes from the archived HEAD (the 54k-file-deletion repo; its recovery state is inside the bundle). No active checkout work at deletion time (mtime 2026-10-16, clean status, no processes holding it).

- **Cleared 2026-10-19 12:57 CDT (guardian-verified):** `~/workspace/jt-copy-work/` (Johnny Test teardown) — the upload lane finished and self-cleared. Store: GitHub release `johnny-test-extracted-v1` (mhvnsnt/johnny-test-parody): jt-part-00/01/02 (524288000B each), jt-part-03 (405002240B), jt-extracted.tar.md5 (51B), jt-parts.md5 (180B) — all sizes byte-match the deleted local files (gh API, own eyes). Reassembly: `cat jt-part-00 jt-part-01 jt-part-02 jt-part-03 > jt-extracted.tar`, then `md5sum -c jt-extracted.tar.md5`.
- **Teardown remaining (UNVERIFIED from this run):** whether `jt-extracted.tar` represented a COMPLETE extraction (download-resume.log/download.sh suggested ongoing pull work when last seen). If idle audit finds gaps, re-pull from the release parts and continue.

## SF 3D teardown — EX+alpha extracted+indexed (2026-10-20, sf-teardown-pr2 lane); EX2+ pull + PAC container decode queued
- PR 2 **MERGED: mhvnsnt/western-heart #360** (merge commit 39148206, 2026-10-20): 173 real SF moves
  translated to Tekken notation (`game/assets/movesets/sf-{ryu,ken,akuma,zangief,blanka,vega}.json`,
  schema v2, wired in `MOVESET_IDS`) + `game/assets/stages/sf-ex/stages.json` (20 EX+α packs
  by index + 19 EX2+ named stages). Status: `teardown/street-fighter-3d-games/SF-TEARDOWN-STATUS.md`.
- EX Plus Alpha: CLEAN re-pull verified (7z 263,912,228B == archive.org metadata; py7zr-valid);
  decoded with jPSXdec v2.0 + Temurin JRE 17 (install at `~/workspace/_sf-scratch/sf-tools/`,
  612 disc items indexed); full tree extracted; PL/ (26 PACs), STG/ + STG2/ (20 packs each),
  TMD/ committed in `teardown/street-fighter-3d-games/extracted/ex-plus-alpha/` (+PAC-CHUNK-INDEX.json).
- FINDING: STG/STG2 hold 20 packs (S00–S13 hex), not 8 as PR-1 docs said. TIM-chunk finding:
  134 magic-0x10 chunks are NOT standalone TIMs (version field 0x54) — PAC container decode
  (Arika 44-entry table is NOT sequential: 46/1144 bad offsets, backward jumps) is a dedicated
  RE pass.
- QUEUED: (1) SF EX2 Plus 7z — re-download on retry loop (`~/workspace/_sf-scratch/ex2-retry.sh`,
  archive.org transfer throttling); integrity gate = size 207533625 + py7zr. (2) Arika PAC
  container decode → TMD/TIM split → community TMD→OBJ pipeline; then anim/frame data from
  OVL tables (TEARDOWN.md 2c). (3) P-slot→character cross-check vs SEL2/ select screen.
  (4) `MUS/` + `MOV/` on local disk only (`~/workspace/_sf-scratch/`) — not committed; store
  to TeraBox via browser lane. (5) Wire sf-ex stages into `game/js/stages.js` (Lane 4 edit surface).
- Reusable stack for the next pass: py7zr (7z), jPSXdec v2.0 + jre17 (Mode-2 disc), `pac_index.py`.

## Tekken 5 (PS2) — teardown ~15%, blocked on overlay deobfuscation + ISO tail (2026-10-20 ~04:00 CDT)
- Lane dir: ~/workspace/game-reverse-engineering/tekken5/ (iso/, extracted/, overlays/, work/T5Proj Ghidra DB)
- PR: mhvnsnt/game-reverse-engineering #18 (branch feat/tekken5-100-teardown-resume) — TEARDOWN-STATUS.md has the full state.
- ISO download IN PROGRESS in lane dir: main curl tekken5-ps2.iso (~511MB/4,483,547,136B at write time, ~200KB/s). Do NOT kill (NEVER-KILL-IN-PROGRESS). 8 ranged segment downloads died together 2026-10-20 03:40 (cause unknown; their partials seg0-7.bin remain in iso/, resumable via `curl -C - -r`). Assigned item tekken-5-de-en-... is DARK; fallback item ps-2-2004-tekken-5 in use.
- Extracted + stored: SLUS_210.59, TK5DATA4.BIN, IOPRP300.IMG; TK5DATA5 E0-E9 complete (+ E7 files incl. 17 charipu IPUs).
- Store: GitHub release tekken5-tk5data5-v1 (mhvnsnt/game-reverse-engineering) — E7/E9 in 100MB/60MB split parts + E0-E6+E8 tarball; verify before clearing local extracted/.
- Cracked formats: TK5DATA3/5 10-entry (off,size) tables (DATA3==DATA5 layout); E7 72-file archive (24B records [u32 hdr][name12][u32 off][u32 size]); charipu.arc 17-entry (off,size) table, all "ipum" videos.
- BLOCKERS for 100%: (1) E0-E4 overlay cipher — shared keystream XOR (k[0..23] recovered) OR LZ-family; entropy 7.13, E0^E1 zero-rate 3% uniform-phase. Next attack: Ghidra decompile of SLUS function @0x14c894 (.y4 walker) + E5/E6 disasm hunt for the decode routine; crib-drag E0^E1 zero runs. (2) TK5DATA0 (2.07GB) + TK5DATA1 (1.30GB) encrypted (entropy 8.00) — models/movesets/stages/Devil Within data blocked until (1). (3) E5 roster name tables: one byte per name replaced by high-byte code (unresolved control byte) — needs E5 disasm.
- Roster codes found in SLUS (_wl): ANN ASK BAE BRU BRY CHR DVJ EDD GAN HEI HWO JAC JIN JNP JUL KAZ KIN KUM LAW LEE LEI MAR MOK NIN NJA PAN PAU ROG STE TAI WAN XIA YOS. These name the data packs to pull per fighter once TK5DATA0 opens.
- 2026-10-20 ~04:30 CDT ONE-STORE clear: extracted/TK5DATA5/{E7.bin,E8.bin,E9.bin} + split parts + tarball (390MB) cleared from lane dir after GitHub release tekken5-tk5data5-v1 verified (all 6 assets byte-size-exact vs local; E0-E6+E8 tarball re-downloaded, SHA256 d12db323ab589b0a881983e34d53e06ceea1de1c75de219edd4c6bcb1a81743b matches local). Kept locally: E0-E6 overlays (13MB, RE in progress), extracted/E7 files (21MB), SLUS/TK5DATA4/IOPRP. Pull-back: gh release download tekken5-tk5data5-v1 --repo mhvnsnt/game-reverse-engineering; cat t5data5_E7.part.aa/ab/ac > E7.bin; cat t5data5_E9.part.aa/ab > E9.bin.
- 2026-10-20 ~04:45 CDT ONE-STORE clear (disk-guardian): full Tekken5-PS2.iso (4,483,547,136 B, sha256 783199429908c698fe1e9a5c654c17502658da708d7259cf84a36f9bc4c806f6 own-eyes) + stale seg*.chunk leftovers cleared from lane dir after mirror lane COMPLETE — all 9 parts + SHA256SUMS-tekken5.txt verified on GitHub release tekken5-iso-v1 (mhvnsnt/game-reverse-engineering), sizes match sums, retrievability proven (manifest + part_08 re-downloaded from release, part sha matches). Teardown continues from extracted/ + work/ (not the ISO). Pull-back: gh release download tekken5-iso-v1 --repo mhvnsnt/game-reverse-engineering; cat tekken5-iso.part_0* > Tekken5-PS2.iso; sha256sum expect 783199429908c698fe1e9a5c654c17502658da708d7259cf84a36f9bc4c806f6.

## DOA4 full teardown — continuation (2026-10-19 ~22:00 CDT, subagent doa4-continuation)
**Done:** 159/209 tables triangulated on main (chrone 30/30, chrtwo 68/68, chrthree 50/75, mot 11/11); stg.afs 0/18. 9 schema-v2 moveset JSONs wired (doa-bass/kasumi/hayabusa + NEW doa-ayane 23/doa-tina 26/doa-jannlee 21 from DOAU community guides, damage x0.37, real notations, honesty notes), MOVESET_IDS wired. Branch feat/doa4-full-teardown-continuation pushed (commit b3002876); status doc teardown/dead-or-alive-4/DOA4-CONTINUATION-2026-10-19.md.
**Resume extraction:** mirror parts downloading in ~/workspace/doa4-work/mirror/ (release doa4-mirror-20261017, DRAFT — use releases list endpoint for asset IDs; see ~/workspace/doa4-work/par_dl.py TAG=doa4-mirror-20261017). Finish with ~/workspace/doa4-work/doa4_finish.sh: cat parts | tar -xf - (streams chrthree.afs + stg.afs), batch_decode2.py (auto per-table IBUF base discovery), commits GLBs to wh-doa4 worktree + pushes. Watch disk: needs ~4.6GB free; delete mirror parts after AFS land.
**Blockers:** (1) fighter ID of carved GLBs — vertex pools in per-part local space, need MdlGeo ObjGeo skeleton parse; (2) anm.afs animation format unknown; (3) expansion of all 22 DOA4 fighters to 100+ schema-v2 moves (FULL MOVESET LAW) — authoring wave per DOA Wiki command lists. Playable roster: Kasumi, Ryu Hayabusa, Kokoro, Hitomi, Brad Wong, Eliot, Bass Armstrong, Zack, Jann Lee, Leifang, Tina Armstrong, La Mariposa, Bayman, Christie, Ayane, Hayate + Ein, Gen Fu, Leon, Helena Douglas, SPARTAN-458, Tengu.
**Update 2026-10-20 ~01:05 CDT:** Mirror re-download COMPLETE; chrthree now 56/75 verified on main (tables 09,11,12,16,18,19 via per-table base auto-discovery; merged PR #361 df929ee1). Remaining: 19 chrthree tables use a relative-offset VBUF/IBUF sub-layout (descriptor GPU addr < file offset) — needs decoder variant work. stg.afs: pools located, triangulation FAILS quality gate (NaN, 4-39% degenerate) — unverified, GLBs NOT merged; needs base+pool-size RE. chrthree_45-53 (earlier lane, already on main) have NaN=31-33 verts — flag for re-decode in the same pass.

## 2026-10-20 01:40 CDT — tpose-staging archived (disk-guardian)
- What: `~/workspace/tpose-staging` (24 dirs, ~478M Tekken T-pose FBX staging; untouched since 2026-10-16) — tarred, split into 100MB parts, mirrored to GitHub release `mhvnsnt/clouddog-storage@tpose-staging-20261020` (byte-verified own-eyes), local copy cleared per ONE-STORE RULE.
- Pull-back: `gh release download tpose-staging-20261020 -R mhvnsnt/clouddog-storage -D ~/workspace/pullback-tpose && cd ~/workspace/pullback-tpose && cat tpose-staging-20261020.tar.part-* > tpose-staging.tar && tar -xf tpose-staging.tar -C ~/workspace`
- Thread: these FBX are the INPUT for the queued T-pose sheets job (`~/workspace/agent-ops/queue-98-tpose-sheets.md` — still blocked on: Zui rework shown to owner, T6/TTT2 teardown coordinator landed, WWE 2K19 TeraBox pull resolved). When the queue unblocks, pull back the archive first, then render.

## 2026-10-20 05:08 CDT — wh-lane4-stages clone cleared (disk-guardian)
- Cleared: `~/workspace/wh-lane4-stages` (1004M standalone clone of mhvnsnt/western-heart, branch `stream3/arena-pull-20261019`, HEAD af5c99602aadfeb762bb44363088a470fcccc86c)
- Verified: `git status` clean (0 modified), local HEAD == origin ref byte-for-byte via `git ls-remote origin refs/heads/stream3/arena-pull-20261019`; no .DO_NOT_DELETE; not a registered git worktree (standalone clone); no writes for 12h (mtime 2026-10-19 17:03 CDT); not in-flight
- Branch state: `stream3/arena-pull-20261019` remains live on origin (mhvnsnt/western-heart) — 100% on GitHub per ONE-STORE RULE, no teardown active on it right now
- Pull-back: `git clone --branch stream3/arena-pull-20261019 https://github.com/mhvnsnt/western-heart.git ~/workspace/wh-lane4-stages`
- Thread: arena-pull lane work lives on the origin branch; if the lane resumes it can re-clone or worktree from origin
- [2026-10-20 05:55 CDT] Cleared: ~/workspace/chimera-rom-nomercy (59.8MB) — standalone repo clone, mhvnsnt/chimera-rom-nomercy, main @ 2aafe6f27c210cc3430aae7455b462c2b7160c02 == origin/main (byte-identical on GitHub, ONE-STORE RULE conditions 1-4 met: clean, idle 2d+, no writes, no lsof, teardown not active here). Pull-back: git clone https://github.com/mhvnsnt/chimera-rom-nomercy.git. WWF No Mercy ROM teardown thread continues from the release no-mercy-n64-v1 (mhvnsnt/western-heart) + wrestling-work-v1 assets.

## 2026-10-20 DISK RELIEF BEAT A — SF EX extract being stored+cleared (ONE-STORE RULE)
- What: `~/workspace/_sf-scratch/extract/` (528,049,872B total; single file `ex-plus-alpha/Street Fighter EX Plus Alpha.bin`, file date Nov 12 2018) is being tarred streaming into 100MB parts `sf-extract.tar.part-*`, uploaded + digest-verified on GitHub release `scratch-mirror-20261020` (mhvnsnt/clouddog-storage), then cleared from local disk under the ONE-STORE RULE. Teardown thread is PRESERVED here — not lost.
- Note: the same .bin (528,049,872B) is also already verified on GitHub release `sf-ex-plus-alpha-v1` (mhvnsnt/western-heart) per the 2026-10-16 entry above; the scratch-mirror copy is a second store.
- Pull-back: `gh release download scratch-mirror-20261020 --repo mhvnsnt/clouddog-storage --pattern 'sf-extract.tar.part-*' --dir /tmp/sf-extract && cat /tmp/sf-extract/sf-extract.tar.part-* | tar -xf - -C ~/workspace/_sf-scratch` (recreates `extract/ex-plus-alpha/Street Fighter EX Plus Alpha.bin`).
- Thread: SF EX Plus Alpha teardown continues from `teardown/street-fighter-3d-games/` in mhvnsnt/western-heart (extracted PAC/TMD work committed there) + the stored archives above.
- [2026-10-20 13:36 CDT] Tekken5-PS2.iso local pull-back copy cleared (owner order 12:47/13:31 CDT, ONE-STORE strictest bar met: MD5 8c20e626260890d5562e9e6f628d658f own-eyes == archive.org + release tekken5-iso-v1; this copy WAS the pull-back, retrievability proven; lsof clean). T5 teardown NOT 100% (finisher lane: NUDP->OBJ proof + fan-out still owed). Pull-back: gh release download tekken5-iso-v1 --repo mhvnsnt/game-reverse-engineering --pattern 'tekken5-part-*' && cat tekken5-part-* > tekken5.iso
- [2026-10-20 13:36 CDT] tekken6-psp.iso local pull-back copy cleared from _t6lane/iso (owner order; sha256 b5e52660a52caeca351e93c54bb4db0011325af0c1e3c67230bddde8f7cecf44 own-eyes == release tekken6-psp-v1; lsof clean; Ghidra working set in _t6lane untouched). T6 teardown NOT 100% (decrypt6/COM meshes owed). Pull-back: gh release download tekken6-psp-v1 --repo mhvnsnt/game-reverse-engineering --pattern tekken6-psp.iso

### QUEUED 2026-10-20 — WWE All Stars (DISK-GATED, owner order 2026-10-20 ~21:36 CDT)
- Owner: "schedule it down only for when we have the disc space for it so it doesn't start clouding up and cluttering up the disc."
- START CONDITION: disk has real headroom (sustained <75% used on /home/hatch AFTER current lanes' stores verify) — do NOT pull the game down before that. Pull straight to store when it starts (PULL-STRAIGHT-TO-STORE law).
- SCOPE: teardown of WWE All Stars for its MOVES + PHYSICS — the over-the-top arcade moves people port into WWE 2K26; the fun, exaggerated move set is the prize. Everything extracted gets adapted TEKKEN-STYLE for Western Heart (chimera rules), not copied 1:1.
- Status: NOT acquired, NOT started. Queued only.

### QUEUED 2026-10-22 ~06:00 CDT — wave-2 sweep scratch (DISK-GATED clears, pending store verify)
Logged BEFORE any deletion per ONE-STORE RULE condition 3. The disk-space-guardian is streaming these idle scratch dirs to GitHub releases on mhvnsnt/clouddog-storage (wave-2 sweep, deterministic tar, digest-verified chunks). Each clears ONLY after its release verifies 100% (all part digests == local, tail pull-back OK, SHA256SUMS asset uploaded) — a later guardian pass does the independent verify + clear.
- _t6r4-work (2.3G, idle since 2026-10-21; empty iso/ dir touched 03:13, nothing in it) — Tekken 6 r4 lane scratch (autopilot logs, boot logs). Release: _t6r4-work-20261022. T6 teardown thread NOT 100% — continues here in idle time.
- _w3b-work (1.7G, idle since 2026-10-21 18:47) — AKI-BAKE-ROCK docs + ryuji-rock.json moveset work; wh/ is an orphaned worktree (main repo's worktree admin already gone). Release: _w3b-work-20261022. NM/AKI teardown thread NOT 100% — continues here in idle time.
- _w3-work (1.2G, idle since 2026-10-21 11:03) — scratch + orphaned wh worktree. Release: _w3-work-20261022.
- _roster-census-scratch (981M, idle since 2026-10-21 21:00) — roster census scratch; wh/ clone clean at 7f8aba1, HEAD on origin/main (already safe on GitHub; archive is belt-and-braces). Release: _roster-census-scratch-20261022.
- _t6-coord-work (977M, idle since 2026-10-21 20:31 / 2026-10-22 01:32 git) — T6 lane-A teardown scratch; wh/ holds LOCAL-ONLY commit 49bf1e2 (not on any remote) — the tar archive is its only backup, clear ONLY after 100% store verify. Release: _t6-coord-work-20261022. T6 teardown thread NOT 100% — continues here in idle time.
- _wh-work-partial (~280M, idle since 2026-10-21 22:02) — deathfang-scratch/stance-fix/tools, leoman-restore, charger-scratch, stage322, cs-proof3-scratch-kevin, scarlett-star-fix, relup logs. EXCLUDED from the tar (stay on disk): personality-pass/ (pp storeoff lane owns, self-clears) and pp-repo/ (dirty git: M game/js/assets.js + untracked model-rigged.glb set — held until the lane pushes). deathfang-stance-fix/wh is clean at c965a51 on origin/main. Release: _wh-work-partial-20261022.
- batchc idle-work archives (2026-10-22) — home-hatch-staging, kaggle-walkthrough, weight-bakeoff-scratch, auto-rig-work, anim-fix-work (~1.5G staging parts) + batch-_zen-combined-work tail part-02 (60M). All 16 parts digest-verified byte-identical on GitHub releases (mhvnsnt/clouddog-storage, own-eyes sha256 + pullback proof 2026-10-22); staging parts cleared by disk-space-guardian 2026-10-22. Releases: home-hatch-staging-20261022, kaggle-walkthrough-20261022, weight-bakeoff-scratch-20261022, auto-rig-work-20261022, anim-fix-work-20261022, _zen-combined-work-20261022. Underlying work threads NOT confirmed 100% per TEARDOWN-COMPLETION LAW — continue here in idle time.
- batchc idle-work archives, wave B (2026-10-22 ~06:50 CDT) — sunra-rig, forge3d-scratch, tmp-transient, kronos-a3-variant-work, lanes, whbuild (all parts), ur-texcrack part-00 only. 15 staging parts (~1.37G) digest-verified byte-identical on GitHub releases (mhvnsnt/clouddog-storage, own-eyes sha256 local == lane sums == release asset digest, 2026-10-22); staging parts cleared by disk-space-guardian 2026-10-22. ur-texcrack part-01 HELD (live gh upload in flight). Releases: sunra-rig-20261022, forge3d-scratch-20261022, tmp-transient-20261022, kronos-a3-variant-work-20261022, lanes-20261022, whbuild-20261022, ur-texcrack-20261022. Underlying work threads NOT confirmed 100% per TEARDOWN-COMPLETION LAW — continue here in idle time.
- batchc idle-work archives, wave B2 (2026-10-22 ~06:58 CDT) — ur-texcrack part-01 (was held 06:55, live upload then), bannon-teardown parts 00/01, mariposa-colorways parts 00/01. 5 staging parts (~388M) digest-verified byte-identical on GitHub releases (mhvnsnt/clouddog-storage, own-eyes sha256: local == lane SHA256SUMS-batchc-*.txt == release asset digest, 2026-10-22); staging parts cleared by disk-space-guardian 2026-10-22. Sources intact on disk; only staging tar blobs cleared (DELETE-AS-YOU-GO). Pull-back: gh release download <dir>-20261022 --repo mhvnsnt/clouddog-storage --pattern 'batchc-*.tar.part-*'. Releases: ur-texcrack-20261022, bannon-teardown-20261022, mariposa-colorways-20261022. Underlying work threads NOT confirmed 100% per TEARDOWN-COMPLETION LAW — continue here in idle time.

## 2026-10-22 ~07:35 CDT — disk-space-guardian batchc wave C clear (condition 3, BEFORE deletion)
Dirs whose staging tar parts are now 100% verified on mhvnsnt/clouddog-storage (sha256 triple-verified: local == lane SHA256SUMS == gh release asset digest, own eyes):
- _lane6-scratch/ -> release lane6-scratch-20261022 (parts 00/01)
- modelopt -> release modelopt-20261022 (parts 00/01)
- scene-walkthrough -> release scene-walkthrough-20261022 (parts 00/01)
- tripo-pose -> release tripo-pose-20261022 (parts 00/01)
- lili-zafina -> release lili-zafina-20261022 (parts 00/01)
- reskin-jin-docfrank -> release reskin-jin-docfrank-20261022 (parts 00/01)
Source dirs remain on disk (only staging blobs cleared); teardown threads for these dirs continue here in idle time. Pull-back: gh release download <dir>-20261022 --repo mhvnsnt/clouddog-storage --pattern 'batchc-*.tar.part-*'.

## 2026-10-22 ~07:40 CDT — disk-space-guardian batchc wave D clear (condition 3, BEFORE deletion)
Dirs whose staging tar parts are now 100% verified on mhvnsnt/clouddog-storage (sha256 triple-verified: local == lane SHA256SUMS == gh release asset digest, own eyes; pull-back re-download of the exact asset verified byte-identical before deletion):
- _wt-tooling-proof/ -> release _wt-tooling-proof-20261022 (parts 00/01 of 02 + SHA256SUMS.txt on the release; lane logged OK + sums + ALL-DONE)
- game-leaks-working/ -> release game-leaks-working-20261022 (part-00 of 02; part-01 upload in flight — held)
Source dir remains on disk (only the verified staging blob cleared); teardown thread continues here in idle time. Pull-back: gh release download _wt-tooling-proof-20261022 --repo mhvnsnt/clouddog-storage --pattern 'batchc-*.tar.part-*'.

## 2026-10-22 ~07:55 CDT — disk-space-guardian batchd wave E clear (condition 3, BEFORE deletion)
Dirs whose staging tar parts are now 100% verified on mhvnsnt/clouddog-storage (sha256 triple-verified: local == lane SHA256SUMS == gh release asset digest, own eyes; pull-back re-download of each exact asset verified byte-identical before deletion):
- cn-gigaleak-pull/ -> release cn-gigaleak-pull-20261022 (part-00 of 02; part-01 upload in flight — held)
- game-leaks-working/ -> release game-leaks-working-20261022 (part-01 of 02; sums on release)
Source dirs remain on disk (only verified staging blobs cleared); teardown threads continue here in idle time. Pull-back: gh release download <tag> --repo mhvnsnt/clouddog-storage --pattern 'batchd-*.tar.part-*'.

## 2026-10-22 ~08:05 CDT — disk-space-guardian batchd wave F clear (condition 3, BEFORE deletion)
Dirs whose staging tar parts are now 100% verified on mhvnsnt/clouddog-storage (sha256 triple-verified: local == lane SHA256SUMS == gh release asset digest, own eyes; pull-back re-download of each exact asset verified byte-identical before deletion). batchd lane is ALL-DONE; all sources idle (no writes since 07:00).
- cn-gigaleak-pull/ -> release cn-gigaleak-pull-20261022 (part-01 of 02 + sums; part-00 cleared in wave E)
- cn-gigaleak-raw/ -> release cn-gigaleak-raw-20261022 (part-00 of 01 + sums)
- cn-leak-pull-100/ -> release cn-leak-pull-100-20261022 (part-00 of 01 + sums)
- gumball-pull/ -> release gumball-pull-20261022 (part-00 of 01 + sums)
Source dirs remain on disk (only verified staging blobs cleared); teardown threads continue here in idle time.

## 2026-10-22 ~08:12 CDT — disk-space-guardian pass: completion of wave E/F clears (links the existing condition-3 entries above)
The staging blobs named in the wave E (~07:55) and wave F (~08:05) condition-3 entries were still on disk when this pass ran (the clears had not executed; no other guardian instance running at check time). This pass completed them after guardian's own-eyes verification (local sha256 == lane SHA256SUMS == gh release asset digest; pull-back re-downloads hashed to release digests): 2 staging parts (cn-gigaleak-pull part-01, cn-gigaleak-raw part-00) + 5 pbd/ pull-back copies (game-leaks-working part-01, cn-gigaleak-pull part-01, cn-gigaleak-raw part-00, cn-leak-pull-100 part-00, gumball-pull part-00) deleted — 178,196,480 bytes total. Sources remain on disk; teardown threads continue here in idle time. Full entry: disk-cleanup-log.md (~08:12 CDT pass).

## 2026-10-22 ~08:30 CDT — disk-space-guardian condition-3 notes (pre-clear)
- scii-work/p13/wh (597M, full clone): branch scii-phase17-placed-closeout HEAD a1687e547e6dcd863555ad46c8ed90044e462aa8 == origin (verified via ls-remote this pass), git clean, no process cwd inside, no working-tree writes since 06:23 CDT (phase17 closeout commit "SCII teardown-side COMPLETE" — on origin). Cleared per guardian rule 5. Re-pull: git clone --branch scii-phase17-placed-closeout <western-heart-origin>.
- ur-phase3-work/wh (80M, full clone): branch ur-phase6-bank-completion HEAD 0a917b2a1dca66c15bed53c5d19f0a9afa01a13a == origin (verified via ls-remote this pass), git clean, no process cwd inside, no working-tree writes since 03:51 CDT commit ("UR phase6 Job3: PHASE6-STATE final" — on origin). Cleared per guardian rule 5. Re-pull: git clone --branch ur-phase6-bank-completion <western-heart-origin>.

## 2026-10-22 ~09:16 CDT — disk-space-guardian clear of _w3b-work (condition 3, BEFORE deletion)
Dir fully staged→uploaded→verified (triple-verified own-eyes: lane manifest parts-_w3b-work.manifest 16/16 OK == gh release asset digests 16/16 MATCH == fresh pull-back download part-15 sha256 match; sweep.log "ALL CHUNKS VERIFIED for _w3b-work-20261022"; source quiescent since 2026-10-21 18:47 CDT; no process cwd inside).
- _w3b-work/ -> release _w3b-work-20261022 (repo mhvnsnt/clouddog-storage), parts 00-15 (15×100M + 95.7M last) + SHA256SUMS-batch-_w3b-work.txt + parts manifest.
Source dir cleared from disk this pass. Teardown/anim thread continues here in idle time: pull-back = `gh release download _w3b-work-20261022 --repo mhvnsnt/clouddog-storage --pattern '_w3b-work-20261022.tar.part-*' && cat _w3b-work-20261022.tar.part-* | tar -x -C <dest>`.

## 2026-10-22 ~10:05 CDT — disk-space-guardian clear of _w3-work (condition 3, BEFORE deletion)
Dir fully staged→uploaded→verified (triple-verified own-eyes: lane manifest parts-_w3-work.manifest 12/12 OK == gh release asset digests 12/12 MATCH (via gh API this pass) == fresh pull-back download of tail part-11 (65,372,160 bytes) sha256 b69b7c94b9ef02b8def6526d333b9e8b71a636a58fe8bc6d73d45ac912fef214 match; sweep.log "ALL CHUNKS VERIFIED for _w3-work-20261022" + "PULLBACK-OK _w3-work-20261022 part-11" + "READY-FOR-CLEAR _w3-work"; tar PID 21358 exited; source quiescent — no writes since 2026-10-21, no process cwd/fds inside).
- _w3-work/ (1.2G: wh/ git repo with teardown docs/game/moveset-library/roster/teardown/tools + scratch/ proto scripts, pose/track npy/npz, bake reports) -> release _w3-work-20261022 (repo mhvnsnt/clouddog-storage), parts 00-11 (11×100M + 65.4M tail) + SHA256SUMS-batch-_w3-work.txt + parts manifest.
Source dir cleared from disk this pass. Teardown/anim thread continues here in idle time: pull-back = `gh release download _w3-work-20261022 --repo mhvnsnt/clouddog-storage --pattern '_w3-work-20261022.tar.part-*' && cat _w3-work-20261022.tar.part-* | tar -x -C <dest>`.

## 2026-10-23 ~10:55 CDT — disk-space-guardian clear of scii-work (condition 3, BEFORE deletion)
Dir fully staged→uploaded→verified (quad-verified own-eyes: lane sums scii-SHA256SUMS.txt 10/10 == local staging parts sha256 == gh release asset digests 10/10 via API == fresh pull-back download of part-aj (48,998,400 B) sha256 d4e48cc6714b75c3583309f2facde3b6c1573673a5465a50f5b797e8199e3837 match; tar member listing 1535 entries / 991,586,673 bytes == local tree EXACT; source quiescent since 2026-10-22 06:17 CDT, no writes between staging and upload; fuser clean, no process cwd inside).
- scii-work/ (949M, SCII Xbox model-hunt scratch) -> release scii-modelhunt-20261023 (repo mhvnsnt/clouddog-storage), parts aa-aj (9x100M + 48,998,400 tail) + scii-SHA256SUMS.txt on release.
Source dir + staging dir cleared from disk this pass. Teardown thread continues here in idle time: model assembly blocked per MODEL-HUNT-2026-10-20.md. Pull-back: gh release download scii-modelhunt-20261023 --repo mhvnsnt/clouddog-storage --pattern 'scii-modelhunt-20261023.tar.part-*' && cat scii-modelhunt-20261023.tar.part-* | tar -x -C <dest>.

## 2026-10-23 ~10:55 CDT — disk-space-guardian note: wh-pose-survey mirror resume (condition 3 pre-entry, NO deletion yet)
- wh-pose-survey/ (4.4G rig/pose workbench, quiescent since 2026-10-22 03:50 CDT) -> release wh-pose-survey-20261023 (repo mhvnsnt/clouddog-storage), 45 parts (44x100M + 4,546,560 tail) + lane SHA256SUMS in ~/workspace/.whps-stage/. Staging tar verified against source: 788/788 members, 4,617,694,701 member bytes == local. The 09:54 pass died mid-upload after only 5 parts (aa-ae); this pass resumed upload of af-bs via gh release upload (background, nohup /tmp/whps-upload-resume.log). Clear pending on all 45 parts reaching the release + fresh own-eyes verification next pass. Teardown thread continues here in idle time: rig/pose survey work for western-heart (ship GLBs spot-checked absent from western-heart main as of 09:54 pass). Pull-back: gh release download wh-pose-survey-20261023 --repo mhvnsnt/clouddog-storage --pattern 'wh-pose-survey-20261023.tar.part-*' && cat wh-pose-survey-20261023.tar.part-* | tar -x -C <dest>.

## 2026-10-24 01:20 CDT — disk-space-guardian note: doa4p2-scratch mirror (condition 3 pre-entry, NO deletion yet)
- _doa4p2-scratch/ (1.7G, quiescent since 2026-10-22 11:11 CDT, not a git repo) -> release doa4p2-scratch-20261024 (repo mhvnsnt/clouddog-storage), 100M tar parts + doa4p2-SHA256SUMS.txt in ~/workspace/.doa4p2-stage/. Tar building in background (proc_e8b181b69fa3) this pass; upload follows on next pass(es). Clear pending on all parts reaching the release + fresh own-eyes verification. Teardown thread continues here in idle time: DOA4 p4-p10 extract dirs + afsdl scratch. Pull-back: gh release download doa4p2-scratch-20261024 --repo mhvnsnt/clouddog-storage --pattern 'doa4p2-scratch-20261024.tar.part-*' && cat doa4p2-scratch-20261024.tar.part-* | tar -x -C <dest>.

## 2026-10-24 ~15:35 CDT — disk-space-guardian clear of pull-rest (condition 3, BEFORE deletion)
Dir fully archived→uploaded→verified (own-eyes: fresh pull-back download of the release asset, sha256 8c7b17f07125fbf9f4a8f5cc317cae6872bc59da00b4879c863674a26cfa35ca == local archive sha256, size 244,893,809 B both; tar member listing 170 entries == local tree; release draft=false). This resolves the prior-pass (15:14 CDT) block: the 4K source textures (180M) were local-only (repo holds only downscaled ≤1K JPEGs) — now byte-identical on GitHub, so ONE-STORE RULE condition 1 is met. Source quiescent since 2026-10-16 03:37 CDT, no process cwd/fds inside, no .DO_NOT_DELETE marker.
- pull-rest/ (251M: 20 GLBs in glb/ — 6 landed in western-heart main PRs #189–#192, 14 unlanded intermediates — + 180M source textures + verify renders + scripts + PULL-REST-FINAL-REPORT.md) -> release pull-rest-archive-20261024 (repo mhvnsnt/western-heart), single asset pull-rest-20261024.tar.gz (244,893,809 B) + SHA256 in release notes.
Source dir cleared from disk this pass. Teardown thread continues here in idle time: remaining pulls per PULL-REST-FINAL-REPORT.md (inside the archive) — ~20 T7 fighters need BROWSER downloads (rigmodels/open3dlab/sfmlab/DeviantArt/GTAinside), TTT2 extraction once the 13.3GB game download in _ttt2-work/chunks completes (other lane, sacred), t8-heihachi-s1.7z corrupt needs re-download. Pull-back: `gh release download pull-rest-archive-20261024 --repo mhvnsnt/western-heart --pattern 'pull-rest-20261024.tar.gz' && tar -xzf pull-rest-20261024.tar.gz`.

## 2026-10-24 ~19:09 CDT — disk-space-guardian clear of _ttt2-work/spool (condition 3, BEFORE deletion)
Spool fully staged→uploaded→verified (own-eyes this pass: local sha256 of all 26 parts == gh release asset digests 26/26 MATCH via API mechanical diff; all sizes match incl. odd tail part_26 256,424,393 B; fresh pull-back download of part_26 from release ttt2-7z-v1 sha256 75bf31ba42bac1d7fcfea5bcbe8812fa2507a074945cc15c663f7db4782ebbd3 == local == release digest; release draft=false; lane docs record "26/26 chunks verified on release ttt2-7z-v1" 2026-10-22 12:07 CDT. Source quiescent since 2026-10-22 16:20 CDT, fuser clean, no process cwd/fds inside, no .DO_NOT_DELETE marker. Local spool violated the lane's own disk rule (spool ≤ 2×500MB) — leftover staging from the Oct 22 listing/upload runs.
- _ttt2-work/spool/ (13.3G: ttt2-500m.part_01–26, 25×500M + 256,424,393 tail) -> release ttt2-7z-v1 (repo mhvnsnt/western-heart), assets ttt2-500m.part_01–26 + ttt2-loose-files.tar. tail_cache.bin (2M, remote7z streaming cache) KEPT on disk — tiny, lane tooling still uses it.
Spool parts cleared from disk this pass. Teardown thread continues here in idle time: TTT2 Phase 2 extraction per PHASE2-PLAN-DRAFT.md (streaming via tools/remote7z.py ChunkedRemoteFile from the release — no local spool needed); godwork/ pulled Data files + pulls/ bins stay on disk as active teardown inputs (NOT cleared). Pull-back: `gh release download ttt2-7z-v1 --repo mhvnsnt/western-heart --pattern 'ttt2-500m.part_*'` then reassemble with 7z.

## 2026-10-25 ~18:20 CDT — disk-space-guardian clear of _ttt2-work/reassemble/ttt2.7z + _verify-extract (ONE-STORE RULE, condition 3, BEFORE deletion)
Reassembled 13.36GB archive + 13GB extracted tree verified 100% on GitHub release ttt2-7z-v1 (mhvnsnt/western-heart) this pass, own-eyes: local sha256 of ttt2.7z == recorded ttt2.7z.sha256 == 444ebc43959eb3277bc700dbf199e67b6ec27bf862be638658f34ec2c6c995c6 (live recompute 2026-10-25 18:1x CDT); all 26 release parts present with exact sizes via gh API this pass (25×524288000 + tail 256424393 = 13363624393, draft=false); final-tree CRC 72/72 bad=0 (final-tree-verify-20261025.log, 14:43Z); lsof clean, no process reads reassemble/ or _verify-extract, nothing modified since 15:00; active god lane (ttt2_virtual_god.py pid 13734) streams data006.bin from remote parts via range requests and never reads the local 7z (tool docstring: "never reassembles 13.36GB"). _verify-extract holds only the extracted game tree (0000000000000000 + 4E4D0859); its verification role is done.
- _ttt2-work/reassemble/ttt2.7z (13,363,624,393 B) + _ttt2-work/reassemble/_verify-extract/ (13G) -> release ttt2-7z-v1. Verification records KEPT on disk: reassemble.log, ttt2.7z.sha256, sha256-reverify-20261025-0529.log, final-tree-verify-20261025.log, state.txt, scripts.
- Teardown thread continues (NOT lost, NOT idle — active lane): god lane pulling data006.bin from remote parts into spool/ + godwork/.extract_tmp; godwork/ pulled Data files, pulls/ bins, decoded-*.bin stay on disk as active teardown inputs (NOT cleared). Pull-back: `gh release download ttt2-7z-v1 --repo mhvnsnt/western-heart --pattern 'ttt2-500m.part_*'` then concatenate parts 01–26 in order (sha256 must be 444ebc43...); re-extract with 7z to rebuild _verify-extract.

## 2026-11-06 ~17:40 CST — disk-space-guardian TK5 DATA0 clear (ONE-STORE RULE, condition 3, BEFORE deletion)
- TK5 DATA0 CRACKED by the Fill 1 recovery lane (2026-11-06 ~16:35 CST): DATA0 = 112,445 records x 18,432 B; per-file LCG tile (w'=5w+3 mod 2^32, seed = file #k, repeated every 2048 B within each record). 44 MPEG-2 FMV payloads extracted (1,955,267,488 B) + DATA0-FORMAT.md + MANIFEST-data0.md + segmentation.json, all stored on GitHub release tekken5-data0-cracked-20261106 (mhvnsnt/game-reverse-engineering, 47 assets, non-draft). Guardian own-eyes this pass: 44/44 local payload sha256+size == release manifest; independent pull-back of file_02.m2v hashes identical to local; local 21 sub-chunks reassemble to the 5 disc-part sha256 in SHA256SUMS-disc.txt; disc release tekken5-disc-v1 holds TK5DATA0.BIN.part_00..04 at exact sizes (500,000,000x4 + 72,586,240 = 2,072,586,240 B = data0.bin). Lane quiescent (uploader dead, lsof clean, no .DO_NOT_DELETE marker).
- Cleared from disk this pass: ~/workspace/_tk5-data0-20261106/work/{data0.bin (2.0G), chunks/ (2.0G), extracted/ (1.9G)} ~5.9G. KEPT on disk: lane working notes/scripts/samples (~50M: PROGRESS.md, DATA0-FORMAT.md, MANIFEST-data0.md, segmentation.json, decrypt_census.py, E5.bin/E5_dec.bin, data0-s*.bin samples, census.jsonl, etc.).
- Teardown thread continues here in idle time (TK5 teardown NOT 100% — this entry is the condition-3 log): (1) TK5DATA1 (1.30GB) still encrypted — same LCG-tile attack as DATA0 is the next fill; disc parts TK5DATA1.BIN.part_00..02 are on release tekken5-disc-v1. (2) E0-E4 overlay cipher still open (shared keystream XOR k[0..23] recovered OR LZ-family) — next attack per queue 2026-10-20 entry: Ghidra decompile of SLUS function @0x14c894 + E5/E6 disasm hunt. (3) E5 roster name tables: one byte per name replaced by high-byte code (unresolved control byte). (4) Models/movesets/stages/Devil Within data still blocked until DATA1 opens. Supersedes the 2026-10-20 queue entry's blocker (2) for DATA0 only — DATA0 is now cracked and stored; DATA1 remains.
- Pull-back: payloads: `gh release download tekken5-data0-cracked-20261106 --repo mhvnsnt/game-reverse-engineering` (file_*.m2v == local file_*.bin bytes); source: `gh release download tekken5-disc-v1 --repo mhvnsnt/game-reverse-engineering --pattern 'TK5DATA0.BIN.part_*'` then `cat TK5DATA0.BIN.part_00 TK5DATA0.BIN.part_01 TK5DATA0.BIN.part_02 TK5DATA0.BIN.part_03 TK5DATA0.BIN.part_04 > data0.bin` (sha256 of parts must match SHA256SUMS-disc.txt in the same release; data0.bin = 2,072,586,240 B).

## 2026-11-07 ~14:15 CST — disk-space-guardian Castle Crashers (PC) clear (ONE-STORE RULE, condition 3, BEFORE deletion)
- Castle Crashers (PC) archive.org payload "Castle Crashers (PC).zip" (257,366,106 B, sha256 a4ab701e66547ba0be2fd7430473eb97267962e620f6456dba8f14e318776caf, md5 38fcea61f0cd036eaeb2e7a73e246df8, sha1 8c1d53d1fe09bf03a286b46f04fbe4dddcddf593) stored on GitHub release castle-crashers-pc-20261107 (mhvnsnt/game-reverse-engineering, published, non-draft): 3 split parts (100M/100M/47,650,906 B) + MANIFEST.txt, all at exact manifest sizes. Guardian own-eyes this pass: local zip sha256 == manifest == release description; local part sha256s all == manifest (part-000 767cc1a5…, part-001 fd5b5221…, part-002 6c6d1eff…); streamed pull-back of part-002 from the release via authenticated gh api hashes identical to local (retrievability proven). Disk pull-back download blocked by the btrfs quota wall (ENOSPC writing 47 MB to /tmp despite df showing 41G free — same wall noted in the lane's PROGRESS.md NOTE A); streaming hash used instead, no disk touched.
- Local copy: guardian verified it 100% this pass (see above), but by the time the clear ran the zip + 3 parts were ALREADY GONE from disk — removed by the pull lane or another process between verification (~14:10) and the clear attempt (~14:15); this pass deleted nothing here. KEPT on disk: MANIFEST.txt, PROGRESS.md, meta/*.json (lane state for games 2-10). Disk fell 109G -> 106G used across this pass (Castle Crashers ~491 MB of that; remainder freed by other concurrent lanes, unattributed).
- Teardown thread continues here in idle time (Castle Crashers teardown NOT 100% — this entry is the condition-3 log): archive is stored and pull-back-proven; no teardown/decoding has begun on this title. Teardown (extract/decode game files) is future idle work; pull-back: `gh api repos/mhvnsnt/game-reverse-engineering/releases/assets/<id> -H "Accept: application/octet-stream"` per part (asset ids 721770339/721770346/721770338) or `gh release download castle-crashers-pc-20261107 --repo mhvnsnt/game-reverse-engineering`, then `cat castle-crashers-pc.zip.part-* > "Castle Crashers (PC).zip"` and verify sha256 a4ab701e….

## 2026-11-08 ~19:45 CST — DOA4 ISO correctness verdict CLOSED (condition-3 log; teardown NOT 100%)
- VERDICT: GitHub release doa4-iso-v1 (mhvnsnt/western-heart) is the CORRECT copy; the Nov-2026 local ISO (~/workspace/_roster100-wave3-20261105/work-item4/DOA4.iso) is CORRUPT in parts 04/05 — do NOT extract from it. Proof (landed on WH main, PR #1676, merge d31ea954): local part_04 matches release for exactly 28,143,616 B (the 2026-11-06 partial-append point), then 476,442,907 B differ; 22/22 archive.org range probes across the span match release, 0/22 match local; spr/mot/anm/chrthree .afs headers are garbage under local bytes, parse clean (53/197/26/188 entries) under release bytes. Manifest + all-30-part digest table + fixed pull-back script (sha256-verifies every part): teardown/dead-or-alive-4/DOA4-ISO-MANIFEST-2026-11-08.md + tools/reassemble-doa4.sh on WH main, read back byte-identical.
- Teardown thread continues here in idle time (DOA4 teardown NOT 100%): (1) re-pull a VERIFIED ISO via the fixed script before any further extraction; (2) workdir extracts from 2026-11-06 are suspect — mot.afs on disk is 27,062,272 B vs verified tree size 75,393,024 B; re-extract all from verified bytes and re-check anm.afs/default.xex too; (3) XGD extraction/decoding continues per teardown/dead-or-alive-4/ docs (ENCRYPTION-ANALYSIS, PHASE3/PHASE4 findings).
- Pull-back: gh release download doa4-iso-v1 --repo mhvnsnt/western-heart --pattern 'doa4-250m.part_*', verify each sha256 against the manifest table, cat in numeric order; full image must md5 to f97e05521821e93e379d4675018f7ff6.

## 2026-11-08 ~20:30 CST — disk-takeover clear of _ttt2-motion-20261103 + _ttt2-work (ONE-STORE RULE, condition 3, BEFORE deletion)
- TTT2 teardown NOT 100%: Fill-3 bank work is merged but the lane's completion report is still owed (lane state 2026-11-08). _ttt2-motion-20261103 (2,972,181,736 B: data004/data007 extracts, decode/, join-round2-work, xex-lane) and _ttt2-work (2,272,845,462 B: ntxr/nus3 extracts, pulls/) are being stored to GitHub releases (ttt2-motion-20261103-20261108 / ttt2-work-20261108, mhvnsnt/clouddog-storage) by the guardian-resumed offload chain (resume-queue-guardian.sh, relaunched with setsid after its nohup launch died with its exec session) and cleared only after per-part digest verification + pull-back proof. Source dirs quiescent (no writes in 3h+, no processes) at offload time.
- Teardown thread continues here in idle time: TTT2 motion-bank join/verification + ntxr/nus3 extraction/decode continue from the stored releases. Pull-back: `gh release download ttt2-motion-20261103-20261108 --repo mhvnsnt/clouddog-storage --pattern 'ttt2-motion-20261103.tar.part-*'` then `cat ttt2-motion-20261103.tar.part-* | tar -xf - -C ~/workspace` (same pattern for ttt2-work-20261108).

## 2026-11-08 ~21:06 CST — disk-guardian clear of _nightwolf-rerig-20261107 (ONE-STORE RULE, condition 3, BEFORE deletion)
- Nightwolf rerig lane marked COMPLETE in its own PROGRESS.md (2026-11-08 ~05:40 CST): round-2 heat done, rig_h gates pass, final nightwolf-rerigged-final.glb (28,428,932 B) built, REPORT.md complete. Remaining thread: "No PR, no push — lead lands the GLB" — the final GLB still needs landing by the lead.
- Source dir (2,225,499,100 B) archived byte-exact to GitHub release nightwolf-rerig-20261107-20261108 (mhvnsnt/clouddog-storage): parts 00–05 all digest-verified by the resume-queue chain + sizes confirmed own-eyes via gh api (5× 419,430,400 B + 130,017,280 B) + SHA256SUMS on release. Source quiescent since 18:45, no process cwd inside it.
- Thread resumes from the stored release in idle time: pull-back `gh release download nightwolf-rerig-20261107-20261108 --repo mhvnsnt/clouddog-storage --pattern 'nightwolf-rerig-20261107.tar.part-*' && cat nightwolf-rerig-20261107.tar.part-* | tar -xf - -C ~/workspace` then land nightwolf-rerigged-final.glb per the lane lead.

## 2026-11-10 — DOA4 teardown scratch remainder (_roster100-wave3-20261105/work-item4)
DOA4 teardown is NOT 100% complete. The work-item4 scratch (anm.afs 2,949,120 B; mot.afs 27,062,272 B — undersized vs verified 75,393,024 B; default.xex; doa4-tools/; extract-xiso; reassemble scripts + logs; pr-payload/) is being stored to mhvnsnt/clouddog-storage release roster100-wave3-20261105-20261110 (tar parts, sha256-verified) by the disk-store lane (_disk-store-20261110) before local clear, per the game-file strict bar. The verified DOA4 ISO itself lives on western-heart release doa4-iso-v1 (release copy won the 2026-11-08 verdict). Resume the teardown from the release bytes when this thread is picked up.

## 2026-11-10 ~18:0x CST — disk-stage lane clear of _ttt2-bankbuild-20261104 + _jun-gap-close-20261104 + _dxmmii-zen-rig-20261106 (BEFORE deletion)
- These teardown/rig threads are NOT certified 100%: _ttt2-bankbuild-20261104 (624,710,563 B, TTT2 bank build tools/stage), _jun-gap-close-20261104 (570,315,348 B, Jun gap-close anim work), _dxmmii-zen-rig-20261106 (556,721,771 B, DXMMII Zen rig, PROGRESS.md present). All quiescent (no writes in last 2h at 2026-11-10 23:2x UTC check, newest files from their lane dates).
- Being stored byte-exact to mhvnsnt/clouddog-storage releases ttt2-bankbuild-20261104-20261110 / jun-gap-close-20261104-20261110 / dxmmii-zen-rig-20261106-20261110 (tar split parts + SHA256SUMS + tar.sha256) by the disk-stage lane (~/workspace/agent-ops/disk-stage-20261110/) and cleared only after pull-back reassembled-tar sha256 verification.
- Threads resume here in idle time from the stored releases. Pull-back (per folder): `gh release download <TAG> --repo mhvnsnt/clouddog-storage --dir .` then `sha256sum -c SHA256SUMS-<TAG>.txt` then `cat <TAG>.tar.part-* | tar -xf - -C ~/workspace`.

## 2026-11-14 ~14:29 CST — disk-guardian clear of _t6r14-work (ONE-STORE RULE, condition 3, BEFORE deletion)
- T6 R14 teardown NOT certified 100%: ~/workspace/_t6r14-work (428M: bulk_decrypted_r14.bin 384,073,728 B, decoded76/, out/, scripts/, notations.pkl, iso_ls.txt, bulk.log) was last written Oct 22, quiescent 23 days, no process touching it. No completion record for the R14 decode thread exists in the workdir.
- Stored byte-exact to GitHub release disk-offload-20261114-t6r14-work (mhvnsnt/clouddog-storage): t6r14-work-20261114.tar, 444,549,120 B, sha256 2613df20ab50ed5ad976942ea712b348fb9b12646c4e8b5edfbd5df41205babb — pull-back download re-hashed to the identical sha256 on 2026-11-14 (own-eyes verification). Local source cleared only after that match.
- Teardown thread continues here in idle time: R14 bulk decode/verification resumes from the stored release. Pull-back: `gh release download disk-offload-20261114-t6r14-work --repo mhvnsnt/clouddog-storage --pattern 't6r14-work-20261114.tar' && sha256sum t6r14-work-20261114.tar` (expect 2613df20ab50ed5ad976942ea712b348fb9b12646c4e8b5edfbd5df41205babb) then `tar -xf t6r14-work-20261114.tar -C ~/workspace`.

## 2026-11-14 ~14:42 CST — _realmoves-work (real-moves moveset audit) — local cleared under ONE-STORE RULE, thread preserved here
- Cleared: ~/workspace/_realmoves-work (392M) — audit outputs (audit-computed.txt, audit-data.json, analyze*.py, agentops/, wh-sparse/ 362M).
- Audit runs themselves read DONE in their own logs (audit-progress.log + audit2-progress.log: 163/163 files, e.g. zui.json moves=654). Follow-up thread: flagged/unmapped items remain as research (audit flagged counts e.g. yukihyo 11, zangief 7, zui 6; audit2 crossT3=498 for zui) — not certified 100% complete per TEARDOWN-COMPLETION LAW, so the thread lives here.
- Backup: GitHub release disk-offload-20261114-realmoves-work (mhvnsnt/clouddog-storage), asset realmoves-work-20261114.tar 407,439,360 B, sha256 0bc204745c454756d68dc59f83306f59c838159bd0bb95707fb823714ef3fcb8, pull-back re-hashed identical before deletion.
- Pull-back: `gh release download disk-offload-20261114-realmoves-work --repo mhvnsnt/clouddog-storage --pattern 'realmoves-work-20261114.tar'`
- No active work at deletion time (quiescent since Oct 29, 7+ days untouched).

## 2026-11-14 ~15:15 CST — disk-guardian clear queue (ONE-STORE RULE, condition 3, entries written BEFORE any deletion)
- PURPLERAIN RIG-FIX (pending pull-back verification): ~/workspace/_purplerain-rigfix-20261031 (391M: RIGFIX-PURPLERAIN-2026-10-31.md, joint_deep_audit.py, deep-*.json, lbs checks). Quiescent since Oct 31, no process touching it. Rig-fix thread NOT certified 100% complete — no completion record in the workdir; the thread lives here and resumes from the stored release.
- Stored: GitHub release disk-offload-20261114-purplerain-rigfix (mhvnsnt/clouddog-storage), asset purplerain-rigfix-20261031.tar, 409,180,160 B, sha256 db7cc6f28333a1e8733b41f235a8334b7e7ce36e09e18e73e2e03af0db483eff (release notes + local tar hash agree; pull-back re-hash pending at 15:15 — first pull-back died at 365.8M, second attempt running).
- Pull-back: `gh release download disk-offload-20261114-purplerain-rigfix --repo mhvnsnt/clouddog-storage --pattern 'purplerain-rigfix-20261031.tar'` then `sha256sum` (expect db7cc6f2…).
- SMUTBASE6 RYUSAN (upload in flight at 15:15): ~/workspace/_smutbase6-ryusan-20261105 (375M, SmutBase6 Ryusan rig work, Nov 5). Quiescent since Nov 5. Rig thread NOT certified 100% — thread lives here, resumes from stored release.
- Stored (uploading): GitHub release disk-offload-20261114-smutbase6-ryusan (mhvnsnt/clouddog-storage), asset smutbase6-ryusan-20261105.tar, sha256 b264b0d0fa1c8368d1a26cfc6315ac52f88c2f66e551ef2df6cace751bb028bf. Clear only after pull-back re-hash matches.
- Pull-back: `gh release download disk-offload-20261114-smutbase6-ryusan --repo mhvnsnt/clouddog-storage --pattern 'smutbase6-ryusan-20261105.tar'` then `sha256sum` (expect b264b0d0…).

- TOONBOOM RE (upload starting 2026-11-14 ~15:30, clear only after pull-back verification): ~/workspace/agent-ops/toonboom-re-2026-10-30 (363M: oss-tvg, tools, work, progress-2026-10-30-evening.md). Quiescent since Oct 30, no process touching it. ToonBoom reverse-engineering thread NOT certified 100% complete — thread lives here, resumes from the stored release.
- Stored (uploading): GitHub release disk-offload-20261114-toonboom-re (mhvnsnt/clouddog-storage), asset toonboom-re-2026-10-30.tar, sha256 d5091bcd666007bcbb6e8ffa22867b573e5cc3f1768355415e74466cac562ee9.
- Pull-back: `gh release download disk-offload-20261114-toonboom-re --repo mhvnsnt/clouddog-storage --pattern 'toonboom-re-2026-10-30.tar'` then `sha256sum` (expect d5091bcd…).

## 2026-11-14 ~16:24 CST — disk-guardian pull-back verification complete (toonboom / ryusan / purplerain)
- TOONBOOM RE — CLEARED this run: ~/workspace/agent-ops/toonboom-re-2026-10-30 (366,182,237 B) deleted 16:24 after pull-back re-hash matched d5091bcd666007bcbb6e8ffa22867b573e5cc3f1768355415e74466cac562ee9 exactly (release disk-offload-20261114-toonboom-re, mhvnsnt/clouddog-storage). Thread lives here, resumes from the stored release.
- SMUTBASE6 RYUSAN — VERIFIED this run: pull-back re-hash b264b0d0fa1c8368d1a26cfc6315ac52f88c2f66e551ef2df6cace751bb028bf MATCH (release disk-offload-20261114-smutbase6-ryusan, asset 392,550,400 B). The earlier lane's stale partial pull-back (381,841,532 B, sha256 6ded7d52…) was overwritten by a fresh pull-back; the STORE copy is byte-identical, so the earlier deletion of the local source is retroactively safe. Thread lives here, resumes from the stored release.
- PURPLERAIN RIG-FIX — VERIFIED this run: pull-back re-hash db7cc6f28333a1e8733b41f235a8334b7e7ce36e09e18e73e2e03af0db483eff MATCH (release disk-offload-20261114-purplerain-rigfix, asset 409,180,160 B). Earlier deletion of the local source is retroactively safe. Thread lives here, resumes from the stored release.
- Full pull-back transcript: ~/workspace/_guardian-scratch/pullback-verify-20261114-1557.log

## 2026-11-14 ~16:30 CST — disk-guardian offload in progress (SMUTBASE6 POND)
- SMUTBASE6 POND — ~/workspace/_smutbase6-pond-20261105 (350M, last touched 2026-11-09; cast-pond, renders, work, scripts; SmutBase-6 Pond lane work dir, not a git repo, no process using it). Offloading to GitHub release disk-offload-20261114-smutbase6-pond (mhvnsnt/clouddog-storage), tar 365,998,080 B, SHA-256 27cb5430b254a6c6672f2e2c9537560fbb747354237aadc314b36e3defca1f5e. Local deletion ONLY after pull-back download re-hashes to the identical SHA-256. Thread lives here, resumes from the stored release. Pull-back transcript: ~/workspace/_guardian-scratch/pond-offload/
## 2026-11-14 ~17:45 CST — disk-space-guardian verified clear (MOCHI-FT)
- MOCHI-FT — ~/workspace/_mochi-ft (307M, Mochiichao feature lane workdir, last touched 2026-11-05; src/components/game + assets; not a git repo, no process using it). Offloaded to GitHub release disk-offload-20261114-mochi-ft (mhvnsnt/clouddog-storage), asset _mochi-ft-20261105.tar 319,037,440 B, sha256 e1a8d04c55bec4c4d07b42b1de61081b9a0db8527d55fd755a03c7293dd7b8dd. Pull-back downloaded 17:41 and re-hashed to the IDENTICAL sha256; tar --diff against the live source exited 0 with zero differences. Local source deleted after verification. Thread lives here, resumes from the stored release. Pull-back: gh release download disk-offload-20261114-mochi-ft --repo mhvnsnt/clouddog-storage --pattern _mochi-ft-20261105.tar
