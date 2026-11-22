# GROK-BOT CAPABILITY STUDY — Full Map + Replication Plan

Date: 2026-10-08. Owner directive: "We need to do everything better and just as good as grok bot from the studies, not just entrance kits and capture pipelines, but that stuff too."

## What "Grok bot" actually is

Two separate things the owner calls "Grok bot":
1. **Grok Build** (xAI's coding agent CLI) — autonomous coding agent: reads files, writes code, runs shell, spawns subagents, manages git. Headless mode, ACP support. This is the "Repo Co Dev" / builder side.
2. **App Builder** (Grok chat sandbox) — builds web apps from chat with live preview at :8080. Has the **imagine_*** tools (native AI image/video generation) and a **skills system** (building-games, design-ui, game-animation-frames, etc.). This is the "Producerbot" side that does videos and game builds.

## Capability map

### 1. Autonomous coding (Grok Build CLI)
- **What**: Long-running coding tasks, git workflows, subagents, plan approval.
- **Output quality**: High — built Brutal Fist's full engine (10 versions), Bannon's recorder hardening, PWA systems.
- **Us**: ✅ MATCH. We do the same thing (subagents, checkpoints, git).

### 2. Live preview + browser QA loop
- **What**: Every build served at :8080, verified with Playwright screenshots before claiming done. `browser-smoke.mjs` audits desktop+mobile.
- **Output quality**: High — catches blank pages, console errors, layout issues.
- **Us**: ⚠️ PARTIAL. We build and test, but the owner can't see a live preview. Our QA is less systematic.
- **Close with**: Standardize a preview + screenshot QA checklist for every web deliverable. Free.

### 3. imagine_text_to_image / imagine_image_to_image (NATIVE AI IMAGES)
- **What**: Generate/edit images directly in the sandbox. Used for sprites, concept art, maps, marketing.
- **Output quality**: High — production game art.
- **Us**: ❌ DON'T HAVE.
- **Close with**: **Pollinations API** (free, no key, verified in our API sweep). Wire as `imagine` replacement. Priority #1.

### 4. imagine_text_to_video / imagine_image_to_video (NATIVE AI VIDEO)
- **What**: Generate/animate video from text or stills. Used for promo videos, animation.
- **Output quality**: High.
- **Us**: ❌ DON'T HAVE. Biggest gap.
- **Close with**: No free equivalent matches it. Best path: (a) Blender procedural animation + real gameplay capture (we have this), (b) Pollinations video if available, (c) AnimateDiff local if GPU allows. Priority #2.

### 5. Video-first animation pipeline (video2dsprite)
- **What**: Base still → AI video (in-place motion) → ffmpeg frames → chroma key → dense sprite sheets.
- **Output quality**: High — smooth walk/run cycles from a single image.
- **Us**: ❌ DON'T HAVE (depends on #4).
- **Close with**: Alternative path — render our 3D rigged models from multiple angles → sprite sheets. We HAVE the models and Blender. This actually beats Grok's 2D path for 3D games. Priority #3.

### 6. Game-building doctrine (skills)
- **What**: Deep playbooks: game loop, 3D orientation, controls (inverted A/D!), per-genre guides, animation frames, character consistency, tilesets, UI icons.
- **Output quality**: High — this is why Grok's games play correctly (it doesn't ship inverted controls).
- **Us**: ⚠️ PARTIAL. We build games but less systematically. The `controls` skill (A/D inversion) is a real lesson.
- **Close with**: Port the key doctrines into our own skill files. Free. Priority #4.

### 7. Character consistency system
- **What**: Turnarounds, state variants, palette swaps, asymmetry bookkeeping across views.
- **Output quality**: High — same character in every image.
- **Us**: ❌ DON'T HAVE systematically.
- **Close with**: For 3D: render turnarounds from our rigged GLBs (we can do this NOW). For 2D: needs #3. Priority #5.

### 8. Playwright recorder + certification gates
- **What**: Real gameplay recording with 11 certification gates (model exists, match reached FIGHT, zero errors, animation reached skeleton, no deformation spikes).
- **Output quality**: High — "proof in the pudding."
- **Us**: ✅ MATCH. We have tools/harness/play_and_record.cjs and the same gates.

### 9. PWA tooling
- **What**: Install checks, offline cache versioning, portrait auditing.
- **Output quality**: High.
- **Us**: ✅ MATCH.

### 10. Entrance video production (Producerbot)
- **What**: 50-second beat-synced entrance videos from repaired models + real music.
- **Output quality**: High (El Toro de Oro is the bar).
- **Us**: ⚠️ BUILDING. Separate worker on the entrance-video pipeline. Our advantage: we have the real models, real music, real beat grids.

## What Grok built for the owner (verified from git/docs)

- **Brutal Fist v1-v10+**: Full TypeScript fighting engine (locomotion, combat, grapple, pin, stages, AI, PWA)
- **Bannon recorder hardening**: 11 certification gates, deformation telemetry
- **Mocap ingestion**: 340-move catalog from .zf3d + Unity clips
- **Model repair workflows**: weight transfer, rigging, UniRig pipeline
- **PWA systems**: install checks, offline cache, portrait audit
- **Intro movies**: docs + player (PR #32, #33)
- **Marketing kits**: in progress
- **Character videos**: pipeline hardened, batch not yet delivered

## Replication priority (owner-value order)

1. **Pollinations image pipeline** (replaces imagine_text_to_image) — unlocks sprites, concept art, marketing. FREE.
2. **3D-to-sprite pipeline** (replaces video2dsprite for 3D games) — render rigged GLBs → sprite sheets. We have everything needed.
3. **Game doctrine port** (controls, building-games, character-consistency) — prevents the bugs Grok doesn't ship.
4. **Video generation research** — hardest gap, explore Pollinations video + local options.
5. **Live preview QA checklist** — standardize screenshot verification.

## Honest assessment

Where Grok beats us: native AI image/video generation (no free equivalent matches it 1:1), systematic game doctrine, live preview loop.
Where we match: autonomous coding, recorder/certification, PWA, model repair.
Where we can beat Grok: real 3D models (we have 130+ rigged characters, Grok generates 2D), real music licensing (owner's connections), canon accuracy (we have the books), cost ($0 vs Grok subscription + usage limits).
