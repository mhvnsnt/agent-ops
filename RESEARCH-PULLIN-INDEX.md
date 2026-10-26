# RESEARCH → PULL-IN INDEX

Master index of every research topic: where the doc landed (repo + path), what was pulled in from it, or why not.
Owner rule 2026-10-16: a finding without a pull-in is incomplete — track until wired or explicitly excluded with license reason.

## Active research branches (2026-10-16)

| Branch | Topics | Research doc → repo | Status |
|---|---|---|---|
| 3D pipeline | image-to-3D (TRELLIS/Hunyuan3D/SF3D…), Source/XPS→GLB Linux, render speed, auto-rigging | → western-heart docs/research/3D-PIPELINE-2026.md ([PR #206](https://github.com/mhvnsnt/western-heart/pull/206), branch 3d-pipeline-doc) | Doc committed+pushed 2026-10-16; Phase 2 pulls next |
| Audio/voice/music | TTS/VC 2026, SFX gen, open music gen, vocal restoration | → cape-jones docs/research/AUDIO-VOICE-MUSIC-2026.md + western-heart docs/research/CHARACTER-VOICE-2026.md | ✅ Wired (2026-10-16) |
| Teardown/RE + engines | QuickBMS/Ghidra/console tooling, Noesis, Godot/Bevy/Unreal/legacy engines, web frameworks | → game-reverse-engineering branch research/re-tooling-20261016 (9 tools, docs, PULL-LOG.md — PR #10 OPEN, awaiting CI fix) + western-heart branch research/engine-survey-20261016 (PR #214 MERGED) | ✅ Pulled + wired, all on origin |
| AI/ML inference | local LLMs, GGUF/quantization, diffusion on T4, LoRA/QLoRA | → cape-jones `docs/research/AI-INFERENCE-HARDWARE-2026.md` + `tools/inference/` (vendored ComfyUI-GGUF Apache-2.0 pinned 6ea2651e, kaggle-llm-server.sh, inference_client.py mock-tested, comfyui-t4-runbook.md URLs verified, qlora-t4-runbook.md, 2 verified ComfyUI workflows, PULLIN-LOG.md) + western-heart `docs/research/AI-INFERENCE-GAMESIDE-2026.md` + `tools/ai-inference/` (client + serve-config) | ✅ Pulled + wired ([cape-jones#36](https://github.com/mhvnsnt/cape-jones/pull/36) merged 2026-10-16, [western-heart#212](https://github.com/mhvnsnt/western-heart/pull/212) merged 2026-10-16 all CI green). Excluded: FLUX weights (non-commercial, URL-only), XTTS-v2 (non-commercial), F5-TTS (CC-BY-NC), Wan2GP (no license). Open: real-GGUF llama-server e2e, first T4 GPU workflow runs (need GPU lane) |
| Procgen + asset pipelines | PCG levels/chars/textures, USD, glTF extensions, material systems | → western-heart docs/research/procgen-asset-pipelines/ | ✅ MERGED (PR #213) |

## Procgen + asset pipelines — merged 2026-10-16 (western-heart PR #213)

Research docs: `docs/research/procgen-asset-pipelines/` (01–07 + README + PULL-LOG).
Wired: `tools/procgen/` (gltf-delivery, game-score, arena-gen, textures, usd).

| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| gltfpack | zeux/meshoptimizer | MIT | tools/procgen/gltf-delivery/ | ✅ wired (22M→20M verified) |
| glTF-Transform | donmccurdy/glTF-Transform | MIT | tools/procgen/gltf-delivery/wh_attire_variants.mjs | ✅ wired (P1/P2 KHR_materials_variants, 46/46 prims) |
| Tone.js | Tonejs/Tone.js | MIT | tools/procgen/game-score/ | ✅ wired (21/21 node tests) |
| Material Maker | RodZill4/material-maker | MIT | tools/procgen/textures/wh_material_maker_export.sh | ✅ wired (CLI verified) |
| TEXTtoPBR algos | Vasco888888/text-to-pbr | MIT | tools/procgen/textures/wh_seamless_pbr.py | ✅ wired (boundary 113.3→0.0) |
| GDQuest PCG concepts | gdquest-demos/godot-procedural-generation | MIT (code) | tools/procgen/arena-gen/ | ✅ wired (mirrored/deterministic) |
| Blender USD IO | Blender built-in | — | tools/procgen/usd/ | ✅ wired (4.0.2 → .usda) |
| MakeHuman | makehumancommunity | AGPL-3.0 | documented only | ❌ excluded (copyleft; use don't fork) |
| MB-Lab | animate1978 (archived 2024) | GPL-3.0 | documented only | ❌ excluded (unmaintained) |
| MIDI-GPT | Metacreation Lab | MIT code, non-commercial models | documented only | ❌ excluded (model terms) |
| Melodrive cracks | — | commercial | — | ❌ excluded (never crack) |

Decisions: USD for authoring/archival, glTF for web delivery; metal/rough only; OpenPBR tracked.
Note: branch `3d-pipeline-research-pullin` (orphaned from main) still holds the sibling's
3D-pipeline doc + tpose-refs deletions — parent to triage separately.
| Netcode/multiplayer | rollback (GGPO/Godot), WebRTC, matchmaking, cloud streaming | → western-heart `docs/research/netcode-multiplayer-streaming.md`, `game/netplay/` (lite-rollback 1.2.1 + webrtc 1.1.0 MIT, fighter-sim, mirror.mjs ALL PASS, demo, signaling server), `tools/netcode/` (netfox + snoringcat-rollback + nakama-client MIT/Apache-2.0, Nakama compose, Sunshine/Moonlight guide), PULLIN log at `tools/netcode/PULLIN.md` | ✅ Pulled + wired (PR #202 merged 2026-10-16, all CI green) |
| Console homebrew + CI | PS2/PSP/GC/N64/Xbox SDKs, emulator debuggers, CI templates | → game-reverse-engineering docs/toolchains/ (ps2/psp/gamecube-wii/n64/xbox/emulator-debuggers/build-systems-2026/ci-game-repos) + tooling/console-toolchains/ (install.sh, dolphin-memscan.py) | 🔄 Pulled + tested (psprecomp 10/10 ctest MIT, dolphin-memory-engine-fork verified, game-ci template: asset_gates + blender_smoke real PNG) — PR #9 (game-rev-eng) + PR #30 (agent-ops) OPEN, red CI (repo-wide no-deletion-guard broken since 2026-10-15, blocker comments posted). Excluded: blender-to-web (rights reserved). Licenses to verify: libdragon, NxDK, ghidra-xbe, extract-xiso, libogc, PSPRecomp, mcp-ppsspp. |

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

### Voice / TTS / audio — 2026-10-16 pull (audio-voice-2026)
| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| F5-TTS (fast zero-shot TTS, bulk ADR) | SWivid/F5-TTS | MIT | cape-jones production/pipeline/audio-2026/ + dialogue_pipeline.py engine; PR #35 merged | ✅ wired |
| CosyVoice 3 (cross-lingual EN↔JA clone + instruction emotion) | FunAudioLLM/CosyVoice | Apache-2.0 | cape-jones production/pipeline/audio-2026/ + dialogue_pipeline.py engine; PR #35 merged | ✅ wired |
| audio.cpp v0.9.2 (GGUF engine: TTS/VC/ASR/VAD/diarize/separate) | 0xShug0/audio.cpp | Apache-2.0 | cape-jones production/pipeline/audio-2026/; PR #35 merged | ✅ wired |
| DiffRhythm (lyrics→full song, 8GB VRAM T4-ready) | ASLP-lab/DiffRhythm | Apache-2.0 | cape-jones production/pipeline/audio-2026/; PR #35 merged | ✅ wired |
| voice-changer (real-time VC rig, create-a-fighter) | w-okada/voice-changer | MIT | cape-jones production/pipeline/audio-2026/ + western-heart tools/character-voice/; PRs #35 + #208 merged | ✅ wired |
| python-audio-separator (vocal/instrument stems) | nomadkaraoke/python-audio-separator | MIT | cape-jones production/pipeline/audio-2026/; PR #35 merged | ✅ wired |
| DeepFilterNet (de-reverb/denoise, phone lines) | Rikorose/DeepFilterNet | MIT/Apache-2.0 dual | cape-jones production/pipeline/audio-2026/ + western-heart tools/character-voice/phone_cleanup_chain.py; PRs #35 + #208 merged | ✅ wired |
| resemble-enhance (speech polish) | resemble-ai/resemble-enhance | MIT | cape-jones production/pipeline/audio-2026/ + western-heart phone_cleanup_chain.py; PRs #35 + #208 merged | ✅ wired |

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
| TripoSR | VAST-AI-Research/TripoSR | MIT | western-heart tools/triposr/ ([PR #209](https://github.com/mhvnsnt/western-heart/pull/209)) | 🔄 PR open (research PR #206) |
| Stable Fast 3D (code) | Stability-AI/stable-fast-3d | Stability Community License (<$1M/yr) | western-heart tools/stable-fast-3d/ ([PR #211](https://github.com/mhvnsnt/western-heart/pull/211)) | 🔄 PR open, weights queued |
| 3D-PIPELINE-2026 research | — | — | western-heart docs/research/3D-PIPELINE-2026.md ([PR #206](https://github.com/mhvnsnt/western-heart/pull/206)) | 🔄 PR open |
| SPAR3D (code) | Stability-AI/stable-point-aware-3d | Stability Community License (<$1M/yr, LICENSE.md vendored) | western-heart tools/spar3d/ (branch 3d-pull-spar3d, 83 files) | 🟡 committed locally — push blocked by GitHub 500 incident 2026-10-16; retry push then open PR |
| XNALara-io-Tools | Valerie-Bosco/XNALara-io-Tools | GPL-3.0 (bundled ALX modules; no top-level file) | western-heart tools/xps-io/ (branch 3d-pull-xpsio, 141 files) | 🟡 committed locally — push blocked by GitHub 500 incident 2026-10-16; retry push then open PR |

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
| YuE2-3B weights | CC-BY-NC-4.0 (HF API verified 2026-10-16) — best open song quality, research/internal only |
| TangoFlux (best open text-to-SFX 2026, ICLR 2026) | Stability AI Community License = non-commercial research-only (repo README verified) |
| Auffusion | Code Apache-2.0, checkpoints CC BY-NC-SA 4.0 — research only |
| IndexTTS2 | Bilibili Model Use License Agreement — commercial needs written permission |
| XTTS | No v3 exists (2026-10-16); CPML non-commercial; Coqui defunct 2024 |
| seed-vc | GPL-3.0 copyleft — MIT voice-changer covers the slot |
| Parler-TTS | Apache-2.0 but stale since 2024-12-10; superseded by Chatterbox |
| Qwen3-TTS | Skipped — upstream take-to-take instability confirmed unfixed |
| MusicGen (Meta) | CC-BY-NC 4.0 |

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

## Mocap + camera-match wave — 2026-10-19 (cape-jones PR #163 MERGED)

Research driver: 3D animation automation directive — real human motion for sitting/acting (hand-posing kept reading robotic). Researched via live web (research.py remote calls down).

| Tool | Source | License | Landed | Status |
|---|---|---|---|---|
| FreeMoCap | freemocap/freemocap (2.0.0-alpha.25) | AGPL-3.0 (disclosed honestly) | cape-jones `production/tools/freemocap/` | ✅ wired — markerless mocap from 2+ webcams/phones, Blender export; sparse pull (core pkg + README/LICENSE/CITATION/pyproject); install at runtime via `pip install freemocap` |
| fSpy-Blender | stuffmatic/fSpy-Blender v1.0.3 | GPL-3.0 | cape-jones `production/tools/fspy-blender/` | ✅ wired — .fspy → solved Blender camera; new `install_fspy_blender.py` (py_compile-clean, --help, dry-run verified vs Blender 4.0.2); fSpy app itself (Electron) NOT vendored — fetch from fspy.io |

## Friction research — CI PAIN (cluster 3/6, 2026-10-19)

Research doc: agent-ops `research-friction-20261019/03-ci-flakes.md` (dedupe: TEAM-RESEARCH-2026-10-19 flagged Oracle ARM + self-hosted runner; this is the deep verification).

| Finding | Status |
|---|---|
| CloudDog sqlite flake root cause: WAL + busy_timeout=30000 already set; DEFERRED lock-upgrade bypasses busy_timeout; per-open schema DDL stampede in 20-thread test → fix = BEGIN IMMEDIATE + app-level retry + serialized schema init (Plan A) | ✅ **LANDED 2026-10-20 (pull-in 2/6)** — PR mhvnsnt/CloudDog-Muse-Storage-Disc-Assistant#41 merged (f0cdcff, CI green 3.11/3.12 + lint + bulk-delete gate). BEGIN IMMEDIATE via `_write_txn` on all write paths + `_retry_locked` backoff + serialized schema init; CI round 1 exposed a second mechanism (per-open `journal_mode=WAL` transition bypasses busy_timeout too) — WAL now set once inside serialized init; load repro 100/100 rounds clean, concurrency test 20/20, cross-process stress 200/200. pytest-rerunfailures deliberately NOT added (hides a real race). |
| CI minute diet: concurrency cancel, path filters, timeout-minutes, matrix trim, caching, retention (Plan B) | 📄 researched — fold into merge-law-ci-watch lane |
| Self-hosted GitHub runner $0/min; Oracle ARM box 2 OCPU/12GB (halved Jun 2026), idle reclaim + capacity errors; card required at signup = OWNER decision (Plan C) | 📄 researched — blocked on owner decision |
| Skipped: pytest-rerunfailures as fix (hides a real daemon race), SourceHut/Cirrus/Codeberg/CircleCI/GitLab/Jenkins/Woodpecker-hosted (paid, OSS-only, FLOSS-mission, or metered) | ❌ excluded, reasons in doc |

## Friction research — full cluster sweep (2026-10-19)

Owner order 2026-10-19 ~23:03 CDT. Consolidated report: agent-ops `FRICTION-RESEARCH-2026-10-19.md`. Six cluster docs in `research-friction-20261019/`. All wire-ups queued (not PR'd) — code targets have a live straight-to-store lane + running daemon in them; integration after check-before-start. Cross-cluster: clusters 4+5 converged on one claim format — integrate once.

| Cluster | Headline | Status |
|---|---|---|
| 01-resilient-transfer | `gh` does NOT retry (confirmed live); fix = stdlib `retry.py` (exponential+jitter, transient/permanent classifier) + `_proxy_env()` sanitizer (TOOLS.md no_proxy IPv6 quirk) + aria2/curl/rclone flag bundles, all wired into the GitHub backend's `_run_gh` (8 attempts, 2s→120s + jitter, redacted proxy endpoint logging) | ✅ LANDED 2026-10-20 ~00:45 CDT — PR mhvnsnt/CloudDog-Muse-Storage-Disc-Assistant#40 merged (daf88af, CI green 3.11/3.12 + lint + bulk-delete gate). Live smoke: real 2MB upload + verify() True. **SPLIT_BYTES removed from this lane's scope by owner decision 2026-10-19 ~23:48 CDT (100MB as the single standard for store()/mirror everywhere is now its own dedicated lane; never touched here — no revert needed).** |
| 02-github-limits | Releases unmetered per GitHub docs (no total-size/bandwidth cap); git-lfs hard NO (metered); manifest-first finalization into law; bounded-parallel uploads | queued — CloudDog integration lane |
| 04-lane-resilience | At-least-once + idempotent units; fencing-epoch checkpoints; progress vs heartbeat split; systemd verified unavailable on this VM | ✅ **LANDED 2026-10-20 ~01:25 CDT (pull-in 5/6)** — checkpoint.sh: fencing-epoch claims + stale-epoch write guard (exit 3), progress_seq/last_progress_at, step_keys, append-only journal.jsonl, fsync hardening; supervisor.sh: STUCK bucket (heartbeat fresh + progress frozen 2 ticks → surfaced, never auto-re-spawned), --no-track read-only, --stuck-ticks; worker-watchdog cron: new 9b STUCK-check step; wild-schema crash in supervisor fixed (14 hand-written malformed checkpoints no longer crash the reader); SOP `LANE-RESILIENCE-SOP.md`; 19 unit tests green (`tests/test_checkpoint_resilience.py`); docs updated (CHECKPOINT_PROTOCOL.md, RESUME_BRIEF_TEMPLATE.md) |
| 05-lane-coordination | `claims` table in existing sqlite registry (owner/action/claim_id/epoch/TTL+heartbeat); hard gates in reaper paths; `clouddog claims check` CLI — the T5 fix | ✅ **LANDED 2026-10-20 (pull-in 2/6)** — PR mhvnsnt/CloudDog-Muse-Storage-Disc-Assistant#43 merged (70d91d7; checks: bulk-delete-gate + test (py3.12) green — CI workflow was slimmed to PR-leg-only by another lane mid-flight, see note). Claims table + claim/heartbeat/release/get/list/expire API (sqlite-only by design, no JSON mirror), fencing via claim_id + per-path epoch, TTL+heartbeat leases; hard gates in `reap_candidates()` (both cmd_reap paths), `Reaper._try_reap` (always wired by src CLI), `claim_gate` fails CLOSED on unreadable store; CLI: `cloud_dog.py claims {claim\|check\|heartbeat\|release\|list\|sweep}`, `clouddog claims check`, `python -m clouddog.claims check` (exit 0 = BLOCKED, 1 = free). +22 tests; full suites green on the merged tree (69 non-v1, 246 v1 incl. stream-lane tests; lint scope clean); live smoke: scan + dry-run reap clean, full claims lifecycle verified against the live registry DB (claim→BLOCKED→heartbeat→release→FREE, stale heartbeat rejected). **Note:** the stream lane merged PR #42 into main mid-flight — conflict in `src/clouddog/cli.py` resolved forward keeping both sides (their `cmd_stream` + my `cmd_claims`), full matrix re-verified on the merge commit. No fresh CI runs attached to the conflict-resolution merge push (GitHub started no workflow runs for that push; unknown cause, possibly maxed Actions minutes) — the merged tree was instead verified with the full local test matrix + lint + live smoke, all green. Deliberately deferred: v1 Daemon `_delete_local` ungated (it only deletes what it stored+verified itself in the same tick — claim owner by construction); lane-claim-on-dispatch wording for briefs/protocols is an agent-ops docs follow-up. |
| 06-browser-transfer | No rclone TeraBox backend exists (verified); AList→WebDAV→rclone is the pull path (AGPL, service use only); ✅ **rclone LANDED 2026-10-19 ~23:55 CDT** — v1.75.2 official static binary, SHA256-verified against rclone.org (`ed7ab1f17876…` matches zip from downloads.rclone.org/v1.75.2), persistent path `~/workspace/tools/rclone/rclone` (present since 2026-10-17; `which rclone` fails — NOT on PATH); smoke test `rclone copy` + `rclone check` local-dir clean (0 differences); `drive.py` resolves via `shutil.which("rclone")` — PATH/RCLONE_PATH wiring + Drive OAuth remain for CloudDog lane; cookie→aria2 SOP | ✅ landed (binary) — PATH wiring + Drive OAuth stay with CloudDog integration lane |
| 06-note | 03-ci-flakes section above is cluster 3/6 of this same sweep | (see above) |

Queued pull-ins 1–18 tracked in `FRICTION-RESEARCH-2026-10-19.md` (consolidated pull-in queue table). Owner decisions: Oracle ARM signup (card), Modal credits (card).

## Friction research — web-game load time 126s (2026-10-25)

Play-verify run 18: fight goes live +126s after stage confirm, 4 missing assets (404s). Research doc: agent-ops `research-friction-20261025/02-load-time-126s.md`. Research + doc only — no game code touched, no PRs. Live probes this pass: `deploy-manifest.json` is summary-only (7,181 files / 5,647,298,304 B — no per-file list); GitHub Pages returns HTTP 206 + `accept-ranges: bytes` (Range works); Pages `cache-control: max-age=600`.

| Candidate | Headline | Status |
|---|---|---|
| KTX2/BasisU via gltfpack `-tc` + shared `KTX2Loader` | Textures are the remaining uncompressed bulk after meshopt `-cc`; Flight Helmet −31.8% total, −83.5% color maps; ETC1S color / UASTC normal, POT resize, own-eyes compare per fighter | queued — western-heart game lane, AFTER the §5 measurement confirms network/texture-bound |
| Draco geometry compression | SKIP — meshopt already wired and decodes faster (1–3 GB/s SIMD); Draco is the slowest loader per Khronos' own deck | excluded |
| @needle-tools/gltf-progressive | MIT lib; 17.4 MB → 715 KB first paint, but needs LOD-processed assets via Needle Cloud (free tier 30 opts) | queued — evaluate for stage scenes only, not fighters |
| Preload next fight during current fight | Own glue, no dependency — cheapest cut to perceived load | queued — western-heart game lane |
| Service worker + Cache Storage (Workbox preferred, Apache-2.0) | Pages HTTP cache is only 10 min; SW cache is the durable layer; Workbox precache manifest doubles as the asset verifier | queued — western-heart game lane |
| Manifest-based 404 verification | No lib exists (SRI doesn't apply to fetch/GLB) — own ~100-line glue; precondition: extend `build_pages.py` to emit per-file manifest | queued — western-heart game lane (+ deploy-script change) |
| Load instrumentation in `loadperf.js` + `?loadreport` | No three.js load profiler exists; marks around fetch/parse/decode/compile/first-render + Resource Timing; stats-gl (MIT) as dev-only overlay | queued — FIRST, before any compression work; the 126s is unmeasured |
| three.js r18x / WebGPU migration | r186 has no GLB-load-path change (verified against release notes); WebGPU changes the renderer, not the loader | excluded for this problem — tracked separately |

## Friction pull-in 6/6 — browser-transfer docs (2026-10-20, DOCS ONLY)

Owner integration order 2026-10-19 ~23:33 CDT. No code, no installs, no deploys in this item.

| Doc | Covers | Status |
|---|---|---|
| agent-ops `BROWSER-TRANSFER-COOKIE-ARIA2-SOP.md` | Queue #17 (cookie→aria2/curl SOP: local-only cookie export, `aria2c -c -x16 -s16 --load-cookies`, curl `-L -f -C - -b` fallback, hash verify, TeraBox .blend 10/10-failure worked example) + queue #18 (yt-dlp `-g` / gallery-dl `-g` as the direct-link lane standards, when to reach for each) | 📄 documented — every flag verified against the real manpages/options + local `curl --help`; `tools/dl/tb-pull.sh` script itself stays with the CloudDog integration lane |
| agent-ops `ALIST-TERABOX-WEBDAV-EVALUATION.md` | Queue #16 evaluation: AList (AGPL-3.0, verified from upstream README), native TeraBox driver (cookie + jsToken + sign, `drivers/terabox/`), TeraBox→AList→WebDAV→rclone bridge, rclone webdav remote syntax verified against the landed v1.75.2 binary's own `--help` | 📄 evaluated — **SERVICE USE ONLY, deployment BLOCKED on owner's word** (AGPL + hosted-service implications); end-to-end bridge test happens at deploy time |

## Friction pull-in 7/7 — OWNER DECISIONS: 100MB single standard + full re-download verify (2026-10-20)

Owner decisions 2026-10-19 ~23:48 CDT ("Yes and yes for now"). Lane worked in isolated clone `~/workspace/_pullin/clouddog-owner-decisions/` (the live `~/workspace/cloud-dog` tree + running daemon were never touched).

| Item | Covers | Status |
|---|---|---|
| 100MB single standard | One constant: `CHUNK_BYTES = 100 * 1024 * 1024` in `src/clouddog/stores/base.py`. Consumers: GitHub backend `SPLIT_BYTES` (was hardcoded 2_000_000_000; `store()` now splits anything >100MB into 100MB parts; `MAX_ASSET_BYTES` 2GB kept as the documented platform ceiling + assert), `cloud_dog.py` mirror `PART_BYTES` (`--part-mb` default derives from it; asserted equal by test), `src/clouddog/streamer.py` `DEFAULT_CHUNK_BYTES` (landed on main via PR #42 mid-flight; standardized via forward merge + alias, was a private 100MiB copy) | ✅ **LANDED 2026-10-20** — PR mhvnsnt/CloudDog-Muse-Storage-Disc-Assistant#44 merged (CI green: bulk-delete-gate + test py3.12 incl. lint; zero file deletions; forward-merged PRs #42/#43 keeping both sides). Tests: `tests/v1/test_owner_decisions.py` (constant equality across all 4 paths, real `split` at the constant, no oversized split literals in chunking code). Live smoke: 150,000,123-byte file split live into part-aa = exactly 104,857,600 B + part-ab = 45,142,523 B; the parts' `gh` upload stalled on the egress proxy (fleet congestion, left running per NEVER-KILL-IN-PROGRESS; backend 7200s timeout + retry owns it) |
| Full re-download verify, every time | `cloud_dog.py verify_github_asset` now routes through the PR #37 retrievability prover (full pull-back + sha256); the release-API name+size+digest shortcut is removed. TeraBox/Kaggle/B2/restic cloud_dog verify paths + `src/clouddog/stores/terabox.py::verify()` FAIL CLOSED with exact reasons (no byte-level re-download wired for those backends). Mirror no longer treats upload-success as verification (kaggle/terabox parts route through the fail-closed verifies). v3 `clouddog/stores/drive.py::verify()` re-downloads via rclone + sha256 (was lsjson size-only). Daemon store-verify covered via backend `verify()` (github already re-downloaded; terabox now raises → daemon keeps local) | ✅ **LANDED 2026-10-20** — same PR #44. Live smoke (release `smoke-ownerdecisions-small-20261020` on mhvnsnt/clouddog-storage): store OK → prover `proven: True, bytes_fetched: 1000000, hash_matched: True` → `verify_github_asset` correct-sha TRUE → tampered-sha FALSE with "sha256 mismatch after pull-back". **Consequence (intended by the decision): terabox/kaggle/b2/restic lanes can store but never auto-clear local copies until byte-level re-download verify is wired for those backends.** Deferred follow-ups (new lanes, not this one): byte-level verify for terabox/kaggle/b2/restic in the prover; aider/copilot/gemini CLIs not installed on this VM (noted per reporting rules) |

## CloudDog governance / training research (2026-10-20)

Owner correction 2026-10-20: CloudDog was "fed" for deleting (bytes freed = reward) instead of trained on correct behavior; two deletions of unstored work resulted (Tekken 5 ISO partial, tripo-wire folder). Research doc: CloudDog repo `docs/GOVERNANCE-TRAINING.md` ([PR #47](https://github.com/mhvnsnt/CloudDog-Muse-Storage-Disc-Assistant/pull/47) MERGED 2026-10-20, merge commit 1d571b4, bulk-delete-gate green; docs-only so the path-filtered test workflow did not trigger). Status PROPOSED like `docs/THRESHOLDS.md` — no behavior changed; build steps await owner approval of the grade vocabulary + ladder parameters.

| Finding / candidate | Source (license) | Applied |
|---|---|---|
| Reward hacking / Goodhart: bytes freed was a proxy that diverged from the true objective (verified-safe storage) | Amodei et al. 2016 via Wikipedia "Reward hacking" | 📄 documented — NO-PROXY rule proposed as law: bytes freed = telemetry only, never a grade / promotion input / cron success condition |
| OPA/Rego (sidecar/Go-lib only, no Python embedding) | Apache-2.0 | ❌ not pulled — ✅ adapt: decision/enforcement split + decision logs on every `policy.evaluate()` / gate verdict |
| AWS Cedar (Rust/Go, no mature Python binding in sources reviewed) | Apache-2.0 | ❌ not pulled — ✅ adapt: principal–action–resource grammar, default-deny, forbid-trumps-permit for `policy.py` |
| Casbin (pycasbin) | Apache-2.0 | ❌ excluded — multi-subject authz; CloudDog's hard questions are temporal/evidentiary (verified-this-run, claim-live, bytes-bind) |
| durable_rules | license NOT verified in sources reviewed | ❌ excluded regardless — C-extension Rete engine, oversized for ~12 rules, breaks single-reader auditability |
| Inspect (UK AISI) dataset/solver/scorer + re-scorable eval logs | MIT | ❌ not pulled into daemon — ✅ adapt shape for the regression-test-per-incident corpus |
| promptfoo CI gate (`check --pass-rate`, non-zero exit blocks PR) | MIT | ❌ not pulled — ✅ adapt gate form at a 100% bar for safety cases |
| Langfuse trace+score persistence; production failure → regression test workflow | MIT core (enterprise modules separate) | ❌ not pulled (no grade export off-host) — ✅ adapt workflow + persistence shape |
| Trust ladder: shadow → supervised → scoped → full; promotion as typed, evidence-gated decision; error budget as autonomy throttle / freeze | clouatre.ca SRE-for-AI-agents; Rootly AI SRE; Google SRE Workbook error-budget policy; CSA NIST AI RMF Agentic Profile | ✅ adapt (core recommendation) — rungs = existing CloudDog modes; `violation` → automatic rung 0; near-miss budget 3/30d → one rung (proposed, uncalibrated); re-earning by graded clean streak, never by clock |
| Scorecard grades: `correct` / `blocked` (positive!) / `violation` / `near_miss` / `error`, per actor × action-kind × window; grade the trace, not just the outcome | Inspect CORRECT/INCORRECT + deterministic-first harness practice | 📄 proposed — step 1 journal attribution (`actor`/`invocation_id`/`grade`/gate legs on `AuditEvent`), step 2 `scorecard` registry table + `clouddog score` CLI |
| Hash-chained audit journal + external head anchor; bare chain alone only proves self-consistency | SOC 2 audit-log write-ups; pipelab "What a Hash Chain Can't Prove" | 📄 proposed — stdlib `hashlib`, canonical JSON, anchored (head, length) committed to the CloudDog repo on guardian cadence |
| Circuit-breaker per-run caps, two-signal rule, kill switch at delete time, choke-point invariant test | Nygard/Fowler circuit breaker; NIST SP 800-12 separation of duties; Rootly autoremediation governance | 📄 proposed — choke point itself already landed (PR #45 `delete_gate.py`); this research defends + extends it |

## TorBox breakthrough research (2026-10-20)

Report: `~/workspace/agent-ops/TORBOX-BREAKTHROUGH-2026-10-20.md`. Root cause of the months-long BAD_TOKEN failure: vault credential placement is `query_param: token`, so Bearer calls sent the literal surrogate; the key was never dead. `requestdl?token=` + CDN Range reads work on the current plan (live-proven). Documents.zip central directory fully parsed (79,772 entries, all STORED) → `torbox-documents-cd-manifest.jsonl`; extraction pipeline running from `agent-ops/torbox-cd-work/extract_dir.py`.

| Finding / candidate | Source (license) | Applied |
|---|---|---|
| TorBox OpenAPI spec (87 paths, sole scheme OAuth2PasswordBearer; only requestdl/rss/getstreamdata take ?token=) | torbox.app official API (public spec) | ✅ wired — connector fix list in breakthrough report §1 (CONNECTOR.md rewrite, tb_reqdl redaction, second bearer entry if ever needed; do NOT regenerate the key) |
| tb_cdn_range_probe.py health probe (statuses/host only, no secrets) | Lane 6, this program | ✅ LANDED in `~/workspace/custom-connectors/custom.torbox/bin/` |
| GitHub Actions range-extraction matrix (public runners, token-as-secret refinement) | Lane 4 prototype, MIT-able own code | ✅ prototype at `agent-ops/torbox-gha-prototype/` (CRC/sha verified vs public Zip64); bulk-pull deployment is the next step in breakthrough report §6 |
| torbox-api Python SDK 1.0.6 | PyPI (official) | ❌ not adopted — tested live; no advantage over raw calls, drops error bodies, no UA |
| rclone debrid backends | rclone 1.75.2 docs/binary | ❌ no TorBox/RD/AllDebrid backend exists; premiumizeme only — downstream glue only |
| Decypharr (Go, MIT, 917★) | GitHub sirrobot01/decypharr | 📄 documented — production-grade TorBox mount candidate post-connector-fix; unnecessary for the range pipeline |
| AllDebrid / Debrid-Link as backup debrids | official APIs (Lane 2 live probes) | 📄 documented — both need one browser login to mint API keys (vault logins unreachable from sandbox cells); AllDebrid has documented too-big failure modes |
| Free-trial seedboxes (Seedhost/Pulsed/Ultra) | official pages (Lane 7) | ❌ excluded with evidence — trials gone or ≤50 GiB vs 350GB file |

## Friction research — Pages 1 GB deploy limit (2026-10-25)

Doc: `agent-ops/research-friction-20261025/01-deploy-pages-limit.md` (local only until a lane pushes; no PR opened by researcher per task).

| Finding / candidate | Source (license) | Status |
|---|---|---|
| GitHub Pages 1 GB published-site cap confirmed; deploy set 5,969 MB = 5.8× over | docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | 📄 documented — full set can never ship on Pages |
| GitHub Release assets send NO CORS headers (live curl probe 2026-10-26: 302 → release-assets, 200, no ACAO; signed URL ~1 h expiry) — direct browser fetch fails | live probe + corsfix.com | ❌ excluded as runtime CDN (releases stay the store, decided 2026-10-19) |
| jsDelivr serves repo files ≤20 MB with CORS `*` + correct `model/gltf-binary` (live probe); 86 MB GLB 403s; documented 20 MB/file cap | jsdelivr README via deepwiki + live probes | 📄 documented — recommend for small assets only; 176 GLBs >20 MB (5,914 MB) not covered |
| Cloudflare R2 free tier: 10 GB storage, 1M Class A / 10M Class B ops, $0 egress — whole 5,969 MB set fits free | developers.cloudflare.com/r2/pricing | 📄 recommended (1st choice asset host) — needs owner word + lane to wire; signup may ask for payment method (verify) |
| Cloudflare Pages free: 25 MiB/file cap on ALL plans kills 98 GLBs (4,178 MB); 20,000 files/site; unlimited bandwidth | developers.cloudflare.com/pages/platform/limits | ❌ excluded for full set; 📄 shell-only host candidate |
| itch.io HTML5: ≤1,000 files, ≤500 MB extracted, ≤200 MB/file; HTML5 = donations only, selling needs Downloadable; butler 2 GB default (increase on request); payouts Direct (PayPal/Stripe) or Collected ($5 min, 7-day hold, PayPal/Payoneer, tax interview) | itch.io/docs/creators/html5, /faq, /payments.amp | 📄 recommended — money path: shell as HTML5 + R2 lazy-load, payout setup now |
| Netlify free: 100 GB bw/mo, 300 build min, no documented total-size cap; repo already has `game/netlify.toml` proxying to Pages | netlify.com KB + support forum | 📄 alt shell host — bandwidth figure uncertain under 2025 credit system, verify at signup |
| Vercel Hobby: non-commercial only | 2026 pricing roundups | ❌ excluded — disqualifies a money-making game |
| Backblaze B2 free 10 GB + 1 GB/day egress | official pricing via 2026 roundups | 📄 viable fallback if R2 signup blocks |
| Shell-only deploy floor ≈ 70–170 MB (code ~10 MB + UI/portraits ~7.5 MB + 1 stage + 2 fighters + movesets/music) — measured from live git-trees API | live `gh api .../git/trees/main?recursive=1` 2026-10-26 (truncated, lower bounds) | 📄 documented — no content needs cutting, only the deploy splits |
