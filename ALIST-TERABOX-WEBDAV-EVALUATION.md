# AList Evaluation — TeraBox -> WebDAV -> rclone Bridge

**Cluster:** FRICTION-RESEARCH 2026-10-19 · pull-in 6/6 (owner order 2026-10-19 ~23:33 CDT)
**Research:** [[research-friction-20261019/06-browser-transfer-alternatives]] · **Index:** [[RESEARCH-PULLIN-INDEX]]
**Status:** EVALUATED 2026-10-20 — DOCUMENTATION ONLY. Nothing installed, nothing deployed.
**Related:** [[BROWSER-TRANSFER-COOKIE-ARIA2-SOP]] (the no-service fallback lane)

> ## SERVICE USE ONLY — do NOT deploy without the owner's word
> AList is AGPL-3.0 and a hosted network service by design. Any deployment (binary, docker,
> install script) requires the owner's explicit go-ahead first. This doc evaluates; it does
> not authorize running it. Verdict status stays "queued" until the owner says deploy.

## What it is

- **AList** — a single-binary file-list / WebDAV program (Go, Gin + SolidJS) that mounts
  dozens of cloud storages behind one web UI, API, and WebDAV endpoint.
- Upstream: the cluster research cites `https://github.com/alist-org/alist`; GitHub search
  this session resolves the live repo as `https://github.com/AlistGo/alist` (50,316 stars,
  2,542 commits, active). Verify the canonical org at deploy time — do not trust either
  from memory.
- **License: AGPL-3.0** — verified from the repo README ("The `AList` is open-source software
  licensed under the AGPL-3.0 license") and the GitHub repo metadata line this session.

## Why it's the strongest TeraBox find

1. **Native TeraBox driver.** Source-level docs (DeepWiki, `drivers/terabox/`): cookie-based
   auth with `jsToken` validation and sign generation — the driver extracts a `jsToken`
   from the page HTML (`drivers/terabox/util.go` 49-53) and generates request signatures via
   a custom `sign` function (util.go 166-187). That is exactly the browser-session-cookie
   path — the only path out of TeraBox, since TeraBox publishes no official export tool,
   no rclone/WebDAV endpoint, and no public OAuth API (per the cluster research).
2. **It also mounts our other lanes:** PikPak, BaiduNetdisk, Quark, Google Drive, OneDrive,
   S3, local disk, and more (README feature list) — one bridge, many sources.
3. **WebDAV out.** AList serves mounted storage over WebDAV (README feature: "WebDav (see
   https://alist.nn.ci/guide/webdav.html for details)"). Community guides address it at
   `http(s)://<alist-host>/dav` — the official guide page could not be fetched this session
   (alist.nn.ci network error), so the `/dav` path stays **to-confirm at deploy time**.
4. **rclone has a Tier 1 WebDAV backend** (`https://rclone.org/webdav/`): config keys
   `url`, `vendor` (`other` for generic servers like AList), `user`, `pass` (must be
   obscured via `rclone obscure`), `bearer_token`. CloudDog is already rclone-based, so
   once AList exists, TeraBox looks like any other rclone remote to the stores pipeline.

## The bridge architecture

```
TeraBox (owner account, browser session cookie)
   |  AList terabox driver: cookie auth + jsToken + sign
   v
AList service (single binary or docker, ONE host the owner approves)
   |  serves the TeraBox mount at /dav (WebDAV, user/pass auth)
   v
rclone remote "alist-tb" (type=webdav, vendor=other)
   |  rclone copy / ls / hash-checked pulls
   v
CloudDog stores -> GitHub / TeraBox permanent store
   |  verify hash-identical on store
   v
local copy cleared (one-store rule; disk is a cache)
```

Proposed rclone wiring — **syntax verified against the actual rclone v1.75.2 binary's own
`--help` on this VM** (binary at `~/workspace/tools/rclone/rclone`, landed by pull-in 1/6;
not on PATH, so call it by full path below). End-to-end (AList side) is NOT testable until
AList is deployed:

```bash
RCLONE=~/workspace/tools/rclone/rclone

# One-time remote setup (deploy lane, after owner approval).
# config create takes key=value pairs; password fields are auto-obscured
# (pass --obscure to be certain, per the command's own help).
"$RCLONE" config create alist-tb webdav \
  url="https://<alist-host>/dav" \
  vendor=other \
  user="<alist-user>" \
  pass="<alist-password>" --obscure

"$RCLONE" lsd alist-tb:/                    # smoke test: list the TeraBox mount
"$RCLONE" copy alist-tb:/<path> /tmp/pull/  # pull
"$RCLONE" check alist-tb:/<path> /tmp/pull/ --download
# check compares sizes + hashes; --download forces byte-level comparison,
# which is the safe mode for WebDAV remotes with weak hash support
```

## AGPL-3.0 — what it means for us (honest read)

- **Running the unmodified upstream binary/docker as an internal service = the intended
  "service use" and the only approved mode.** No vendoring AList source into any repo of
  ours, no forks, no patches, no rebranding.
- AGPL's network clause (section 13) is written for exactly this shape: users interacting
  with a modified version over a network must be offered its source. Running upstream
  **unmodified**, with the upstream source link intact, keeps us on the safe side of that
  clause. If we ever need a modified build, that's a new owner decision with the source
  offer planned first.
- Hosted-service implication: an AList instance holds live cloud cookies (TeraBox, PikPak,
  etc.). It is a credential-bearing service — bind it to localhost / the tailnet only,
  never public-internet exposure, credentials via the Secure Vault pattern, never in code
  or config committed to a repo.
- This is the same pattern as the repo's other AGPL tools (e.g. FreeMoCap AGPL-3.0,
  documented-only / runtime-install): use it, don't fork it.

## Risks and open questions (for the deploy lane, not blockers to this eval)

- **Cookie freshness is the operational weakness.** TeraBox expires cookies on logout /
  password change / inactivity — the AList mount will need the same "refresh cookies"
  step as the SOP lane. Surface it as a named step, not a failure.
- **Upstream breakage risk.** The driver depends on TeraBox's web internals (jsToken, sign);
  TeraBox UI/API changes can break it until upstream patches. Fallback = the
  cookie->aria2 SOP ([[BROWSER-TRANSFER-COOKIE-ARIA2-SOP]]).
- **WebDAV hash support.** rclone WebDAV remotes vary in hash support by server; the
  end-to-end check (mount -> copy -> hash match) must be proven at deploy before the lane
  is declared green. Until then, verify pulled bytes with `sha256sum` locally per the SOP.
- **`/dav` path and the current docs home** (alist.nn.ci vs alistgo.com) need a live
  confirm at deploy time; the official WebDAV guide failed to fetch this session.
- **What is NOT decided here:** deploy host, credentials handling, exposure, version pin.
  All owner-gated.

## Verdict

- **Evaluation: PASS as documented.** AList is the right bridge design for the TeraBox pull
  problem (native driver + WebDAV + rclone Tier 1), license understood, risks named.
- **Deployment: BLOCKED on owner's word** (AGPL + hosted-service implications, per task).
  Queue #16 stays "queued" in [[RESEARCH-PULLIN-INDEX]] with this doc as its evaluation.
- **Fallback lane already documented:** [[BROWSER-TRANSFER-COOKIE-ARIA2-SOP]] needs no
  service at all — cookies + aria2/curl, works as soon as the lane tools are installed.

**Index:** [[RESEARCH-PULLIN-INDEX]]
