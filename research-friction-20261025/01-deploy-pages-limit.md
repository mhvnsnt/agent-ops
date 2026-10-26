# Deploy vs GitHub Pages 1 GB limit — Western Heart web game

**Date checked:** 2026-10-25/26 (all limits below verified against live sources on those dates; live `curl` probes run 2026-10-26 ~04:08 UTC).
**Context:** [[RESEARCH-PULLIN-INDEX]] · [[FRICTION-RESEARCH-2026-10-19]] (releases-as-store decided there: <2 GiB/asset, 1000 assets/release, no total-size/bandwidth cap — this doc does NOT re-decide that).
**Problem:** `tools/deploy/build_pages.py` builds a gh-pages branch from `origin/main` (roots `game/**`, `customization/creation-suite-ui/**`, `packages/creation-suite/{src,ui,ui2}/**`, plus a reference closure). Current deploy set = **5,969 MB** vs GitHub Pages' **1 GB published-site limit**. Live site `https://mhvnsnt.github.io/western-heart/` frozen on the Oct 24 build. Owner decision pending: "what gets cut".
**Repo:** `mhvnsnt/western-heart`, 6,637 `.glb` files on main (6,619 counted in the live tree probe below; the git-trees API response was truncated, so counts are lower bounds).

## 0. The numbers that decide everything (measured live, 2026-10-26)

From `gh api repos/mhvnsnt/western-heart/git/trees/main?recursive=1` (truncated at 100k entries — 57,929 files listed, 12,650.8 MB total, so these are lower bounds):

| Slice | Files | Size |
|---|---|---|
| All `.glb` in repo | 6,619 | 8,086.3 MB |
| `.glb` **>20 MB** (176 files) | 176 | **5,914 MB (73% of all GLB bytes)** |
| `.glb` **>25 MiB** (98 files) | 98 | **4,178 MB** |
| `.glb` ≤20 MB | 6,443 | 2,172 MB |
| Median `.glb` | — | 0.01 MB (most GLBs are tiny props/attire pieces) |
| `roster/` (creation-suite roster) | 708 | 6,131.8 MB (GLB 5,991.2 MB) |
| `game/` | 2,386 | 1,745.8 MB (GLB 1,141.9 MB) |
| `game/assets/models/` | 75 | 1,112.9 MB |
| `customization/` | 9,790 | 502.0 MB (GLB 224.7 MB) |
| `game/` non-GLB (js 9.0 MB, json 260.7 MB, mp3 236.8 MB, png 49.9 MB, ogg 30.6 MB, …) | — | ~604 MB |

Two facts fall out of this:

1. **The bloat is concentrated, not diffuse.** 176 huge files hold ~3/4 of all GLB bytes. Everything else is small. Any fix that handles those 176 files handles the problem.
2. **`roster/` (6.1 GB) is mostly NOT in the deploy set.** `build_pages.py` deliberately does not follow `customization/creation-suite-ui/data/roster-attires.json` (2.0 GB of attire models; following it would put the site at 3.7 GB per the script's own comment). The 5,969 MB deploy set is the closure over `game/` + creation-suite roots + referenced files — dominated by `game/assets/models/` fighters and referenced roster/attire files.

## 1. Q1 — GitHub Pages limits, confirmed from live docs

Source: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits (checked 2026-10-25):

> - "GitHub Pages source repositories have a recommended limit of 1 GB."
> - "**Published GitHub Pages sites may be no larger than 1 GB.**"
> - "GitHub Pages deployments will timeout if they take longer than 10 minutes."
> - "GitHub Pages sites have a *soft* bandwidth limit of 100 GB per month."
> - "GitHub Pages sites have a *soft* limit of 10 builds per hour. This limit does not apply if you build and publish your site with a custom GitHub Actions workflow."

Other relevant limits: GitHub blocks individual files >100 MB in a git push (25 MB via browser upload) — the deploy script already flags files >95 MB. GitHub's own remedy text on the limits page is telling: if you exceed the quotas they suggest "putting a third-party content distribution network (CDN) in front of your site, making use of other GitHub features such as releases, or moving to a different hosting service." I.e. GitHub itself blesses the split-hosting shape in Option A — with one catch found in §2.

**Verdict: the 1 GB published-site cap is hard and confirmed. 5,969 MB is 5.8× over. The full set can never ship on Pages as-is.**

## 2. Q2 — Option A: shell on Pages + GLBs lazy-loaded from GitHub Releases

### 2a. Release-asset CORS — TESTED LIVE, and it FAILS

Probed 2026-10-26 ~04:08 UTC with `curl -I -H "Origin: https://mhvnsnt.github.io"` against the real release asset `https://github.com/mhvnsnt/western-heart/releases/download/tekken6-psp-v1/tekken6-psp.iso`:

- `github.com/.../releases/download/...` → **HTTP 302** to `release-assets.githubusercontent.com/...` with a signed query string. **No `Access-Control-Allow-Origin` header.**
- Final host `release-assets.githubusercontent.com` → **HTTP 200**, `Content-Type: application/octet-stream`, `Content-Disposition: attachment`, `Accept-Ranges: bytes`. **Still no `Access-Control-Allow-Origin` header**, even with an `Origin` header sent.
- The signed URL expires in ~1 hour (`se=2026-10-26T05:00:02Z` on a 04:08 request) — every page load must re-resolve the redirect; you cannot hardcode the final URL.
- Side note: the 302 carries a ~9 KB `Content-Security-Policy` header, which is already breaking strict HTTP clients in the wild (hacs/integration#5643, 2026-10-22: aiohttp's 8,190-byte line limit aborts the download).

Why this kills the naive version of Option A: three.js `GLTFLoader` loads models with `fetch()`/XHR, and the browser will refuse to expose the response body to JavaScript without `Access-Control-Allow-Origin`. A plain `<a href>` download or a navigation works (no CORS check), but **in-game lazy loading from a release asset does not**. This matches independent write-ups (https://corsfix.com/blog/fetch-github-release, 2025-05-06: "GitHub's release CDN isn't set up for direct browser fetches").

**Verdict on releases-as-runtime-CDN: SKIP for direct browser fetch.** Releases stay the *store* (already decided 2026-10-19, unmetered, <2 GiB/asset) — but they cannot be the runtime asset server without a CORS-adding proxy in front. A Cloudflare Worker (free tier: 100,000 requests/day) relaying `release → Worker adds ACAO:* → browser` is the known fix, but it adds a moving part and the Worker would stream multi-GB through the free CPU/egress path — workable for occasional fighter loads, not elegant. Prefer a host that sends CORS natively (§2b/§6).

### 2b. jsDelivr serving repo files — TESTED LIVE, works up to 20 MB, 403 above

Probed live 2026-10-26 against real repo files, `Origin: https://mhvnsnt.github.io`:

| File | Result |
|---|---|
| `cdn.jsdelivr.net/gh/mhvnsnt/western-heart@main/AGENTS.md` | 200, `Content-Type: text/markdown`, `Access-Control-Allow-Origin: *` |
| `.../game/assets/models/awa-pop.glb` (405 KB) | 200, **`Content-Type: model/gltf-binary`**, `Access-Control-Allow-Origin: *` |
| `.../game/assets/models/cape-jones.glb` (86 MB) | **403 Forbidden**, `Content-Length: 49` |
| `raw.githubusercontent.com/.../awa-pop.glb` (405 KB) | 200, `Access-Control-Allow-Origin: *`, `Content-Type: application/octet-stream`, `Cache-Control: max-age=300` |

Documented limits (jsDelivr README, via https://deepwiki.com/jsdelivr/jsdelivr/3-usage-guide): **single files >20 MB (for GitHub) are not supported by default; packages >150 MB are not supported**; branch URLs cache 12 h, version/commit URLs cache up to 1 year and are permanent in S3; cache can be purged only for semver versions. Limits can be raised by opening an issue in the jsDelivr repo.

Applied to our numbers: jsDelivr would serve 6,443 of 6,619 GLBs (2,172 MB) — but **not the 176 files >20 MB (5,914 MB) that are the whole problem**. It is a real, free, CORS-clean CDN for the small files and useless for the big ones. Also note jsDelivr serves from *committed repo files*, so the big GLBs would still have to live in the git repo (they do today) — no help with repo size.

**Verdict on jsDelivr: PARTIAL — recommend for small assets only (≤20 MB files, correct `model/gltf-binary` MIME, CORS clean, global CDN, no account). Skip as the whole-game solution.**

### 2c. Statically / githack

- **Statically** (https://statically.io/): free CDN for GitHub/GitLab/Bitbucket/npm, no account, powered by bunny.net + Cloudflare. URL form `https://cdn.statically.io/gh/:user/:repo@:tag/:file`. No published per-file size limit found — but also no published SLA, and it is a small one-person service (its `/img/` endpoint was already disabled "due to abuse and high traffic"). **Verdict: SKIP as primary; acceptable as a fallback mirror for small files only. Unverified at 90 MB — do not bet the game on it.**
- **raw.githack.com**: same class, serves `raw.githubusercontent.com` with correct MIME. Same verdict.
- **raw.githubusercontent.com itself**: verified live to send `Access-Control-Allow-Origin: *` and serve a 405 KB `.glb` (as `application/octet-stream`, which is fine for `fetch()` + `GLTFLoader.parse` — MIME doesn't matter for arrayBuffer parsing). No documented per-file cap found. BUT: `Cache-Control: max-age=300`, no edge CDN, no SLA, and GitHub's guidance is not to use it as a CDN; a 92 MB file over it is untested here. **Verdict: viable emergency fallback for small files; not the plan.**

## 3. Q3 — Option B: itch.io HTML5 hosting (the money unlock)

Official docs: https://itch.io/docs/creators/faq and https://itch.io/docs/creators/html5 (HTML5 doc corroborated by https://portalready.world/portals/itch-io/ and https://app.cinevva.com/guides/itch-io-launch-guide, both checked 2026-10-25).

### HTML5 (play-in-browser) limits — hard caps

ZIP file requirements from itch.io's HTML5 docs:

- **≤1,000 files** after extraction (files + directories counted; Babylon.js forum reports the page errors instead of the game if exceeded)
- **≤500 MB total** extracted
- **≤200 MB per single file**
- File names ≤240 chars incl. path, case-sensitive, UTF-8; only `.zip` accepted
- Game served from a subdirectory of itch.io's HTML CDN: absolute paths (`/...`) break; requests to other domains must be HTTPS (so lazy-loading GLBs from R2/jsDelivr is *allowed*); the CDN gzips HTML/JS/CSS/SVG/WASM/WAV/**GLB**/PCK itself

**The shell fits easily** (§5 estimates 70–170 MB, a few hundred files). The full 5,969 MB set does not — same split-hosting shape as Option A, but on itch's player instead of Pages.

### Downloadable builds — much bigger headroom

- Web uploader: 1 GB default; **butler CLI: 2 GB default**; limit raised on request (community reports: standard increase to 4 GB for anyone who asks; non-standard 5+ GB harder). Butler docs/community report a **30 GB uncompressed hard cap** per build — that figure is *not* verified against itch.io's own docs, treat as community-reported.
- Butler (https://itch.io/docs/butler/) is a free CLI (itch.io's own tool, no license cost): resumable, delta/patch uploads — only changed files re-upload. Since May 2026 the itch desktop app (26.12.0+) wraps butler in a GUI upload section with a change preview — relevant because the owner is phone-only: **the desktop-app GUI path is the phone-friendly one only if he has a PC; the CLI path is a lane job, not an owner job.**

### Money: the part that matters most

- **Open revenue sharing:** the seller picks itch.io's cut from **0% to 100%, default 10%**. Payment-processor fees separate (Stripe ~2.9% + $0.30).
- **Two payout models** (https://itch.io/docs/creators/payments.amp, checked 2026-10-25):
  - **Direct to you:** each purchase goes straight to the seller's own PayPal or Stripe account. No itch.io threshold. Seller handles VAT/tax themselves.
  - **Collected by itch.io, paid later:** revenue accumulates in the itch.io balance; **7-day hold** after purchase; **$5.00 USD minimum** to request a payout; payout review takes at least 7 days (typically 10–14); paid out via **PayPal or Payoneer**; requires a **tax interview** (one-time $3 verification fee per the payments docs) and a selected payout method. Max 3 payouts in progress. Unclaimed earnings over a year can incur a charge.
- **Critical constraint for the browser game: HTML5 games can only take donations.** To charge for access, the project kind must be **Downloadable**. So the money path is: free playable HTML5 shell on itch (donations on) **+** a paid Downloadable build (or the same game sold as a download) — the browser version alone cannot be sold.
- Account/project limits for new accounts: soft cap 20 project pages, 10 files per page — both raised on request. No approval queue for free games.

**Verdict on itch.io: RECOMMEND — as the money + distribution path, not as the whole-game host.** Ship the shell as an HTML5 project (≤500 MB, ≤1,000 files — it fits), lazy-load GLBs from R2 (§6), turn donations on, and set up the payout mode *now* (Direct to PayPal/Stripe if he has one, else Collected) so the account is money-ready before the game is. The 6 GB full build can go up as a Downloadable via butler later (2 GB default cap needs a support request for an increase; 30 GB community-reported hard cap leaves room).

## 4. Q4 — Option C: Cloudflare Pages / Netlify / Vercel free tiers

### Cloudflare Pages (free)

Source: https://developers.cloudflare.com/pages/platform/limits/ (checked 2026-10-25).

| Limit | Free |
|---|---|
| Builds/month | 500 (1 concurrent, 20-min timeout) |
| Files per site | **20,000** |
| **Max file size** | **25 MiB — on every plan, including paid** |
| Custom domains | 100/project |
| Bandwidth (static) | **Unlimited** |

**The 25 MiB per-file cap kills the full set outright**: 98 GLBs >25 MiB (4,178 MB) cannot be deployed at all, on any plan. The 20,000-file cap is also a risk for the full set (57,929 files listed in the repo tree, truncated). Pages is **viable for the shell only** — and even then only if every shell-bundled GLB is ≤25 MiB (pick small fighters for the bundled set, or keep all fighters in R2). Unlimited bandwidth is the best-in-class trait here.

### Netlify (free)

- **100 GB bandwidth/month, 300 build minutes/month** (free plan; Netlify moved to a credit system in late 2025 — some 2026 roundups now report the free plan as ~15 GB effective under 300 credits/mo, so treat the 100 GB figure as *uncertain, verify on the pricing page at signup*).
- **No documented total site-size cap**: Netlify support forum (2019, https://answers.netlify.com/t/free-plan-website-size-limit/2084): "there is no intended size limitation in normal use" — the old 100 MB error was a bug triggered by newlines in filenames. Netlify's own Drop-vs-Vercel page (https://www.netlify.com/knowledge-base/netlify-drop-vs-vercel-drop/) says Drop works best under 50 MB total and files >10 MB may stall — **use the Netlify CLI, not drag-and-drop, for a multi-GB deploy**.
- **Notable: the repo already has a Netlify site.** `game/netlify.toml` on main (checked 2026-10-26) publishes `game/` as root and proxies `/roster/*`, `/customization/*`, `/packages/*`, `/game/*`, `/stages/*` (200 rewrites) to `https://mhvnsnt.github.io/western-heart/...`. The team already leans on Netlify as a second host — but note those proxies point *at Pages*, so Netlify currently inherits the Pages 1 GB problem rather than solving it.
- Bandwidth math: at 100 GB/mo, ~1,000 full ~100 MB game loads exhaust the month. Fine for testing, not for a hit.

**Verdict on Netlify: RECOMMEND as shell host / second mirror.** Free, no total-size cap documented, CLI deploys handle big files, commercial use allowed on free. But it does not solve the asset problem by itself — same split-hosting shape, and the 100 GB bandwidth cap binds before Pages' does.

### Vercel (Hobby/free)

- Hobby: **100 GB bandwidth/mo, 6,000 build minutes/mo, 1 concurrent build, 100 deployments/day** (multiple 2026 pricing roundups; Vercel's own pricing page).
- **Hobby is personal, non-commercial use only.** A revenue-generating game on Hobby violates the terms; commercial use requires Pro at **$20/user/month** + metered usage (bandwidth overage ~$0.15/GB or flat-rate CDN tiers for new teams).
- No total site-size cap claimed in the sources checked; Vercel Blob storage is a separate paid product (Hobby 1 GB).

**Verdict on Vercel: SKIP.** The non-commercial clause disqualifies it for a game whose whole point is making money; Pro's metered bandwidth is the wrong cost shape for 100 MB game loads.

## 5. Q5 — Option D: shrink the deploy set (what is the floor?)

No shrinking work was done — this is an assessment only, from the live tree data in §0.

**Shell-only set (what Pages would need to host):**

| Component | Size (measured or estimated) |
|---|---|
| Game code: `game/js/` 2.5 MB + `game/*.js`/`*.mjs`/`*.css` | **~10 MB** |
| UI + portraits: `game/assets/ui/` 0.1 MB + `game/assets/portraits/` 7.3 MB | **~7.5 MB** |
| One stage (from `game/assets/stages/`, 53.4 MB for all stages) | **~1–5 MB** |
| Two fighters, e.g. Demonio 8.8 MB + Jin 26.4 MB (or smaller picks) | **~10–35 MB** |
| Their moveset JSONs + a couple of music tracks | **~10–30 MB** |
| Creation-suite UI (`packages/creation-suite/{src,ui,ui2}/` 6.2 MB total) | **~6 MB** |
| **Shell total** | **~70–170 MB** |

Even the pessimistic end (~170 MB) is **6× under the 1 GB cap**. The shell could carry 4–6 fighters and still fit. The full `game/` non-GLB content is ~604 MB, but the closure only pulls referenced files — the shell is the floor, not the whole `game/` tree.

**What "cutting" would actually mean:** nothing has to be cut from the *game*, only from the *deploy*. The 176 big GLBs (5,914 MB) move to the asset host; the other 6,443 small GLBs (2,172 MB) could stay on Pages in theory — but they alone are 2.2× over the cap, so even the small set must be split. The honest floor for a *playable* Pages deploy is the shell above; everything else loads on demand.

**Related shrink lever (not done here, noted for a later lane):** the 176 big GLBs are uncompressed Tripo exports. `gltfpack` (MIT, already wired in `western-heart/tools/procgen/gltf-delivery/` per [[FRICTION-RESEARCH-2026-10-19]] — 22 MB → 20 MB verified on one file) and Draco/KTX2 compression could cut fighter sizes materially, but compression is a *separate* work item: it changes load code (Draco decoder) and needs per-fighter verification. It lowers the asset-host bill; it does not remove the need for split hosting, because even 2,172 MB of small GLBs is over 1 GB.

## 6. Q6 — Other free/industry-standard routes

### Cloudflare R2 + Pages — the strongest pairing

Source: https://developers.cloudflare.com/r2/pricing/ (checked 2026-10-25).

| | Free tier (monthly, recurring) | Paid |
|---|---|---|
| Storage | **10 GB** | $0.015/GB-mo |
| Class A ops (writes/lists) | 1M | $4.50/M |
| Class B ops (reads) | 10M | $0.36/M |
| **Egress** | **$0, unlimited** | $0 |

**The entire 5,969 MB deploy set fits inside the free 10 GB storage tier.** At paid rates the same 6 GB would cost ~$0.09/month. Zero egress is the decisive trait — a player downloading 100 MB of fighters costs nothing, unlike S3 ($0.09/GB) or metered hosts. R2 buckets support configurable CORS rules (documented R2 feature — set `Access-Control-Allow-Origin: *` on the bucket; verify at setup) and public buckets serve over `*.r2.dev` or a custom domain. Upload via `wrangler r2` CLI, S3-compatible API, or the dashboard — a lane job, not an owner job.

**Verdict: RECOMMEND — R2 is the asset host in the recommended path.** Cost $0 at current size; the only open check is signup (Cloudflare may ask for a payment method on file for R2 even on the free tier — verify at setup, do not auto-signup).

### Backblaze B2 — fallback object store

Free tier: 10 GB storage, 1 GB/day egress free; paid $0.006/GB-mo storage, $0.01/GB egress (free via the Cloudflare Bandwidth Alliance when routed through Cloudflare). S3-compatible. **Verdict: viable fallback if R2 signup blocks; R2's $0 egress is simpler.**

### Other notes

- **Git LFS: already excluded** 2026-10-19 (metered bandwidth, 10 GiB free) — do not revisit.
- **GitHub Actions artifacts: 90-day cap** — excluded 2026-10-19.
- **A Cloudflare Worker as a CORS proxy in front of Releases** (§2a): technically works, free tier 100k req/day, but streams multi-GB through Workers and re-resolves a 1-hour signed URL per load. **Fallback only.**

## Verdict table

| Option | Verdict | License / cost | Why |
|---|---|---|---|
| Full set on GitHub Pages | **Skip** (impossible) | Free | 1 GB hard cap confirmed from GitHub docs; set is 5,969 MB |
| Shell on Pages + GLBs from GitHub Releases (direct fetch) | **Skip** | Free | Verified live: release assets send **no CORS headers**; `fetch()` from the game will fail. Releases stay the store, not the runtime CDN |
| Shell on Pages + small GLBs via jsDelivr | **Recommend (partial)** | Free, no account | Verified live: 200 + `model/gltf-binary` + `ACAO:*` for ≤20 MB; 403 above 20 MB. Covers 6,443 files but not the 176 that matter |
| Shell on Pages + all GLBs on **Cloudflare R2** | **Recommend (1st choice)** | Free tier (10 GB storage, $0 egress); ~$0.09/mo paid | Whole 5,969 MB set fits free tier; CORS-configurable; zero egress = no bill for game downloads |
| Shell on Pages + GLBs on raw.githubusercontent | Skip (fallback only) | Free | Verified CORS `*`, but 300 s cache, no CDN/SLA, untested at 90 MB |
| Statically / githack | Skip (fallback only) | Free | No published size limit, but small service, no SLA, unverified at 90 MB |
| itch.io HTML5 (shell) + R2 lazy-load + donations | **Recommend (money path)** | Free; seller picks itch cut 0–100% (default 10%) + Stripe ~2.9%+$0.30 | Shell fits 500 MB / 1,000-file caps; external HTTPS lazy-load allowed; but HTML5 = donations only — selling needs a Downloadable build |
| itch.io Downloadable build (full game, butler) | Recommend (later) | Free; same revenue share | 1 GB web / 2 GB butler default, increase on request; 30 GB community-reported hard cap; butler = resumable + delta uploads |
| Cloudflare Pages (full set) | **Skip** | Free | 25 MiB/file cap on all plans kills 98 GLBs (4,178 MB); 20,000-file cap also binds |
| Cloudflare Pages (shell only) | Recommend (alt shell host) | Free, unlimited bandwidth | Shell fits; unlimited static bandwidth beats Pages/Netlify caps |
| Netlify free (shell / mirror) | Recommend (alt shell host) | Free | No documented total-size cap; CLI handles big deploys; **repo already has `game/netlify.toml`** (but it proxies to Pages today). 100 GB/mo bandwidth uncertain under 2025 credit system — verify at signup |
| Vercel Hobby | **Skip** | Free, non-commercial only | Non-commercial clause disqualifies a money-making game; Pro $20/seat + metered bandwidth is the wrong shape |
| Backblaze B2 | Viable fallback | Free 10 GB + 1 GB/day egress | S3-compatible; R2's $0 egress is simpler |
| Git LFS / Actions artifacts | **Excluded** (2026-10-19) | Metered / 90-day cap | Do not revisit |

## Recommended path

**1st choice — split hosting, $0:**
1. **Shell on GitHub Pages (unchanged deploy, smaller set):** `build_pages.py` deploys only the shell — code + UI + portraits + 1 stage + 2–4 bundled fighters + their movesets (~70–170 MB, well under 1 GB). The live URL stays `https://mhvnsnt.github.io/western-heart/`. No owner decision about "what gets cut" is needed — nothing is cut from the game, only from the deploy.
2. **All GLBs on Cloudflare R2 (one bucket, CORS `*`):** upload the 5,969 MB set (fits the free 10 GB tier). The game loader fetches fighter/stage/attire GLBs from the R2 public URL on demand (per-fighter loading already matches the game's architecture). Keep GitHub Releases as the *store of record* (already decided); R2 is the *runtime* mirror, re-synced from releases.
3. **jsDelivr as the small-file fast path (optional):** files ≤20 MB can load from `cdn.jsdelivr.net` (verified CORS + correct MIME); R2 covers everything else. One manifest, two bases — or R2-only for simplicity. Decide in the wiring lane.
4. **itch.io in parallel (the money unlock):** create the itch.io account + project now, set payout mode (Direct to PayPal/Stripe, or Collected with the tax interview + $5 minimum), publish the same shell as an HTML5 project (fits 500 MB / 1,000 files) with donations on, lazy-loading from R2. Later: paid Downloadable build via butler (request the limit increase past 2 GB when the time comes).

**Fallback:** shell on Pages + assets split jsDelivr (≤20 MB) / R2 (>20 MB) is the same architecture with a different default base; Netlify free replaces Pages as shell host if Pages ever objects to the bandwidth; Cloudflare Pages replaces Pages as shell host if the shell's bundled fighters are all ≤25 MiB.

## Concrete next steps (for a wiring lane — no PRs opened by this research)

1. Owner decision (one line): approve split hosting (shell on Pages + R2) instead of cutting content. This replaces the pending "what gets cut" question.
2. Create a Cloudflare account + R2 bucket (lane job; verify whether a payment method is required at signup; do not auto-signup on the owner's behalf without his word — card rules from 2026-10-19 still apply).
3. Upload the deploy set's GLBs to R2 from the GitHub Releases store (do not re-derive from local disk), set the bucket CORS rule, and verify with `curl -I -H "Origin: ..."` + a real browser `fetch()` of a >25 MB GLB.
4. Wire the game loader to an asset-base URL (R2 public URL, with jsDelivr as optional small-file base), behind a one-line config — no per-file code changes.
5. Change `build_pages.py` (or add a `--shell-only` mode) so the gh-pages deploy ships the shell set only; verify the new deploy is <1 GB and the Oct 24-frozen site updates.
6. itch.io account + payout setup (owner's phone; lane prepares the project page and the shell ZIP, owner taps through account/payout screens).
7. Re-check at wiring time: R2 CORS behavior on a public bucket, Netlify free bandwidth under the credit system, itch.io butler 30 GB cap against itch.io's own docs.

## Blocked / open questions

- **Owner decision:** split hosting vs. cutting content. Recommendation above makes cutting unnecessary — needs his word.
- **R2 signup:** whether Cloudflare requires a payment method for the free tier. Card-required signups are owner-only (2026-10-19 rule).
- **itch.io account + payout setup:** owner phone-only; the lane can prep everything else but the account/payout screens are his taps. Earnings still $0; this is the unlock.
- **Butler 30 GB hard cap:** community-reported, not verified against itch.io's own docs.
- **Netlify free bandwidth:** 100 GB/mo vs ~15 GB under the 2025 credit system — conflicting 2026 sources; verify on Netlify's pricing page at signup.
- **Draco/KTX2 compression of the 176 big GLBs:** separate work item (gltfpack already wired in `tools/procgen/gltf-delivery/`); lowers R2/egress load but does not remove the need for split hosting.

## Sources (every limit claimed, checked 2026-10-25/26)

- GitHub Pages limits — https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- GitHub Releases as store (decided 2026-10-19) — https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases (limits: <2 GiB/asset, 1000 assets/release, no total-size/bandwidth cap)
- Release-asset CORS — live `curl -I` probe 2026-10-26 04:08 UTC against `github.com/mhvnsnt/western-heart/releases/download/tekken6-psp-v1/tekken6-psp.iso` (302, no ACAO; final `release-assets.githubusercontent.com` 200, no ACAO; signed URL ~1 h expiry); corroborated by https://corsfix.com/blog/fetch-github-release and hacs/integration#5643
- jsDelivr limits — https://deepwiki.com/jsdelivr/jsdelivr/3-usage-guide (README: >20 MB GitHub files unsupported by default, >150 MB packages unsupported); live `curl` probes 2026-10-26 (405 KB GLB 200 + `model/gltf-binary` + `ACAO:*`; 86 MB GLB 403)
- raw.githubusercontent CORS — live `curl` probe 2026-10-26 (200, `ACAO:*`, `application/octet-stream`, `max-age=300`)
- Statically — https://statically.io/
- itch.io HTML5 docs — https://itch.io/docs/creators/html5 (via https://portalready.world/portals/itch-io/ and https://app.cinevva.com/guides/itch-io-launch-guide); Creator FAQ — https://itch.io/docs/creators/faq; payments — https://itch.io/docs/creators/payments.amp
- Cloudflare Pages limits — https://developers.cloudflare.com/pages/platform/limits/
- Cloudflare R2 pricing — https://developers.cloudflare.com/r2/pricing/
- Netlify Drop size guidance — https://www.netlify.com/knowledge-base/netlify-drop-vs-vercel-drop/; free-plan size limit — https://answers.netlify.com/t/free-plan-website-size-limit/2084
- Vercel Hobby commercial-use restriction — multiple 2026 pricing roundups (https://livemy.app/blog/vercel-pricing, https://dev.to/nayankyada/vercel-pricing-2026-what-you-actually-pay-for-a-real-nextjs-project-33md); verify on https://vercel.com/pricing at signup
- Backblaze B2 free tier — https://leanopstech.com/blog/backblaze-b2-pricing-2026/ and https://devopsboys.com/blog/cloudflare-r2-vs-aws-s3-vs-backblaze-b2-2026
- Repo tree measurements — live `gh api repos/mhvnsnt/western-heart/git/trees/main?recursive=1` 2026-10-26 (truncated at 100k entries; lower bounds)
- `game/netlify.toml` on main — `gh api repos/mhvnsnt/western-heart/contents/game/netlify.toml` 2026-10-26 (200 proxy rewrites to `mhvnsnt.github.io/western-heart/`)
