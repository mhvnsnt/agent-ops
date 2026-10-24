# game-ci — reusable GitHub Actions CI for game repos

One workflow, four gates: **asset validation → headless tests → Blender check → Godot export**. Red CI stays open with a comment naming the blocker — the job names make the failing gate obvious.

## Adopt in a repo

1. Copy `workflows/game-ci.yml` → `.github/workflows/game-ci.yml`
2. Copy `scripts/asset_gates.py` → `scripts/asset_gates.py` (or point the workflow at your own)
3. Copy `scripts/blender_smoke.py` → `scripts/` and **replace it with the repo's real checks** (armature validation, T-pose framing, white-void background, proof thumbnails). The smoke script only proves the headless pipeline works.
4. Set `GODOT_VERSION` and the two `barichello/godot-ci:` image tags to the repo's Godot version (must match — 4.4 in the template).
5. Commit `export_presets.cfg` (never `.gitignore` it). Preset names in the matrix must match `export_presets.cfg` **exactly, case-sensitive**.

## What's tested (2026-10-16, this VM)

| Script | Test | Result |
|---|---|---|
| `asset_gates.py` | Synthetic repo: bad-magic GLB, 501 MB `.blend` over cap, banned `.pem`, case-colliding `Tex.PNG`/`tex.png`, 5000px-wide PNG | 4 errors + 1 warning caught, exit 1 ✅ |
| `blender_smoke.py` | Blender 4.0.2 `-b --python` under `xvfb-run` | Rendered real 256×256 Cycles PNG (38 KB — not black) ✅ |

## Patterns used (2026)

- **Godot:** `barichello/godot-ci:4.4` container (or `chickensoft-games/setup-godot@v2`); `godot --headless --export-release`; GUT tests as a `needs:` gate; version from `git describe`; Web exports use the GL-Compatibility renderer.
- **Blender:** 4.x tarball + `xvfb-run -a blender -b --python` (Blender hard-requires a display even headless).
- **Asset gates:** stdlib-only Python — size caps, banned extensions, GLB magic/version/JSON validation, case-collision detection, texture dimension warnings.
- **Cost control:** release builds for real targets only; no giant debug×platform×version matrices.

## Notes

- Secrets (keystores, signing certs) go in GitHub Actions secrets, never in the repo.
- Large binaries (renders, ISOs, model packs) go to Releases/TeraBox, not git history.
- Godot C# projects: use `barichello/godot-ci:mono-<ver>` and `use-dotnet: true` with the setup-godot action.
