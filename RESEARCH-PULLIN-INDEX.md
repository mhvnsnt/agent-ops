# RESEARCH → PULL-IN INDEX

Master index of every research topic: where the doc landed (repo + path), what was pulled in from it, or why not.
Owner rule 2026-10-16: a finding without a pull-in is incomplete — track until wired or explicitly excluded with license reason.

## Active research branches (2026-10-16)

| Branch | Topics | Research doc → repo | Status |
|---|---|---|---|
| 3D pipeline | image-to-3D (TRELLIS/Hunyuan3D/SF3D…), Source/XPS→GLB Linux, render speed, auto-rigging | → western-heart docs/ (pending) | Researching |
| Audio/voice/music | TTS/VC 2026, SFX gen, open music gen, vocal restoration | → cape-jones docs/ + western-heart docs/ (pending) | Researching |
| Teardown/RE + engines | QuickBMS/Ghidra/console tooling, Noesis, Godot/Bevy/Unreal/legacy engines, web frameworks | → game-reverse-engineering docs/ + western-heart docs/ (pending) | Researching |
| AI/ML inference | local LLMs, GGUF/quantization, diffusion on T4, LoRA/QLoRA | → cape-jones + western-heart docs/ (pending) | Researching |
| Procgen + asset pipelines | PCG levels/chars/textures, USD, glTF extensions, material systems | → western-heart docs/ (pending) | Researching |
| Netcode/multiplayer | rollback (GGPO/Godot), WebRTC, matchmaking, cloud streaming | → western-heart docs/ + game/ (pending) | Researching |
| Console homebrew + CI | PS2/PSP/GC/N64/Xbox SDKs, emulator debuggers, CI templates | → game-reverse-engineering docs/toolchains/ (9 docs) + tooling/console-toolchains/ ; CI template → agent-ops ci-templates/game-ci/ | ✅ wired 2026-10-16 |

## Previously pulled (pre-index, from 2026-PULL-SUMMARY + cape-jones PRs #15–#20)

### Animation / interpolation
| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| ToonCrafter | GitHub (SIGGRAPH Asia 2024) | open | ~/workspace/tools/ + Kaggle guide | ✅ wired |
| AnimeInbet | GitHub (ICCV 2023) | open | ~/workspace/tools/ | ✅ wired |
| RIFE | GitHub | open | cape-jones pipeline | ✅ wired |
| LayerInbetween | SIGGRAPH 2026 | open | cape-jones PR #17 | ✅ wired |
| LTX-2.5 | — | open | cape-jones PR #17 | ✅ wired |
| EverAnimate | — | open | cape-jones PR #17 | ✅ wired |
| OPEN-TOON | — | open | cape-jones PR #17 | ✅ wired |
| ComfyUI VideoFX Suite | — | open | cape-jones PR #17 | ✅ wired |

### Voice / TTS / audio
| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| Chatterbox | GitHub | MIT | ~/workspace/tools/ | ✅ wired (character default) |
| Kokoro | GitHub | Apache-2.0 | ~/workspace/tools/ | 🔄 installing |
| OpenVoice | GitHub | open | ~/workspace/tools/ | ✅ wired |
| Dia | GitHub | open | ~/workspace/tools/ | ✅ wired |
| StyleTTS2 | GitHub | open | ~/workspace/tools/ | ✅ wired |
| LuxTTS | — | open | cape-jones PR #18 | ✅ wired |
| MMAudio | GitHub | open | ~/workspace/tools/ | ✅ wired |

### Upscaling / restoration
| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| RealESRGAN (anime 6B) | GitHub | BSD-3 | ~/workspace/tools/ | ✅ wired |
| SPAN | — | open | cape-jones | ✅ wired |
| OmniColor | — | open | cape-jones PR #17 | ✅ wired |

### 3D / rigging
| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| ChibiRigKit | GitHub | open | ~/workspace/tools/ | ✅ wired |
| Blender Source Tools | GitHub | open | ~/workspace/tools/source-tools/ | 🔄 wiring (render agent) |
| guided-tweening | GitHub | open | ~/workspace/tools/ | ✅ cloned |
| smart2d | GitHub | open | ~/workspace/tools/ | ✅ cloned |
| tiny-2d-rig | GitHub | open | ~/workspace/tools/ | ✅ cloned |

### Video / generation
| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| Kandinsky 6.0 | — | MIT | cape-jones PR #18 | ✅ wired |
| BasicPBC (auto-color) | GitHub (CVPR 2024) | open | ~/workspace/tools/ | ✅ wired |

### Pipeline / misc
| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| OpenTimelineIO | GitHub | open | ~/workspace/tools/ | ✅ wired |
| Awesome-AI4Animation | GitHub | curated list | ~/workspace/tools/ | ✅ cloned |
| lvsfunc/kagefunc | GitHub | open | cape-jones | ✅ wired |

### Documented, NOT pulled (excluded with reason)
| Tool | Reason not pulled |
|---|---|
| MiniMax H3 | License excludes US/EU/UK/KR — unusable for US production |
| TalkingPose | Research-only license |
| Wav2Lip | Relicensed non-commercial |
| Fish Speech / Breeze TTS 2 weights | Non-commercial |
| comfyui-rife-tensorrt | CC-BY-NC-SA non-commercial (pulled then deleted) |
| Stable Audio 3 / Magenta Realtime 2 / MiniMax Music 3.0 | Documented, GPU models — pull pending |

## Conventions
- New entries go under the branch that found them, then graduate here when merged.
- "✅ wired" = installed + tested + pushed green. "🔄" = in progress. "❌ excluded" = license reason documented.
- Every research doc lives in a repo (never local-only).

## Knowledge management (meta-research, 2026-10-16)
Research on how to manage research across 66 repos. Doc: agent-ops `RESEARCH-CONVENTIONS.md`.
| Finding | Source | Applied |
|---|---|---|
| Polyrepo (5+ repos) → dedicated docs repo for system-wide docs; each repo keeps own `docs/` | greglamb/claude-gcode-tools guide-strategy | agent-ops = docs hub (already was); per-repo `docs/research/` |
| ADRs: short, dated, immutable; never edit — supersede with new linked record | alz-repo-best-practices; chrisclements1987 meta-repo-seed | `docs/adr/` + `adr-template.md` in agent-ops |
| One-line context index: condense every decision into one actionable sentence, feed to AI tools | dev.to "Enforcing ADRs with Deterministic Architecture Tests" | RESEARCH-PULLIN-INDEX.md one-line-per-topic format |
| Dedupe: URL+text dedup before ingestion; source trail survives synthesis | dev.to "From too many sources to knowledge I can use again" | `research-check.sh` + index-first rule |
| Research→action: findings become decision-ready insights linked to source, then tracked work items | SwarmLens case study; aiwire.net KM survey | index status column: researching → wired / excluded / queued |
| ADR industry pattern: 1-2 page max, same repo as code, immutable, status metadata; IBM Watson 80+ ADRs → 3x faster onboarding; failure modes = over-documentation, tool complexity, isolated docs | chrisclements1987 meta-repo-seed; selvarajmurugesan90 ops-engineering-skills; dhruvil29 orchitkit | ADR-lite in RESEARCH-CONVENTIONS.md (docs/adr/, never edit — supersede) |
| Multi-repo orgs: home-assistant/architecture (dedicated architecture repo + Discussions → ADR), NixOS/rfcs (PR-based RFCs), Astro (staged discussions → RFC PR → living doc) | markcuda omarchy-kids-mode research | agent-ops as docs hub; per-repo docs/research/ |
| Game studios: searchable wikis (rarely deleted, project-grouped), TDD split into granular docs, "research light, recordings are definitions", docs open/online/visual not Word | arxiv 1101.5833; Jagex (mcvuk) | hub + granular per-repo docs |
| Docs generators: mkdocs-material wins for our shop (Python, 1 pkg, live-reload + search in dev, GitHub Pages, Mermaid native) vs Docusaurus (Meta, ~3,400 npm pkgs, build-only search) vs Starlight/Rspress | hackmamba.io 2026; joeledwardson dev-setup ADR-008 | ✅ wired: mkdocs.yml + docs/ symlinks + .github/workflows/docs.yml (Pages) |
| PKM tools: Logseq (AGPL-3.0, open source, outliner, block-addressable — best for LLM-written content) vs Obsidian (proprietary, 4,500+ plugins, better for long-form); both local-first markdown + git | mehmetgoekce llm-wiki; freshtechtips 2026 | convention: plain markdown + git + [[wikilinks]] (no app needed for agents) |
| Zettelkasten: atomicity (one idea per note), unique addressing, dense interlinking via [[wikilinks]]; distributed teams = shared workspace + linking conventions + knowledge gardening | jqueiroz notenav; taskade.com; Luhmann 90k cards | [[wikilink]] cross-reference convention in RESEARCH-CONVENTIONS.md |
| Dedupe lesson: "the URL is an attribute of the copy, not the entity — dedupe on normalized content fields; treat URLs as provenance, not identity" | dev.to imapphelp | research-check.sh + index-first rule (check before researching) |

## Pulled 2026-10-16 — Console homebrew/RE toolchains + build systems/CI

| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| psprecomp (Allegrex→C static recomp) | sp00nznet/psprecomp | MIT | game-reverse-engineering docs/toolchains/psp.md + tooling/console-toolchains/install.sh | ✅ wired (built, 10/10 ctest pass; needs `-lm` — upstream CMake gap) |
| dolphin-memory-engine-fork (Dolphin live-memory R/W) | PyPI | MIT | pip recipe in install.sh; tooling/console-toolchains/dolphin-memscan.py | ✅ wired (v2.1.3 import + API verified) |
| game-ci template (Godot export + Blender headless + asset gates) | original (2026 patterns) | ours | agent-ops ci-templates/game-ci/ | ✅ wired (asset_gates + blender_smoke tested on VM) |
| PS2SDK/ps2toolchain (ps2dev) | ps2dev org | AFL-2.0 / BSD-2-Clause / MIT | install recipe (prebuilt tarball) | 📄 documented (Urban Reign lane) |
| pspsdk/pspdev | pspdev org | BSD | install recipe (docker pspdev/pspdev:latest) | 📄 documented (Tekken 6 PSP lane) |
| devkitPPC r50 + libogc 3.1.0 / libogc2 | devkitPro / extremscorner | verify in repo | install recipe (dkp-pacman) | 📄 documented (WMXIX lane) |
| libdragon (GCC 16, rdpq, n64.mk) | DragonMinded/libdragon | verify in repo | install recipe (toolchain-continuous-prerelease) | 📄 documented (No Mercy lane) |
| NxDK + ghidra-xbe + extract-xiso | XboxDev org | verify in repo | install recipe | 📄 documented (SCII Xbox lane) |
| mcp-ppsspp (PPSSPP debugger MCP) | dmang-dev/mcp-ppsspp | verify before wiring | docs/toolchains/emulator-debuggers.md | ⏸️ queued (license unconfirmed) |
| PSPRecomp | jessicanataliagta/PSPRecomp | verify before wiring | docs/toolchains/psp.md | ⏸️ queued (license unconfirmed) |
| cth9191/blender-to-web | — | rights reserved | referenced only | ❌ excluded (no reuse license) |

Research docs: game-reverse-engineering `docs/toolchains/` (README + ps2/psp/gamecube-wii/n64/xbox/emulator-debuggers/build-systems-2026/ci-game-repos).
