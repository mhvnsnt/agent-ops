# 01 — Large GitHub release-asset uploads dying on ~12-minute connection resets (curl rc 56)

**Date:** 2026-11-27 (research pass 22:08–22:30 CST)
**Problem class:** resilient transfer / upload resets — follow-up to [[FRICTION-RESEARCH-2026-10-19]] cluster 1 (`research-friction-20261019/01-resilient-transfer.md`), which already decided the 100 MB chunk quantum and the stdlib-retry pattern. This pass answers the narrower question the Nov 27 arcade mirror lane raised: *why do ~2 GB parts die at ~12 min, and what exactly do `gh` vs `curl` do differently?*
**Status:** research only. No lane touched, no upload run, nothing deleted. Wire-up is queued for the CloudDog / arcade-mirror integration lane (same owner as the Oct 19 queue items 1–7).

## 1. Problem statement + log evidence

Per the lane brief (Nov 27 2026, arcade mirror lane — Pokken part-01, DX part-00):

| Attempt | Part | Result | Elapsed | Note |
|---|---|---|---|---|
| 1–3 | Pokken part-01 (~2 GB) | curl exit 56, `Recv failure: Connection reset by peer` | ~12.4 / 11.9 / 12.3 min | 3 consecutive failures, same signature |
| 1–3 | DX part-00 (~2 GB) | curl exit 56 | ~12.3 min, one attempt ~20.6 min | 3 consecutive failures |
| — | same lane's part-00 | `gh` CLI upload path | landed | PULLBACK-OK, sha matched |

That is 6/6 curl failures on 2 GB parts vs 1/1 `gh` success on a part — a pattern, not a flake. Two nuances that matter for the diagnosis:

- **The reset time is a mode, not a hard wall.** Five of six failures cluster at 11.9–12.4 min, but one attempt survived to ~20.6 min before resetting. A hard 12-minute middlebox cutoff would not allow a 20.6-minute attempt. The shape is a *stochastic* reset whose hazard rises around ~12 min (consistent with an egress-proxy / load-balancer connection-lifetime or idle-timeout policy, or GitHub-side upload-connection handling) — not a deterministic timer. This is a hypothesis, not a verified cause: no proxy logs were available to this pass.
- **Historical corroboration in `disk-cleanup-log.md`:** the same signature predates Nov 27. Gumball Flash.rar (1.94 GB): 500 MB parts failed 3 attempts each with "connection reset/hung"; the lane fell back to chunked strategy. The Oct 19 research already recorded "uploads >485 MB ALL failed; 100 MB-via-curl is the proven working size". The Nov 27 incident is the same failure at the same size class — the arcade lane is evidently still splitting at ~2 GB instead of the decided 100 MB quantum (shop standard decided 2026-10-20, landed PR #44: 100 MB chunk quantum for store()/mirror).

**Throughput observed:** ~2 GB / 12 min ≈ **2.8 MB/s**. (For reference, other lanes have seen ~1.2 MB/s, e.g. the Scooby-Doo pull-back noted in the disk-cleanup log — the link is slow *and* variable, so sizing must survive the slow end, not the average.)

## 2. What the live sources actually say

### 2.1 The GitHub release-asset upload API has no resume

GitHub's own REST docs for "Upload a release asset" (`POST /repos/{owner}/{repo}/releases/{release_id}/assets`, via the release's `upload_url` on `uploads.github.com`):

- "GitHub expects the asset data in its raw binary form… You will send the raw binary content of the asset as the request body."
- "Most libraries will set the required `Content-Length` header automatically."
- No `Content-Range`, no chunk/session parameter, no `Accept-Ranges` on upload anywhere in the endpoint docs. The only failure note is: "When an upstream failure occurs, you will receive a `502 Bad Gateway` status. This may leave an empty asset with a state of `starter`. It can be safely deleted."
- Same filename re-upload → `422`; the old asset must be deleted first.

Source: https://docs.github.com/en/rest/releases/assets#upload-a-release-asset (crawled 2026-11-13).

**Consequence:** a mid-transfer reset (rc 56) discards everything already sent. There is no byte-offset resume to invoke — `curl -C -` / `Range` resume is a *download* mechanism and does not apply to this POST. The only "resume" available is at the *part* level: re-upload a whole part that is small enough to usually complete. This is exactly the 100 MB + per-part sha256 + manifest design the Oct 19 research already adopted (its tus-shaped pattern without the tus protocol).

### 2.2 `gh release upload` does NOT retry and does NOT resume

Verified against live sources, three ways:

1. **The manual lists no retry/resume flag.** `gh release upload <tag> <files>...` has exactly one flag, `--clobber` — and the manual warns: "When using `--clobber`, existing assets are deleted before new assets are uploaded. If the upload fails, the original assets will be lost." No `--retry`, no `--resume`, no `--concurrency` flag. Source: https://cli.github.com/manual/gh_release_upload
2. **The code uploads whole files, concurrently across files — not chunks within a file.** `pkg/cmd/release/shared` exposes `ConcurrentUpload(httpClient, hostname, uploadURL, numWorkers, assets []*AssetForUpload)` — the parallelism is *N files at once*, and `UploadOptions.Concurrency` is documented as "maximum number of simultaneous uploads". Nothing in the shared package splits one asset into resumable chunks. Source: https://pkg.go.dev/github.com/cli/cli/v2/pkg/cmd/release/shared and https://pkg.go.dev/github.com/ungtb10d/cli/v2/pkg/cmd/release/upload
3. **The Oct 19 cluster-1 finding stands:** "`gh` CLI does NOT retry transient failures (no `--retry` flag; go-gh single-attempt client)."

**License:** MIT (Copyright (c) 2019 GitHub Inc.). Source: https://pkg.go.dev/github.com/cli/cli/v2@v2.88.0/pkg/cmd/release/shared?tab=licenses ; local `gh` is v2.102.0 (2026-09-30), verified live this pass via `gh --version`.

### 2.3 What `gh` does differently from raw curl — and what it does not

| Aspect | `gh release upload` | raw `curl` POST to `uploads.github.com` |
|---|---|---|
| Endpoint / body | Single POST of raw file bytes to the release `upload_url`, `Content-Length` set | Same endpoint, same single POST, same raw body (when the lane uses `--data-binary @file` / `-T`) |
| HTTP version | Go `net/http` — HTTP/2 negotiated by default over TLS | Local curl 8.5.0 ships nghttp2 1.59.0; HTTP/2 also negotiated by default |
| Streaming | Streams from the open file | Streams from the file with `-T` / `--data-binary` (does not load it into memory) |
| Retry on rc 56 | **None** — single attempt, exit 1 | **None by default** — rc 56 is *not* in curl's default transient-retry set; needs `--retry-all-errors` |
| Resume | None (API offers none) | None (API offers none; `-C -` is download-only) |
| Keepalive | Go transport keepalives | TCP keepalive on by default; `--keepalive-time` only tunes *idle* probes |
| Failure artifact | A failed upload can leave a `starter`-state empty asset (per GitHub docs) | Identical — same server-side behaviour |

**Honest conclusion on the Nov 27 contrast (curl 0/6, gh 1/1): the docs give no mechanism by which `gh` would be inherently more resilient to a mid-transfer reset.** Both make the same single-shot POST. The single `gh` success is one sample and is equally consistent with "a fresh attempt at a lucky time" (recall one curl attempt survived 20.6 min — the reset is stochastic). Do **not** conclude "`gh` fixes it" and keep pushing 2 GB parts through `gh`. The fix is part size + per-part retry, not tool choice. What `gh` *is* good for: it resolves the release and builds the correct `upload_url` + auth + content-type in one command, so it remains the recommended *transport* for each 100 MB part — just never for a 2 GB part.

One real `gh` hazard to keep: `--clobber` deletes the existing asset *before* the new upload, so a failed `--clobber` re-upload destroys a good asset. Lanes must check-then-upload (skip if an asset with the same name/size/sha256 digest already exists) and delete-then-retry only the failed part — never `--clobber` a part that already verified.

### 2.4 curl flags, assessed one by one (local curl 8.5.0, verified live)

Sources: https://curl.se/docs/manpage.html ; https://curl.se/cvssource/docs/options-in-versions (`--retry-all-errors` 7.71.0, `--retry-connrefused` 7.52.0, `--retry` 7.12.3, `--keepalive-time` 7.18.0, `--speed-limit`/`--speed-time` 4.7).

- `--retry 5 --retry-all-errors` — **PULL IN (as part of the wrapper, §4).** curl's default retry set covers HTTP 408/429/500/502/503/504 + some connection failures; a mid-body reset (rc 56) is *not* retried by default. `--retry-all-errors` (7.71.0+) broadens it to transient errors including resets. Local curl 8.5.0 supports it. Cost: each retry restarts the part from byte zero — at 100 MB / 2.8 MB/s that is ~36 s, acceptable; at 2 GB it is ~12 min per retry, which is why this flag alone never fixes the 2 GB case. Curl's own docs warn `--retry-all-errors` is "the sledgehammer" and can duplicate non-idempotent requests — here the POST is not idempotent (same-name re-upload → 422; possible `starter` partial), so the retry must live inside an idempotent wrapper (check → delete-stale → upload → verify), not as a bare curl flag.
- `--retry-connrefused` — **include, harmless.** Covers rc 7 at connect time; irrelevant to a mid-transfer rc 56 but costs nothing.
- `--retry-delay 10 --retry-max-time 900` — **include.** Bounds the retry storm; exponential backoff is curl's default between retries, `--retry-delay` sets the floor.
- `--speed-limit 100000 --speed-time 60` — **PULL IN as fail-fast.** Aborts (exit 28) if throughput stays under ~100 KB/s for 60 s, turning a hung-but-not-dead transfer into a retryable failure instead of a silent stall past the reset window. It does not prevent resets and does not resume anything.
- `--keepalive-time 20` — **SKIP as a fix (harmless to set).** TCP keepalive probes fire only after the connection has been *idle* for the interval (default 60 s); during an active upload the connection is never idle, so no probe is ever sent mid-transfer. It cannot prevent a reset that lands while bytes are flowing. The Oct 19 research already mapped this correctly.
- `--http1.1` (force HTTP/1.1 instead of HTTP/2) — **EXPERIMENT ONLY, do not adopt on theory.** Some guides suggest it for rc 56 (a proxy/LB mishandling an H2 stream is a real failure class). Counter-evidence in our own data: `gh` (Go, HTTP/2 by default) *succeeded* where curl (HTTP/2 by default) failed, which weakens the "HTTP/2 is the cause" hypothesis. Correct test: A/B one 100 MB part with `--http1.1` vs default, same hour, several repetitions; adopt only on a measured difference.
- `--max-time` — **include per part.** A per-attempt ceiling (e.g. 600 s for a 100 MB part) bounds a hung transfer. Never set a single `--max-time` for a whole 2 GB upload — that just re-creates the wall.
- `-C -` / `--continue-at` — **DOES NOT APPLY.** Download resume; the upload endpoint accepts no `Range`/`Content-Range`. Any lane passing `-C -` on an upload is cargo-culting.

## 3. Quantification — what part size survives the reset window

Computed live this pass (python3, from the observed ~2.8 MB/s; 1 MB = 10⁶ B, 2 GB ≈ 2,048 MB):

| Part size | Time per attempt @ 2.8 MB/s | Time per attempt @ 1.2 MB/s (slow end seen on other lanes) | Verdict |
|---|---|---|---|
| 25 MB | 9 s | 21 s | overkill; 4× the API calls of 100 MB for no benefit |
| 50 MB | 18 s | 42 s | fine, but 2× the calls of 100 MB |
| **100 MB** | **36 s** | **83 s** | **recommended — the decided standard** |
| 128 MiB | 46 s | 112 s | fine, no reason to deviate from 100 MB |
| 200 MB | 71 s (1.2 min) | 167 s (2.8 min) | would also survive, but re-deciding gains nothing |
| 256 MB | 91 s (1.5 min) | 213 s (3.6 min) | survivable, still 4× the exposure of 100 MB |
| 500 MB | 179 s (3.0 min) | 417 s (7.0 min) | **no** — already failed 3× each at this size (Gumball, Oct) |
| 1 GB | 366 s (6.1 min) | 853 s (14.2 min) | **no** — exceeds the ~12 min mode at the slow end |
| 2 GB | 731 s (12.2 min) | 1,707 s (28 min) | **no** — attempt duration ≈ reset mode; expected failure |

Failure-cost math (illustrative Poisson model: reset hazard with mean ~12–20 min; a 2 GB attempt lasting 12.2 min has failure probability on the order of ½–⅔, matching 3/3 failures being plausible but not certain):

- **2 GB part, 3 attempts:** ~36.6 min of transfer, **0 bytes kept** — every retry restarts from zero.
- **100 MB part, 3 attempts worst case:** ~1.8 min; a single part failing costs ~36 s + backoff. A full 2 GB file = 21 × 100 MB parts, ~11.9 min sequential at 2.8 MB/s; one failed part costs 36 s, not 12 min.
- **Margin:** at the observed reset mode (~714 s / 11.9 min), a 100 MB attempt uses ~5% of the window at 2.8 MB/s and ~12% at 1.2 MB/s. Even a 10× slowdown (0.28 MB/s) still completes a 100 MB part in ~6 min — inside the window. That is the safety case for keeping 100 MB rather than raising it.

**Recommendation (exact): chunk 100 MB (100,000,000 B — the decided quantum, do not re-decide), per-part retry up to 5 attempts, exponential backoff 10 s → 120 s with jitter, per-attempt `--max-time 600`, skip-if-verified, delete-`starter`-then-retry. Parallelism: sequential or at most 2 concurrent part uploads — the 2.8 MB/s looks like an uplink/proxy cap, so parallel uploads will not multiply throughput and may trip the reset sooner; measure before raising concurrency.**

## 4. Candidate table

| # | Candidate | Source | License | Verdict | Why (honest) |
|---|---|---|---|---|---|
| A | **Enforce the 100 MB standard on the arcade lane + per-part retry loop (stdlib glue, no new dep)** | Shop standard decided 2026-10-20 (PR #44); pattern in `research-friction-20261019/01-resilient-transfer.md` §W2–W3 | n/a (own code) | **PULL IN — the fix** | Only candidate that changes the failure math: attempts drop from ~12 min to ~36 s, inside the reset window with 20× margin. Proven working size (100 MB-via-curl, mirror mode). Cost is a lane change, not a tool. |
| B | **`gh` CLI as the only upload path (vs raw curl)** | https://cli.github.com/manual/gh_release_upload ; https://pkg.go.dev/github.com/cli/cli/v2/pkg/cmd/release/shared ; https://docs.github.com/en/rest/releases/assets | MIT | **PULL IN as transport, SKIP as a fix** | Use `gh release upload` per 100 MB part (it builds the right URL/auth). Do not claim it retries or resumes — it does neither, and the manual + source prove it. The Nov 27 gh success is one sample with no supporting mechanism. Never `--clobber` a verified part. |
| C | **rclone as a GitHub-releases uploader** | Backend list: https://en.wikipedia.org/wiki/Rclone ; v1.76.0 release notes (new backends Dosya, Infomaniak kDrive — no GitHub): https://forum.rclone.org/t/rclone-release-v1-76-0/54456 | MIT | **SKIP (re-verified live)** | No GitHub backend exists in rclone (confirmed again against the current backend list and the 2026-11-06 v1.76.0 release notes). The Oct 19 finding stands. rclone *is* still the right tool for the B2 fallback (row E) — different job. |
| D | **tus protocol / resumable-upload server fronting GitHub releases** | https://tus.io/implementations.html (tusd, tus-node-server, tus-py-client — all MIT) ; GitHub upload docs (no `Content-Range`): https://docs.github.com/en/rest/releases/assets | MIT (implementations) | **SKIP** | tus needs a tus-speaking *server*. GitHub's upload endpoint is a single raw-body POST with no tus/Range support, so there is nothing to speak tus to. Running our own tus relay would need a host with storage + bandwidth — it just moves the 2 GB upload to a different server. Keep the pattern (100 MB + sha256 + manifest = tus-shaped, per Oct 19). |
| E | **Backblaze B2 large-file API as fallback store (native resumable multipart)** | https://www.backblaze.com/docs/cloud-storage-large-files ; rclone B2 backend (`backend/b2/upload.go`, chunked large uploads) | B2 API: proprietary service, S3-compatible; rclone MIT; b2sdk Apache 2.0 | **QUEUED — strongest true-resumable fallback** | Real multipart resume: `b2_start_large_file` → parts 5 MB–5 GB → `b2_list_parts` shows what's landed → `b2_finish_large_file` with per-part SHA1; interrupted uploads resume from the missing parts only. 10 TB/file ceiling. Pricing (Oct 2026): $6.95/TB/mo, first 10 GB free, uploads free, egress free to 3× stored then $0.01/GB — a 2 TB mirror ≈ $13.90/mo, pull-back proofs inside the 3× allowance are free. **Blocked on owner:** NO-SPEND law — any B2 spend needs his say-so; no account signup by lanes. Also note B2 had EU upload failures Oct 30–31 2026 per its status feed (secondary source, not verified against the feed this pass). |
| F | **TeraBox upload API (unofficial) as fallback store** | https://deepwiki.com/seiya-dev/terabox-node/5.1-upload-system-deep-dive ; https://deepwiki.com/seiya-npm/terabox-api ; gist: https://gist.github.com/nis267/74c6315f6dbd24a0b8889acdd08789e6 | terabox-api / terabox-node license **not verified this pass** — do not vendor until checked | **QUEUED — fallback exists, needs a lane** | Real chunked resume: `precreate` returns a `block_list` of missing chunks, `.tbtemp` tracks progress, RapidUpload dedupes by hash; segment cap 120 MiB; premium 20 GB/file, free 4 GB/file. But: unofficial cookie-based API (jsToken/bdstoken captured from a browser session), no public/official API. The shop already uses TeraBox via the browser lane; wiring `tb-upload` needs that lane for cookie capture (same dependency as Oct 19 cluster 6). Does not fix the GitHub path. |
| G | **Kaggle datasets API as fallback store** | Kaggle CLI changelog (resumable uploads 1.3.9/1.5.14/1.5.15; state-file hardening 2.2.5): https://raw.githubusercontent.com/Kaggle/kaggle-api/main/CHANGELOG.md ; https://pypi.org/project/kaggle/ (Apache 2.0) | Apache 2.0 | **SKIP as a store; queued as an experiment at most** | `kaggle datasets create/version` does have resumable uploads with persisted state — the only fallback here with resume built into its official CLI. But it is a *dataset* store (metadata, slugs, versioning semantics), not a generic blob store; and shop Kaggle auth is currently fragile (legacy-key rotation hazard, OAuth migration pending per `~/TOOLS.md`). Do not route mirror traffic through it without a lane proving dataset round-trip + auth stability first. |
| H | **aria2 / wget as uploaders** | aria2: https://aria2.org/ (download manager; comparison table: "Upload … No" for aria2/wget, "Yes" for curl) ; wget manual: https://Www.GNU.Org/software/wget/manual/wget.pdf (self-described "download utility"); HTTP resume analysis: https://www.sysax.com/topics/http-https-file-transfer/large-files-over-http/ | aria2 GPLv2; wget GPLv3 | **SKIP — excluded honestly** | Both are downloaders. aria2 has no HTTP upload verb at all; wget can `--post-file` a body but has no upload resume (HTTP defines no upload Range; `Range` is for responses) and a retry restarts the whole body. Keep aria2 for the pull-back/download side where it is proven. |
| I | **curl flag bundle (`--retry-all-errors`, `--speed-limit/--speed-time`, `--keepalive-time`, `--http1.1`)** | https://curl.se/docs/manpage.html | curl license (MIT/X derivative — curl is MIT-licensed) | **PULL IN the retry + stall-killer subset; SKIP keepalive as a fix; `--http1.1` as an experiment only** | `--retry 5 --retry-all-errors --retry-connrefused --retry-delay 10 --retry-max-time 900` + `--speed-limit 100000 --speed-time 60` + `--max-time 600` per 100 MB part: cheap, correct, and already the Oct 19 template. `--keepalive-time` cannot help an active transfer (idle-only probes). `--http1.1` unproven — A/B it, don't adopt it. All of this is worthless at 2 GB: a retried 2 GB PUT still restarts from zero. |
| J | **Third-party upload actions (svenstaro/upload-release-action, softprops/action-gh-release)** | svenstaro retry: https://deepwiki.com/svenstaro/upload-release-action/7.2-error-handling-patterns (3 attempts, `@lifeomic/attempt`, exponential backoff) ; softprops: https://deepwiki.com/softprops/action-gh-release/3-development-guide (`@octokit/plugin-retry`, MIT per that page) | svenstaro license not re-verified this pass; softprops MIT | **SKIP for VM lanes** | Both retry the *whole file* (3 attempts, restart from zero) — same cost math as curl retry at 2 GB. Both run only inside GitHub Actions runners, not on this VM. Useful pattern reference only (retry-with-backoff around a whole-asset upload). Not a pull-in for the arcade lane. |
| K | **github-release-retry (PyPI)** | https://pypi.org/project/github-release-retry/1.0.1/ ("retries (deleting partial assets) if not [verified]"; `--retry_limit` default 5) | License not checked this pass | **SKIP** | Whole-file retry with partial-asset deletion — the right *shape* (verify-then-retry) but at whole-file granularity. At 100 MB parts our own stdlib wrapper does the same with no new dependency (stdlib-only law). At 2 GB it has the identical restart-from-zero cost. |

## 5. Recommended wire-up (exact)

For the arcade mirror lane (and any lane still splitting at ~2 GB). No new dependency; stdlib glue + tools already installed (`gh` 2.102.0, curl 8.5.0 — both verified live on this VM).

**Step 1 — split at 100 MB (the decided quantum; if the lane has its own splitter, change the constant, not the design):**

```bash
# 100,000,000-byte parts, deterministic names, per-part sha256
split -b 100000000 -d --suffix-length=2 "$FILE" "${FILE}.part-"
sha256sum "${FILE}".part-* > "${FILE}.parts.sha256"
```

**Step 2 — per-part upload loop (idempotent: skip-if-verified, delete-`starter`-then-retry).** Pseudocode for the lane wrapper; the CloudDog integration lane owns the real implementation in the store backend:

```bash
for part in "${FILE}".part-*; do
  name="$(basename "$part")"
  # skip if the asset is already on the release with matching size + digest
  if gh release view "$TAG" -R "$REPO" --json assets \
      --jq ".assets[] | select(.name==\"$name\")" | grep -q .; then
    # lane must compare size/digest here (release API returns size + sha256 digest)
    echo "SKIP verified $name"; continue
  fi
  # delete any 'starter'-state partial left by a 502/reset before retrying
  # (asset id lookup via gh api; delete only assets in state 'starter' or with wrong size)
  attempt=0; until [ $attempt -ge 5 ]; do
    attempt=$((attempt+1))
    if gh release upload "$TAG" "$part" -R "$REPO"; then break; fi
    sleep $((10 * attempt))   # 10s, 20s, 30s… backoff; add jitter in the real wrapper
  done
done
# then upload the manifest (part list + sha256s + total size) as its own asset, and
# verify by pull-back: gh release download + sha256sum -c, per the existing lane pattern
```

If the lane uses raw curl instead of `gh` for a part, the equivalent per-part command:

```bash
curl -L --fail --show-error \
  --retry 5 --retry-all-errors --retry-connrefused \
  --retry-delay 10 --retry-max-time 900 \
  --speed-limit 100000 --speed-time 60 --max-time 600 \
  --keepalive-time 60 \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @"$part" \
  "https://uploads.github.com/repos/$OWNER/$REPO/releases/$RELEASE_ID/assets?name=$(basename "$part")"
```

Notes on the flags: `--retry-all-errors` is what makes rc 56 retryable (not in curl's default set); `--speed-limit/--speed-time` turns a stall into a retryable exit 28; `--max-time 600` caps a 100 MB attempt at 10 min (at the slowest observed 1.2 MB/s a part needs 83 s, so 600 s is 7× headroom); `--keepalive-time` is included at its default purely for explicitness — it does not fix resets (§2.4).

**Step 3 — verify per part, then manifest:** after each part lands, confirm via the release API (size + `digest` field) before deleting the local part (delete-as-you-go per the 2026-10-17 owner order). Upload `<file>.parts.sha256` / manifest as a release asset last (manifest-first finalization per Oct 19 queue item 4). Pull-back verify with `gh release download` + `sha256sum -c` before clearing anything local.

**Step 4 — measure, don't assume:** log per-part attempt count + duration + exit code. If 100 MB parts still reset, the reset is not (only) duration-driven — escalate with the per-part timings, and A/B `--http1.1` on a few parts.

## 6. What stays blocked / queued

- **The arcade lane's 2 GB split is the actual bug.** Nothing in this pass can fix it — only the lane change in §5 can. Until the lane enforces 100 MB, expect further rc 56 failures at ~12 min; each costs ~12 min and keeps 0 bytes.
- **Root cause of the ~12 min reset is unverified.** Candidates: egress-proxy connection-lifetime cap, LB idle/max-duration policy, GitHub-side upload handling. No proxy logs were available to this pass; the stochastic shape (one 20.6-min attempt) rules out a simple hard timer. Do not present any single cause as established.
- **B2 fallback (row E):** needs an owner spend decision (NO-SPEND law) + account setup. No signup attempted.
- **TeraBox programmatic upload (row F):** needs a browser lane to capture jsToken/bdstoken/cookie; license of `terabox-api` unverified.
- **Kaggle (row G):** auth fragility (legacy-key rotation; OAuth migration pending) blocks any reliance; experiment-only.
- **gh source direct read failed this pass:** `browser.open` on `github.com/cli/cli/blob/v2.106.0/pkg/cmd/release/shared/fetch.go` returned a fetch error (DNS/timeout, no HTTP status). The `gh` findings above rest on the manual, pkg.go.dev (which renders the same source), and the Oct 19 source read — not on a fresh direct read of the file. A lane with repo access can re-confirm `ConcurrentUpload` in one read.
- **No A/B test of `--http1.1` vs HTTP/2 was run** (read-only brief; no uploads run). It remains an experiment, not a recommendation.

## Sources (every claim above traces to one of these)

- GitHub REST docs, upload a release asset: https://docs.github.com/en/rest/releases/assets#upload-a-release-asset
- `gh release upload` manual: https://cli.github.com/manual/gh_release_upload
- cli/cli shared package (ConcurrentUpload, UploadOptions): https://pkg.go.dev/github.com/cli/cli/v2/pkg/cmd/release/shared ; https://pkg.go.dev/github.com/ungtb10d/cli/v2/pkg/cmd/release/upload
- cli/cli license (MIT): https://pkg.go.dev/github.com/cli/cli/v2@v2.88.0/pkg/cmd/release/shared?tab=licenses
- curl manual + option versions: https://curl.se/docs/manpage.html ; https://curl.se/cvssource/docs/options-in-versions
- curl rc 56 semantics: https://dev.to/kalemi/econnreset-and-connection-reset-by-peer-in-ci-2ga0
- rclone backends / v1.76.0: https://en.wikipedia.org/wiki/Rclone ; https://forum.rclone.org/t/rclone-release-v1-76-0/54456
- B2 large files: https://www.backblaze.com/docs/cloud-storage-large-files ; B2 pricing: https://www.zerobuffer.io/blogs/backblaze-b2-pricing
- TeraBox upload deep dive: https://deepwiki.com/seiya-dev/terabox-node/5.1-upload-system-deep-dive ; https://deepwiki.com/seiya-npm/terabox-api
- Kaggle resumable uploads: https://raw.githubusercontent.com/Kaggle/kaggle-api/main/CHANGELOG.md ; https://pypi.org/project/kaggle/
- tus implementations: https://tus.io/implementations.html
- aria2 vs curl upload comparison: https://aria2.org/ ; wget manual: https://Www.GNU.Org/software/wget/manual/wget.pdf ; HTTP resume analysis: https://www.sysax.com/topics/http-https-file-transfer/large-files-over-http/
- svenstaro upload-release-action retry: https://deepwiki.com/svenstaro/upload-release-action/7.2-error-handling-patterns ; softprops action-gh-release: https://deepwiki.com/softprops/action-gh-release/3-development-guide
- github-release-retry: https://pypi.org/project/github-release-retry/1.0.1/
- gh-large-releases two-tier chunking (2 GB big / 25 MB streaming): https://deepwiki.com/ading2210/gh-large-releases/4.1-data-flow-and-storage
- Prior shop research: `~/workspace/agent-ops/research-friction-20261019/01-resilient-transfer.md` ; `~/workspace/agent-ops/FRICTION-RESEARCH-2026-10-19.md` ; `~/workspace/agent-ops/disk-cleanup-log.md` (Gumball 500 MB reset entries, Scooby ~1.2 MB/s note)
- Live local evidence: `gh version 2.102.0 (2026-09-30)`; `curl 8.5.0 … nghttp2/1.59.0`; quantification computed live with python3 from the observed 2.8 MB/s (see §3).

[[RESEARCH-PULLIN-INDEX]] — index entry owed: add "upload resets rc56 / 100 MB enforcement on arcade lane" as a queued pull-in (owner: CloudDog / arcade-mirror integration lane) pointing at this doc; not edited here because this pass is research-only.
