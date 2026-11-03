# Audit — audioport (@reneturcios/audioport)

- **Repo:** github.com/CloudCorpRecords/audioport (MIT)
- **Version:** 0.1.0 (`package.json`, `VERSION` in `src/audioport.ts`, `server.json` 0.1.0)
- **Method:** `git clone` is broken VM-wide (`unable to write symref for HEAD: Operation not permitted`) and codeload tarballs return 0 bytes through the proxy. Primary method used: **`gh api repos/CloudCorpRecords/audioport/contents/<path>` (base64 content, decoded) and `gh api …/git/trees/main?recursive=1` for the file listing**; the transcriber evidence lines (`AUDIOPORT_TRANSCRIBER_COMMAND` at :41/:223, whitespace-split at :230) were re-verified through this route and match. Core `src/audioport.ts` also read in full via supplementary `raw.githubusercontent.com` fetches with identical content/line numbers. `src/audioport/package.json` persisted under `src/` via the file-write tool.
- **Files read:** `package.json`, `README.md`, `Dockerfile`, `server.json`, `src/audioport.ts`, `src/cli.ts`, `src/mcp.ts`, `src/types.ts`, `src/index.ts` (pattern scan + core full read).

## Findings

- **Install scripts:** none in `package.json` (scripts: `build`/`dev`/`test` only). Lockfile `hasInstallScript` only on dev-only `esbuild`/`fsevents`. Runtime deps: `@modelcontextprotocol/sdk ^1`, `zod ^3` only.
- **Network egress:** **none in the package.** No `fetch`/http/net imports, no URLs in code (Dockerfile label aside). Explicitly no hosted transcription service and no API key anywhere.
- **Credential/env access — exactly one key:** `AUDIOPORT_TRANSCRIBER_COMMAND`, read at `src/audioport.ts:41` (constant) and `:223` (`process.env[TRANSCRIBER_COMMAND_ENV]` in `createDefaultTranscriber`). No other env keys; no credential files read.
- **Process execution:**
  - Audio tools: `runExecFile` (`src/audioport.ts:53`) is `execFile(command, args, {timeout: 300000, maxBuffer: 16MB})` — argument arrays, **no shell**. Callers pass the literals `"ffmpeg"`/`"ffprobe"` with fixed flag arrays (metadata probe, convert, trim seek, `loudnorm` normalize).
  - **Transcription (the note):** when `AUDIOPORT_TRANSCRIBER_COMMAND` is set by the operator, its value is whitespace-split (`commandLine.split(/\s+/)`, `src/audioport.ts` in `createDefaultTranscriber`) and run via the same `execFile` with the audio file path appended as the last argument; stdout is the transcript. This is an operator-configured local command executed by design (README documents it, e.g. `whisper-cli --model base`). It is **not** a shell (no shell parsing/injection surface beyond the operator's own configured words; quoting inside the variable is not supported, by construction), it is never set by the package, and when unset `transcribe` fails with an error naming the variable — no fallback, no network substitute.
- **eval / new Function:** none.
- **fs writes:** none by the package itself; ffmpeg writes caller-specified output paths.
- **Telemetry / data collection:** none.
- **Obfuscation:** none.
- **Dockerfile:** two-stage `node:20-alpine`, `npm ci`, `USER node`, no ffmpeg bundled. No curl|sh.

## Verdict: CLEAN-WITH-NOTES

One env key, `AUDIOPORT_TRANSCRIBER_COMMAND`, and it names a **local command the operator chooses** which audioport then runs via arg-array `execFile` (no shell) with the input path appended — justified and documented; adopters should treat setting that variable as granting that command execution, because it is one. Everything else: no egress, no keys, no shell, no install scripts.
