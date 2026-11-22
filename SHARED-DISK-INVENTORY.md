# SHARED DISK INVENTORY — what every agent has on disk

**Owner rule (2026-10-14):** Agents talk to EACH OTHER via this file. Before you re-download, re-extract, or claim something is "gone/lost," CHECK THIS FILE FIRST. If it's here, use it — don't duplicate it. If you add or remove something big (>100MB), UPDATE THIS FILE.

**Last updated:** 2026-10-15 ~02:15 EDT by disk-emergency lane (subagent)

## TeraBox session keeper (owner 2026-10-16 — permanent sign-in fix)
TeraBox auth = long-lived `ndus` cookie; sign-outs come from the Chromium profile resetting, not expiry. Uploads now go through the API path `~/workspace/tools/terabox-uploader/tbupload.py` (4MB chunks, auto-verify, no 225MB browser cap) — NOT browser tasks. `terabox-session-keeper` cron runs every 6h to verify + self-heal. If TeraBox looks "signed out": do NOT trust the probe — run `tbupload.py resolve` (TRY-BEFORE-YOU-FLAG). Only a failed real attempt counts. Design: `~/workspace/agent-ops/TERABOX-SESSION-KEEPER.md`.

## Continuous research + pull-in (owner 2026-10-16 — standing law)
Keep doing deep research on EVERYTHING related to all our work and keep pulling in what you find (open source first; document non-open-source licenses honestly, never crack/bypass). Wire it up, push green via branch → PR → merge, never clobber anyone's work. PULL-STRAIGHT-TO-STORE — no local disk hoarding. Workflow: `~/workspace/agent-ops/CONTINUOUS-RESEARCH-PULLIN-WORKFLOW.md`.

## Changes 2026-10-15 (disk emergency 96% → 73%)
- **DELETED** `~/workspace/trippedd-studio/` (19G local clone) — pushed all local branches (incl. 3 stash→store/stash-* branches) + 2 tags to origin, verified 0 local-only commits. Re-cloneable from mhvnsnt/TRIPPEDD-Production-studios-.
- **DELETED** `~/workspace/eastern-mind/wh_eastern_mind/` (414M), `terabox/` staging zips (403M), 3 cda wavs (181M) — all verified on western-heart main (PR #160) / repo soundtrack. Kept cdimg/ + emtlsotn.zip (game files, TeraBox pending).
- **VERIFIED+closed** audio-fix-work: EP01 FIXED master safe on drive-storage release `ep01-fixed-master-2026-10-14` (draft, part_aa/ab/ac state=uploaded, 2.42GB, ftyp confirmed). Local dir already removed by lane.
- **DELETED** `~/workspace/terabox-staging/home-hatch-backup/` (363M) — all 6 files byte-match published release home-hatch-backup-2026-10-14.
- **DELETED** `~/workspace/terabox-staging/gamerev-western-heart-assets/` (75M staging tar) — source intact at game-reverse-engineering/western-heart-assets/.
- **DELETED** `~/workspace/tools/chibirigkit/` (391M) — clean clone of public repo, re-downloadable.
- **Left alone (active processes):** video-fix-tools, font-wizard, cn-leak-pull-100, ep01-loti-swap.
- **Left alone (game files, need TeraBox + owner go-ahead):** T6 ISO, Def Jam partial ISO, SF EX bins, VF5 1.3G (on GH release vf5-model-library-v1, TeraBox pending), eastern-mind cdimg/zip, mdickie installers.

---

## Large files on disk (>500MB)

| Path | Size | What it is | Safe elsewhere? | Notes |
|---|---|---|---|---|
| `~/workspace/game-reverse-engineering/tekken6/tekken6-psp.iso` | 816MB | Tekken 6 PSP ISO | ✅ GitHub release `tekken6-psp-v1` | Recovered 2026-10-14 19:13 EDT. DO NOT DELETE — T6 decrypt lane needs it. |
| `~/workspace/western-heart-vf5/teardown/virtua-fighter-5/` | 1.3GB | VF5 model library (19 fighters + 38 stages) | ❌ NOT on GitHub yet | Push in progress (smaller chunks). DO NOT DELETE. |
| `~/workspace/ep01-loti-swap/EP01-THE-WALK-v2.mp4` | 2.4GB | EP01 finished with LOTI splice | ❌ Local only | Needs TeraBox/GitHub before any delete. |
| `~/workspace/ep01-assembly/EP01-THE-WALK-finished.mp4` | 2.3GB | EP01 master (older) | ❌ Local only | Do not delete while audio-fix lane active. |
| `~/workspace/terabox-staging/def-jam/SLUS_210.04.Def Jam - Fight for NY.iso` | partial of 4.69GB (in-flight from archive.org, sibling lane) | Def Jam FFNY PS2 ISO | ❌ Local only | Resume-capable (`curl -L -C -`). DO NOT DELETE (game file, resume law). |
| `~/workspace/game-reverse-engineering/street-fighter-3d-games/downloads/Street Fighter EX3 (USA).bin` | 701,813,280 bytes | SF EX3 PS2 (SLUS_201.30) | ✅ GitHub release `sf-ex3-v1` (uploading) | Byte-exact vs archive.org 2026-10-14. DO NOT DELETE (game file). |
| `~/workspace/game-reverse-engineering/street-fighter-3d-games/extracted/ex-plus-alpha/Street Fighter EX Plus Alpha.bin` | 528,049,872 bytes | SF EX Plus Alpha PS1 (SLUS_005.48) | ✅ GitHub release `sf-ex-plus-alpha-v1` (uploading) | Byte-exact vs archive.org 2026-10-14. DO NOT DELETE (game file). |
| `~/workspace/game-reverse-engineering/street-fighter-3d-games/downloads/Street Fighter EX2 Plus.7z` | 207,533,625 bytes | SF EX2 Plus PS1 7z source | ✅ GitHub release `sf-ex2-plus-v1` | Source archive. DO NOT DELETE. |
| `~/workspace/game-reverse-engineering/street-fighter-3d-games/downloads/Street Fighter EX Plus Alpha.7z` | 263,912,228 bytes | SF EX Plus Alpha PS1 7z source | ✅ GitHub release `sf-ex-plus-alpha-v1` | Source archive. DO NOT DELETE. |
| `~/workspace/audio-fix-work/EP01-THE-WALK-finished-FIXED.mp4` | 2.3GB | EP01 master (audio-fixed) | ❌ Local only | Audio-fix lane active on this. DO NOT DELETE. |

## Disk status
- **Current:** 73% (25GB free) as of 2026-10-15 ~02:15 EDT (was 96% at 01:38 EDT)
- **Owner ceiling:** 88% hard ceiling (popup at 90%)
- **Target:** <75% for TTT2/DOA4 lanes

## Agent claims — who has what
| Agent | Has on disk | Needs |
|---|---|---|
| Ashes (Muse) | T6 ISO, T6 decrypt tools, EP01 v2 | — |
| VF5 recovery worker | VF5 1.3GB lib (pushing to GitHub) | — |
| Grok Bot integration worker | western-heart clone (temp) | — |
| T6 EBOOT worker | Uses shared T6 ISO + tools | — |

## Rules
1. **Check this file before downloading anything >100MB.** If it's already here, use the existing copy.
2. **Update this file when you add or remove anything >100MB.**
3. **Never delete anything marked DO NOT DELETE** without owner approval.
4. **Upload → verify → THEN delete.** Never delete before the backup is confirmed.

## Owner inventory update (2026-10-14 20:34 EDT)
**On disk:**
- Tekken 6 (PSP) — `game-reverse-engineering/tekken6/` (821MB) — ISO byte-verified, EBOOT decrypted, sector cipher reversed
- Tekken 3 — `game-reverse-engineering/tekken3/` (407MB) — 100% teardown
- WWF No Mercy — `game-reverse-engineering/wwf-no-mercy/` (48MB) — ROM confirmed, 100% teardown
- Virtua Fighter 5 — `game-reverse-engineering/virtua-fighter-5/` (136MB) + `western-heart-vf5/teardown/virtua-fighter-5/` (1.3GB, re-pushing to GitHub)
- Street Fighter 3D — `game-reverse-engineering/street-fighter-3d-games/` (1.2GB)
- WWE 2K — `game-reverse-engineering/wwe2k/` (86MB) — anim packs on GitHub
- TTT2 — `game-reverse-engineering/tekken-tag-tournament-2/` (134MB) — full 13.3GB on GH release `ttt2-7z-v1`
- Soulcalibur II — `game-reverse-engineering/soulcalibur/` (4.9MB) — PS2 ISO on GH release, ~60% teardown
**On GitHub only:** DOA4 (7.8GB, `doa4-iso-v1`), WMXIX (ISO, `wmxix-iso-v1`, 80%), Urban Reign (extracted, 95%)
**Not acquired:** SFV (full game), Tekken 7 (full game), DOA6/SCVI (binaries)

## Eastern Mind lane (wh-easternmind-100, done 2026-10-15 ~02:25 UTC)
| Path | Size | What it is | Safe elsewhere? | Notes |
|---|---|---|---|---|
| `~/workspace/eastern-mind/emtlsotn.zip` | 549MB | Eastern Mind game archive (from GH release) | ✅ GitHub release `eastern-mind-v1` | DO NOT DELETE — game file, TeraBox pending |
| `~/workspace/eastern-mind/cdimg/` | 665MB | CloneCD .img+.ccd+.sub (game CD) | ✅ Re-extractable from zip | Game file, TeraBox pending |
| `~/workspace/eastern-mind/wh_eastern_mind/` | 414MB | Organized teardown (5,707 files by WH stage) | ✅ western-heart main (PR #160) | TeraBox upload pending (browser lane) |
| `~/workspace/eastern-mind/cda-*.wav` | 188MB | 3 CD audio tracks (WAV) | ✅ In wh_eastern_mind/soundtrack/ + GH | TeraBox staging |
| `~/workspace/eastern-mind/extract_dxr.py` | 12KB | Director 4 RIFX extractor | ✅ In lane dir | Reusable for other Director games |

## Changes 2026-10-15 (CN small-end pull lane)
- **PULLED+STORED** Camp Lazlo series bible: `Camp Lazlo Bible - Long.pdf` (43,326,081B) + `.epub` (17,277,267B) from IA `camp-lazlo-bible-long`, byte-verified, pushed to mhvnsnt/cn-gigaleak-camp-lazlo main. Local deleted.
- **SKIPPED** Gumball S2 Rigs: IA `Gumball S2 Rigs.zip` (685,983,662B) byte-identical to GitHub release asset in cn-gigaleak-gumball. Already held.
- **IN PROGRESS** cn-pull-smallend lane: staging at `~/workspace/cn-pull-smallend/`. Next: animaniacsleak (779MB).
- **PULLED+STORED** duck-dodgers_202610 new finds: `smiling-friends.zip` (748,767B) + `khsqgj.pdf` (7,830,039B) → cn-gigaleak-cartoon-vault main; `randycunning ham t.zip` (149,468,015B) → cartoon-vault release `randy-cunningham-v1`. All byte-verified. Local deleted.

## Changes 2026-10-15 (CN big-end pull lane — CLAIM)
- **CLAIMED by big-end lane** (do not duplicate): cow-chicken batch from IA `cow-chicken` (25.74GB mirror):
  - Gym Partner.zip (3.01GB) → mhvnsnt/cn-gigaleak-gym-partner [DARK SOURCE, HIGH PRIORITY]
  - Powerpuff Girls Original.zip (1.14GB) → mhvnsnt/cn-gigaleak-powerpuff-girls
  - Powerpuff Girls Special.zip (1.92GB) → mhvnsnt/cn-gigaleak-powerpuff-girls
  - PPGZ.zip (0.13GB) → mhvnsnt/cn-gigaleak-powerpuff-girls
  - Johnny Test.zip (1.42GB) → mhvnsnt/cn-gigaleak-cartoon-vault
  - DUCK DODGERS.zip (0.42GB) → check holdings first
  - Johnny Bravo.zip (0.19GB) → mhvnsnt/cn-gigaleak-johnny-bravo
  - Total ~8.2GB. SKIP: Scooby-Doo MI, EEN, KND, Dexter's, Robot Chicken, Space Ghost, Fosters (all complete).
- **CLAIMED by big-end lane**: regular-show_202610 (18.89GB) → mhvnsnt/cn-gigaleak-regular-show (NOT STARTED, fully missing)
- **IN PROGRESS** cn-pull-bigend lane: Adventure Time.zip (51.68GB from cartoon-network_20261014) chunking 7x8GB → mhvnsnt/cn-gigaleak-adventure-time release at-cnzip-20261015. Staging: `~/workspace/cn-pull-bigend/work-at/`. Sequential: cow-chicken batch queues after AT.zip, then Regular Show.
- **SKIPPED** (duplicate): gumball_leak (48.03GB) = same file as Cartoon Network.zip's Gumball.zip (44.74GB). Gap-fill only after Gumball lane completes.
- **PULLED+STORED** Animaniacs (182 files, 775MB, all byte-verified) from IA `animaniacsleak` → cn-gigaleak-cartoon-vault release `animaniacs-complete-v1` (752MB zip, MD5 af22b5e1df4ff1ebf3275a037f80ad6b). Local deleted.

## Changes 2026-10-15 (CN TorBox big-pull lane — CLAIM)
- **CLAIMED by torbox-big lane** (do not duplicate): Gym Partner gaps (123 files, 4.80GB) via TorBox torrent 119449922. All 123 confirmed in torrent. Extracting to `~/workspace/torbox-pull/gympartner-gaps/` → mhvnsnt/cn-gigaleak-my-gym-partner.
- **CLAIMED by torbox-big lane**: Regular Show full (2,999 files, 27.73GB) via TorBox. IA lane has NOT started RS (no releases in cn-gigaleak-regular-show). Manifest ready at /tmp/rs-torbox-manifest.txt. Will pull after Gym Partner completes (disk constraint).
- **NOT claimed (IA lane active)**: Adventure Time.zip (51.68GB) — IA big-end is pulling this. TorBox has 89GB of individual AT files but overlap risk; holding until IA completes or gap analysis done.

## Changes 2026-10-16 (STORE-EVERYTHING-THEN-CLEAN campaign, ~11:40-12:00 EDT)
- **DELETED** `game-reverse-engineering/street-fighter-3d-games/downloads/Street Fighter EX3 (USA).bin` (701MB) — byte-identical on GH (western-heart `sf-ex3-v1`, 701,813,280B uploaded) AND TeraBox (`/game-files/sfex3-usa-bin/` 14/14, sha256 059a9516…). Idle queue #2. Per relaxed game-files law.
- **UPLOADED to GH** (TeraBox pending): EX3 bin → `sf-ex3-v1` ✅ done; root.olk (662M) + mishima-dojo (257M) → `game-binaries-20261016` (in progress); EX Plus Alpha 7z (252M) → `sf-ex-plus-alpha-v1` (retrying); TEKKEN.psarc (4.5G) → `game-binaries-20261016` (splitting, proxy flapping).
- **STAGED for TeraBox**: `~/workspace/terabox-staging/game-re/` — full game-reverse-engineering → `/western-heart/teardowns/`, 25 batches + 9 oversized, ALL PENDING browser lane. Plan: `BATCH-PLAN.json`. Hard links (zero extra disk). DO NOT DELETE staging until TeraBox verifies.
- **TeraBox manifest**: `~/workspace/agent-ops/TERABOX-STORE-MANIFEST-20261016.md` — what's on TeraBox, what's staged, what still needs upload.
- **Disk**: 87% → 88% (transient, split parts) → target <75% after TeraBox batch + deletions.
- **Protected (do not touch)**: tekken6/ (active recon), hero-parts-pull, cn-pull-*, wmxix-iso (dolphin agent), terabox-staging/def-jam (resume), dxmmii-limbs, your_files, ep01-chronomap, tools/.
