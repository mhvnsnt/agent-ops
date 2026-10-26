# Load time 126s — web-game asset delivery research

**Date:** 2026-10-25 (research pass; sources checked 2026-10-25/26)
**Friction:** play-verify run 18 (2026-10-25, Pantera vs Demonio) — fight goes live **+126s after stage confirm**, 4 missing assets (404s), FREE CAMERA overlaps top-right meter.
**Repo:** mhvnsnt/western-heart, Three.js web game at https://mhvnsnt.github.io/western-heart/ (frozen on Oct 24 build; deploy blocked separately — see below).
**Index:** [[RESEARCH-PULLIN-INDEX]] · prior friction sweep: [[FRICTION-RESEARCH-2026-10-19]] (restic/aria2/zstd/croc decided there — not re-researched).
**Method:** live docs/repos/issues only. Every technical claim below carries its source URL. Nothing from training guesses. No game code touched, no PRs opened — research + doc only, per task.

## What was verified live during this pass (2026-10-26 ~04:09 UTC)

These are measurements of the actual deployed site, not claims from other agents:

- `deploy-manifest.json` on the live site is a **summary only** — `{"format": "wh-pages-deploy/1", "ref": "7badfc7d…", "files": 7181, "bytes": 5647298304}`. **No per-file list, no hashes.** It cannot verify individual assets today; `tools/deploy/build_pages.py` must be extended to emit a per-file manifest before any manifest-based check can work.
- The whole deploy is **5,647,298,304 bytes / 7,181 files** — 5.6 GB, which is why the deploy is blocked against the 1 GB Pages limit (separate issue, but it frames the load problem: the fight is pulling from a very large asset set).
- **HTTP Range requests WORK on GitHub Pages.** Live probe: `curl -r 0-1023` on the site root returned **HTTP 206, `accept-ranges: bytes`, `content-range: bytes 0-375/376`**, via Fastly. Range-based resume/chunked fetch is available on our host — no infrastructure change needed.
- three.js latest is **0.186.1** (npm registry, checked 2026-10-25), MIT.

## 0. The honest starting point: nobody knows where the 126s goes

There is no measurement of the 126 seconds anywhere — no breakdown into network / parse / decode / GPU upload / shader compile. Everything below is a *candidate* fix for an *unmeasured* bottleneck. The single highest-value action is §5 (instrument first). Every compression verdict below is conditional on that measurement: if the 126s is network, KTX2 + caching wins; if it is shader compile on first render, none of the compression work matters and the fix is `renderer.compileAsync` warm-up instead.

---

## 1. KTX2 / Basis Universal textures (KHR_texture_basisu)

### What it actually saves vs embedded PNG/JPEG in a GLB

Two different savings, often conflated:

1. **Download size** — real but uneven. The Khronos glTF-Sample-Models Flight Helmet example, processed with glTF-Transform (PNG → KTX2/BasisU, color = ETC1S, non-color = UASTC): base color 11.41 MB → 1.88 MB (**−83.5%**), normal/ORM maps 17.75 MB → 17.93 MB (**+1.0%** — slightly *larger*), total 43.06 MB → 29.37 MB (**−31.8%**). Source: https://deepwiki.com/KhronosGroup/glTF-Sample-Models/5-advanced-use-cases (quoting `2.0/FlightHelmet/README.md`).
2. **GPU memory + upload time** — the guaranteed win. KTX2 textures stay block-compressed in GPU memory instead of expanding to raw RGBA on upload. A 2048×2048 texture is ~2.6 MB compressed vs ~21 MB uncompressed RGBA (three.js forum measurement, https://discourse.threejs.org/t/estimate-ktx2-texture-memory-size/45793). glTF-Transform's own docs state the same: GPU textures "(1) upload to the GPU much more quickly, and (2) require much less GPU memory. In certain cases they may also have smaller filesizes than PNG or JPEG textures, but this is not guaranteed." Source: https://gltf-transform.dev/modules/extensions/classes/KHRTextureBasisu

### Production pipeline (current, Oct 2026)

- **glTF-Transform 4.5.1** (MIT, Node ≥ 20; registry.npmjs.org/@gltf-transform/cli/latest, checked 2026-10-25). Commands `gltf-transform etc1s in.glb out.glb` / `gltf-transform uastc in.glb out.glb`; shells out to the `ktx` CLI per texture. Already wired in this shop: `tools/procgen/gltf-delivery/` uses glTF-Transform (see [[RESEARCH-PULLIN-INDEX]] — "gltfpack | zeux/meshoptimizer | MIT" and "glTF-Transform | donmccurdy/glTF-Transform | MIT" entries).
- **KTX-Software 4.4.2** — the `ktx` CLI supersedes the old standalone `toktx`/`ktx2ktx2` tools (https://docs.vulkan.org/tutorial/latest/15_GLTF_KTX2_Migration.html). License note: GitHub lists KTX-Software as NOASSERTION (REUSE/SPDX multi-license repo — https://github.com/KhronosGroup/KTX-Software); read `LICENSE.md` before vendoring. **You do not need to install it for the recommended path** — see below.
- **gltfpack `-tc`** is the one-command path and it is *already in the pipeline*: `gltfpack -cc -tc` does meshopt geometry + KTX2/BasisU textures in a single pass (https://npm.io/package/gltfpack; flags also at https://hexmos.com/freedevtools/man-pages/user-commands/file-management/gltfpack/). `-tu` switches to UASTC, `-tqN` sets quality (default 8), `-tsR` scales texture dimensions. This is the same tool that already produced the PR-verified `-cc` meshopt output — adding `-tc` is a flag change, not a new dependency.

### Three.js wiring — confirmed required

`GLTFLoader` does **not** handle KTX2 on its own. You must wire it:

```js
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('path/to/basis/'); // Basis Universal transcoder WASM
ktx2Loader.detectSupport(renderer);
gltfLoader.setKTX2Loader(ktx2Loader);
```

Confirmed by three.js forum (https://discourse.threejs.org/t/how-to-load-a-gltf-that-uses-ktx2-textures-getting-error-setktx2loader-must-be-called-before-loading-ktx2-textures/48792 — the error is literally "`setKTX2Loader` must be called before loading KTX2 textures") and the loader table at https://deepwiki.com/avatarsdk/metaperson-loader-threejs/7.1-asset-loaders (`GLTFLoader.setKTX2Loader()` / `setMeshoptDecoder()` side by side). **KTX2Loader is NOT deprecated** — maintainer-confirmed Nov 2025 (https://discourse.threejs.org/t/has-ktx2loader-been-deprceated/87937). Two wiring traps, both from the forum: (a) use **one shared KTX2Loader instance** — three.js warns "Multiple active KTX2 loaders may cause performance issues" (https://discourse.threejs.org/t/dispose-of-the-ktx-loader-with-r3f-when-asset-is-laoded/74689); (b) never `dispose()` it before the async load finishes. The Basis transcoder WASM ships inside the three.js repo (`examples/jsm/libs/basis/`) — no extra download.

### Quality / transparency gotchas (character textures — this matters for fighters)

- **ETC1S for color, UASTC for data.** Don McCurdy's guide (https://www.donmccurdy.com/2024/02/11/web-texture-formats/): "ETC1S works well on color textures, but not as well on data textures like normal maps"; "UASTC … Quality is sufficient for both color and data textures, including normal maps. UASTC data is larger than ETC1S, but benefits from … Zstandard" — expect UASTC files 1–2× JPEG/ETC1S at the same resolution. Khronos' own deck says the same: "Normal maps often need higher precision and typically use UASTC mode" (https://www.khronos.org/assets/uploads/apis/KTX-2.0-Launch-Overview-Apr21_.pdf).
- **Alpha is preserved only if the material actually uses it.** Forum case (https://discourse.threejs.org/t/how-do-i-make-gltf-transform-uastc-input-glb-output-glb-preserve-alpha-channels-in-my-image-textures/73475): `gltf-transform uastc` appeared to drop alpha — root cause was the Blender export: the image alpha wasn't plugged into the Principled BSDF alpha socket, so the exporter never marked the material transparent. Check with `ktx info` for the `KHR_DF_FLAG_ALPHA_STRAIGHT` flag. Pipeline rule: verify alpha in the source export before blaming the compressor.
- **Non-power-of-two + mipmaps can go dark.** `gltf-transform etc1s` on NPOT textures produced textures that render darker at distance (mipmap selection issue); fix is `--power-of-two` (https://discourse.threejs.org/t/ktx2-compressed-textures-come-out-darker-than-the-originals/51618). Fighter textures should be resized to POT as part of the pass.
- **Transcode cost is real but small** — one DeepWiki-derived estimate puts KTX2 transcoding at ~50 ms per asset-scale load; the forum consensus is it pays for itself in upload time. Measure per fighter (see §5), don't assume.

### Verdict — Q1

**ADOPT — highest-leverage next compression step, conditional on §5 confirming the load is texture/network-bound.** Geometry is already meshopt-compressed (`-cc`); textures are the remaining uncompressed bulk in every fighter GLB. Path: add `-tc` to the existing gltfpack step in the Kaggle-GPU pipeline (no new tool, no KTX-Software install), wire one shared `KTX2Loader` into `game/js/assets.js`, convert per-fighter with ETC1S for base-color and UASTC for normal/ORM, resize to POT, and own-eyes-compare every fighter before/after (alpha + normal-map check per the gotchas above). If §5 shows the 126s is *not* texture-bound, this drops to a background win, not the fix.

---

## 2. Draco vs meshopt — one-paragraph verdict

**SKIP Draco. Do not add it.** Meshopt is already wired (`-cc`, PR-verified 2026-10-16) and it is the faster decoder: the meshoptimizer docs put SIMD decode at **1–3 GB/s** on modern desktops (https://app.unpkg.com/meshoptimizer@0.20.0/files/README.md), the v1 decoder exceeds **5 GB/s** on Apple M4 and the new meshlet decoder reaches **10 GB/s** on one core (https://meshoptimizer.org/v1.html; https://zeux.io/2026/09/30/billions-of-triangles-redux/). Draco's own trade-off is documented the other way: "Draco is slowest per frame loading, it has significant loading latency" (Khronos glTF BOF, SIGGRAPH Asia Dec 2025, https://www.khronos.org/assets/uploads/developers/presentations/glTF_Gaussian_Splats_-_glTF_BOF_SIGGRAPH_Asia_Dec25.pdf), and the independent summary is "Draco for maximal compression; meshopt for fast streaming" (https://novedge.com/blogs/design-news/design-software-history-gltf-and-khronos-architecting-a-runtime-centric-web-native-format-for-portable-3d). Draco would buy a small extra size reduction at the cost of a second decoder, slower decode, and a second extension (`KHR_draco_mesh_compression`) in every file — strictly worse for a load-time problem, where decode speed is the currency. Note for the future: meshoptimizer 1.3.0 is current (Oct 2026) and a new `KHR_meshopt_compression` extension is being finalized (https://meshoptimizer.org/v1.html) — when it lands, the migration is gltfpack-side, not a Draco decision.

---

## 3. Runtime loading patterns for a fighter game

### GLTFLoader has no progressive / partial load

`GLTFLoader.load()` fetches the **entire** file via `FileLoader` and only then calls `parse()` (source walk: https://deepwiki.com/avatarsdk/metaperson-loader-threejs/7.1-asset-loaders — "The loader uses `FileLoader` internally to fetch the binary data, then parses it"). There is no built-in streaming parse, no HTTP Range use, no partial render. Any progressive behaviour has to come from *different assets* (LOD files) or *different code* (custom fetch + parse), not from a loader flag.

### Needle gltf-progressive — the real progressive option

**@needle-tools/gltf-progressive** (MIT, npm `latest` = **4.0.0-alpha.8** as of 2026-10-25 — note the `latest` tag currently points at an alpha; the 3.x line is the stable pin: https://registry.npmjs.org/@needle-tools/gltf-progressive/latest; https://www.npmjs.com/package/@needle-tools/gltf-progressive). One-line plugin:

```js
import { useNeedleProgressive } from '@needle-tools/gltf-progressive';
useNeedleProgressive(gltfLoader, renderer);
```

It streams mesh/texture LODs by on-screen density — Needle's own numbers: a 17.4 MB model shows first pixels after a **715 KB** initial download, full detail streams in behind (https://cloud.needle.tools/articles/needle-cloud-modelviewer, published 2025-06-09, updated 2026-07-03). **Catch:** progressive loading needs assets that *contain* the LOD levels. Needle Cloud generates them (upload → pipeline does up to 6 mesh LODs + progressive textures, Draco for static / meshopt for animated, KTX2/WebP — free tier 30 optimizations). That is a third-party cloud step in the asset pipeline, and the runtime lib alone does nothing for our existing single-LOD GLBs. **Verdict: EVALUATE for stages, not fighters.** A fighter must be full-quality the instant the round starts — LOD streaming buys nothing mid-fight, and the value case (big static stage scenes appearing in <1s) is real but secondary. If adopted, generate LODs for stages only, keep fighters single-file. Do not adopt before §5 proves first-paint latency (not total bytes) is the problem.

### HTTP Range / resumable fetch — available, but GLTFLoader won't use it

Range works on our host (verified live above: HTTP 206). That enables: chunked/resumable `fetch()` with `Range: bytes=` for big GLBs, and ETag-guarded resume. But it requires custom fetch-then-`GLTFLoader.parseAsync(arrayBuffer)` glue — `load()` will never do it. **Verdict: own-glue fallback, not the primary fix.** Worth ~50 lines only if §5 shows network stalls/drops (not steady slow transfer) — a dropped 100 MB fetch restarting from zero is a stall class Range fixes; a steady 126s download is not.

### Preload the next fight during the current one — the cheap, high-value pattern

No library needed. While the player fights, `fetch()` the next likely fighters (or the whole next match-up once both are locked) in the background and put the responses in Cache Storage (or just hold the ArrayBuffers / parsed GLTFs in memory). The ecosystem pattern is: load during idle/attract time, never on the critical path. Concretely for this game: after both fighters lock, the *stage-confirm → fight-live* window is the only load that matters — pre-warming both fighters at *select-screen highlight* (already partially done via `warmFight`) plus background-fetching the stage during character select moves the bytes earlier. **Verdict: ADOPT as own glue (~100 lines, no dependency).** This is the single cheapest cut to perceived load time if the bytes are the problem — it doesn't reduce total bytes, it moves them out of the 126s window.

### Service worker / Cache Storage — makes the 2nd load instant

Standard, well-trodden: a service worker precaches the game shell and caches GLBs on first fetch (cache-first for immutable hashed assets, network-first for the manifest). Two routes:

- **Workbox** (Google, Apache-2.0; v7.2.0 seen in production bundles — https://deepwiki.com/kherrick/x-app/5.4-workbox-runtime): `precacheAndRoute()` for the shell + a `CacheFirst` runtime route for `.glb` with `ExpirationPlugin` caps. Workbox's precache manifest (URL + revision hash) **is also the asset-verification mechanism** for §4 — it fails loudly on hash mismatch. This is the only option where verification comes free with the caching.
- **Hand-rolled SW** (~60 lines, MDN pattern: https://developer.mozilla.org/docs/Web/Progressive_web_apps/App_structure) — install → `cache.addAll()` shell, fetch handler cache-first for GLBs. No dependency, full control.

One host fact that makes this *necessary*, not optional: GitHub Pages serves our files with `cache-control: max-age=600` (observed live in the Range probe headers) — the browser HTTP cache only holds assets 10 minutes. A SW Cache Storage bucket is the durable layer; without it, every session re-downloads everything. **Caveat:** SW scope is the Pages path (`/western-heart/`); registration must live at that scope, and the first visit still pays full download — the win is visits 2+. **Verdict: ADOPT — Workbox preferred** (precache manifest doubles as the §4 verifier; Apache-2.0; the shop already has a Workbox-shaped need). Hand-rolled SW is the fallback if the build step can't produce the precache manifest.

### Retry — GLTFLoader has none built in

`LoadingManager.onError` fires per failed URL and the load just fails. Any retry (exponential backoff, 3 attempts, then named error) is own glue around `loadAsync`. Include it in the §4 verifier module, not as a separate lib.

---

## 4. Killing the 404s — manifest-based verification

### The current manifest can't do this

Verified live: `deploy-manifest.json` is `{format, ref, files: 7181, bytes: 5647298304}` — no per-file entries. **Step zero is extending `tools/deploy/build_pages.py` to emit a per-file manifest** (`path`, `size`, `sha256`) as a deploy artifact. That is a build-script change, not a game change, and it is a precondition for everything below.

### Is there an existing lib?

**No small open-source lib was found for manifest-based game-asset verification.** What exists is adjacent, not applicable:

- **Subresource Integrity (SRI)** covers `<script>` / `<link>` / preload tags only — "not images, fonts, iframes, or `fetch()` calls" (https://inventivehq.com/blog/what-is-subresource-integrity-sri; MDN: https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/SRI). GLBs loaded via `fetch`/`GLTFLoader` cannot use SRI. Skip.
- **Workbox precache manifest** (see §3) is the closest real machinery: URL + revision hash, verified at install, loud failure. If Workbox is adopted, use its manifest as the verifier — do not build a second one.
- Everything else found is framework-specific (Vite/Craft/Nuxt SRI plugins) — not usable in a vanilla-JS game.

### The pattern (own glue, ~100 lines — acceptable, it's wiring)

1. Build emits `asset-manifest.json`: every fight-critical URL + size + sha256.
2. At boot (before the select screen), `fetch(asset-manifest.json)`, then for each entry `fetch(url, {method: 'HEAD'})` — or a ranged `GET bytes=0-0` if HEAD is ever filtered — and compare `content-length` to the manifest; on mismatch/404, record the named asset.
3. If any fight-critical asset is missing: **fail before the fight loads with the asset's name on screen** ("Missing: `fighters/pantera.glb` (404)"), not a silent spinner + retry stall. Non-critical assets (a stage prop) degrade with a named warning instead.
4. Retry each failed fetch 3× with backoff before declaring it missing (transient flakes are real — see [[FRICTION-RESEARCH-2026-10-19]] cluster 1).
5. Optionally verify sha256 of the fetched bytes with `crypto.subtle.digest` for the two fighter GLBs only (full-hash on every asset is overkill; size + 200 is enough for the 404 class).

**Verdict: own-code job, ~100 lines, no lib to pull.** The only dependency is the build-side manifest extension. If Workbox lands first, its precache manifest replaces steps 1–2.

---

## 5. Measuring first — where does the 126s go?

### The standard approach (all citable, all available today)

| Segment | How to measure | Source |
|---|---|---|
| Network per asset | `performance.getEntriesByType('resource')` — `responseEnd - startTime` per URL, plus `transferSize` (0 = served from cache) | https://picostitch.com/blog/2020/11/28-resource-timing-part1/ |
| Fetch progress | `GLTFLoader.load()` `onProgress` (`xhr.loaded / xhr.total`) — already exists in `load-progress.js`; log it with timestamps, don't just render it | three.js `GLTFLoader` API (onProgress callback); LoadingManager pattern at https://www.webcodingcenter.com/three-js/textures-and-asset-loaders--progress-tracking-with-loadingmanager.html |
| Parse + decode | `performance.mark()` / `measure()` around `fetch` → `GLTFLoader.parseAsync` → meshopt/KTX2 decode; log `performance.measure()` deltas | Performance API (`mark`/`measure`) — standard web API |
| Shader compile + first GPU frame | `renderer.compileAsync(scene, camera)` timed, then first `render()`; `renderer.info.render.calls` / `renderer.info.memory` (textures, geometries) for the steady state | three.js `renderer.info` (https://www.utsubo.com/blog/threejs-best-practices-100-tips — "Check your progress with `renderer.info.render.calls`") |
| Frame/GPU during load | **stats-gl 4.2.3** (MIT, https://npm.io/package/stats-gl; https://socket.dev/npm/package/stats-gl) — `new Stats({trackGPU:true}); stats.init(renderer)` — FPS/CPU/GPU panels for WebGL *and* WebGPU | README: "WebGL/WebGPU Performance Monitor with real-time FPS, CPU, and GPU timing" |
| Frame capture (if GPU-side is suspect) | **Spector.js** — Chrome/Firefox extension, records every draw call (https://tympanus.net/codrops/2025/02/11/building-efficient-three-js-scenes-optimize-performance-while-maintaining-quality/) | frame-level, not load-level — use only if §5a points at the GPU |

### Is there a three.js load profiler?

**No dedicated open-source three.js *load* profiler was found.** stats-gl and Spector.js profile *frames*, not *loads*. The load-side methodology that exists as a citable template is a measurement protocol, not a package: a recent independent experiment (Oct 2026) measured exactly the five phases — (1) fetch + read body, (2) parse GLB + decode geometry, (3) `compileAsync`, (4) render + await GPU queue completion, (5) two subsequent frames — with Resource Timing for transfer bytes, run 20×, median reported (https://medium.com/@1228566953qq/three-js-glb-loading-cache-decode-and-the-first-gpu-frame-bead0f5691ab). Their headline: meshopt shrank a 319,648-byte plant GLB to 130,296 bytes (59.2%) and cut fresh-URL first-frame median 35.7 ms → 17.6 ms — i.e. on a small local asset the win is real but small; the 126s case is two orders of magnitude bigger and almost certainly dominated by something else (bytes, stalls, or compile).

### Concrete "measure, then cut" plan

1. Extend the existing `game/js/loadperf.js` (do not build a second profiler): wrap the stage-confirm → fight-live path with `performance.mark()` at **stage-confirm → fetch-start → fetch-end → parse-end → decode-end → compileAsync-end → first-render**, and dump `performance.getEntriesByType('resource')` filtered to the fight's URLs plus `renderer.info` at fight-live.
2. Add a `?loadreport` query param that downloads/prints that JSON — the playtest lane runs it once per fight and pastes the numbers. No new dependency; stats-gl is optional garnish for the frame side only.
3. Decision rule, written down before the numbers exist: if network > 70% → cut bytes (§1 KTX2, §3 preload/cache); if parse/decode > 30% → cut decode work (fewer/lighter textures, check for oversized attributes); if compileAsync/first-render dominates → pre-warm shaders during select screen (`renderer.compileAsync` on the locked fighters while the player is still picking a stage).

**Verdict: ADOPT the own-instrumentation plan; stats-gl ADOPT as a dev-only overlay (MIT, `npm i stats-gl`, `stats.init(renderer)`); no load-profiler lib exists to pull.**

---

## 6. three.js r18x — did anything change GLB loading?

**Short answer: no material change to the GLB load path.** Verified against the primary sources, not roundups:

- Latest is **0.186.1** (npm registry, 2026-10-25; MIT).
- **r186 release notes contain zero KTX2/GLTFLoader entries** — searched the full release page for "KTX2" (no hits): https://github.com/mrdoob/three.js/releases/tag/r186. The r186 changes are WebGPU/TSL/materials (retroreflectivity, SunLight cascaded shadows, `compileAsync` crash fix #34378, PCFSoftShadowMap removal). The one load-adjacent item is the `compileAsync()` crash fix — worth having, not a reason to upgrade alone.
- Migration-relevant changes across r181–r186 (https://www.utsubo.com/blog/webgpu-threejs-migration-guide): r181 deprecates `renderAsync()`/`computeAsync()`; r182 renames `colorBufferType` → `outputBufferType`; r183 renames `PostProcessing` → `RenderPipeline`; r185 changes premultiplied alpha in `WebGPURenderer`; r186 removes `PCFSoftShadowMap` for WebGPU. None touches `GLTFLoader`.
- **WebGPU backend** (stable since r171, zero-config imports since r180) is the big 2026 shift, but it changes the *renderer*, not the *loader*: GLB fetch/parse/decode is identical; the win would be GPU-side (compute, timestamp queries). Migrating the game to `WebGPURenderer` means porting custom shaders to TSL — a project, not a load fix. **Track, don't adopt for this problem.**
- Unverified claims to ignore: AI-content-farm roundups assert "r180 GLTFLoader now supports progressive loading" and "KTX2 BC4/BC5 in r182" — neither appears in the actual release notes. Do not cite them, do not plan on them.

---

## Verdict table

| # | Candidate | License | Verdict | Why (one line) |
|---|---|---|---|---|
| 1a | KTX2/BasisU textures via gltfpack `-tc` (ETC1S color / UASTC normal) | MIT (gltfpack, glTF-Transform) | **ADOPT** (after §5 confirms network/texture-bound) | Textures are the remaining uncompressed bulk; one flag on the existing pipeline; Flight Helmet −31.8% total, −83.5% on color maps |
| 1b | KTX-Software `ktx` CLI install | NOASSERTION on GitHub (REUSE multi-license — read LICENSE.md first) | **SKIP** | Not needed — gltfpack `-tc` bundles its own Basis encoder; glTF-Transform path only if the Kaggle pipeline wants it |
| 1c | `KTX2Loader` wiring in `game/js/assets.js` | MIT (three.js) | **ADOPT** with 1a | Required for KHR_texture_basisu; one shared instance, transcoder path from three.js repo |
| 2 | Add Draco (`KHR_draco_mesh_compression`) | Apache-2.0 / BSD (draco) | **SKIP** | Meshopt already wired and decodes faster (1–3 GB/s SIMD, up to 10 GB/s meshlet); Draco is the slowest loader per Khronos' own deck |
| 3a | @needle-tools/gltf-progressive | MIT (lib); asset generation is a Needle Cloud service (free tier 30 opts) | **EVALUATE for stages only** | 17.4 MB → 715 KB first paint is real, but needs LOD-processed assets and buys nothing for fighters that must be full-quality at round start |
| 3b | HTTP Range / resumable fetch | — (own glue, web standard) | **ADOPT as fallback glue** | Verified working on GitHub Pages (live 206); only pays if §5 shows drops/stalls, not steady slowness |
| 3c | Preload next fight during current fight | — (own glue) | **ADOPT** | Cheapest cut to perceived load: moves bytes out of the 126s window; no dependency |
| 3d | Service worker + Cache Storage (Workbox preferred) | Apache-2.0 (Workbox) | **ADOPT** | Pages HTTP cache is only 10 min (`max-age=600` observed); SW cache is the durable layer; Workbox precache manifest doubles as the §4 verifier |
| 3e | Hand-rolled SW (~60 lines) | — (own glue) | Fallback to 3d | Use only if Workbox's build step can't produce the precache manifest |
| 4 | Manifest-based 404 verification | — (own glue ~100 lines; no lib exists) | **ADOPT** (own code) | Current manifest is summary-only — extend `build_pages.py` first; SRI doesn't apply to fetch/GLB; fail with the asset's name, not a silent stall |
| 5a | Own load instrumentation in `loadperf.js` (marks around fetch/parse/decode/compile/first-render + Resource Timing + `?loadreport`) | — (own glue) | **ADOPT FIRST** | No three.js load profiler exists; this is the precondition for every other item |
| 5b | stats-gl (dev overlay) | MIT | **ADOPT** (dev-only) | FPS/CPU/GPU panels for WebGL+WebGPU; frame-side only, complements 5a |
| 5c | Spector.js | (browser extension) | **HOLD** | Frame capture; use only if 5a points at the GPU |
| 6 | three.js upgrade / WebGPU migration for load speed | MIT | **SKIP for this problem** | r186 has no GLB-load-path change; WebGPU changes the renderer, not the loader |

## Recommended sequence (measure first, then cut in order)

1. **Measure (one playtest run, no code risk).** Extend `game/js/loadperf.js` with the §5 marks + `?loadreport` dump; run Pantera vs Demonio once; paste the phase breakdown. This decides everything below. *Owner of the numbers: the play-verify lane.*
2. **Kill the 404s (parallel with 1, build-side).** Extend `tools/deploy/build_pages.py` to emit per-file `asset-manifest.json` (path + size + sha256); add the ~100-line boot verifier (HEAD + size check, named failure, 3× retry). The 4 missing assets from run 18 get named, not silently retried.
3. **If network-bound: cut bytes + move them earlier.** (a) gltfpack `-tc` KTX2 pass on fighter + stage GLBs in the Kaggle pipeline, ETC1S color / UASTC normal, POT resize, own-eyes compare per fighter; (b) wire the shared `KTX2Loader`; (c) preload next fight during the current fight; (d) Workbox SW + Cache Storage so the second load is instant.
4. **If decode/parse-bound:** audit the two fighter GLBs for oversized attributes/textures (the per-file manifest from step 2 gives sizes; the §5 marks give the split) before reaching for new codecs — Draco is already ruled out.
5. **If compile/first-render-bound:** pre-warm with `renderer.compileAsync` on locked fighters during stage select; revisit after the numbers.
6. **Later / tracked:** Needle progressive for stage scenes (evaluate after 1–3 land); three.js WebGPU migration (tracked, not a load fix); `KHR_meshopt_compression` finalization (gltfpack-side when it lands).

## Blocked / open questions

- **The 126s is unmeasured.** Nothing above is proven to fix it until §5 runs. Do not start the KTX2 re-encode of all fighters before the measurement — it is the most expensive step and the wrong one if the bottleneck is compile.
- **Deploy is 5.6 GB / 7,181 files vs the 1 GB Pages limit** (live manifest, 2026-10-26). Load-time work targets the frozen Oct 24 build; the deploy-size problem is separate and may change which assets are even reachable.
- **The 4 missing assets from run 18 ARE named — correction (2026-10-25, parent pass):** the original "unnamed" claim in this doc was wrong. Play-verify run 18's HTTP log (`~/workspace/_playverify-20261025/http8123.log`) + memory name all four: `roster/demonio/anatomy/anatomy-layers.json`, `game-src/js/intro-interactions.js`, `customization/parts/no-mercy/glb/body_parts/model_1171.glb`, `customization/eye-library/eye-classic-original.png`. Note `game-src/js/intro-interactions.js` looks like a wrong-path bug (`game-src/` vs `game/js/`) — a game-lane fix, not a loader fix. The §4 verifier is still worth building: it names missing assets at runtime in production, where there is no play-verify log to read.
- **KTX-Software license** is NOASSERTION on GitHub — irrelevant if the gltfpack `-tc` path is used (recommended), but any lane that installs the `ktx` CLI must read `LICENSE.md` first.
- **Needle Cloud** asset generation is a third-party service step (free tier: 30 optimizations) — needs an owner call before any fighter GLB is uploaded to it; stages-only evaluation avoids the question for now.
- **FREE CAMERA overlapping the top-right meter** is a UI bug from run 18, not a load problem — out of scope here, noted for the game lane.

## Sources (every technical claim above)

- three.js latest 0.186.1, MIT — https://registry.npmjs.org/three/latest
- three.js r186 release notes (no KTX2/GLTFLoader entries) — https://github.com/mrdoob/three.js/releases/tag/r186
- three.js migration guide r181–r186 — https://www.utsubo.com/blog/webgpu-threejs-migration-guide
- glTF-Transform `KHR_texture_basisu` docs — https://gltf-transform.dev/modules/extensions/classes/KHRTextureBasisu
- glTF-Transform CLI 4.5.1, MIT, Node ≥ 20 — https://registry.npmjs.org/@gltf-transform/cli/latest
- KTX2 / BasisU migration + `ktx` CLI supersedes `toktx` — https://docs.vulkan.org/tutorial/latest/15_GLTF_KTX2_Migration.html
- KTX-Software repo (license NOASSERTION, REUSE) — https://github.com/KhronosGroup/KTX-Software
- KTX-Software 4.4.2 release notes — https://sourceforge.net/projects/khronos-ktx.mirror/files/v4.4.2/
- Flight Helmet KTX2 sizes (−83.5% color, +1% normal, −31.8% total) — https://deepwiki.com/KhronosGroup/glTF-Sample-Models/5-advanced-use-cases
- Khronos KTX 2.0 launch (ETC1S/UASTC guidance) — https://www.khronos.org/assets/uploads/apis/KTX-2.0-Launch-Overview-Apr21_.pdf and https://www.khronos.org/news/press/khronos-ktx-2-0-textures-enable-compact-visually-rich-gltf-3d-assets
- Texture format guide (ETC1S color / UASTC normal, 1–2× sizes) — https://www.donmccurdy.com/2024/02/11/web-texture-formats/
- KTX2 GPU memory (2048² ≈ 2.6 MB vs 21 MB RGBA) — https://discourse.threejs.org/t/estimate-ktx2-texture-memory-size/45793
- `setKTX2Loader` required + error text — https://discourse.threejs.org/t/how-to-load-a-gltf-that-uses-ktx2-textures-getting-error-setktx2loader-must-be-called-before-loading-ktx2-textures/48792
- KTX2Loader not deprecated (Nov 2025) — https://discourse.threejs.org/t/has-ktx2loader-been-deprceated/87937
- Single shared KTX2Loader warning — https://discourse.threejs.org/t/dispose-of-the-ktx-loader-with-r3f-when-asset-is-laoded/74689
- Alpha preservation (Blender export root cause) — https://discourse.threejs.org/t/how-do-i-make-gltf-transform-uastc-input-glb-output-glb-preserve-alpha-channels-in-my-image-textures/73475
- NPOT/mipmap dark-texture fix (`--power-of-two`) — https://discourse.threejs.org/t/ktx2-compressed-textures-come-out-darker-than-the-originals/51618
- gltfpack flags (`-cc`, `-tc`, `-tu`, `-tq`, `-ts`) — https://npm.io/package/gltfpack and https://hexmos.com/freedevtools/man-pages/user-commands/file-management/gltfpack/
- GLTFLoader internals (FileLoader → parse, no streaming) — https://deepwiki.com/avatarsdk/metaperson-loader-threejs/7.1-asset-loaders
- Draco slowest per-frame loading — https://www.khronos.org/assets/uploads/developers/presentations/glTF_Gaussian_Splats_-_glTF_BOF_SIGGRAPH_Asia_Dec25.pdf
- Draco vs meshopt summary — https://novedge.com/blogs/design-news/design-software-history-gltf-and-khronos-architecting-a-runtime-centric-web-native-format-for-portable-3d
- meshopt decode 1–3 GB/s SIMD — https://app.unpkg.com/meshoptimizer@0.20.0/files/README.md
- meshopt v1 decoder >5 GB/s, meshlet 10 GB/s; KHR_meshopt_compression in progress — https://meshoptimizer.org/v1.html and https://zeux.io/2026/09/30/billions-of-triangles-redux/
- Needle gltf-progressive (17.4 MB → 715 KB first paint) — https://cloud.needle.tools/articles/needle-cloud-modelviewer
- @needle-tools/gltf-progressive 4.0.0-alpha.8, MIT — https://registry.npmjs.org/@needle-tools/gltf-progressive/latest and https://www.npmjs.com/package/@needle-tools/gltf-progressive
- Workbox runtime/precaching (v7.2.0 in the wild) — https://deepwiki.com/kherrick/x-app/5.4-workbox-runtime
- Service worker pattern (MDN) — https://developer.mozilla.org/docs/Web/Progressive_web_apps/App_structure
- SRI scope (script/link only, not fetch) — https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/SRI and https://inventivehq.com/blog/what-is-subresource-integrity-sri
- Resource Timing API — https://picostitch.com/blog/2020/11/28-resource-timing-part1/
- LoadingManager progress pattern — https://www.webcodingcenter.com/three-js/textures-and-asset-loaders--progress-tracking-with-loadingmanager.html
- renderer.info / profiling tools — https://www.utsubo.com/blog/threejs-best-practices-100-tips
- stats-gl 4.2.3, MIT — https://npm.io/package/stats-gl and https://socket.dev/npm/package/stats-gl
- Spector.js — https://tympanus.net/codrops/2025/02/11/building-efficient-three-js-scenes-optimize-performance-while-maintaining-quality/
- Load-phase measurement protocol (fetch → parse → compileAsync → first frame, 20 runs) — https://medium.com/@1228566953qq/three-js-glb-loading-cache-decode-and-the-first-gpu-frame-bead0f5691ab
- Live probes by this pass (2026-10-26 ~04:09 UTC): `deploy-manifest.json` summary-only (7,181 files / 5,647,298,304 bytes); `curl -r 0-1023` → HTTP 206, `accept-ranges: bytes`; Pages `cache-control: max-age=600`.
