# Security Audit — muse-marketplace

- **Repo:** github.com/CloudCorpRecords/muse-marketplace (MIT)
- **Version:** 0.1.0 (`package.json`)
- **npm:** `@reneturcios/muse-marketplace` · **Bins:** `muse-marketplace` and `mmkt` → `dist/cli.js`
- **Dependencies:** runtime `@modelcontextprotocol/sdk ^1`, `zod ^3`; dev `@types/node ^20`, `tsx ^4`, `typescript ^5`
- **Method used:** `git clone` is broken VM-wide (“unable to write symref for HEAD: Operation not permitted”) and codeload tarballs return 0 bytes through the proxy, and tar extraction into the scratch tree hit write-EPERM — so no local `src/` copy could be persisted. Primary method per coordinator: `gh api repos/CloudCorpRecords/muse-marketplace/git/trees/main?recursive=1` for the file inventory and `gh api repos/CloudCorpRecords/muse-marketplace/contents/<path>` (base64 content) for source, cross-checked with streamed `raw.githubusercontent.com` reads: full-file reads of `package.json`, `src/cli.ts`, `src/registry.ts` (all but the scaffold tail), and `grep -n` scans of the remaining files listed under Coverage. Nothing was installed or run.
- **Coverage:** All executable source covered — `package.json`, every file in `src/` (`cli.ts`, `index.ts`, `mcp.ts`, `registry.ts`, `types.ts`), plus `test/*.ts`, `site/app.js`, `site/index.html`, `Dockerfile`, `server.json`, workflows. The `registry/**` asset tree (SVG assets, `listing.json`/`bundle.json`/`index.json`, persona markdown) and `docs/` were covered by full tree inventory + type/size review, not by downloading every asset file — none of them are executable formats, and the registry code rejects executable extensions at validate/install time (see Findings).

## Findings

- **Install hooks:** Scripts are `build`, `dev`, `test` only. **No** `preinstall` / `postinstall` / `prepare`.
- **Network egress: none.** Grep across all of `src/` finds no `fetch`, no `http/https/net/tls`, no WebSocket, no `child_process`, no `eval` / `new Function`. The MCP mode is stdio-only. Despite the “marketplace” name, **installing a listing downloads nothing** (see below).
- **Env access: exactly one variable.** `src/registry.ts:32` — `process.env.MUSE_MARKETPLACE_REGISTRY`, a path override for where the registry directory lives (also settable via `--root`). No other `process.env` in `src/`; no credential stores, tokens, `~/.ssh` / `~/.aws` / Keychain access.
- **What “install” actually does — verified local copy with strong vetting** (`src/registry.ts` `installListing()`):
  - The registry is the **bundled local `registry/` tree** (or the `MUSE_MARKETPLACE_REGISTRY` / `--root` directory). Install is `copyFileSync` from that local tree to a caller-provided destination (CLI default `./muse-assets`, `--dest` to override); the destination is checked to stay under the provided base dir.
  - Before copying, the listing must pass `validateListing()`: every file's **byte size and sha256 must match `listing.json`**, media types must be on an allowlist (`image/*`, `text/markdown`, `text/plain`, `application/json`, `audio/*`), and a **blocked-extensions denylist rejects executables and code** (`.exe .dll .so .sh .bat .ps1 .js .mjs .ts .py .rb .php .jar .msi .bin .run`, …). Path-traversal paths (`..`, absolute, drive-letter) are rejected and each file must resolve inside its listing dir.
  - sha256 is re-verified **after** the copy, and an `install-receipt.json` is written into the destination. Invalid/tampered listings are refused.
  - Consistent with that, the bundled registry content is inert: SVG avatar assets, `listing.json` / `bundle.json` / `index.json`, and markdown personas — no executable assets in the tree (per the `gh api` inventory).
- **Other filesystem writes:** rebuilding `registry/index.json` (`index` command, `src/registry.ts` writeIndex), and `init` scaffolding a new listing (placeholder SVG + `listing.json`) inside the registry dir. Nothing outside the registry dir / install dest.
- **Static site:** `site/app.js:111` `fetch("data.json")` — a same-directory relative fetch of the bundled catalog data for the preview site; `innerHTML` rendering there uses that bundled local data only.
- **Metadata / CI:** `server.json` carries `static.modelcontextprotocol.io` (schema), `registry.npmjs.org` (registryBaseUrl), `ghcr.io/cloudcorprecords/muse-marketplace:0.1.0` and `github.com` manifest strings — never fetched by the tool. Dockerfile is the standard `node:20-alpine` build. Workflows are the fleet template (`registry-publish.yml` CI-only `curl` of mcp-publisher v1.8.1; `publish.yml` uses `secrets.NPM_TOKEN` in CI).
- **Obfuscation / data collection:** None. Plain readable TypeScript; no telemetry/analytics.

## Verdict: CLEAN-WITH-NOTES

The single note: it reads one environment variable, **`MUSE_MARKETPLACE_REGISTRY`** (`src/registry.ts:32`), solely as a registry-path override. Everything else is negative in the best way: **zero network egress, zero subprocesses, zero credential access**, and its install path is a checksum-verified, extension-denylisted **local copy** of inert media/markdown assets — it cannot fetch or install remote code.
