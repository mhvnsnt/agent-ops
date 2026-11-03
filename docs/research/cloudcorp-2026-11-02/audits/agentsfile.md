# Audit — agentsfile (@reneturcios/agentsfile)

- **Repo:** github.com/CloudCorpRecords/agentsfile (MIT)
- **Version:** 0.1.0 (package.json) — pin `@reneturcios/agentsfile@0.1.0`
- **Bin:** `agentsfile` → `dist/cli.js`
- **Dependencies:** `@modelcontextprotocol/sdk` ^1 (lock: 1.32.2), `zod` ^3 (lock: 3.25.76). Dev: @types/node ^20, tsx ^4, typescript ^5.
- **npm `files`:** `["dist", "server.json"]` — tests/fixtures/.github are NOT in the published package.
- **Method used:** Same sandbox block as the rest of this batch: git clone and tarball extraction to `src/agentsfile/` failed (`Operation not permitted` / 0-byte files). Audit was done by downloading the codeload tarball of `main` in-memory (Python urllib) and scanning/reading every file from memory. No install, no execution of the tool.
- **Stated job:** Validate AGENTS.md and CLAUDE.md against repo reality: referenced paths, package.json scripts, and documented commands checked against the actual tree.

## Findings

- **Install scripts:** none. Scripts are only `build` (`tsc`), `dev`, `test`.
- **Network egress:** none. No fetch/http/https/net/tls/WebSocket/axios/undici anywhere in `src/`. Hosts in the repo are only github.com (docs/homepage), registry.npmjs.org (publish config), and the static.modelcontextprotocol.io schema identifier string in server.json (not fetched). No telemetry/analytics endpoints or code.
- **Env/credential access:** none. Zero `process.env` reads in src. Examined and benign: `src/core.ts:55` includes the string `".npmrc"` in a list of well-known config **filenames** whose existence in the checked repo is tested with `existsSync` (`src/core.ts:85`) — the file's contents are never read, and no credential store (~/.ssh, ~/.aws, keychain, browser profiles, .git-credentials) is touched anywhere.
- **Execution:** none in src. No child_process/spawn/exec of commands, no `eval`/`new Function`/`vm`, no curl|sh. (spawn/writeFile matches exist only in `test/pipe.test.ts`, the test harness that launches the tool's own CLI — test code, not shipped.)
- **fs behaviour:** read-only, scoped to the user-specified repo: `existsSync` / `readFileSync` / `statSync` (`src/core.ts:16,85,156-158,186,261,276`) on AGENTS.md/CLAUDE.md, package.json, and paths those files reference. **No fs writes anywhere in src.**
- **Obfuscation:** none. No base64 strings ≥200 chars; plain readable TypeScript.

## Verdict: CLEAN
Fully local, read-only validator. No egress, no env/credential access, no execution, no writes, no install scripts.

## Method update (supersedes the method bullet above)
- **Primary method (per coordinator update): `gh api`.** Re-verified end-to-end via GitHub API:
  - `gh api repos/CloudCorpRecords/agentsfile/git/trees/main?recursive=1` — full tree listing: **35 blobs, not truncated**, matching the earlier in-memory full-tree scan.
  - `gh api repos/CloudCorpRecords/agentsfile/contents/<path>` (base64) — fetched and scanned: `package.json`, **all of `src/`** (cli, core, index, mcp, types), `server.json`, `Dockerfile` — 8 files. **Every contents-API blob SHA matched the tree-listing SHA.**
  - Coverage note: no `bin/` or `scripts/` directory exists in this repo — bin entry `dist/cli.js` is built from `src/cli.ts`. Tests/fixtures/docs/workflows/package-lock were covered by the earlier full-tree in-memory scan. The gh-api re-scan of all executable source found NET/ENV/EXEC/EVAL/FSWRITE all 0. Verdict unchanged.
