# TorBox Support Ticket — DRAFT (do not send without owner approval)

**To:** TorBox Support
**Subject:** API rejects every key for my account (403 BAD_TOKEN) while dashboard works fine — Essential plan, torrent cached

---

Hi TorBox team,

I need help with an API authentication problem on my account that I cannot fix from my side.

**Account:** fmmg.mars@gmail.com
**Plan:** Essential (active, renews November 18, 2026)
**Content in question:** one cached torrent on my account (added 2026-10-15, shows Cached / Download Ready in my dashboard, a single ~350GB zip file).

**What works:**
- I can sign in to the dashboard normally.
- The dashboard generates working direct download links for the file.
- The torrent itself is cached and healthy.

**What does not work:**
- Every API call authenticated with my account's API key is rejected. This has been true across many freshly generated keys over multiple days, entered carefully and tested immediately after generation.

**Timeline:**
- 2026-10-15: API worked after I re-registered the key in my tooling (a download-link request succeeded).
- Shortly after I used "Get New API Key" in my account settings, every key started failing, and no key generated since has worked at the API.
- 2026-10-19: I generated fresh keys several times and entered each one immediately. Every test failed the same way.
- 2026-10-20 (three separate test sessions, most recently this evening): same failures, unchanged.

**Exact behavior observed (tested today, 2026-10-20):**
- `GET /v1/api/torrents/requestdl?torrent_id=<my torrent>&token=<key>` → HTTP 403, `{"success": false, "error": "BAD_TOKEN", ...}` (125-byte body). Same with `file_id=0` added.
- `GET /v1/api/notifications/rss?token=<key>` → HTTP 403, same BAD_TOKEN body. (Per your public OpenAPI spec these are two of the five endpoints that accept a query token, so the call shape should be right.)
- `GET /v1/api/user/me` with `Authorization: Bearer <key>` → HTTP 403 BAD_TOKEN.
- The same key works when the dashboard itself signs a download link, so the key is not simply "wrong."

**What I am asking:**
1. Can you check on your side whether my account's API access has been flagged, revoked, or left in a bad state after the key regenerations?
2. Is there a server-side reset of my API authentication state that does not require me to keep generating new keys? Generating new ones has not helped across 5+ attempts.
3. If something about my plan or account status limits API use, please tell me exactly what it is — your pricing page lists API access on all plans, and I am on a paid plan.

I am not asking for anything unusual: I just want to download my own cached file programmatically, in ranges, instead of through a browser. Any details you need from me (timestamps of failed requests, the torrent ID), I can provide.

Thank you.

---

## Internal notes (not part of the ticket)

- Draft prepared 2026-10-20 by the disk-cleanup/TorBox-retry coordinator lane, from parent-verified evidence only.
- Evidence stack: parent probes 2026-10-20 00:23 CDT (Bearer /user/me → 403 BAD_TOKEN), parent probes ~17:50 CDT (requestdl x2 + rss → 403, success=false), coordinator probes ~19:3x CDT (same three → 403, 125-byte bodies), vault forensics (entry placement confirmed `query_param: token`, name `access_token`, type `api_key`, no timestamps exposed).
- No token value, signed URL, or surrogate appears anywhere in this draft, by design.
- Owner has rejected the TorBox Pro upgrade repeatedly; this ticket deliberately asks for an account-state fix, not a plan change.
- SEND ONLY with owner approval.
