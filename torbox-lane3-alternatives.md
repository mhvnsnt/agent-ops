# Lane 3 — Alternative Debrid / Seedbox Sweep for a 350 GB Single-File Torrent

Date: 2026-10-20 (researched live this session)
Target: `Documents.zip` — 350,016,069,428 B (≈326 GiB / 350 GB decimal)
Infohash: `856d01039553693d51c2a98523ca2c9829e8bb63`
Magnet source: pastebin.com/nhH7LYfp — **verified live this session**: magnet fetched, `dn=Documents`, 15 trackers (opentrackr, demonii, etc.).

## Bottom line (honest, evidence-based)

**No free tier in this sweep can hold a 350 GB single file. Not one.**
Every free tier caps at 1–50 GB — 7× to 350× too small. The only *free* paths that
even touch 350 GB are:

1. **PikPak 5-day Premium trial via invite code** — 10 TB storage, cloud-download
   has *no per-file size cap* (bounded only by storage). This is the single
   credible free shot. It is a trial, not a free tier, and signup is
   browser/app + captcha — parent/browser lane required.
2. **Pulsed Media free seedbox** — real free tier, but only **50 GiB** — fails on size.

Everything else free fails outright. The cheapest *paid* fact (report only, no
recommendation to buy): **TorBox Pro $10/mo — 1 TB max per download, 1 TB
storage** (official pricing page, fetched this session). TorBox Standard/Essential
($3–5/mo, 200 GB max) and the TorBox free plan (10 GB max) all fail — which is
exactly the known TorBox problem this lane was asked to work around.

## Ranked table

| # | Service | Free tier / trial? | Max torrent / file (free) | Max if paid | API? | Range links? | Google OAuth signup? | Verdict for 350 GB |
|---|---------|--------------------|---------------------------|-------------|------|--------------|----------------------|--------------------|
| 1 | **PikPak** | Free 6 GB; **5-day full Premium (10 TB) via invite code** | 6 GB free; **10 TB during trial** | 10 TB Premium | Unofficial API (auth+captcha); WebDAV read-only, Premium-only | Via WebDAV / direct links — standard HTTP, not documented as guaranteed | Email/phone; Google sign-in offered in app (unverified from desktop web) | **ONLY free candidate that can fit it — trial window only** |
| 2 | **TorBox** | Free forever | **10 GB** | Standard $5/mo: 200 GB; **Pro $10/mo: 1 TB**, 1 TB storage | Yes, official, incl. `checkcached` | Yes — `requestdl` returns direct HTTPS links (standard CDN behaviour) | Yes (TorBox supports Google signup — parent to confirm at signup screen) | Free FAIL; Pro is cheapest proven paid fit |
| 3 | **Premiumize** | **No free / no trial** — paid only | — | Cloud 1 TB, but fair-use: **1,000 points ≈ 1,000 GB rolling 30 d**, +30/day top-up, storage also burns points (≈350 pts to hold + ≈350 to download a 350 GB file — feasible in points *only if* account is fresh/full, booster packs extra) | Yes, official | Direct links, standard HTTP | No (email/password) | Paid-only; points math is tight, €9.99/mo or €69.99/yr |
| 4 | **Real-Debrid** | Free account = demo only; **no free premium trial** | No published per-file cap for premium torrents | Premium €3/15 d, €4/30 d, €9/90 d, €16/180 d | Yes, official (`/torrents/addMagnet`, `/torrents/instantAvailability/{hash}`, `/unrestrict/link`) | Unrestricted links are direct HTTPS; Range works in practice via download managers (not a documented guarantee) | No (email/password) | Plausible paid fit, **size behaviour for a 350 GB uncached torrent is unverified** — RD is cache-centric; an uncached 350 GB torrent must actually download to RD first, and RD has removed/throttled large uncached torrents historically. Do NOT assume it works without a test add. Also 2026 keyword content filter may block by filename. |
| 5 | **AllDebrid** | **7-day free trial** (SMS verification, fair-use) | Trial under fair-use — no published 350 GB allowance | €2.99/mo recurring / €3.99/30 d one-time | Yes, official (`magnet/upload`) | Direct links, standard HTTP | No | Trial exists but fair-use + no published max ⇒ **unproven for 350 GB**; SMS step = owner-phone friction |
| 6 | **Pulsed Media (seedbox)** | **Free 30-day trial seedbox, 50 GiB**, 250 MB RAM, when slots open; 14-day money-back on paid | **50 GiB — FAIL** | V1000 from 1 TB storage (paid, ~€6.99/mo class) | No debrid API; SSH/SFTP/rclone/WebDAV on the box itself | Yes — you control the box: HTTPS/SFTP/WebDAV from your own files, Range is yours | No (email/billing account) | Free FAIL on size; paid seedbox *would* work and gives full control |
| 7 | **Seedr** | Free **2 GB** | **2 GB — FAIL by 175×** | Lite $3.95/10 GB, Basic $7.95/50 GB, Pro $12.95/500 GB, Master $19/1 TB (official pricing fetched) | API only on highest legacy tiers | Direct HTTPS download links | Email; social signup offered | Free FAIL; even Pro (500 GB) is a paid fit only, Master 1 TB comfortable |
| 8 | **Offcloud** | Free starter: 3 files / ~10 GB class limits (sources conflict on exact wording: "3 files free", "10 GB free storage/conversion", Chrome listing: 100 links incl. 2 torrent sources) | **~10 GB — FAIL** | $9.99/mo (listings vary $49.99–69.99/yr) | Yes (`cloud.*` endpoints documented in third-party integrations) | Direct links | No clear Google OAuth evidence | Free FAIL |
| 9 | **Put.io** | **No free tier** — $0.99 one-day trial only (official plans page, fetched) | — | 100 GB $9.99/mo, 1 TB $19.99/mo, 10 TB $49.99/mo | Yes, official OAuth API | Yes — direct download URLs, family/storage model | **Yes — Google Pay/Apple Pay at checkout; account signup via email/Google reported** | Paid-only; 1 TB plan fits |
| 10 | **Bitport** | Free **1 GB**, 1 torrent/day | **1 GB — FAIL by 350×** | $5/30 GB, $10/100 GB, $15/250 GB — **even top paid (250 GB) FAILS** | No public API found | HTTP (free) / HTTPS (paid) | Email/Facebook historically | FAIL at every tier |
| 11 | **Mega-Debrid** | Freemium label, premium required for torrent converter (extension states "You need a premium account") | Not published — no evidence of ≥350 GB | ~€4/mo class | Yes (third-party integrations) | Generated host links | No | Unproven; no published torrent size evidence — do not rely on it |
| 12 | **Furk.net** | Invite/Facebook-gated free account, limited | Not published; Furk is a *cache/search* service — only serves files already in its cache, it does not fetch arbitrary 350 GB torrents on demand for free users | Paid plans exist | Yes, documented API (`api.furk.net`) — requires account API key | Direct links for cached files | Facebook historically | FAIL for this use: no evidence this hash is in Furk's cache; public API test returned empty (see below) |
| 13 | **Instant.io / WebTorrent** | Free, open | Browser WebRTC peers only — a 350 GB file in a browser tab is not viable; no persistence, no seeding infrastructure, peers must be WebRTC-capable (regular torrent seeders are not) | n/a | WebTorrent JS API | Streaming in-browser only, no Range-capable hosted link | n/a | FAIL — wrong tool at this scale |
| 14 | **Debrid-Link** | "Partiellement gratuit" seedbox/debrid (FR) | Free limits not published in English docs found this session | Paid seedbox tiers | Yes | Direct links | No | Unproven — no ≥350 GB evidence found |

## Evidence / source URLs (fetched or returned this session)

- TorBox official pricing (fetched): https://torbox.app/pricing — Free 10 GB max, Standard $5/mo 200 GB max + 500 GB storage, Pro $10/mo 1 TB max + 1 TB storage, API Access on all tiers.
- Seedr official pricing (fetched): https://www.seedr.cc/pricing — Basic $7.95/50 GB, Pro $12.95/500 GB, Master $19/1 TB, Lite $3.95/10 GB. Free = 2 GB: https://nw1.seedr.cc/products/students/ ("account reverts to free tier limits (2GB)").
- Put.io official plans (fetched): https://put.io/plans — "No permanent free tier. The way in is the $0.99 one-day trial."
- Premiumize fair use: https://www.premiumize.me/fairuse (login-walled when fetched; system described at https://koditips.com/premiumize-kodi-info-review-setup/ — 1,000 points max, +30/day, 1 TB cloud, €9.99/mo or €69.99/yr, free account registration but paid membership required to use; and http://www.cloudtorrent.net/provider/premiumize-me/ — "There are no free or trial memberships", ~1 point = 1 GB, storage charged 1 pt/GB).
- Real-Debrid pricing / no free trial: https://koditips.com/real-debrid/ and https://www.firesticktvstream.com/what-is-real-debrid/ (€3/15 d – €16/180 d; "no free trial of the premium tier, very limited free account"). API shape: https://pkg.go.dev/github.com/divyam234/go-debrid/realdebrid (base `https://api.real-debrid.com/rest/1.0`, AddMagnet, GetInstantAvailability).
- PikPak free 6 GB / Premium 10 TB, invite = 5 days Premium: https://gist.github.com/uqeax34/fdfbbb944fe24c3e60160f159bb091f8 and https://www.cloudslinker.com/support-clouds/pikpak/ ("Cloud download from magnet/torrent/URL: no per-file size cap; bounded by your storage", WebDAV Premium-only read-only, monthly transfer quota since Sep 2023 — **quota size unpublished, a 350 GB pull could hit it; unverified**).
- Offcloud free limits: https://omghowto.com/best-cloud-torrenting-service-providers/ ("only 3 files with the free account", $9.99/mo) and https://quickfever.com/best-cloud-torrenting-sites ("free plan offers up to 10GB of storage or torrent conversion", 3 torrent links/month).
- Bitport free 1 GB: https://quickfever.com/best-cloud-torrenting-sites and https://technofaq.org/posts/2016/07/hassle-free-torrenting-at-work-or-university-using-bitport/ (Free 1 GB / $5 30 GB / $10 100 GB / $15 250 GB).
- Pulsed Media free seedbox 50 GiB / 30 days: https://wiki.pulsedmedia.com/wiki/Computer_resource ("A free 30-day trial (50 GiB, 250 MB RAM) is offered when trial slots are open", 14-day money-back) and https://wiki.pulsedmedia.com/wiki/Seedbox_Feature_Comparison (free tier: Yes).
- AllDebrid 7-day trial: https://troypoint.com/best-debrid-services/ ("Free Trial – 7 Days (fair use policy)", SMS verification, €2.99/mo recurring).
- Mega-Debrid: https://chrome.google.com/webstore/detail/mega-debrid/gakkobdjiifadnllomenhnpojjdaoaad ("You need a premium account to use this extension", torrent converter, 160+ hosts, site https://www.mega-debrid.eu).
- Furk: https://cdn-b.saashub.com/compare-1337x-vs-furk-net ("Limited Free Features", subscription model).

## Live tests performed (API-level, no browser — this subagent cannot operate a live browser)

Target hash used in every test: `856d01039553693d51c2a98523ca2c9829e8bb63`

### Top candidate 1 — PikPak
- **Blocked before any transfer test.** PikPak's API requires an authenticated
  account and a captcha-gated sign-in flow; a no-auth probe of its user API
  returned an empty response (no public/cache endpoint exists to query).
  There is no public "is this hash cached?" endpoint.
- Exact browser path for parent (below) is the only way in.

### Top candidate 2 — TorBox (free tier account test)
- `POST https://api.torbox.app/v1/api/torrents/checkcached` with the target
  hash → `{"detail":"Not authenticated"}` — cache check requires an account
  token. No anonymous test possible.
- Even with a token, the **free plan hard-caps at 10 GB max download size**
  (official pricing above), so a free TorBox account *cannot* accept this
  torrent regardless of cache status. Test outcome: **FAIL by plan limit, proven from official pricing — no signup needed to know.**

### Other API probes
- Real-Debrid `GET /rest/1.0/torrents/instantAvailability/{hash}` no-auth →
  `{"error":"bad_token","error_code":8}` — availability check is token-gated.
- Furk public API probe → empty response; Furk API requires an account key.
- Magnet itself: **live-verified** from pastebin raw (see top).

## Public mirror / webseed search — is the payload already mirrored?

**No full payload mirror found. Two pointer-only archive.org items found — important, do not mistake them for mirrors:**

1. archive.org advancedsearch for the infohash → 1 hit: **`gigaleaks-2010-cn`**
   — description literally embeds this hash ("cartoon network gigaleak torrent
   magnet hash: 856d…bb63 … totals out to 300+ gigs"). Its files are ONLY:
   `GIGALEAKS2010CN.torrent` (11,399,677 B) + archive.org metadata files.
   **It is the .torrent file, not the 350 GB payload.**
2. **`cnleaks_202610` — "Cartoon Network Leak Torrent (Re-upload)"** — same
   story: `CNleaks.torrent` at the identical 11,399,677 B + metadata only.
3. `documents.zip.-005-20251030` on archive.org is a *different, unrelated*
   split part (414,920,992 B `Documents.zip.005.zip`) — not this torrent.
4. General web search for the infohash returned **zero** torrent-index,
   webseed, or mirror results (search index has no record of this hash
   outside the archive.org pointers above). No `urlList` webseeds are in the
   magnet (tracker list only, verified from the raw magnet).

So: no HTTP mirror / webseed shortcut exists. The content must actually be
fetched from the swarm by *something* with ≥350 GB of room.

## Exact signup paths for parent / browser lane (no owner manual work)

### Path A — PikPak 5-day Premium trial (the only FREE fit) — TRY FIRST
1. Browser → https://mypikpak.com → Sign up (email `fmmg.mars@gmail.com` or
   Google sign-in if offered in the app/web flow presented).
2. Enter invite code **`74098243`** in the invitation-code field during
   registration (per the PikPak review/invite documentation above) → +5 days
   Premium, 10 TB.
   ⚠️ Unverified live: invite codes rotate; if this code is rejected, the
   fallback is any current invite code from PikPak's own referral surface —
   do NOT pay.
3. New Task / Cloud Download → paste the full magnet from
   pastebin.com/nhH7LYfp → confirm the single file ≈350 GB fits the 10 TB quota.
4. Watch for: (a) cloud-download completing from PikPak's cache/peers,
   (b) the unpublished monthly transfer quota — if PikPak refuses or stalls
   on quota, this path is dead and Path B is the fallback.
5. Get link: file → Download (direct link) or enable WebDAV
   (Settings → Experimental Features, Premium-only, read-only) for
   Range-capable pulls.
6. **Clock risk: 5 days.** The 350 GB must finish cloud-downloading AND be
   pulled out / Range-served inside the trial window.

### Path B — TorBox Pro (paid fact: $10/mo) — proven-fit fallback
Owner already knows TorBox; Pro is the tier that actually fits: 1 TB max per
download, 1 TB permanent storage, official API.
`createtorrent` with the magnet → poll `mylist` → `requestdl` for the
Range-capable direct link. Standard/Essential (200 GB) and Free (10 GB)
**cannot** be used — do not retry them for this file.

### Path C — Real-Debrid €3 / 15 days (paid, UNPROVEN for this size)
Only as an experiment if A and B are rejected: signup at real-debrid.com,
€3 tier, API token → `instantAvailability` first (if cached, it just works);
if not cached, `addMagnet` and watch whether RD will actually ingest a
350 GB torrent. Budget this as a €3 test, not a solution.

## Recommendation ranking (free-first)

1. **PikPak invite trial** — free, fits on paper, one shot, 5-day clock, quota risk.
2. **TorBox Pro $10** — not free, but the only *documented, API-proven* fit in the whole sweep.
3. **Pulsed Media paid seedbox (≥1 TB tier)** — full control, Range is self-hosted; free tier is a decoy at 50 GiB.
4. Everything else: free tiers fail by 7×–350×, or paid tiers are unproven at 350 GB (Premiumize points, Real-Debrid uncached ingestion).
