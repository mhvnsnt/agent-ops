# Audit — testdelta (@reneturcios/testdelta)

- **Repo:** github.com/CloudCorpRecords/testdelta (MIT)
- **Version:** 0.1.0 (package.json) — pin `@reneturcios/testdelta@0.1.0`
- **Bin:** `testdelta` → `dist/cli.js`
- **Dependencies:** `@modelcontextprotocol/sdk` ^1 (lock: 1.32.2), `zod` ^3 (lock: 3.25.76). Dev: @types/node ^20, tsx ^4, typescript ^5.
- **npm `files`:** `["dist", "server.json"]` — tests/fixtures/.github are NOT in the published package.
- **Method used:** Same sandbox block as the rest of this batch: git clone and tarball extraction to `src/testdelta/` failed (`Operation not permitted` / 0-byte files). Audit was done by downloading the codeload tarball of `main` in-memory (Python urllib) and scanning/reading every file from memory. No install, no execution of the tool.
- **Stated job:** Base-vs-head test result differ: given two test result JSON files, reports named tests added, removed, fixed, and broken.

## Findings

- **Install scripts:** none. Scripts are only `build` (`tsc`), `dev`, `test`.
- **Network egress:** none. No fetch/http/https/net/tls/WebSocket/axios/undici anywhere in `src/`. Hosts in the repo are docs/schema only (github.com, registry.npmjs.org publish config, static.modelcontextprotocol.io schema string in server.json). No telemetry/analytics.
- **Env/credential access:** none. Zero `process.env` reads in src; no credential-store paths anywhere in src.
- **Execution:** none in src. No child_process/spawn/exec, no `eval`/`new Function`/`vm`, no curl|sh. spawn/writeFile appear only in test harness files (not shipped).
- **fs behaviour:** read-only, scoped to the user-specified result file(s): `readFileSync` / `statSync` (`src/core.ts:28,99,113,122,129`) on the base/head JSON inputs. **No fs writes anywhere in src.**
- **Obfuscation:** none. No base64 strings ≥200 chars; plain readable TypeScript; test fixtures are tiny hand-readable JSON pairs.

## Verdict: CLEAN
Fully local, read-only differ. No egress, no env/credential access, no execution, no writes, no install scripts.

## Method update (supersedes the method bullet above)
- **Primary method (per coordinator update): `gh api`.** Re-verified end-to-end via GitHub API:
  - `gh api repos/CloudCorpRecords/testdelta/git/trees/main?recursive=1` — full tree listing: **30 blobs, not truncated**, matching the earlier in-memory full-tree scan.
  - `gh api repos/CloudCorpRecords/testdelta/contents/<path>` (base64) — fetched and scanned: `package.json`, **all of `src/`** (cli, core, index, mcp, types), `server.json`, `Dockerfile` — 8 files. **Every contents-API blob SHA matched the tree-listing SHA.**
  - Coverage note: no `bin/` or `scripts/` directory exists in this repo — bin entry `dist/cli.js` is built from `src/cli.ts`. Tests/fixtures/docs/workflows/package-lock were covered by the earlier full-tree in-memory scan. The gh-api re-scan of all executable source found NET/ENV/EXEC/EVAL/FSWRITE all 0. Verdict unchanged.
