# DISK AUDIT — 2026-10-16

**Disk:** 80% (78G/100G on /dev/mapper/rv). Owner target <69%.
**Auditor:** Subagent 900fbc16 (parent: main agent fa293ec0)
**Rule:** ONE-STORE RULE — verified 100% on GitHub OR TeraBox = may clear local. No deletions by auditor (research only).

---

## Summary Table

| # | Directory | Size | Backed Up? | Active Lane? | Verdict |
|---|-----------|------|------------|--------------|---------|
| 1 | cn-pull-bigend/ | 17G | PARTIAL (uploading) | YES — push-chunk1.py live | KEEP ON DISK |
| 2 | tools/ | 8.1G | UNKNOWN (not verified) | YES — actively used | NEEDS BACKUP FIRST |
| 3 | game-reverse-engineering/ | 5.5G | MIXED (see detail) | PARTIAL (tekken6-ps3 uploading) | MIXED — clear verified, keep active |
| 4 | cn-gigaleak-pull/ | 5.5G | PARTIAL (uploading) | YES — Johnny Test upload live | KEEP ON DISK (for now) |
| 5 | doa4-bass/ | 5.1G | NO (source parts on GH, ISO being built) | YES — DOA4 teardown agent | KEEP ON DISK |
| 6 | cn-pull-smallend/ | 4.6G | PARTIAL | YES — Gumball Flash upload live | KEEP ON DISK (for now) |
| 7 | tt-capejones/ | 4.5G | PARTIAL | YES — Teen Titans copy agent | KEEP ON DISK |
| 8 | cape-jones/ | 2.0G | YES (git repo, pushed) | YES — active work repo | KEEP ON DISK (active work) |
| 9 | dxmmii-limbs/ | 1.7G | YES (git repo, pushed) | NO — work complete | SAFE TO CLEAR |
| 10 | terabox-staging/ | 1.5G | NO (staging area) | YES — staging for uploads | KEEP ON DISK |

**Total audited:** ~54G
**Immediately clearable:** ~1.7G (dxmmii-limbs)
**Clearable after uploads verify:** ~8-10G (game-re verified subdirs, Johnny Test, Gumball Flash)

---

## Detailed Findings

### 1. ~/workspace/cn-pull-bigend/ (17G) — KEEP ON DISK

**Contents:** work-at/ with at-cnzip-000.bin (8.0G) + 17 split parts (500M each, aa-aq). Scripts: chunked_pull.py, push-chunk1.py.

**Backup status:** PARTIAL — uploading to GitHub release `at-cnzip-20261015` (mhvnsnt/cn-gigaleak-adventure-time). Parts aa-af verified on release, part_ag upload in flight as of audit.

**Active lane:** YES — checkpoint cn-pull-bigend-20261015.json = running. push-chunk1.py (pid 65762) actively uploading. Heartbeat 2026-10-16 18:36 CDT.

**Can work be done from remote?** NO — this IS the upload source. The 8GB .bin is being split and pushed. Clearing now would kill the lane.

**Verdict:** KEEP ON DISK. Re-audit after all parts verify on GitHub release, then clear per ONE-STORE RULE.

---

### 2. ~/workspace/tools/ (8.1G) — NEEDS BACKUP FIRST

**Contents:** 30+ tool directories. Largest:
- blender/ (1.3G) — Blender 4.0.2 install
- motion-graphics/ (519M)
- trackA-interpolation/ (494M), trackA-rigging/ (466M)
- body-replace/ (450M), tekken-decrypt/ (366M)
- Plus 25+ smaller tools (100-300M each)

**Backup status:** UNKNOWN — not verified. Per TOOLS-TO-STORE LAW (owner 2026-10-16): "Every tool gets pushed to the appropriate repo and/or TeraBox BEFORE it's disposed from disk."

**Active lane:** YES — tools are actively used by all lanes (blender for renders, tekken-decrypt for T6 work, etc.).

**Can work be done from remote?** PARTIAL — many tools are re-downloadable (blender, audacity) or already in repos. But re-downloading 8GB is wasteful; better to push to TeraBox once per TOOLS-TO-STORE LAW.

**Verdict:** NEEDS BACKUP FIRST. Recommend: push entire tools/ to TeraBox (one-time), then keep only actively-used tools local. Blender (1.3G) is essential — keep. Audit individual tools for repo placement.

---

### 3. ~/workspace/game-reverse-engineering/ (5.5G) — MIXED

**Contents:**
- street-fighter-3d-games/ (421M)
- tekken3/ (407M)
- tekken6-ps3/ (155M)
- western-heart-assets/ (126M)
- wwe2k/ (86M), wwf-no-mercy/ (48M)
- Plus docs, small dirs

**Backup status:**
- ✅ tekken3/ → GitHub `tekken3-ps1-v1` (NOT draft, published)
- ✅ street-fighter-3d-games/ → GitHub `sf-ex-plus-alpha-v1` (NOT draft, published)
- ⏳ tekken6-ps3/ → GitHub `tekken6-ps3-full-v1` (DRAFT, upload in flight)
- ❓ western-heart-assets/, wwe2k/, wwf-no-mercy/ — not verified

**Active lane:** PARTIAL — tekken6-ps3 upload is live. Others: no active teardown (per background, these were verified 2026-10-16).

**Verdict:**
- **SAFE TO CLEAR:** tekken3/ (407M), street-fighter-3d-games/ (421M) — both 100% on GitHub, no active work. Log to disk-cleanup-log.md, log to TEARDOWN-IDLE-QUEUE.md if teardown <100%.
- **KEEP:** tekken6-ps3/ (155M) — upload in flight, do not touch.
- **NEEDS VERIFICATION:** western-heart-assets/, wwe2k/, wwf-no-mercy/ — verify GitHub backup before clearing.
- **Potential savings:** ~828M immediately clearable.

---

### 4. ~/workspace/cn-gigaleak-pull/ (5.5G) — KEEP ON DISK (for now)

**Contents:**
- staging/ (4.0G) — johnny-test/ with Johnny Test.zip
- terabox-staging/ (1.6G)

**Backup status:** PARTIAL — Johnny Test.zip download COMPLETE (1,415,713,110 bytes, md5 verified vs IA). Upload to GitHub `johnny-test-cowchicken-v1` (mhvnsnt/cn-gigaleak-johnny-test) STARTED, in flight as of 18:34 CDT.

**Active lane:** YES — checkpoint cn-gigaleak-archiveorg-pull.json = running. Upload chain live.

**Verdict:** KEEP ON DISK until GitHub upload verifies, then clear per ONE-STORE RULE. Re-audit in ~1 hour.

---

### 5. ~/workspace/doa4-bass/ (5.1G) — KEEP ON DISK

**Contents:** doa4.iso (3.0G, growing) + parts/ (1.2G). DOA4 ISO being reassembled from 30 GitHub release parts.

**Backup status:** NO (local build) — source parts are on GitHub `doa4-iso-v1` (mhvnsnt/western-heart), but the assembled ISO is local-only until teardown extracts what we need.

**Active lane:** YES — DOA4 teardown agent (ff88ba0f) actively downloading. Checkpoint doa4-teardown.json = running, attempts 5.

**Verdict:** KEEP ON DISK. This is the #1 priority lane (Bass Armstrong for Vain Abel). Do not touch.

---

### 6. ~/workspace/cn-pull-smallend/ (4.6G) — KEEP ON DISK (for now)

**Contents:**
- at-2015/ (2.8G) — Adventure Time 2015 assets
- Gumball Flash.rar (1.9G)

**Backup status:**
- Gumball Flash.rar: md5 byte-perfect vs archive.org. Upload to `gumball-flash-v1` (DRAFT) in flight.
- at-2015/: 664/675 files per background; backup status not fully verified.

**Active lane:** YES — Gumball Flash upload live (attempt 4).

**Verdict:** KEEP ON DISK until uploads verify. Gumball Flash.rar clearable after `gumball-flash-v1` verifies (and draft is finalized).

---

### 7. ~/workspace/tt-capejones/ (4.5G) — KEEP ON DISK

**Contents:**
- cape-jones/ (2.1G)
- extracted/ (1.1G)
- TEEN TITANS.zip (702M)
- tt100m-aa through ah (8×100M parts)

**Backup status:** PARTIAL — Teen Titans releases exist (`teen-titans-complete-v1` published, `teen-titans-cowchicken-v1` draft). Local is a copy lane.

**Active lane:** YES — Teen Titans copy agent (9d61b444) per parent task.

**Verdict:** KEEP ON DISK. Active copy lane. Re-audit after lane completes.

---

### 8. ~/workspace/cape-jones/ (2.0G) — KEEP ON DISK (active work)

**Contents:** Git repo. production/ (724M), assets/ (117M), docs/, 3d-assets/, etc.

**Backup status:** YES — git repo, latest commit 9705d75c (Merge PR #47), pushed to mhvnsnt/cape-jones.

**Active lane:** YES — this is the owner's active Cape Jones project repo. Working files.

**Can work be done from remote?** YES technically (clone when needed), but this is an ACTIVE WORK REPO — the owner works in it constantly.

**Verdict:** KEEP ON DISK. Active work files per ONLY-KEEP-ESSENTIALS-LOCAL LAW. The 724M production/ should be audited for GitHub push (MEDIA-TO-REPO LAW).

---

### 9. ~/workspace/dxmmii-limbs/ (1.7G) — SAFE TO CLEAR

**Contents:** Git repo. viz/ (627M), blend/ (398M), renders/ (31M), scripts/, BUILD.md, etc.

**Backup status:** YES — git repo, latest commit b3861de ("QC render outputs 2026-10-16"), pushed. Per background: "dxmmii-rig-worker marked done (successor lanes)."

**Active lane:** NO — work is complete. No active checkpoint.

**Can work be done from remote?** YES — clone from GitHub when needed.

**Verdict:** SAFE TO CLEAR (~1.7G). Work is done, committed, pushed. This is the cleanest immediate win. Disc-cleaner can clear this now per ONE-STORE RULE.

---

### 10. ~/workspace/terabox-staging/ (1.5G) — KEEP ON DISK

**Contents:**
- def-jam/ (1.4G) — Def Jam FFNY ISO (SLUS_210.04)
- game-re/ (1.3G) — game-re batch staging
- game-binaries/ (62M), plus small dirs

**Backup status:** NO — this is a STAGING area for uploads. Def Jam ISO is NOT on GitHub (no def-jam release on mhvnsnt/wrestling-game). **GAME FILE — NEVER-DELETE-GAME-FILES LAW applies.**

**Active lane:** YES — staging for TeraBox upload lanes.

**Verdict:** KEEP ON DISK. Def Jam ISO needs TeraBox upload before any action. Staging dirs are active.

---

## Priority Actions for Disc-Cleaner

### Immediate (safe now):
1. **dxmmii-limbs/ (1.7G)** — work done, pushed. Clear now.
2. **game-reverse-engineering/tekken3/ (407M)** — on GitHub, no active work. Clear per ONE-STORE RULE.
3. **game-reverse-engineering/street-fighter-3d-games/ (421M)** — on GitHub, no active work. Clear per ONE-STORE RULE.
   - **Immediate total: ~2.5G**

### After uploads verify (re-audit in 1-2 hours):
4. **cn-gigaleak-pull/staging/johnny-test/** — clear after `johnny-test-cowchicken-v1` verifies (~1.4G)
5. **cn-pull-smallend/Gumball Flash.rar** — clear after `gumball-flash-v1` verifies (~1.9G)
6. **cn-pull-bigend/work-at/** — clear after all parts verify on `at-cnzip-20261015` (~17G — the big one)
   - **Potential total: ~20G**

### Needs work before clearing:
7. **tools/ (8.1G)** — push to TeraBox per TOOLS-TO-STORE LAW, then clear non-essentials
8. **terabox-staging/def-jam/ (1.4G)** — upload ISO to TeraBox first (GAME FILE, never auto-delete)

### Do not touch:
- doa4-bass/ (active teardown, #1 priority)
- tt-capejones/ (active copy lane)
- cape-jones/ (active work repo)
- game-reverse-engineering/tekken6-ps3/ (upload in flight)

---

## Notes
- Did NOT duplicate disc-cleaner agent work — this is audit only, no deletions.
- All GitHub release checks done via `gh release view` (live, 2026-10-16).
- TeraBox backup status not verified (no API creds) — assumed NOT backed up unless GitHub confirmed.
- Re-audit recommended after the in-flight uploads complete (~1-2 hours).
