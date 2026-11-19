# Live-view tunnels: zrok 401 loop still running, localhost.run burst-throttled, cloudflared + localtunnel blocked at the egress

- **Date:** 2026-11-18 ~23:05–2026-11-19 ~00:30 EST (continuous-friction-research pass)
- **Index:** [[RESEARCH-PULLIN-INDEX]] (entry added by this pass)
- **Status:** researched + live-tested; no new tunnel wired — every free leg
  is either dead, throttled, or blocked at the egress (see verdicts).
  The fix for the stable URL is still the owner/browser step from
  2026-11-15; the 401 circuit-breaker from that pass is still unapplied.
- **Dedupe:** `research-check.sh "cloudflared tunnel"` / `"cobalt tiktok
  download"` — zero hits in the index. `research-check.sh "zrok"` hits
  only the lane's own docs + the 2026-11-15 diagnosis
  (`research-friction-20261115/02-zrok-401-restart-loop.md`) — this doc
  is the follow-up: what changed since, and the two new legs tested.

## TL;DR

The owner's only window onto the live build (phone-only) rides two
tunnels, and both are degraded tonight: the stable zrok URL
`https://fmmg-live.shares.zrok.io` is still 502 (401 token, same as
Nov 15 — the watchdog still restarts it every 5 minutes, ~288 futile
restarts/day, because the 401 circuit-breaker recommended Nov 15 was
never applied), and the localhost.run rotating tunnel works but warns
it is about to be burst-throttled ("Almost out of burst ... will be
slowed. Paid plans get priority bandwidth"). Two new free legs were
tested live this pass and both fail **at the egress proxy**, not at the
vendor: cloudflared Quick Tunnel cannot provision
(`api.trycloudflare.com` returns HTTP 403 "Your request was blocked"
through the proxy), and localtunnel never issues a URL
(`server.localtunnel.me` returns an empty reply). bore was already
tried Nov 13 and failed ("deadline has elapsed"). There is no third
free tunnel to wire from this VM right now.

## 1. Evidence (live, this pass)

| Fact | Value |
|---|---|
| zrok stable URL | `curl https://fmmg-live.shares.zrok.io/` → **HTTP 502** (2026-11-19 05:15 UTC) |
| zrok restart loop | `zrok-share.log` 05:15:02 UTC: "proxied share restarted (pid 138276)" then immediately `[ERROR]: unable to run share (the zrok controller answered '401 unauthorized'; check the account token); retrying will not change the answer` — identical to Nov 15. No 401 handling, no backoff, no stop condition in the wrapper. |
| localhost.run | **ALIVE** at 05:15 UTC: tunnel registered 05:15:00 UTC, `9883eb052a5810.app.lhr.life`, ssh process PID 138199 alive (`-R 80:localhost:6080`). The Nov 17 death ("Timeout, server localhost.run not responding", 502) was transient — the watchdog regenerates it. |
| localhost.run burst | Same registration notice: "Almost out of burst: in about 2s 9883eb052a5810.app.lhr.life will be slowed. Paid plans get priority bandwidth: https://admin.localhost.run" — the free tier throttles after a burst. VNC over a slowed tunnel is the owner's live view degrading, not dying. |
| bore | Already tried by the live-view lane Nov 13 (`bore-test4.log`): connected (`remote_port=53264`, listening at 127.0.0.1:53264) then `Caused by: deadline has elapsed`. Failed; not re-tried (same egress). |
| cloudflared binary | 2026.11.1, downloaded from the GitHub release, **sha256-verified**: standalone binary `97bb3b02d23a5980fc9c15a1a270e692da1923f103f920d5b16d4931d5ab55e7` is byte-identical to the binary inside the same-release `.deb` (`ar x` + `tar -xzf`, same hash). `cloudflared --version` → `2026.11.1 (built 2026-11-17-15:04 UTC)`. |
| cloudflared quick tunnel | **FAILS**: `cloudflared tunnel --url http://localhost:18099 --protocol http2` → `failed to request quick Tunnel: Post "https://api.trycloudflare.com/tunnel": tls: first record does not look like a TLS handshake`. Root cause at the egress: `curl -X POST https://api.trycloudflare.com/tunnel` → **HTTP 403 "Your request was blocked"** (1.16 s); GET `/` → 403 too. The provisioning endpoint is blocked by the egress proxy, so no quick tunnel (and no named tunnel — same endpoint + an account) can be created from this VM. Binary NOT installed persistently (40 MB on a 78%-full disk for a tool that cannot provision); re-download from the release when the block lifts. |
| localtunnel | **FAILS**: `npx -y localtunnel --port 18099` installed and ran, printed **no URL in ~2 min**; `localtunnel.me` itself answers 302, but `server.localtunnel.me` (the tunnel server, wss) returns an **empty reply** (curl 000). The client never completes registration through the egress proxy. Process killed after the test. |
| Test server | Local `python3 -m http.server 18099` served `CLOUDFLARED-QUICK-TUNNEL-PROOF-20261118` on 127.0.0.1 throughout; killed after the tests. |

## 2. Candidates (license + honest verdict)

| Tool | Source | License (verified) | Verdict |
|---|---|---|---|
| **cloudflared Quick Tunnel** (`trycloudflare.com`, no account, one command) | cloudflare/cloudflared (GitHub release 2026.11.1) | Apache-2.0 (upstream) | ❌ **BLOCKED at the egress** — `api.trycloudflare.com` 403s through the proxy. Not a vendor problem; nothing to install until the egress allowlist changes. Re-test then. Limits if it ever works: ephemeral random hostname, 200 in-flight requests, no SSE, no uptime guarantee, fully public (no auth by default; `--allowed-mail` PIN needs an Oct 2026+ release — 2026.11.1 qualifies). |
| **localtunnel** (`localtunnel.me`, npm) | localtunnel/localtunnel | MIT | ❌ **BLOCKED at the egress** — no URL issued; `server.localtunnel.me` empty reply. Same class as cloudflared. |
| **bore** (`bore.pub`) | ekzhang/bore | MIT | ❌ already tried Nov 13 — connected then `deadline has elapsed`. Not re-tried. |
| **localhost.run** (current fallback) | localhost.run (SSH `-R`) | — (service) | ✅ **WORKING, throttled** — alive now; free tier burst-slows ("Almost out of burst"). The tunnel advertises a paid custom-domain plan at admin.localhost.run for a stable domain + priority bandwidth — an **owner money decision**, not a research pull. |
| **zrok re-enable** (the actual fix for the stable URL) | OpenZiti forum thread, verified 2026-11-15 | — | ✅ **the fix, owner/browser step** — `zrok2 disable && zrok2 enable <fresh token from myzrok.io>` (see 2026-11-15 doc §4). Still not done; a detached pass cannot mint the token. |
| **serveo.net** (SSH `-R`, like localhost.run) | serveo.net | — (service) | 📄 untested — same SSH class as the working localhost.run leg; only worth a test if localhost.run dies outright. Not tested this pass (no outage to justify it). |
| **ngrok free tier** | ngrok | — (service, account required) | 📄 not tested — needs an account/signup; free tier shows a warning page to visitors and rate-limits. Weaker than localhost.run on every axis here; no test run. |

## 3. Recommended (lane / owner applies)

1. **Live-view lane (queued since Nov 15, still unapplied):** add the
   401 circuit-breaker to `zrok-share-proxied.sh` — on a 401 in the
   share log, stop restarting, write one `NEEDS-REENABLE` line, re-check
   at most hourly. ~288 futile restarts/day become one visible alert.
   (Not applied here: the script is a live lane's file.)
2. **Owner decision (the stable URL):** either re-enable zrok with a
   fresh console token (free, restores `fmmg-live.shares.zrok.io`), or
   take localhost.run's paid custom-domain plan (stable domain +
   priority bandwidth, kills both the rotation and the burst-throttle).
   Until one lands, live view = the rotating localhost.run address,
   burst-throttled.
3. **Egress allowlist (runtime/owner call, not a lane fix):** if
   `api.trycloudflare.com` is ever allowlisted, cloudflared Quick
   Tunnel is the immediate third leg — binary verified this pass,
   one command, no account. Re-test, don't assume.
4. **Do not burn more passes on tunnel roulette:** bore, cloudflared,
   localtunnel are all now tested against this egress. The next tunnel
   test only happens if the egress changes or localhost.run dies.

## 4. Blocked / not done here

- No zrok re-enable (needs a fresh console token — browser step).
- No live-view script edited, no tunnel restarted, no localhost.run
  process touched (it was alive and serving).
- No cloudflared binary installed persistently (blocked tool, 40 MB).
- No paid plan taken (owner money decision).
