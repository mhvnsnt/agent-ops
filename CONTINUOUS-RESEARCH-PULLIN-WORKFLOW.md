# Continuous Research + Pull-In Workflow

**Law:** CONTINUOUS RESEARCH + PULL-IN LAW (owner 2026-10-16 ~12:36 EDT) — in ~/AGENTS.md.
**Coordinator agent:** spawned 2026-10-16 ~12:36 EDT (research + pull-in across all domains).

## The directive (owner's words)
"Keep doing deep research on everything related to anything we've talked about or any of the work we got going and keep pulling in open source stuff or anything you find. Keep vertically and horizontally branching and expanding everything. Pull it in, wire it up, get it pushed green without breaking anything or clobbering anything on any side or destroying any work that's been done."

## Workflow
1. **Research first** — GitHub trending, 2026 roundups, Hacker News, papers. Never guess from training data (RESEARCH-BEFORE-ANSWER LAW).
2. **Pull in** — open source first. Non-open-source: document license status honestly; do NOT crack commercial software or bypass paywalls. Precedent: Cape Jones LICENSE EXCLUSIONS (MiniMax H3 region-excluded, Wav2Lip non-commercial, Fish Speech weights non-commercial — documented, NOT pulled).
3. **Wire up** — install, test, document in the repo it belongs to.
4. **Push green** — branch → PR → merge, ONLY when green + non-destructive. Conflicts keep both sides. Red CI stays open with a comment naming the blocker. Never rebase/squash/force-push.
5. **PULL-STRAIGHT-TO-STORE** — clone into repo checkouts, wire up there, push. Local disk is transient work only.
6. **Log** — what was pulled, source URL, license, where it landed.

## Domains (vertical + horizontal branches)
- 3D: renderers, converters, retargeting, rigging, T-pose pipelines, image-to-3D
- Animation: interpolation, inbetweening, mocap, cartoon pipelines
- Game engines: production-grade, legacy, 2026 new/acclaimed
- Video: upscalers, restoration, frame interpolation, encoding
- Audio/voice: TTS, voice cloning, SFX
- Teardown/RE: Ghidra scripts, format parsers, console tooling
- Web/playable: Three.js, game frameworks

## Priority order
Highest-value gaps in current pipelines first (render speed, Source/XPS conversion, TTS/voice, teardown tooling), then branch outward continuously.

## Standing rules that govern this work
- NO-LAZY-WORK LAW — best quality, no shortcuts, research everything
- NO-HAND-TOOLING LAW — proven tools over hand-rolled hacks
- MERGE-IT-YOURSELF LAW — merge when green, never leave open
- NO-SWEEP-INFLIGHT / NEVER-KILL-IN-PROGRESS — never touch in-flight work
- NO-DISK-STAGING / WORK-SMARTER — repos are the workbench
