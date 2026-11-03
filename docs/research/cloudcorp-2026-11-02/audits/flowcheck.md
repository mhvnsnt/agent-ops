# Security Audit — flowcheck

- **Repo / package:** github.com/CloudCorpRecords/flowcheck — `@reneturcios/flowcheck`
- **Version (pin this):** 0.1.2
- **Bin:** `dist/cli.js` (CLI + stdio MCP server)
- **Dependencies:** `@modelcontextprotocol/sdk ^1`, `yaml ^2.6.0`, `zod ^3` (dev: `@types/node ^20`, `tsx ^4`, `typescript ^5`)
- **License:** MIT
- **Method used:** git clone and codeload tarballs failed on this VM (clone symref write error; tarballs 0 bytes through the proxy). Source was fetched file-by-file through the GitHub API contents endpoint via the GitHub MCP connector (`get_file_contents`, the same contents API `gh api repos/CloudCorpRecords/flowcheck/contents/<path>` wraps), saved as raw API snapshots in `src/flowcheck/rawsnap/`, and audited in-memory with line-accurate scans; flagged lines were read in context.
- **Coverage:** `package.json`, `Dockerfile`, `server.json`, and ALL of `src/` (cli.ts, core.ts, index.ts, mcp.ts, types.ts). No `bin/` or `scripts/` directory exists. `test/` not line-audited — not shipped (`files`: `dist`, `server.json`).

## Findings

- **Install scripts:** scripts are only `build` (tsc), `dev`, `test`. **No preinstall / postinstall / prepare.**
- **Network egress: none.** Imports are only `node:fs` (read-only: `readdirSync`, `readFileSync`, `statSync` — src/core.ts:22), `node:path`, the `yaml` parser, MCP SDK (stdio), `zod`. A grep for `fetch`/http across all source returns zero hits in the tool's own code.
- **Credential / env access: none.** Zero `process.env` reads. The two `GITHUB_TOKEN` hits are advisory prose *about the workflows being audited*: src/core.ts:567 (explaining that a missing top-level `permissions:` block leaves the default token permissive) and src/core.ts:742 (a note that a job which never uses the token can run with `permissions: {}`). The tool never touches a real token.
- **eval / exec:** none — no `eval`, `new Function`, `vm`, `child_process`.
- **Obfuscation:** none.
- **fs writes:** none. It parses workflow YAML under the user-supplied path and renders a report/plan to stdout; even its "harden plan" is output as text, not applied.
- **Hosts in shipped files (metadata only):** `github.com`, `static.modelcontextprotocol.io`, `registry.npmjs.org` (package.json/server.json/Dockerfile label).

## Verdict: CLEAN

A purely local, read-only auditor: no egress, no env/credential access, no execution, no writes.
