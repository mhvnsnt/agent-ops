# Security Audit — commitcheck

- **Repo:** github.com/CloudCorpRecords/commitcheck (MIT)
- **Version:** 0.1.0 (`package.json`)
- **npm:** `@reneturcios/commitcheck` · **Bin:** `commitcheck` → `dist/cli.js`
- **Dependencies:** runtime `@modelcontextprotocol/sdk ^1`, `zod ^3`; dev `@types/node ^20`, `tsx ^4`, `typescript ^5`
- **Method used:** `git clone` is broken VM-wide (“unable to write symref for HEAD: Operation not permitted”) and codeload tarballs return 0 bytes through the proxy, and tar extraction into the scratch tree hit write-EPERM — so no local `src/` copy could be persisted. Primary method per coordinator: `gh api repos/CloudCorpRecords/commitcheck/git/trees/main?recursive=1` for the file inventory and `gh api repos/CloudCorpRecords/commitcheck/contents/<path>` (base64 content) for source, cross-checked with streamed `raw.githubusercontent.com` reads (`curl | grep -n` for exact line numbers; full-file reads of `package.json`, `src/cli.ts`, `src/mcp.ts`, and the `src/core.ts` git-call context). Nothing was installed or run.
- **Coverage:** All executable source covered — `package.json`, every file in `src/` (`cli.ts`, `core.ts`, `index.ts`, `mcp.ts`, `types.ts`), plus `Dockerfile`, `server.json`, workflows, and `test/` (grep-scanned). Test fixtures under `test/fixtures/` (plain commit-message `.txt` files) were covered by tree listing, not full per-fixture download.

## Findings

- **Install hooks:** `package.json` scripts are only `build` (`tsc`), `dev`, `test`. **No** `preinstall` / `postinstall` / `prepare`.
- **Network egress:** None. No `fetch`, `http/https/net/tls`, WebSocket, or URL literals in `src/` (grep-verified). MCP mode is stdio-only (`src/mcp.ts`, tool `check_commits`).
- **Credential / env / secret access:** None. No `process.env` in `src/`; no `~/.ssh`, `~/.aws`, Keychain, browser-profile, or token access. It reads commit *messages* from the target repo's history — that is the tool's stated input, read locally via git.
- **Code execution — one fixed, shell-free subprocess:** `src/core.ts:19` imports `execFileSync` from `node:child_process`; `src/core.ts:308` calls
  `execFileSync("git", ["-C", target, "log", "-n", String(MAX_COMMITS), "--format=%H%x00%B%x1e"], { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 })`.
  Argument array, no `shell` option (so no shell interpretation), fixed subcommand/flags; `target` is the user-supplied repo path. This is the tool's core function (reading git history). No other subprocess use in `src/`; `exec(` hits at `src/core.ts:97,109` are RegExp matches. No `eval` / `new Function`.
- **Filesystem:** No writes in `src/` (grep-verified). Tests write git fixtures only under `mkdtemp` dirs and spawn the tool's own CLI (`test/pipe.test.ts:20,29,40,72`).
- **Hardcoded hosts (metadata only, never fetched):** `github.com` (repo URL / OCI label, `Dockerfile:22`), `static.modelcontextprotocol.io` (`server.json` `$schema`), `registry.npmjs.org` (`server.json` `registryBaseUrl`).
- **CI note (not shipped code):** `.github/workflows/registry-publish.yml:18` downloads the official MCP registry publisher v1.8.1 tarball (`curl -L https://github.com/modelcontextprotocol/registry/… | tar xz`) in the author's publish workflow; `publish.yml` uses `secrets.NPM_TOKEN` in CI. Standard fleet template; not install/runtime behaviour.
- **Obfuscation / data collection:** None. Plain readable TypeScript; no telemetry/analytics, no minified blobs.

## Verdict: CLEAN

Local commit-message hygiene checker. Its only subprocess is a fixed, shell-free `git log` read of the user-supplied repository — exactly its job. No egress, no env/credential access, no install hooks, no writes in shipped source.
