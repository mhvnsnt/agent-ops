# DEF JAM: FIGHT FOR NY — TeraBox Upload Handoff

**For: parent agent / browser-lane worker (subagents cannot use the browser)**
**Written:** 2026-10-14 ~20:40 EDT by worker `wh-defjam-100` (checkpoint: `~/workspace/agent-ops/checkpoints/wh-defjam-100.json`)

---

## 1. What needs uploading

| Item | Value |
|---|---|
| **File** | `SLUS_210.04.Def Jam - Fight for NY.iso` |
| **Local path** | `/home/hatch/workspace/terabox-staging/def-jam/SLUS_210.04.Def Jam - Fight for NY.iso` |
| **Full size (expected)** | **4,694,573,056 bytes** (4.47 GB) |
| **Source** | Archive.org item `slus-210.04.-def-jam-fight-for-ny`, file `SLUS_210.04.Def Jam - Fight for NY.iso` |
| **TeraBox destination** | `/western-heart/defjam/SLUS_210.04.Def Jam - Fight for NY.iso` |
| **SHA note** | No published checksum on the archive.org item; verify by exact byte size 4,694,573,056 after download. |

## 2. Download status (as of 2026-10-14 20:40 EDT)

- **Partial on disk:** 516,710,400 bytes (~11.0%) at the local path above.
- **Download PAUSED, not failed.** Resume-capable server confirmed (`Accept-Ranges: bytes`; 1 MB range test OK).
- **Why paused:** VM disk hit **92%** (owner HARD CEILING is 88%, popup at 90%) during the pull — other lanes were filling disk concurrently. Worker stopped its curl to stop contributing.
- **To resume** (only when disk is safely below 80%):
  ```bash
  cd ~/workspace/terabox-staging/def-jam
  curl -L -C - --retry 5 --retry-delay 15 --retry-all-errors \
    -o "SLUS_210.04.Def Jam - Fight for NY.iso" \
    "https://archive.org/download/slus-210.04.-def-jam-fight-for-ny/SLUS_210.04.Def%20Jam%20-%20Fight%20for%20NY.iso"
  ```
  (`-C -` resumes the 516MB partial — never restart from zero. Verified working.)

## 3. Verification steps after download completes

1. `stat -c%s "SLUS_210.04.Def Jam - Fight for NY.iso"` must print `4694573056`.
2. Sanity: first bytes of a PS2 ISO contain a system descriptor (check with `file` or `isoinfo` if available).
3. **NEVER-DELETE-GAME-FILES LAW:** do NOT delete the ISO — not for disk space, not after GitHub. It stays until it is **verified on TeraBox AND the owner confirms**. If disk pressure demands action, upload first, verify, report, WAIT for owner go-ahead.

## 4. TeraBox upload (browser lane)

1. Open TeraBox (owner's account, Google login via fmmg.mars@gmail.com — already signed in per owner 2026-10-12).
2. Navigate to / create folder `/western-heart/defjam/`.
3. Upload the verified ISO from the local path above.
4. Confirm the uploaded file size reads 4,694,573,056 bytes in TeraBox.
5. Report back: uploaded (Y/N), TeraBox size match, link/expiry if shared.

## 5. Context

- Teardown is 100% COMPLETE (surgical range extraction): models+data in `mhvnsnt/wrestling-game/teardown/def-jam-fight-for-ny/` (PR #2 merged); animation/grappling findings in `mhvnsnt/western-heart/teardown/def-jam-fight-for-ny/ANIMATION-FINDINGS.md` (PR #68 merged). This ISO is the **full-disc archival copy** for TeraBox per the all-night teardown push.
- Rename map: `~/workspace/game-reverse-engineering/RENAME-MAP.md` (Def Jam section added 2026-10-14; WH names owner-assigned, currently none assigned — files not yet renamed).
