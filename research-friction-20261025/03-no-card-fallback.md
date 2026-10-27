# No-card fallback asset host — Western Heart GLBs (if Cloudflare R2 doesn't work out)

> **⚠️ CORRECTION — 2026-10-27 (same day, after the B2 stand-up attempt): the doc's central claim was WRONG for the public-bucket path.** "No card at signup" is true, but "no card to host the game" is FALSE for a **public** B2 bucket: creating one demands a payment history or a **$1.00 one-time card payment** (verified live in the browser 2026-10-27 ~11:09 CDT on the real account — see §2.1). The verdict is now **CONDITIONAL**, and the fully card-free path is a **private bucket + Cloudflare Worker proxy (§4)**. What did NOT change: signup is still name + email only, private buckets are still card-free, and the no-card hard cap (§2.2) still holds for the private-bucket path. Nothing else in this doc was re-verified; this correction touches the B2 verdict, §2.1, §2.2, §2.5, §3 steps 2 and 6, the IDrive e2 row, §6, §7, and adds the new §4 — nothing else changed.

**Date checked:** 2026-10-27 (every limit below verified against a live source on that date; live sources are named in §7 — nothing here is stated from training data).
**Context:** [[01-deploy-pages-limit]] (the requirement numbers) · R2 is the 1st-choice asset host (owner decision 2026-10-26: Pages shell + GLBs on R2); the R2 signup stalled 2026-10-27 ~09:47 CDT at the "Add R2 subscription" step (Total Due Now $0.00, but subscription auto-renews and bills a payment method on file). This doc answers: if R2 doesn't work out, where do the GLBs go with NO card, NO payment method, free forever?
**Requirement (from the 01 doc + the R2 manifest):** ~**5,329.7 MB** of GLB models, **2,242 files**, including **176 files >20 MB** and **98 files >25 MiB**, largest file ~90 MB. Served to browsers with CORS (`Access-Control-Allow-Origin`) so three.js `GLTFLoader` `fetch()` works. No card at signup; a **PUBLIC bucket needs a $1 one-time card payment** (or payment history) — see §2.1; the fully card-free hosting path is a **private bucket + Cloudflare Worker proxy (§4)**. The no-card hard cap (§2.2) applies to the private-bucket path.
**Owner decision 2026-10-27 ~10:04 CDT: WAIT for the no-card fallback — do NOT accept the R2 subscription / preauthorization terms. R2 stays untouched: no subscription, no bucket, no public URL. This research is what unblocks hosting — the verified host below is the one to stand up first. Owner then tapped "Stand up B2 now" (~10:20 CDT); the stand-up attempt the same morning (~11:09 CDT) is what falsified the public-bucket claim — see §2.1.**

## 0. The numbers that decide everything

| Fact | Value | Source |
|---|---|---|
| Full asset set | 5,329.7 MB / 2,242 files | `tools/deploy/r2-upload-manifest.json` (WH PR #1152) |
| Free-tier headroom on any 10 GB host | ~4.7 GB | arithmetic |
| A full game load | ~100 MB per player session | 01 doc §4 / play-verify |
| B2 free egress | 3x average stored volume/mo ≈ **16 GB/mo ≈ ~160 full loads/mo** | Backblaze's own page, opened 2026-10-27 |
| R2 free egress (for comparison) | $0, unlimited | Cloudflare R2 pricing (01 doc) |

Two consequences: (1) any 10 GB free tier fits the set — the binding constraint is **egress**, not storage; (2) the fallback only needs to survive until R2 works or traffic grows past ~160 full loads/mo, at which point the Cloudflare-fronted path (§4) or R2 takes over.

## 1. Verdict table

| Host | Verdict | Free storage | Max single file | CORS | Card required? | What would break |
|---|---|---|---|---|---|---|
| **Backblaze B2** | **CONDITIONAL — public bucket needs a $1 one-time card payment (or payment history); private buckets are card-free** | **10 GB** | 5 GB single PUT / 10 TB multipart | Per-bucket CORS rules (UI + CLI + API), up to 100 rules | **YES for a public bucket** — $1.00 + tax one-time card payment (credited to the account) or a payment history on file; **NO for signup or a private bucket** (name + email only) | Public bucket is blocked until the $1 payment is made (owner-only, card); the card-free path is a private bucket + Cloudflare Worker proxy (§4). Free egress ~16 GB/mo (~160 full loads/mo); heavy traffic hits download caps (403), not bills; no built-in CDN (fix: Cloudflare in front, §4); set can't grow past 10 GB without a card |
| IDrive e2 | **SKIP — no permanent free tier** | 10 GB (trial allowance) | 5 GB single PUT / 5 TB multipart | S3-compatible (CORS not verified) | **YES to use beyond the trial** — 10 GB is a trial allowance, not a permanent free tier; paid plans start at $6/TB/month with a 1 TB minimum charge | IDrive's own e2 page frames it as "Try with 10 GB Free" against $6/TB/month pricing (verified live 2026-10-27, §7); the "permanently free, no card" claims in secondary sources describe IDrive's *backup* Basic plan, not e2 object storage. Do not use as the fallback. |
| Netlify free | SKIP as asset host (shell host only, already known) | n/a | n/a | n/a | No card at signup | 300 credits/mo HARD cap, ~15 GB/mo effective bandwidth — far too small for ~100 MB game loads; projects pause when credits exhaust (no overages — that part is a real hard cap) |
| Supabase Storage free | SKIP | **1 GB** | n/a | n/a | No | 1 GB < 5.33 GB needed; projects pause after 7 days inactivity |
| Firebase Storage (Spark) | SKIP | 5 GB (Spark) | n/a | n/a | **YES** — Cloud Storage now requires Blaze (linked billing account = card) since 2026-02-03 | Firebase Hosting Spark has 10 GB storage but only 360 MB/day transfer — too small |
| Bunny.net | SKIP (trial only) | none permanent | n/a | n/a | No card to *start* | 14-day free trial only, then $1/mo minimum + pay-as-you-go. Cheapest PAID fallback if ever needed (~$0.05/mo storage + $0.01/GB egress) |
| Tigris | SKIP | **5 GB/mo** | n/a | n/a | **No** — "No card to start" on official pricing page | 5 GB < 5.33 GB needed — fails by 0.33 GB |
| Filebase | SKIP | **5 GB** | n/a | n/a | n/a | 5 GB < 5.33 GB needed |
| Scaleway Object Storage | SKIP | **75 GB** + 75 GB/mo egress | n/a | Yes — official CORS docs | **YES** — card required to create a bucket | 75 GB would fit easily, but account activation requires binding a credit card (first-hand report + 2020 writeup); one 2026 comparison also lists its free tier as a 3-month trial |
| Storj | SKIP | 25 GB (was) | n/a | n/a | n/a | Free tier is now a 30-day trial only; Storj Labs filed Chapter 11 on 2026-07-26 — do not make it the only copy |
| Oracle Cloud Always Free | SKIP | **20 GB** object storage + 10 TB/mo egress | n/a | n/a | **YES** — card required for identity verification (Oracle's own FAQ: temporary $1–3 authorization hold) | 20 GB would fit; card kills it |
| Tebi | SKIP (dead) | 25 GB (was) | n/a | n/a | YES (for the free tier, when it existed) | **Closed March 31, 2026** |
| Wasabi | SKIP | none | n/a | n/a | n/a | No free tier; 30-day trial, $6.90/mo minimum after |

Already excluded in the 01 doc and not re-checked here: GitHub Releases as runtime CDN (no CORS, verified live), jsDelivr as whole-game host (403 above 20 MB, verified live), Cloudflare Pages full set (25 MiB/file cap), Vercel Hobby (non-commercial only), Git LFS (metered).

## 2. Why Backblaze B2 wins — the evidence

### 2.1 No card, verified three ways

- AgentDeals (read 2026-10-23): "Backblaze B2 does not require a credit card for the free tier."
- VerdantTCS setup guide: "You'll be asked for your name and email address and then to verify your email address on clicking sign up. Your first 10GB of storage is free... after that you'll need to add a payment method."
- Hacker News first-hand account: "Backblaze lets you create a new account w/o credit card info, within the free 10GB limit. You only need a credit card to go past 10GB. They have a big button to click to run free proof-of-concept tests that exceed 10GB." (Same author, on Scaleway: "they won't allow creating a bucket until credit card details are entered" — the contrast is the point.)

### CORRECTION 2026-10-27 — a PUBLIC bucket needs a card (the falsification)

The three sources above are all about **signup**, and they are still true. What they do not say — and what this doc wrongly assumed — is that a **public** bucket is also card-free. It is not:

- **Verified live in the browser 2026-10-27 ~11:09 CDT** (sign-in as fmmg.mars@gmail.com; the account already existed, with 4 private buckets from Oct 9–10: mars-music-archive, trippedd-show-footage, wizard-gang-masters, wizard-gang-voice; endpoint s3.us-east-005.backblazeb2.com): creating a PUBLIC bucket opens a dialog saying **"A payment history is required, or pay a one-time fee ($1.00 + appl. taxes) that is credited to your account"**, with card number / expiry / CVC / country / zip fields and a "Purchase and Make Bucket" button. No card was entered, no bucket was created. So the $1 is a real, card-based gate on the exact step the game needs.
- **Backblaze's own help docs say the same thing** (help.backblaze.com integration guides, re-checked 2026-10-27): "If this is your first time creating a public bucket, complete the following tasks to ensure that you have the correct permissions to create a public bucket: 1. Verify your email address. 2. Have a payment history on file, or use the credit card form to pay a small fee that is credited to your account balance."
- **What stays true:** signup is name + email only, and **private** buckets are card-free (the account already holds 4 of them, created Oct 9–10 with no card). The $1 fee is credited to the account balance — it is not a charge for storage — but it still requires a card, which is the owner's hard line. The fully card-free hosting path is therefore a private bucket + Cloudflare Worker proxy (§4).

### 2.2 The no-card state IS a hard cap — this is the guard the owner asked for

This is the finding that matters most, because the owner's R2 order was "set it up to keep it from going over the monthly limits and remember and actually set it up and save that":

- hafiz.dev (2026, first-hand): "B2 blocks uploads at 10 GB until you add a card... My first backup ran happily until it crossed 10 GB, then every upload failed with `storage cap exceeded`." And: "Adding a card fixes it, but it also flips every cap to 'No Cap'. So the account that was safely limited a minute ago now has unlimited daily spend. Go straight to **Caps & Alerts** and set them again by hand. Backblaze emails you at 75% and 100% of each cap."
- MSP360 knowledge base (updated 2026-10-16): "You have reached the limit of the free BackBlaze Daily Storage Cap... log on to the 'Caps & Alerts' page under your BackBlaze account and edit the cap limits."
- Backblaze's own API docs (`b2_download_file_by_name`): error codes `download_cap_exceeded` ("Usage cap exceeded") and `transaction_cap_exceeded` — "Daily transaction caps apply to non-paying accounts. To view or adjust your caps, sign in to your B2 Cloud Storage account online and select the Caps & Alerts link."

In plain language: **with no payment method on file there is nothing to charge, and overage is BLOCKED (uploads fail, downloads 403), not billed.** That is a real hard cap — the thing Cloudflare does not offer (§5). **Scope (correction 2026-10-27): this cap holds for the private-bucket path (§4).** It does not remove the $1 card gate on creating a public bucket (§2.1) — a no-card account can store and serve privately, but cannot make a bucket public until that gate is cleared. The one rule that must never be broken: **do NOT add a card to "fix" a cap hit** — adding one flips every cap to "No Cap" and the guard is gone.

### 2.3 Size fits with room

- 10 GB free storage vs a 5.33 GB set = ~4.7 GB headroom. Largest WH file ~90 MB vs the 5 GB single-PUT limit — no file splitting needed. (Max file: 5 GB single PUT / 10 TB multipart, per CloudsLinker 2026 comparison — secondary source; margin is so large the exact figure doesn't matter.)

### 2.4 CORS — official docs, works for browser fetch

Backblaze's own CORS guide and CLI docs: CORS rules live on the bucket; default is deny; rules specify `allowedOrigins` (can be `["https"]` = any HTTPS origin), `allowedOperations` (including `b2_download_file_by_name`, `b2_download_file_by_id`, `s3_get`, `s3_head`), `allowedHeaders`, `exposeHeaders`, `maxAgeSeconds`. Set in the web UI (bucket → CORS Rules, including a one-click "share with all origins" option) or via CLI/API (`b2 bucket update --cors-rules ...`). Up to 100 rules per bucket. The exact rule for the game is in §3 step 4.

### 2.5 Egress — the honest limit, and the free fix

- Backblaze's own page (opened 2026-10-27): "free egress up to three times your average monthly stored data, and free API transactions." 3x 5.33 GB ≈ **16 GB/mo ≈ ~160 full ~100 MB loads/mo**. Downloads past the free allowance are $0.01/GB — moot without a card, because the download cap blocks instead of billing (§2.2).
- **Free-egress fix if traffic grows — and the card-free serving path:** serve B2 through Cloudflare's CDN (the Cloudflare Bandwidth Alliance — Backblaze's own case study + multiple 2026 comparisons: egress via Cloudflare is free/unlimited). For the card-free path this is not a later add-on, it is the serving layer itself: the private bucket + Cloudflare Worker proxy in §4 routes every download through Cloudflare. At low traffic the fallback also works by direct private-bucket downloads with signed URLs, but the Worker proxy is the intended path.
- Transactions: 2,500/day free Class B & C (Rilavek 2026 table; VerdantTCS). A full session fetching ~50–100 GLBs burns ~50–100 of those, so ~25–50 full sessions/day before the daily transaction cap binds. The loader should not HEAD every file on every load.

### 2.6 Correction to the 01 doc's B2 line

The 01 doc said "10 GB storage, 1 GB/day egress free." The 1 GB/day figure is the **daily free download allowance**; the monthly egress allowance is **3x average stored volume** (Backblaze's own page). Both are true at once; the 3x figure is the one that decides how many players the free tier serves (~160 full loads/mo).

## 3. Recommended fallback — exact setup steps (Backblaze B2)

Do these once the owner gives the word to create the account — R2 is on hold per the 2026-10-27 ~10:04 CDT decision above, so B2 is the host to stand up first. No account is created by this research.

1. **Sign up** at backblaze.com (name + email only, verify email). **Do NOT add a payment method** — adding one flips every cap to "No Cap" (§2.2).
2. **Create bucket — DECISION POINT (correction 2026-10-27).** Two paths; the owner picks one:
   - **A. Public bucket — needs a card (owner-only).** Create bucket `western-heart-assets`, files **allPublic**. First public bucket on the account triggers the payment dialog: **"A payment history is required, or pay a one-time fee ($1.00 + appl. taxes) that is credited to your account"** — card number / expiry / CVC / country / zip, "Purchase and Make Bucket" button. The owner must enter the card himself; no agent enters it. The $1 is credited to the account balance (not a storage charge), but it is still a card, so this path is only open if the owner accepts it. Then copy the exact public URL from the bucket page (`https://f000.backblazeb2.com/file/<bucket>/<file>` — the `f000` number varies by account/region, do not guess it).
   - **B. Private bucket — fully card-free (recommended if no card).** Create bucket `western-heart-assets`, files **private**. No payment dialog, no card — the account already holds 4 private buckets made exactly this way. The bucket is then served publicly through the Cloudflare Worker proxy in §4; the loader points at the Worker URL, not at B2 directly.
3. **Caps & Alerts — set it up and SAVE it (the owner's guard order).** Open the Caps & Alerts page and confirm/record: storage cap 10 GB, daily download cap, daily transaction caps; email alerts at 75% and 100% (defaults per hafiz.dev — verify they are on). Record the cap values + a screenshot in this repo so the setup is saved and remembered, not just set once.
4. **CORS rule** on the bucket (UI: bucket → CORS Rules → "Share everything in this bucket with all origins", or the CLI rule below from Backblaze's own docs — `["https"]` = any HTTPS origin, which covers both Pages and itch):

```json
[{"corsRuleName":"downloadFromAnyOrigin","allowedOrigins":["https"],"allowedHeaders":["range"],"allowedOperations":["b2_download_file_by_id","b2_download_file_by_name"],"exposeHeaders":["x-bz-content-sha1"],"maxAgeSeconds":3600}]
```

5. **Upload** the same 2,242-file manifest as R2 (`tools/deploy/r2-upload-manifest.json` in western-heart) via the `b2` CLI, rclone, or `aws s3 sync` against the S3-compatible endpoint (`s3.<region>.backblazeb2.com`). No file splitting needed (largest file ~90 MB « 5 GB single-PUT limit). Verify with `b2 list-file-names` + SHA-1 spot checks (B2 stores a SHA-1 per file).
6. **Wire the loader:** set `ASSET_CONFIG.remoteBase` to the serving URL — the B2 public URL for path A, or the Cloudflare Worker URL for path B (§4) — the same one-line config as the R2 plan (WH PR #1152). Keep jsDelivr as the ≤20 MB fast path.
7. **Verify with own eyes:** `curl -I -H "Origin: https://mhvnsnt.github.io" <b2-file-url>` shows `Access-Control-Allow-Origin: *` (or the origin); then a real browser `fetch()` of a >25 MB GLB; then a full fight loads.
8. **Guard (ongoing):** check the Caps & Alerts page weekly; storage must stay ≤10 GB. If downloads start 403ing with `download_cap_exceeded`, that is the cap working, not a bug — do NOT add a card to "fix" it; wait for the daily reset or move traffic to the Cloudflare-fronted path (§4).

## 4. Card-free alternative — PRIVATE B2 bucket + Cloudflare Worker proxy (the correction's answer)

This is the path that keeps hosting fully card-free after the §2.1 correction: the bucket stays **private** (no $1 gate), and a Cloudflare Worker serves it publicly. The pattern is real and documented by Backblaze itself — it is not a hack.

**How it works:** the Worker holds a B2 application key (stored as an encrypted Cloudflare secret, never in source code) and signs each incoming browser request with AWS SigV4 against B2's S3-compatible API, fetches the file from the private bucket, and streams the response back to the browser. The browser never talks to B2 directly and never sees the key. Backblaze's own docs: "Deliver Private Backblaze B2 Content Through Cloudflare CDN" (backblaze.com/docs/cloud-storage-deliver-private-backblaze-b2-content-through-cloudflare-cdn) and the blog "How to Serve Data From a Private Bucket with a Cloudflare Worker"; reference implementation: backblaze-b2-samples/cloudflare-b2 (signs requests with `B2_APPLICATION_KEY_ID` / `B2_APPLICATION_KEY`, GET + HEAD only, bucket listing blocked by default).

**Setup steps (once the owner gives the word):**
1. Create the bucket **private** (§3 step 2, path B) and upload the manifest as in §3 step 5.
2. In the B2 console, create an application key scoped to that one bucket, download-only (`readFiles`); note the keyID + applicationKey once.
3. In the Cloudflare dashboard (account already has **Workers Free Active**, verified 2026-10-27 — no new subscription), create a Worker from the backblaze-b2-samples/cloudflare-b2 code; set `B2_APPLICATION_KEY_ID` as a variable and `B2_APPLICATION_KEY` as an **encrypted secret** (Backblaze's own doc: never save secrets in source files).
4. Set the bucket's info to `{"Cache-Control":"public"}` (optionally `"public, max-age=86400"`) — Backblaze's own doc: by default Cloudflare does **not** cache content when the request carries an authorization header, so without this every request hits B2.
5. **CORS is the Worker's job, not the bucket's.** The browser talks to the Worker, so B2's bucket CORS rules do not apply to these responses — the Worker must add `Access-Control-Allow-Origin` (and answer `OPTIONS` preflights) in its own response. Verify with `curl -I -H "Origin: https://mhvnsnt.github.io"` against the Worker URL before wiring the loader (§3 step 7).
6. Point `ASSET_CONFIG.remoteBase` at the Worker URL (§3 step 6, path B).

**Limits — stated honestly:**
- **Workers Free: 100,000 requests/day, 10 ms CPU per invocation, hard stop** (requests beyond the cap fail; no overage, no bill — verified against Cloudflare's pricing/limits pages via 2026 roundups, checked 2026-10-27). A full session fetches ~50–100 GLBs, so ~1,000–2,000 full sessions/day before the request cap binds — and the B2 daily transaction cap (2,500/day free Class B/C) binds first on cache misses, so caching (§4 step 4) is load-bearing, not optional.
- **Bandwidth Alliance — what is and is not verified:** Backblaze's own guide presents this Worker path as serving private B2 content through Cloudflare CDN with "free data transfer between Backblaze B2 and Cloudflare." What I could **not** verify from a primary source is whether the free-egress treatment applies byte-for-byte identically to Worker-origin fetches vs plain CDN cache fetches. Cache hits never touch B2 at all, so the accounting that matters is cache-miss traffic — **check the B2 Caps & Alerts / usage page after stand-up and record what it shows**; do not claim free egress for the Worker path as settled fact until that first usage reading.
- **No built-in CDN caching unless configured** — step 4 above is what turns the Worker into a cached CDN path; skip it and every download is a B2 transaction.
- **Key handling:** a leaked application key exposes the whole bucket — scope it to the one bucket, download-only, and rotate it if it ever appears in a log, a repo, or a screenshot.

## 5. Cloudflare R2 guard — what actually exists (for the guard setup, not a fallback)

The owner ordered (2026-10-27 ~09:49 CDT): "set it up to keep it from going over the monthly limits and remember and actually set it up and save that." Here is what exists, verified against Cloudflare's own docs today:

- **Budget alerts** ([developers.cloudflare.com/billing/manage/budget-alerts/](https://developers.cloudflare.com/billing/manage/budget-alerts/), checked 2026-10-27): "Budget alerts are informational only. **They do not pause or cap usage.**" They email when cumulative usage-based spend crosses a dollar threshold you define; they reset each billing period. Path: Manage Account > Billing > Billable Usage > Create budget alert. **PayGo-only** — creatable only once the R2 subscription exists.
- **Default $10 account-level alert** (June 2026 changelog, via ppc.land 2026 writeup): for eligible PayGo accounts — also informational only, fires the day after a threshold is crossed (usage processed once a day).
- **Usage-based billing alerts:** also notify-only ("does not limit product usage") — and on this account they cannot even be created right now ("No eligible usage-based products are available on this account", verified in the dashboard 2026-10-27, since R2 isn't subscribed).
- **Bottom line, stated plainly: Cloudflare offers NO hard spending cap and NO alert that can stop R2 usage.** The $36,000 queue-loop bill writeup (ppc.land, 2026) is the public cautionary tale. The owner's "cannot go over the free limits" requirement cannot be met by a dashboard setting on Cloudflare. The real R2 guard is three things: (a) the set stays 5.33 GB vs the 10 GB free tier — size discipline, checked at every upload; (b) a budget alert at $0.01 or $1 once the subscription exists; (c) weekly usage checks against the R2 dashboard. **If a hard cap is ever non-negotiable, B2's no-card state is the only host in this research that has one** — a genuine reason to prefer B2 as the fallback even though R2's egress is freer. Per the owner's 2026-10-27 ~10:04 CDT decision, R2 stays untouched until the fallback is stood up — no subscription, no bucket, no public URL.

## 6. What would break / honest limits

- **Public-bucket $1 card gate (§2.1):** the direct public-B2 path is blocked until the owner pays $1 by card (or has payment history). The card-free path is §4.
- **Worker request cap (§4):** 100,000 Worker requests/day free, hard stop; ~1,000–2,000 full sessions/day at ~50–100 GLBs per session, less if caching is misconfigured.

- **B2 free egress ~16 GB/mo:** a viral week (thousands of players) exhausts it; downloads then 403 until the cap resets. Mitigation: Cloudflare CDN in front (Bandwidth Alliance = free egress), or split traffic R2 + B2.
- **B2 has no built-in CDN:** first-byte latency is higher than R2/jsDelivr edge; acceptable for GLB loads, not ideal.
- **10 GB storage ceiling:** the set is 5.33 GB today; roster growth past 10 GB needs either a card (owner decision) or pruning.
- **Transaction cap 2,500/day free Class B/C:** heavy listing/HEAD traffic counts; the loader should not HEAD every file per load.
- **IDrive e2 — settled, SKIP (correction 2026-10-27):** IDrive's own e2 page prices monthly storage at "$6/TB/Month (Try with 10 GB Free)" with yearly plans starting at 1 TB ($59.50/year) — the 10 GB is a trial allowance, not a permanent free tier (verified live on idrive.com/s3-storage-e2/e2-vs-microsoft-azure, 2026-10-27; AeroFTP's provider doc, checked 2026-07-30, reads the pricing page the same way: "No permanent free tier... 1 TB minimum charge"). The "permanently free, no credit card" claims in secondary sources describe IDrive's *backup* Basic plan (10 GB free, no card — IDrive's own signup pages confirm that for backup), not e2 object storage. The conflict is resolved by keeping the products apart: e2 is not a free host.
- **R2 guard gap (§5):** if R2 is the live host, the only thing standing between the game and a bill is size discipline + email alerts. Record the budget-alert threshold and the current usage in the repo the day the subscription is created.

## 7. Sources (every limit claimed, checked 2026-10-27)

- Backblaze B2 official page (opened) — https://www.backblaze.com/b2/cloud-storage.html — "free egress up to three times your average monthly stored data, and free API transactions"; S3-compatible.
- Backblaze CORS, CLI docs — https://www.backblaze.com:8443/docs/cloud-storage-enable-cors-with-the-cli
- Backblaze CORS guide — https://www.backblaze.com/blog/?p=103250 — default deny; per-bucket rules; "share with all origins" UI option.
- Backblaze API docs, download caps — https://www.backblaze.com:8443/apidocs/b2-download-file-by-name — `download_cap_exceeded` / `transaction_cap_exceeded`; "Daily transaction caps apply to non-paying accounts."
- B2 no-card hard cap, first-hand — https://hafiz.dev/blog/macbook-offsite-backups-restic-backblaze-b2 — "B2 blocks uploads at 10 GB until you add a card"; caps flip to "No Cap" when a card is added; email at 75% and 100%.
- B2 storage-cap error, KB (updated 2026-10-16) — https://kb.msp360.com/cloud-vendors/backblazeb2/unable-to-upload-files-to-b2-due-to-exceeded-storage-cap
- B2 signup + pricing, guide — https://verdanttcs.com/knowledge_base/create-and-set-your-backblaze-b2-api-credentials/ — name + email only; 10 GB free; $0.005/GB/mo storage; $0.01/GB downloads; 1 GB/day free downloads; 2,500/day free Class B & C.
- B2 public bucket payment requirement, Backblaze's own help docs — https://help.backblaze.com/hc/en-us/articles/360047779293-Quickstart-Guide-for-StorageCraft-ImageManager-and-Backblaze-B2 (same text in every B2 integration guide, re-checked 2026-10-27): "If this is your first time creating a public bucket... 1. Verify your email address. 2. Have a payment history on file, or use the credit card form to pay a small fee that is credited to your account balance." Corroborated live in the browser 2026-10-27 ~11:09 CDT on the real account (fmmg.mars@gmail.com; 4 private buckets already on the account): dialog "A payment history is required, or pay a one-time fee ($1.00 + appl. taxes) that is credited to your account", card fields + "Purchase and Make Bucket" button; no card entered, no bucket created.
- Private B2 bucket + Cloudflare Worker proxy, Backblaze's own docs — https://www.backblaze.com/docs/cloud-storage-deliver-private-backblaze-b2-content-through-cloudflare-cdn ("You can use Cloudflare Workers to serve data from a *private* Backblaze B2 Cloud Storage bucket... free data transfer between Backblaze B2 and Cloudflare"; set bucket info `{"Cache-Control":"public"}` or Cloudflare will not cache authorized requests) and https://www.backblaze.com/blog/how-to-serve-data-from-a-private-bucket-with-a-cloudflare-worker/ (Worker signs each request with the application key + key ID, streams the response back). Reference implementation: backblaze-b2-samples/cloudflare-b2 — https://deepwiki.com/backblaze-b2-samples/cloudflare-b2 (GET/HEAD only, listing blocked, key as Cloudflare secret).
- Cloudflare Workers Free limits — https://heygalatea.com/guides/how-to-deploy-astro-on-cloudflare-workers/ (from Cloudflare's Workers pricing + limits pages, checked Oct 24, 2026: 100,000 requests/day, 10 ms CPU, free) and https://blog.blazingcdn.com/en-us/cloudflares-pricing-for-developers-a-closer-look-at-workers-pages (Free: 100,000 requests/day, hard stop, no overage). Bandwidth Alliance free-egress-for-Worker-path NOT verified byte-for-byte from a primary source — flagged as open in §4.
- B2 max file size — https://cloudslinker.com/backblaze-b2-vs-cloudflare-r2 (secondary): 5 GB single PUT / 10 TB multipart.
- Cloudflare budget alerts, official docs — https://developers.cloudflare.com/billing/manage/budget-alerts/ — "Budget alerts are informational only. They do not pause or cap usage."
- Cloudflare no-hard-cap corroboration — https://ppc.land/developer-faces-36-000-cloudflare-bill-after-queue-loop-post-says/ — "$36,000 bill"; default $10 alert (June 2026 changelog) informational only.
- Tebi closed 2026-03-31 — http://blog.51sec.org/2023/04/integrate-sharex-with-free-forever-s3.html — "[Updated] - Tebi.io closed on March 31, 2026"; free tier required a credit card.
- Oracle card requirement, Oracle's own FAQ — https://www.oracle.com/ba/database/data-warehouse-trial.html — "we use your contact information and credit/debit card information for account setup and identity verification"; temporary authorization hold, removed in 3–5 days.
- Scaleway card requirement, first-hand — https://news.ycombinator.com/item?id=28932209 — "they won't allow creating a bucket until credit card details are entered"; contrasted with B2 no-card signup.
- Scaleway card requirement, writeup — https://en.xiaoz.org/post/14281 — "Activating the account requires binding a credit card"; 75 GB free storage + 75 GB free traffic.
- Scaleway CORS, official docs — https://www.scaleway.com/en/docs/object-storage/api-cli/setting-cors-rules/?ref=botzenhart.io
- IDrive e2 free tier — SETTLED 2026-10-27, SKIP. IDrive's OWN e2 page — https://www.idrive.com/s3-storage-e2/e2-vs-microsoft-azure (opened 2026-10-27): monthly storage "$6/TB/Month (Try with 10 GB Free)", yearly plans from 1 TB ($59.50/year). AeroFTP provider doc — https://docs.aeroftp.app/providers/idrive-e2.html — reads the same pricing page: "No permanent free tier. The pricing page offers 'Try with 10GB Free' as a trial allowance... 1 TB minimum charge" (checked 2026-07-30). The CloudsLinker line "Free tier: 10 GB of storage permanently free, no credit card required" (https://www.cloudslinker.com/support-clouds/idrive/) is contradicted by IDrive's own wording and is not used. Note: IDrive's *backup* Basic plan (10 GB free, no card) is a different product — that is where the "permanently free" claims come from.
- Bunny.net trial-only — https://www.cloudpicked.com/bunnycdn-review-en.html — "14-day free trial, no credit card required; $1/month minimum"; storage $0.01/GB, CDN $0.01/GB EU/NA. And https://dev.to/nayankyada/bunny-stream-pricing-2026-free-trial-limits-storage-costs-when-to-upgrade-2j56 — "doesn't have a free tier in the traditional sense — it has a 14-day free trial."
- Free-S3-providers list — https://raw.githubusercontent.com/mmichaelb/terraform-free-s3-providers/main/README.adoc — Scaleway 75 GB, B2 10 GB, R2 10 GB, Oracle 10 GB, Tebi 25 GB, Filebase 5 GB, Storj 25 GB.
- Requirement numbers — `research-friction-20261025/01-deploy-pages-limit.md` (01 doc): 176 GLBs >20 MB (5,914 MB), 98 >25 MiB (4,178 MB); R2 manifest 2,242 models / 5,329.7 MB (WH PR #1152).
- Supabase (1 GB free storage, 7-day pause), Firebase (Blaze/card required since 2026-02-03; Hosting Spark 360 MB/day), Netlify (300 credits/mo, ~15 GB/mo effective), Storj (30-day trial; Chapter 11 2026-07-26), Tigris (5 GB/mo, "No card to start" on official pricing page), Filebase (5 GB): verified 2026-10-27 in the prior research pass this session; no URLs re-captured in this doc's pass.
