# Cape Jones → Wizard Gang Transfer Inventory — mhvnsnt/cape-jones @ main

**Generated:** 2026-11-02 (research subagent, gh CLI authenticated as `mhvnsnt`)
**Repo:** `mhvnsnt/cape-jones` — "Cape Jones show repo (Space Ghost -> CAPE JONES, proprietary rename)"
**Main HEAD verified:** `ccef6cb4e3d65e6125a078d88472829b6fd6ce4d` — 2026-11-02T03:34:39Z — "Push-everything: landing prep, Nick verify, dialogue pass, Rick and Morty rig sheets (#358)"
**Repo size (GitHub `diskUsage`):** 6,338,354 KB (~6.5 GB compressed). Blob bytes in the tree payload alone: ~7.49 GB uncompressed.
**Raw tree saved:** `~/workspace/agent-ops/cjwg-cape-tree.json` (15 MB)

## ⚠️ Coverage caveat — read first

`GET repos/mhvnsnt/cape-jones/git/trees/main?recursive=1` returned **`"truncated": true` with 53,436 entries** (49,199 blobs + 4,237 trees). The payload ends mid-path inside `production/tools/fmodel/FModel/Views/Resources/Converters/…`. Everything alphabetically **before** that point is enumerated exactly below (path + byte size, copied from the API). Everything after it was verified a second way — GitHub **Contents API** listings (root, `production/tools/`, `tools/`, `shared/`, `stages/`, `proof/`, `notebooks/`, and the Nov-1 batch folders) plus targeted subtree tree calls (e.g. `production/tools/rife`). For those later areas the **directory and its top-level/sample contents are exact**, but a full recursive file-by-file enumeration does **not** exist in this inventory — do not treat §11/§12 as exhaustive per-file lists.

## Transfer rule applied (FREE-GAME RULE, as briefed)

- **YES** — craft, tools, code, flows, techniques, templates, rig *systems*, timing/structure, presets, pipelines, wiring docs. Transfer, rename/re-skin for Wizard Gang.
- **NO** — Cape Jones characters, names, logos, verbatim script/dialogue, Cape Jones art/story, episode outputs, character sheets, voice/audio of characters. Also **NO** for third-party donor-show character art/names (Gumball / Foster's / Smiling Friends / Scooby-Doo / Rick and Morty / Space Ghost etc.) — only their *timing, layer structure, rig construction and movement technique* are YES.
- **MIXED** — file/folder contains a transferable system wrapped around CJ/donor art or CJ naming. Transfer the system, scrub the name, leave/replace the art.
- Wizard Gang already has its own base layer (Pipeline One: Chatterbox voices, Viggle body replacement, Muse video base, pan-and-zoom parallax). Items below are additive to that, not replacements for it.

---

## 1. Nov 1–2 landing wave — PRs #337–#358 (all MERGED, verified via `gh pr list`)

| PR | Merged (UTC) | Title (verbatim) |
|---|---|---|
| #337 | 2026-11-01T20:15:58Z | Land movement dance presets, clean A/B/C + arm-snap-fixed A/C (20261101) |
| #338 | 2026-11-01T20:26:46Z | Batch D1: side rig auto + wrist fix + FLA choose side/back + v4 cape fix + top5 fixed Blender render (2026-11-01) |
| #339 | 2026-11-01T20:32:16Z | Batch D2: wire-up-cannot-do Toon Boom export + fast clips (2026-11-01) |
| #340 | 2026-11-01T20:35:49Z | Batch D3: dance test + movement library clips (2026-11-01) |
| #341 | 2026-11-01T20:40:26Z | Batch D4a: dance scene Videos 1-2 (EN/JP FINAL) (2026-11-01) |
| #342 | 2026-11-01T20:43:14Z | Batch D4b: dance flash fix Videos 3-4 fixed pair, faststart (2026-11-01) |
| #343 | 2026-11-01T20:47:34Z | Batch D5: Nosferatu Video 5 + anatomy fix bundle (2026-11-01) |
| #344 | 2026-11-01T20:50:27Z | Batch D6: Blender 5.2.3 rig fixed + arm-snap last-3 fix + refined rig with Grease Pencil overlay (2026-11-01) |
| #345 | 2026-11-01T20:52:21Z | Batch D7: donor FLA rig pull — listings/structure summaries ONLY (2026-11-01) |
| #346 | 2026-11-01T20:55:11Z | Batch D8: Universal knee-feet rule update — 2026-11-01 12:07 CST supersedes 11:30 leg1/leg2 version (learning gate rules.json) |
| #347 | 2026-11-01T20:55:32Z | Batch D9: Mars making money / good experience rule doc (2026-11-01) |
| #348 | 2026-11-01T22:39:50Z | Batch E1: snap-sooner lock study + snap-early motion + refer-back index |
| #349 | 2026-11-01T22:48:28Z | Batch E2: CJ-01 to CJ-10 clean, layer removal only |
| #350 | 2026-11-01T22:57:54Z | Batch E3: true head turn, true forward kick, snapped preset B |
| #351 | 2026-11-01T23:10:15Z | Batch E4: side rig next steps, belt/palm trials |
| #352 | 2026-11-01T23:16:37Z | Batch E5: GIF previews, 12-principles checks, beat-sync prep, unknown-archive listing |
| #353 | 2026-11-01T23:55:07Z | Beat-sync presets: A chosen, B and C saved as alternates (2026-11-01) |
| #354 | 2026-11-02T00:05:31Z | Finish5 F1: clean episode CJ-01 to CJ-30 (MP4 + chat MP4 + audio + dialogue blanks + report) |
| #355 | 2026-11-02T00:06:49Z | Finish5 F2: Cape Jones + Charlie placeholder interaction (MP4/GIF/contact/SFX/report/list/builders) |
| #356 | 2026-11-02T03:18:53Z | Push-everything: Charlie v3 + v3.1, kick master, spinning bust final |
| #357 | 2026-11-02T03:29:25Z | Push-everything: elbow 90deg + native sole boot + angle sheets 2-4 |
| #358 | 2026-11-02T03:34:39Z | Push-everything: landing prep, Nick verify, dialogue pass, Rick and Morty rig sheets |

Also in the same window, just before #337: #330 monetization+conversation systems, #332 side-rig anatomy fix + 5 gate tools, #333 top5 Blender rig / side+back packs, #335/#336 Toon Boom Linux + arm snap + head turn.

**Top-level layout of main (Contents API, exact):** code/pipeline under `production/`, a 17k-entry character-rig tree under `cape-jones-rig/`, 3D under `3d-assets/`, a second tool tree at root `tools/` (24 subdirs), `docs/` (222 entries in payload), `anims/`, `characters/`, `stages/` (`stages/cape-house`, `stages/jungle-outpost`), `shared/cast`, `proof/`, `notebooks/colab`, plus ~45 dated Nov-1 batch folders at root (each = builder script + report + proof media + output). That dated-batch pattern is itself a transferable working method: every batch is self-documenting and re-runnable.

---

## 2. `production/pipeline/` — the core transferable pipeline (84 entries, all exact)

This is the single highest-value folder for Wizard Gang. All are small code/docs (312 B – 33,089 B). **Verdict for the folder: YES**, except files whose *content* is Cape Jones episode/character-specific (flagged MIXED/NO per row).

### 2.1 Pipeline maps & wiring docs
| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/pipeline/ANIMATION-PIPELINE-2026.md` | 5,711 | Master 2D stage map: Draw Tahoma2D → Rig/Tween Synfig → Interpolate RIFE (Kaggle GPU) → Composite OpenToonz → Finish (FLIPACLIP post) → Blender VSE/ffmpeg assembly. Written 2026-10-19 explicitly "prove it on Cape Jones, then use it for the other shows" | **YES** |
| `production/pipeline/FLIPACLIP-POST-PIPELINE.md` | 5,691 | See §6.1 | **YES** |
| `production/pipeline/LED-SCENE-ASSEMBLER.md` | 3,458 | Doc for the LED/lighting scene assembler below | **YES** (technique) |
| `production/pipeline/trackA-wiring-guide.md` | 6,243 | Track-A ffmpeg FX wiring guide | **YES** |
| `production/pipeline/kaggle_commit_guide.md` | 1,580 | How Kaggle notebook outputs get committed back to repo | **YES** |
| `production/pipeline/example_manifest.json` | 312 | Example shot manifest schema | **YES** |

### 2.2 Shot assembly, render & interpolation
| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/pipeline/cape_jones_pipeline.sh` | 7,142 | Top-level episode pipeline driver shell script | **MIXED** — flow YES, CJ name/paths scrub |
| `production/pipeline/scene_assembler.py` | 6,446 | Assembles scenes from parts | **YES** |
| `production/pipeline/led_scene_assembler.py` | 13,873 | Assembles LED-lit scenes (pairs with `led_controller.py`) | **YES** |
| `production/pipeline/led_controller.py` | 13,650 | LED colour/level controller for scene lighting | **YES** |
| `production/pipeline/ep1_render.py` | 9,469 | Episode render driver | **MIXED** — EP1-specific settings |
| `production/pipeline/ep1_render_chunk.sh` | 1,807 | Chunked render wrapper | **YES** |
| `production/pipeline/render_half_interp.py` | 5,205 | Half-rate render + interpolation finish | **YES** |
| `production/pipeline/scene_aware_interp.py` | 7,392 | Scene-cut-aware frame interpolation (doesn't blend across cuts) | **YES** |
| `production/pipeline/ldf_vfi_wrapper.py` | 2,909 | Wrapper for LDF-VFI frame interpolation (`production/tools/LDF-VFI/`) | **YES** |
| `production/pipeline/cycles_speed_config.py` | 5,059 | Blender Cycles speed settings | **YES** |
| `production/pipeline/render_looks.py` | 3,076 | Applies render looks/grades | **YES** |
| `production/pipeline/grades.py` | 16,910 | Colour grade library/presets in code | **YES** |
| `production/pipeline/comp_glow.py` | 5,146 | Compositing glow pass | **YES** |
| `production/pipeline/finish.py` | 5,585 | Final finish pass (grades → cards → export chain) | **YES** |
| `production/pipeline/proxy_gen.py` | 4,819 | Proxy media generation | **YES** |
| `production/pipeline/upscale_span.py` | 5,153 | Upscaling spans of footage | **YES** |
| `production/pipeline/batch_process.sh` | 2,336 | Batch processing driver | **YES** |
| `production/pipeline/flamenco-manager.ep1.yaml` | 2,471 | Flamenco render-farm manager config | **MIXED** — template YES, EP1 values no |
| `production/pipeline/compute/cj-render.py` | 9,903 | Cloud/GPU render entry point | **MIXED** — rename, flow YES |
| `production/pipeline/compute/COMPUTE-README.md` | 2,158 | Compute routing overview | **YES** |
| `production/pipeline/compute/flamenco-setup.md` | 3,169 | Flamenco setup | **YES** |
| `production/pipeline/compute/kaggle-ops.md` | 1,866 | Kaggle ops notes | **YES** |
| `production/pipeline/compute/lightning-ai-setup.md` | 2,323 | Lightning AI setup | **YES** |
| `production/pipeline/compute/sheepit-setup.md` | 2,815 | SheepIt render-farm setup | **YES** |

### 2.3 FX, type & image tools
| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/pipeline/anime_fx.py` | 7,180 | Anime-style FX generation | **YES** |
| `production/pipeline/energy_blast.py` | 10,251 | Energy-blast VFX (CJ "blaster" gag is CJ-specific; blast technique generic) | **MIXED** |
| `production/pipeline/fx-particles.py` | 5,728 | Particle FX | **YES** |
| `production/pipeline/cartoon-fx.sh` | 1,924 | Cartoon FX ffmpeg chain | **YES** |
| `production/pipeline/ffmpeg-animation-filters.sh` | 3,749 | ffmpeg animation filter chains | **YES** |
| `production/pipeline/trackA-ffmpeg-fx-chains.sh` | 3,139 | Track-A FX chains | **YES** |
| `production/pipeline/retro_fx.py` | 3,103 | Retro/VHS FX | **YES** |
| `production/pipeline/kinetic_type.py` | 7,183 | Kinetic typography | **YES** |
| `production/pipeline/lower_thirds.py` | 5,424 | Lower-third graphics | **YES** |
| `production/pipeline/stroke_reveal.py` | 8,458 | Stroke-reveal animation | **YES** |
| `production/pipeline/pupil_gag.py` | 4,747 | Pupil/eye gag animation helper | **YES** (technique) |
| `production/pipeline/palette-enforce.py` | 4,356 | Enforces a show palette on footage | **YES** — swap in WG palette |
| `production/pipeline/deghost.py` | 4,672 | De-ghosting cleanup (also duplicated at `production/tools/deghost.py`, 4,672) | **YES** |
| `production/pipeline/cleanup_lines.py` | 1,956 | Line cleanup (full version lives in the FlipaClip post chain, §6.1; also `production/tools/cleanup_lines.py`) | **YES** |
| `production/pipeline/vs-anime-cleanup.vpy` | 2,595 | VapourSynth anime cleanup script | **YES** |

### 2.4 Script → animatic → dialogue → audio
| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/pipeline/fountain_to_animatic.py` | 10,158 | Fountain screenplay → animatic | **YES** |
| `production/pipeline/fountain_to_beats.py` | 4,882 | Fountain screenplay → beat sheet | **YES** |
| `production/pipeline/animatic_builder.py` | 3,775 | Builds animatics | **YES** |
| `production/pipeline/storyboard_sheet.py` | 3,300 | Storyboard contact sheets | **YES** |
| `production/pipeline/dialogue_pipeline.py` | 11,396 | Dialogue processing pipeline | **YES** (flow); no CJ dialogue content in the tool itself |
| `production/pipeline/lipsync_align.py` | 2,801 | Lip-sync alignment | **YES** |
| `production/pipeline/tts_voices.py` | 7,910 | TTS voice driver | **YES** — WG keeps its own Chatterbox voices (Pipeline One); this is a fallback/utility, not a replacement |
| `production/pipeline/tts_voices_2026.py` | 4,971 | 2026 TTS voice driver update | **YES** (same note) |
| `production/pipeline/voice_convert.py` | 2,826 | Voice conversion | **YES** |
| `production/pipeline/transcribe_translate.py` | 7,127 | Transcription + translation (EN/JP workflow behind the EN/JP FINAL dance videos) | **YES** |
| `production/pipeline/music_gen.py` | 4,541 | Music generation hook | **YES** |
| `production/pipeline/sfx_gen.py` | 2,291 | SFX generation | **YES** |
| `production/pipeline/stem_sep.py` | 1,921 | Audio stem separation | **YES** |
| `production/pipeline/audio_restore.py` | 2,569 | Audio restoration | **YES** |
| `production/pipeline/audio-2026/README.md` | 3,047 | 2026 audio stack readme | **YES** |
| `production/pipeline/audio-2026/TOOL-LOG.md` | 4,516 | Audio tool log | **YES** |
| `production/pipeline/audio-2026/gen_notebook_audio2026.py` | 3,569 | Generates the audio Kaggle notebook | **YES** |
| `production/pipeline/audio-2026/kaggle_setup_audio2026.py` | 5,445 | Kaggle audio environment setup | **YES** |

### 2.5 Publishing, QA gates & utilities
| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/pipeline/kaggle_queue.py` | 33,089 | Kaggle job queue manager — largest pipeline script | **YES** |
| `production/pipeline/save_outputs.py` | 17,506 | Saves/collects pipeline outputs to repo | **YES** |
| `production/pipeline/ingest_queue.py` | 5,119 | Ingest queue | **YES** |
| `production/pipeline/claim_gate.py` | 5,839 | "Claim" QA gate (work must pass before being called done) | **YES** |
| `production/pipeline/verify_claim.py` | 7,996 | Verifies completion claims against evidence | **YES** |
| `production/pipeline/checkpoint_audit.py` | 4,367 | Checkpoint audit | **YES** |
| `production/pipeline/contradiction_probe.py` | 5,370 | Detects contradictory status claims in docs | **YES** |
| `production/pipeline/instance_animator_wrapper.py` | 2,489 | Wrapper for `production/tools/InstanceAnimator/` | **YES** |
| `production/pipeline/thumbnail_gen.py` | 5,595 | Thumbnail generation | **YES** |
| `production/pipeline/social_export.sh` | 2,571 | Social-format exports | **YES** |
| `production/pipeline/youtube_upload.py` | 5,491 | YouTube upload | **YES** |
| `production/pipeline/podcast_feed.py` | 2,972 | Podcast feed generation | **YES** |
| `production/pipeline/merch_qr.py` | 2,388 | Merch QR generation | **YES** |
| `production/pipeline/metadata_gen.py` | 3,384 | Metadata generation | **YES** |
| `production/pipeline/obs_scene_json.py` | 4,077 | OBS scene JSON generation | **YES** |
| `production/pipeline/research.py` | 4,662 | Research helper used by the pull-in lanes | **YES** |
| `production/pipeline/pull-to-repo.sh` | 1,634 | Pulls finished work into the repo | **YES** |
| `production/pipeline/flipaclip_post.sh` | 4,208 | FlipaClip post driver — see §6.1 (duplicate: `production/tools/flipaclip_post.sh`, 4,208) | **YES** |

---

## 3. `production/tools/` — vendored tool stack (34,276 entries in payload for the pre-`fmodel` portion alone)

Whole upstream projects vendored into the repo, most with a `CAPE-JONES-WIRING.md` / `WIRING.md` / README explaining how they were hooked up. **The wiring docs are the transferable gold; the vendored code is open-source upstream — for Wizard Gang, re-pull upstream at the pinned version and copy only the wiring doc + local patches, don't copy 1 GB of vendored trees.** Sizes below are payload aggregates (files / blob MB).

| Path | Files / size (payload) | What it is | WG? |
|---|---|---|---|
| `production/tools/audio/` | 24,663 files / 812.9 MB | Vendored Audacity (`production/tools/audio/audacity/…`) + MuseScore (`production/tools/audio/musescore/…`, incl. soundfonts `…/musescore/share/sound/MS Basic.sf3` 51,278,610 B and `FluidR3Mono_GM.sf3` 23,712,790 B) + test samples. Bulk is upstream test data | **MIXED** — tools YES (re-pull upstream); do NOT copy the 813 MB wholesale |
| `production/tools/colmap/` | 2,340 / 20.6 MB | COLMAP photogrammetry (camera/scene reconstruction) | **YES** (re-pull) |
| `production/tools/alicevision/` | 1,711 / 64.6 MB | AliceVision photogrammetry (Meshroom engine) | **YES** (re-pull) |
| `production/tools/comfyui/` | 1,422 / 49.2 MB | ComfyUI node image/video generation | **YES** (re-pull) |
| `production/tools/flowblade/` | 1,183 / 48.5 MB | Flowblade MLT video editor | **YES** (re-pull) |
| `production/tools/blenrig6/` | 689 / 42.4 MB | BlenRig 6 Blender auto-rigging | **YES** |
| `production/tools/fmodel/` | 361 / 4.0 MB (payload truncated inside this folder) | FModel — Unreal asset viewer/extractor (.NET) | **YES** |
| `production/tools/anime-upscaling/` | 303 / 3.1 MB | Anime upscaling stack | **YES** |
| `production/tools/blendertools/` | 288 / 6.7 MB | Blender add-on collection | **YES** |
| `production/tools/cloudrig/` | 245 / 16.5 MB | CloudRig Blender rigging framework | **YES** |
| `production/tools/coa_tools2/` | 196 / 17.1 MB | COA Tools 2 — cut-out animation in Blender (directly relevant to WG's cut-out/piece rigs) | **YES** |
| `production/tools/cartoon-studio/` | 175 / 6.4 MB | Cartoon studio tooling | **YES** |
| `production/tools/bgremoval/` | 125 / 8.0 MB | Background removal | **YES** |
| `production/tools/LDF-VFI/` | 108 / 75.5 MB | LDF-VFI frame interpolation incl. weights `production/tools/LDF-VFI/metrics/fvd/i3d_pretrained_400.pt` (50,939,526 B) and `…/metrics/VFIPS/exp/eccv_ms_multiscale_v33/model.pytorch` (18,435,575 B) | **YES** — weights to a release, not git (§13) |
| `production/tools/chibirigkit/` | 104 / 30.8 MB | Chibi rig kit | **YES** |
| `production/tools/SCAIL-2/` | 102 / 48.4 MB | SCAIL-2 animation tooling | **YES** |
| `production/tools/depth-anything-v2/` | 93 / 66.4 MB | Depth Anything V2 depth estimation (drives 2.5D parallax depth — complements WG Pipeline One pan/zoom parallax) | **YES** |
| `production/tools/auto-seat/` | 67 / 197.3 MB | Auto-seat / sitting-pose tooling; contains two ~97 MB proof blends (§13) | **MIXED** — code YES, CJ sitting proofs NO |
| `production/tools/dia/` | 35 / 0.8 MB | DIA tooling | **YES** |
| `production/tools/afk-rig/` | 34 / 17.6 MB | AFK rig tooling | **YES** |
| `production/tools/InstanceAnimator/` | 25 / 4.2 MB | Instance animator (wrapped by `production/pipeline/instance_animator_wrapper.py`) | **YES** |
| `production/tools/BLENDER-5X-UPGRADE.md` | 2,455 B | Blender 5.x upgrade notes | **YES** |
| `production/tools/PIPELINE-SCALING-WIRING.md` | 3,211 | How the tool stack scales/wires together | **YES** |
| `production/tools/RETRY-PULLS-README.md` | 2,127 | Retry policy for failed tool pulls | **YES** |

### 3.1 `production/tools/` folders after the truncation point (Contents API — directory + sample contents exact, recursive list not enumerated)

All of these exist on main as directories under `production/tools/`: `freemocap/` (has `CAPE-JONES-WIRING.md` 3,569 B), `fspy-blender/`, `gl-transitions/`, `glaxnimate/` (full source + `CAPE-JONES-WIRING.md` 3,067 B), `hyperframes-effects-gallery/`, `image-to-3dlab/`, `ldf-vfi/` (note: separate lowercase twin of `LDF-VFI/`), `lipsync/` (subdirs `latentsync/`, `musetalk/`), `ltx-video/`, `ltx2/`, `mesh-repair/`, `mesh2motion/`, `meshroom/`, `mhr/`, `ml-autorig/`, `mlt/`, `mocap-retarget/`, `mocap/` (`README.md` 1,641 B + `sambody4d/`), `mpfb2/`, `natron/` (full source + `CAPE-JONES-WIRING.md` 6,070 B), `one-to-all-animation/`, `open-sora/`, `opentimelineio/`, `opentoonz/` (only `README.md` 2,388 B at top — wiring/readme stub, not full source), `openvoice/`, `pencil2d/` (full source), `pinocchio-src/`, `pinocchio/`, `piper-tts/`, `ppf-contact-solver/`, `realesrgan/`, `rhubarb-lip-sync/`, `rife/` (§6.2), `simple-retarget-tool/`, `skintokens-autorig/`, `soma-x/`, `stt/`, `synfig/` (only `README.md` 2,613 B at top — stub), `tahomad2d/` (only `README.md` 2,241 B at top — stub), `theanimescripter/`, `three-anime-style/`, `toon-shader/`, `tripo-pull/`, `tts-webui/`, `uassetapi/`, `ue4ss/`, `video-gif-studio/`, `wan2.1/`, `wan2.2/`, `wiggle2/`.

**Verdict for §3.1: YES for every tool/wiring doc** (all are generic open-source production tools: mocap/retarget, lip-sync, 2D animation, compositing, TTS/STT, video generation). Transfer method = read the `*WIRING*.md`, re-pull upstream, re-apply wiring. None of these folders is Cape Jones art.

---

## 4. Movement / dance preset systems (Nov 1 wave)

### 4.1 PR #337 — `movement-dance-presets-20261101/` (17 entries, exact)
Builder + index transfer; the rendered outputs are Cape Jones pieces and do **not** transfer as art.
| Path | Size | What it does | WG? |
|---|---|---|---|
| `movement-dance-presets-20261101/build_clean.py` | 4,468 | Builds the clean preset clips | **YES** |
| `movement-dance-presets-20261101/PRESET-INDEX-20261101.md` | 2,150 | Preset definitions: A = Smiling 9-layer structure, B = Foster's punch/walk structure, C = Smiling 5-layer structure; arm-snap-fixed A/C variants (arms crossing chest moved on top of torso); all 1100×750, 24 fps, h264+AAC, faststart, MD5s listed. Index itself states: "Cape Jones pieces only, arranged to donor timing/structure… No actual visual character from another show, and no character dialogue from another show, is in any preset" | **YES** (index/system) |
| `movement-dance-presets-20261101/CLEAN-REPORT-20261101.md` | 4,060 | Verification report for the clean builds | **YES** (method) |
| `movement-dance-presets-20261101/A-SMILING-STRUCTURE-CLEAN-20261101.mp4` (+ `.gif`, + `…-ARM-SNAP-FIXED-CLEAN-20261101.mp4/.gif`) | 320,992 / 649,140 (arm-snap: 326,584 / 653,118) | Preset A output — CJ pieces on Smiling Friends layer structure/timing | **NO** as art; **YES** as timing/structure reference |
| `movement-dance-presets-20261101/B-FOSTERS-STRUCTURE-CLEAN-20261101.mp4` (+ `.gif`) | 308,088 / 640,939 | Preset B output — Foster's punch/walk structure. Index flags B "a little off and needs fixing… NOT claimed approved" | **NO** as art; **YES** structure |
| `movement-dance-presets-20261101/C-SMILING-5LAYER-STRUCTURE-CLEAN-20261101.mp4` (+ `.gif`, + arm-snap-fixed pair) | 325,589 / 630,214 (arm-snap: 328,909 / 626,245) | Preset C output | **NO** as art; **YES** structure |
| `movement-dance-presets-20261101/A-SMILING-STRUCTURE-20261101.wav`, `B-FOSTERS-STRUCTURE-20261101.wav`, `C-SMILING-5LAYER-STRUCTURE-20261101.wav` | 448,100 / 609,506 / 441,044 | Preset audio beds | **NO** |

### 4.2 PR #340 — `movement-library-clips-20261101/` (32 entries, exact)
A reusable **movement library**: 8 numbered donor-movement clips, each as `.mp4` + `.gif` + `.wav`, plus the workflow doc that turns any character into a template on that movement. This is the direct ancestor of a Wizard Gang movement library.
| Path | Size | What it does | WG? |
|---|---|---|---|
| `movement-library-clips-20261101/build_clips.py` | 4,766 | Builds all library clips | **YES** |
| `movement-library-clips-20261101/MOVEMENT-LIBRARY-20261101.md` | 10,686 | Library catalogue/method | **YES** |
| `movement-library-clips-20261101/TEMPLATE-CHARACTER-WORKFLOW-20261101.md` | 4,185 | How to swap a template character onto a library movement | **YES** — core WG reuse |
| `movement-library-clips-20261101/CLIPS-20261101.json` | 1,889 | Machine-readable clip index | **YES** (format) |
| `movement-library-clips-20261101/GATE-RESULTS-20261101.md` | 1,734 | QA gate results | **YES** (method) |
| `…/01-gumball-dance-strut-twist.{mp4,gif,wav}` | 316,950 / 2,715,239 / 398,706 | Gumball dance strut+twist movement | **MIXED** — timing/motion YES, donor name/art NO |
| `…/02-gumball-fight-kick.{mp4,gif,wav}` | 117,928 / 3,369,197 / 444,572 | Gumball fight kick | **MIXED** (same) |
| `…/03-fosters-pose-swap-gesture.{mp4,gif,wav}` | 161,803 / 196,604 / 275,228 | Foster's pose-swap gesture | **MIXED** (same) |
| `…/04-smiling-friends-pose-swap-head.{mp4,gif,wav}` | 476,287 / 819,621 / 492,200 | Smiling Friends pose-swap/head move | **MIXED** (same) |
| `…/05-scooby-song-step.{mp4,gif,wav}` | 255,627 / 569,876 / 342,260 | Scooby song step | **MIXED** (same) |
| `…/06-nick-baked-cache-walk.{mp4,gif,wav}` + `06-nick-baked-cache-walk.mp4.flash.csv` (2,580) + `.flash.json` (744) | 214,770 / 388,802 / 246,122 | Walk cycle from a baked Alembic cache (Nick donor, §5) + flash-safety analysis files | **MIXED** (same); flash-analysis format **YES** |
| `…/07-johnny-bravo-flex-dance.{mp4,gif,wav}` | 204,802 / 310,784 / 275,228 | Johnny Bravo flex dance | **MIXED** (same) |
| `…/08-richard-scooby-gang-step.{mp4,gif,wav}` | 302,434 / 1,815,157 / 395,180 | Richard (Gumball) / Scooby gang step | **MIXED** (same) |

### 4.3 Dance choreography extraction — `production/dance-choreo/` (PR #275 era, on main)
| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/dance-choreo/dance-gumball-darwin-words-sc057-sc059.json` | 1,494,080 | Extracted choreography data: Darwin's dance, Gumball "The Words" (GB214) Sc057 (198 f) + Sc059 twist (105 f), 25 fps, ~107 BPM beat grid, twist 32 keys f43–97. Keyframes/timing as JSON — the "extract rig dance → swap your character on" asset | **YES** for keyframe/timing data; **NO** for the Darwin character/name — re-label on transfer |
| `production/dance-choreo/README.md` | 6,076 | Method: pull dance animation from pro rigs as choreography, swap own character onto the motion once 2D FLAs exist; proof rendered from source SWF with JPEXS FFDec | **YES** |
| `production/dance-choreo/INVENTORY.md` | 5,026 | Choreo inventory | **YES** |
| `production/dance-proof-2d/build_dance.py` (7,300) + `stage2_render.py` (8,635) + `make_music.py` (2,646) + `README.md` (3,041) under `production/dance-proof-2d/` | — | 2D dance proof builder/renderer/music | **YES** (builders); `production/dance-proof-2d/chiptune-alt.wav` (926,144) **NO** |
| `production/dance-proof-3d/build_dance.py` (15,391) + `make_chiptune.py` (3,140) + `README.md` (3,563) under `production/dance-proof-3d/` | — | 3D dance proof builder (the PR #270–#274 stack's successor work) | **YES** (builders) |
| `production/assets/dance-proof/cj-dance-proof-2d-v1.mp4` (5,867,106) + `cj-dance-proof-2d-sheet.png` (549,042) under `production/assets/dance-proof/` | — | Rendered CJ dance proof | **NO** |

### 4.4 PR #341/#342 — dance scenes + flash fix
| Path | Size | What it does | WG? |
|---|---|---|---|
| `dance-scene-2videos-20261101/build_scene.py` | 7,432 | Dance scene builder (Video 1) | **YES** |
| `dance-scene-2videos-20261101/build_scene2.py` | 7,889 | Dance scene builder (Video 2) | **YES** |
| `dance-scene-2videos-20261101/make_sfx.py` | 2,726 | SFX track builder | **YES** |
| `dance-scene-2videos-20261101/REPORT-20261101.md` | 9,783 | Build/verification report | **YES** (method) |
| `dance-scene-2videos-20261101/SCENE2-META-20261101.json` | 1,361 | Scene metadata | **YES** (format) |
| `dance-scene-2videos-20261101/dance-scene-V1-EN-FINAL-20261101.mp4` | 26,840,791 | FINAL dance scene Video 1 (EN) | **NO** — CJ episode output; also §13 size flag |
| `dance-scene-2videos-20261101/dance-scene-V2-JP-FINAL-20261101.mp4` | 26,821,597 | FINAL dance scene Video 2 (JP) | **NO**; §13 |
| `dance-scene-2videos-20261101/check-V1-cut1.png` … `check-V2-cut4.png` (8 files, 670,387–894,878) | — | Per-cut proof frames | **NO** |
| `dance-flash-fix-20261101/flash_check.py` | 8,395 | **Photosensitivity/flash-safety checker** — analyses video, emits `.flash.csv`/`.flash.json` (frame flash events). Used across dance/movement folders | **YES** — high value, show-agnostic |
| `dance-flash-fix-20261101/build_fixed.py` (6,267) + `build_fixed_v1.py` (5,973) + `build_sfx.py` (3,702) | — | Rebuilds dance test with flash fixes + faststart | **YES** |
| `dance-flash-fix-20261101/dance-test-FIXED-v2-EN-full-SFX-FASTSTART-20261101.mp4` | 28,546,238 | Fixed Video 3 (EN) | **NO**; §13 |
| `dance-flash-fix-20261101/dance-test-FIXED-v2-JP-full-SFX-FASTSTART-20261101.mp4` | 28,548,173 | Fixed Video 4 (JP) | **NO**; §13 |
| `dance-flash-fix-20261101/dance-test-FIXED-v2-one-loop-20261101.mp4` (+ `.flash.csv` 4,882 + `.flash.json` 490) | 2,174,634 | One-loop test + its flash analysis | **NO** (clip); analysis format **YES** |
| `dance-test-20261101/build_test.py` (1,618) + `build_test2.py` (1,338) + `DANCE-TEST-REPORT-20261101.md` (7,983) | — | Dance test builders/report (PR #340 D3) | **YES** |
| `dance-test-20261101/dance-test-EN-excerpt-20261101.mp4` / `-JP-excerpt-` (1,874,405) / `-visual-silent-` (1,798,518) / `.gif` (7,628,092) + check frames | — | Dance test outputs | **NO** |

### 4.5 Beat-sync presets — PR #352/#353
| Path | Size | What it does | WG? |
|---|---|---|---|
| `beatsync-presets-20261101/BEATSYNC-PRESETS-20261101.md` | 6,303 | Solves a real mismatch: song 152 BPM vs visual grid ~107 BPM (measured 105.4). Preset A (CHOSEN): re-time visual ×1.42056 to 152 BPM; Preset B: stretch audio ×0.70395 to ~107 BPM; Preset C saved as alternate. Includes the rule: flash gate MUST re-run after any re-time | **YES** — generic audio/visual sync technique + preset format |
| `batch-c-gif-principles-beatsync-20261101/` (21 entries) | — | PR #352 source batch: GIF previews, 12-principles checks, beat-sync prep (`…/beatsync/BEATSYNC-PREP-20261101.md`, option-A sample MP4 185,604 B) | **YES** (method/docs); sample media **NO** |

### 4.6 Other movement systems inside `cape-jones-rig/`
| Path | Entries/size | What it does | WG? |
|---|---|---|---|
| `cape-jones-rig/poses-as-movements-20261031/build_movements.py` (8,845) + `MOVEMENTS-META-20261031.json` (523) + report (3,619); folder 494 entries / 33.0 MB of frames | — | Turns static poses into movements (pose-to-motion builder) | Builder **YES**; frames **NO** |
| `cape-jones-rig/movements-interp-v2-20261031/build_interp_v2.py` (13,999) + `REPORT-20261031.md` (7,858); 285 entries / 30.6 MB | — | Movement interpolation v2 (punch→flex etc.) | Builder **YES**; frames **NO** |
| `cape-jones-rig/inbetween-20261031/INBETWEENING-STACK-20261031.md` (6,938) + `build_inbetween.py` (14,429) + `blender_gp_interpolate.py` (1,358); 318 entries / 49.5 MB | — | Inbetweening stack (Grease Pencil interpolation + arc tracking) | **YES** (stack/builders); outputs **NO** |
| `cape-jones-rig/dance-recreation-20261031/build_recreation.py` (4,143) + `DANCE-RECREATION-REPORT-20261031.md` (7,803) + `AUDIO-SLOT-EN-JP-20261031.md` (1,973); 446 entries / 232.1 MB | — | Full dance recreation build | Builder/docs **YES**; 232 MB of media **NO** + §13 |
| `cape-jones-rig/shimmy-step-fix-20261101/`, `jump-chain-fix-20261101/`, `jump-hands-flip-vertical-20261101/`, `dance-arm-snap-20261031/`, `dance-kneefeet-fix-20261031/`, `dance-kneefeet-fix-correction-20261031/`, `dance-improved-20261031/`, `dance-inbetween-hands-20261031/`, `dance-inbetween-hands-lastframe-fix-20261031/`, `ghoul-shuffle-v2-free-hands-20261031/`, `ghoul-shuffle-v3-hand-mobility-20261031/`, `ghoul-shuffle-lastframe-handswap-20261031/` | 57–122 entries each | Dated movement-fix batches (step, jump chain, hand flips, knee/feet, arm snap) — each a worked fix with builders + proofs | Method/builders **YES**; CJ/gag media **NO** |
| `ARM-FRONT-SNAP-RULE.md` (root, 18,132) + `cape-jones-rig/ARM-FRONT-SNAP-RULE.md` (17,661) + `arm-front-snap-auto-20261101/` (40 entries, incl. `CLIP-SNAP-AUDIT-20261101.csv`) + `arm-snap-last3-fix-20261101/` (14) + `preset-b-arm-snap-20261101/` (16) + `blender523-motion-arm-snap-early-20261101/` (7) + `blender523-motion-snap-lock-study-20261101/` (11) | — | The "arm snap" rule system: when arms cross the body they snap to the correct layer, with audit CSV + lock study | **YES** — layer-ordering technique, directly reusable for WG piece rigs |
| `cape-jones-rig/KNEE-FEET-RULE.md` (7,514) + PR #346 learning-gate `rules.json` update + `HEAD-TURN-RULE-20261101.md` (root, 734) | — | Universal knee/feet and head-turn animation rules | **YES** |

---

## 5. PR #345 — donor FLA rig pull: `donor-fla-rig-pull-20261101/` (7 entries, exact)

**Critical honest finding (from the folder's own report): there are NO donor `.fla`/`.swf` binaries in this repo.** PR #345 landed *listings and structure summaries only* — exactly as its title says.

| Path | Size | What it does | WG? |
|---|---|---|---|
| `donor-fla-rig-pull-20261101/DONOR-FLA-RIG-PULL-REPORT-20261101.md` | 7,273 | States plainly: actual .fla/.swf binaries are NOT on disc; what exists is verified remote-release listings (GitHub central-directory/range reads), a local Gumball file listing (2,259 entries, listing only), and structure summaries (layer stacks, part counts, fps, frame counts, timing grids). Builds are STRUCTURE RETARGETS to CJ's own pieces, marked TEMPLATE-PLACEHOLDER. A real binary parse is a separate step, not claimed | **YES** — method + honesty template |
| `donor-fla-rig-pull-20261101/INVENTORY-20261101.json` | 8,192 | Donor inventory table: Gumball (S2 62 .fla, CN-Leaks 71 .fla, RAR5 2,259 files, 20 dance FLAs; Darwin "The Words" GB214 Sc057/Sc059 the only verified performed dance); Foster's Frankie (1 binary FLA, 430 part comps, turnarounds 3/4:118 / side:82 / 3/4-back:30 / front:28 / back:16); Foster's web reels (7 .fla + 15 .swf, 1,618–2,190 f @24 fps); Smiling Friends Charlie/Pim (2 XFL FLAs, 82,390 B / 296,483 B, Animate 22, 1920×1080, scene timelines EMPTY — rigs only); Randy Cunningham (6 .fla, 4 .swf, scene RC118_SC001 + AE project + BG .ai); Nick single-show (8 Maya .ma rigs + 4 Alembic .abc caches f1-182/183-244/244-399/400-586, 1,028 audio files listed) | **YES** for structure/counts/timing; **NO** donor names/art as WG content |
| `donor-fla-rig-pull-20261101/LIPSYNC-TIMING-20261101.csv` | 6,741 | Lip-sync timing grid extracted from donor structure | **YES** (timing data) |
| `donor-fla-rig-pull-20261101/build.py` | 12,142 | Builds placeholder structure retargets from the listings | **YES** |
| `donor-fla-rig-pull-20261101/check_template_gate.py` | 1,191 | Gate: verifies a build is really template/placeholder, not shipped donor art | **YES** |
| `donor-fla-rig-pull-20261101/PLACEHOLDER-STRUCTURE-20261101.png` | 73,613 | Placeholder structure proof image | **NO** (image), method YES |
| `full-leak-20261101/vault-small-shows/MANIFEST-20261101.json` + `REPORT-20261101.md` + `releases_groupD_20261101.txt` (13 entries total in `full-leak-20261101/`) | — | PR #358-era leak/listing manifest for small-show vault material | Listing/method **YES**; the 5 `ACTUAL-DONOR-PLACEHOLDER-RickAndMorty-*-RIG-SHEET-20261101.png` files under `full-leak-20261101/vault-small-shows/files/` **NO** |
| `cape-jones-rig/gumball-full-leak-file-list-20261031.json` (460,945) + `gumball-full-leak-rar5-summary-20261031.md` (1,646) | — | Full Gumball leak file listing + RAR5 summary (listing only, no binaries) | Listing **YES** as an index; content **NO** |
| `unknown-archive-listing-20261101/UNKNOWN-ARCHIVE-LISTING-20261101.md` (17,365) + `archive-scan-20261101.txt` (3,565) | — | PR #352: listing/scan of an unidentified archive | **YES** (method) |

**Transfer implication:** a Wizard Gang FLA-donor lane cannot copy donor rigs *from this repo* — it must repeat the pull (range-read listings → structure summary → retarget) against the owner's holdings/releases, reusing `build.py` + `check_template_gate.py` + the inventory JSON schema.

---

## 6. Render / post pipelines

### 6.1 FlipaClip post — the finished 2D post chain
| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/pipeline/FLIPACLIP-POST-PIPELINE.md` | 5,691 | 5-stage post for hand-drawn phone animation (12 fps → broadcast): (1) ffmpeg denoise+deflicker `hqdn3d=1.5:1.5:6:6`, `deflicker=size=5`; (2) OpenCV line cleanup; (3) RIFE v4 interpolation 12→24 fps at source res (CPU ~26 s/pair; `--fast` = ffmpeg `minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir`); (4) upscale — Lanczos default, `--upscale` = ESPCN ×4 → Lanczos 2× (`models/ESPCN_x4.pb`); then grades → bloom → audio master → cards. One command: `flipaclip_post.sh input.mp4 output.mp4 [--upscale]` | **YES** — verbatim WG reuse (any hand-drawn WG material) |
| `production/pipeline/flipaclip_post.sh` | 4,208 | The driver script above (duplicate at `production/tools/flipaclip_post.sh`, 4,208) | **YES** |
| `production/pipeline/cleanup_lines.py` | 1,956 | Line cleanup: bilateral filter (preserves flat colour/edges), thin-line detection excluding large connected fills (>4,000 px — the fix that stopped fills being recoloured), pinhole morphological close, crisp near-black line redraw. Never recolours fills | **YES** |

### 6.2 RIFE / interpolation
| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/tools/rife/` (subtree verified) | — | Full vendored RIFE repo: `README.md` (9,583), `WIRING.md` (2,216), `inference_video.py` (11,008), `inference_video_enhance.py` (7,710), `inference_img.py` (4,561), `inference_img_SR.py` (2,870), `model/warplayer.py` (1,209), `model/loss.py` (4,641), `demo/` GIFs/PNGs | **YES** (re-pull upstream + copy `WIRING.md`) |
| `production/kaggle/rife/README.md` | 2,732 | RIFE on Kaggle GPU route (the production route in ANIMATION-PIPELINE-2026: 12→24 fps on T4 in minutes vs CPU hours) | **YES** |
| `production/pipeline/render_half_interp.py` / `scene_aware_interp.py` / `ldf_vfi_wrapper.py` | 5,205 / 7,392 / 2,909 | See §2.2 | **YES** |
| `cape-jones-rig/experimental-25-20261031/group-a-interpolation/proofs/rife-proxy-jojo01-to-jojo02-20261031.gif` (441,084) + `.png` (135,344) | — | RIFE proof pair on pose frames | **NO** (media); proof method YES |
| `docs/research/INTERPOLATION-RESEARCH.md` (5,556), `docs/research/POST-INTERPOLATION.md` (6,093), `docs/research/PRO-INBETWEENING-RESEARCH.md` (9,955) | — | Interpolation research/wiring notes | **YES** |

### 6.3 Lighting presets & looks
| Path | Size | What it does | WG? |
|---|---|---|---|
| `docs/lighting/REAL-LIGHTING-RESEARCH.md` | 14,823 | Real lighting research base | **YES** |
| `docs/lighting/LED-CONTROLLER.md` | 5,466 | LED controller design (pairs with `led_controller.py`) | **YES** |
| `docs/lighting/COLOR-GRADES.md` | 4,050 | Grade definitions | **YES** |
| `docs/lighting/RENDER-LOOKS.md` | 2,641 | Render looks | **YES** |
| `docs/lighting/DYNAMIC-RIM-BLASTER-LIGHTING.md` | 3,253 | Dynamic rim lighting | **MIXED** — rim technique YES, "blaster" gag NO |
| `docs/lighting/previews/` (15 PNGs, 151,964–219,631 each: `cj-day`, `cj-night`, `cj-ember`, `cj-ghost`, `cj-gold`, `cj-royal`, `cj-trippy`, `cj-beach-day`, `cj-beach-sunset`, `cj-ocean`, `outside-acid`, `outside-dusk`, `outside-noir`, `outside-storm`, …) | — | Look preview stills | **NO** (CJ stills); preset values in the docs **YES** |
| `docs/lighting/references/` (10 PNGs, 154,289–271,322: bulb/LED-strip reference photos) | — | Lighting reference photos | **YES** (generic reference) |
| `3d-assets/living-room/lighting/LIGHTING-RIG.md` | 7,175 | Blender lighting rig doc | **YES** |
| `3d-assets/living-room/lighting/apply_lighting_rig.py` | 11,000 | Applies the lighting rig in Blender | **YES** |
| `3d-assets/living-room/lighting/set_led_preset.py` | 2,556 | Sets an LED preset | **YES** |
| `3d-assets/living-room/lighting/render_proof.py` | 2,728 | Lighting proof render | **YES** |
| `cape-jones-rig/figure-matched-lighting-presets-vertical-horizontal-20261031/` (64 entries / 31.8 MB): `build_presets.py` (8,498), `PRESET-INDEX-20261031.json` (34,653), report (4,663), `presets/S1-v2-warm-overhead/PRESET-S1-v2-warm-overhead-20261031.json` (3,739) + per-preset horizontal/lit-transparent/on-grey PNGs | — | Figure-matched lighting preset system in both orientations (portrait+landscape — same dual-orientation discipline WG uses) | System/index/builders **YES**; CJ preset proof PNGs **NO** |
| `cape-jones-rig/LIGHTING-LEVELS-0-5.md` (4,656) + `LIGHTING-LEVELS.md` (2,788) + `apply_lighting_levels.py` (4,010) + `apply_lighting_level2_v2.py` (8,453) | — | 0–5 lighting-level system + Blender appliers | **YES** |
| `cape-jones-rig/shading-preset-library-20261031/` (50 entries / 3.4 MB): `SHADING-PRESET-INDEX-20261031.md` (12,781), tier contact sheets (archive/clean/experimental/reference/soft/strong/test_only) | — | Tiered shading preset library | Index/system **YES**; contacts **NO** |
| `cape-jones-rig/shadow-presets-angle-level-20261031/` (78 entries / 20.7 MB): `angle_level/front-bright.png`, `back-darkness.png`, … (angle × level matrix) + terminology/report docs | — | Shadow preset matrix by camera angle × light level | System/docs **YES**; CJ shadow stills **NO** |
| `cape-jones-rig/DUAL-LIGHT-RIM-MIX-20261031.md` (8,721), `RIM-COLOR-RULE.md` (4,782), `rim-bleed-glow-library.json` (7,796), `COMPOSITING-LIGHTING-SPEC.md` (2,859), `COLOR-LIGHTING-COMPOSITING-RESEARCH-20261031.md` (3,328) | — | Rim/dual-light/compositing rules | **YES** |
| `cape-jones-rig/shafts-…` family: `shafts-fix-100-20261031/` (71 entries), `shafts-environmental-depth-lighting-upgrade-20261031/`, `shafts-v4-grounded-20261031/`, `shafts-volumetric-upgrade-20261031/`, `godray-level3/4/5-20261031/` | — | Volumetric light-shaft / godray levels | Technique **YES**; EXR/media **NO** (§13) |
| `production/colab/cape_jones_lighting_reel_colab.ipynb` (8,250) + `validate_lighting_reel_notebook.py` (5,748) under `production/colab/` | — | Lighting-reel Colab notebook + validator | **MIXED** — notebook flow YES, CJ reel NO |
| `.github/workflows/lighting-reel-preflight.yml` | 929 | CI preflight for the lighting reel | **YES** |

### 6.4 Compositing / colour / VFX stack in `cape-jones-rig/`
| Path | Size | What it does | WG? |
|---|---|---|---|
| `cape-jones-rig/apply_compositor.py` | 16,125 | Applies the Blender compositor stack | **YES** |
| `cape-jones-rig/blender-compositor-stack.py` | 10,556 | Compositor stack definition | **YES** |
| `cape-jones-rig/compositor-stack-spec.json` | 7,976 | Compositor spec (machine-readable) | **YES** |
| `cape-jones-rig/WIRED-COMPOSITOR-STATUS.md` | 5,188 | Compositor wiring status | **YES** |
| `cape-jones-rig/UNIVERSE-COLOR-LANGUAGE*.md` (7,233 / 20,597 / 16,691 / +addendum 4,913) | — | Show colour-language system | **MIXED** — system YES, CJ palette NO (WG writes its own) |
| `cape-jones-rig/EFFECTS-DESIGN-V2-20261031.md` (14,997), `COLOR-KEY-VFX-STACK-10.md` (3,183), `INDUSTRY-VFX-PIPELINE.md` (6,655) | — | VFX design/pipeline docs | **YES** |
| `cape-jones-rig/presets/effects-sunbeam-preset-v1-20261031/blender_effects_v2_proof.py` (9,439) + preset doc (4,133) | — | Sunbeam effect preset | **YES** (code/doc); proof PNG **NO** |

---

## 7. Flash / FLA tooling

| Path | Size | What it does | WG? |
|---|---|---|---|
| `cape-jones-rig/build-fla-timeline.jsfl` | 3,555 | JSFL: builds an FLA timeline programmatically in Adobe Animate | **YES** |
| `cape-jones-rig/build-cape-jones-rig.jsfl` (3,621), `build-cape-jones-rig-v2.jsfl` (3,810), `build-cape-jones-rig-v7.jsfl` (3,459), `build-cape-jones-rig-v8.jsfl` (3,524) | — | JSFL rig builders (versioned) | **MIXED** — JSFL technique YES, CJ rig content NO |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/tool1_opencv_match.py` | 2,705 | FLA piece labelling tool 1: OpenCV template match | **YES** |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/tool2_embedding_knn.py` | 2,322 | Tool 2: embedding + kNN piece identification | **YES** |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/tool3_naming_schema.py` | 4,650 | Tool 3: piece naming schema | **YES** |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/tool4_xfl_jsfl.py` | 3,377 | Tool 4: XFL/JSFL export of labelled pieces | **YES** |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/tool5_swf_ruffle.py` | 3,966 | Tool 5: SWF playback/QA via Ruffle | **YES** |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/label_pieces.py` (5,366), `apply_corrections.py` (1,854), `fix_bands_regen.py` (3,008) | — | Labelling driver + human-correction loop + band regen | **YES** |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/README.md` (9,925) + `TOP5-FLA-PIECE-LABELLING-20261031.md` (8,717) + `MARS-EYE-WORKFLOW-20261031.md` (3,856) | — | Top-5 labelling method + owner-eye correction workflow | **YES** |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/ruffle` | 36,522,400 | Vendored Ruffle binary (SWF player) sitting in git | **YES** tool, but **§13: belongs in a release, not git** |
| `cape-jones-rig/fla-piece-labelling-top5-20261031/batch-60-20261031/` (contact sheets, `proposals.json` 78,264, `corrected.json` 82,197, correction txts) | — | A worked 60-piece labelling batch | Method **YES**; CJ piece sheets **NO** |
| `cape-jones-rig/wired-100-20261031/wired-xfl-punch-20261031/DOMDocument.xml` | 7,976 | A wired XFL document (Animate uncompressed FLA) proving the XFL path | **MIXED** — XFL structure YES, CJ content NO |
| `fla-choose-side-back-20261101/` (14 entries, PR #338) | — | FLA piece choosing for side/back views (`choose-BACK-cape.png`, `choose-BACK-arms-hands.png`, …) | Method **YES**; CJ pieces **NO** |
| `cape-jones-rig/build-still-20261101/fla-corrections/` + `cape-jones-rig/fla-compare-flex-inspect-20261101/fla-corrections/` (`NOTES-20261101.md` 6,729/9,552, `build_native_sheets.py` 1,934, `corrected-preview*.json` 87,006/82,090) | — | FLA correction/native-sheet workflow | **YES** (workflow/builders); sheets **NO** |
| `cape-jones-rig/fla-compare-flex-inspect-20261101/REPORT-20261101.md` (9,303) + `comparison-tests/` (Blender full-height scripts 1,750/1,443) | — | FLA-vs-Blender comparison inspection | **YES** |
| Toon Boom route (the FLA-adjacent pro 2D route): `toon-boom-linux-20261101/README-LINUX-WIRING-20261101.md` (2,839), `ROUTE-REPORT-20261101.md` (8,166), `install-harmony-rocky-chroot.sh` (3,318); `cape-jones-rig/toon-boom-10-ways-20261101/10-WAYS-REPORT-20261101.md` (25,239) + `DECISION-TABLE-20261101.csv` (1,635) + `scripts/check_env.py` (1,148); `cape-jones-rig/toon-boom-own-version-20261101/` (README 2,601, wiring checklist 4,816); `cape-jones-rig/toon-boom-wire100-20261101/`; `wire-up-cannot-do-20261101/WIRED-UP-REPORT-20261101.md` (8,054) + `LAUNCH-READY-20261101.md` (1,844) + `build_fast_clip.py` (6,431) + Toon Boom exporter subdir (PR #339) | — | Getting Toon Boom Harmony running on Linux (Rocky chroot/container) + an in-house Toon-Boom-style fallback + fast-clip exporters | **YES** — all wiring/install craft; container chunks §13 |

---

## 8. 3D assets & tooling — `3d-assets/` (507 entries in payload)

| Path | Entries/size | What it does | WG? |
|---|---|---|---|
| `3d-assets/cape-jones-rig/` | 290 entries / 956.3 MB | CJ 3D rig blends: `cape_jones_rigged.blend` (95,744,707), `cape_jones_rigged_w5r.blend` (92,125,095), `cape_jones_rigged_w5r_clean.blend` (96,835,930), `cape_jones_rigged_w5r_idle.blend` (96,975,121), `cape_jones_rigged_w5r_idle_cape_STEP1.blend` (96,903,454), `sitting_pose_library.blend` + `sitting_pose_library_fixed.blend` (96,943,918 each), `.scratch/led_test.blend` (96,847,082), `.scratch/snap_test.blend` (96,832,427), `idle-test/idle_frames.zip` (19,840,331) | **NO** — CJ character rig; §13 size flag on every blend |
| `3d-assets/living_room.blend` | 92,300,171 | CJ living-room set blend | **NO**; §13 |
| `3d-assets/living-room/` | 112 entries / 11.1 MB | Set pieces + the lighting subfolder in §6.3 | Lighting **YES**; set art **NO** |
| `3d-assets/face-rig/` | 20 entries / 93.3 MB | Face rig + `3d-assets/face-rig/tools/rhubarb/Rhubarb-Lip-Sync-1.14.0-Linux.zip` (87,225,003) | Face-rig *method* **YES**; CJ face **NO**; Rhubarb zip §13 (re-pull upstream) |
| `3d-assets/tripo-sitting-model/` | 34 entries / 101.3 MB | Tripo sitting model: `pieces/him.glb` (9,588,684), `pieces/chair.glb` (9,514,928), `canon-matched/` and `owner-spec/` grounded duplicates | **NO** (CJ model); Tripo→grounding workflow **YES** |
| `3d-assets/animation/` | 19 entries / 20.9 MB | 3D animation assets | **MIXED** |
| `3d-assets/blaster-vfx/` | 14 entries / 2.7 MB | Blaster VFX assets | **NO** (CJ gag prop) |
| `3d-assets/attire2-pieces/` | 8 entries / 2.3 MB | CJ attire pieces | **NO** |
| `3d-assets/sitting-physics/` | 7 entries | Sitting physics setup | **YES** (technique) |
| `3d-assets/living_room_layout.json` | small | Room layout data | **NO** |
| `mocap_retarget.py` (root) | 8,283 | Mocap retargeting script | **YES** |
| `proof_render.py` (root) | 1,293 | Proof render driver | **YES** |
| `proof/sitting_mocap.blend` | 92,973,898 | Mocap sitting proof blend | **NO**; §13 |
| `anims/show/cape-jones/*.glb` (9 files, 103,168–166,768: `ep1_cape_stance.glb`, `ep1_cape_strike_light.glb`, `ep1_cape_strike_heavy.glb`, `ep1_cape_hit.glb`, `ep1_cape_hit_launch.glb`, `ep1_cape_ko.glb`, `ep1_cape_portal_flight.glb`, `ep1_cape_channel_flip.glb`, `idle.glb`) + `anims/show/EP01-FIGHT-CHOREOGRAPHY.md` (4,847) | — | EP01 cape-channel animation clips (GLB) + fight choreography doc | Clips **NO**; GLB-per-move library *format* **YES** |
| `anims/show/pantera/ep1_pantera_stance.glb` (74,832) + `ep1_pantera_grab.glb` (61,932) | — | Pantera (Western Heart crossover) clips | **NO** for CJ repo purposes — belongs to Western Heart lane, not WG |
| Blender 5.2.3 toon rig batches: `blender523-rig-fixed-20261101/cape_jones_toon_blender523_FIXED.blend` (114,612), `blender523-rig-refined-20261101/cape_jones_toon_blender523_REFINED.blend` (118,221), `blender523-motion-arm-snap-early-20261101/cape_jones_toon_blender523_SNAP_EARLY.blend` (118,701), each with renders/reports (PR #344) | — | Small toon-style Blender 5.2.3 rigs + Grease Pencil overlay refinement | Rig *approach* **YES**; CJ blends **NO** |
| `production/sitting-saga-20261023/scripts/` (72 entries): `capebake/` (Blender bake/build-stage scripts, kernels, render kernels), `sitcanon/` (build-final, composites, mech-scratch stage builders), `root-probes/phys-cape*.py` (7 physics probes) | — | The sitting-saga build system: staged Blender scene builds + cape physics probes | System **YES**; CJ sitting content **NO** |

### 8.1 Root `tools/` (Contents API — 24 subdirs, exact names)
`tools/blender-mcp/`, `tools/camera-match/`, `tools/crt-tv/`, `tools/extra-lights/`, `tools/hdri-textures/`, `tools/inference/`, `tools/layout-rules/`, `tools/led-3d/`, `tools/light-editor/`, `tools/lighting/`, `tools/pulled/`, `tools/render-manager/`, `tools/rigging/`, `tools/scatter/`, `tools/scene-render/`, `tools/show-cloth/`, `tools/show-retarget/`, `tools/show/`, `tools/studio-speed/`, `tools/textures-proc/`, `tools/upscale-denoise/`, `tools/volumetrics/`, `tools/weights/`, `tools/wired/`.
**Verdict: YES** as a category (Blender MCP, camera match, lighting/LED, retarget, cloth, scatter, volumetrics, upscale/denoise are all show-agnostic craft). Recursive contents not enumerated (post-truncation zone) — a follow-up lane should tree `tools/` subtree-by-subtree before copying anything.

---

## 9. The `cape-jones-rig/` 2D piece-rig system (17,475 entries in payload — the show's core)

This is a sliced-piece 2D rig: character cut into labelled pieces, assembled by JSON spines, posed by locked-joint rigs, checked by gate scripts. **The system is the most WG-relevant thing in the repo after `production/pipeline/`; the pieces are Cape Jones and do not transfer.**

### 9.1 System / code (YES)
| Path | Size | What it does | WG? |
|---|---|---|---|
| `cape-jones-rig/joint_locked_rig.py` (7,976) + `_v4` (6,178) + `_v5` (7,378) + `_v6` (7,435) + `_v7` (6,534) + `_v7b` (5,407) + `_v7c` (5,676) | — | Locked-joint piece rig, versioned | **YES** |
| `cape-jones-rig/locked-joints-v3.json` (1,184) … `locked-joints-v6.json` (1,225), `locked-default-tpose.json` (1,471), `locked-default-tpose-v8-candidate.json` (1,499), `locked-default-rig.json` (1,559), `cape-jones-rig-spine.json` (4,507) | — | Joint-lock + T-pose + spine data schemas | **YES** (schemas; re-author values for WG cast) |
| `cape-jones-rig/assemble_tpose_default.py` | 2,155 | Assembles default T-pose from pieces | **YES** |
| `cape-jones-rig/slice_clean.py` | 4,877 | Clean slicing of character art into pieces | **YES** |
| `cape-jones-rig/check_arm_alignment.py` (2,986), `check_gauntlet_flip.py` (2,513) | — | Rig QA checkers | **YES** (pattern; gauntlet check is CJ-part-specific) |
| `cape-jones-rig/render_clips.py` (1,297), `render_clips_v6.py` (1,509), `render_walk.py` (825) | — | Clip/walk renderers | **YES** |
| `cape-jones-rig/repose_tests_v1.py` (4,140), `repose_tests_v2.py` (3,488) | — | Repose test harness | **YES** |
| `cape-jones-rig/pipeline-auto-20261101/pipeline_auto.py` (8,344) + `HOW-TO-USE-3-STEPS.md` (669) + gate JSONs | — | One-shot automated rig pipeline with literal-vs-real gate outputs | **YES** |
| `cape-jones-rig/pose_driven_swaps.json` (1,189), `layout-passes-templates.json` (1,353), `shot-spec-templates.json` (2,619), `color-shot-spec-template.json` (1,960), `audio-cue-template.json` (230) | — | Template/data formats for poses, layouts, shots, cues | **YES** |
| `cape-jones-rig/asset-manifest.json` | 95,179 | Full rig asset manifest format | **YES** (format) |
| `cape-jones-rig/rig-drag-widget-20261101.html` (6,463) + `rig-drag-widget-v2-20261101.html` (579,967) | — | Browser drag-the-rig widget (v2 is media-heavy) | **YES** (v1 pattern) |
| Side/back/front rig batches (PRs #332/#333/#338/#351/#356/#357): `side-rig-auto-20261101/build_auto.py` (19,174) + `make_blender.py` (2,073) + `side-rig-auto-spine.json` (1,171); `side-pack-new-20261101/MANIFEST.json` (3,022); `back-pack-base-20261101/MANIFEST.json` + report (20 entries); `batch-b-side-rig-next-20261101/` (67 entries); `side-bent-layer-fix-20261101/`, `side-rig-fixed-20261101/`, `side-rig-wrist-fix-20261101/`, `shots-CJ01-CJ10-layer-removed-20261101/` (PR #349), `production-extensions-elbow-sole-20261101/build_native_sole.py` + elbow/sole folders (54 entries), `production-extensions-20261101-angle-sheets-234/` (28 entries, bird's-eye/worm's-eye/diagonal-lunge derived assemblies) | — | Auto side-rig generation, piece packs per view, layer fixes, native sole/elbow construction, derived angle sheets | Builders/manifests/method **YES**; every CJ piece PNG **NO** |
| `cape-jones-rig/12-PRINCIPLES-CHECKLIST-20261031.md` (4,229), `ANIMATION-SYSTEM.md` (5,228), `SHOW-BUILDING-METHOD.md` (2,586), `PIPELINE-TEMPLATE-20261031.md` (5,661), `UNIVERSAL-PIPELINE.md` (5,110), `TV-PRODUCTION-STACK-20261031.md` (12,443) | — | Animation principles gate + show-building method docs | **YES** |
| Gate/rule docs at root: `AUDIT-FIXES.md` (949), `HONEST-LABELING-RULE-20261101.md` (2,265), `REFER-BACK-INDEX-20261101.md` (8,905); folders `learning-remembering-gate-20261101/` (32 entries, PR #346), `high-thinking-gates-20261101/` (23), `honest-audit-20261101/` (13) | — | The learning/honesty gate system: correction log, calibration, claim-vs-completion rules | **YES** — process craft, show-agnostic |

### 9.2 CJ art / content (NO — do not transfer)
`cape-jones-rig/sliced-clean-20261031/` (3,142 entries / 125.9 MB), `sliced-68-unsliced-20261031/` (1,122 / 57.3 MB), `cut-limbs*/`, `pieces/`, `pack1/`, `pack1-clean/`, `cape-jones-sliced.zip` (854,783), `cape-jones-pack1-clean.zip` (1,316,446), all `assembly-preview*.png`, `rig-apose-*.png`, character pose/movement frame folders (`rig-chains-20261031/` 789 / 52.3 MB, `showcase/` 456 / 141.0 MB, `storyboards-animatic-20261031/` 418 / 171.9 MB, `shots-endtoend-20261031/`, `shots-final-painted-bg-20261101/` 68 / 127.7 MB, `transparent-plates-*/` ~200 MB combined), `characters/cape-jones.md` (5,467), `characters/design-sheet.png` (477,048), `characters/sheets/` (10 sheets, 84,648–433,309), `characters/COWL-COLOR-OPTIONS.md` (1,201). **All NO** — Cape Jones character, design, story.

### 9.3 Mouth / lip-sync production (MIXED)
`cape-jones-rig/lipsync-production-20261031/` (257 entries / 50.0 MB: `build_chart.py` 10,074, `build_composites.py` 6,874, `build_fitted.py` 7,589, `build_gifs_audio.py` 7,508, `REPORT-20261031.md` 19,417), `cape-jones-rig/eyes-mouths-production-20261031/`, `mouth-clean-pipeline-general-20261031/`, `mouth-packs-clean-pipeline-20261031/`, `mouth-jaw-movement-20261031/`, `visemes-v2-20261031/`, `superhero-mouths-20261031/`, `MODEL-SHEET-VISEME-PLAN.md` (4,000), `characters/sheets/06-viseme-phoneme-mouth-matrix.jpg` (351,622). **Builders, chart method and the mouth-clean pipeline: YES. CJ mouth/viseme art: NO** (WG re-authors visemes for its own cast; Rhubarb/LatentSync/MuseTalk wiring in §3/§8 covers the automated side).

---

## 10. Episode / scene outputs & remaining Nov batches (mostly NO, builders YES)

| Path | What it is | WG? |
|---|---|---|
| `episode-cj01-cj30-clean-20261101/episode-cj01-cj30-clean-20261101.mp4` (39,085,468) + `-chat.mp4` (8,729,599) + `episode-audio-clean-20261101.wav` (PR #354) | Clean CJ-01→CJ-30 episode | **NO**; §13 |
| `episode-cj01-cj30-clean-20261101/DIALOGUE-LINE-SHEET-20261101.md` (255 lines added) | Dialogue line sheet with blanks | **NO** — verbatim dialogue document; the *blank line-sheet format* is YES |
| `episode-cj01-cj30-clean-20261101/EPISODE-CLEAN-REPORT-20261101.md` | Clean-up report (layer removal method) | **YES** (method) |
| `nosferatu-video5-20261101/build_video5.py` + `VIDEO5-REPORT-20261101.md` (8 entries) | Video 5 builder | Builder **YES** |
| `nosferatu-video5-20261101/video5-johnny-nosferatu-20261101.mp4` (37,695,725) | Video 5 output | **NO**; §13 |
| `placeholder-interaction-charlie-20261101/` (9 entries, PR #355) + `charlie-piece-placement-fix-20261101/` (18) + `charlie-piece-placement-fix-v3-1-20261101/` (16) + PR #356 Charlie v3/kick-master folders | CJ + Charlie (Smiling Friends donor placeholder) interaction: builders, SFX, placement fixes | Builders/placement method **YES**; Charlie/CJ media **NO** |
| `kick-elbow-fix-20261101/` (11 entries): `FULL-EXTENDED-FRONT-KICK-MASTER-APPROVED-20261101.md` + report | Approved front-kick master (technique: extended kick construction, elbow 90° rule from PR #357) | **YES** (technique/docs); media NO |
| `batch-a-head-turn-forward-kick-20261101/` (21, PR #350), `anatomy-fix-bundle-20261101/` (21, PR #343), `blender523-rig-fixed-20261101/` (17), `blender523-rig-refined-20261101/` (13), `arm-snap-last3-fix-20261101/` (14), `spinning-flexing-bust-front-insert-20261101/`, `rig-34-locked-neck-v4-cape-fix-20261101/` | Head-turn/kick/anatomy/rig-fix batches | Method/builders **YES**; CJ media **NO** |
| `monetization-systems-20261101/` (11 entries, PR #330): `README-20261101.md`, `clip-plan-template.csv`, conversation/monetization systems | Clip-plan + monetization system templates | **YES** (templates/systems) |
| `duplicate-review-ui-v2-20261031/` (13 entries): `build_data.py` + review UI + proof contacts | Duplicate-asset review UI | **YES** |
| `production-extensions-landing-prep-20261101/` (17, PR #358): `canonical-index.csv/.json`, `inventory.csv/.json`, `landing-manifest.md`, `rename-dedupe-map.csv/.json`, `pick-sheet.html` | Landing-prep indexing/dedupe system | **YES** (system); CJ pick images **NO** |
| `next-part-20261101/DIALOGUE-PASS-APPROVED-20261101.md` + `NICKELDEON-2024-VERIFY-20261101.md` (PR #358) | Dialogue pass + a donor verify note | **NO** (dialogue); verify method YES |
| `docs/story/EP01-IMMORTAL-QOMBAT-SHOOTING-SCRIPT.md` (24,973), `docs/story/EP01-M4-CUE-SHEET.md` (8,166), `docs/SHOW-BIBLE.md` (11,387), `docs/SHOW-BIBLE-SEED.md` (1,392) | CJ script/bible | **NO** — verbatim script + story. (Bible *structure* is a generic template, but do not copy content) |
| `stages/cape-house/`, `stages/jungle-outpost/`, `shared/cast/` | CJ stages/cast data | **NO** |
| `production/PILOT-NOTES.md` (1,892) | CJ pilot notes | **NO** |

---

## 11. Wiring / architecture / research docs (YES as a library)

| Path | Size | What it does | WG? |
|---|---|---|---|
| `docs/COMPLETE-PIPELINE.md` | 19,988 | End-to-end pipeline doc | **YES** |
| `docs/STUDIO-ARCHITECTURE.md` | 15,501 | Studio architecture | **YES** |
| `docs/AUTOMATION.md` | 5,780 | Automation map | **YES** |
| `docs/pipeline/EP1-RENDER-PIPELINE.md` | 16,370 | Render pipeline (detailed) | **YES** (scrub EP1 specifics) |
| `docs/pipeline/KAGGLE-GPU-SETUP.md` | 11,758 | Kaggle GPU setup | **YES** |
| `docs/pipeline/COLAB.md` | 7,699 | Colab route | **YES** |
| `docs/pipeline/2D-TO-3D-RULES.md` | 3,328 | 2D→3D rules | **YES** |
| `docs/production/MOVEMENT-GAP-RESEARCH.md` | 19,988 | Movement-gap research (why movements fail + fixes) | **YES** |
| `docs/production/CAPE-JONES-PRODUCTION-MODEL.md` | 7,536 | Production model | **MIXED** — model YES, CJ specifics NO |
| `docs/ASSET-INVENTORY.md` (4,208), `docs/HERO-FILES-CATALOG.md` (3,509), `docs/WIRING-STUBS.md` (1,280), `docs/ANIM-GATE.md` (839), `docs/CLOTH-COLLISION-2026-10-24.md` (11,793), `docs/RENDER-ORIENTATION.md` (3,509), `docs/KAGGLE-FIXES.md` (2,658), `docs/TOONCRAFTER-PATCH-V5.md` (1,180) | — | Catalogues, gates, cloth, orientation, ToonCrafter patch | **YES** |
| `docs/HANDOFF-CAPE-JONES-X-WESTERN-HEART.md` | 5,024 | Existing cross-show handoff doc (precedent for this CJ→WG handoff) | **YES** (as precedent/template) |
| `docs/research/` (~70 files) incl. `FULL-PRODUCTION-STACK.md` (10,867), `PIPELINE-SCALING-2026.md` (14,102), `TOONCRAFTER-FULL-STACK.md` (14,863), `BEST-RIGGING-TECH-2026.md` (22,089), `AUTO-RIGGING-TOOLS-2026.md` (16,076), `FREE-3D-TOOLS.md` (29,824), `AUDIO-VOICE-MUSIC-2026.md` (16,162), `TRACK-A…F-PULL.md` series, `RENDER-2026-OPTIMAL.md` (8,543), `WEIGHT-BAKEOFF-2026.md` (21,592) | — | The research library behind every pull-in | **YES** — transfer wholesale as reference |
| `cape-jones-rig/WIRED-PULLS-20261031.md` (19,400), `FREE-FIRST-WIRING.md` (10,358), `INDUSTRY-STANDARDS-PULL-20261031.md` (10,049), `METHODS-PULLED-20261031.md` (2,267), `FREE-STACKS-INDUSTRY-STANDARDS.md` (3,431) | — | What was pulled, from where, how wired | **YES** |
| `cape-jones-rig/wired-100-20261031/WIRED-INVENTORY-20261031.md` (11,957) + `build_wired.py` (9,546) + `build_tool_projects.py` (5,618) + `build_gap_closure.py` (8,464) + `build_extra.py` (5,833) | — | "Wired-100" inventory + builders (audio loudnorm −14 LUFS outputs incl.) | **YES** |
| `production/tools/*/CAPE-JONES-WIRING.md` pattern (verified in `glaxnimate/`, `natron/`, `freemocap/`) + `production/tools/rife/WIRING.md` (2,216) + `production/colab/gen_tooncrafter_colab.py` (14,330) + `gen_viggle_colab.py` (11,989) + `cape_jones_tooncrafter_colab.ipynb` (13,195) + `cape_jones_viggle_colab.ipynb` (10,679) | — | Per-tool wiring docs + Colab notebook generators (ToonCrafter, Viggle — Viggle is already WG Pipeline One) | **YES** (rename on copy) |
| `AGENTS.md` (14,507), `WORKING-METHOD.md` (316), `TEAM-CONVERSATION.md` (10,107), `.github/copilot-instructions.md` (2,374), `.github/workflows/cast-ci.yml` (1,979) | — | Repo working method + CI | **YES** (method/CI pattern) |
| `MARS-MAKING-MONEY-GOOD-EXPERIENCE-RULE-20261101.md` (862, PR #347) | — | Owner rule doc | **YES** (owner rule, show-agnostic) |

---

## 12. Kaggle / Colab compute lane

| Path | Size | What it does | WG? |
|---|---|---|---|
| `production/kaggle/rife/README.md` | 2,732 | RIFE-on-Kaggle (§6.2) | **YES** |
| `production/kaggle/tooncrafter/fp16_patch_cell_v5.py` | 1,425 | ToonCrafter FP16 patch cell | **YES** |
| `production/kaggle/tooncrafter/kernel-metadata.json` | 374 | Kaggle kernel metadata | **YES** |
| `production/kaggle/tooncrafter/re_push_tooncrafter.sh` | 1,101 | Re-push kernel script | **YES** |
| `production/colab/` (6 files, §11) + `notebooks/colab/` | — | Colab notebooks (lighting reel, ToonCrafter, Viggle) | **YES** (flows) |
| `production/pipeline/kaggle_queue.py` (33,089) + `compute/*` (§2.2) | — | Queue + compute routing (Kaggle / Lightning / SheepIt / Flamenco) | **YES** |

---

## 13. ⚠️ Big binaries that should live in RELEASES, not git

Everything below is **currently committed to git** on main. For the Wizard Gang transfer, **do not copy any of these into WG git** — move/keep them as GitHub Release assets (the pattern this repo already uses for archives, §14) or leave them behind entirely (all CJ-art ones are NO-transfer anyway).

### ≥ 20 MB in git (30 blobs in the tree payload, exact)
| Size (B) | Path |
|---|---|
| 97,148,658 | `production/tools/auto-seat/proof_sitting.blend` |
| 97,146,816 | `production/tools/auto-seat/proof_sitting.blend1` |
| 96,975,121 | `3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend` |
| 96,943,918 | `3d-assets/cape-jones-rig/sitting-redo/sitting_pose_library_fixed.blend` |
| 96,943,918 | `3d-assets/cape-jones-rig/sitting_pose_library.blend` |
| 96,903,454 | `3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle_cape_STEP1.blend` |
| 96,847,082 | `3d-assets/cape-jones-rig/.scratch/led_test.blend` |
| 96,835,930 | `3d-assets/cape-jones-rig/cape_jones_rigged_w5r_clean.blend` |
| 96,832,427 | `3d-assets/cape-jones-rig/.scratch/snap_test.blend` |
| 95,744,707 | `3d-assets/cape-jones-rig/cape_jones_rigged.blend` |
| 92,300,171 | `3d-assets/living_room.blend` |
| 92,125,095 | `3d-assets/cape-jones-rig/cape_jones_rigged_w5r.blend` |
| 87,225,003 | `3d-assets/face-rig/tools/rhubarb/Rhubarb-Lip-Sync-1.14.0-Linux.zip` |
| 51,278,610 | `production/tools/audio/musescore/share/sound/MS Basic.sf3` |
| 50,939,526 | `production/tools/LDF-VFI/metrics/fvd/i3d_pretrained_400.pt` |
| 39,085,468 | `episode-cj01-cj30-clean-20261101/episode-cj01-cj30-clean-20261101.mp4` |
| 37,695,725 | `nosferatu-video5-20261101/video5-johnny-nosferatu-20261101.mp4` |
| 36,522,400 | `cape-jones-rig/fla-piece-labelling-top5-20261031/ruffle` (a binary executable in git) |
| 33,543,073 | `cape-jones-rig/rig-34-locked-neck-v5-cape-fix-20261101/animation-lean/sit-lean-neck-v5-cape-fix-20261101.gif` |
| 33,364,189 | `cape-jones-rig/rig-34-locked-neck-v6-cape-collar-20261101/animation-lean/sit-lean-neck-v6-cape-collar-20261101.gif` |
| 28,548,173 | `dance-flash-fix-20261101/dance-test-FIXED-v2-JP-full-SFX-FASTSTART-20261101.mp4` |
| 28,546,238 | `dance-flash-fix-20261101/dance-test-FIXED-v2-EN-full-SFX-FASTSTART-20261101.mp4` |
| 26,840,791 | `dance-scene-2videos-20261101/dance-scene-V1-EN-FINAL-20261101.mp4` |
| 26,821,597 | `dance-scene-2videos-20261101/dance-scene-V2-JP-FINAL-20261101.mp4` |
| 26,424,747 | `cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/shafts-glare-blender.exr` |
| 26,424,747 | `cape-jones-rig/shafts-fix-100-20261031/methods/I4-glare-v4.exr` |
| 25,695,560 | `production/tools/audio/audacity/au3/tests/samples/FifeAndDrumsStereo.wav` |
| 23,712,790 | `production/tools/audio/musescore/share/sound/FluidR3Mono_GM.sf3` |
| 21,907,994 | `cape-jones-rig/anim-sit-locked-20261101/sit-lean-locked-20261101.gif` |
| 21,721,152 | `cape-jones-rig/rig-34-locked-default-sitting-neck-v2-20261101/animation-lean/sit-lean-neck-v2-20261101.gif` |

### Other release-worthy items in git
- `proof/sitting_mocap.blend` — 92,973,898 B.
- `toon-boom-linux-20261101/rocky9-container.tar.xz.part-00` / `.part-01` / `.part-02` (26,214,400 B each) + `.part-03` (7,561,996 B) — a container image chunked into git; textbook release asset.
- `production/tools/LDF-VFI/metrics/VFIPS/exp/eccv_ms_multiscale_v33/model.pytorch` — 18,435,575 B (model weights).
- `3d-assets/cape-jones-rig/idle-test/idle_frames.zip` — 19,840,331 B.
- `cape-jones-rig/parts-catalogue-20261031/index.html` — 14,467,076 B (a single HTML catalogue).
- Hundreds of 5–20 MB proof GIFs/MP4s across `cape-jones-rig/` (e.g. the `ghoul-shuffle-*`, `dance-inbetween-*`, `rig-34-*` animation GIFs at 9–17 MB each) — individually under the line, collectively the reason `cape-jones-rig/` carries multiple GB.
- Vendored upstream trees (`production/tools/audio/` 813 MB, `comfyui/`, `natron/`, `pencil2d/`, `alicevision/`, `colmap/`…) — for WG, pin + re-pull upstream; never vendor-copy.

## 14. Releases already on `mhvnsnt/cape-jones` (30 tags, verified)

The repo already keeps big archives release-side — this is the correct destination pattern for §13. Tags (newest first): `cape-jones-worktree-archive-2026-10-30`, `preserve-mpfb-wired-rig-20261030`, `fullstack-sit-tests-20261029`, `3d-scenes-20261029`, `ep01-full-video-20261025`, `ep01-final-v2-20261024`, `cape-3d-work-20261024`, `sitting-saga-intermediates-20261023`, `sitting-final-20261023`, `recliner-mech-20261023`, `ep01-final-20261023`, `cape-bake-20261023`, `viggle-inputs-mirror-20261021-p2`, `viggle-inputs-mirror-20261021`, `viggle-inputs-archive-20261020`, `sitting-wt-sitcanon-20261019`, `sitting-wt-mocapsit-20261019`, `sitting-wt-autoseat-20261019`, `sitcanon-anim-placed-20261020`, `star-rig-work-archive-20261019`, `snapshot-cj-pose-stage-20261019b`, `sitcanon-work-archive-20261019`, `rig-scratch-archive-20261019`, `disk-cleanup-beatB-meshrepair-scratch-20261019b`, `disk-cleanup-beatA-20261019`, `cj-archives-20261018`, `cape-jones-episode-cuts-20261019`, `rig-deform-fix-20261018`, `mpfb-wired-20261017`, `weight-bakeoff-20261017`. Asset style: 100 MB / 250 MB / 500 MB split parts (`.part-00`, `.100m-aa`, `.part-000`…) + `SHA256SUMS-*.txt`. Notable: `sitcanon-anim-placed-20261020` also carries small reusable scripts (`sitcanon_retarget.py` 10,132 B, `render_front.py` 893 B, `render_proof.py` 1,325 B) alongside its ~160 MB blends. **Verdict: release *pattern* YES; CJ release contents NO.**

---

## 15. Transfer shortlist — what a Wizard Gang lane should take first

1. **Pipeline core:** all of `production/pipeline/` (§2) + `docs/COMPLETE-PIPELINE.md` + `docs/STUDIO-ARCHITECTURE.md` + `production/pipeline/ANIMATION-PIPELINE-2026.md`.
2. **Post chain:** FlipaClip post (§6.1) + RIFE Kaggle route (§6.2) + `grades.py` / `render_looks.py` / `finish.py`.
3. **Flash safety:** `dance-flash-fix-20261101/flash_check.py` + the `.flash.csv/.flash.json` convention + the beat-sync re-time rule (§4.5).
4. **Movement system:** `movement-library-clips-20261101/build_clips.py` + `TEMPLATE-CHARACTER-WORKFLOW-20261101.md` + `MOVEMENT-LIBRARY-20261101.md`; preset system `movement-dance-presets-20261101/build_clean.py` + `PRESET-INDEX-20261101.md`; choreo schema `production/dance-choreo/dance-gumball-darwin-words-sc057-sc059.json` (timing only, re-labelled).
5. **Piece-rig system:** `cape-jones-rig/joint_locked_rig_v7c.py` lineage, spine/joint-lock JSON schemas, `slice_clean.py`, `assemble_tpose_default.py`, side/back pack builders + manifests (§9.1), arm-snap + knee-feet + head-turn rules.
6. **FLA tooling:** JSFL builders (technique), FLA piece-labelling tools 1–5 (§7), donor-pull method (`donor-fla-rig-pull-20261101/build.py` + `check_template_gate.py` + inventory schema) — remembering §5: **no donor binaries exist in this repo to copy**.
7. **Lighting:** §6.3 docs + `led_controller.py` / `led_scene_assembler.py` + figure-matched preset system (builders/index format) + lighting-levels appliers.
8. **Wiring library:** every `*WIRING*.md` in `production/tools/` + `docs/research/` wholesale (§11) — then re-pull the open-source tools into WG at pinned versions instead of copying vendored trees.
9. **Process gates:** claim/verify gates (§2.5), learning/honesty gates (§9.1), 12-principles checklist, dated-batch-with-builder+report+proof folder pattern (§1).

**Explicitly NOT transferring:** Cape Jones character art/pieces/sheets/rigs (2D and 3D), CJ names/logos, EP01 script/bible/dialogue line sheets, all episode/dance/scene output MP4s as content, CJ voice/audio, CJ stages, donor-show character art and names (Gumball/Foster's/Smiling Friends/Scooby-Doo/Johnny Bravo/Rick and Morty/Nick), and every §13 binary as a git copy.

## 16. Method / sources

- `gh repo view mhvnsnt/cape-jones`, `gh api repos/mhvnsnt/cape-jones/git/trees/main?recursive=1` → `~/workspace/agent-ops/cjwg-cape-tree.json` (53,436 entries, `truncated: true`, HEAD sha above).
- Contents-API listings for: repo root, `production/tools/`, `tools/`, `shared/`, `stages/`, `proof/`, `notebooks/`, `toon-boom-linux-20261101/`, `top5-software-20261101/`, `wire-up-cannot-do-20261101/`, `unknown-archive-listing-20261101/`, `side-rig-auto-20261101/`, `side-pack-new-20261101/`, and `production/tools/{lipsync,opentoonz,synfig,tahomad2d,pencil2d,glaxnimate,natron,freemocap,mocap,mocap-retarget}/`; subtree tree for `production/tools/rife/`.
- `gh pr list --state all` + per-PR file lists for #337, #340, #341, #342, #345, #353, #354, #355.
- Raw-content reads of: `production/pipeline/FLIPACLIP-POST-PIPELINE.md`, `production/pipeline/ANIMATION-PIPELINE-2026.md`, `movement-dance-presets-20261101/PRESET-INDEX-20261101.md`, `donor-fla-rig-pull-20261101/DONOR-FLA-RIG-PULL-REPORT-20261101.md`, `production/dance-choreo/README.md` + `INVENTORY.md`, `production/kaggle/rife/README.md`, `movement-library-clips-20261101/TEMPLATE-CHARACTER-WORKFLOW-20261101.md`, `beatsync-presets-20261101/BEATSYNC-PRESETS-20261101.md`.
- No clone was made. No path in this file was invented: every path is copied from an API response above; areas only verified at directory level are labelled as such.
