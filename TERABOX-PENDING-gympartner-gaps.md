# TeraBox-pending: torbox-pull gym-partner gaps (2026-10-16)

BLOCKER: TeraBox API uploader (~/workspace/tools/terabox-uploader/tbupload.py) has NO
credentials (.creds.json missing) as of 2026-10-16 ~14:50 EDT. Session keeper restoring
separately. DO NOT re-run uploads until creds verified via `tbupload.py resolve`.

## What is GitHub-done (awaiting TeraBox mirror)
GitHub release: mhvnsnt/cn-gigaleak-my-gym-partner / tag `gym-partner-gaps-torbox-v1`
(title: "Gym Partner gap files (TorBox batch, 46/123)")

| Asset | Size (bytes) | SHA256 |
|---|---|---|
| gym-partner-gaps-torbox-v1.tar.gz | 315079542 | 957ddb6ef25317d3728f8ed12973e8280ba7b9dbdd0e7996f59ca6727548f548 |
| MANIFEST-gym-partner-gaps-torbox-v1.txt | (per-file list, 46 rows) | — |

Tarball contents: `gympartner-gaps/` = 46 files, 576,225,384 bytes total
(Document/Gym Partner/Gym Partner/Backgrounds: 1 .ai, 4 .eps, 23 .jpg, 18 .psd).
Pulled 2026-10-15 from TorBox cached torrent 119449922 (350GB CN gigaleak Documents zip),
46/122 of the 123-wanted gap list (gympartner-manifest.txt).
Per-file manifest (sha256, size, path) is in the release MANIFEST asset and at
/tmp/gym-gaps-manifest.txt (ephemeral — re-derive from release if needed).

Local source: DELETED 2026-10-16 ~16:00 EDT after byte-identical GitHub verify, per owner sharpened directive
  (GitHub 100% + verified = sufficient for non-game files; TeraBox not required before delete).
  Re-create from the GitHub release asset if a TeraBox mirror is wanted later.

## Target TeraBox paths (convention: bulk store /CN-Gigaleak/<show>/, capitalized)
  /CN-Gigaleak/gym-partner/gym-partner-gaps-torbox-v1.tar.gz
  /CN-Gigaleak/gym-partner/MANIFEST-gym-partner-gaps-torbox-v1.txt

## Verify steps once creds restored
1. `tbupload.py upload <tarball> /CN-Gigaleak/gym-partner/` (re-create tarball from
   local gympartner-gaps/ + /tmp manifest, or download from GitHub release asset)
2. `tbupload.py ls /CN-Gigaleak/gym-partner/` — confirm name + byte size match
3. Only then: delete local ~/workspace/torbox-pull/gympartner-gaps/ and log it.

## Not part of this batch (left local, lane-owned)
- ~/workspace/torbox-pull/gympartner-manifest.txt (123-wanted list — TorBox lane resumes from it)
- ~/workspace/torbox-pull/rs-manifest.txt (2999 Regular Show entries — RS lane's)
- ~/workspace/torbox-pull/*.log (lane evidence)
- 76 remaining Gym Partner gaps: NOT pulled (TorBox CDN degraded; lane parked per
  checkpoint cn-pull-torbox-big-20261015.json — parent may relaunch)
