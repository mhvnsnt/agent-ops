# CJWG Tools Audit — What Is Actually Runnable Locally Right Now

**Date:** 2026-11-02 (checked live this run, America/Chicago)
**Method:** `ls`/`which`/`--version` + python import checks on this VM only. Nothing installed, nothing downloaded. The 31.3 GB tools archive was NOT pulled.
**Statuses:** `RUNTIME-OK` = runnable now from a workspace path · `SYSTEM-OK` = runnable now from system PATH · `ARCHIVE-ONLY` = not on local disk, verified in the GitHub archive · `MISSING` = not on PATH / not on disk (archive status noted where known)

---

## Headline

- **`~/workspace/tools/` does not exist.** Confirmed: `ls: cannot access '/home/hatch/workspace/tools': No such file or directory`. This matches `TOOLS.md`: the whole folder (31.3 GB, 251,892 files) was stored 2026-10-31 to GitHub release `tools-archive-2026-10-31` on `mhvnsnt/western-heart` (29 hash-verified pieces, pull-back tested) and the local copy was deleted.
- **Archive verified live this run (listing only, no download):** `gh release view tools-archive-2026-10-31 --repo mhvnsnt/western-heart` → tag `tools-archive-2026-10-31`, published 2026-10-31T17:33:58Z, assets `chunk-000.tar.gz` … `chunk-019b.tar.gz` etc. Restore per `TOOLS.md`: `gh release download tools-archive-2026-10-31 --repo mhvnsnt/western-heart`, reassemble per the release's `MANIFEST-tools.md` (chunks: `gunzip | tar -x`; `.segNN`: `cat` in order).
- **The FLA/XFL chain does NOT need that archive.** Python 3.12 + Pillow + lxml + stdlib `zipfile` + ffmpeg 8.1.2 are all system-live, and working in-repo Python XFL parsers/renderers already exist outside `tools/` (see FlashXFLParser row). Bitmap-part FLA build → parse/validate → PNG frames → MP4 is runnable today with zero restore.
- **Everything heavy/GUI is archive-only:** Blender (all versions), Krita, Synfig, Kdenlive, melt, Natron, Ghostscript, Java, .NET, Tahoma2D, OpenToonz, BasicPBC, FlashXFLParser.

Disk at audit time: `/dev/mapper/rv 150G, 91G used, 59G free (61%)`.

---

## Table

| Tool | Status | Path / version (as checked) | Needed for FLA chain? |
|---|---|---|---|
| `~/workspace/tools/` (whole folder) | ARCHIVE-ONLY | Absent on disk; archive = `mhvnsnt/western-heart` release `tools-archive-2026-10-31`, verified by `gh release view` this run | No — see minimal chain below |
| python3 | SYSTEM-OK | `/usr/bin/python3` — Python 3.12.3 | **Yes — core** |
| pip / pip3 | SYSTEM-OK | `/usr/bin/pip`, `/usr/bin/pip3` — pip 24.0 (python 3.12) | Support only |
| Pillow (PIL) | SYSTEM-OK | `PIL 10.2.0`, `/usr/lib/python3/dist-packages/PIL/` — `from PIL import Image` OK | **Yes — core (PNG part compositing)** |
| lxml | SYSTEM-OK | `lxml 5.2.1`, `/usr/lib/python3/dist-packages/lxml/` | **Yes — XFL XML parse/validate** |
| zipfile (stdlib) | SYSTEM-OK | stdlib, `/usr/lib/python3.12/zipfile/` (+ `xml.etree.ElementTree` stdlib OK) | **Yes — core (.fla is a ZIP)** |
| numpy | SYSTEM-OK | 1.26.4 (pip list) | Support (image work) |
| ffmpeg | SYSTEM-OK | `/usr/bin/ffmpeg` — ffmpeg 8.1.2; PNG/APNG encoders present | **Yes — core (frames → clip)** |
| ffprobe | SYSTEM-OK | `/usr/bin/ffprobe` — ffprobe 8.1.2 | Yes — verify clips |
| zip / unzip | SYSTEM-OK | `/usr/bin/zip`, `/usr/bin/unzip` — UnZip 6.00 | Support (.fla inspect) |
| xvfb-run / Xvfb | SYSTEM-OK | `/usr/bin/xvfb-run`, `/usr/bin/Xvfb` | Only for GUI/Blender headless |
| node | SYSTEM-OK | `node` on PATH — v24.22.1 | No |
| npm | SYSTEM-OK | `/opt/hatch-image/bin/npm` — 10.9.4 | No |
| gh | SYSTEM-OK | `/usr/bin/gh` — 2.102.0 | Only to restore the archive |
| ghostscript / gs | MISSING | `which gs ghostscript` → not found; no `/usr/bin/*ghost*`. Was in `tools/` (per TOOLS.md) → archive-only | No for bitmap chain; would help PDF/EPS/SVG raster paths |
| blender | ARCHIVE-ONLY | `which blender` → not found. Was `tools/blender/` 4.0.2, `tools/blender-4.5/` 4.5.3, `tools/blender-5/` 5.2.3 LTS (wiring logs 2026-10-29) — all in the archive | No |
| krita | ARCHIVE-ONLY | `which krita` → not found. Host app was already missing 2026-10-29 (only plugins on disk then); any Krita bits are in the archive | No |
| synfig | ARCHIVE-ONLY | `which synfig` → not found. Was wired+proven 2026-10-29 as Synfig Studio 1.5.5 in `tools/synfig/` — in the archive | No |
| kdenlive | ARCHIVE-ONLY | `which kdenlive` → not found. Was wired+proven 2026-10-29 as 26.08.2 AppImage in `tools/kdenlive/` — in the archive | No |
| melt (MLT) | ARCHIVE-ONLY | `which melt` → not found. Was `tools/mlt/melt` 7.43.0 (from the Kdenlive bundle; 6.6.0 from Synfig as fallback) — in the archive. ffmpeg covers its FLA-chain job | No — ffmpeg substitutes |
| natron | ARCHIVE-ONLY | `which natron` → not found. Was Natron 2.5.0, headless-verified, in `tools/natron/` — in the archive | No |
| inkscape | MISSING | `which inkscape` → not found; no version output. Listed among archived `tools/` paths in TOOLS.md-era docs, but no local binary today | No for bitmap chain; gap for faithful SVG/vector-shape rasterising (see limits) |
| java | ARCHIVE-ONLY | `which java` → not found. Was `tools/java/jdk-21.0.5+11-jre/bin/java` (verified 2026-10-29, needed by JPEXS FFDec) — in the archive | No (only for FFDec/SWF work) |
| dotnet (.NET SDK) | MISSING / ARCHIVE-ONLY | `which dotnet` → not found. FlashXFLParser harness was built with .NET SDK 8.0.427 in `tools/FlashXFLParser/harness/` — in the archive | No if the Python parser is used (recommended); **yes only to run the original C# FlashXFLParser** |
| FlashXFLParser (upstream C#) | ARCHIVE-ONLY | No folder found: `find ~/workspace -iname "*FlashXFL*"` → no directory anywhere on disk. Was `~/workspace/tools/FlashXFLParser/` (cloned + wired+proven 2026-10-29 on Pim/Charlie rigs) — in the archive. Only mentions on disk now are in memory-staging copies, not code | No — replaced locally, see next row |
| Python XFL parsers / renderers (in-repo) | RUNTIME-OK | Present and Python-runnable today, outside `tools/`: `~/workspace/agent-ops/fla-puppets-program-2026-10-30/work/parse_xfl.py` (7.2K, stdlib ET; invoked with no args it runs and errors on missing args — i.e. it executes), `…/work/walk_xfl.py` (2.7K), `~/workspace/agent-ops/wizard-gang-real-hands-2026-10-29/src/xfl_render.py` (11K) + `xfl_render_fallback.py`, `~/workspace/agent-ops/wizard-gang-industry-2026-10-29/src/xfl_render_local.py` (11K) + `render_all_xfl.py` | **Yes — this is the validator/renderer to use** |
| BasicPBC | ARCHIVE-ONLY | No folder found: `find ~/workspace -iname "*BasicPBC*"` → nothing. Was `~/workspace/tools/basicpbc/` (wired+proven 2026-10-29, torch 2.2.2+cpu venv, checkpoints 105,523,141 B / 50,350,481 B) — in the archive. Needs torch/CLIP (~GBs), not a light restore | No — colourisation stage only, not FLA build/validate/render |
| Tahoma2D / OpenToonz / Glaxnimate / Storyboarder | ARCHIVE-ONLY | None on PATH/disk (all were `tools/` or repo-source only on 2026-10-29) — in the archive / cape-jones repo docs | No |
| ImageMagick (`convert`/`magick`), rsvg-convert | MISSING | `which` → not found for both | No — Pillow covers PNG work |
| Real XFL source rigs (inputs, not tools) | RUNTIME-OK | On disk in agent-ops, e.g. `fla-puppets-program-2026-10-30/gumball/…_xfl/`, `wizard-gang-real-hands-2026-10-29/darwin_xfl/GB200_ORIGINAL_PUPPET_DARWIN_Version002_CS5.xfl`, `wizard-gang-v2-put-to-use-2026-10-29/smiling/{charlie,pim}_xfl/`; prior PNG renders in `your_files/wizard-gang-part-libraries/_candidates/xfl-full-renders/` | Inputs — chain can be proven on these today |

Note on TRIPPEDD: no FlashXFLParser/BasicPBC code or docs were found under `~/workspace/trippedd/` or `~/workspace/_cjwg-20261102/{cape-jones,trippedd}/` (both `_cjwg-20261102` subdirs are empty). All FlashXFLParser/BasicPBC ground truth is in `~/workspace/agent-ops/wizard-gang-v2-missing-tools-wireup-2026-10-29.md` and `wizard-gang-real-anim-local-tools-2026-10-29.md`.

---

## Minimal FLA chain — what is needed, and whether we have it

### 1. Build FLA / XFL (zip-based) — ✅ runnable now
- An uncompressed `.xfl` is a folder: a `<name>.xfl` marker file + `DOMDocument.xml` + `DOMSymbolItem` XML under `LIBRARY/` + bitmaps under `LIBRARY/`/`bin/`. A modern `.fla` is that same tree ZIPped.
- Needs only: python3 + stdlib `zipfile` + `xml.etree.ElementTree`/`lxml` to write the XML and zip it. **All SYSTEM-OK.** No Animate, no Java, no archive restore.
- Caveat: legacy pre-CS5 `.fla` is OLE2 binary, not ZIP/XFL — the XFL route cannot write/read those as XFL (the 2026-10-29 lane hit exactly this with the Frankie rig and decoded it at OLE level instead).

### 2. Validate / parse — ✅ runnable now (Python), C# parser optional
- Use the in-repo Python parsers above (`parse_xfl.py` / `walk_xfl.py` / `xfl_render_local.py`): they read `DOMDocument.xml` → timelines → layers → frames → `DOMSymbolInstance`/`DOMBitmapInstance` with matrices, `libraryItemName`, `firstFrame`/`loop`. That covers structural validation (well-formed XML via lxml, symbol refs resolve, frame counts/durations sane).
- FlashXFLParser (C#) is a stricter XmlSerializer model of the same data, but running it needs the archive restored **plus** a .NET SDK (also not on PATH). Not worth a 31 GB restore for validation the Python parser already does. Restore it only if a rig parses differently in C# vs Python and that discrepancy matters.

### 3. Render PNG parts → frames → clip — ✅ runnable now, with one honest limit
- Needs: Pillow (composite bitmap parts per frame using each instance's matrix) + ffmpeg (PNG sequence → MP4/WebM). **Both SYSTEM-OK** (Pillow 10.2.0, ffmpeg 8.1.2 with PNG encoder). This is exactly what `xfl_render.py` / `xfl_render_local.py` already did — prior outputs survive in `your_files/wizard-gang-part-libraries/_candidates/xfl-full-renders/`.
- **Limit:** `DOMShape` vector geometry is the weak spot — the local Python renderers handle symbol/bitmap instances and pass on raw shapes. Faithful vector-shape rasterising would want Inkscape/Ghostscript/a real Flash renderer, all MISSING/archive-only today. For rigs whose parts are bitmaps (the pro Gumball/Smiling Friends puppets in hand), this does not block. For vector-only rigs, expect shape parts to be missing/flat until a rasteriser is restored — log it as a gap, don't fake it.

### Bottom line for the FLA chain
**Nothing needs to be installed or restored to start.** Build, validate, and bitmap-render a FLA/XFL scene to a watchable clip today with: `python3 3.12.3 + Pillow 10.2.0 + lxml 5.2.1 + zipfile (stdlib) + ffmpeg/ffprobe 8.1.2` + the in-repo Python XFL code listed above.
Restore from `tools-archive-2026-10-31` only when a step genuinely needs: Blender/Krita/Synfig/Tahoma2D (authoring/drawing), Ghostscript/Inkscape (vector rasterising), Java+FFDec (SWF decompile), .NET+FlashXFLParser (C# cross-check), or BasicPBC (paint-bucket colourisation, plus its torch venv).
