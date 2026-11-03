# Security Audit — injectcheck

- **Repo / package:** github.com/CloudCorpRecords/injectcheck — `@reneturcios/injectcheck`
- **Version (pin this):** 0.1.19
- **Bin:** `dist/cli.js` (single bin serves CLI + stdio MCP server)
- **Dependencies:** `@modelcontextprotocol/sdk ^1`, `zod ^3` (dev: `@types/node ^20`, `tsx ^4`, `typescript ^5`)
- **License:** MIT
- **Method used:** git clone and codeload tarballs failed on this VM (clone symref write error; tarballs 0 bytes through the proxy). Source was fetched file-by-file through the GitHub API contents endpoint via the GitHub MCP connector (`get_file_contents`, the same contents API `gh api repos/CloudCorpRecords/injectcheck/contents/<path>` wraps), saved as raw API snapshots in `src/injectcheck/rawsnap/`, and audited in-memory with line-accurate scans; flagged lines were read in context.
- **Coverage:** `package.json`, `Dockerfile`, `server.json`, and ALL of `src/` (cli.ts, index.ts, mcp.ts, scan.ts, types.ts). No `bin/` or `scripts/` directory exists in the repo. `test/` and docs were not line-audited — they are not shipped (package.json `files`: `dist`, `server.json`).

## Findings

- **Install scripts:** package.json scripts are only `build` (tsc), `dev`, `test`. **No preinstall / postinstall / prepare.**
- **Network egress: none in the tool's own code.** Imports across all of src/ are only `node:fs` (read-only: `readFileSync`, `readdirSync`, `statSync` — src/cli.ts:24, src/scan.ts:21), `node:path`, the MCP SDK (stdio transport), and `zod`. No `fetch`, no http/https/net/tls modules, no WebSocket, no telemetry/analytics endpoints anywhere.
- **Credential / env access: none.** Zero `process.env` reads in the entire source.
- **Flagged-but-benign (detection DATA, read in context):** this is a prompt-injection scanner, so its rule tables contain the attack strings it detects. Examples: exfil-noun regex at src/scan.ts:309 (credentials/secrets/`~/.ssh`/`id_rsa`/`.aws`/`.npmrc` patterns), credential-read pattern at src/scan.ts:871, curl|sh / wget|sh lure rules at src/scan.ts:1609–1610, placeholder URLs in comments at src/scan.ts:1632–1636. All are RegExp literals matched against scanned content — never executed, never fetched.
- **eval / exec:** no `eval`, `new Function`, `vm`, or `child_process` anywhere. (The many `.exec(` hits are `RegExp.prototype.exec`.)
- **Obfuscation:** none. No long base64 blobs in shipped source; base64 strings appear only inside detection rules.
- **fs writes:** none. Output is stdout only. The tool reads only the path/file/text the user asks it to scan.
- **Hosts appearing in shipped files (metadata only, never contacted):** `github.com` (package homepage + Dockerfile OCI label, Dockerfile:22), `static.modelcontextprotocol.io` (server.json `$schema`), `registry.npmjs.org` (server.json registry base).
- **Dockerfile:** two-stage build; `npm ci` runs at image-build time only — not an install hook of the npm package.

## Verdict: CLEAN

No egress, no env/credential access, no execution primitives, no writes. Every flagged string is detection-rule data for the scanner's stated job.
