# Audit — shipcheck (@reneturcios/shipcheck)

- **Repo:** github.com/CloudCorpRecords/shipcheck (MIT)
- **Version:** 0.2.0 (package.json) — pin `@reneturcios/shipcheck@0.2.0`
- **Bin:** `shipcheck` → `dist/cli.js`
- **Dependencies:** `@modelcontextprotocol/sdk` ^1 (lock: 1.32.2), `zod` ^3 (lock: 3.25.76). Dev: @types/node ^20, tsx ^4, typescript ^5.
- **npm `files`:** `["dist", "server.json"]` — tests/.github are NOT in the published package.
- **Method used:** Same sandbox block as the rest of this batch: git clone and tarball extraction to `src/shipcheck/` failed (`Operation not permitted` / 0-byte files). Audit was done by downloading the codeload tarball of `main` in-memory (Python urllib), scanning every file, and reading `src/check.ts` call sites in context. No install, no execution of the tool.
- **Stated job:** Verify a release actually shipped: git tag, GitHub release, package metadata, npm, PyPI, MCP Registry, and GHCR all agree on the same version.

## Findings

### Install scripts — none
package.json scripts are only `build` (`tsc`), `dev`, `test`. No preinstall/postinstall/prepare.

### Network egress — exactly the registries its job checks (GET-only metadata)
All in `src/check.ts`, base URLs as constants at `src/check.ts:26-29`:
- `api.github.com` (`GH_API`, :26) — repo/release/tag/commit metadata via `ghJson()` at :94.
- `registry.npmjs.org` (`NPM_API`, :27) — package metadata, `checkNpm()` fetch at :915 with only a `User-Agent: shipcheck/<version>` header.
- `pypi.org` (`PYPI_API`, :28) — `GET /pypi/<pkg>/json` at :999-1001. PyPI is part of the stated job (package.json description and README:29-30 list the `pypi-version`/`pypi-latest` checks alongside npm), so this egress is justified on its own stated job, same class as npm.
- `registry.modelcontextprotocol.io` (`REGISTRY_API`, :29) — server version listing at :1125-1132.
- `ghcr.io` — anonymous public-image flow only: `GET https://ghcr.io/token?service=ghcr.io&scope=repository:<image>:pull` (:1201-1202), then `GET https://ghcr.io/v2/<image>/tags/list` with the anonymous token ghcr.io itself returned (:1218-1221).
- Human-facing `source:` URLs (github.com/…, www.npmjs.com/package/…, pypi.org/project/…) are strings printed in the report, not extra fetches.
No other hosts, no telemetry/analytics, no POST/upload of user data anywhere — all fetches are GET metadata lookups for the repo/package the user named.

### Credential / env access — one key, sent only where it belongs
- The **only** env var read in the entire repo's src is `GITHUB_TOKEN`: `src/check.ts:1272` (`opts.githubToken ?? process.env.GITHUB_TOKEN`), documented at `src/cli.ts:13` ("GITHUB_TOKEN is optional and only raises GitHub API rate limits").
- It is used only as `Authorization: Bearer <token>` in `ghHeaders()` (`src/check.ts:79`), which is used only by `ghJson()` for `api.github.com` requests (`src/check.ts:94`). It is **not** sent to npm, PyPI, the MCP Registry, or GHCR (GHCR uses its own anonymous token, above). When unset, GitHub calls are unauthenticated.
- No access to ~/.ssh, ~/.aws, keychain, browser profiles, .git-credentials, or any other credential store. No other `process.env` reads in src.

### Execution / writes / obfuscation — none
- No `child_process`, spawn, `eval`, `new Function`, `vm`, or curl|sh in src (the `exec` matches in `src/check.ts` are all `RegExp.prototype.exec` parsing calls, e.g. :54, :170-301).
- No fs writes in src (no writeFile/appendFile/createWriteStream/rm/unlink); it only fetches remote metadata and prints a report.
- No base64 blobs ≥200 chars; plain readable TypeScript.
- CI/Dockerfile pattern is the same benign maintainer pipeline as the sibling tools (publish workflow, `npm ci` image build); not part of the npm package runtime.

## Verdict: CLEAN-WITH-NOTES
- Egress is limited to the five surfaces its job exists to cross-check — api.github.com, registry.npmjs.org, pypi.org, registry.modelcontextprotocol.io, ghcr.io — all GET metadata for the user-named release.
- It reads one env var, `GITHUB_TOKEN` (`src/check.ts:1272`), and sends it only to api.github.com as a Bearer header (`src/check.ts:79,94`) for rate limits; GHCR access is the standard anonymous public-image token flow.

## Method update (supersedes the method bullet above)
- **Primary method (per coordinator update): `gh api`.** Re-verified end-to-end via GitHub API:
  - `gh api repos/CloudCorpRecords/shipcheck/git/trees/main?recursive=1` — full tree listing: **20 blobs, not truncated**, matching the earlier in-memory full-tree scan.
  - `gh api repos/CloudCorpRecords/shipcheck/contents/<path>` (base64) — fetched and scanned: `package.json`, **all of `src/`** (check, cli, index, mcp, types), `server.json`, `Dockerfile` — 8 files. **Every contents-API blob SHA matched the tree-listing SHA.**
  - Coverage note: no `bin/` or `scripts/` directory exists in this repo — bin entry `dist/cli.js` is built from `src/cli.ts`. Tests/docs/workflows/package-lock were covered by the earlier full-tree in-memory scan. The gh-api re-scan reproduced identical findings (ENV: only src/check.ts:1272 GITHUB_TOKEN; EXEC/EVAL/FSWRITE: 0; hosts in the executable source: api.github.com, ghcr.io, pypi.org, registry.modelcontextprotocol.io, registry.npmjs.org, github.com, www.npmjs.com, static.modelcontextprotocol.io — the fetch calls themselves go through the injected `fetchFn`/`fetch` parameters whose call sites were read in full in the first pass). Verdict unchanged.
