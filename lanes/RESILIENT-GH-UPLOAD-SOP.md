# RESILIENT-GH-UPLOAD-SOP — stall-proof GitHub release uploads for lanes

**Problem (2026-10-20..22, recurring):** `gh release upload` does ONE HTTP POST per
asset with only 3 retries at a constant 200ms backoff and NO low-speed stall
detection (verified in cli/cli trunk `pkg/cmd/release/shared/upload.go`). Against
a congested egress proxy a stalled POST hangs indefinitely; when it finally dies,
the lane loses the whole file. The longtail lane lost `1981.zip`–`1985.zip`
repeatedly — "FAILED after 4 retries (TimeoutError)" — one ~400MB file at a time,
no resume. `gh` also uploads with 5-way concurrency and `--clobber` deletes the
old asset BEFORE re-uploading (lose-on-failed-retry).

**Standard tool:** `lanes/resilient-gh-upload.sh OWNER/REPO TAG FILE [--dry-run]`
(stdlib/bash only — lane-vendorable; no CloudDog import, since CloudDog's local
copy was removed by owner order 2026-10-21).

## What it does

1. **Splits** the file into exactly-100MB parts (`split -b 104857600 -d -a 4` →
   `{name}.0000`, `{name}.0001`, …). The 100MB single standard is the owner law;
   `RU_PART_SIZE` override exists for tests only — do not ship smaller parts
   without owner approval.
2. **Manifest** (`{name}.manifest.json`: `name`, `size`, `sha256` of the whole
   file, `part_size`, ordered `parts[]`, `tool`, `standard`) uploaded as its own
   asset **LAST** — a present manifest implies all parts landed. Schema matches
   CloudDog's 100MB-part convention so CloudDog can reabsorb lanes later.
3. **Per-part upload via curl** straight at
   `POST https://uploads.github.com/repos/OWNER/REPO/releases/RID/assets?name=…`
   (the same endpoint `gh` uses) with:
   - `-T` streaming (no RAM buffering of the part),
   - explicit `Content-Length` + `Content-Type: application/octet-stream`,
   - `--speed-limit 1000 --speed-time 60` → a stall aborts with exit **28**
     ("Operation too slow") instead of hanging for days,
   - `--connect-timeout 30 --max-time 1800`,
   - **sequential** parts (gh's 5-way concurrency is counterproductive through
     the struggling proxy).
4. **Bounded retry loop:** up to 8 attempts per part, backoff
   10→30→60→120→300→600→600s with ±25% jitter. Retries: curl 7/28/52/55/56,
   HTTP 5xx/429. **Aborts (no retry):** 401/403/404/422 and other curl errors.
5. **Idempotent resume:** parts already on the release with matching size are
   SKIPPED; size-mismatched parts are DELETE-then-reuploaded (gh-large-releases
   `delete_matching_assets` precedent). Worst case re-sends 100MB, never the
   whole file. Delete-before-retry applies ONLY to same-name part assets during
   retry — never to pre-existing whole-file assets.
6. **Verify:** per-part size (+ `digest` when the API returns it) from the 201
   response; final whole-manifest re-list of release assets.

## When to use it

Any lane uploading release assets bigger than ~50MB through this VM's egress.
`--dry-run` resolves the release and prints the plan without uploading.

## Tests

`lanes/tests/test-resilient-upload.sh` — 15 stubbed tests (no network):
split/manifest schema, stall→retry→success, idempotent skip, 401 aborts with
exactly 1 attempt, size-mismatch DELETE+reupload, final-verify. All green.

## Pattern credit

Naming (`{name}.{index:04d}`), manifest shape, and delete-then-reupload resume
adopt the **pattern** of ading2210/gh-large-releases — whose license was verified
as **LGPL-3.0**, so its code is NOT vendored (copyleft). Stall-kill semantics from
curl's documented `--speed-limit/--speed-time` (exit 28).
