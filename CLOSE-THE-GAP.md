# CLOSE THE GAP — Free Tools vs Gemini for Production Work

**Date:** 2026-10-10 | **Owner question:** "Why was this so easy with Gemini but ur doing such a bad job, and what free tools close the gap?"

## The honest answer first

Gemini does native multimodal editing: it SEES the image, UNDERSTANDS "the E" contextually, and outputs the edit in one shot. No GPU setup, no masks, no seeds, no iteration.

I work through code: write a script → run → look at output → adjust → repeat. Every step loses information. That's the gap, and no free tool fully closes it — but the right stack narrows it dramatically.

**The key strategic fact:** the heavy free tools need GPU. This VM has none. The owner's GPU map (Kaggle 30 GPU-hrs/wk T4×2, Colab, Lightning AI) is how we run them — not locally, but as API endpoints the agent calls.

---

## CATEGORY 1: Image editing/generation (the direct Gemini replacement)

### P0 — Wire now

**ComfyUI (headless API)** — https://github.com/comfyanonymous/ComfyUI
- What: node-graph diffusion engine. Every UI action = HTTP POST to `/prompt`. Agent posts workflow JSON, polls, downloads result.
- Gap closed: inpainting ("remove the fence"), img2img ("make background black"), ControlNet (preserve structure while restyling), upscaling — all via API, no GUI.
- Agent-drivability: EXCELLENT. `curl http://host:8188/prompt -d @workflow.json`. 50 lines of Python for full automation.
- Cost: 8GB VRAM minimum (SDXL with effort), 12-16GB comfortable. CPU mode exists but is painfully slow.
- Wire-up: run on Kaggle T4 (16GB) as persistent API server → agent calls it like a service.

**Pollinations.ai** (already tested working, zero signup)
- What: free text+image API. No GPU, no setup, just HTTP.
- Gap closed: quick generations, variations, concept art. NOT precise editing (can't do "fix the E").
- Agent-drivability: PERFECT. It's already a REST API.
- Priority: keep using for fast drafts; ComfyUI for precision work.

### P1 — Later

**stable-diffusion.cpp** — CPU inference for SD 1.5
- Runs on CPU with no GPU (~77 min/image at 512px — too slow for iteration, but works for overnight batches).
- Use case: only if Kaggle GPU is exhausted.

**Fooocus** — simplified SD GUI
- Easier than ComfyUI but less agent-drivable. Skip for agent workflows; ComfyUI API is better.

### Honest limit
SD inpainting needs a MASK (which pixels to replace) + prompt + seed tuning. Gemini needs only "fix the E." The mask-generation step is where agents lose time. Mitigation: use SAM (Segment Anything) for auto-masking from a text/click prompt → feed mask to SD inpainting. This pipeline (SAM → mask → SD inpaint) is the closest free equivalent to Gemini's "edit this part."

---

## CATEGORY 2: Photo (upscaling, restoration, cutouts)

### P0 — Wire now (most run on CPU fine)

**Real-ESRGAN** — https://github.com/xinntao/Real-ESRGAN (BSD-3)
- 4x upscaling, runs on CPU (slow) or any GPU. CLI: `realesrgan-ncnn-vulkan -i in.png -o out.png`.
- Already proven in the art-stack lane.

**rembg + BiRefNet** — background removal / cutouts
- `rembg i input.png output.png --model birefnet-general`. SOTA matting, CPU-capable.
- This IS the free "remove.bg" — already wired in art-stack.

**LaMa** — https://github.com/advimman/lama (Apache-2.0)
- Object removal via inpainting. Thin objects (fence wires, watermarks) erase cleanly.
- In art-stack as `inpaint.py` (OpenCV fallback working; LaMa hook pending).

**GFPGAN / CodeFormer** — face restoration
- GFPGAN (Apache-2.0): fast face fix. CodeFormer: better on badly damaged faces, fidelity slider.
- CLI available. CPU-runnable for single images.

### P1 — Later
**SwinIR / HAT** — higher-quality upscaling than Real-ESRGAN, slower. For hero images only.

---

## CATEGORY 3: Video

### P0 — Have already
- **ffmpeg** (have): cutting, captions, format conversion, thumbs.
- **RIFE** (MIT): frame interpolation 24→48/60fps. Runs on GPU; CPU possible for short clips.
- **EBSynth**: style transfer from keyframes. Already in the WG EP02 pipeline.

### P1 — Needs GPU (Kaggle)

**AnimateDiff** (Apache-2.0)
- Animates any SD 1.5 checkpoint. Integrates with ComfyUI as nodes → same API drivability.
- Needs 8GB+ VRAM. Short clips (2-4s), good for gags/bumpers/stingers.

**Stable Video Diffusion** (open weights)
- Image-to-video. 8GB+ VRAM. Foundation for many paid tools.

**Wan 2.1** — newer, better quality than SVD/AnimateDiff. Heavier VRAM.

### P2 — Watch
**Mochi 1**, **Allegro** — open video models, evolving fast. Revisit quarterly.

### Honest limit
Free local video gen does SHORT clips (2-10s) at modest quality. Nothing free matches Gemini/Veo/Sora for long coherent video. Strategy: use free tools for bumpers, stingers, gags (short = their sweet spot), not episodes.

---

## CATEGORY 4: 3D/CGI

### P0 — Have
- **Blender 4.0.2** (have): modeling, rigging, rendering, Python API. The backbone.

### P1 — Wire on Kaggle GPU

**TripoSR** (MIT) — https://github.com/VAST-AI-Research/TripoSR
- Single image → textured 3D mesh in ~0.5s on A100, works on low VRAM.
- CLI available. `halldm2000/image-to-3d` wraps it + TRELLIS + Hunyuan3D with a unified CLI.
- Best for: rapid character/prop drafts from concept art.

**TRELLIS** (Microsoft, MIT) — https://github.com/microsoft/TRELLIS
- Best QUALITY open image-to-3D. Outputs mesh + PBR materials as GLB.
- Needs ~16GB VRAM (fits Kaggle T4). Python API: `TrellisImageTo3DPipeline.from_pretrained("microsoft/TRELLIS-image-large")`.
- Original TRELLIS also does text-to-3D (TRELLIS.2 is image-only).

**Hunyuan3D 2.1** — open WEIGHTS but restrictive license (1M MAU gate, excludes EU/UK/Korea, no training on outputs). Quality is high but license is a trap for commercial work. Prefer TRELLIS (MIT).

### Honest limit
Image-to-3D gives unrigged static meshes. Rigging still needs Blender work (or Mixamo). No free tool does "photo → rigged game character" in one shot. Pipeline: TripoSR/TRELLIS (mesh) → Blender (cleanup + rig) → game.

---

## CATEGORY 5: Music + film scoring (biggest gap)

### P0 — Wire now

**MusicGen** (Meta, via facebookresearch/audiocraft) — MIT-ish open, COMMERCIAL USE OK
- Text-to-music AND melody-guided. `musicgen.py --prompt "dark trap beat 140bpm" --duration 30`.
- Runs on CPU (slow) or GPU. Best open model for instrumental generation.
- Gap closed: background music, loops, genre sketches for scenes.

**Riffusion** (MIT)
- Spectrogram diffusion, FAST. 5s native window, script stitches longer via crossfade.
- Best for: quick beat/loop ideas.

**Stable Audio Open** (Stability Community License — NON-COMMERCIAL ONLY)
- 44.1kHz stereo, up to 47s, can continue existing audio ("add energy, build into chorus").
- ⚠️ License trap: non-commercial only. Fine for internal/show use, NOT for selling packs.
- Needs ~16GB VRAM for good quality.

**YuE** (Apache-2.0, m-a-p/YuE-s1-7B-anneal-en-cot)
- Full SONGS WITH VOCALS. Chain-of-thought prompting (Verse/Chorus/Bridge).
- 7B model, needs GPU. This is the open answer to Suno/Udio.

### P1 — Production tools

**Demucs** (Meta, open) — stem separation. Split any track into vocals/drums/bass/other. Free, local.
**Ardour** (free DAW) / **LMMS** (free DAW) — arrangement, mixing, MIDI.
**AIVA** (free tier) — AI composition focused on classical/orchestral/film scoring. Web-based, free tier limited.

### The realistic free film-scoring pipeline
1. **Spotting:** owner describes mood per scene (or temp track reference).
2. **Generate:** MusicGen (instrumental cues) or YuE (vocal songs) → 3-5 variants per cue.
3. **Arrange:** Ardour/LMMS — cut to picture, layer, add transitions.
4. **Stems:** Demucs to isolate/replace elements.
5. **Mix:** Ardour + free plugins.

### Honest limit
AI music does NOT do leitmotif development, precise hit-point syncing, or emotional arc across a 20-min episode. It generates CUES (30-60s mood pieces). A human (or agent with a DAW) still assembles the score. For the owner's shows: generate per-scene cues with MusicGen → cut to picture in Ardour. That's the real pipeline.

Suno/Udio (paid) are better at full songs, but YuE is the free answer and it's Apache 2.0.

---

## WIRE-UP PRIORITY SUMMARY

| Priority | Tool | Category | Why now |
|----------|------|----------|---------|
| **P0** | ComfyUI headless API on Kaggle T4 | Image edit/gen | Closest to Gemini editing; agent calls it as a service |
| **P0** | SAM → mask → SD inpaint pipeline | Image edit | Auto-masking kills the biggest friction vs Gemini |
| **P0** | MusicGen | Music | Commercial-safe AI music, CLI-driven |
| **P0** | YuE | Music/vocals | Free Suno alternative, Apache 2.0 |
| **P0** | Demucs | Audio | Free stem separation |
| **P1** | TripoSR / TRELLIS on Kaggle | 3D | Image-to-3D drafts; TRELLIS for quality |
| **P1** | AnimateDiff via ComfyUI | Video | Short gags/bumpers/stingers |
| **P1** | Ardour or LMMS | DAW | Assemble AI cues into real scores |
| **P1** | RIFE | Video | Frame interpolation for existing footage |
| **P2** | Wan 2.1, Mochi 1 | Video | Watch — quality improving fast |
| **P2** | SwinIR/HAT | Photo | Marginal gain over Real-ESRGAN |

## Already have (don't re-buy/re-build)
rembg, BiRefNet, LaMa/OpenCV inpaint, Real-ESRGAN, potrace/vtracer, Pillow, ImageMagick, ffmpeg, Blender, EBSynth, Pollinations.ai, faster-whisper, espeak-ng.

## What free tools CAN'T match (be honest with owner)
1. **One-shot contextual editing** ("fix the E" with no mask, no seed tuning). Mitigation: SAM auto-masking narrows this.
2. **Long coherent video** (30s+ with consistent characters). Free tools do shorts well; episodes need the EP01 method (image-animation per still).
3. **Full film scores with dramatic arc.** AI makes cues; assembly is still human/agent work in a DAW.
4. **Photo → rigged game character** in one step. Mesh gen + Blender rigging is a two-stage pipeline.

## The infrastructure answer
Everything heavy runs on the owner's existing free GPU (Kaggle 30hrs/wk T4×2 primary, Colab/Lightning backup) as API servers. The agent never runs diffusion locally — it POSTs to the GPU box and gets results back. This is the architecture that makes "free" actually work at production scale.
