# Audit — mcpaudit (@reneturcios/mcpaudit)

- **Repo:** github.com/CloudCorpRecords/mcpaudit (MIT)
- **Version:** 0.1.2 (package.json) — pin `@reneturcios/mcpaudit@0.1.2`
- **Bin:** `mcpaudit` → `dist/cli.js`
- **Dependencies:** `@modelcontextprotocol/sdk` ^1 (lock: 1.32.1), `zod` ^3 (lock: 3.25.76). Dev: @types/node ^20, tsx ^4, typescript ^5.
- **npm `files`:** `["dist", "server.json"]` — tests/fixtures/.github are NOT in the published package.
- **Method used:** Same sandbox block as the rest of this batch: git clone and tarball extraction to `src/mcpaudit/` failed (`Operation not permitted` / 0-byte files — network-fetched content cannot be written to disk by tar/python/node in this VM). Audit was done by downloading the codeload tarball of `main` in-memory (Python urllib), scanning every file, and reading `src/probe.ts`, `src/cli.ts` etc. in full from memory. No install, no execution of the tool.
- **Stated job:** Audit any MCP server: handshake, tool schemas, missing descriptions, error handling — by actually launching the server under test over stdio.

## Findings

### Install scripts — none
package.json scripts are only `build` (`tsc`), `dev`, `test`. No preinstall/postinstall/prepare.

### Network egress — none
Zero network code in `src/`: no `fetch`, http/https/net/tls, WebSocket, axios, or undici anywhere in src. Remote (HTTP) MCP targets are explicitly **refused**, not contacted: `src/probe.ts:103-107` + `remoteUnsupportedError()` at `src/probe.ts:73-75`. Hosts appearing elsewhere are docs/schema identifiers only (github.com, registry.npmjs.org in publish config, static.modelcontextprotocol.io schema URL in server.json, mcp.context7.com / mcp.deepwiki.com as README examples). No telemetry/analytics of any kind.

### Code execution — spawning the target server is the stated job, and only that
- `src/probe.ts:113-119` launches the user-specified server command via the SDK's `StdioClientTransport` (command + args + cwd exactly as given via CLI args, `--config` file, `--cmdline`, or the MCP tool — `src/cli.ts:5-9,58-60`, `src/mcp.ts`). It then does initialize, tools/list, prompts/resources counts, one deliberately-bad tools/call (`src/probe.ts:216-243`, name `mcpaudit_nonexistent_tool_zz9`), and a liveness ping.
- No `eval` / `new Function` / `vm` / direct `child_process` in src; no downloading of code; nothing remote is executed. This is exactly the exception the audit brief grants mcpaudit.

### Env access — full host env is passed TO the audited server (note)
- `src/probe.ts:109-111`: the probe builds the child environment by copying **every** `process.env` entry, then overlaying user-supplied `target.env` (`src/mcp.ts:26`: optional `env` record param, "Extra environment variables for the server process"; also settable via the audited config file).
- This env goes only to the locally spawned target process (the SDK transport requires an explicit env map; an MCP client normally inherits env for the server it launches, and servers commonly need API keys this way). mcpaudit itself sends nothing anywhere — it has no network code (above) and no fs writes in src (below).
- Practical implication, worth a note rather than a rejection: **the server being audited receives your full environment (including any API keys in it)**, because mcpaudit launches it the way a real MCP client would. Audit untrusted servers from a scrubbed environment.

### fs writes — none in src
No `writeFile/appendFile/createWriteStream/rm/unlink` in `src/`. Reads: user-specified config/tools-dump files (`src/cli.ts:13` `readFile`). All writes in the repo are in tests creating fixture servers/temp dirs.
No base64 blobs ≥200 chars, no obfuscation; sources are plain readable TypeScript.

## Verdict: CLEAN-WITH-NOTES
- Spawning the target MCP server is its stated job; it executes only the exact local command the user supplies, never remote/downloaded code, and refuses HTTP targets.
- It copies the full host `process.env` into that target server's environment (`src/probe.ts:109-111`) — local client-style inheritance needed to launch real servers, not exfiltration (mcpaudit has zero network egress and zero fs writes), but run it against untrusted servers with a scrubbed env.

## Method update (supersedes the method bullet above)
- **Primary method (per coordinator update): `gh api`.** Re-verified end-to-end via GitHub API:
  - `gh api repos/CloudCorpRecords/mcpaudit/git/trees/main?recursive=1` — full tree listing: **27 blobs, not truncated**, matching the earlier in-memory full-tree scan.
  - `gh api repos/CloudCorpRecords/mcpaudit/contents/<path>` (base64) — fetched and scanned: `package.json`, **all of `src/`** (audit, cli, index, mcp, probe, types), `server.json`, `Dockerfile` — 9 files. **Every contents-API blob SHA matched the tree-listing SHA.**
  - Coverage note: no `bin/` or `scripts/` directory exists in this repo — bin entry `dist/cli.js` is built from `src/cli.ts`. Tests/fixtures/docs/workflows/package-lock were covered by the earlier full-tree in-memory scan. The gh-api re-scan reproduced identical findings (NET: 0; ENV: only src/probe.ts:110; EXEC: StdioClientTransport at src/probe.ts:16,113; EVAL/FSWRITE: 0). Verdict unchanged.
