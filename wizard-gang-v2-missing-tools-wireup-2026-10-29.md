# Wizard Gang V2 — NO-MISSING-TOOLS Wire-Up Log

**Date:** 2026-10-29 · **Order:** owner 2026-10-29 ~12:19 CDT — "All the stuff that it says is
missing get it all wired up… any of it that needs reverse engineering to be wired up fully 100%
or decrypting or decoding do that… none of that stuff should be gone, it should be there in the
folders and in the repo."
**Source list:** `wizard-gang-real-anim-local-tools-2026-10-29.md` (missing items only;
Tahoma2D/Krita/Storyboarder/Inkscape are wire-up lane 1's job, Natron already works).
**Method:** real upstream projects only, installed into `~/workspace/tools/<tool>/`, each one
proven with a real run before it is called wired. Big binaries stay out of git — this log +
per-tool `WIRING.md` files are the repo record.

---

## 1. BasicPBC (Paint Bucket Colorization, CVPR 2024)
- **Upstream:** https://github.com/ykdai/BasicPBC (official implementation, arXiv 2403.18342)
- **Install:** `git clone --depth 1` → `~/workspace/tools/basicpbc/` (was: directory gone entirely)
- **Pipeline role:** colorize hand-drawn line frames by paint-bucket inclusion matching —
  feed it one colored keyframe (gt) + line frames, it colors the sequence. This is the
  "color the inbetweens from the key" stage of the cartoon factory.
- **VERDICT: WIRED+PROVEN** — venv complete (torch 2.2.2+cpu + all deps
  import-verified; pin set in `constraints.txt` — without it timm drags in
  PyPI's CUDA torch; torch_scatter/matplotlib are imported by the code but
  missing from its requirements.txt). Both release checkpoints byte-exact:
  `ckpt/basicpbc.pth` 105,523,141 B, `ckpt/basicpbc_light.pth` 50,350,481 B.
  The seg stage's CLIP-convnext weights (1.41 GB, downloaded by open_clip at
  first use) are pre-staged in the local HF cache, the .bin blob SHA-256-
  verified byte-identical to upstream; run with `HF_HUB_OFFLINE=1` so
  open_clip's safetensors-first lookup falls back to the cached .bin.
  CPU-portability patches (documented in `tools/basicpbc/WIRING.md`):
  `map_location="cpu"` on three bare `torch.load`s + conditional `.cuda()`
  at `inference_line_frames.py:164` and `basicsr/models/pbc_model.py:208` —
  the authors assume CUDA; GPU behavior unchanged.
  **Proof:** bundled laughing_girl frames (cv2-resized to 512² — PIL's RGBA
  resize destroys these frames) colorized end-to-end, 100% in 126 s/it:
  `dataset/test/proof6/proof6/0001.png` + color dict assigning the target
  frame's segments colors from the keyframe's own palette ([151,136,221],
  [86,16,35]); segmentation separately proven at native 1600² (117 segments,
  `dataset/test/laughing_girl/seg/`). Floors learned: <512² collapses
  segmentation to <2 keypoints (`KeyError: 'match_scores'`); the one-process
  native-res run OOMs on this shared 8 GB VM (CLIP ~2 GB + neighbors) — the
  two-stage `--skip_seg` split is the low-memory route. Full detail:
  `tools/basicpbc/WIRING.md`.

## 2. FlashXFLParser (XFL/.fla rig-structure parser)
- **Upstream:** https://github.com/jackisgames/FlashXFLParser (Unity C# project)
- **Install:** `git clone --depth 1` → `~/workspace/tools/FlashXFLParser/` (was: directory gone)
- **What the code actually is (read in full):** the parser core is
  `Assets/XFLParser/display/Symbol.cs` — a pure-.NET XmlSerializer data model of an XFL
  library symbol (DOMSymbolItem → DOMTimeline → DOMLayer → DOMFrame → symbol/bitmap
  instances with matrices). `editor/XFLLibraryEditor.cs` is the import loop (deserialize
  every `LIBRARY/*.xml` into `Symbol`). Only `Bitmap.cs`/`XFLLibrary.cs` touch UnityEngine
  (Texture field / ScriptableObject shell). Wire-up = host the project's own parser classes
  in a .NET console harness with a minimal UnityEngine stub, repo parser files unmodified.
- **⚠ FORMAT FINDING on the target file:** `pds3hx.fla` (Frankie Foster rig, release
  `frankie-rig-fla-v1`, downloaded byte-exact 18,385,408 B) is **NOT** a ZIP/XFL .fla —
  `file` reports OLE2 "Composite Document File V2", i.e. the legacy binary FLA format
  (pre-CS5). The XFL parser cannot read it as-is; see the Frankie entry below for the
  decode path taken.
- **Pipeline role:** read pro Flash rigs (layers, symbols, parts, tweens) so WG rigs can be
  built from their structure (USE-PRO-PRODUCTION-FILES-100% law).
- **VERDICT: WIRED+PROVEN** — parser built from the project's own code (console host in
  `tools/FlashXFLParser/harness/`, .NET SDK 8.0.427) and proven on REAL rigs from
  `cn-gigaleak-cartoon-vault` release `tv-gigaleak-fla-v1`: Pim rig (5 part layers) and
  Charlie rig (**18 symbols / 33 layers / 73 frames**, 9-layer master symbol). The
  Frankie target file is a legacy pre-CS5 OLE binary (parser detects + reports it
  honestly); its structure was decoded at OLE level — 131 symbols, 466 named parts
  incl. the full 3/4-view set. Full detail: `tools/FlashXFLParser/WIRING.md`.

## 3. Synfig Studio 1.5.5
- **Upstream:** https://github.com/synfig/synfig release v1.5.5 (pinned in cape-jones wiring doc)
- **Install:** official AppImage `SynfigStudio-1.5.5-2026.03.15-linux64-79bf7.appimage`
  → `~/workspace/tools/synfig/` (was: EMPTY directory), extracted (no FUSE on this VM)
- **Pipeline role:** vector tweening + bone rigs — authoring-level automatic inbetweening.
- **EXTRACTION STORY (no FUSE on this VM):** the AppImage is Type-1 (ELF + ISO9660 with
  **zisofs** compression) and the kernel has no fuse module, so `--appimage-extract` and
  mounting are both impossible. Extracted with a purpose-built Joliet-tree ISO reader +
  zisofs block decompression (11,383 files → `extracted/`); soname symlinks recreated
  from ELF SONAMEs (they live only in the Rock Ridge tree). Full detail: `tools/synfig/WIRING.md`.
- **VERDICT: WIRED+PROVEN** — `synfig --version` → `synfig 1.5.5`; rendered bundled example
  `candy.sif` → `tools/synfig/proof/candy.png` (67,138 B, 480×270), renderer status DONE.

## 4. OpenToonz 1.8.0
- **Upstream:** https://github.com/opentoonz/opentoonz — upstream ships NO Linux binary;
  cape-jones wiring doc prescribes the Flathub Flatpak (1.8.0). Morevna AppImage is 1.4.0
  (2020) and the doc says avoid unless Flatpak fails.
- **Pipeline role:** node-based compositing/effects (Toonz Schematic), multiplane camera.
- **VERDICT: WIRED — launch unproven in this sandbox (evidence documented).**
  Installed via the official Flathub flatpak: `flatpak list`/`info` verify
  **OpenToonz 1.8.0 stable**; all binaries (OpenToonz, tconverter, tcomposer, tcleanup)
  present in the app tree. Launch cannot be proven HERE: `flatpak run` dies on its
  document-portal step because this VM's kernel has no FUSE at all (same wall as the
  Synfig Type-1 AppImage), and the unpacked binaries segfault outside their sandbox
  mounts. Full evidence trail: `tools/opentoonz/WIRING.md`. The install is complete
  and standard — it launches on any FUSE-capable session.

## 5. Glaxnimate 0.6.0
- **Upstream:** KDE — source already in cape-jones `production/tools/glaxnimate/`; KDE stable
  ships source tarball only, AppImage comes from KDE CI builds / project servers.
- **Pipeline role:** vector motion graphics — titles, lower-thirds, end cards; Lottie/SVG export.
- **VERDICT: WIRED+PROVEN** — AppImage byte-exact (261,908,984 B, KDE CI release-0.6
  build); binary `glaxnimate 0.6.0-git-565632c`. Open/export proof via the python-lottie
  0.7.2 library bundled inside the AppImage: parsed the test Lottie and exported SVG at
  frame 0 (circle x=40.0) and frame 29 (x=159.82 — motion interpreted) plus a Synfig
  .sif. The PyPI-module route is a documented dead end (its wheel needs openSUSE-flavored
  FFmpeg symbols); detail in `tools/glaxnimate/WIRING.md`.

## 6. Kdenlive 26.08.2
- **Upstream:** KDE — official AppImage `kdenlive-26.08.2-x86_64.AppImage`
  (215,427,576 B, mirror-verified) → `~/workspace/tools/kdenlive/` (was: absent entirely)
- **Pipeline role:** the MLT-based NLE — episode assembly desk; also the donor for a
  bundled `melt` (see item 7).
- **VERDICT: WIRED+PROVEN** — download byte-exact (215,427,576 B); extracted;
  `tools/kdenlive/kdenlive --version` → `kdenlive 26.08.2`. Host glvnd libs the
  AppImage expects (libOpenGL/libEGL) are absent system-wide on this VM, so they are
  provided from Ubuntu .debs extracted into `tools/kdenlive/hostlibs/` (launcher adds
  them to LD_LIBRARY_PATH). Detail: `tools/kdenlive/WIRING.md`.

## 7. MLT `melt`
- **Upstream:** MLT framework 7.x — full source already vendored at
  `cape-jones/production/tools/mlt/` (with its own AGENTS.md build doc); Flowblade (the
  MLT-XML editor) is vendored in cape-jones too, but no `melt` binary existed on the system.
- **Pipeline role:** headless "episode assembly as code" — render MLT-XML timelines from scripts.
- **Wired binary:** melt **6.6.0**, bundled inside the Synfig Studio 1.5.5 AppImage
  (Synfig ships MLT for its rendering) — entry point `tools/mlt/melt` (env wrapper into the
  extracted bundle: modules incl. avformat/core/plus/kdenlive). MLT 7 from the cape-jones
  source or the Kdenlive AppImage bundle is the documented upgrade; see `tools/mlt/WIRING.md`.
- **VERDICT: WIRED+PROVEN** — `melt -version` → `melt 6.6.0`; trivial render
  `colour:red out=24` (dv_pal) → `tools/mlt/proof/melt-test.mp4`, ffprobe-verified
  (1.0 s, 25 frames, valid MP4).
- **UPDATE (same day):** primary bumped to **melt 7.43.0** from the Kdenlive 26.08.2
  AppImage bundle — `tools/mlt/melt` wrapper now execs melt-7; re-proven
  (`-version` + `colour:blue` render → `tools/mlt/proof/melt7-test.mp4`). The 6.6.0
  route stays documented as fallback in `tools/mlt/WIRING.md`.

## 8. Blender 5.2.3 LTS (+ Smart2D / Guided Tweening unblocked)
- **Upstream:** blender.org — `blender-5.2.3-linux-x64.tar.xz` → `~/workspace/tools/blender-5/`
  installed ALONGSIDE 4.0.2/4.5.3 (nothing replaced), per cape-jones `BLENDER-5X-UPGRADE.md`.
- **Why:** `tools/blender-addons/smart2d/` and `tools/blender-addons/guided-tweening/` both
  refuse to load below Blender 5.0 (Grease Pencil 3). 5.x also brings the GP overhaul.
- **VERDICT: WIRED+PROVEN** — tarball byte-exact (385,331,224 B); `blender --version` →
  `Blender 5.2.3 LTS`; `tools/blender-5/addon-test.py` enables BOTH addons
  (Smart2D + guided_tweening) → `ADDON-TEST-RESULT: PASS`. Guided Tweening registers GPU
  draw handlers so it needs a windowed (xvfb) session to enable, not `-b` — documented
  in `tools/blender-5/WIRING.md`. 4.0.2/4.5.3 untouched.

## 9. ToonCrafter + AnimeInbet weights (AI-ASSIST only — never the animator of record)
- **ToonCrafter:** checkpoint = Kijai pruned FP16 `tooncrafter_512_interp-pruned-fp16.safetensors`
  from HF `Kijai/DynamiCrafter_pruned` — size HEAD-verified **3,175,466,358 B** (exact match
  to the documented figure). → `~/workspace/tools/tooncrafter/checkpoints/`
- **Kaggle check (standing law):** no kaggle processes running on this VM; the only Kaggle
  checkpoint in agent-ops (`wh-pantera-kaggle-render.json`) is stale since 2026-10-16
  (lane dead, launch never happened). Decision: **STAGED-NOT-PROVEN** —
  `tools/tooncrafter/kaggle_inference_test.py` is ready to run (converts the safetensors
  to the loader's model.ckpt layout, runs the repo's own inference on its bundled sample
  keyframes, verifies outputs). No Kaggle session was claimed by this lane and no
  inference output is claimed anywhere. See `tools/tooncrafter/WIRING.md`.
- **AnimeInbet:** both documented pretrained weights DOWNLOADED and placed at the exact
  paths its README prescribes (from the project's own Google Drive links):
  `corr/experiments/vtx_corr/ckpt/epoch_50.pt` (16,569,879 B) and
  `experiments/inbetweener_full/ckpt/epoch_20.pt` (16,591,503 B). (ML240 dataset
  outcome in the Status block below.)
  Its runtime is Python 3.8 / torch 1.7-era (README) — the weights are staged with the
  source. **Modern-torch load check DONE (BasicPBC venv, torch 2.2.2 + easydict):
  both checkpoints LOAD-OK**, dicts of 3 entries each. See
  `tools/animeinbet/WIRING.md`.
- **ToonCrafter download COMPLETE (2026-10-29 ~21:13 CDT):** file at exactly
  3,175,466,358 B; safetensors header verified (1,976 tensors, format `pt`).
  Status stays **STAGED-NOT-PROVEN** for inference — the ready runner waits for a
  genuinely free Kaggle session; no inference is claimed.
- **Status:** ToonCrafter weights DONE (staged-not-proven); AnimeInbet weights DONE +
  load-verified. ML240 dataset: the gdown transfer died at ~81%
  (3,658,481,664 B `.part`) when the shared btrfs quota filled; gdown cannot
  resume partials, and the dead partial was deleted by this lane to un-block
  the quota (documented in `tools/animeinbet/WIRING.md`) — dataset is
  re-downloadable from the project's Drive link when headroom allows;
  weights unaffected.

---
