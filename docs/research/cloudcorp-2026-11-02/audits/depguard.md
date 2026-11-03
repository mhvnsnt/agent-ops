# Security Audit — depguard

- **Repo / package:** github.com/CloudCorpRecords/depguard — `@reneturcios/depguard`
- **Version (pin this):** 0.4.0
- **Bin:** `dist/cli.js` (CLI + stdio MCP server)
- **Dependencies:** `@modelcontextprotocol/sdk ^1`, `zod ^3` (dev: `@types/node ^20`, `tsx ^4`, `typescript ^5`)
- **License:** MIT
- **Method used:** git clone and codeload tarballs failed on this VM (clone symref write error; tarballs 0 bytes through the proxy). Source was fetched file-by-file through the GitHub API contents endpoint via the GitHub MCP connector (`get_file_contents`, the same contents API `gh api repos/CloudCorpRecords/depguard/contents/<path>` wraps), saved as raw API snapshots in `src/depguard/rawsnap/`, and audited in-memory with line-accurate scans; flagged lines were read in context.
- **Coverage:** `package.json`, `Dockerfile`, `server.json`, and ALL of `src/` (cli.ts, content.ts, core.ts, history.ts, index.ts, mcp.ts, popular.ts, registry.ts). No `bin/` or `scripts/` directory exists. `test/` not line-audited — not shipped (`files`: `dist`, `server.json`).

## Findings

- **Install scripts:** scripts are only `build` (tsc), `dev`, `test`. **No preinstall / postinstall / prepare.** (Fittingly, flagging other packages' install scripts is this tool's job.)
- **Network egress — opt-in only, two registry hosts:** the core is offline. Online checks run only behind explicit flags (`--online`, `--content` parsed at src/cli.ts:84–96; registry.ts:1–6 header states "These run ONLY behind an explicit online flag"). Endpoints: `https://registry.npmjs.org/<name>` packuments (src/registry.ts:24, src/content.ts:44, src/history.ts:339) and `https://pypi.org/pypi/<name>/json` (src/history.ts:337–339). In content mode it also downloads both versions' tarballs from the packument's own `dist.tarball` URL (src/content.ts:48–55, byte-capped by `MAX_TARBALL_BYTES`) and extracts them **in memory only** (src/content.ts:60–63: "Extracts to an in-memory map only") for static diffing — downloaded code is never written to disk, installed, or executed. No tokens are sent (no auth headers; the tool reads no env vars at all).
- **Credential / env access: none.** Zero `process.env` reads in the entire source; no token of any kind. The `.ssh` / `.aws` / `process.env`-secret hits at src/content.ts:113–123 and the `RISKY_SCRIPT_RE` at src/core.ts:427 are detection rules applied to *scanned packages'* files — data, not behavior.
- **child_process — one justified, safe use:** `execFileSync("git", ["-C", dir, "show", `${ref}:${file}`], …)` at src/core.ts:408 inside `loadSnapshotFromGit()` — fixed binary, argv array, no shell, so the user-supplied `--base <ref>` cannot become shell injection. It reads dependency manifests at a git ref, which is the tool's stated function.
- **fs writes:** none. No write/append/mkdir calls in src/.
- **eval / obfuscation:** no `eval`, `new Function`, or `vm`; no long base64 blobs outside detection patterns. `gunzipSync` (src/content.ts:21) is used solely for the in-memory tarball reader above.
- **Other hosts in shipped files (metadata only):** `github.com`, `static.modelcontextprotocol.io`, `registry.npmjs.org` (server.json/package.json).

## Verdict: CLEAN-WITH-NOTES

Notes: (1) Egress to registry.npmjs.org and pypi.org occurs only in explicit `--online` / `--content` / history modes; tarballs are fetched from the registry packument's URL, size-capped, and parsed in memory — never installed or executed. (2) One child-process call: `execFileSync("git", …)` with a fixed binary and argv array at src/core.ts:408 to read manifests at a git ref — its stated job, no shell. (3) No env vars, tokens, or credential stores are read at all.
