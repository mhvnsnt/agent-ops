# Audit — videokit (@reneturcios/videokit)

- **Repo:** github.com/CloudCorpRecords/videokit (MIT)
- **Version:** 0.1.0 (`package.json`, `VERSION` in `src/video.ts`, `server.json` 0.1.0; repo last pushed 2026-10-30)
- **Method:** `git clone` is broken VM-wide (`unable to write symref for HEAD: Operation not permitted`) and codeload tarballs return 0 bytes through the proxy. Primary method used: **`gh api repos/CloudCorpRecords/videokit/contents/<path>` (base64 content, decoded) and `gh api …/git/trees/main?recursive=1` for the file listing**; key evidence lines (e.g. the `execFile` executor) were re-verified through this route and match. Supplementary reads via `raw.githubusercontent.com` to stdout gave identical content/line numbers. `src/videokit/package.json` persisted under `src/` via the file-write tool.
- **Files read:** `package.json`, `README.md`, `Dockerfile`, `server.json`, `src/video.ts` (full core), `src/cli.ts`, `src/mcp.ts`, `src/types.ts`, `src/index.ts` (pattern scan + spot reads); `test/video.test.ts`, `package-lock.json` pattern-scanned.

## Findings

- **Install scripts:** none in `package.json` (scripts: `build`/`dev`/`test` only). Lockfile `hasInstallScript` only on dev-only `esbuild`/`fsevents` (via tsx). Runtime deps: `@modelcontextprotocol/sdk ^1`, `zod ^3` only.
- **Network egress:** **none.** No `fetch`, no http/net imports, no URLs in code (only the Dockerfile OCI source label). No sockets at all.
- **Credential/env access:** **none.** `process.env` does not appear in `src/` at all.
- **Process execution — its job, done safely:** `src/video.ts:14,22` — the only executor is `execFile(binary, args, {timeout: 120000, maxBuffer: 16MB})` from `node:child_process`, where `binary` is the literal union `"ffmpeg" | "ffprobe"` and `args` is a constructed string array (probe: `-v quiet -print_format json -show_format -show_streams <file>`; thumbnail/trim/resize/transcode/frames/audio likewise fixed flag arrays with user values as single array elements). **No `shell` option, no string interpolation into a command line, no `exec`/`spawn` string form, no remote code.** Missing binaries surface as honest ENOENT tool errors.
- **eval / new Function:** none.
- **fs writes:** the package itself performs no fs operations; output files are written by ffmpeg to the caller-specified output paths (that is the tool's function).
- **Telemetry / data collection:** none.
- **Obfuscation:** none.
- **Dockerfile:** two-stage `node:20-alpine`, `npm ci`, `USER node`; bundles no ffmpeg (host binaries used). No curl|sh.

## Verdict: CLEAN

No egress, no env/credential access, no shell, no install scripts. The only execution surface is arg-array `execFile` of the host's `ffmpeg`/`ffprobe`, which is the package's stated job.
