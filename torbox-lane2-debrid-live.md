# LANE 2 (RETRY) — Debrid-Link + AllDebrid Live Tests

Date: 2026-10-20 (America/Chicago). Agent: live-test subagent (depth 2).
Target torrent: infohash `856d01039553693d51c2a98523ca2c9829e8bb63`, dn=Documents — ONE file at torrent level: `Documents.zip`, 350,016,069,428 bytes (~350 GB), wrapping 72,369 files inside the zip.
Method note: page text was fetched with browser tools; API probes were real HTTP calls to the providers' APIs (curl). No website was "visited" in a browser session, no login was performed, no secrets were printed, written, or passed anywhere. No paid upgrades. No local staging beyond this report.

## VERDICT (bottom line)

- **Neither service could be live-tested with the owner's account from this sandbox, and neither can be driven end-to-end without a browser step.** The blocker is credential access, not the APIs: both APIs exist, are documented, and answered live probes.
- **AllDebrid:** API key can be obtained two ways, both need a logged-in browser session ONCE: (a) the Apikey dashboard on alldebrid.com, or (b) the official PIN flow — which I initiated live without any login (see below), but the PIN must be submitted on alldebrid.com/pin by a logged-in user. After that one step, everything (magnet upload/status/files, link unlock) is pure API, no browser again.
- **Debrid-Link:** API token is issued from the logged-in account area on debrid-link.com. No PIN/OAuth-style remote flow was found in any documentation. Same one-time browser requirement; after that, pure API.
- **350 GB viability is NOT proven for either service, and AllDebrid's own docs contain hard failure modes that make it doubtful** (see Limits). Nobody should promise the owner that either service will swallow this torrent until an authenticated magnet/upload test returns `ready`/downloading for this exact hash.

## 1. Connector / vault check

- `muse.connector_search` for "alldebrid", "debrid-link", "debrid link", "AllDebrid API": **no connector exists** for either service. Only unrelated hits (TorBox, Stripe-Link, etc.).
- `~/workspace/custom-connectors/` on disk: only `custom.torbox`, `custom.terabox`, and `custom.legacy-*` (ai-horde, elevenlabs, gemini, github-pat, groq, mistral, resend, vercel-ai-gateway). No AllDebrid / Debrid-Link connector dirs — matches the coordinator's 2026-10-20 verification.
- Secure Vault / dynamic credentials, metadata only:
  - `authdc cred list` → HTTP 403: "ingress auth callbacks are not reachable from the runtime cell (deny-by-default…)".
  - `authdc cred lookup --domain alldebrid.com`, `--domain debrid-link.com`, `--provider alldebrid`, `--provider debrid-link` → all HTTP 403: "credential lookup not available to cell callers".
  - Surrogate flow via `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py` (`dynamic_credential_entry`), tried names `alldebrid`, `alldebrid.com`, `AllDebrid`, `debrid-link`, `debrid-link.com`, `debridlink`, `custom.alldebrid`, `custom.debrid-link` × entries `access_token`/`apikey`/`api_key`/`password`/`username` → **every call HTTP 403**: "this connector's credentials are not available to the sandbox; use the connector's privsep…".
  - Interpretation (evidence-based): from this sandbox there is **no way to enumerate or use** the saved alldebrid.com / debrid-link.com vault entries — they cannot even be confirmed to be API keys vs. website username/password. The 403 is a cell-policy denial, not proof the entries don't exist. A privsep/parent lane or a browser lane holding the vault session is required to use them.

## 2. AllDebrid — official API (docs.alldebrid.com, API v4)

Docs read in full for the relevant sections (Authentication, Rate limiting, Pin auth, Magnet).

- Base: `https://api.alldebrid.com/v4/…` (some endpoints at `/v4.1/`). Auth: apikey via `Authorization: Bearer <apikey>` header (docs also show `?apikey=` in examples). All endpoints need a valid apikey except documented public ones (`/v4/ping`, `/v4.1/pin/get`, `/v4/hosts`, …).
- Rate limits (official): **12 req/s, 600 req/min**; excess → 429/503.
- Magnet endpoints: `POST /v4/magnet/upload` (param `magnets[]`, URIs or hashes), `POST /v4/magnet/upload/file`, `POST /v4.1/magnet/status`, `POST /v4/magnet/files`, `POST /v4/magnet/delete`, `POST /v4/magnet/restart`.
- Magnet requirements/errors (official): `MAGNET_MUST_BE_PREMIUM` (premium account required), `MAGNET_TOO_MANY_ACTIVE` — **max 30 active magnets**, `MAGNET_NO_SERVER` (server/VPN IPs refused for this feature — a datacenter egress IP can be rejected; worth flagging for any server-side lane).
- Correcting the task brief: the brief said "GET /v1/user" — the current API is **v4**; the user endpoint is `GET /v4/user`. There is no v1 in the current docs.

### Live probes (2026-10-20, unauthenticated + demo)

| Call | HTTP | Body (exact) |
|---|---|---|
| `GET /v4/ping` (public) | 200 | `{"status":"success","data":{"ping":"pong","version":"4"}}` |
| `GET /v4/user` (no key) | 200 | `{"status":"error","error":{"code":"AUTH_MISSING_APIKEY","message":"The auth apikey was not sent"}}` |
| `POST /v4/magnet/upload` with the target magnet, no key | 200 | same `AUTH_MISSING_APIKEY` JSON |
| `GET /v4.1/pin/get` (public) | 200 | `{"status":"success","data":{"pin":"93DA","check":"<check-token>","expires_in":600,"user_url":"https://alldebrid.com/pin/?pin=93DA","base_url":"https://alldebrid.com/pin/"}}` |
| `POST /v4/pin/check` for that PIN (not submitted by anyone) | 200 | `{"status":"error","error":{"code":"PIN_INVALID","message":"The pin is invalid"}}` — recorded as observed; docs split pin/get (v4.1) from pin/check (v4), and an unsubmitted PIN yields no apikey either way. The flow still requires a logged-in human/browser session to submit the PIN at alldebrid.com/pin. |
| `GET /v4/user` with the docs' **demo** key `staticDemoApikeyPrem` | 200 | `"demo": true`, static demo user (`demoUserPremium`, `isPremium: true`) — proves endpoint shape only |
| `POST /v4/magnet/upload` with demo key + target magnet | 200 | `"demo": true` with a **static fake response about an unrelated Ubuntu ISO** — the demo key does NOT process the submitted magnet. It proves nothing about acceptance of the 350 GB torrent. Recorded so nobody mistakes it for a successful test. |

### Can an API key be obtained WITHOUT browser login?

**No.** Official docs, Authentication section: keys are managed in the "Apikey dashboard" (logged-in website) or generated "remotely (with user action) through the PIN flow" — step 2 of the PIN flow is the user submitting the PIN on the AllDebrid pin page, which requires the account session. I proved step 1 works unauthenticated (live PIN issued above); steps 2–3 cannot complete without that logged-in submission.

## 3. Debrid-Link — API v2

- Base: `https://debrid-link.com/api/v2/…`; auth token sent as `Authorization: Bearer <token>` (token issued from the logged-in account on debrid-link.com; no PIN/OAuth remote-grant flow appears in any documentation found).
- Known routes (from the provider's API surface + open-source clients, e.g. debrid-blackhole): `GET /account/infos`, `POST /seedbox/add`, `GET /seedbox/list`, `GET /seedbox/cached`, downloader endpoints. Base URL `https://debrid-link.com/api/v2` is corroborated by multiple independent clients.
- Bare `https://debrid-link.com/api` fetched as text returned `{"result":"KO","ERR":"unknowR","ts":…}` — it is an API root, not a docs page. No public, browsable API reference with numeric limits was found (site docs sit behind the account area).

### Live probes (2026-10-20, unauthenticated)

| Call | HTTP | Body (exact) |
|---|---|---|
| `GET /api` (curl, follows to canonical host) | 301 | nginx "301 Moved Permanently" (bare root redirects; the browser text fetch of the same URL returned the `unknowR` JSON above) |
| `GET /api/v2/account/infos` (no token) | **401** | `{"success":false,"error":"badToken","error_description":"The authentication token is invalid or expired."}` |
| `GET /api/v2/seedbox/list` (no token) | **401** | same `badToken` JSON |
| `POST /api/v2/seedbox/add` with the target magnet, no token | **401** | same `badToken` JSON — auth is enforced before any magnet/size validation, so size acceptance cannot be probed without a real token |
| `GET /api/v2/account/infos` with a bogus Bearer token | **401** | same `badToken` JSON |
| `GET /api/v2/INVALIDTOKEN/account/infos` (token-as-path-segment guess) | **404** | `{"success":false,"error":"unknowR","error_description":"Unknown API endpoint."}` — confirms the token is NOT a URL path segment; it is the Bearer header |

### Can an API token be obtained WITHOUT browser login?

**No evidence of any such path.** Unlike AllDebrid there is no documented PIN flow. The token is created/copied inside the logged-in account on debrid-link.com. One browser login is required once; afterwards all seedbox operations are API-only.

## 4. Limits vs. a 350 GB single-file torrent

### AllDebrid (official docs, Magnet status codes)

The API docs publish **no numeric max torrent/file size** for magnet/upload. They do publish these magnet failure states, which are the real constraints for this job:

- statusCode **8 — "File too big"**: a too-big failure state exists; the threshold is not stated in the API docs.
- statusCode **7 — "Not downloaded in 20 min"**
- statusCode **10 — "Download took more than 72h"**: magnets that can't finish within 72 h are failed.
- statusCode **15 — "File not available - no peer"**
- Max **30 active magnets** (fine here — this job is 1 magnet).
- Premium account required for magnets (`MAGNET_MUST_BE_PREMIUM`). Account premium status of the saved login is unknown (could not be checked — see §1).
- On the 2026-10-15 rejection "for file count": at torrent level this torrent has exactly **1 file**, so a file-count rejection does not fit the torrent structure; the 72,369 files are inside the zip and invisible to the torrent layer. If a rejection recurs with a real key, the documented candidates are statusCode 8 (too big) or the 20-min/72-h rules — the authenticated test will say which, via `/v4.1/magnet/status`.

Assessment: **unproven, with documented failure modes pointing against it.** A 350 GB single file is exactly the shape statusCode 8 exists for. Do not treat AllDebrid as viable until an authenticated upload of hash `856d01039553693d51c2a98523ca2c9829e8bb63` returns a live status.

### Debrid-Link

- No numeric seedbox size/quota limit could be verified from official public documentation (docs are behind login; web searches returned no official limit page). **Stated honestly: unknown, not "unlimited."**
- The seedbox model means the 350 GB must fit the account's seedbox storage quota — that quota is only visible in `GET /account/infos` with a real token, which is the first call the browser-enabled lane should make.
- Assessment: **unproven.** Same authenticated test required: `POST /seedbox/add` with the magnet, then poll the seedbox list; a quota rejection will surface there if one exists.

### Range support on generated download links

- **Not testable in this lane**: generating a real download link requires an authenticated account with a ready file on either service, which §1–§3 show is impossible from this sandbox. No Range claim is made either way.
- What can be said from docs: AllDebrid serves unlocked links via `POST /v4/link/unlock` returning a direct link (+ optional streaming variants via `/v4/link/streaming`); the API docs do not state Range/206 behavior. Debrid-Link likewise returns direct links from seedbox files; no published Range statement found. The authenticated lane should test with `curl -r 0-1048575 -I <link>` on the real link and record the HTTP status (206 vs 200) and `Accept-Ranges` header before committing to a chunked-download design.

## 5. Exact browser step the parent must route (one-time, per service)

Neither service needs the owner to do manual work on an ongoing basis — the browser step can be done by a browser lane using the saved vault logins. What is needed, precisely:

1. **AllDebrid (choose one):**
   a. Browser lane logs in at alldebrid.com with the saved login → Apikey dashboard → copy/create the account apikey → register it as a proper dynamic credential/connector so API lanes can use the surrogate flow. **Then** run: `GET /v4/user` (confirm `isPremium: true` and `premiumUntil`), `POST /v4/magnet/upload` with hash `856d01039553693d51c2a98523ca2c9829e8bb63`, poll `POST /v4.1/magnet/status`, record the exact statusCode.
   b. OR complete the PIN flow: a fresh `GET /v4.1/pin/get` (PINs expire in 600 s — the PIN `93DA` issued during this test will already be expired; generate a new one at run time) → browser lane, logged in, opens the returned `user_url` and submits → poll `POST /v4/pin/check` until `activated: true` returns the apikey → store as in (a) and run the same tests.
2. **Debrid-Link:** browser lane logs in at debrid-link.com with the saved login → account/API area → copy/create the API token → register as a dynamic credential. **Then** run: `GET /api/v2/account/infos` (record premium status + any seedbox quota fields), `POST /api/v2/seedbox/add` with the magnet, poll `GET /api/v2/seedbox/list`, record exact JSON.
3. Whichever service accepts the magnet: generate the file's download link and run the Range probe (`curl -r 0-1048575 -I`) before designing the pull-down.

Until step 1 or 2 lands a real key/token in the credential store, **no API-only lane can test these services further** — every authenticated endpoint on both services was live-probed and rejects keyless/bogus calls exactly as documented above.
