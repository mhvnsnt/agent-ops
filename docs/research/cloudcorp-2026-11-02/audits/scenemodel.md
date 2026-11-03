# Audit — scenemodel (@reneturcios/scenemodel)

- **Repo:** github.com/CloudCorpRecords/scenemodel (MIT)
- **Version:** 0.1.0 (`package.json` `"version":"0.1.0"`, also `VERSION = "0.1.0"` in `src/blender.ts`, `server.json` 0.1.0)
- **Method:** `git clone` is broken VM-wide (`unable to write symref for HEAD: Operation not permitted`) and codeload tarballs return 0 bytes through the proxy. Primary method used: **`gh api repos/CloudCorpRecords/scenemodel/contents/<path>` (base64 content, decoded) and `gh api …/git/trees/main?recursive=1` for the file listing** — slow (~10s/call) but reliable; key evidence lines were re-verified through this route and match. Supplementary reads via `raw.githubusercontent.com` to stdout gave identical content/line numbers. `src/scenemodel/package.json` is persisted under `src/` via the file-write tool; the rest of the tree was audited from the fetched content, not persisted (exec-redirected downloads are zeroed by this VM).
- **Files read in full:** `package.json`, `README.md`, `Dockerfile`, `server.json`, `src/blender.ts`, `src/cli.ts`, `src/mcp.ts`, `src/types.ts`, `src/index.ts`; pattern-scanned: `test/blender.test.ts`, `.github/workflows/*`, `package-lock.json`.
- **Scope:** all source in the repo (5 TS files).

## Findings

- **Install scripts:** none. `package.json` scripts are only `build` (tsc), `dev`, `test`. No `preinstall`/`postinstall`/`prepare`. `package-lock.json` `hasInstallScript` appears only on dev-only `esbuild` 0.28.2 and `fsevents` 2.3.3 (via tsx, `"dev": true`) — standard build tooling, not runtime deps. Runtime deps are only `@modelcontextprotocol/sdk ^1` and `zod ^3`.
- **Network egress — exactly one channel:** `src/blender.ts:31,56` `createConnection({host, port})` from `node:net`, one TCP socket per command, JSON `{type, params}` to the Blender addon. Default `localhost:9876`. That is the documented, expected channel.
  - Host/port are user-configurable via env (below), so the socket *can* point at a non-localhost Blender (the test at `test/blender.test.ts:25` uses `192.168.1.5:9999`). It goes only where the operator's env says.
  - **No HTTP client anywhere:** no `fetch`, no `http/https` imports, no URLs in code except the Dockerfile OCI label. PolyHaven (`get_polyhaven_categories`, `search_polyhaven_assets`, `download_polyhaven_asset`) and Hunyuan3D (`generate_hunyuan3d_model`) are **not** called by this package — the command names are forwarded over the Blender socket and the *Blender addon* performs any PolyHaven/Hunyuan traffic. scenemodel itself holds no PolyHaven/Hunyuan endpoint, key, or egress for them.
- **Credential/env access:** `process.env` read in exactly one place, `src/blender.ts:36-44` (`socketConfigFromEnv`): keys **`BLENDER_HOST`**, **`BLENDER_PORT`** only. No API keys of any kind in the package.
- **Code execution — by design, noted per brief:** `executeBlenderCode` (`src/blender.ts`, `execute_code` command) sends caller-supplied Python over the local Blender socket to be executed inside Blender. This is the tool's documented purpose; the code originates from the local CLI/MCP caller, is not fetched from anywhere, and the transport is the operator-configured Blender socket above.
- **eval / Function / child_process / shell:** none anywhere in `src/`.
- **fs writes:** none. The package never touches the filesystem; even the viewport screenshot is reduced to a summary (format + byte/base64 lengths, `summariseScreenshot`) and image content is explicitly not returned.
- **Telemetry / data collection:** none. The header comment in `src/blender.ts` states upstream blender-mcp's telemetry/user_id tools were deliberately omitted, and no analytics code exists.
- **Obfuscation:** none; small, commented, readable TypeScript.
- **Dockerfile:** two-stage `node:20-alpine`, `npm ci`, runs as `USER node`, entrypoint is the built CLI. No curl|sh, no extra downloads beyond npm ci of the lockfile.

## Verdict: CLEAN-WITH-NOTES

Notes are the design surface itself: (1) one TCP egress channel to `BLENDER_HOST:BLENDER_PORT` (default `localhost:9876`) — justified, documented; (2) env read is only `BLENDER_HOST`/`BLENDER_PORT`; (3) it forwards PolyHaven/Hunyuan3D requests and arbitrary Blender Python to the addon over that socket — any real internet egress or code execution happens inside the user's Blender addon, not in this package. Nothing else found.
