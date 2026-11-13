# Release upload at the 100 MB standard — tested wrapper

- **Date:** 2026-11-12 ~22:15–22:30 CST (continuous-friction-research pass)
- **Index:** [[RESEARCH-PULLIN-INDEX]] (entry to be added by the merge lane)
- **Status:** researched (prior passes) + wrapper script TESTED end-to-end
  this pass; adoption by lanes is queued, not done here.
- **Dedupe:** no re-research. The 100 MB standard was decided 2026-10-20
  (CloudDog PR #44); the 408 failure mode 2026-11-06; the `starter` trap
  2026-10-31; resumable download 2026-11-09. What was missing was a
  single tested script that *enforces* the standard instead of documenting
  it. This pass built and proved that script.

## TL;DR

Lanes keep uploading 1.9 GB parts (`store2.sh`/`chunker.py` hardcode
`PART=1900000000`) despite the owner 100 MB standard. Tonight the wgpl
mirror lane's 1.99 GB `part00` upload stalled ~24 min behind the egress
proxy with no progress, and the disk sits at 80% (119G/150G) with the
~2 GB source + ~1.95 GB staging parts un-clearable until verification
completes. The wrapper in this dir (`gh-release-upload-100mb.sh`) splits
at 100 MB, checks per-part asset state (never size-only), deletes `starter`
placeholders before retry, retries uploads, and verifies each part by
state + size + full re-download sha256. Tested live this pass on a 120 MB
file → 2 parts, both verified, exit 0, ~5 min total.

## 1. The problem tonight

- Disk: 119G/150G (80%) at 22:12 CST, up from 74% at 19:12. Top consumers
  are all active Nov 9–12 work; nothing verified 100% on a store, so per
  the ONE-STORE RULE nothing moves (guardian logs, 2026-11-12 19:12–21:44).
- wgpl mirror lane: `gh release upload` of `wgpl.tar.part00` (1.99 GB,
  sha256 `f73e71c2…`) stalled after retrying; connection ESTAB via the
  egress proxy, no progress for minutes (guardian 21:44 CST). Read-only
  check this pass: the release `wizard-gang-part-libraries-20261112`
  (mhvnsnt/clouddog-storage) now holds `part01` (`uploaded`, 39,731,200 B)
  + `MANIFEST.sha256`; `part00` is absent — the stalled 1.9 GB POST left
  no trace (not even a `starter`). The lane evidently moved on; the
  1.99 GB part was never verified.
- The pattern repeats because the tooling does not enforce the standard:
  `store2.sh`/`chunker.py` hardcode 1.9 GB parts and bare `--clobber`
  with no retry (2026-11-06 finding, never fixed at the source).

## 2. The wrapper (`gh-release-upload-100mb.sh`, this dir)

Stdlib + `gh` CLI only. Per part (`<basename>.part00`, `.part01`, …):

1. Preflight: `gh auth`, file exists, release exists (caller creates it;
   the script never auto-creates a release).
2. Split at `--part-mb` (default 100) with `split`; per-part sha256
   manifest kept at `<file>.parts/MANIFEST.sha256`.
3. State check via `gh api` (state + size): `uploaded` at the expected
   size → skip (idempotent re-run); `starter` → `gh release delete-asset
   -y` then re-upload; any other unexpected state → refuse to clobber,
   flag for investigation.
4. Upload with 3 attempts, 15/30/45 s backoff (`gh` has no retry; the
   loop is the retry).
5. Verify: re-query state=`uploaded` + size, then full re-download of
   the part and sha256 compare. A part is not done until the hash
   matches after pull-back (owner 2026-10-20 full-verify decision).
6. Parts removed after verification; manifest kept.

## 3. Live test this pass

- Scratch release `friction-test-20261112` in `mhvnsnt/agent-ops`
  (created for the test, deleted after — see §4).
- Test file `upload-test-120mb.bin`, 120,000,000 bytes, sha256
  `2ea021ad…dc0535`.
- Run log: `upload-test-run.log` (this dir). Result:
  - `split 120000000 bytes into 2 part(s) of 100M`
  - `VERIFIED upload-test-120mb.bin.part00 state=uploaded size=104857600 sha256 match`
  - `VERIFIED upload-test-120mb.bin.part01 state=uploaded size=15142400 sha256 match`
  - `ALL PARTS DONE` — wrapper exit 0, ~5 min total (upload + re-download
    verify through the egress proxy).
- The `starter`-delete path was NOT live-proven (no starter existed to
  delete); it follows the 2026-10-31 documented `delete-asset` flow and
  is code-reviewed only. The skip-if-uploaded path was not live-proven
  either (fresh release); both are small, well-understood branches.
- `bash -n` clean on both scripts in this dir.

## 4. Cleanup (this pass)

- Scratch release `friction-test-20261112` deleted via
  `gh release delete` after the test (assets + tag removed).
- Local test file `upload-test-120mb.bin` (120 MB) and its `.parts/`
  dir deleted after verification. Kept as evidence in this dir:
  `upload-test-run.log`, `upload-test-120mb.sha256`,
  `upload-test-MANIFEST.sha256` (part hashes).
- Nothing else touched: the wgpl lane's stalled upload was observed
  read-only, never killed, restarted, or re-uploaded (NEVER-KILL-IN-PROGRESS).

## 5. Recommended (lane owners apply)

1. **Adopt the wrapper** (or its pattern) in every lane that uploads
   release assets: `store2.sh`/`chunker.py` and the gumball/wgpl mirror
   lanes should split at 100 MB and verify by state+hash. The 1.9 GB
   chunk size is the bug; the wrapper is the fix.
2. **Retire `PART=1900000000`** at the source — grep the repos for the
   hardcoded value and replace with the 100 MB standard.
3. **GHA runner upload path** (queued since 2026-11-06, prototype in
   `torbox-gha-prototype/`, never run end-to-end): still blocked on a
   fine-grained PAT mint (browser step). Note this pass: GitHub API core
   rate limit is healthy (4928/5000 at ~22:20 CST) — the limit is not the
   blocker; the PAT is.
4. Disk stays at 80% until the wgpl parts verify; nothing to clear until
   then (ONE-STORE RULE). The dedup pilot (2026-11-09, 18.32 GB
   hash-confirmed recoverable, jdupes method proven) remains the only
   quantified relief valve, still awaiting owner go-ahead for a wider
   link pass.

## 6. Blocked / not done here

- No lane script modified (`store2.sh`/`chunker.py`/mirror lanes are live;
  owners adopt the wrapper).
- No in-flight upload touched (wgpl part00 observed only).
- No GHA upload workflow run (PAT mint is a browser step).
- No disk freed by this pass (freed_bytes 0 by design — nothing verified
  100% yet).
