# Security Audit — actionpin

- **Repo / package:** github.com/CloudCorpRecords/actionpin — `@reneturcios/actionpin`
- **Version (pin this):** 0.1.8
- **Bin:** `dist/cli.js` (CLI + stdio MCP server)
- **Dependencies:** `@modelcontextprotocol/sdk ^1`, `zod ^3` (dev: `@types/node ^20`, `tsx ^4`, `typescript ^5`)
- **License:** MIT
- **Method used:** git clone and codeload tarballs failed on this VM (clone symref write error; tarballs 0 bytes through the proxy). Source was fetched file-by-file through the GitHub API contents endpoint via the GitHub MCP connector (`get_file_contents`, the same contents API `gh api repos/CloudCorpRecords/actionpin/contents/<path>` wraps), saved as raw API snapshots in `src/actionpin/rawsnap/`, and audited in-memory with line-accurate scans; flagged lines were read in context.
- **Coverage:** `package.json`, `Dockerfile`, `server.json`, and ALL of `src/` (cli.ts, core.ts, index.ts, mcp.ts, types.ts). No `bin/` or `scripts/` directory exists. `test/` not line-audited — not shipped (`files`: `dist`, `server.json`).

## Findings

- **Install scripts:** scripts are only `build` (tsc), `dev`, `test`. **No preinstall / postinstall / prepare.**
- **Credential access — justified:** reads exactly one env key, `process.env.GITHUB_TOKEN`, at src/core.ts:860 inside `ghHeaders()`. It is placed only in an `Authorization: Bearer` header (src/core.ts:861) sent to **hardcoded** `https://api.github.com` URLs (src/core.ts:881–884 git-ref/commit lookups; src/core.ts:900–903 annotated-tag dereference). There is no base-URL override anywhere in the tool, so the token cannot be redirected to another host by configuration. Resolving a tag to a commit SHA is impossible without the GitHub API — this is the tool's stated job. The token is optional (requests work unauthenticated at lower rate limits).
- **Network egress:** `api.github.com` only, via an injectable `FetchFn` (real global `fetch` passed in at src/cli.ts:98,103 and src/mcp.ts:42; unit tests inject fixtures and never touch the network, src/types.ts:135–146). No other hosts are contacted; `github.com` / `static.modelcontextprotocol.io` / `registry.npmjs.org` appear only as metadata in package.json/server.json.
- **fs writes — feature-scoped:** the CLI `fix` command rewrites the user's own workflow files in place at src/core.ts:1046 (`writeFileSync(file, lines.join("\n"))` inside `applyPinPlan`) — that rewrite *is* the tool's purpose, is user-invoked, and has a `--dry-run` path. The MCP surface exposes only `auditWorkflows` / `auditOrg` / `buildPinPlan` (src/mcp.ts:7), not the apply/write path.
- **eval / exec:** none — no `eval`, `new Function`, `vm`, `child_process`. No `~/.ssh`, `~/.aws`, keychain, or browser-profile access.
- **Obfuscation / data collection:** none. No telemetry endpoints.

## Verdict: CLEAN-WITH-NOTES

Notes: (1) `GITHUB_TOKEN` env read at src/core.ts:860, sent only as a Bearer header to hardcoded api.github.com endpoints to resolve action refs to SHAs — required by its job, no override path. (2) Egress is api.github.com only. (3) The CLI `fix` command writes the user's workflow files in place (src/core.ts:1046) — the tool's stated purpose; the MCP tools are read/plan-only.
