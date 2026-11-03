# Security Audit — readmeaudit

- **Repo:** github.com/CloudCorpRecords/readmeaudit (MIT)
- **Version:** 0.1.0 (`package.json`)
- **npm:** `@reneturcios/readmeaudit` · **Bin:** `readmeaudit` → `dist/cli.js`
- **Dependencies:** runtime `@modelcontextprotocol/sdk ^1`, `zod ^3`; dev `@types/node ^20`, `tsx ^4`, `typescript ^5`
- **Method used:** `git clone` is broken VM-wide (“unable to write symref for HEAD: Operation not permitted”) and codeload tarballs return 0 bytes through the proxy, and tar extraction into the scratch tree hit write-EPERM — so no local `src/` copy could be persisted. Primary method per coordinator: `gh api repos/CloudCorpRecords/readmeaudit/git/trees/main?recursive=1` for the file inventory and `gh api repos/CloudCorpRecords/readmeaudit/contents/<path>` (base64 content) for source, cross-checked with streamed `raw.githubusercontent.com` reads (`curl | grep -n` for exact line numbers; full-file reads of `package.json`, `src/cli.ts`, `src/mcp.ts`). Nothing was installed or run.
- **Coverage:** All executable source covered — `package.json`, every file in `src/` (`cli.ts`, `core.ts`, `index.ts`, `mcp.ts`, `types.ts`), plus `Dockerfile`, `server.json`, workflows, and `test/` (grep-scanned). Test fixtures under `test/fixtures/` were covered by tree listing + the fixture-consuming code/tests, not by full per-fixture download.

## Findings

- **Install hooks:** `package.json` scripts are only `build` (`tsc`), `dev`, `test`. **No** `preinstall` / `postinstall` / `prepare`.
- **Network egress:** None in source. No `fetch`, `http/https/net/tls`, WebSocket, or URL literals anywhere in `src/` or `test/` (grep-verified). The MCP mode is stdio-only (`src/mcp.ts`, `StdioServerTransport`, single tool `audit_readme`).
- **Credential / env / secret access:** None. No `process.env` anywhere in `src/`; no `~/.ssh`, `~/.aws`, Keychain, browser-profile, or token access.
- **Code execution:** No `eval`, `new Function`, or `child_process` in `src/`. Hits for `exec(` are RegExp: `src/core.ts:146` `pattern.exec(line)`, `src/core.ts:317` token set lookup.
- **Filesystem:** Read-only in `src/`. `src/core.ts:24` imports `existsSync, readFileSync, readdirSync, statSync`; reads are of the *target package being audited* — `src/core.ts:79` its `package.json`, `:95` its README, `:250` its source files. No `writeFile` in `src/`.
- **Tests only:** `test/pipe.test.ts:19,77` spawns the tool's own CLI in temp fixture dirs; `test/core.test.ts` `writeFileSync` writes fixture files under `mkdtemp` dirs. Test code, not shipped runtime.
- **Hardcoded hosts (metadata only, never fetched by the tool):** `github.com` (repo URL / OCI label, `Dockerfile:22`), `static.modelcontextprotocol.io` (`server.json` `$schema`), `registry.npmjs.org` (`server.json` `registryBaseUrl` — MCP registry manifest metadata).
- **CI note (not shipped code):** `.github/workflows/registry-publish.yml:18` downloads the official MCP registry publisher (`curl -L https://github.com/modelcontextprotocol/registry/releases/download/v1.8.1/mcp-publisher_linux_amd64.tar.gz | tar xz`) in the author's publish workflow; `publish.yml` uses `secrets.NPM_TOKEN` in CI. Standard fleet template; does not run at install or runtime.
- **Obfuscation / data collection:** None. All TypeScript is plain readable source; no minified blobs, no base64 payloads, no telemetry/analytics.

## Verdict: CLEAN

A purely local, read-only README-vs-package auditor. No egress, no env/credential access, no install hooks, no writes outside test temp dirs.
