# Audit — skillcheck (@reneturcios/skillcheck)

- **Repo:** github.com/CloudCorpRecords/skillcheck (MIT)
- **Version:** 0.1.0 (package.json) — pin `@reneturcios/skillcheck@0.1.0`
- **Bin:** `skillcheck` → `dist/cli.js`
- **Dependencies:** `@modelcontextprotocol/sdk` ^1 (lock: 1.32.2), `zod` ^3 (lock: 3.25.76). Dev: @types/node ^20, tsx ^4, typescript ^5.
- **npm `files`:** `["dist", "server.json"]` — tests/fixtures/.github are NOT in the published package.
- **Method used:** Same sandbox block as the rest of this batch: git clone and tarball extraction to `src/skillcheck/` failed (`Operation not permitted` / 0-byte files). Audit was done by downloading the codeload tarball of `main` in-memory (Python urllib) and scanning/reading every file from memory. No install, no execution of the tool.
- **Stated job:** SKILL.md validator: frontmatter presence/shape, name matching the directory, description present, markdown links resolving to real files, referenced files existing on disk.

## Findings

- **Install scripts:** none. Scripts are only `build` (`tsc`), `dev`, `test`.
- **Network egress:** none. No fetch/http/https/net/tls/WebSocket/axios/undici anywhere in `src/`. Despite checking "dead links", links are resolved against the local filesystem (`existsSync` on the resolved destination, `src/core.ts:406,426`) — external URLs are never fetched. Hosts elsewhere are docs/schema only (github.com, registry.npmjs.org publish config, static.modelcontextprotocol.io schema string) plus `example.com` inside a test fixture SKILL.md.
- **Env/credential access:** none. Zero `process.env` reads in src; no credential-store paths (~/.ssh, ~/.aws, keychain, browser profiles, .git-credentials, .npmrc) anywhere in src.
- **Execution:** none in src. No child_process/spawn, no `eval`/`new Function`/`vm`, no curl|sh. The only `exec` matches are `RegExp.prototype.exec` (`src/core.ts:132,390,420`). spawn/writeFile appear only in test harness files (not shipped).
- **fs behaviour:** read-only, scoped to the user-specified skill directory: `existsSync` / `readFileSync` / `statSync` (`src/core.ts:16,253-279,406,426`) on SKILL.md and files it references. **No fs writes anywhere in src.**
- **Obfuscation:** none. No base64 strings ≥200 chars; plain readable TypeScript.

## Verdict: CLEAN
Fully local, read-only validator. No egress, no env/credential access, no execution, no writes, no install scripts.

## Method update (supersedes the method bullet above)
- **Primary method (per coordinator update): `gh api`.** Re-verified end-to-end via GitHub API:
  - `gh api repos/CloudCorpRecords/skillcheck/git/trees/main?recursive=1` — full tree listing: **25 blobs, not truncated**, matching the earlier in-memory full-tree scan.
  - `gh api repos/CloudCorpRecords/skillcheck/contents/<path>` (base64) — fetched and scanned: `package.json`, **all of `src/`** (cli, core, index, mcp, types), `server.json`, `Dockerfile` — 8 files. **Every contents-API blob SHA matched the tree-listing SHA.**
  - Coverage note: no `bin/` or `scripts/` directory exists in this repo — bin entry `dist/cli.js` is built from `src/cli.ts`. Tests/fixtures/docs/workflows/package-lock were covered by the earlier full-tree in-memory scan. The gh-api re-scan of all executable source found NET/ENV/EXEC/EVAL/FSWRITE all 0. Verdict unchanged.
