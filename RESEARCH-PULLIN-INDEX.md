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
| Console homebrew + CI | PS2/PSP/GC/N64/Xbox SDKs, emulator debuggers, CI templates | → game-reverse-engineering docs/ (pending) | Researching |

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
