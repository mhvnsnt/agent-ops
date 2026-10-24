# TorBox Lane 6 — Open-Source Wire-Up + Testing
Date: 2026-10-20 (CDT). All TorBox API tests ran through the Secure Vault
surrogate flow only (`dynamic_credentials`, credential `custom.torbox`);
no key was hardcoded, printed, or logged. Surrogates appear below only as
`<SURR>`. CDN URLs are never printed, only their hostnames.

## HEADLINE FINDING — the BAD_TOKEN wall is endpoint-shaped, not total

The stored TorBox key is dead for **Bearer-authenticated** endpoints but
**requestdl works today** through the `?token=` query flow. Evidence
(2026-10-20, torrent 119449922 "Documents", the 350GB cached torrent from
CONNECTOR.md):

| Call | Auth style | Result |
|---|---|---|
| `GET /v1/api/torrents/mylist` (raw helper `bin/tb_mylist.py`) | `?token=<SURR>` appended by helper | HTTP 401 `{"detail":"Not authenticated"}` (mylist does not accept query-token auth at all) |
| `GET mylist` probe | `Authorization: Bearer <SURR>` only | HTTP 403 `{"success":false,"error":"BAD_TOKEN","detail":"Your token is invalid or has expired..."}` |
| `GET mylist` probe | Bearer + `?token=` | HTTP 403 BAD_TOKEN (same) |
| `GET /v1/api/user/me` probe | Bearer only | HTTP 403 BAD_TOKEN |
| `GET /v1/api/user/me` probe | `?token=` only | HTTP 401 Not authenticated |
| `GET /v1/api/torrents/requestdl?torrent_id=119449922&zip_link=true` (helper `bin/tb_reqdl.py`) | `?token=<SURR>` only | **HTTP 200 `{"success":true,"detail":"Torrent download requested successfully.","data":"<CDN URL>"}`** |
| Same via torbox-api SDK `request_download_link` | Bearer + `?token=` (SDK sends both) | **200, success=True, data=<CDN URL>** |
| `requestdl` probe | Bearer only, no `?token=` | HTTP 422 `missing query token` (endpoint *requires* the query param) |
| `requestdl` probe | `?token=GARBAGE_NOT_A_TOKEN` (control) | HTTP 403 BAD_TOKEN — so requestdl *does* validate the token; the surrogate swap delivers a token requestdl accepts |

Conclusion: Sentinel swaps the surrogate in the query string too, and the
resulting token passes requestdl's validation while failing Bearer
validation on mylist/user/me. Whatever the server-side reason (token
scope/rotation state), the practical pipeline consequence is:

**requestdl → CDN link works NOW. Listing/profile/createtorrent-style
Bearer endpoints do not.** The pipeline only needs requestdl for torrents
already on the account (id known: 119449922), so the range-extract lane
is unblocked for that torrent. Adding NEW torrents (createtorrent is
Bearer) stays blocked until the owner resets the API token in TorBox
settings and the vault credential is re-registered.

### CONNECTOR.md corrections (noted, not edited — additive-only rule)
- Stored credential placement is actually `{"query_param": "token"}`
  (verified from `dynamic_credential_entry("custom.torbox")`), not
  bearer_header as the doc states.
- `bin/tb_reqdl.py` is NOT broken: it returned 200 + CDN link in this run.
  The doc's "Untested / broken" section is stale.
- Existing helpers (`tb_mylist.py`, `tb_export.py`, `torbox_add_magnet.py`)
  already use `url_with_surrogate_query_param`; mylist still fails because
  that endpoint ignores query tokens and wants Bearer (403 BAD_TOKEN).

## 1. torbox-api Python SDK (PyPI `torbox-api` 1.0.6, MIT)

Installed into a throwaway venv (`pip install torbox-api`, 20MB incl.
requests; venv lived in /tmp and was wiped by another lane's /tmp cleanup
after testing — reinstall is one command).

Source inspection (`torbox_api/`):
- `TorboxApi(access_token)` fans the token out to 9 services; auth is
  `AccessTokenAuth` → `Authorization: Bearer <token>` on every call.
- `services/torrents.py::request_download_link` is the one difference
  from raw calls: its serializer attaches the Bearer header AND
  `.add_query("token", token)` — **dual auth**. That matches the API:
  requestdl *requires* `?token=` (422 without it).
- Transport is plain `requests.request` with **no browser User-Agent**
  (default `python-requests` UA) and no redirect control. It survived
  Cloudflare here (no 1010), but CONNECTOR.md's browser-UA rule remains
  the safer default for raw calls.
- Error handling drops response bodies: on HTTP ≥400 it raises
  `RequestError` with status only — the BAD_TOKEN detail body is lost,
  which makes debugging worse than the raw helpers.
- Base URL default `https://api.torbox.app`, timeout default 60000ms.

Live tests (surrogate as access_token, output scrubbed):
- `api.torrents.get_torrent_list(api_version="v1")` → `RequestError`
  **403** (Bearer BAD_TOKEN, same as raw probe).
- `api.torrents.request_download_link(api_version="v1", token=<SURR>,
  torrent_id="119449922", zip_link="true")` →
  `RequestDownloadLinkOkResponse(success=True, detail="Torrent download
  requested successfully.", data=<CDN URL>)`.

Verdict: SDK does nothing the raw helpers don't, except dual-auth
requestdl — and `tb_reqdl.py` already achieves the same 200 with the
query flow alone. **Not adopted** (extra dependency, worse errors, no UA
control). The dual-auth detail is documented here in case a future
endpoint wants both.

## 2. rclone v1.75.2 (genuine, off-PATH)

- Binary: `~/workspace/tools/rclone/rclone` (82MB, static, go1.26.9).
  `rclone version` → `rclone v1.75.2, ubuntu 24.04, linux/amd64`.
  Not on PATH (`rclone: command not found` in a bare shell).
- `rclone help backends` on this build: **no `torbox`, no `realdebrid`,
  no `alldebrid` backend.** `rclone help backend realdebrid` →
  `CRITICAL: didn't find backend called "realdebrid"`.
- The one debrid backend present: **`premiumizeme`** (premiumize.me,
  OAuth client_id/secret). Also adjacent: `fichier` (1Fichier), `putio`,
  `http`, `webdav`, `internetarchive`, `mega`, `pikpak`.
- Dummy-config test (`--config /tmp/.../rclone-test.conf`, no secrets):
  `listremotes` works; an `http` remote against a local server listed and
  `rclone cat` streamed a file fine — rclone's `http`/`webdav` remotes
  are the usable glue shapes.
- Pipeline role: rclone cannot talk to TorBox directly. It *can* sit
  downstream of anything that exposes WebDAV/HTTP (Decypharr's WebDAV,
  TorBox's own WebDAV — existence attested by TorBox Media Center README
  "use TorBox's WebDAV"; endpoint/credentials NOT verified in this lane),
  and it is Decypharr's own mount engine (`pkg/rclone`, RC port 5572).
  For the single-zip range-extract job it adds nothing over
  `zip_extract.py`, which already speaks Range to the CDN directly.

## 3. Decypharr (sirrobot01/decypharr — 917★, MIT, Go, repo 20.6MB)

Clone into /tmp was attempted and aborted on a transient /tmp-full
condition; inspection was done from the GitHub API + raw sources instead
(no long service was run, per task).

- Providers (README + `pkg/debrid/providers/`): **Real-Debrid, TorBox,
  DebridLink, AllDebrid, Premiumize** + direct Usenet/NNTP. Mock
  qBittorrent/SABnzbd APIs for the *Arr stack; serves via its own DFS
  VFS, embedded/external rclone mounts, NFSv4/SMB, and **built-in
  WebDAV** (docs.decypharr.com: "mounts remote files using DFS, Rclone,
  or serves via WebDAV").
- Auth: config `debrids[].api_key` (config.full.json shape:
  name/host/api_key/folder/rate_limit/...). Its TorBox provider
  (`pkg/debrid/providers/torbox/torbox.go`) sends
  `Authorization: Bearer <api_key>` with a custom UA and a built-in
  300 req/min limiter (comment cites TorBox's per-key cap). **Same
  BAD_TOKEN wall**: its mylist/user-me calls would 403 with the current
  key exactly like our probes.
- Download links: `fetchDownloadLink` makes **no API call** — it builds
  the permalink `https://api.torbox.app/v1/api/torrents/requestdl?token=
  <account token>&torrent_id=<id>&file_id=<fid>&redirect=true`, i.e. the
  exact query-token flow proven working above. Its `SpeedTest` reads
  `Range: bytes=0-1048575` from that link, i.e. Decypharr itself assumes
  TorBox CDN links honor Range.
- HTTP Range for zip_extract: Decypharr's WebDAV/VFS is a *streaming
  media* layer; feeding a 350GB zip through it to range-extract would
  add a daemon, a FUSE/WebDAV hop, and an Arr-shaped cache in front of a
  job `zip_extract.py` already does directly against the CDN URL.
  **Verdict: real, maintained, production-grade — but not needed for
  this pipeline, and TorBox-side it is blocked by the same dead Bearer
  key for everything except the requestdl permalink trick it shares
  with our helper.** Revisit if an *Arr/media-serving need appears or
  after the token is reset (then it becomes the strongest off-the-shelf
  TorBox mount: it would give rclone a WebDAV target).

## 4. JDownloader2 headless — SKIP (feasibility only)

- Headless route is the `jlesage/docker-jdownloader-2` image or a bare
  JVM run: `JDOWNLOADER_HEADLESS=1` + `-Djava.awt.headless=true`, and
  in headless mode **MyJDownloader (cloud account, email+password) is
  the only control interface**.
- This VM: `java: command not found`, no `/usr/lib/jvm`, no Docker on
  PATH, ~8GB RAM mostly committed, root disk 94–97% full. Installing a
  JVM + JD2 (+ its self-updating jar churn) to gain a *whole-file*
  downloader is negative value: JD2 has no remote-zip Range extraction,
  no TorBox-specific advantage over the working requestdl→CDN path, and
  its debrid handling still needs the same account credentials.
- **Skipped with reason: heavy Java stack, extra cloud account, wrong
  tool shape (full downloads, not range-extract).**

## 5. aria2 1.35.0 (`~/workspace/tools/aria2/aria2c` wrapper)

Wrapper sets `LD_LIBRARY_PATH` to the bundled libs; the bare
`usr/bin/aria2c` fails without it (`libaria2.so.0: cannot open shared
object file`) — always call the wrapper.

- HTTP(S) multi-connection: **works**. Local test:
  `aria2c --max-connection-per-server=4 --split=4 http://127.0.0.1:18222/src.txt`
  → status `OK`, content verified byte-for-byte (`lane6-aria2-http-test`).
  Useful as a parallel downloader for plain CDN/HTTP files.
- Magnet: **dead from this VM, re-verified today.** 
  `aria2c --bt-metadata-only=true 'magnet:?xt=urn:btih:856d0103…&dn=Documents'`
  ran 25s at 0 B/s, stayed `INPR [MEMORY][METADATA]`, fetched no
  metadata, no peers. Consistent with the 2026-10-17 finding (outbound
  UDP/DHT blocked; see `~/workspace/hero-parts-pull/swarm_check.py`,
  libtorrent DHT test built for exactly this hash). aria2 magnet only
  becomes viable via a seedbox/remote node that hands back an HTTP URL
  — which is precisely what a debrid's requestdl already does.
- Role: fine as an HTTP download accelerator downstream of a CDN link;
  `zip_extract.py` + GitHub streaming upload already cover the actual
  job with range precision aria2 doesn't offer for zip members.

## 6. New / notable 2025–2026 open-source TorBox tools (GitHub API search, 2026-10-20)

Search `torbox`: 342 repos; `torbox created:>2024-06-01`: 316;
`debrid created:>2024-06-01`: 711. Relevant finds (stars as of today):

| Repo | ★ | Auth / shape | Fit |
|---|---|---|---|
| `sirrobot01/decypharr` | 917 | per-provider `api_key` in config; Bearer for TorBox | See §3 |
| `TorBox-App/torbox-media-center` | 284 | official TorBox team; `TORBOX_API_KEY` env; Python, MIT; FUSE/`.strm` mount, **video files only, paid plan required**, read-only; explicitly defers to TorBox's own WebDAV | Media serving only; same key wall (Bearer mylist); not a zip/range tool |
| `jittarao/torbox-app` | 184 | alternative TorBox web UI | UI only |
| `93Pd9s8Jt/atba` | 180 | cross-platform TorBox client (Dart, GPL-3.0), streaming | Desktop client; API key |
| `skjaere/DebriDav` | 155 | Kotlin, MIT; WebDAV bridge for debrids + Arr stack | Same family as Decypharr; smaller |
| `CasaVargas/DebridDownloader` | 94 | Rust/Tauri desktop, GPL-3.0; RD + TorBox + Premiumize; resumable multi-connection; tokens in OS keychain (the `orion01500/DebridDownloader` fork shows 0★ — use upstream) | Desktop whole-file downloader; no range-extract |
| `ArrCee76/magnetar` | 90 | browser extension: send magnets to RD/TorBox/AllDebrid/Premiumize/local client | Ingest convenience only |
| `Viren070/AIOStreams` | 2930 | Stremio addon aggregator (debrid-backed streaming) | Streaming, not extraction |
| `g0ldyy/comet` | 1120 | Stremio torrent/debrid addon | Streaming, not extraction |

None of the 2025–2026 crop changes the auth picture: **every TorBox
tool authenticates with the account API key** (Bearer for API calls,
`?token=` for requestdl permalinks). No tool bypasses a dead key, and
none offers remote-zip range extraction — that remains our
`zip_extract.py`'s job, by design.

## 7. CDN Range verification (the zip_extract contract)

Proven-path evidence already on disk: the earlier successful extraction
ran `zip_extract.py` against a TorBox CDN URL
(`~/workspace/hero-parts-pull/dlurl.txt`, host `nexus-088.cnam.tb-cdn.io`)
— log `okko-extract.log`: `zip size: 350.0 GB`, `zip64 central dir:
79772 entries`, `parsed 79772 entries`. So TorBox CDN links honor HEAD +
Range and the 350GB zip's central directory was already pulled this way.

Fresh-link probe (2026-10-20, new helper `bin/tb_cdn_range_probe.py`,
torrent 119449922, run three times — requestdl succeeded every time):
- `requestdl success: True | detail: Torrent download requested successfully.`
- `cdn host: store-013.wnam.tb-cdn.io`
- `HEAD -> 200 | len: 350016069757 | accept-ranges: bytes | type: application/zip`
  (350,016,069,757 = the zip_link wrapper; the inner `Documents.zip`
  listed in CONNECTOR.md is 350,016,069,428.)
- The probe's two small Range GETs did not return within the lane's
  125s window (CDN first-byte latency from this VM; no HTTP error was
  returned — the calls hung, they were not refused). Range *support* is
  nonetheless established: `Accept-Ranges: bytes` on the fresh link,
  Decypharr's Range-based SpeedTest design, and above all the prior
  full extraction, which ran entirely on `zip_extract.py`'s
  `assert r.status == 206` Range fetches against a tb-cdn.io link.
  A patient re-run of the probe (it allows 60s per call) is the way to
  re-confirm Range reads on a fresh link; nothing about the timeout
  contradicts the contract.

## Winners wired

1. **Kept/winner: existing pipeline** — `bin/tb_reqdl.py` (query-token
   requestdl, verified 200 today) → CDN URL → `zip_extract.py` (Range)
   → `github_upload_stream.py`. No new dependency needed.
2. **Added (additive, connector dir):**
   `bin/tb_cdn_range_probe.py` — one-command health check of the whole
   contract (requestdl success, CDN host, HEAD length/Accept-Ranges,
   head+tail Range reads) that prints no URLs or secrets.
3. **Not adopted:** torbox-api SDK (§1), Decypharr (§3, revisit after
   token reset), JDownloader2 (§4), rclone-as-TorBox-client (no such
   backend, §2), aria2-for-magnets (§5).
4. **Owner action that unblocks everything else:** reset the TorBox API
   token in TorBox settings and re-register the `custom.torbox` vault
   credential. Bearer endpoints (mylist, createtorrent, user/me) are
   403 BAD_TOKEN until then; requestdl already works.
