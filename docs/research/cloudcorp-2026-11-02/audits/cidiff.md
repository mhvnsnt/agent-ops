# Security Audit — cidiff

- **Repo / package:** github.com/CloudCorpRecords/cidiff — `@reneturcios/cidiff`
- **Version (pin this):** 0.1.2
- **Bin:** `dist/cli.js` (CLI + stdio MCP server)
- **Dependencies:** `@modelcontextprotocol/sdk ^1`, `zod ^3` (dev: `@types/node ^20`, `tsx ^4`, `typescript ^5`)
- **License:** MIT
- **Method used:** git clone and codeload tarballs failed on this VM (clone symref write error; tarballs 0 bytes through the proxy). Source was fetched file-by-file through the GitHub API contents endpoint via the GitHub MCP connector (`get_file_contents`, the same contents API `gh api repos/CloudCorpRecords/cidiff/contents/<path>` wraps), saved as raw API snapshots in `src/cidiff/rawsnap/`, and audited in-memory with line-accurate scans; flagged lines were read in context.
- **Coverage:** `package.json`, `Dockerfile`, `server.json`, and ALL of `src/` (cli.ts, diff.ts, index.ts, mcp.ts, types.ts). No `bin/` or `scripts/` directory exists. `test/` not line-audited — not shipped (`files`: `dist`, `server.json`).

## Findings

- **Install scripts:** scripts are only `build` (tsc), `dev`, `test`. **No preinstall / postinstall / prepare.**
- **Credential access — justified:** `GITHUB_TOKEN` is read at src/diff.ts:573 and src/diff.ts:600 (`token ?? process.env.GITHUB_TOKEN`, an explicit token parameter wins) and sent only as `Authorization: Bearer` by `ghHeaders()` (src/diff.ts:68–75) on GitHub API requests for PR / check-run / status data (src/diff.ts:425, 464–465). Comparing a PR's CI against its base requires the GitHub API — this is the tool's stated job.
- **Network egress:** GitHub API only. Default base is the hardcoded `https://api.github.com` (src/diff.ts:21). **Note the override:** `githubApiBase()` (src/diff.ts:29–34) honors `CIDIFF_GITHUB_BASE_URL`, then `GITHUB_BASE_URL`, before falling back to the public API — the comment (src/diff.ts:24–27) documents this as the GitHub Enterprise / localhost-proxy pattern. If a user sets those env vars, their token is sent to the base *they* configured; nothing in the tool sets or influences that value.
- **Env keys read (complete list):** `GITHUB_TOKEN`, `CIDIFF_GITHUB_BASE_URL`, `GITHUB_BASE_URL`. Nothing else.
- **fs writes:** none anywhere in src/ (no write imports). Reports go to stdout / MCP responses.
- **eval / exec:** none — no `eval`, `new Function`, `vm`, `child_process`. No `~/.ssh`, `~/.aws`, keychain, or browser-profile access.
- **Obfuscation / data collection:** none. No telemetry endpoints. Other hosts in shipped files are metadata only (`github.com`, `static.modelcontextprotocol.io`, `registry.npmjs.org`).

## Verdict: CLEAN-WITH-NOTES

Notes: (1) `GITHUB_TOKEN` read at src/diff.ts:573,600 for GitHub API auth — its job requires it. (2) Egress is the GitHub API; the API base defaults to api.github.com but is user-overridable via `CIDIFF_GITHUB_BASE_URL` / `GITHUB_BASE_URL` (src/diff.ts:29–34), in which case the token goes to the user-configured base (standard GHE pattern). (3) No writes, no exec, no other env access.
