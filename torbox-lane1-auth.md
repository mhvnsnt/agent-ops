# TorBox API Auth — Lane 1, Round 2 (2026-10-20)

**Scope:** Root-cause the BAD_TOKEN / 401 failures against ground truth (account
fmmg.mars@gmail.com, torrent 119449922 "Documents.zip", infohash
856d01039553693d51c2a98523ca2c9829e8bb63). Supersedes the auth conclusions of
`TORBOX-RESEARCH-2026-10-19.md` (Round 1) where they conflict — Round 1's central
assumption (the key is dead / plan is the problem) is **disproven by live tests below**.
No real API key appears anywhere in this file; all authenticated tests ran through the
Secure Vault surrogate flow per `custom.torbox/CONNECTOR.md`.

---

## VERDICT — root cause is a three-layer placement mismatch, not a dead key

1. **The vault-stored TorBox token is VALID right now.** Proven 2026-10-20 15:58 UTC:
   `GET /v1/api/torrents/requestdl?torrent_id=119449922&token=<surrogate>` → **HTTP 200**,
   and the returned CDN link serves byte ranges of the actual 350 GB zip (see §4).
   The "stale/revoked vault entry" hypothesis is **dead**.
2. **The vault credential is registered with placement `{"query_param": "token"}`** —
   Sentinel/authd only substitutes the `hsurr:` surrogate in that one spot. Put the
   surrogate in an `Authorization: Bearer` header and the **literal surrogate string**
   reaches TorBox, which correctly answers `403 {"error":"BAD_TOKEN"}`. Every Bearer
   failure through our tooling is explained by this alone.
3. **Most TorBox endpoints accept ONLY Bearer auth.** The live OpenAPI spec marks them
   `OAuth2PasswordBearer`; sending the (valid) token as `?token=` to them returns a raw
   FastAPI `401 {"detail":"Not authenticated"}` — the query parameter is ignored
   entirely. Only a small set of endpoints (`requestdl`, `notifications/rss`,
   `stream/getstreamdata`, usenet/webdl `requestdl`) take `?token=` at all.
   So our helpers fail in both directions:
   - `tb_mylist.py` / `tb_export.py` send `?token=` to Bearer-only endpoints → **401**.
   - Anything sending Bearer via the vault sends an unsubstituted surrogate → **403 BAD_TOKEN**.

**Net: the API, the account, and the stored key all work. Our connector's auth
plumbing is what's broken.** The one endpoint family the 350 GB job actually needs
(`requestdl` + CDN range reads) works **today, unchanged** — see §4.

---

## 1. Live API documentation (fetched 2026-10-20 15:39–15:47 UTC)

- Swagger UI: `https://api.torbox.app/docs` (FastAPI).
- OpenAPI spec (public, no auth): `https://api.torbox.app/openapi.json` →
  HTTP 200, 96,620 bytes, OpenAPI 3.1.0, title "TorBox API", version **1.0.0**,
  server `https://api.torbox.app`. (Probed `/v1/openapi.json`,
  `/v1/api/openapi.json`, `/docs/openapi.json` → all 404.)
- Human docs: `https://api-docs.torbox.app/` — states auth as
  `AUTHORIZATION Bearer {{api_key}}`; rate limits are now **per API token,
  300/min** ("We no longer accept IP whitelisting requests due to rate limiting
  being API token based, rather than IP based"); error table confirms
  `BAD_TOKEN` = "The provided token is invalid", `NO_AUTH`, `AUTH_ERROR`,
  `OAUTH_VERIFICATION_ERROR`, `DOWNLOAD_TOO_LARGE` (Free 10 GB / Essential
  200 GB / Standard 200 GB / Pro 500 GB byte limits as documented).
- **Only security scheme in the spec:** `OAuth2PasswordBearer`
  (oauth2 password flow, tokenUrl `token`). No API-key header scheme, no cookie scheme.

### Endpoint inventory — 87 paths in the live spec

Auth key: **B** = Bearer only (`OAuth2PasswordBearer`) · **Q** = `?token=` query
param declared · **P** = public / no auth in spec.

**general** — `GET /` (P) · `GET /v1/api/changelogs/json` (P) ·
`GET /v1/api/changelogs/rss` (P) · `GET /v1/api/stats` (P) ·
`GET /v1/api/stats/30days` (P) · `GET /v1/api/speedtest` (P) ·
`GET /v1/api/notifications/mynotifications` (B) ·
`POST /v1/api/notifications/clear` (B) · `POST /v1/api/notifications/clear/{id}` (B) ·
`POST /v1/api/notifications/test` (B) ·
`GET /v1/api/notifications/rss` (**Q**, `token` required)

**user** — `GET /v1/api/user/me` (B) · `GET /v1/api/user/stats` (B) ·
`GET /v1/api/user/subscriptions` (B) · `GET /v1/api/user/transactions` (B) ·
`GET /v1/api/user/transaction/pdf` (B) · `GET /v1/api/user/referraldata` (B) ·
`POST /v1/api/user/addreferral` (B) · `GET /v1/api/user/getconfirmation` (B) ·
`PUT /v1/api/user/settings/editsettings` (B) · `DELETE /v1/api/user/deleteme` (B) ·
`POST /v1/api/user/refreshtoken` (B + web **session_token** in body — see §3) ·
`GET /v1/api/user/auth/device/start` (**P**) ·
`POST /v1/api/user/auth/device/token` (**P**, body `device_code`)

**torrents** — `POST createtorrent` (B) · `POST asynccreatetorrent` (B) ·
`POST controltorrent` (B) · `POST controlqueued` (B) ·
`PUT edittorrent` (B) · `GET mylist` (B) · `GET exportdata` (B) ·
`GET getqueued` (B) · `GET checkcached` (B) · `POST checkcached` (B) ·
`POST magnettofile` (P) · `GET/POST torrentinfo` (P) ·
`GET requestdl` (**Q**: `token`, `torrent_id` required) — all under `/v1/api/torrents/`

**usenet** (`/v1/api/usenet/`) — `createusenetdownload`, `asynccreateusenetdownload`,
`controlusenetdownload` (B) · `PUT editusenetdownload` (B) · `GET mylist` (B) ·
`GET/POST checkcached` (B) · `GET provider/account` (B) ·
`POST provider/account/resetpw` (B) · `GET provider/connection` (P) ·
`GET requestdl` (**Q**: `token`, `usenet_id`)

**webdl** (`/v1/api/webdl/`) — `createwebdownload`, `asynccreatewebdownload`,
`controlwebdownload` (B) · `PUT editwebdownload` (B) · `GET mylist` (B) ·
`GET/POST checkcached` (B) · `GET hosters` (P) ·
`GET requestdl` (**Q**: `token`, `web_id`)

**queued** — `GET /v1/api/queued/getqueued` (B) ·
`POST /v1/api/queued/controlqueued` (B)

**rss** (`/v1/api/rss/`) — `POST addrss` (B) · `POST controlrss` (B) ·
`POST modifyrss` (B) · `GET getfeeds` (B) · `GET getfeeditems` (B)

**stream** — `GET /v1/api/stream/createstream` (B) ·
`GET /v1/api/stream/getstreamdata` (**Q**: `token` + `presigned_token` required)

**integration** (`/v1/api/integration/`) — cloud-upload jobs, all (B):
`POST googledrive` · `POST dropbox` · `POST onedrive` · `POST gofile` ·
`POST pixeldrain` · `POST 1fichier` · `GET jobs` · `GET job/{job_id}` ·
`DELETE job/{job_id}` · `GET jobs/{hash}` ·
OAuth linking: `GET oauth/{provider}` (P, redirect) ·
`GET/POST oauth/{provider}/callback` (P) · `GET oauth/{provider}/success` (P) ·
`POST oauth/{provider}/register` (B) · `DELETE oauth/{provider}/unregister` (B) ·
`GET oauth/me` (B) · `POST oauth/discord/linked_roles` (B)

**vendors** (`/v1/api/vendors/`) — all (B): `GET account` · `GET getaccount` ·
`GET getaccounts` · `POST register` · `POST registeruser` ·
`DELETE removeuser` · `PUT updateaccount` · `PATCH refresh`

---

## 2. Vault credential metadata (2026-10-20 15:54 UTC, value never exposed)

`dynamic_credential_entry("custom.torbox")` via
`/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`:

- Entry keys returned: `name`, `placement`, `sending_account`, `surrogate`, `type`.
  **No timestamp fields exist** in the surrogate response (no created/updated at) —
  entry staleness cannot be dated from authd; it doesn't matter, the key tests live (§4).
- `name`: `access_token` · `type`: `api_key`
- **`placement`: `{"query_param": "token"}`** ← contradicts CONNECTOR.md, which claims
  bearer_header placement and calls `tb_reqdl.py` "broken for this reason". The doc is
  stale; the registration is query_param, and `tb_reqdl.py`'s approach is the correct one.
- Surrogate format check: prefix `hsurr:` ✓, total length 38 (32-char body),
  charset `[A-Za-z0-9._~-]`, 2 colon segments — a well-formed surrogate, correctly
  returned by authd. **No surrogate mangling in the exchange itself**; substitution
  works exactly where the placement says it should (proven by §4 D/E vs A/C).

## 3. Token taxonomy — is there a separate integration token?

No separate "integration token" exists. Distinct credential types found:

| Credential | Used for | Source |
|---|---|---|
| **API key / API token** (one per account) | Bearer on B-endpoints; `?token=` on Q-endpoints; embedded in generated download URLs; WebDAV password (v9) | Settings page / `refreshtoken` |
| **Web session token** | ONLY sensitive ops: `POST /v1/api/user/refreshtoken` body `{"session_token": …}` ("Gives the user a new API token. Requires the user's session token from the website due to security concerns") and `deleteme` | Website login session |
| **OAuth tokens** (third-party apps/vendors) | `OAuth2PasswordBearer` scheme, tokenUrl `token`; TorBox.NET documents `AccessTokenExpired`/`RefreshTokenAsync` as **OAuth2-only** — API-key failures surface as plain `BAD_TOKEN` | OAuth flow / vendors endpoints |
| **Device-code grant** | `GET /v1/api/user/auth/device/start` (public) returns `device_code`, 6-digit `code`, `verification_url` (`https://torbox.app/oauth/device`), `interval`, `expires_in: 600`; `POST …/auth/device/token` then "Returns the user's token once the device code is authorized" — i.e. it hands over the **same API token** after web authorization. Added in changelog v8 (2025-09-03); free users enabled v8.2.1 (2025-12-20). **Verified live today** (§4 H). | API + website approval |
| **Presigned download token** | CDN URLs are `…/dld/<presigned>?token=<api_token>` (pattern documented since changelog v3.5); valid ~1 hour per old changelog note | `requestdl` response |
| **Integration OAuth links** (Discord/Google Drive/etc.) | Link third-party accounts TO TorBox; authorized **by** the API token, they don't replace it | `/integration/oauth/*` |

**Revocation semantics ("Get New API Key"):** No public doc, issue, or changelog entry
states the semantics explicitly (searched web + GitHub clients 2026-10-20; results
were noise from the unrelated torbox.ch project). Indirect evidence for a
**single-token model**: the token is singular everywhere ("your API key" in settings
since v3.0; one `refreshtoken` operation that "gives the user a new API token" gated
by the web session token; rate limits keyed per token). Under that model, generating a
new key replaces the old one server-side. **But it cannot explain our failures:** the
token currently in the vault — registered before/during the click spree — **still
authenticates today** (§4). Whatever the dashboard clicks did, the vault's token is
the account's currently accepted token (or an accepted one). Do not build plans on
"the vault key was revoked" — it was not, as of 2026-10-20 16:13 UTC.

## 4. Live test matrix — 2026-10-20 (all via vault surrogate, browser UA, redirects off)

| # | Call | Time (UTC) | Result |
|---|---|---|---|
| — | `GET https://api.torbox.app/` (no auth) | 15:47:09 | **200** `{"success":true,"detail":"API is running."}` headers: `x-ratelimit-limit: 300`, CF-RAY …-DFW |
| — | `GET /v1/api/stats` (no auth) | 15:47:12 | **200** `total_users: 1081688, total_servers: 268` |
| — | `GET /v1/api/changelogs/json` (no auth) | 15:47 | **200**, 752,380 bytes, 100 entries, latest v9.2 (2026-08-17) |
| — | `bin/tb_mylist.py` (as shipped) | 15:55:37 | **HTTP 401** (traceback, exit 1) — helper sends `?token=` to a Bearer-only endpoint |
| A | `GET /v1/api/user/me`, `Authorization: Bearer <surrogate>` | 15:58 | **403** `{"success":false,"error":"BAD_TOKEN","detail":"Your token is invalid or has expired. Please log in again or reset your token."}` — literal surrogate reached TorBox unsubstituted |
| B | `GET /v1/api/user/me?token=<surrogate>` | 15:58 | **401** `{"detail":"Not authenticated"}` — query token ignored on Bearer endpoints |
| C | `GET /v1/api/torrents/mylist?limit=5`, Bearer surrogate | 15:58 | **403 BAD_TOKEN** (same body as A) |
| D | `GET /v1/api/torrents/requestdl?torrent_id=119449922&token=<surrogate>` | 15:58 | **200** `{"success":true,"detail":"Torrent download requested successfully.","data":"https://nexus-306.snam.tb-cdn.io/dld/<presigned>?token=<redacted>"}` |
| E | `GET /v1/api/notifications/rss?token=<surrogate>` | 15:58 / 16:07 | **200**, account's real notification feed (see §5) — second independent proof the substituted token authenticates |
| F | `GET /v1/api/torrents/torrentinfo?hash=856d…` (public) | 15:58 | 500 `UNKNOWN_ERROR` "Could not download full metadata…" (endpoint quirk, not auth) |
| G | `GET /v1/api/torrents/exportdata?torrent_id=119449922&type=torrent`, Bearer surrogate | 16:07 | **403 BAD_TOKEN** (expected — Bearer-only endpoint) |
| H | `GET /v1/api/user/auth/device/start?app=Lane1Probe` (no auth) | 16:07 | **200** device code issued, `verification_url: https://torbox.app/oauth/device`, `expires_in: 600` |
| I | `GET /v1/api/usenet/requestdl?token=<surrogate>` (no id) | 16:07 | **422** validation (missing `usenet_id`) — no auth rejection |
| J | **CDN range proof** on a fresh `requestdl` link (in-process, URL never printed) | 16:13:02 | `Range: bytes=0-1023` → **206**, `Content-Range: bytes 0-1023/350016069416`, `Accept-Ranges: bytes`, first bytes `PK\x03\x04` (ZIP header). `Range: bytes=-131072` → **206**, tail content is ZIP central-directory data (visible path fragment "…orts/MGM Shorts/") |

Notes on J: served object size is **350,016,069,416** bytes — 12 bytes less than the
350,016,069,428 figure in the brief (torrent-reported vs CDN-served size; use the
served figure for range math). No `DOWNLOAD_TOO_LARGE` was raised for `requestdl`
link generation or range reads on this account today, despite the documented
Essential 200 GB limit — **observed behavior beats the doc here**; whether a full
350 GB single-stream pull behaves differently is untested (and unnecessary: the
extraction plan is range-based).

## 5. Account timeline from the account's own notification feed (§4 E)

Retrieved via the working `?token=` RSS endpoint — the account talking about itself:

- **2026-10-15T14:48:39Z** — "Free Trial Activated" (TorBox **Pro** free trial, 24 h)
- **2026-10-16T20:50:12Z** — "Premium Expired" ("downgraded to the free plan")
- **2026-10-18T17:06:59Z** — "Payment Successful"

Consistent with ground truth (first key worked 2026-10-15 during the Pro trial;
Essential paid 2026-10-18). Nothing in the feed mentions token resets, security
locks, or auth incidents.

## 6. Changelog / status — any auth change after 2026-10-15?

- Official changelog feed (`/v1/api/changelogs/json`, fetched today): **latest entry
  is v9.2, 2026-08-17** — nothing published between 2026-08-17 and today at all.
  v9.2's only API note: auth-accepting routes optimized (~20 ms/req). No auth-model
  change, no revocation change.
- Recent auth-relevant history: v9.1 (2026-07-31) "API rewritten to be fully async",
  T3 403 fixes (T3 only); v9 (2026-07-01) WebDAV gains API-key Basic auth
  (username `torbox`, password = API key) and T3 (S3-compatible) launches;
  v8.4 (2026-02-13) rate limits switched to per-API-key; v8.1 (2025-10-25) speedups
  "for routes with API keys"; v8 (2025-09-03) device-code flow added.
  **None of this breaks existing API-key auth** — and §4 proves it didn't.
- Status page `status.torbox.app`: only recent item is CDN/transcoding maintenance
  2026-09-28 (resolved). No October API/auth incident. API root + stats answer 200
  today through our normal egress proxy — **the Round 1 "Cloudflare/proxy rejects
  our API calls" hypothesis is also dead**: unauthenticated and `?token=` calls
  traverse the same proxy fine; only the Bearer-surrogate calls fail, at TorBox's
  own auth layer, because of what we put in the header.

## 7. Helper / doc defects found (independent of the key)

1. `bin/tb_mylist.py` + `bin/tb_export.py`: architecturally incapable of working —
   they attach the credential as `?token=` to Bearer-only endpoints (spec §1).
   Their 401s were never evidence about the key.
2. `bin/torbox_add_magnet.py`: **crashes with `NameError`** (verified live 2026-10-20):
   calls `url_with_surrogate_query_param`, which is never imported (it imports
   `add_surrogate_to_request` instead). Also moot for auth — `createtorrent` is
   Bearer-only, so even fixed, it needs Bearer placement.
3. `custom.torbox/CONNECTOR.md` is stale: claims bearer_header placement ("so
   requestdl cannot be called through the surrogate", "tb_reqdl.py is broken").
   Reality is the exact inverse: placement is `query_param: token`, and the
   requestdl-style helper is the one that works.
4. `bin/tb_reqdl.py` prints the raw `requestdl` JSON — the returned CDN URL embeds
   the **real API token** (see §3, presigned-URL pattern). Anyone running it as-is
   sprays the key into logs. It must redact `token=` before printing. (This lane's
   probes redacted in-process and never printed a full link.)

## 8. What this unblocks / recommended shape for the parent lane

- **The 350 GB extraction can proceed NOW with zero credential changes:**
  `requestdl` via the existing vault `?token=` flow (tb_reqdl pattern, with the
  §7.4 redaction fix) → CDN link → tail-range reads for the ZIP central directory
  (72,369-file manifest) → targeted range extraction. All proven live in §4 D/J.
  `mylist`/`exportdata` are **not** needed for this pipeline.
- **If Bearer-only endpoints are ever needed** (mylist, exportdata, createtorrent,
  user/me, integrations): the credential must exist in the vault with
  `bearer_header` placement — placement is per-registration, so the clean shape is a
  **second vault entry for the same key** with bearer placement, leaving the working
  query_param entry untouched. That's a vault re-registration decision for the
  parent (agent-side flow), not an owner task.
- **Alternative token source if the vault key ever does die:** the device-code flow
  (§3) is live and public — a browser lane with the standing TorBox sign-in can
  authorize `https://torbox.app/oauth/device` and the API hands back the account's
  current token. No dashboard key-copying involved.
- **Do not** chase: plan changes for auth reasons (auth is not plan-gated and the
  documented download-size limit did not fire on the needed path), key regeneration
  (the current token works; regenerating would only risk invalidating the working
  vault entry), or proxy bypasses (proxy is exonerated).

## Evidence index

- OpenAPI spec: `https://api.torbox.app/openapi.json` (HTTP 200, 96,620 B, 2026-10-20 15:39 UTC) — 87 paths, sole scheme `OAuth2PasswordBearer`.
- Docs: `https://api-docs.torbox.app/` (Bearer auth, per-token rate limits, error table, DOWNLOAD_TOO_LARGE limits).
- Changelogs: `https://api.torbox.app/v1/api/changelogs/json` (200, 2026-10-20 15:47 UTC); latest v9.2 2026-08-17.
- Status: `https://status.torbox.app/maintenance/1075910` (2026-09-28 CDN maintenance, resolved; no October auth incident).
- Live probes: §4 table, 2026-10-20 15:47–16:13 UTC (10:47–11:13 CDT), all through the vault surrogate; key material redacted in-process and never written to disk or logs.
