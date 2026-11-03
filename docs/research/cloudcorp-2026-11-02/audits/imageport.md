# Audit — imageport (@reneturcios/imageport)

- **Repo:** github.com/CloudCorpRecords/imageport (MIT)
- **Version:** 0.1.0 (`package.json`, `VERSION` in `src/imageport.ts`, `server.json` 0.1.0)
- **Method:** `git clone` is broken VM-wide (`unable to write symref for HEAD: Operation not permitted`) and codeload tarballs return 0 bytes through the proxy. Primary method used: **`gh api repos/CloudCorpRecords/imageport/contents/<path>` (base64 content, decoded) and `gh api …/git/trees/main?recursive=1` for the file listing**; the executor evidence lines were re-verified through this route and match. Core `src/imageport.ts` also read in full via supplementary `raw.githubusercontent.com` fetches with identical content/line numbers. `src/imageport/package.json` persisted under `src/` via the file-write tool.
- **Files read:** `package.json`, `README.md`, `Dockerfile`, `server.json`, `src/imageport.ts`, `src/cli.ts`, `src/mcp.ts`, `src/types.ts`, `src/index.ts`.

## Findings

- **Install scripts:** none in `package.json` (scripts: `build`/`dev`/`test` only). Lockfile `hasInstallScript` only on dev-only `esbuild`/`fsevents`. Runtime deps: `@modelcontextprotocol/sdk ^1`, `zod ^3` only.
- **Network egress:** **none.** No `fetch`/http/net imports, no URLs in code (Dockerfile label aside). README's "no network call anywhere in this package" is accurate against the source.
- **Credential/env access:** **none.** `process.env` does not appear in `src/`.
- **Process execution — its job, done safely:** `src/imageport.ts:15,42` — one default executor, `execFile(command, args, {timeout: 120000, maxBuffer: 16MB})`, argument arrays, **no shell**. All call sites use the literals `"identify"` / `"convert"` with fixed arrays:
  - metadata: `identify -format "%m|%w|%h|%[colorspace]|%b" <input>` (`:68`)
  - resize: `convert <input> -resize <geometry> <output>` (`:105`)
  - convert: `convert <input> <effectiveOutput>` (`:134`)
  - crop: `convert <input> -crop <WxH+X+Y> +repage <output>` (`:152`)
  - rotate: `convert <input> -rotate <angle> <output>` (`:164`)
  User values enter as single array elements / validated numbers formatted into the geometry string — there is no command-line string for a shell to reinterpret, and no ImageMagick policy/script execution is invoked. Missing binaries surface as honest ENOENT errors.
- **eval / new Function:** none.
- **fs writes:** none by the package itself; ImageMagick writes caller-specified output paths.
- **Telemetry / data collection:** none.
- **Obfuscation:** none.
- **Dockerfile:** two-stage `node:20-alpine`, `npm ci`, `USER node`; bundles no ImageMagick. No curl|sh.

## Verdict: CLEAN

No egress, no env/credential access, no shell, no install scripts. The only execution surface is arg-array `execFile` of the host's ImageMagick `convert`/`identify`, which is the package's stated job.
