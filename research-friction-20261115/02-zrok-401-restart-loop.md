# zrok stable share: 401 unauthorized + futile 5-minute restart loop

- **Date:** 2026-11-15 ~23:15 EST (continuous-friction-research pass)
- **Index:** [[RESEARCH-PULLIN-INDEX]] (entry added by this pass)
- **Status:** diagnosed from the live log + live `zrok2` calls; fix is a
  browser/console step (fresh enable token) + a watchdog guard — neither
  applied by this pass (see §4)
- **Dedupe:** `research-check.sh "zrok"` — only prior hits are the lane's
  own docs (`ZROK.md`, `zrok-share.sh` history) and log mentions. The
  2026-11-12 supervisor-deaths doc is a *different* daemon (M. Engine
  supervisor, `node server.js`) — this is the zrok share, not that. New.

## TL;DR

The stable live-view URL `https://fmmg-live.shares.zrok.io/vnc.html` is
**down tonight** (HTTP 502). The watchdog restarts the zrok share every 5
minutes and every restart dies instantly with:

```
[ERROR]: unable to run share (the zrok controller answered
'401 unauthorized'; check the account token); retrying will not change
the answer
```

The 401 is terminal, not transient — zrok's own message says so. The
watchdog loop can never fix it; it has been failing the same way since
at least 03:37 UTC (22:37 CT). The upstream fix (OpenZiti forum, verified
thread) is `zrok disable` + `zrok enable <fresh token from the myzrok.io
console>` — a browser step, not a script step. What a script *can* do is
stop the futile loop: on 401, stop restarting and log a single
NEEDS-REENABLE alert instead of one failed restart every 5 minutes. The
rotating localhost.run tunnel is the working live-view path tonight and
the watchdog keeps it up; nothing the owner uses is blocked by the zrok
outage except the stable address itself.

## 1. Evidence (live, this pass)

| Fact | Value |
|---|---|
| Stable URL | `curl https://fmmg-live.shares.zrok.io/vnc.html` → **502** (23:06 EST) |
| Share process | **none running** (`ps` shows Xvnc/websockify/ttyd up since 20:54, no zrok) |
| Restart loop | `zrok-share.log`: 03:37, 03:42, 03:47, 04:03, 04:07, 04:12 UTC — every pass: "URL down and no share process — restarting PROXIED share", then the 401 error immediately. Still failing at 04:12 UTC (23:12 EST). |
| `zrok2 status` | Environment present: Account Token `<<SET>>`, EnvZId `<<SET>>`, apiEndpoint `https://api-v2.zrok.io` (from env). Config exists — the controller rejects it. |
| `zrok2 list shares` | **panic: `[GET /shares][401] listSharesUnauthorized`** (live, this pass) |
| `zrok2 list names` | **panic: `[GET /share/names][401] listAllNamesUnauthorized`** (live, this pass) |
| Current wrapper | `_live-view-sni-proxy-20261114/zrok-share-proxied.sh` — restarts whenever the URL is down and no `zrok2 share public.*fmmg-live` process matches. **No 401 handling, no backoff, no stop condition.** The share process exits immediately on 401, so the next 5-min pass restarts it again, forever. |
| Working fallback | localhost.run tunnel regenerating every ~5 min (watchdog log 22:37–23:07 CT, fresh `*.app.lhr.life` addresses each pass). Live view itself is up; only the stable zrok address is down. |
| History | Same class of failure on 2026-11-15 ~00:03 CT: share token went stale ("name in use"), fixed by manually deleting the stale token with `zrok2 delete share` and restarting. Tonight's failure is different — 401 on the *account* token, not a name conflict. |

## 2. What upstream says (real sources, read this pass)

- **OpenZiti Discourse, "Zrok stopped working (401 Unauthorized error)"**
  (https://openziti.discourse.group/t/zrok-stopped-working-401-unauthorized-error/2764,
  read live 2026-11-16 04:08 UTC): the reporter's fix was `zrok disable`
  then `zrok enable <my token>`; a maintainer confirms that should not be
  necessary routinely. A second reporter fixed it only after `zrok disable`,
  changing the account token, and removing the local zrok-share state.
- **Same thread, maintainer on stuck shares:** free accounts are limited
  to **5 shares**; if a share process is killed without its shutdown hook
  running, the share stays allocated ("they get stuck"). There is **no
  method to release shares from the command line** — release from the web
  interface, or call the unshare API directly:
  `curl -H "X-TOKEN: <accountToken>" -XDELETE -H "Content-Type:
  application/zrok.v1+json" -d '{"envZId": "<ziti_identity>",
  "shareToken": "<shareToken>", "reserved": <bool>}'
  https://api-v1.zrok.io/api/v1/unshare`
  (`ziti_identity` is in `$HOME/.zrok/environment.json`; `reserved` must
  match the share's actual reserved state or the removal silently fails).
  `GET /api/v1/overview` with the same `X-TOKEN` header lists all
  environments and shares (share-count check against the 5-share limit).
- **zrok's own error text** (in our log): "'zrok2 agent' retries transient
  failures with backoff" — i.e. 401 is classified non-transient by zrok
  itself. Retrying a share start on 401 is, by the tool's own words, futile.

## 3. Candidates / verdicts

| Candidate | Verdict |
|---|---|
| `zrok disable` + `zrok enable <fresh token>` (fresh enable token from myzrok.io console) | ✅ **the fix** — upstream-verified. Needs a browser step (console token); a detached research pass cannot mint it. Main agent / owner step. |
| Watchdog 401-circuit-breaker: on a 401 in the share log (or `zrok2 list shares` 401), stop restarting, write one `NEEDS-REENABLE` line, and re-check at most hourly until a human re-enables | ✅ **recommended, queued** — small patch to `zrok-share-proxied.sh` (or its caller). Stops the 5-min spawn loop and turns an invisible repeated failure into one visible alert. The localhost.run tunnel path is untouched (it is the working fallback). |
| `zrok2 agent` as the share supervisor | 📄 noted, not adopted — the lane's ZROK.md already records it auto-restarts reserved-name shares, but it cannot fix a dead account token either; same 401. No advantage over the watchdog + breaker. |
| Unshare API / overview API (curl) | 📄 documented — the tool to check the 5-share quota and release stuck shares *if* the count is the problem. Needs the account token (present in the local zrok config; never print it, never commit it). Do not call it speculatively: first check `zrok2 list shares` after re-enable; if the count is at 5 with stale entries, release the stale ones via the console or the API. |
| Re-reserving the name `fmmg-live` | ❌ not needed (yet) — the name is reserved; the failure is auth, not the name. Only re-reserve if re-enable loses the reservation (check `zrok2 list names` after re-enable). |
| Deleting local zrok state (`~/.zrok/`) as a fix | ❌ excluded — the forum reporter did it as part of a scattershot fix; the clean, verified fix is disable + re-enable. Do not delete state blindly (it holds the environment identity). |

## 4. Recommended (and what is blocked)

1. **Owner / main-agent step (the actual fix):** in a browser, open the
   myzrok.io console for `fmmg.mars@gmail.com`, copy a fresh environment
   enablement token, then on the VM:
   `zrok2 disable && zrok2 enable <fresh token> --headless`
   (never write the token to a file, chat, or repo — it is consumed once
   by `zrok2 enable`, per the lane's ZROK.md). Then verify
   `zrok2 list shares` no longer 401s, and restart the share via the
   watchdog's normal path. If the name reservation is gone, re-run
   `zrok2 create name -n public fmmg-live` first.
2. **Live-view lane (queued patch):** add the 401-circuit-breaker to
   `zrok-share-proxied.sh`: capture the share-start output; if it contains
   `401 unauthorized`, touch a marker (e.g. `$LIVE/.zrok-401`) and skip
   restarts while the marker is fresh (< 1 h), logging
   `NEEDS-REENABLE` once per marker lifetime; clear the marker when a
   share start succeeds. This turns ~288 futile restarts/day into one
   alert. (Not applied here: the proxied script is a live lane's file and
   the share is down *now* — a research pass does not edit a live lane's
   restart path blind.)
3. **After re-enable:** check the share count against the free 5-share
   limit (`zrok2 list shares` / overview API). The VM has killed share
   processes without shutdown hooks repeatedly (VM restarts ~20:53 EST
   tonight, ~23:57 CST Nov 14, and the runtime's ~2 h SIGTERM cycle) —
   each such kill can strand an allocation. Release stale ones from the
   console if the count is at the limit.

## 5. Blocked / not done here

- No `zrok disable` / `zrok enable` attempted: it needs a fresh console
  token, which only a browser session can mint. No token value was read,
  printed, or recorded by this pass.
- No live share touched, no watchdog file edited, no restart attempted
  (the loop is already restarting every 5 min; another restart changes
  nothing while the token is dead).
- The stable URL stays down until step 1 above runs. The localhost.run
  rotating tunnel remains the live-view path in the meantime (watchdog
  regenerates it; last good address 23:07 CT).
