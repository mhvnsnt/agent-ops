# Security Audit — specforge

- **Repo:** github.com/CloudCorpRecords/specforge (MIT)
- **Version:** 0.1.0 (`package.json`)
- **npm:** `@reneturcios/specforge` · **Bin:** `specforge` → `dist/cli.js`
- **Dependencies:** runtime `@modelcontextprotocol/sdk ^1`, `zod ^4`; dev `@types/node ^20`, `tsx ^4`, `typescript ^5`
- **Method used:** `git clone` is broken VM-wide (“unable to write symref for HEAD: Operation not permitted”) and codeload tarballs return 0 bytes through the proxy, and tar extraction into the scratch tree hit write-EPERM — so no local `src/` copy could be persisted. Primary method per coordinator: `gh api repos/CloudCorpRecords/specforge/git/trees/main?recursive=1` for the file inventory and `gh api repos/CloudCorpRecords/specforge/contents/<path>` (base64 content) for source, cross-checked with streamed `raw.githubusercontent.com` reads: full-file reads of `package.json` and `src/specforge.ts` (including the executor section at the end), and `grep -n` scans of the remaining files listed under Coverage. Nothing was installed or run.
- **Coverage:** All executable source covered — `package.json`, every file in `src/` (`cli.ts`, `index.ts`, `mcp.ts`, `specforge.ts`, `types.ts`), plus `test/specforge.test.ts`, `Dockerfile`, `server.json`, workflows. `README.md` / `BUILD-REPORT.md` / `CHANGELOG.md` are docs (inventoried).

## Findings

- **Install hooks:** Scripts are `build`, `dev`, `test` only. **No** `preinstall` / `postinstall` / `prepare`.
- **Network egress in specforge's own code: none directly.** No `fetch`, `http/https/net/tls`, or WebSocket anywhere in `src/` (grep-verified). MCP mode is stdio-only (`src/mcp.ts` registers the spec/git/quality tools over `StdioServerTransport`). Indirect egress via the quality tools is itemised below.
- **Env access: exactly one variable.** `SPECFORGE_ROOT` — `src/specforge.ts` `ROOT_ENV` / `resolveRoot()` (`src/specforge.ts:47`; call sites `src/cli.ts:123`, `src/mcp.ts:305`). It only sets the workspace root path (default: CWD). No other `process.env` reads in `src/`; no credential stores, tokens, `~/.ssh` / `~/.aws` / Keychain access.
- **Filesystem writes — confined to the specs tree:** all `writeFile`/`appendFile` hits (`src/specforge.ts:183-525`) write inside `<root>/specs/<NNN>-<slug>/`: `spec.md`, `research.md`, `constitution.md`, `plan.md`, `tasks.md`, `clarifications.json` (+ a `contracts/` dir). That is the tool's stated function.
- **Code execution — fixed command table through a shell-free executor:** `src/specforge.ts:659` `defaultExecutor` is `execFile(command, args, { cwd }, …)` — **no shell**. The only commands ever passed to it are hardcoded in the same file (end of `src/specforge.ts`):
  - `git checkout -b <branch>` (`gitCreateBranch`; branch name validated: non-empty, no whitespace),
  - `npx prettier --check .` or, with fix, `--write` (`qualityFormat`),
  - `npx eslint . [--fix]` (`qualityLint`),
  - `npm test [-- --coverage]` (`qualityTest`),
  - `npm audit [fix]` (`qualitySecurityAudit`).
  No arbitrary command string from user input, spec files, or config is ever executed; the `Executor` is injectable only programmatically (tests inject fakes).
- **Consequences of those fixed commands (the notes):**
  1. **`npx prettier` / `npx eslint` will download those packages from `registry.npmjs.org` and run them** if they are not already in the target project's `node_modules` — network egress + execution of downloaded (mainstream, but downloaded) code, triggered only by explicitly invoking the `quality_format` / `quality_lint` tools.
  2. **`npm audit` sends the project's dependency names/versions to `registry.npmjs.org`** (standard npm audit behaviour), and with `fix: true`, **`npm audit fix` modifies `package.json` / lockfile / `node_modules`**. Likewise `prettier --write` and `eslint --fix` mutate project files. All fix modes are explicit caller options, not defaults.
- **Metadata / CI:** `server.json` carries `static.modelcontextprotocol.io` (schema), `registry.npmjs.org` (registryBaseUrl), `ghcr.io` image id, `github.com` repo strings — manifest metadata, not fetched by the tool. Dockerfile is a plain multi-stage `node:20-alpine` build (`npm ci --no-audit --no-fund`, no curl). Workflows are the fleet template (`registry-publish.yml:17` CI-only `curl` of mcp-publisher v1.8.1; `publish.yml` uses `secrets.NPM_TOKEN` in CI).
- **Obfuscation / data collection:** None. Plain readable TypeScript; no telemetry/analytics, no minified blobs.

## Verdict: CLEAN-WITH-NOTES

Notes: (1) env access is limited to **`SPECFORGE_ROOT`** (workspace path); (2) its quality/git tools run a **fixed, shell-free command table** (`git checkout -b`, `npx prettier`, `npx eslint`, `npm test`, `npm audit`) in the target project — of which **`npx` can download and run prettier/eslint from `registry.npmjs.org`** when absent locally, **`npm audit` reports the dependency list to the npm registry**, and the opt-in **fix modes mutate project files/dependencies**. All are the tool's stated quality-check job, explicitly invoked, with no arbitrary-command surface. No direct egress, no credentials, no install hooks.
