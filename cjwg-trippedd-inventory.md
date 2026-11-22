# TRIPPEDD-Production-studios- — Current Main Inventory (Wizard Gang target repo)

- **Repo:** `mhvnsnt/TRIPPEDD-Production-studios-` (note trailing hyphen)
- **Branch checked:** `main`
- **Main HEAD (verified via `gh api repos/mhvnsnt/TRIPPEDD-Production-studios-/commits/main`):**
  `dae6d1658ace42acef1e10385305889c84b60c17` — 2026-10-31T12:26:27Z —
  "Merge pull request #298 from mhvnsnt/fix/characterizer-frame-conjugation-20261031"
- **Tree source:** `gh api repos/mhvnsnt/TRIPPEDD-Production-studios-/git/trees/main?recursive=1`
  — 1,042 entries, `truncated: false`
- **Raw tree saved to:** `~/workspace/agent-ops/cjwg-trippedd-tree.json`
- **Method note:** All paths/sizes below are copied from that API tree output only.
  File contents summarised below were read via `gh api …/contents/<path>?ref=main`.

Top-level layout (entry counts include tree nodes):

| Path | Entries |
|---|---|
| `production/` | 584 (incl. the `production` tree node itself) |
| `toonboom-re/` | 229 |
| `tools/` | 192 |
| `docs/` | 26 |
| `ai-body-replace/` | 6 |
| `.github/` (incl. `.github/workflows/no-deletion-guard.yml`, 997 B) | 3 |
| `AGENTS.md` (10,852 B), `WORKING-METHOD.md` (316 B) | 2 files |

---

## 1. `production/wizard-gang-fla/` — in detail (72 entries)

This is exactly the PR **#293** file set:
PR #293 — "Wizard Gang FLA proof V001: Ashes puppet + arrival scene (.fla/XFL)",
MERGED 2026-10-30T22:42:34Z,
https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/pull/293
(`gh pr view 293 --json files` returns exactly the paths in this folder.)

### 1a. Top-level files

| Path | Size (B) |
|---|---|
| `production/wizard-gang-fla/PROGRAM-LOG.md` | 12,840 |
| `production/wizard-gang-fla/README.md` | 2,943 |
| `production/wizard-gang-fla/WG101ARRIVAL_Sc001_Clean_V001_ASH.fla` | 7,437,962 |
| `production/wizard-gang-fla/WG101_ORIGINAL_PUPPET_ASHES_VERSION_001.fla` | 7,408,720 |

Per `README.md` (read via API):

- `WG101_ORIGINAL_PUPPET_ASHES_VERSION_001.fla` — Ashes puppet (modern `.fla` =
  zipped XFL). 13-frame labelled pose library, HEADCOMP with 8 face states,
  EYESCOMP (colourway swaps + base-white set), MOUTHCOMP (14 Mouth Set One
  shapes), parts on real pivots from the library cut-apart set.
- `WG101ARRIVAL_Sc001_Clean_V001_ASH.fla` — scene to `FIRST-SHOT-SPEC`
  ("The wizards have arrived"): 1920×1080 @ 24 fps, 72 frames, Gumball scene
  stack, puppet copied into scene library, Pipeline One parallax push-in.
- Validation claimed in README: both `.fla` unzip round-trip clean;
  FlashXFLParser full parse, exit 0 — puppet 18 symbols / 36 layers / 253
  frames; scene 21 symbols / 39 layers / 256 frames.
- Known limits logged in README / PROGRAM-LOG: source figure is a
  crossed-arms illustration — no elbow segment, no legs/hips/knees, no chest
  under the crossed arms; Mouth Set One strips and base-white eye overlays
  failed registration over the baked face and ship as library swap frames;
  scene mouth is the grill deform; V002 needs a clean face plate.

### 1b. `production/wizard-gang-fla/docs/`

| Path | Size (B) |
|---|---|
| `production/wizard-gang-fla/docs/ashes-inventory.md` | 30,483 |
| `production/wizard-gang-fla/docs/gumball-dissection.md` | 35,710 |
| `production/wizard-gang-fla/docs/renderer-contract.md` | 24,129 |

README gloss: Ashes part inventory (200 PNGs measured), Gumball puppet+scene
dissection, XFL renderer contract.

### 1c. `production/wizard-gang-fla/proof/` — what is actually on main

- `production/wizard-gang-fla/proof/frames/f000.png` … `f052.png` — **53 frames
  only** (f000–f052, sizes 177,679–224,228 B, with `f052.png` 196,673 B).
- `production/wizard-gang-fla/proof/pose_0.png` (614,604 B)
- `production/wizard-gang-fla/proof/pose_3.png` (642,445 B)
- `production/wizard-gang-fla/proof/pose_7.png` (671,362 B)
- `production/wizard-gang-fla/proof/pose_9.png` (654,581 B)

**Not on main** (no such paths in the tree): any scene MP4, any
`frame_strip.png`, `poses_sheet.png`, or `structure_sheet.png` under
`production/wizard-gang-fla/proof/`, and frames f053–f071.

### 1d. `production/wizard-gang-fla/tools/`

| Path | Size (B) | What it is (read via API) |
|---|---|---|
| `production/wizard-gang-fla/tools/build_ashes.py` | 23,869 | XFL authoring. Builds both `.fla` files. Reads the cut-apart set (`parts.json`, pivots/bboxes), defines matrix helpers (`mat_mul/mat_T/mat_R/mat_S/about`), an `FLA` class writing `DOMDocument.xml` + `LIBRARY/*.xml` + `bin/*.dat` and zipping to `.fla`; `build_library()` (HEADCOMP / MOUTHCOMP — 14 Set-One shapes / EYESCOMP etc.), `build_master()` / pose library, `build_puppet()` (1920×1080, 24 fps, root `WG101_ORIGINAL_PUPPET_ASHES_VERSION_001`), `paint_bg()` (authored far/mid/near BG plates, labelled set dressing), `build_scene()` (72 frames, keyframes at f0/f36/f71, Gumball-style layers incl. `audio`, `framecounter`, `fieldguide`, `layout`). All character art = real library cut-apart files; BG plates are authored in-script. |
| `production/wizard-gang-fla/tools/fla_render.py` | 5,222 | "Minimal XFL compositor: executes the FLA files authored by build_ashes.py." Parses `DOMDocument.xml`/LIBRARY symbols, walks `DOMSymbolInstance`/`DOMBitmapInstance` with full Flash matrices (inverse-warp via PIL), honours `loop` = single frame / play once / loop. CLI: `fla_render.py <xfl_dir> [--symbol …] [--frame N] [--scene] --out … [--scale …] [--bg …]`. Exists because, per its docstring, the local leaf renderer cannot draw bitmap/nested files (see `docs/renderer-contract.md` in the folder docs). |
| `production/wizard-gang-fla/tools/finish_proof.py` | 4,658 | See §1e — the unfinished proof package. |

### 1e. What `finish_proof.py` still owes

Docstring (verbatim): *"Finish the Ashes FLA proof package: frames 53-71, MP4,
frame strip, pose sheet, Gumball-vs-Ashes structure sheet, motion verification
numbers. Safe to re-run; exits early if the sandbox write block is still active."*

Hard-coded build root in the script: `B = "/home/hatch/workspace/fla-build"`,
frames dir `f"{B}/proof/frames"`, scene XFL
`f"{B}/out/WG101ARRIVAL_Sc001_Clean_V001_ASH"`. Steps:

0. Write-block probe — saves `/tmp/_probe.png`; exits 3 with
   "WRITE BLOCK STILL ACTIVE" if the write fails/zero-byte.
1. **Remaining frames f053–f071** — loops `range(72)`, skips any existing
   `f%03d.png` > 10,000 B, otherwise `fla.render_scene(f)`. On current main
   only f000–f052 exist, so the owed render set is **f053–f071 (19 frames)**.
2. **Scene MP4** — `proof/WG101ARRIVAL_Sc001_V001.mp4`, ffmpeg, 24 fps,
   `libx264 -crf 17 -pix_fmt yuv420p +faststart`, from `f%03d.png`.
3. **Frame strip sheet** — `proof/frame_strip.png`, beats
   (0 NEUTRAL, 12 ANTICIPATION, 20 GESTURE+TALK, 32 GESTURE+TALK, 44 POINT,
   56 TRANSITION, 66 SETTLE (blink), 71 REST_X grin hold), tiles 470×264.
4. **Pose sheet** — `proof/poses_sheet.png`, from `pose_0/3/7/9.png`
   (NEUTRAL / GESTURE_WIDE / POINT / SETTLE), tiles 300×648.
5. **Structure sheet** — `proof/structure_sheet.png`,
   "PUPPET STRUCTURE — GUMBALL PRODUCTION vs WIZARD GANG (same anatomy)":
   GB200 puppet 008 vs WG101 Ashes V001 rows (format, stage, view rigs,
   master pose library, HEADCOMP, MOUTH, EYESCOMP, hands, validation).
6. Motion verification — pixel-diff / % pixels changed between consecutive
   strip frames, printed (not saved as a file).

README's "WIP at push time (owner pause order 2026-10-30)" names the same
debt in shorter form: *"Scene frames f053-f071, the MP4 encode, the
frame-strip sheet and the structure comparison sheet were mid-render when a
sandbox write failure blocked local file writes"* — i.e. the **two sheets**
named there are the frame-strip and the structure sheet; the script
additionally (re)builds the pose sheet in step 4. `PROGRAM-LOG.md` §
"INCIDENT — SANDBOX EXEC WRITE BLOCK (2026-10-30 ~17:24 CDT)" records the
EPERM write block as the cause: "Frames f053+ and the MP4 encode are BLOCKED
on it, not on the build."

**Bottom line:** to complete the proof package, run
`python3 tools/finish_proof.py` (idempotent, self-probing) — nothing in the
current main tree shows it has been run/committed since PR #293.

---

## 2. `docs/wizard-gang/` — contents

| Path | Size (B) |
|---|---|
| `docs/wizard-gang/FIRST-SHOT-SPEC.md` | 4,754 |
| `docs/wizard-gang/FLA-PRODUCTION-STANDARD.md` | 10,151 |
| `docs/wizard-gang/ORIGINAL-PIPELINE-V1-FROZEN.md` | 6,401 |
| `docs/wizard-gang/REAL-ANIMATION-V2-STACK.md` | 7,767 |
| `docs/wizard-gang/RIG-DISSECTION.md` | 8,734 |
| `docs/wizard-gang/WG-PRODUCTION-METHOD.md` | 7,240 |
| `docs/wizard-gang/WG-RIG-TEMPLATE.md` | 9,712 |
| `docs/wizard-gang/audits/wizard-gang-real-anim-local-tools-2026-10-29.md` | 34,762 |
| `docs/wizard-gang/audits/wizard-gang-real-anim-repo-audit-2026-10-29.md` | 59,630 |
| `docs/wizard-gang/pipeline-one/PIPELINE-ONE-MOTION-METHOD.md` | 2,086 |
| `docs/wizard-gang/pipeline-one/ashes_pipeline-one_motion-test_v1.mp4` | 3,294,559 |
| `docs/wizard-gang/pipeline-one/ashes_pipeline-one_motion-test_v1_DARKFACE_SILENT.mp4` | 2,937,862 |
| `docs/wizard-gang/pipeline-one/ashes_pipeline-one_motion-test_v1_strip.png` | 1,241,413 |
| `docs/wizard-gang/pipeline-one/ashes_pipeline-one_motion-test_v2_strip.png` | 1,210,431 |
| `docs/wizard-gang/pipeline-one/ashes_pipeline-one_motion-test_v2_voidface_SILENT.mp4` | 2,160,665 |

### FLA production standard — PR #285

- **Path: `docs/wizard-gang/FLA-PRODUCTION-STANDARD.md`** (10,151 B) — the
  **only** file in PR #285: "docs(wizard-gang): FLA production standard",
  MERGED 2026-10-30T21:20:21Z,
  https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/pull/285
- Content (head read via API): owner directive 2026-10-30 ("make fla puppets
  and rigs and scene files for all our shows", Wizard Gang first); derived
  from a full XML dissection of two Gumball production files
  (`GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`, `GB202REMOTE_Sc094_Clean_V023_STN.fla`,
  from `mhvnsnt/cn-gigaleak-gumball` release `gumball-s2-rigs-v1`).
  Companions named in-doc: `WG-RIG-TEMPLATE.md`, `RIG-DISSECTION.md`,
  `FIRST-SHOT-SPEC.md`.
- Rules in-doc: `.fla` = ZIP of XFL XML, author XFL directly, validate by
  round-trip parse (FlashXFLParser); naming
  `WG<block>_ORIGINAL_PUPPET_<CHAR>_VERSION_<NNN>.fla` /
  `WG<block><EPSLUG>_Sc<NNN>_<Stage>_V<NNN>_<INITIALS>.fla`; symbols
  `WG_<CHARCODE>_<VIEW>_<PART>` with `HEADCOMP/BODYCOMP/EYESCOMP/MOUTHCOMP`;
  views FRONT | TQ | BACK | FLOP (drawn, not mirrored); puppet stage =
  asset-container sheet (never animate on it), scene = 1920×1080, both
  24 fps, animate on 2s; master symbol per view, labelled pose library +
  `loop="single frame"` addressing, anatomical `transformationPoint` pivots
  identical across keyframes, joint segmentation where art allows with
  gaps logged, in-file NOTES guide layers; required sets per character
  (body parts, mouth ≥12 core drawings, eyes — both colourway + base-white
  variants, hands, pose library ≥3); Ashes exception (only cast member with
  a mouth — diamond grill; other eight void-faced); T-pose rule (owner's
  corrected 2026-10-30 version: T-pose art is a legitimate rig base, the
  bar is on posed-out output); scene layer stack, lock layers not being
  animated.

---

## 3. `production/` and `docs/` overall structure

### `production/`

Two children only:

1. **`production/wizard-gang-fla/`** — 72 entries, §1 above (the FLA lane).
2. **`production/WIZARD_GANG_EP01/`** — 510 entries (Pipeline One era):
   - `production/WIZARD_GANG_EP01/TRIP-EFFECTS-DIRECTION.md` (2,553 B)
   - `production/WIZARD_GANG_EP01/end-credit-mw.mp4` (16,983 B)
   - `production/WIZARD_GANG_EP01/animation-study/` — 404 entries, by show
     folder: `fosters-cnleaks/` (the bulk — Foster's production art:
     `.eps` 122, `.ai` 65, `.jpg` 37, `.tif` 16, `.fla` 10, `.doc` 9 across
     all of WIZARD_GANG_EP01), `fosters-home/`, `grim-adventures/`,
     `robot-chicken/`.
   - `production/WIZARD_GANG_EP01/video/` — 104 entries: subfolders
     `faceswap/`, `faceswap-v2/`, `headswap/`, `headswap-v2/`, `new-scenes/`,
     `.thumbnails/`, plus loose MP4s incl. `kiko-music-video-ROUGH-v1.mp4`
     (93,770,235 B), `kiko-encore-anyway-v1.mp4` and `-MIX-v1`…`v5`,
     `viggle-chunk1/2/3-*.mp4`, `viggle-muta-test-1.mp4`, and
     `media-generation-kiko-*` MP4/JSON pairs.
   - File-type totals for `production/WIZARD_GANG_EP01/` blobs:
     `.eps` 122, `.mp4` 67, `.ai` 65, `.jpg` 37, `.tif` 16, `.json` 14,
     `.fla` 10, `.doc` 9, `.wav` 7, `.md` 4, `.pdf` 4, `.psd` 4, `.swf` 1,
     others singletons. (These `.fla` are study/production files under
     `animation-study/`, not Wizard Gang scene files.)

### `docs/`

| Path | Size (B) |
|---|---|
| `docs/BUILD-MAP-FREE-VERSIONS.md` | 32,826 |
| `docs/INDUSTRY-STACK-STATUS.md` | 8,559 |
| `docs/NO-DATA-LOSS-RULES.md` | 3,635 |
| `docs/industry-eps-renders-2026-10-30/LOG.md` | 3,344 |
| `docs/industry-eps-renders-2026-10-30/MANIFEST.md` | 5,322 |
| `docs/industry-eps-renders-2026-10-30/manifest.json` | 87,896 |
| `docs/wizard-gang/…` | §2 above (17 entries incl. subfolders) |

### Other top-level production-adjacent trees

- `toonboom-re/` — 228 entries under `toonboom-re/`: `README.md` (2,559 B),
  `data/`, `docs/`, `oss-tvg/`, `proofs/`, `tools/` (incl.
  `toonboom-re/tools/render.py` 29,531 B, `rigmap.py`, `gainstats.py`,
  `nickdir.py`, `zipdir.py`, and Rust `tvg1008/`, `tvgdump/`, `tvgrender/`).
- `ai-body-replace/` — `KAGGLE-SETUP.md` (2,096 B), `README.md` (3 B), plus
  tree nodes only in the recursive listing beyond those two blobs.

---

## 4. `tools/` wiring already present **in this repo**

`tools/` = 191 paths under the prefix (192 incl. tree node), 11 tool packages,
each with a `README.md`:

| Package | Entries | Notable exact paths |
|---|---|---|
| `tools/characterizer/` | 20 | `tools/characterizer/characterizer/core.py` (30,066 B), `operators.py`, `panels.py`, `profiles.py`; profiles `cape_jones_canon.json`, `cmu_bvh.json`, `mixamo.json`, `rigify.json`, `rokoko.json`, `tripo.json`; `tests/` (3 test files + log). This is the package fixed by main-HEAD PR #298. |
| `tools/checkpoint-render-driver/` | 8 | `checkpoint_render_driver.py` (15,935 B), `render_one.py`, `run.sh`, `config.example.json`, `tests/TEST-LOG.md` |
| `tools/effectorkit/` | 12 | `effectorkit_gn.py` (30,977 B), `addon/effectorkit/__init__.py`, `effectorkit_library.blend` (180,046 B), demo + test files |
| `tools/gluegraph/` | 9 | `gluegraph_addon/__init__.py`, `constraints.py`, `fracture_core.py`, `tests/` |
| `tools/mouthswap-bridge/` | 18 | `mouthswap_bridge.py` (15,282 B), `blender_mouthswap.py`, `tests/` incl. sample mouths A–H/X PNGs |
| `tools/natron-card-look-kit/` | 34 | `gizmos/` (CJLedDeepPurpleGlow, CJLedPartyGlow, CJLook1PaleWash, CJLook2DeepSaturation, TrippeddCard25D), `card-kit/community-donor/PM_Camera*`, `PM_Card3D*`, `docs/CARD-PROJECTION-RECIPE.md`, `LOOKS-AND-LED-KNOBS.md`, `SOURCES-AND-PROVENANCE.md`, `test/` |
| `tools/puppet-control-sheets/` | 34 | `puppet_control_sheets/generate_puppet_scene.py` (19,223 B), `validate_scene.py`; `templates/wizard-gang.json`, `templates/cape-jones-2d.json`; `docs/CONTROL-SHEET.md`, `TAHOMA2D-SURFACE-NOTES.md`; `toonzscript/apply_pose_exposure.js`; `test-output/testpuppet/…` (`.tnz` + renders) |
| `tools/pyro-shaping-pack/` | 22 | `pyro_lib.py`, `apply_pyro.py`, `build_presets.py`, presets campfire/chimney_smoke/explosion_burst/fog_bank/jet_flame, `pyro_presets.blend` (521,179 B) |
| `tools/sculpt-finisher/` | 6 | `sculpt_finisher.py` (28,912 B), `test_finisher.py`, logs |
| `tools/smartmask-presets/` | 16 | `presets/apply_smartmask_preset.py`, `smartmask_presets.json`, `install_ucupaint.sh`, `tests/output/…` incl. `smartmask_preset_library.blend` (2,359,472 B) |
| `tools/wedgerunner/` | 12 | `wedgerunner.py` (9,091 B), `blender_driver.py`, `examples/`, `tests/` |

Plus the FLA-specific wiring in §1d (`production/wizard-gang-fla/tools/`)
and the Toon Boom RE wiring in `toonboom-re/tools/` (§3). There is **no**
repo-root FLA/Animate, Tahoma2D, or Krita package in-tree — those are
external/local tools documented in the audits (§5), not vendored here.

---

## 5. What tools were "wired" 2026-10-29, per the docs in this repo

Source docs (exact paths):

- `docs/wizard-gang/audits/wizard-gang-real-anim-local-tools-2026-10-29.md`
- `docs/wizard-gang/audits/wizard-gang-real-anim-repo-audit-2026-10-29.md` (59,630 B — all-146-repos audit, not read in full for this inventory)
- `docs/wizard-gang/REAL-ANIMATION-V2-STACK.md` ("Opened 2026-10-29 by owner order")

**Precision note:** the 2026-10-29 local-tools audit is an *inventory/verification
pass*, and says so itself: every entry "checked on disk 2026-10-29… **Nothing
was installed, deleted, run… in this pass**." So 2026-10-29 status ≠ wired —
it is the verified status at that date:

**WORKS on 2026-10-29 (per that audit's summary table):**

- Blender 4.0.2 (`tools/blender/` — local `~/workspace/tools`, not this repo) and Blender 4.5.3 (`tools/blender-4.5/`)
- Pencil2D 0.7.2 (`tools/pencil2d/`)
- Friction 1.0.0-rc.3 (`tools/friction/`)
- `tools/color/presets.sh` + `color-thief/` (ffmpeg looks; ffmpeg 8.1.2 on system)
- Rhubarb Lip Sync 1.14.0 (`tools/rhubarb/`, ELF binary 7,331,192 B) + `tools/lipsync/` (`rhubarb_to_visemes.py`, `caption.py`)
- `tools/script-tools/` (`fountain_to_cues.py`, `build_animatic.py`)
- Natron 2.5.0 (`tools/natron/`, headless renders verified 2026-10-19 and 2026-10-23 per audit)
- JPEXS FFDec 26.3.0 (`tools/jpexs-ffdec/ffdec.jar`) + Java JDK 21.0.5 in `tools/java/`
- Audacity (`tools/audacity/`)

**WORKS-WITH / STORED-ONLY / BLOCKED on 2026-10-29 (selected):**
Tiny 2D Rig Tools (WORKS-WITH, not yet installed into Blender), COA Tools 2
(STORED-ONLY, in cape-jones), Guided Tweening + Smart2D (BLOCKED — need
Blender 5.0, local max 4.5.3), OPEN-TOON, Glaxnimate, AnimeInbet /
LayerInbetween / ToonCrafter / ToonComposer (AI-ASSIST, STORED-ONLY),
OpenFaceFX, Gentle, Storyboard app, OpenTimelineIO, OpenCue, CGRU/Afanasy,
Flamenco, Kitsu+Zou, Duik, ChibiRigKit — all STORED-ONLY.

**MISSING locally on 2026-10-29 (per audit):** Synfig Studio (empty dir),
Tahoma2D 1.6, OpenToonz 1.8.0, Krita 6.0.4 host (its plugins orphaned),
BasicPBC, Storyboarder 2.1.0 (Wonder Unit), FlashXFLParser, Kdenlive,
MLT/`melt` binary.

**The 2026-10-29 stack doc** (`REAL-ANIMATION-V2-STACK.md`) names the V2
chain to wire from that inventory: Pipeline One stays as base layer
(Chatterbox voices, Viggle body replacement, Muse video base, pan-and-zoom
parallax); on top — GMSS `tools/puppet/wizard-rig-proof/` cast part packs +
nijilive `.inp` puppets, Tahoma2D (from vendor-tools), Blender Grease Pencil
+ Tiny 2D Rig / COA Tools 2, Pencil2D, Glaxnimate, Rhubarb, Natron,
Flowblade+MLT, Storyboarder, Fountain script tools; AI-assist only:
ToonCrafter / AnimeInbet / LayerInbetween.

**Superseding update in-repo (next day):** `docs/INDUSTRY-STACK-STATUS.md`
is dated **2026-10-30**, not 10-29, and records the wired+verified state
*after* the free wire-up pass: Blender 4.0.2 + 4.5.3 + **5.2.3**, Godot
4.7.2, Natron 2.5.0, **Krita 6.0.4**, **Tahoma2D 1.6.3**, Pencil2D 0.7.2,
**Storyboarder 2.1.0**, Rhubarb 1.14.0, ffmpeg 8.1.2 — all WIRED+VERIFIED;
OpenToonz 1.8.0 INSTALLED but launch-blocked in this VM only (no `/dev/fuse`).
The 10-29 "MISSING" entries for Krita/Tahoma2D/Storyboarder therefore do
**not** describe the later state — quote them only with their date.

---

## Gaps / caveats

- The two 2026-10-29 audit docs and most `docs/wizard-gang/*.md` files were
  inventoried from the tree (exact path + size) and only sampled by content
  (`FLA-PRODUCTION-STANDARD.md`, `REAL-ANIMATION-V2-STACK.md`,
  `INDUSTRY-STACK-STATUS.md`, local-tools audit summary table) — full-text
  claims beyond those samples are not asserted here.
- No path in this inventory was constructed or guessed; any file not in the
  recursive tree (e.g. the finish_proof outputs in §1c) is reported as absent.
