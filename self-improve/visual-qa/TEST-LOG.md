# SELF-IMPROVE ROUND 2 — TEST LOG (S8)
Written 2026-11-16 by the successor lane (predecessor died 15:15:04Z before
testing anything — every tool below was built untested; this log is the first
time any of them ran on a real case). All runs live in
`~/workspace/_self-improve2-20261116/tests/`.

Rule of this log: a tool is DONE only when a real case and a control both
behave as expected. A PASS on a good case alone proves nothing; the control
must FAIL.

## Real cases used (all on disk, verified present 2026-11-16)
- Adri #138 perf plates: `~/workspace/your_files/adri-perf-beat{1,2,3}-*-2026-11-09.png`
  (side-by-side source-photo + render plates with a caption bar).
- Angel-Megami v22 multi-angle set: `~/workspace/your_files/angel-megami-v22-{front,q34,profile,bun-front}-20261110.png`.
- Afro v2 frames-after: `~/workspace/_afro-refit-20261110/proof/megami-afro-v2/frames-after/f{000,040,080,120}.png`.
- Life Cut v2.2 film: `~/workspace/your_files/adri-biology-life-cut-v2.2-nogarments.mp4`
  (3,132f / 104.4s / 600x600, sha256 1ab243fb... — the film of record).
- Waddle v3 side-by-side: `~/workspace/your_files/adri-waddle-sidebyside-v3-20261109.mp4`
  (1440x1580, 188f, 6.27s) + extracted frame `tests/waddle-f90.png` and
  the cropped Adri panel `tests/waddle-adri-panel.png`.
- Reference library: `~/workspace/agent-ops/self-improve/reference/` —
  all 8 manifest sha256s MATCH the files on disk; sintel-360p.webm decodes
  (VP9 640x272, 888.06s, 52,936,857 B).

## Synthetic controls (LABELLED — they test the measurement, not the pipeline)
- `washout-control-synthetic.png` — Adri beat1 blended 70% toward white +
  desaturated (mimics the Megami live-proof washout).
- `black-control-synthetic.png` — Adri beat1 at 5% brightness.
- `tpose-control-synthetic.png` / `armsdown-control-synthetic.png` — v2
  silhouettes with REALISTIC proportions (head 13% of height, arms at
  16–20%). v1 had the head at 8.5% and arms at 9.6% — ABOVE the 15–25%
  shoulder band, so the band measured torso and the T-pose PASSED.
  A bad control, not a tool bug; fixed by re-proportioning, not by
  touching the tool.
- `flatcard-control-synthetic.png` — solid rectangle "figure" on white.
- `flat-control-synthetic.png` — solid colour image (no subject at all).

## color_light_check.py (S2)
- Washout control: FAIL washout 84.2 (≥60) ✓. Black control: FAIL clip lo 27.4% ✓.
- Sintel-face/jpg frames: first run FAIL junk 6.3% — the REFERENCE failed
  its own check. Root cause: the "unnatural magenta" band was h>280, which
  catches CRIMSON (280–360) — legitimate red hair and lips. Sintel's red
  hair scored 6.3% junk. FIX: magenta band narrowed to 290–330; crimson/red
  (330–360, 0–20) excluded; green band 80–160 kept (green blotches on skin
  are vertex-colour junk). Re-test: sintel-face junk 6.3 → 0.0, all three
  Sintel frames PASS.
- Adri #138 plates, WHOLE plate: FAIL clip hi 15–19.5% — the source-photo
  half's bright wall + the render's blown neck. The plate is NOT one
  subject (source + render + caption bar). FIX: added `--crop X0 Y0 X1 Y1`
  (fractional region) + a scope note in the docstring.
- Adri #138 plates, RENDER HALF ONLY (--crop 0.5 0 1 0.9): FAIL clip hi
  31.7–39.4%. Diagnostic confirmed the mask is sane (corner median dark
  16–20, subject 64.6% of the crop) and 32.9% of subject pixels are ≥254 —
  the blown neck/chest/shoulders are REAL (verified by eye on the plate),
  not a mask artifact. THIS IS A REAL CATCH: the #138 renders ship with
  ~1/3 of the subject clipped — round-1 "loaded OK" never surfaced it.
  Whether it is a defect or a lighting choice is the owner's call; the
  tool flags, it does not condemn. beat2 also trips colour cast 29.2
  (threshold 28, borderline — recorded, not re-tuned).
- Angel v22 front: PASS (washout 7.1, clip 0/0, cast 6, junk 0.5).

## pose_check.py (S3)
- Synthetic T v2: FAIL "T-POSE: shoulders 4.72x hip width" ✓.
  Synthetic arms-down v2: PASS shoulder 1.0 ✓. (v1 T PASSED — bad control,
  see above; the tool was right, the control was wrong.)
- sombra_tpose.png (S1's "real T-pose control"): UNRELIABLE, subject 0.7%
  of frame. Viewed by eye: alpha is 255 EVERYWHERE (opaque white bg, no
  alpha subject) and the figure is a tiny speck under a huge grey blob —
  a broken/thumbnail render, NOT a T-pose control. The tool was right to
  refuse; the S1 note was wrong. No real T-pose render exists on disk —
  honest gap (see below).
- Afro v2 frames f000/f040/f080/f120: UNRELIABLE "not full-body framing
  (bbox top 41–50%, height 50–59%)" — the afro proof frames are
  head/shoulder framings. Correct refusal.
- Angel v22 front: UNRELIABLE (headshot, bbox top 30%) — correct refusal.
- Waddle Adri panel: UNRELIABLE (bbox top 39%, height 48%) — the figure
  does not fill the frame. Correct refusal.
- GAP: no full-body, frame-filling void render exists on disk to give
  pose_check a real PASS case. The first real full-body proof render is
  its first real test. OpenPose keypoints would help here — weights are
  NOT fetchable from this box (CMU empty reply, ZheC mirror 0 bytes,
  HuggingFace 404; prototxt IS fetched, 46,372 B).

## face_check.py (S3)
- v22 front + q34: face found, PASS. v22 profile: UNRELIABLE "no
  frontal/3-4 face found — eyes must judge" ✓ (correct — profile).
- Likeness front vs bun-front (same person, different hair): SSIM 0.731,
  worst geometry delta 0.017 → PASS ✓. Self-ref sanity: SSIM 1.0, delta 0.0 ✓.
- Sintel-face: face found, PASS ✓.

## video_probe.py (S4)
- Life Cut v2.2, --every 60 (53 samples): motion range 0.49–121.36 (real
  motion present); frozen runs [1,2,1,1,1,1,2,2,1,1]; contact sheet
  written (viewed by eye — the whole film at a glance: meal, workout,
  vomit, road trip, Kimiko block, lab telemetry).
- First run: FAIL on 27/53 samples "failed colour check" — the per-sample
  colour check is calibrated for VOID renders; on busy film frames it fires
  on bright set elements (white table, bright walls) while the film itself
  is normally exposed (verified by eye on the contact sheet). FIX: added
  `--film` mode — per-sample colour verdicts are reported per row but do
  NOT fail the video; only BLACK/BLOWN frames and frozen stretches fail.
  Re-run --film: FAIL only on the frozen runs (correct — the 348 frozen
  frames are intentional per the film report; the tool says "judge whether
  the hold is intentional").
- Lab block (frames 2832–3131, "frozen, byte-identical" as PNGs) decodes
  with inter-sample motion 1.38–6.25, not ~0 — the mp4 encode introduces
  small per-frame differences. The frozen threshold (1.5) catches part of
  the block; the rest reads as near-frozen. Recorded, not re-tuned: the
  threshold measures the DECODED video, which is what the owner watches.

## turntable_proof.py (S5)
- Images mode, v22 front/q34/profile: PASS, all angles present, contact
  sheet written ✓.
- Images mode, front only: FAIL "missing angles: q34, profile, back" ✓.
- Video mode, waddle v3 sbs (not a turntable): FAIL "turntable does not
  turn: aspect spread 0.0 over 12 samples" ✓.

## depth_check.py (S6 — NEW, not in the predecessor's build)
- Model: Depth Anything V2 small ONNX, FETCH-VERIFIED from HuggingFace
  `onnx-community/depth-anything-v2-small` (onnx/model.onnx, 99,060,839 B,
  sha256 recorded in the kit README). onnxruntime 1.30.0 was already on
  the box — no install. (MiDaS was tried first: Intel-ISL v2_1 and isl-org
  v3_1 release URLs both return a 9-byte "Not Found"; v3_1 ships OpenVINO
  IR only and openvino is NOT installed. Depth Anything is the working path.)
- v22 front: PASS subj_std 0.2219, separation 0.573 ✓. Waddle panel: PASS
  0.1786 / 0.216 ✓. Depth-map PNG viewed by eye: real depth — head, neck,
  shoulders, chest with proper falloff, background far.
- Flat-card control: first threshold 0.02 PASSED it (std 0.07) — the depth
  model hallucinates structure on a flat rectangle. Real renders measure
  0.18–0.22, the card 0.07. FIX: threshold raised to 0.10 (between the two).
  Re-test: flat card FAIL 0.070 < 0.1 ✓, real renders still PASS ✓.
  Threshold calibrated on 3 cases only — re-check on more renders.
- Flat solid-colour image: UNRELIABLE (no subject/background split) ✓.

## pre_delivery_checklist.py (S7)
- Still, NO --seen: DELIVERY-READY NO ("NO OWN-EYES ATTESTATION") ✓.
- Still, WITH --seen: DELIVERY-READY YES ✓ (v22 front, sha256 recorded).
- Video v2.2, WITH --seen + --allow-frozen: DELIVERY-READY YES ✓ —
  video_decode PASS (ffprobe 3,132 frames), video_probe WARN (intentional
  frozen: reststop 1236–1259 + lab 2832–3131 per film report), sha256
  1ab243fb... == the recorded film hash EXACT.
- BUG FOUND IN TESTING: the video branch called frame_set_gate.py with the
  mp4 as the frames dir and no --expect — argparse errored, so EVERY video
  failed the gate. FIX: --frames-dir + --expect run the full gate; without
  them the checklist runs the ffmpeg full-decode + ffprobe count directly
  and records that contiguity was not re-checked. Also added --crop
  passthrough for still plates and --allow-frozen (frozen-runs-only FAIL
  → WARN with the attested reason; black/blown can never be attested away).

## reference_compare.py (S10)
- v22 front vs sintel-face, first version: BELOW on washout (7.07 vs 0.0),
  contrast, saturation (102 vs 193) — the band compared EXACT values with
  a tight tolerance, so a washout of 7 counted as BELOW a reference of 0
  (both far inside the good range) and a face render's saturation "failed"
  against a fire-lit film still (different content, not a quality gap).
  FIX: range-aware bands — BELOW only when ours is in the BAD range
  (washout >40, contrast <20, saturation outside 20–220, clip >5,
  cast >28); MEETS when ours is in the good range; ABOVE when ours beats
  the reference's own value. Shoulder ratio: out-of-band is always BELOW
  (a T-pose has a HIGHER ratio — never ABOVE). Re-test: v22 front MEETS
  on all five in-range metrics; washout control BELOW on washout (84.2),
  contrast (7.5) and saturation (3.4) ✓. Side-by-side sheet written.

## What round-2 catches that round-1 missed (the point of this lane)
1. The #138 Adri renders clip ~1/3 of the subject (hot neck/chest lighting)
   — colour check, verified by eye, not a mask artifact.
2. The Sintel reference failed the first junk check — the hue band caught
   legitimate red hair; calibration fixed before it could false-fail a
   real render.
3. The checklist failed EVERY video (frame_set_gate misuse) — fixed.
4. video_probe failed a normally-exposed film on 27/53 samples (void-render
   calibration on busy frames) — --film mode added.
5. reference_compare failed a good render for differing from the reference's
   exact numbers — range-aware bands.
6. A flat card passes a naive depth check — threshold calibrated on the
   real-vs-card gap.

## Honest gaps (still can't be seen / done)
- MediaPipe pose + CLIP: torch NOT installed, MediaPipe broken (numpy 2).
  No install was made (zero-install rule); pip-installing torch is a
  ~800MB+ decision for the parent, not this lane.
- OpenPose keypoints: weights not fetchable (3 attempts, see pose section).
  Silhouette mode is the primary pose tool; keypoints stay a hook.
- No real T-pose render and no full-body frame-filling void render on
  disk — pose_check has no real PASS case yet.
- CLIP/semantic similarity: needs torch — same gap as above.
- Depth threshold (0.10) calibrated on 3 cases only.
- Reference library gaps (in manifest.json): digital humans (MetaHuman
  Behance — BROWSER-GATED, in BROWSER-QUEUE.md), fluid work (Tears of
  Steel named next pull), best facial-expression rig test (same
  BROWSER-GATED item).

## WIRE-IT-EVERYWHERE run (2026-11-16)

- Kit landed in canonical home (PP PR #199, merge 99fa94c6): 32/32 files
  hash-verified on main + AGENTS.md blob match. Smoke-tested FROM the repo
  home: pair_compare --help OK, color_light_check on landed sintel-face.jpg
  PASS (washout 0.0), reference_compare --help OK (landed manifest resolves).
- Catch 1: PP root .gitignore (*.jpg, *.webm) silently dropped the 8
  reference media files from the first commit (25 files, not 33). Found by
  counting PR files vs the kit file list before merging. Fix: force-add with
  the exception documented in the commit message (2nd commit 8ae74bd).
- Catch 2: western-heart instruction-gate failed the first PR body (plain
  paragraph). Fix: 6-section body per the gate script; gate passed on
  re-run; PR #1748 merged ee3c0806.
- Kit improvements from this run: `lane-ops/pr_body_template.md` (new),
  README "Wiring notes" section (new), this log entry.
- Other repos wired (rules + pointer only, each PR + readback verified):
  western-heart #1748, dream-girl #90 (AGENTS.md created — none existed),
  Bannon #94, Physics-sandbox-playground- #15, cape-jones #410,
  ConcreteDragon2 #10.

