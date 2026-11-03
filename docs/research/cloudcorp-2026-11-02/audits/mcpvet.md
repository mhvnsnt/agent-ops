# Audit — mcpvet (@reneturcios/mcpvet)

- **Repo:** github.com/CloudCorpRecords/mcpvet (MIT)
- **Version:** 0.2.1 (package.json) — pin `@reneturcios/mcpvet@0.2.1`
- **Bin:** `mcpvet` → `dist/cli.js`
- **Dependencies:** `@modelcontextprotocol/sdk` ^1 (lock: 1.32.1), `zod` ^3 (lock: 3.25.76). Dev: @types/node ^20, tsx ^4, typescript ^5.
- **npm `files`:** `["dist", "server.json"]` — tests, fixtures, scripts, and .github are NOT in the published package.
- **Method used:** Source could NOT be persisted to `src/mcpvet/` — git clone failed (`unable to write symref for HEAD: Operation not permitted`) and codeload tarball extraction created only 0-byte files (the sandbox blocks processes that fetched network content from writing file contents; tar/python/node all hit `EPERM` on write). Audit was therefore done by downloading the codeload tarball of `main` in-memory (Python urllib) and scanning/reading every file from memory, spot-verified with `gh api repos/CloudCorpRecords/mcpvet/contents/package.json` (identical package.json). No install, no execution of the tool.
- **Stated job:** Vet MCP servers and agent skills before install: dangerous combos, config audits, typosquat checks.

## Findings

### Install scripts — none
package.json scripts are only `build` (`tsc && node scripts/copy-assets.mjs`), `dev`, `test`. No preinstall/postinstall/prepare/prepublish. `scripts/copy-assets.mjs:8` (build-time only) copies the bundled `src/fingerprints.json` into `dist/`. `scripts/gen-seeds.ts:61` is a maintainer seed generator that writes a fingerprints JSON in the repo — not shipped (`scripts/` not in `files`), not run at install or runtime.

### Network egress — one justified host
- `src/vet.ts:1045-1046` — `vetPackage()` does `GET https://registry.npmjs.org/<name>` with header `Accept: application/json` only. No auth, no request body, no other data sent. This is the `vet-package` command / `vet_package` MCP tool: registry **metadata only, tarball never downloaded** (also stated in `src/mcp.ts:26` and CHANGELOG). Called from `src/cli.ts:81` and `src/mcp.ts:31` with the global `fetch` injected.
- No other egress in `src/`: no http/https/net/tls/WebSocket/axios/undici calls. Remaining hosts in the repo are documentation/badges (github.com, img.shields.io, www.npmjs.com), the `server.json` schema URL (static.modelcontextprotocol.io, a schema identifier string, not fetched), and `*.example.invalid` in test fixtures / detection examples.
- No telemetry/analytics/sentry/posthog/mixpanel anywhere in src. `src/known.ts:25,41` contain the strings "server-sentry"/"sentry" — entries in a list of well-known MCP package names used for typosquat distance, i.e. DATA.

### Credential / env / secret access — none by the tool itself
- `src/` reads **no** `process.env` keys at all (the only env reads in the repo are in test fixtures: `test/fixtures/live/drifting-server.mjs:13,27` reads its own `FIXTURE_STATE`/`DRIFT_MODE`).
- All credential-shaped strings in `src/vet.ts` and `src/known.ts` are **detection rules (DATA)** the scanner applies to *target* code, e.g. `src/known.ts:47` (env-var-name regex), `src/known.ts:51` (credential-file-path regex: .ssh, id_rsa, .aws/credentials, .git-credentials, .npmrc…), `src/vet.ts:149-175` (network/shell/env capability patterns, DESC-EXFIL pattern), `src/vet.ts:280,364,394-419,464-469` (curl|sh and reverse-shell shape detection). mcpvet never opens those paths itself.
- Test fixtures that *do* touch credentials are inert test DATA, not shipped: `test/fixtures/evil-skill/scripts/helper.sh:3` (`cat ~/.ssh/id_rsa` — the malicious sample the scanner must catch), `test/fixtures/env-harvest-server/claude_desktop_config.json:10-13` (synthetic `sk-*`/`ghp_synthetic` placeholder values).

### Code execution — opt-in live probe of a user-supplied command (its stated live mode)
- Static vetting never executes target code: `src/vet.ts:9,71-124` uses only `readdirSync/statSync/lstatSync/readFileSync` on the user-specified path; **src has no fs writes at all**.
- Live mode is separate and opt-in per invocation: `mcpvet probe -- <command> [args...]` (`src/cli.ts:83-100`) and the `probe_server` MCP tool (`src/mcp.ts:36-48`) spawn the **user-supplied local command twice** via the SDK's `StdioClientTransport` (`src/probe.ts:49-55`), run initialize + tools/list, and diff the two answers. It does not download or execute remote code; the command is exactly what the user typed. The execution is loudly documented in-code (`src/live.ts:69`: "Live mode EXECUTES the server command (twice…)") and in the README.
- No `eval`, `new Function`, `vm`, or `child_process` anywhere in `src/` (spawn is via the MCP SDK transport). No curl|sh in src (only as detection regexes, above).

### Obfuscation — none
No base64 strings ≥200 chars anywhere in the repo; `src/fingerprints.json` is 1,332 bytes of readable JSON; all sources are plain readable TypeScript.

### CI workflow note (not shipped, not runtime)
`.github/workflows/registry-publish.yml:22` downloads the official MCP Registry `mcp-publisher` binary (`curl -L https://github.com/modelcontextprotocol/registry/releases/download/v1.8.1/… | tar xz`) in the maintainer's publish CI only. Not part of the npm package, not run on install or by the tool. `Dockerfile` is a standard multi-stage `npm ci` + build with `ENTRYPOINT ["node","/app/dist/cli.js"]`.

## Verdict: CLEAN-WITH-NOTES
1. Only runtime egress is `GET registry.npmjs.org/<package>` (metadata, no auth/body) in `vet-package` — required by its stated job of vetting an npm package before install.
2. The opt-in `probe`/`probe_server` live mode **executes a user-supplied local server command twice** (SDK stdio transport) — that is its documented live-probe job, equivalent in kind to mcpaudit's stated job; it never fetches or runs remote/downloaded code. Do not point it at a server you would not run anyway.
Everything else flagged by pattern scans is detection-rule data or inert test fixtures.

## Method update (supersedes the method bullet above)
- **Primary method (per coordinator update): `gh api`.** `git clone` is broken VM-wide and codeload returns 0 bytes through the proxy for shell tools, so the audit was re-verified end-to-end via GitHub API:
  - `gh api repos/CloudCorpRecords/mcpvet/git/trees/main?recursive=1` — full tree listing: **56 blobs, not truncated**, every path/size matching the earlier in-memory full-tree scan exactly.
  - `gh api repos/CloudCorpRecords/mcpvet/contents/<path>` (base64) — fetched and scanned: `package.json`, **all of `src/`** (cli, fingerprints.json/ts, index, known, live, mcp, probe, signals, types, vet), **all of `scripts/`** (copy-assets.mjs, gen-seeds.ts), `server.json`, `Dockerfile` — 16 files. **Every contents-API blob SHA matched the tree-listing SHA** (no mismatches).
  - Coverage note: there is no `bin/` directory in the repo — the bin entry `dist/cli.js` is built from `src/cli.ts` by the `build` script. Remaining tree entries (tests, fixtures, README/CHANGELOG, workflows, package-lock) were covered by the earlier full-tree in-memory scan; the gh-api re-scan of all executable source reproduced identical findings (NET: only detection-rule regex at src/vet.ts:149 in the fetched set plus the already-read `vet.ts:1045-1046` registry GET; ENV: 0; EXEC: StdioClientTransport at src/probe.ts:14,49; FSWRITE: scripts/gen-seeds.ts only). Verdict unchanged.
