# Game Dev Studio Pipeline Landscape — researched 2026-10-13

Owed to the Wizard Gang side chat (owner asked: "what's out there that'll help with
my game development and the production pipeline... the studio for my game developing").

His pipeline today: Blender rigs → Mixamo clips → Three.js PWA games / UE5 →
2D cutout shows (Goodville South-Park-style paper cutout) → video pipeline → pages.

All items below are free/open-source or free-tier, found via public sources on
2026-10-13. LICENSE MUST BE VERIFIED before wiring into any repo or commercial
build. Nothing below is a leak, mirror, or grey-area source — the leak-hunting
line is respected; this is the legit half of the question.

## Animation & motion — his #1 bottleneck (the no-fake-animation law)

1. **Cascadeur** (cascadeur.com) — AI + physics-assisted keyframe animation
   (AutoPosing/AutoPhysics). Free tier covers revenue under $100k. Built for
   exactly his problem: believable grapples/throws/impacts without a mocap
   suit. Pair with Mixamo retarget for his fighters.
2. **DeepMotion** (deepmotion.com) — phone/webcam video → full-body mocap
   FBX/BVH including face & hands. Free tier = short previews. Indie recipe:
   phone on tripod → DeepMotion → Cascadeur polish → retarget onto his rigs.
3. **Rokoko Vision** (rokoko.com/products/vision) — free AI markerless mocap
   from video + smartphone facial capture app. One-supplier pipeline.
4. **AnimationGPT** (github.com/nixiCodex) — open-source text-to-BVH motion,
   trained on game combat/action. Free. Direct fit for generating combat moves
   (strikes, grapples) as a starting point for hand-polish.
5. **AccuRIG** — free automatic rigging for creatures AND characters. Second
   opinion next to Mixamo auto-rig, useful for his non-humanoid mechs.
6. **many_mocap** (github.com/ehsanwwe/many_mocap) — open-source two-camera
   markerless mocap → animation-ready BVH. DIY, free, Blender-compatible.

## 2D cutout shows — Goodville's method (biggest find)

7. **papermotion / ai-animation-studio** (github.com/bogeling/ai-animation-studio)
   — open-source PAPER CUT-OUT animation engine with parallel/GPU renderer and
   agent skills for making films as code. This is the Goodville method in
   software form: cut pieces + timeline + render, ~2 min for a 50s 1080p film
   on laptop GPU. HIGHEST pull-in priority for the shows.
8. **OPEN-TOON** (github.com/mijim/OPEN-TOON) — brand-new open-source 2D
   animation app (drawing + rigging + compositing), GPL-3.0, created Sept 2026.
   Early (49 commits) — watch, don't build production on it yet.
9. **Storyboarder** (Wonder Unit) — free, open-source storyboarding with
   Photoshop integration. For show pre-production (animatics, beat boards).

## Video / production automation

10. **OpenMontage** (github.com/victorjackson2201/openmontage) — open-source
    agentic video production system: Piper TTS narration, Remotion/HyperFrames
    rendering, FFmpeg post, auto-captions with word timing. Fits his network
    ID cards, bumpers, and commercial production.

## Suggested pull-in order (when disk is healthy)

1. papermotion → evaluate against the Goodville cutout pipeline
2. Cascadeur → test on one grapple sequence (GRAB→LIFT→LOCKUP→THROW)
3. DeepMotion free tier → one phone-captured walk cycle
4. OpenMontage → one network bumper end-to-end
5. AnimationGPT, AccuRIG, many_mocap → combat-move experiments
6. OPEN-TOON → watch only

## Constraints noted at research time

- Disk was at 86% on 2026-10-13 ~18:30 ET (guardian cron cleaning). Do NOT
  clone/eval anything until disk is back under 75%.
- Existing coverage this ADDS to (not duplicates): bannon-video-pipe
  docs/AI_RIGGING_RESEARCH.md (rigging tooling), the 3,000+ free-tool catalog,
  the free compute arsenal. The new layer here is MOTION SOURCES and the
  CUTOUT-SHOW ENGINE — those were the gaps.
