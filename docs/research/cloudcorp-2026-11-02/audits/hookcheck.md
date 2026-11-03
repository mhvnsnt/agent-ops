# Security Audit — hookcheck

- **Repo / package:** github.com/CloudCorpRecords/hookcheck — `@reneturcios/hookcheck`
- **Version (pin this):** 0.1.18
- **Bin:** `dist/cli.js` (CLI + stdio MCP server)
- **Dependencies:** `@modelcontextprotocol/sdk ^1`, `zod ^3` (dev: `@types/node ^20`, `tsx ^4`, `typescript ^5`)
- **License:** MIT
- **Method used:** git clone and codeload tarballs failed on this VM (clone symref write error; tarballs 0 bytes through the proxy). Source was fetched file-by-file through the GitHub API contents endpoint via the GitHub MCP connector (`get_file_contents`, the same contents API `gh api repos/CloudCorpRecords/hookcheck/contents/<path>` wraps), saved as raw API snapshots in `src/hookcheck/rawsnap/`, and audited in-memory with line-accurate scans; flagged lines were read in context.
- **Coverage:** `package.json`, `Dockerfile`, `server.json`, and ALL of `src/` (cli.ts, core.ts ~197KB, index.ts, mcp.ts, types.ts). No `bin/` or `scripts/` directory exists. `test/` not line-audited — not shipped (`files`: `dist`, `server.json`).

## Findings

- **Install scripts:** scripts are only `build` (tsc), `dev`, `test`. **No preinstall / postinstall / prepare.**
- **Network egress: none in the tool's own code.** Imports are only `node:fs` (read-only: `existsSync`, `lstatSync`, `readdirSync`, `readFileSync`, `statSync` — src/core.ts:7), `node:path`, MCP SDK (stdio), `zod`. Its README claim "no network in the core scan" matches the source.
- **Credential / env access: none in code.** The only `process.env` hits are comments describing shapes it detects in *scanned* code: src/core.ts:1113 (`process.env.NODE_ENV` given as a non-flagged example), src/core.ts:1200–1201 (env-dump shapes), src/core.ts:1311 (`process.env.SECRET` in a comment about print disclosure). The tool itself reads no environment variables.
- **Flagged-but-benign (detection DATA, read in context):** hookcheck is a hook/persistence auditor, so src/core.ts is full of attack-pattern data: exec-call name list at core.ts:345, curl-pipe-shell rule at core.ts:34, credential-path patterns (`~/.ssh`, `.aws/credentials`, `.gnupg`) at core.ts:956–965, `.npmrc` write detection at core.ts:1049–1071, fetch/eval flow analysis at core.ts:2394–2532. All are patterns/classifiers applied to scanned repos — the tool never performs these actions.
- **eval / exec:** no `eval`, `new Function`, `vm`, or `child_process` in the tool's own code (hits are the name lists/regexes above).
- **Obfuscation:** none; no long base64 blobs outside detection patterns.
- **fs writes:** none. Verdicts go to stdout / MCP responses. It reads the repo tree the user points it at.
- **Hosts in shipped files:** `github.com`, `static.modelcontextprotocol.io`, `registry.npmjs.org` (all metadata in package.json/server.json/Dockerfile label); `pyenv.run` at src/core.ts:2794 is an entry in a `KNOWN_INSTALLER_HOSTS` allowlist (data — the documented pyenv installer endpoint, core.ts:2800–2803), never contacted.

## Verdict: CLEAN

No egress, no credential/env reads, no execution, no writes. All flagged content is the detection rule set for its stated job.
