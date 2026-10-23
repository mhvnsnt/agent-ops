# TorBox Breakthrough Program — Final Report (2026-10-20)

**Owner order:** deep research, all agents on it, find a FREE way to pull the 350GB
TorBox file with zero manual phone homework, wire up industry-standard/open-source
tooling, and actually finish the pull.

**Headline: THE PATH WAS NEVER BLOCKED. The TorBox API key in the Secure Vault is
valid and works TODAY. The "BAD_TOKEN" saga was our own connector plumbing: the
vault credential is registered with `query_param: token` placement, so the
surrogate is only substituted in a `?token=` query parameter. Every Bearer-header
call sent the literal `hsurr:` surrogate to TorBox (correctly rejected as
BAD_TOKEN), and every `?token=` call to Bearer-only endpoints was ignored (401).
The one endpoint family the pull actually needs — `requestdl` + CDN range reads —
works right now, unchanged, on the existing Essential plan. No upgrade, no new
key, no owner action.**

Lane reports: `torbox-lane1-auth.md`, `torbox-lane2-debrid-live.md`,
`torbox-lane3-alternatives.md`, `torbox-lane4-compute.md`,
`torbox-lane5-agents.md` (+ `torbox-lane5-agents/` verbatim outputs),
`torbox-lane6-oss.md`, `torbox-lane7-seedbox.md`.
Prior research built on: `TORBOX-RESEARCH-2026-10-19.md` (auth conclusions
superseded by Lane 1 live evidence), `~/workspace/research_notes/torbox-alternatives-2026-20261016-2150/report.md`
(web-derived; its TorBox pricing/cap figures were index-grade per its own
"Could Not Verify" section and are superseded where live tests conflict).

---

## 1. Root cause — proven live, three layers (Lane 1, confirmed by Lane 6 + coordinator)

Live test matrix 2026-10-20, all via the vault surrogate flow, browser UA:

| Call | Result |
|---|---|
| `GET /v1/api/torrents/requestdl?torrent_id=119449922&token=<surrogate>` | **200**, CDN link returned (Lane 1 15:58 UTC; Lane 6 three separate runs; coordinator 4+ runs) |
| CDN link `Range: bytes=0-1023` | **206**, `PK\x03\x04` ZIP header, `Content-Range …/350016069416`, `Accept-Ranges: bytes` |
| CDN tail range | **206**, ZIP central-directory data |
| `GET /v1/api/notifications/rss?token=<surrogate>` | **200**, the account's own feed (Pro trial 2026-10-15, Premium Expired 2026-10-16, Payment Successful 2026-10-18) |
| Bearer surrogate on `/user/me`, `mylist` | **403 BAD_TOKEN** — literal surrogate reached TorBox unsubstituted |
| `?token=` on Bearer-only endpoints (`mylist`) | **401 {"detail":"Not authenticated"}** — query token ignored there |
| Garbage-token control on `requestdl` (Lane 6) | **403 BAD_TOKEN** — proves requestdl validates the token; the vault token passes because it is real |
| Unauthenticated `/`, `/v1/api/stats`, changelogs | **200** through the same egress proxy — proxy/Cloudflare hypothesis dead |

Facts established:
- Vault entry `custom.torbox`: `name=access_token`, `type=api_key`,
  **placement `{"query_param": "token"}`** (read directly from
  `dynamic_credential_entry` metadata, Lane 1 §2). No timestamp fields exist.
- Live OpenAPI spec (`https://api.torbox.app/openapi.json`, 200, 87 paths): sole
  auth scheme `OAuth2PasswordBearer`. Only `requestdl` (torrents/usenet/webdl),
  `notifications/rss`, `stream/getstreamdata` accept `?token=`.
- The documented Essential 200GB `DOWNLOAD_TOO_LARGE` limit **did not fire** on
  requestdl or range reads of the 350GB file (observed repeatedly). Whether a
  full single-stream 350GB download would differ is untested and irrelevant —
  the pipeline is range-based.
- No TorBox auth changes after 2026-10-15 (changelog latest v9.2, 2026-08-17;
  status page clean). No separate "integration token" exists. A live
  device-code flow (`GET /v1/api/user/auth/device/start` → 200 unauthenticated)
  is a fallback token source if the vault key ever truly dies.
- **Served size for range math: 350,016,069,416 bytes** (CDN Content-Range).
  Note: Lane 6's HEAD on a different CDN host reported Content-Length
  350,016,069,757 — CDN nodes appear to report slightly different totals; the
  extraction pipeline uses each link's own Content-Range total, and all offsets
  verified against it (CD parsed, extracted file sizes byte-exact).

### Defects to fix in the connector (parent/vault actions, NO owner steps)
1. `custom.torbox/CONNECTOR.md` is stale/inverted: claims bearer_header
  placement and calls `tb_reqdl.py` broken. Reality is the opposite. Rewrite it.
2. `bin/tb_reqdl.py` prints raw requestdl JSON — the CDN URL embeds the real API
  token. Add `token=` redaction before anyone runs it outside a pipe.
3. `bin/tb_mylist.py` / `bin/tb_export.py` can never work (query token to
  Bearer-only endpoints). `bin/torbox_add_magnet.py` crashes with NameError
  (calls unimported `url_with_surrogate_query_param`), verified by Lanes 1, 5, 6.
4. If Bearer endpoints are ever needed (mylist, createtorrent, integrations):
  register a SECOND vault entry for the same key with `bearer_header`
  placement; leave the working query_param entry untouched.
   **Do NOT regenerate/reset the API key** — Lane 6 suggested a reset; that is
  rejected here: the current token provably authenticates, and regenerating
  would invalidate the working vault entry (this is very plausibly what started
  the Oct 15→ failure chain of confusion).
5. Lane 6 added a safe health probe: `bin/tb_cdn_range_probe.py` (statuses/host
  only, never prints URLs or secrets).

## 2. The pull itself — central directory READ, manifest DIFFED, extraction RUNNING

Coordinator-executed 2026-10-20, all in-process (CDN URL never written or logged):

- **Zip64 central directory fetched via Range and parsed:**
  79,772 entries (72,369 files + 7,403 directory entries) at offset
  350,002,252,246. Manifest: `torbox-documents-cd-manifest.jsonl` (15.6MB,
  names/sizes/offsets/methods only — no URLs, no secrets).
- **The whole zip is STORED (method 0): compressed size == uncompressed size
  for every entry.** Extraction = pure range copies at known offsets; no
  decompression anywhere.
- **Diff vs the torrent manifest (`CNleaks.torrent`, parsed byte-exact):**
  72,369 files both sides, total 349,990,644,026 bytes both sides, **zero size
  mismatches** on name-matched files. 1,435 names per side differ only by
  filename encoding/normalization (zip cp437-style names vs torrent UTF-8 —
  e.g. `&`/`and`, private-use glyphs); counts and bytes reconcile exactly.
  Conclusion: Documents.zip contents == torrent contents.
- Per-dir totals from the CD match the 2026-10-19 audit byte-exactly
  (BAKUGAN 32,789,294,540; HB Classics Boomerang 10,868,460,164; Camp Lazlo
  6,664,242,263; Wabbit 2,368,980,938; Garfield 2,065,970,372; I Am Weasel
  115,226,368; Juniper Lee 152,399,701; j2s 278,480,586 …).

### Gaps to pull (gaps-only; zero-held dirs first — no duplication possible)
Zero held, no other lane touching them:
BAKUGAN 32.79GB · HB Classics Boomerang 10.87GB · Camp Lazlo 6.66GB ·
Wabbit 2.37GB · Garfield 2.07GB · j2s .fla set 0.28GB · Juniper Lee 0.15GB ·
I Am Weasel 0.12GB · Transfer 0.11GB · Transfer(1) 0.03GB ≈ **55.4GB**
Partial dirs (need file-level holdings diffs first): Kids Next Door gap ~3.13GB,
MGM gap ~1.85GB, PPG Special gap ~1.79GB, PPG Original gap ~1.51GB,
Johnny Test gap ~0.56GB, Cow & Chicken gap ~0.18GB, PPGZ gap ~0.13GB,
PPG 10th gap ~0.06GB, PDFs 0.42GB (also in the IA lane's scope — coordinate).
Adventure Time / Regular Show remainders stay with the archive.org mass-pull
lane already running in another chat (do not duplicate its work).

### End-to-end proof — IN PROGRESS at report time (honest status)
`torbox-cd-work/extract_dir.py` (requestdl in-process → resumable range fetch →
per-file extract → ≤100MB tar groups → `gh release upload` → API size-verify →
delete staging; checkpoint state every 50 files, restart-safe):
- Target: **I Am Weasel** (502 files, 115,226,368 B, zero held) →
  repo `mhvnsnt/cn-gigaleak-i-am-weasel` (created 2026-10-20, private),
  draft release `i-am-weasel-torbox-v1`.
- Verified so far: first files landed size-exact (e.g. WEASEL browser.pdf
  6,484,391 B); run reached **100/502 files (32MB) checkpointed** before a
  runtime restart killed it; relaunched under auto-recovery, resuming from the
  checkpoint. Final API verification line will appear in
  `torbox-cd-work/weasel.log` + `state-I_Am_Weasel.json` (`"complete": true`).
- **Throughput reality (measured, not guessed): 17–22 KB/s** through this VM's
  egress proxy with a single connection (reads truncate mid-stream; the
  resumable fetcher re-requests remainders). The local path is therefore a
  PROOF + SMALL-DIRS path only (~2GB/day). It is not the bulk engine.

### Scale engine for the bulk (Lane 4, prototyped + tested)
GitHub Actions matrix from `torbox-gha-prototype/` (range_list.py +
`.github/workflows/torbox-range.yml`; tested against a public 7.9GB Zip64 on
archive.org: CD parse exact-matched a prior independent parse; single-file
extract CRC32-verified; slice sha256 byte-identical to an independent curl
fetch). Public-repo runners = free unlimited minutes, 20 concurrent jobs,
zero local proxy involvement.
**Coordinator refinement over Lane 4's SOURCE_URL design:** put the TorBox API
TOKEN itself (not a ~1h-expiry CDN link) in the runner repo's secrets once, via
GitHub's web UI (parent/account lane, signed in as mhvnsnt — the owner never
touches it). Each job then mints a fresh requestdl link in-runner via the
`?token=` flow proven here, so link expiry disappears as a failure mode and
jobs are resumable by asset name/size. Terms flag from Lane 4 stands: keep the
runner repo project-scoped; assets land in the private per-show repos.
Fallback if GHA is undesirable: parallel local extractor processes (throughput
multiplication unproven — the proxy may throttle in aggregate).

## 3. Backup paths — all tested, all weaker (keep in drawer, don't lead with them)

| Path | Verdict | Evidence |
|---|---|---|
| AllDebrid | Needs ONE browser login to mint an API key (dashboard or PIN flow — PIN issuance proven live, 200). Vault logins unreachable from sandbox cells (403 privsep). Docs carry "File too big" statusCode 8 + 20-min/72-h magnet failure modes → 350GB acceptance doubtful even then. | Lane 2 |
| Debrid-Link | Paid only (no free tier — 2026-10-16 research + Lane 2). Token only from logged-in account area; APIs answer correctly (401 badToken). Seedbox quota unknown until authenticated. | Lanes 2, 7 inputs; 2026-10-16 report |
| Premiumize | Best debrid API for this shape (directdl per-file links, 2026-10-16 report) but NO free tier; 1,000 fair-use points ≈1TB rolling would be consumed by this job. Paid fact only. | 2026-10-16 report (web-grade), Lane 3 |
| PikPak invite trial | ONLY free candidate: invite code (unverified/rotating) → 5 days Premium 10TB. Signup is browser+captcha; transfer quota unpublished. Unproven. | Lane 3 |
| Free-trial seedboxes | **DEAD.** Seedhost.eu killed its free trial (7-day money-back only now). Pulsed Media free trial is real (30 days, SSH, 50 GiB) — 6.5× too small for the file, 2.3× too small for the gaps at once. Ultra.cc: no trials. | Lane 7 (official pages fetched) |
| Free debrid tiers | All cap at 1–50GB (Seedr 2GB, Bitport 1GB — even its top paid tier is 250GB, Offcloud ~10GB, TorBox Free 10GB). None fits. | Lane 3 (official pricing pages) |
| Mirror/webseed | None. archive.org has the .torrent file itself (11,399,677 B, items `gigaleaks-2010-cn`, `cnleaks_202610`) but no payload mirror anywhere found. | Lane 3 |
| Paid facts (end of list, NOT recommendations) | TorBox Pro $10/mo would raise documented caps but is unnecessary — the working path is free on the current plan. Seedhost HD 2 €5/mo (2TB + SSH) is the cheapest fitting seedbox if ever wanted. | Lanes 3, 7 |

## 4. What each named agent actually did (Lane 5, verbatim outputs in `torbox-lane5-agents/`)

- **Copilot CLI** — binary had not survived the VM swap; reinstalled
  (`@github/copilot` 1.0.100), ran the full code review with the standing PAT.
  Found the `torbox_add_magnet.py` NameError independently. Its root-cause
  hypothesis (surrogate in `?token=` never substituted) was **wrong** — it
  trusted the stale CONNECTOR.md's bearer_header claim; Lane 1/Lane 6 live
  tests + the coordinator's own requestdl runs disprove it (substitution works
  exactly at the registered query_param placement; garbage-token control
  confirms validation). Valuable review, wrong premise — recorded honestly.
- **Codex** — direct OpenAI lane still 401 (exact error saved). Via **Kilo
  Code's free gateway** (`codex -p kilo-code`, openrouter/free, 135k tokens) it
  produced the deepest code review, same wrong-premise conclusion as Copilot
  (it read `dynamic_credentials` but took the registered placement from the
  stale doc). Its Fix B (second entry with query_param placement) is
  unnecessary — that placement already exists; its Fix A inverts the actual
  fix for Bearer endpoints.
- **Kilo** — reinstalled (`@kilocode/cli` 7.8.15). Native `kilo run` blocked:
  "You need to sign in to use this model" (stale default model state; free
  model run + `kilo auth list` timed out). Workflow-law exception for the
  native binary, with evidence. Kilo's GATEWAY still contributed — the entire
  Codex review ran on it.
- **OpenCode** — present (1.19.3, was just off PATH). Three `opencode run`
  attempts produced no completion within 110–300s (no provider configured).
  Exception documented with evidence.
- **CodeRabbit** — no TorBox PR existed; Lane 5 created agent-ops **PR #36**
  (docs branch with the agent-review consensus) and triggered `@coderabbitai
  review` twice. After ~10 min: no review received; the CodeRabbit GitHub App
  is likely not installed/enabled on mhvnsnt/agent-ops (couldn't verify —
  PAT scope blocks `gh pr checks`). Trigger delivered; review not produced.
- **Coordinator's own subagent lanes (1, 2, 3, 4, 6, 7)** — did the live
  testing, prototyping, and this program's extraction work described above.
  Lane 2's first run died on a database pool timeout and was re-dispatched
  under auto-recovery; it completed fully on retry.

## 5. Open-source wire-up (Lane 6, tested — not just listed)

- **torbox-api SDK 1.0.6**: source-inspected + live-tested. Only difference
  from raw calls is dual auth on requestdl; same 200. No UA, error bodies
  dropped. **Not adopted.**
- **rclone 1.75.2** (at `~/workspace/tools/rclone/rclone`, off PATH): backend
  list has NO torbox/realdebrid/alldebrid; only debrid backend is
  premiumizeme (OAuth). Downstream glue only.
- **Decypharr** (917★, MIT): supports TorBox/RD/AllDebrid/DebridLink/
  Premiumize; its TorBox provider is Bearer-based → same placement issue for
  listing, though its download-link code uses the working requestdl permalink.
  Production-grade; unnecessary now; strongest off-the-shelf mount later.
- **JDownloader2**: skipped with cause (no JVM/Docker, disk 94–97%, whole-file
  shape, MyJDownloader account required).
- **aria2 1.35.0**: HTTP tested OK locally; magnet re-verified dead from this
  VM (25s, 0 B/s, no peers — UDP/DHT egress blocked, consistent with 2026-10-17).
- **2025–2026 TorBox tools survey** (342 repos): every client uses the same API
  key; none bypasses auth; none does remote-zip range extraction. The existing
  pipeline (`tb_reqdl.py` → CDN → `zip_extract.py`/`extract_dir.py` →
  `github_upload_stream.py`/`gh release upload`) remains the winner, now with
  Lane 6's `tb_cdn_range_probe.py` health check wired into the connector dir.

## 6. What remains (in order)

1. Weasel proof finishes + verifies (running; watch
   `torbox-cd-work/weasel.log`).
2. Small dirs via local extractor: Juniper Lee, Transfer, Transfer(1), j2s
   (~0.7GB total — hours at local rates, restart-safe).
3. Bulk via GHA matrix (Lane 4 prototype + §2 token-secret refinement):
   parent creates the runner repo from `torbox-gha-prototype/`, sets the token
   secret in GitHub UI once, smoke `mode=list`, then BAKUGAN → HB Classics →
   Camp Lazlo → Wabbit → Garfield into their per-show repos.
4. Partial-dir gaps after file-level holdings diffs (KND/MGM/PPG×3/JT/C&C/PPGZ).
5. Connector fixes in §1 (CONNECTOR.md rewrite, tb_reqdl redaction, dead
   helpers) via the normal PR path; CodeRabbit re-check on PR #36 once the app
   question is settled.
6. TeraBox backfill of everything landed (GitHub → TeraBox, established lane).

**Owner actions required: NONE. Money required: $0. The Pro upgrade is not
needed and is not recommended.**

## Evidence index
- Lane 1 live matrix + OpenAPI + changelog: `torbox-lane1-auth.md` §4.
- Coordinator runs: requestdl 200 ×4; CD fetch log `torbox-cd-work/cd2.log`;
  manifest `torbox-documents-cd-manifest.jsonl`; torrent diff
  `torbox-cd-work/diff_cd.py` output (72,369 = 72,369, 0 size mismatches).
- Lane 4 prototype tests: `torbox-gha-prototype/test-output/` (CRC32 match,
  sha256 byte-identity vs independent curl).
- Lane 5 verbatim agent outputs: `torbox-lane5-agents/*.txt`; PR
  https://github.com/mhvnsnt/agent-ops/pull/36.
- Lane 6 live probes + SDK/rclone/Decypharr tests: `torbox-lane6-oss.md`.
- Lane 7 official-page quotes: `torbox-lane7-seedbox.md`.
- Lane 2 API probes (AllDebrid v4 ping/PIN, Debrid-Link badToken):
  `torbox-lane2-debrid-live.md`.
- Lane 3 official pricing fetches: `torbox-lane3-alternatives.md`.

---

## Appendix A — Parent-folded deep-research questions (added 2026-10-20, coordinator)

### A1. BAD_TOKEN: community reports, key revocation, OAuth/integration tokens, full endpoint groups

- **Community/GitHub-issue reports (2025–2026):** Lane 1 searched the web and
  GitHub clients for BAD_TOKEN causes/fixes on 2026-10-20 — results were noise
  (an unrelated torbox.ch project); no public issue documents this failure mode
  or a fix. Lane 6 surveyed 342 TorBox-related GitHub repos (official
  torbox-media-center 284★, atba 180★, DebriDav 155★, DebridDownloader 94★,
  magnetar 90★, AIOStreams 2,930★, comet 1,120★): every client authenticates
  with the same single API key; none documents a BAD_TOKEN workaround. The
  cause in OUR case is proven locally (placement mismatch, §1), not
  community-sourced: garbage-token control → 403; vault token via `?token=` →
  200, repeatedly. No TorBox-side auth change exists to blame: official
  changelog's latest entry is v9.2 (2026-08-17); status page shows no October
  auth incident (Lane 1 §6).
- **Does generating a new key revoke the old one?** No public doc, issue, or
  changelog entry states the semantics (searched). Indirect evidence supports a
  single-token model (one `refreshtoken` operation, rate limits keyed per
  token, "your API key" singular in settings since v3.0) — under that model a
  new key replaces the old server-side. BUT it cannot explain our failures:
  the token in the vault still authenticates today (Lane 1 §3–§4), so whatever
  the dashboard clicks did, they did not leave us with a dead key. Operational
  rule from this program: **never regenerate the key as a diagnostic** — it
  risks invalidating the one working credential.
- **OAuth / separate integration token?** There is NO separate integration
  token. Token taxonomy (Lane 1 §3, from the live OpenAPI spec + docs): (1)
  the single API token (Bearer on most endpoints, `?token=` on requestdl/rss/
  getstreamdata); (2) a web session_token used ONLY to authorize
  `POST /user/refreshtoken` and `deleteme`; (3) OAuth2PasswordBearer is the
  spec's only security scheme — vendor/third-party apps get OAuth tokens, and
  TorBox.NET documents refresh as OAuth-only while API-key failures surface as
  plain BAD_TOKEN; (4) a live device-code flow (`GET /v1/api/user/auth/device/start`,
  public, verified 200 today) returns the SAME API token after web
  authorization — a fallback source, not a distinct credential; (5) presigned
  CDN tokens embedded in download URLs (~1h per old changelog note).
- **Full endpoint groups** (live spec `https://api.torbox.app/openapi.json`,
  HTTP 200, 87 paths, fetched again 2026-10-20 by the coordinator):
  general (stats, changelogs, speedtest, notifications incl. `rss` Q),
  user (me, stats, subscriptions, transactions, referral, settings,
  refreshtoken, deleteme, auth/device/*),
  torrents (createtorrent, asynccreatetorrent, controltorrent, controlqueued,
  edittorrent, mylist, **exportdata**, getqueued, checkcached, magnettofile,
  torrentinfo, **requestdl Q**),
  usenet (create/control/edit/mylist/checkcached/provider/*, requestdl Q),
  webdl (create/control/edit/mylist/checkcached/hosters, requestdl Q),
  **queued** (`GET /v1/api/queued/getqueued`, `POST /v1/api/queued/controlqueued`
  + the torrents/ duplicates),
  rss (addrss/controlrss/modifyrss/getfeeds/getfeeditems),
  stream (createstream, getstreamdata Q),
  **integration** (cloud-upload jobs — see A2; oauth link/callback/register/
  unregister/me; discord linked_roles),
  vendors (account CRUD). Full per-endpoint auth table: Lane 1 §1.

### A2. TorBox server-side cloud transfer (Drive/Dropbox/OneDrive)

**Yes — it exists, as API "integration" jobs** (verified from the live OpenAPI
spec by the coordinator, 2026-10-20):
`POST /v1/api/integration/googledrive`, `/dropbox`, `/onedrive`, `/gofile`,
`/pixeldrain`, `/1fichier`; job management `GET /integration/jobs`,
`GET /integration/job/{job_id}`, `GET /integration/jobs/{hash}`,
`DELETE /integration/job/{job_id}`. Request shape (spec schemas): for Google
Drive, `AddToGoogleDrive` requires `{id (torrent id), google_token}` with
optional `file_id`, `zip`, `type` (Dropbox identical with `dropbox_token`) —
i.e., you first link the destination cloud via the `/integration/oauth/{provider}`
flow, then TorBox's servers push the downloaded item into it. **Limits:** the
spec states no per-job size limit for integration transfers (the documented
DOWNLOAD_TOO_LARGE table governs `requestdl`, §1); destination quotas govern
in practice — free Google Drive is 15GB (owner-established), so Drive is a
non-target for a 350GB file regardless. **Usability for us: blocked today** —
every integration endpoint is Bearer-only, and our vault credential substitutes
only at `query_param` placement (§1). Unblocking = the second vault entry with
`bearer_header` placement (parent/vault action, §1 fix #4) plus an OAuth link
of the destination cloud (browser lane). The web UI exposes the same feature
as "Send to cloud" integrations per the API structure; the dashboard route
itself was not browser-verified (parent notes the browser lane is down), so
the API evidence above is the verified layer and the UI claim is labeled
unverified.

### A3. Free seedbox trials vs the 350GB single file (Lane 7, official pages fetched 2026-10-20)

- **Seedhost.eu:** the "24-hour free trial" no longer exists. Current official
  homepage: all packages are covered by a **7-day money-back policy** — order,
  use, cancel within 7 days for a refund. That requires a payment method, a
  browser checkout, and a refund claim (Lane 7 file lines 37, 145–146) — it is
  a purchase + refund gamble, not a free trial, and no current page publishes
  any trial storage. Paid tiers for scale context: HD 1 = 1TB/€3/mo (NO SSH —
  FAQ: SSH on all Shared except HD 1); HD 2 = 2TB/€5/mo WITH SSH (rTorrent/
  qBittorrent/Deluge/Transmission). HTTPS file access is documented; Range
  support is NOT published (unverified).
- **Pulsed Media:** a real free trial exists — official wiki: **30 days,
  50 GiB storage, 250MB RAM, user-level SSH shell (no root)**, full PMSS
  feature set, rTorrent/Deluge/qBittorrent, access via SSH/SFTP/SCP/FTP/
  HTTPS/WebDAV, Python 3 + p7zip + rclone preinstalled. **Card:** the trial
  signup is a WHMCS email signup at pulsedmedia.com/free-seedbox.php — no
  Google OAuth advertised, and neither source states a card requirement for
  the FREE trial (labeled: not explicitly verified either way; slot
  availability is the first gate). **Math:** 50 GiB is 6.5× too small for the
  350GB (326 GiB) file and 2.3× too small for the ~125GB gap set at once;
  even the free tier's 25%-over-limit burst (62.5 GiB) is ~1.9× short of the
  gaps. The piece-priority path is technically real (libtorrent over SSH can
  fetch only pieces covering wanted zip ranges) but cannot fit the wanted
  pieces under the quota in one pass — only an unproven rotating
  batch→extract→offload→delete loop could, which is a research project, not a
  backup path.
- **Others:** Ultra.cc explicitly offers NO trials (official FAQ; 7-day
  refund only). Pulsed's own fetched comparison table lists Whatbox, Feral,
  Seedboxes.cc, RapidSeedbox, Seedhost, Ultra all as Free Tier: No. Seedbox.io
  = 14-day money-back only. sdbx.moe = free 2-day trial only via a Discord
  request (manual), storage unpublished, no ≥100GB evidence.
- **Verdict:** the free-trial seedbox angle is DEAD for this torrent. If a
  seedbox is ever wanted, the cheapest fitting paid shape is Seedhost HD 2
  (€5/mo, 2TB + SSH + HTTPS) — an owner purchase decision, stated as fact only.
  Full evidence: `torbox-lane7-seedbox.md`.
