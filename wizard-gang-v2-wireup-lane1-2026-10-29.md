# Wizard Gang REAL-ANIMATION V2 — Wire-up Lane 1 Report

**Date:** 2026-10-29 · **Lane:** wire-up lane 1 (owner order 2026-10-29) · **Inputs:** `wizard-gang-real-anim-repo-audit-2026-10-29.md` + `wizard-gang-real-anim-local-tools-2026-10-29.md` (both read first, paths/versions taken from them)
**Scope done:** JOB 1 install the V2 install base from `mhvnsnt/vendor-tools` release `vendor-tools-v1`; JOB 2 inventory the Wizard Gang puppet cast in God-Molecule-Show-Studio. **Nothing pushed or merged. GMSS main not modified** (read-only sparse clone). Natron 2.5.0 NOT reinstalled (already local; re-verified only).
**Download discipline:** all four release assets were pulled with `gh release download` in one detached, logged sequence (`~/workspace/agent-ops/wg-v2-download.log`); no in-progress download was ever killed. Every asset's SHA256 was compared **programmatically** against the release API digest — **all 4 MATCH**.

---

## JOB 1 — Installed tools (verified version output)

Disk before: ~61 GB free. Disk after: **54 GB free** (`/dev/mapper/rv 150G, 65% used`). Footprints: tahoma2d 1.3 G, krita 1.5 G, storyboarder 557 M, inkscape 226 M (extracted trees included — these are tools in active use, local install is correct per store-and-work-off-disk).

### 1. Tahoma2D 1.6.3 — ✅ WORKS (GUI + headless CLIs)
- Downloaded: `~/workspace/tools/tahoma2d/Tahoma2D-1.6.3-linux-clang.tar.gz` — 328,382,822 B, sha256 `6ca474922bfb86cf601b5c0e484461a5b7122000ced96a107a413abbb9cf1561` == release digest.
- Extracted: `~/workspace/tools/tahoma2d/Tahoma2D/` (436 MB, 1,626 files: `Tahoma2D.AppImage`, `tahomastuff/`, bundled `rhubarb/`, bundled `ffmpeg/`) + AppImage extracted to `Tahoma2D/squashfs-root/` (binaries in `squashfs-root/usr/bin/`: `Tahoma2D`, `tahoma2d`, `tconverter`, `tcomposer`, `tcleanup`, `tfarmcontroller`, `tfarmserver`, `lzocompress`, `lzodecompress`).
- **Verified output:** `Tahoma2D  v1.6.3` (from `Tahoma2D -version`; note single-dash flags — `--version` prints usage). `tconverter` and `tcomposer` both execute headless under Xvfb and print their usage (tcomposer = the headless scene renderer for the episode lane).
- Bundled Rhubarb verified: `Rhubarb Lip Sync version 1.13.0` (`Tahoma2D/rhubarb/rhubarb`) — older than the standalone local Rhubarb 1.14.0, but present and runnable.
- **Launch gotchas (baked into wrappers, below):** (a) the AppImage bundles **no libOpenGL.so.0** — host has none either; borrow Natron's copy via `LD_LIBRARY_PATH=…:~/workspace/tools/natron`. (b) `/tmp` is a 512 MB tmpfs that sat at 100% — `APPIMAGE_EXTRACT_AND_RUN=1` truncated `libturbojpeg.so.0` to 0 bytes there and the AppImage failed with "file too short"; run from the extracted `squashfs-root` on workspace disk instead.
- Wrappers: `~/workspace/tools/tahoma2d/run-tahoma2d.sh` (GUI, Xvfb) and `run-tcomposer.sh` (headless render). Wrapper re-verified end-to-end: prints `Tahoma2D  v1.6.3`.

### 2. Krita 6.0.4 — ✅ WORKS (reactivates the 3 orphaned Krita plugins)
- Downloaded: `~/workspace/tools/krita/krita-6.0.4-x86_64.AppImage` — 385,731,064 B, sha256 `4ec9a45892308134b0ff5410f30aa9e68ae58d0dae5fb122666cfd27dfd6de9f` == release digest. Extracted to `~/workspace/tools/krita/squashfs-root/` (1.1 GB; `usr/bin/krita`, `kritarunner`, bundled ffmpeg/ffprobe).
- **Verified output:** `krita 6.0.4 (git 57db7cd)` (from `krita --version` under `xvfb-run -a`; Qt initialized, GLX context enabled).
- **Launch gotcha:** host has no `libEGL.so.1` — supply it from the existing stack: `LD_LIBRARY_PATH=<krita>/usr/lib:~/workspace/tools/egl-stack/usr/lib/x86_64-linux-gnu:~/workspace/tools/natron`. Baked into wrapper `~/workspace/tools/krita/run-krita.sh`.
- Side effect: the host app now exists again for `tools/krita-ai-diffusion/`, `tools/krita-batch-exporter/`, `tools/krita-spritesheet-generator/` and the COA Tools 2 Krita exporter (plugin install itself not done in this lane).

### 3. Storyboarder 2.1.0 — ✅ LAUNCHES (Electron GUI app)
- Downloaded: `~/workspace/tools/storyboarder/Storyboarder-2.1.0-linux-x86_64.AppImage` — 130,041,205 B, sha256 `aa068c49665ba72a9177351a3bf1c1ed15262c0481854f462cf4e556767b8b32` == release digest. Extracted to `~/workspace/tools/storyboarder/squashfs-root/` (`storyboarder` Electron binary + `resources/app.asar`).
- **Verified:** binary launches under `xvfb-run -a` with `--no-sandbox` and stays up (it ignores `--version`/`--help` and boots the app — first-run log: "Loading preferences from /home/hatch/.config/Storyboarder/pref.json … Could not read prefs. Loading defaults." — the ENOENT is the normal first-run path). Version confirmed from its desktop entry: `X-AppImage-Version=2.1.0`, Name=Storyboarder, "The fastest way to storyboard."
- **Launch gotcha:** needs `libXtst.so.6`, which ships in its own `squashfs-root/usr/lib` — put that on `LD_LIBRARY_PATH`. Wrapper: `~/workspace/tools/storyboarder/run-storyboarder.sh`.

### 4. Inkscape 1.4.4 — ⚠️ DOWNLOADED + VERIFIED, BINARY BLOCKED on this VM's library set
- Downloaded: `~/workspace/tools/inkscape/inkscape_1.4.4-ubuntu22.04_amd64.deb` — 26,529,444 B, sha256 `87b35e53f87ee6e6dadd7e023b9bafcb0f53703fc994bc8746cab8f799b36454` == release digest. Package metadata verified: `Package: inkscape, Version: 1:1.4.4+202605061432+dcaf3e7d9e~ubuntu22.04.1, Architecture: amd64`.
- Extracted (no system install — apt is broken on this VM, see TOOLS.md): `~/workspace/tools/inkscape/extracted/` (`usr/bin/inkscape`, `inkview`; bundles only lib2geom + its own libs).
- **Blocker, exact:** `inkscape --version` cannot start — **21 shared libraries "not found"** per `ldd`, all Ubuntu 22.04 desktop libs the .deb expects from the host: libgiomm-2.4, libglibmm-2.4, libgtkmm-3.0, libgdkmm-3.0, libatkmm-1.6, libpangomm-1.4, libcairomm-1.0, libsigc-2.0, libboost_filesystem.so.1.74.0, libgsl.so.27, libgc.so.1, libpoppler.so.118, libpoppler-glib.so.8, libpotrace.so.0, libgspell-1.so.2, libgtksourceview-4.so.0, libMagick++-6.Q16.so.8, libdouble-conversion.so.3 (+ repeats). Borrowing the GTKmm stack from the (parallel-lane) Synfig extraction resolved the *mm family but the version-pinned libs (boost 1.74, poppler 118, gsl 27…) have no on-box source. **Fix path for a later lane:** install the .deb where its 22.04 dependency closure exists, or pull the dependency .debs into `tools/inkscape/extracted` the same way. The asset itself is intact and correct — do not re-download.

### 5. Natron 2.5.0 — ✅ already local, NOT reinstalled, re-verified
- `~/workspace/tools/natron/Natron-2.5.0-Linux-x86_64-no-installer/bin/NatronRenderer` with its own libdir on the path prints: `Natron version 2.5 at commit 53ee17e34438005425230468916ff223cfd8a403 on branch tags/v2.5.0` (the `natron-render.sh` wrapper in the same folder does this env fix).

---

## JOB 2 — Puppet cast inventory (God-Molecule-Show-Studio)

**Checkout:** blobless sparse clone at `~/workspace/_wg-v2-wireup/gmss/` (main, read-only), sparse set `tools/puppet tools/animation tools/character`. Puppet tree on disk: **611 files, 247 MB** — 425 PNG, 95 PY, 39 JSON, 21 NPY, **18 .inp**, 11 MD. Matches the audit census (611 blobs / 257 MB on main).
**Root docs:** `RIG_PROOF.md` + `RIG_PROOF_WAVE5–WAVE11.md` + `SETUP_WIZARD_WAVE7/9.md` (11 waves of rig-proof iteration) + `setup-wizard-fix/` (nijigenerate editor-GUI fix attempt, with screenshots).

### Cast table — all 9 characters × standard + battle = 18 puppets

Counts are measured, not quoted: parts = numbered PNGs in `parts/` (excl. `_`-prefixed work files: masks/composites); rig layers = PNGs in `rig_layers/` (includes eye-closed + mouth swap layers); params = entries in `proofs/rig_parameters.json` (== params parsed out of the .inp); textures/animations/physics = parsed out of the .inp binary itself. Every puppet has 9 nodes and 2 physics rigs.

| Puppet | .inp file | .inp bytes | Params | Animations in .inp | Textures in .inp | Part PNGs | Rig-layer PNGs | Pose proofs |
|---|---|---|---|---|---|---|---|---|---|
| Ashes | `ashes/Ashes.inp` | 1,919,651 | **24** | 18 | 15 | 10 | 13 | 6 |
| Ashes Battle | `ashes-battle/AshesBattle.inp` | 1,631,048 | 21 | 18 | 13 | 10 | 12 | 5 |
| Cipher | `cipher/Cipher.inp` | 1,709,526 | 16 | 13 | 11 | 8 | 9 | 4 |
| Cipher Battle | `cipher-battle/CipherBattle.inp` | 1,336,988 | 14 | 13 | 9 | 6 | 8 | 4 |
| Echo | `echo/Echo.inp` | 1,545,719 | 16 | 13 | 11 | 8 | 9 | 3 |
| Echo Battle | `echo-battle/EchoBattle.inp` | 1,222,755 | 14 | 13 | 10 | 10 | 9 | 4 |
| Hollow | `hollow/Hollow.inp` | 1,574,288 | 12 | 11 | 9 | 8 | 9 | 4 |
| Hollow Battle | `hollow-battle/HollowBattle.inp` | 1,094,846 | 11 | 11 | 6 | 4 | 6 | 4 |
| Kiko | `kiko/Kiko.inp` | 3,862,859 | 18 | 10 | 9 | 8 | 7 | 2 |
| Kiko Battle | `kiko-battle/KikoBattle.inp` | 1,436,407 | 14 | 13 | 9 | 6 | 8 | 4 |
| Onyx | `onyx/Onyx.inp` | 1,835,870 | 18 | 13 | 12 | 16 | 10 | 3 |
| Onyx Battle | `onyx-battle/OnyxBattle.inp` | 1,225,437 | 14 | 13 | 9 | 6 | 8 | 4 |
| Sombra Negra | `sombra/Sombra.inp` | 1,110,313 | 12 | 11 | 7 | 6 | 7 | 4 |
| Sombra Battle | `sombra-battle/SombraBattle.inp` | 1,128,244 | 12 | 11 | 7 | 5 | 7 | 4 |
| Static | `static/Static.inp` | 1,486,096 | 16 | 13 | 11 | 8 | 9 | 4 |
| Static Battle | `static-battle/StaticBattle.inp` | 1,429,150 | 14 | 13 | 9 | 6 | 8 | 4 |
| Theory | `theory/Theory.inp` | 1,481,099 | 16 | 13 | 11 | 8 | 9 | 4 |
| Theory Battle | `theory-battle/TheoryBattle.inp` | 1,318,734 | 14 | 13 | 9 | 6 | 8 | 4 |

Per-character folder contents (uniform across all 18): `<Name>.inp`, `<name>_crop_source.png` (the group-shot crop the parts were cut from), `parts/` (numbered part PNGs + `parts_manifest.json` with per-layer pixels/bbox + `_figmask.npy`/`_clean_bgr.npy` work files), `rig_layers/` (stack-ordered layers incl. `eye_closed_l/r` and, for Ashes, `09_mouth.png` + `9_mouth_cavity.png`), `proofs/` (pose renders: neutral / head-turn / blink / comparison + `rig_parameters.json`), and the scripts `extract_parts.py`, `cut_parts.py`, `build_rig.py`, `render_poses.py`, `validate_inp.py`.

**Parameter shape:** standard Live2D-style set — EyeLOpen/ROpen + EyeLSmile/RSmile (blink/smile), AngleX/Y/Z (head), BodyAngleX/Y/Z, ArmLA/LB + ArmRA/RB, Breath, Acc0 (accessory), HairSide* (hair/braid sway, Ashes has 6). **Only Ashes (both variants) has mouth parameters** — `ParamMouthOpenY` + `ParamMouthForm` — because only Ashes has a mouth (the gold grill); the other 8 are void faces, consistent with the MOUTH-SET work. **Weakest rigs:** Kiko standard (18 params but NO eye or mouth params at all — Angle/Hair/Body/Arms/Breath only; only 7 rig layers, no eye-closed layers, only 2 proofs, no blink) and Hollow Battle (11 params, 4 parts, 6 textures). **Richest:** Ashes standard (24 params, 15 textures, 18 animations, mouth + grill).

### Validation — validate_inp.py
- **As shipped, every `validate_inp.py` FAILS** — each hardcodes the dead path `/home/hatch/workspace/god-molecule-studio/tools/puppet/wizard-rig-proof/<char>/<Name>.inp` (old checkout name). One-line path fix needed per file; GMSS was NOT modified by this lane.
- **With only the path corrected** (copies run from /tmp): **all 18 puppets PASS** — each prints `…INP STRUCTURALLY VALID`: magic `TRNSRTS\0` OK, JSON payload parses (meta/nodes/param/physics present), every parameter has node bindings, `TEX_SECT` present, and **every texture blob in every .inp decodes as an image** (counts in the table above). An independent parse by this lane (struct + PIL) reproduced the same node/param/physics/animation/texture counts.

### Formats — what opens what
| Format | What it is | Opens in |
|---|---|---|
| `.inp` (18) | **nijilive puppet** (Inochi2D-family serialization; built headlessly by `build_rig.py` via the image2live2d toolchain, Apache-2.0) | **nijigenerate / nijilive** editor + Inochi2D runtimes. NOT a DragonBones or Blender format. Honest caveat from `RIG_PROOF.md` itself: no .inp has ever been opened in the nijigenerate GUI — headless GUI automation hit the first-run setup wizard (synthetic clicks don't register; the `setup-wizard-fix/` folder documents the fix attempt). Structural validity is proven; editor-open is not. |
| PNG part packs + `rig_layers/` (425 PNGs) | The universal asset — cut, stacked, swap-ready (eye-closed, mouth) | Krita 6.0.4 (installed above), Tahoma2D 1.6.3 (installed above), Blender via COA Tools 2 / Tiny 2D Rig, any compositor. `render_poses.py` already renders posed stills from the rig data headlessly (the `proofs/` PNGs are deformations of the actual .inp data, not mockups). |
| `.blend` | **None for the WG cast.** The only .blend in the wider GMSS tools tree is `tools/character/Marshead_rigged_v1.blend` (a 3D Mars head, not a WG puppet). | Blender — not applicable to the cast today; a Blender cast rig would be built FROM the PNG packs (COA Tools 2 / Tiny 2D Rig route). |
| DragonBones | **No DragonBones-format WG rig exists** (no `_ske.json`/`_tex.json` anywhere in the puppet tree). `tools/animation/DRAGONBONES_WIRING.md` names DragonBones as the free skeletal path and claims cloned MIT runtimes at `tools/animation/upstream/dragonbones-js/` — **that directory is ABSENT from main HEAD** (verified in this checkout; `tools/animation/` holds only the doc + 7 Python scripts: animate_rig.py, blender_import.py, build_slice.py, fallback_render.py, make_visual_evidence.py, proxy_generator.py, rig_proxy.py). | DragonBones is a doc, not a rig source, today. |

---

## Recommendation — FIRST proof shot

**Use the nijilive `.inp` format, Ashes standard — the only format in which a finished, validated WG rig actually exists.**

- **Character/rig:** Ashes standard — richest rig in the cast (24 params, 15 textures, 18 animations) and the ONLY standard puppet with a working mouth (`ParamMouthOpenY`/`ParamMouthForm` on the grill layer), so the proof can include a line of dialogue with Rhubarb-driven grill movement, not just a silent pose.
- **Exact files:**
  - Rig: `~/workspace/_wg-v2-wireup/gmss/tools/puppet/wizard-rig-proof/ashes/Ashes.inp` (canonical source: GMSS `tools/puppet/wizard-rig-proof/ashes/Ashes.inp`)
  - Pose/animation driver: `ashes/render_poses.py` (already renders true deformations of this rig headlessly — extend it from stills to a PNG sequence: neutral → head-turn (ParamAngleX=30, ParamAngleY=-15) → blink (ParamEyeLOpen/R=0) → mouth-open line (ParamMouthOpenY), on 2s per the mystery-coast doctrine)
  - Ground-truth targets: `ashes/proofs/ashes_pose_neutral.png`, `ashes_pose_head-turn_mouth-open.png`, `ashes_pose_blink.png`, `ashes_pose_comparison.png`
  - Param map: `ashes/proofs/rig_parameters.json`; part fallback/QA: `ashes/parts/` + `ashes/parts/parts_manifest.json`, `ashes/rig_layers/`
  - Validator (fix the one hardcoded path line first): `ashes/validate_inp.py`
  - Assembly: sequence → ffmpeg; grade with `tools/color/presets.sh` (`vibrant-cartoon`); comp/finish in Natron 2.5.0 if a background plate is added.
- **Why this first:** zero re-rigging — the rig, its animations, its pose proofs and its validator all exist and passed today; the renderer path (`render_poses.py`) is the one WG-rig renderer that has demonstrably produced correct output on this VM. The shot proves the actual V2 asset, not a rebuild of it.
- **Why not the alternatives first:** DragonBones has no WG rigs (doc only, runtimes absent from HEAD — building there means re-rigging all 18 from PNGs before frame one). A Blender COA/Tiny-2D-Rig rebuild from the PNG packs is the strongest *second* path (Blender headless is proven on this VM) but is still a re-rig; Tahoma2D is now installed and verified (incl. headless `tcomposer`) and is the doctrine episode stage, but no WG `.tnz` scene exists yet — make it shot 2's stage test rather than betting the first proof on two unproven firsts at once. The known open risk on the recommended path is the nijigenerate GUI (never successfully operated headless) — the proof shot deliberately does NOT depend on the GUI; it drives the .inp through the Python renderer. A human/first-GUI open of `Ashes.inp` in nijigenerate remains an owed check for full editor-based production.

---

## Lane notes / loose ends
- `/tmp` tmpfs (512 MB) was at 100% during this lane (other lanes' AppImage extractions) — AppImage work must extract to workspace disk. This lane cleaned only its own `/tmp/appimage_extracted_*`.
- Parallel lanes were active during this run (Synfig extraction in `tools/synfig/`, Blender 5 downloads, Frankie .fla pull) — left untouched per check-before-start; bandwidth contention is why the ~870 MB of downloads took ~55 min wall-clock.
- Inkscape is the only install-base item not executable on this VM (dependency wall, exact list above) — flagged for a dependency-closure lane, NOT silently dropped.
- GMSS checkout is blobless/sparse (512 MB on disk incl. `.git`); delete `~/workspace/_wg-v2-wireup/` freely once downstream lanes have pulled what they need — canonical source is GMSS main.
