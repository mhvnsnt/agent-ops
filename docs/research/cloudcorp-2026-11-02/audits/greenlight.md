# Security Audit — greenlight

- **Repo / package:** github.com/CloudCorpRecords/greenlight — `@reneturcios/greenlight`
- **Version (pin this):** 0.25.0
- **Bin:** `dist/cli.js` (one bin serves the CLI and the stdio MCP server, src/index.ts)
- **Dependencies:** `@modelcontextprotocol/sdk ^1`, `zod ^4.6.7` (dev: `@types/node ^20`, `tsx ^4`, `typescript ^5`)
- **License:** MIT
- **Method used:** git clone and codeload tarballs failed on this VM (clone symref write error; tarballs 0 bytes through the proxy). Source was fetched file-by-file through the GitHub API contents endpoint via the GitHub MCP connector (`get_file_contents`, the same contents API `gh api repos/CloudCorpRecords/greenlight/contents/<path>` wraps), saved as raw API snapshots in `src/greenlight/rawsnap/`, and audited in-memory with line-accurate scans; every flagged area was read in context.
- **Coverage:** `package.json`, `Dockerfile`, `server.json`, `action.yml`, `.mcp.json`, ALL 58 files of `src/`, ALL of `scripts/` (llm-claim-smoke.mjs, sync-readme-test-count.sh, trust-index-dry-run.ts), and the shipped `integrations/` tree (mcp.json read in full; claude-code/CLAUDE.snippet.md read in full; per-agent subdir listings taken). No `bin/` directory exists. Not line-audited: `test/`, `docs/`, `data/`, `examples/`, `protocol/`, `maintainer/`, `.github/` — none of these are in the npm package (`files`: `dist`, `server.json`, `integrations`), so they cannot affect an install.

## Install scripts

package.json scripts: `build` (tsc), `dev`, `index` (tsx src/friction-index.ts — a maintainer script that regenerates the policy-index data file in the author's repo), `test`, `readme:count` (bash scripts/sync-readme-test-count.sh). **No preinstall / postinstall / prepare** — nothing runs at install time.

## Network egress (complete host list)

All GitHub API traffic goes through `apiGet`/`apiPost` in src/github.ts unless noted.

1. **api.github.com** — the tool's primary API (issue/PR verdicts, claims, radar, digests). Default base is hardcoded (src/github.ts:19). Override via `GREENLIGHT_GITHUB_BASE_URL` passes through `sanitizeApiBase()` (src/github.ts:30–56): http/https only, embedded credentials, query strings and fragments stripped, invalid values fall back to the default.
2. **raw.githubusercontent.com** — file-contents fetches (src/github.ts:20, and the best-effort cached contents path at src/github.ts:959).
3. **cloudcorprecords.github.io** — the author's own public static files, GET-only, no token or auth headers sent: the Agent Policy Index at `…/greenlight/policy.json` (src/index-drift.ts:25–26, src/wave.ts:32, fetched at src/index-drift.ts:139 and cached to `~/.greenlight/policy-index-cache.json`) and the public Claim Ledger JSONs (default base src/passport.ts:22, GETs at src/passport.ts:110,126; src/claim-import.ts:21).
4. **claim-api-wine.vercel.app** — the author's hosted claim-API service, `DEFAULT_API_BASE` at src/claim-api.ts:39. Used **only** by the explicit `--via-api` surface: `greenlight auth login`, `claim --via-api`, `release --via-api`, `heartbeat --via-api`, and the MCP tools `api_status` / `claim_via_api` / `heartbeat_via_api` (module header, src/claim-api.ts:4–17). Calls are GET status/installation and POST `/v1/claims`, `/v1/claims/release`, `/v1/claims/heartbeat` carrying claim payloads (owner/repo/issue) with the user's token (src/claim-api.ts:586–624). Base resolution order is `--api-base` flag → `GREENLIGHT_API_BASE` env → config file → hosted default, and **a flag/env-supplied base is cached into `~/.config/greenlight/config.json`** for later runs (src/claim-api.ts:78–107). If the hosted app path is unavailable it falls back to direct GitHub API comments with a printed notice (src/claim-api.ts:13–17).
5. **api.fireworks.ai** — optional LLM claim classification. Enabled **only when the user sets `FIREWORKS_API_KEY`** (`llmEnabled()` is literally `Boolean(env.FIREWORKS_API_KEY)`, src/llm-claims.ts:51–53). POSTs to `{base}/chat/completions` (src/llm-claims.ts:324); default base `https://api.fireworks.ai/inference/v1` (src/llm-claims.ts:35), overridable via `GREENLIGHT_LLM_BASE_URL`, model via `GREENLIGHT_LLM_MODEL`. Data sent: GitHub issue **comment bodies truncated to 2,000 chars, at most 25 per call** (src/llm-claims.ts:38–41) — i.e., public issue text from repos the user is evaluating, sent to the user's own LLM account.
6. **github.com (OAuth device flow)** — `greenlight auth login` runs GitHub's device flow (src/claim-api.ts:19–23, 46–47) with a baked-in OAuth **client id** `Ov23liv9yM4RTci0UysE` (src/claim-api.ts:45 — a public client identifier, not a secret; overridable via `GREENLIGHT_OAUTH_CLIENT_ID`). Resulting scope is `public_repo`.
7. **127.0.0.1 (inbound, the `proxy` subcommand)** — a localhost forwarder that attaches the user's token server-side. It binds **127.0.0.1 only** (src/proxy.ts:116), forwards to **exactly one upstream, https://api.github.com** (src/proxy.ts:24, 62–105), strips incoming Authorization headers and attaches only the startup token (src/proxy.ts:75–79); the token is read once from env and never logged or stored (src/proxy.ts:12–18).
   - **Hardening note (not a verdict changer):** absolute-form request targets are rejected (src/proxy.ts:66–70), but a *protocol-relative* target (`//other-host/…`) is not explicitly rejected, and `new URL(target, upstream)` at src/proxy.ts:71 would resolve it cross-host — a local process could then use the proxy as a token oracle against another host. Exposure is localhost-only and the token still never leaves in cleartext to the caller, but the check should also reject targets starting with `//`.

Other hosts appearing in source are metadata or detection data only: `github.com`, `static.modelcontextprotocol.io`, `registry.npmjs.org`, `registry.modelcontextprotocol.io` (package/server metadata), `nodejs.org` and `cla-assistant.io` (help/detection text), `api.github.com.` (a trailing-dot string in a test-oriented constant). **No telemetry / analytics / Sentry / PostHog / Mixpanel anywhere** (grep-verified across all 58 src files).

## Credential / env access

Env keys read (complete list from scan): `GITHUB_TOKEN`, `GH_TOKEN`, `FIREWORKS_API_KEY`, `GREENLIGHT_API_TOKEN`, `GREENLIGHT_API_BASE`, `GREENLIGHT_GITHUB_BASE_URL`, `GREENLIGHT_OAUTH_CLIENT_ID`, `GREENLIGHT_LEDGER_URL`, `GREENLIGHT_LLM_BASE_URL`, `GREENLIGHT_LLM_MODEL`, `GREENLIGHT_AGENT_ID`, `GREENLIGHT_GITHUB_USER`, `GREENLIGHT_CLAIMS_FILE`, `GREENLIGHT_CAPABILITIES_PATH`, `GREENLIGHT_TRUST_FILE`, `GREENLIGHT_TRUST_MEMORY`, `GREENLIGHT_CLAIM_DAILY_CAP`, `GREENLIGHT_CLAIM_MIN_INTERVAL_S`, `GREENLIGHT_REQUEST_TIMEOUT_S`.

- `GITHUB_TOKEN`/`GH_TOKEN` are read at src/github.ts:162–164 and sent only as a Bearer header to the (sanitized) GitHub API base. A GitHub contribution tool reading the standard GitHub token env vars is justified.
- **Token storage (the user's own token, from `auth login`):** OS keychain first — macOS `security` and Linux `secret-tool` via fixed-binary `execFile`/`spawn` with argv arrays, the token passed over stdin on store (src/claim-api.ts:187–225) — falling back to `~/.greenlight/api-token` written with mode `0o600` plus an explicit `chmodSync 0600` (src/claim-api.ts:227–247, store selection at 287–295). `GREENLIGHT_API_TOKEN` / `--token` are passthrough alternatives (src/claim-api.ts:309–324). In two claim paths the resolved token is temporarily assigned into `process.env.GITHUB_TOKEN` in-process and restored/deleted afterwards (src/claim-api.ts:1011–1023, 1137–1143).
- **Not touched:** no access to `~/.ssh`, `~/.aws`, `~/.gnupg`, `.git-credentials`, browser profiles, or any other application's credentials anywhere in src/ (grep-verified). The only keychain interaction is greenlight storing/retrieving **its own** token.

## Code execution

- **No `eval`, `new Function`, or `vm` anywhere.** Base64 use is decoding GitHub API content payloads (src/github.ts:661, src/guard.ts:744, src/protocol-fetch.ts:168, src/automate.ts:159). No remote code is ever downloaded and executed; no curl|sh.
- **child_process, all accounted for:**
  - Fixed-binary `git` with argv arrays, no shell: src/autopilot-fixes.ts:191, src/ci-prep.ts:474, src/verify.ts:57, plus the keychain helpers above.
  - `sh -c` in exactly two **user-invoked features whose purpose is running the target repo's own commands locally**: `ci-prep` executes the repo's CI step scripts via `spawnSync("sh", ["-c", script])` (src/ci-prep.ts:451, env `{...process.env, CI: "true"}` at :456) and probes for `act`/`docker` (src/ci-prep.ts:624–643); `verify` runs the repo's test command the same way (src/verify.ts:131). The scripts executed come from the repo the user points the tool at — the same trust decision as running `npm test` in that repo — never from the network.
- **action.yml** (the repo's GitHub Action form) only reads its own `greenlight-guard.json` report with `node -e` one-liners (action.yml:50, 55, 87).

## fs writes (all feature-scoped)

- `~/.greenlight/` — the tool's own state: `autopilot.json` / `autopilot-replies.json` (src/autopilot.ts:129–133, 187–188, 1038–1039), `babysit.json` (src/babysit.ts:248, 265), `my-claims.json` (src/claims-registry.ts:66, 89), `capabilities.json` (src/capabilities.ts:55, 87), `trust.json` (src/trust.ts:336, 173), `posting-ledger.json` (src/posting-ledger.ts:80, 174, 408), `api-token` (above), policy-index cache.
- `~/.cache/greenlight/` — best-effort API response cache (src/github.ts:57, cacheSet at :100–106) and the doctor write-probe (src/doctor.ts:54, 106).
- `~/.config/greenlight/config.json` — the cached claim-API base (above).
- In the user's project: `PREP.md` prep files (src/automate.ts:885–886), evidence-pack markdown to a user-named output file (src/cli.ts:1634), scout campaign files (src/scout.ts:85), and `greenlight init` copying agent configs (src/init.ts:178) from the shipped `integrations/` snippets.
- Temp work dirs (`mkdtempSync`) for autopilot fix application (src/autopilot.ts:68, writes at :882, 894) and verify (src/verify.ts:17).
- Nothing writes outside the user's home, their project, or temp dirs. The posting ledger stamps entries with `GREENLIGHT_AGENT_ID` or `"<hostname>:<pid>"` (src/posting-ledger.ts:68–72) — recorded in that local ledger file.

## Shipped integrations/

`integrations/mcp.json` and each per-agent `.mcp.json` are the same 100-byte config registering `npx -y @reneturcios/greenlight@0.25.0 mcp` — the tool itself. `integrations/claude-code/CLAUDE.snippet.md` (read in full) is workflow guidance for the user's agent that explicitly requires the human's explicit go-ahead before posting anything to GitHub.

## Verdict: CLEAN-WITH-NOTES

This is a large GitHub contribution tool and its surface matches its stated job; nothing malicious, spying, or unjustified was found. The notes an installer should know:

1. **Hosted claim API:** `claim`/`release`/`heartbeat --via-api` and `auth login` talk to the author's hosted service at claim-api-wine.vercel.app by default (src/claim-api.ts:39), sending claim payloads and the user's token; a custom `--api-base`/`GREENLIGHT_API_BASE` is silently cached to `~/.config/greenlight/config.json` (src/claim-api.ts:78–107).
2. **Token custody:** with `auth login`, the user's GitHub token (public_repo scope, device flow, client id at src/claim-api.ts:45) is stored in the OS keychain, or in `~/.greenlight/api-token` at mode 0600 when no keychain exists (src/claim-api.ts:227–295). Day-to-day operation uses `GITHUB_TOKEN`/`GH_TOKEN` from env (src/github.ts:162–164).
3. **Opt-in LLM egress:** only if `FIREWORKS_API_KEY` is set, issue comment bodies (≤2,000 chars each, ≤25/call) are sent to api.fireworks.ai for claim classification (src/llm-claims.ts:35, 51–53, 324).
4. **Author-hosted public data:** the policy index and claim ledger are fetched GET-only, with no token, from cloudcorprecords.github.io (src/index-drift.ts:25–26, src/passport.ts:22).
5. **Local execution features:** `ci-prep` and `verify` run the *target repo's own* CI/test commands via `sh -c` (src/ci-prep.ts:451, src/verify.ts:131) — do not run them against untrusted repos. All other subprocess use is fixed-binary `git`/keychain tools with argv arrays.
6. **Proxy subcommand:** binds 127.0.0.1 only and forwards only to api.github.com (src/proxy.ts:24, 116); minor hardening gap — protocol-relative (`//host`) targets are not rejected alongside absolute-form ones (src/proxy.ts:66–71).
7. **State writes** are confined to `~/.greenlight/`, `~/.cache/greenlight/`, `~/.config/greenlight/`, temp dirs, and user-named/project files (PREP.md, evidence packs, `init` agent configs).
