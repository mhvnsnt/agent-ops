# Social-video downloads: cobalt tested, FB reel 1481081410582657 still unfetched — the wall is cookies, not downloaders

- **Date:** 2026-11-18 ~23:05–2026-11-19 ~00:30 EST (continuous-friction-research pass)
- **Index:** [[RESEARCH-PULLIN-INDEX]] (entry added by this pass)
- **Status:** researched + live-tested; nothing wired — cobalt's hosted
  routes are unusable from this VM and the reel is login-gated, so no
  downloader fixes it. The one remaining route (signed-in browser
  DevTools network capture) is already queued from the 23:31 EST
  browser-task failure.
- **Dedupe:** `research-check.sh "cobalt tiktok download"` — zero hits.
  The FB-reel fallback chain (PR #269) is the lane's own work, not a
  prior research pass; this doc records what the chain proved and tests
  the one candidate the chain never tried.

## TL;DR

The Júss Jåyy reel (1481081410582657) still has no video file after
the full fallback chain v2 (FAILED.md in
`~/workspace/_fb-reel-pelvic-20261118/s5/`, 2026-11-19 04:10 UTC):
yt-dlp 2026.10.26 "Cannot parse data" on every URL form, the page
parser finds 0 mp4/dash URLs in 359 KB fetches, and the two TikTok
candidates are now confirmed DEAD in the browser ("This page isn't
available", tikwm + Tikdown fail). The one candidate the chain never
tried — cobalt — was tested live this pass and fails on **both**
hosted routes from this VM: the main API instance `co.wuk.sh` times
out with 0 bytes, and `api.cobalt.tools` answers HTTP 400
`error.api.auth.jwt.missing` (hosted API now needs JWT auth). And even
a working cobalt would not fetch this reel: it plays only while
signed in, and cobalt would need the Facebook session cookies — which
live in the Muse browser profile, not on this VM's disk (the exact
reason the chain's S3 cookies step already failed). The wall is the
cookie bridge, not the downloader. Stop burning lanes on downloader
roulette for this reel.

## 1. Evidence (live, this pass + the lane's FAILED.md)

| Fact | Value |
|---|---|
| Reel | facebook.com/reel/1481081410582657, Júss Jåyy (100039802262713), post 1841377207199004, public, 2026-11-17, caption "what in the actual f@wkkkkk !! #reels" |
| S1 meta | OK (facebook-cli post read) |
| S2 yt-dlp 2026.10.26 | "Cannot parse data" on share / reel / m-watch / www-watch / legacy-video-video-php / poster-videos forms; legacy-video-php: "This video is only available for registered users. Use --cookies-from-browser or --cookies" |
| S3 cookies | FAILED — **no local browser profile with a Facebook cookie store on this VM** (Chromium/Chrome/Firefox profile dirs checked; the cloud browser's profile is not on this VM's disk) |
| S4 page parser | Pages fetch (346–549 KB) but contain **0 mp4, 0 dash_manifest, 0 playable_url** — Facebook serves anonymous requests an empty shell |
| S5 TikTok candidates | @film19900208 7609242650490850573 + @amandatonnesen 7621494613538311442 — yt-dlp: "Your IP address is blocked from accessing this post" (per-post: control @stagestor still fetches fine, so not an IP ban) |
| Browser task 23:31 EST | Both TikTok candidates DEAD in cloud + device browsers ("This page isn't available"; tikwm + Tikdown fail) — likely deleted/private since Mar 2025. FB reel plays while signed in (Mars Fmmg, reCAPTCHA cleared) but Facebook offers NO download; fdown.net "might be private", Getfvid "not found" |
| Cobalt `co.wuk.sh` (main API instance per README) | **Unreachable from this VM**: POST timed out after 40 s, 0 bytes received; repeat GET → HTTP 000 (1.7 s) |
| Cobalt `api.cobalt.tools` | POST → **HTTP 400 `{"status":"error","error":{"code":"error.api.auth.jwt.missing"}}`** (1.6 s) — hosted API requires JWT auth now; not a usable backend |
| Cobalt `cobalt.tools` web | HTTP 200 — the site is up; only the API routes fail |
| yt-dlp s5 batch | The 8h+ stalled yt-dlp PID 51098 noted by the guardian at 22:40 EST is gone as of this pass (no yt-dlp process in `ps`); the s5 lane wrote its FAILED.md and stopped. No process killed by this pass. |
| Remaining untried route | **DevTools Network capture while the signed-in reel plays** — the follow-up to the same browser task failed to start ("browser continuation is temporarily inconclusive; retry after recovery finishes"). Still queued, not superseded by anything here. |

## 2. Candidates (license + honest verdict)

| Tool | Source | License (verified) | Verdict |
|---|---|---|---|
| **cobalt hosted API** (`co.wuk.sh` / `api.cobalt.tools`) | imputnet/cobalt (GitHub README read live this pass) | **AGPL-3.0** code; branding/mascots copyrighted, NOT under AGPL | ❌ **excluded for this VM** — `co.wuk.sh` unreachable (timeout, 0 bytes); `api.cobalt.tools` needs JWT auth. Matches the independent warning that hosted instances "use bot protection and are not intended to be used in other projects without explicit permission" — self-host or ask an instance owner. Free for personal projects per README; commercial use needs your own instance. |
| **cobalt self-hosted** (Node API server) | imputnet/cobalt, `docs/run-an-instance.md` | AGPL-3.0 | 📄 **queued, not wired — and useless for THIS reel** — no Docker on this VM (Node 24 is present, so a node self-host is buildable in principle), but the reel is login-gated: cobalt supports a `cookies.json` for services that need login, and there are no FB session cookies on this VM (S3 failure above). Self-hosting moves the IP problem, it does not remove it — a self-hosted instance from this VM meets the same datacenter-IP blocks. Worth one test later for **public** TikTok/FB links only, after the cookie-bridge question is answered. |
| **yt-dlp 2026.10.26** (current stable, Oct 26) | yt-dlp/yt-dlp | Unlicense (upstream) | ✅ already the chain's tool — TikTok extractor fixed Aug 19 for public videos/share URLs; per-post blocks ("Your IP address is blocked from accessing this post") are server-side, not version-fixable. No newer version to chase. |
| **gallery-dl** | gallery-dl/gallery-dl | GPL-2.0 | 📄 not a fix for this reel — its Facebook extractor also needs cookies; same S3 wall. Not tested (no new capability vs yt-dlp here). |
| **tikwm / Tikdown / fdown.net / Getfvid** | third-party download sites | — | ❌ already tried by the browser task — all fail on these videos ("might be private" / "not found" / unavailable). |
| **Browser DevTools network capture (signed-in reel playing)** | — (technique, not a tool) | — | ✅ **the remaining route** — capture the DASH/mp4 URL from the signed-in browser's network tab while the reel plays. Already queued from the 23:31 EST browser failure; retry the follow-up when the browser recovers. Nothing in this pass supersedes it. |

## 3. The actual gap (for the next lane, not this pass)

The chain's S3 failure is the whole story: **the signed-in session
lives in the Muse browser profile, and its cookies never reach this
VM's disk.** Every VM-side downloader (yt-dlp, cobalt, gallery-dl)
hits the same wall on login-gated content, and every hosted API hits
the same wall plus auth/rate limits. The fix, if anyone wants it, is a
**cookie bridge** — a supported way for a signed-in browser session's
cookies to reach a VM-side downloader for one URL (export from the
browser lane, consume with `--cookies` / cobalt `cookies.json`,
local-only, never committed) — not another downloader. That bridge
does not exist today; building it is a browser-lane + downloader-lane
design question, not a research pull. Do not present any downloader
as the answer until the bridge exists.

## 4. Recommended

1. **For this reel:** run the queued DevTools network capture in the
   signed-in browser (retry the follow-up). No more downloader lanes.
2. **For future public-link downloads:** one self-hosted cobalt test
   (node, no Docker needed) against a known-public TikTok/FB link —
   only after deciding the cookie question, and only for public links.
3. **Do not re-test** `co.wuk.sh` / `api.cobalt.tools` from this VM
   until something changes (egress or cobalt's auth) — both failures
   are recorded with exact errors above.

## 5. Blocked / not done here

- No video file obtained for the reel; the motion study stays blocked
  on the file (owner's ask, 2026-11-18).
- No cobalt instance installed (hosted routes dead; self-host gated on
  the cookie bridge).
- No browser task started by this pass (the DevTools follow-up belongs
  to the browser lane; its continuation failed to start on its own).
- No cookies read, exported, or recorded by this pass.
