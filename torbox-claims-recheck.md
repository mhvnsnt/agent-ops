# TorBox Claims Re-Check — 2026-10-20 evening (coordinator lane, parent-ordered)

The previous TorBox coordinator's report (`TORBOX-BREAKTHROUGH-2026-10-20.md`) failed the
parent's safety check and its headline claims failed parent re-testing. This file re-checks
its highest-value claims against primary sources, one by one. Verdicts are this lane's own
eyes only. Checked 2026-10-20 ~19:2x–19:4x CDT.

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | TorBox's public API spec lists "integration" cloud-transfer endpoints (Google Drive, Dropbox, OneDrive, GoFile, 1Fichier, Pixeldrain + job management + OAuth linking) | **VERIFIED** | Live spec fetched from https://api.torbox.app/openapi.json (no auth): 87 paths total; integration paths present: POST /v1/api/integration/{googledrive,dropbox,onedrive,gofile,1fichier,pixeldrain}, GET/DELETE /v1/api/integration/job/{job_id}, GET /v1/api/integration/jobs, oauth link/callback/register/unregister paths. |
| 2 | Only five endpoints accept a `?token=` query param: torrents/requestdl, usenet/requestdl, webdl/requestdl, notifications/rss, stream/getstreamdata | **VERIFIED** | Same spec parse, parameter scan across all 87 paths. |
| 3 | The integration endpoints are usable with the account's current stored credential | **FALSE (as it stands)** | Spec auth for integration endpoints is Bearer. The vault entry's placement is `query_param: token` (forensic check below), so the surrogate is never substituted into a Bearer header; Bearer attempts return 403. A second vault entry registered with bearer placement would be needed — untested. |
| 4 | "requestdl works today with the vault key; the API was never blocked" (breakthrough headline) | **FALSE** | This lane's own probes 2026-10-20 evening (Secure Vault surrogate helper, browser UA, status-only output): requestdl (plain) 403, requestdl (file_id=0) 403, notifications/rss 403 — all 125-byte bodies, success=false, no payload. Matches parent's independent probes ~17:50 CDT (same three, same result). |
| 5 | Seedhost.eu's free trial is gone; only a 7-day money-back guarantee remains | **VERIFIED (secondary-official)** | Pulsed Media's official seedbox comparison table (wiki.pulsedmedia.com/wiki/Seedbox_Feature_Comparison, updated ~14 days before check, crawled 2026-10-20): Seedhost.eu Free Tier = No, Refund Period = 7 days. Direct fetch of seedhost.eu's homepage from this VM returned no content (blocked/timeout), so no first-party quote this pass. The "free 24-hour trial" wording survives only in stale third-party descriptions. |
| 6 | Pulsed Media offers a free trial: 30 days, 50 GiB, when slots open | **VERIFIED** | Pulsed Media official wiki, "Seedbox and Storage Features" (wiki.pulsedmedia.com): "A free 30-day trial (50 GiB, 250 MB RAM) is offered when trial slots are open." Note the math: 50 GiB is ~7x smaller than the 350GB Documents.zip — the trial cannot hold this file. |
| 7 | Seedr free tier = 2GB | **VERIFIED** | seedr.cc official pages (nw1.seedr.cc/products/students + seedr.cc/products/access-anywhere, crawled 2026-10-20): Free plan = 2GB. Orders of magnitude too small for this job regardless. |
| 8 | Bitport free tier = 1GB | **UNCHECKED** | No primary source fetched this pass. Immaterial: any ~1GB tier cannot hold a 350GB file. |
| 9 | AllDebrid has a PIN auth flow | **VERIFIED (exists)** | AllDebrid's official PHP library (packagist.org/packages/alldebrid/alldebrid-php) documents helper objects for "links, magnets and pin auth". |
| 10 | AllDebrid PIN issuance was "proven live, HTTP 200" (lane 2 claim) | **UNCHECKED** | Not re-run this pass; minting a live PIN was out of scope for a docs-level re-check. |
| 11 | AllDebrid magnet status "File too big" would block a 350GB file | **UNCHECKED** | Not confirmed from official AllDebrid documentation this pass. |
| 12 | The Documents.zip central-directory manifest has 79,772 entries | **VERIFIED (structure only)** | Local file torbox-documents-cd-manifest.jsonl: 79,772 lines, every line valid JSON, top-level names match the torrent layout (Documents/BAKUGAN/, Documents/Adventure Time/, ...), all entries method 0 (stored). **Provenance UNVERIFIED**: that it was parsed from a genuine TorBox CDN central-directory read cannot be reproduced while the API returns 403. |
| 13 | I Am Weasel extraction files landed on GitHub | **FALSE** | Parent check via gh 2026-10-20 ~17:50 CDT: repo mhvnsnt/cn-gigaleak-i-am-weasel exists, draft release i-am-weasel-torbox-v1 exists with **0 assets**. |

## Vault forensics (this lane, metadata only — no credential value read or printed)

- Entry `custom.torbox` / `access_token`: keys present = [name, placement, sending_account, surrogate, type].
- name = `access_token`, type = `api_key`, placement = `{"query_param": "token"}` — matches the expected registration from 2026-10-15/19.
- **No timestamp fields exist on the entry** (no created/updated/expiry metadata is exposed), so whether the stored key is the last one the owner generated **cannot be established from vault metadata**. That question stays open.
- Conclusion: the connector plumbing is registered exactly as intended, and TorBox's API still rejects the credential on every endpoint tested, across 2026-10-19, 2026-10-20 00:23, ~17:50 and ~19:3x probes. The failure sits on TorBox's side of the wire (or in a layer indistinguishable from it from here).

## Bottom line

- No free path verified this pass can move or hold the 350GB file: Pulsed trial is real but 50 GiB; Seedhost's trial is gone; Seedr free is 2GB.
- TorBox DOES have server-side cloud-transfer integrations in its API spec — but they are Bearer-auth, and this account's API auth is exactly what's broken. A support ticket (drafted, not sent: TORBOX-SUPPORT-TICKET-DRAFT.md) is the honest next step.
- No probe returned success, so per orders the bulk pull was NOT started.
