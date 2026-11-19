# SELF-IMPROVE KIT — how the agent team works better

Built 2026-11-16 (owner order ~09:21 EST: "stop bullshitting me... running me
in circles"). The proof is the work getting better, not the claim.

## The audit (why we were circling — named from our own recent records)

1. **Search-only research.** Realism lanes (b), (c+d) hit 429s on 11+ sources and
   recorded "re-fetch later" with no mechanism; lane (10) ranked tools on
   SEARCH-verified evidence only. A ranked list mixed verified and unverified
   items (HY-Motion ranked #6 with "licence unread — blocker").
   Fix: `research-verify/verify_sources.py` + the EVIDENCE-LABEL rule.
2. **Addenda arriving after lanes completed.** Sends to lanes (10), (c+d), (f)
   FAILED — they had already finished; follow-up lane (10b) had to be spawned.
   Fix: coordinator holds addenda in a mailbox file; synthesis folds them in.
   Never send follow-ups to a completed lane.
3. **Browser-gated checks with no owner-side path.** Mixamo stayed UNVERIFIED
   ("needs a BROWSER lane") with nowhere to go. Fix: `BROWSER-QUEUE.md` —
   the exact URL + what to confirm, for the parent to run in the live browser.
4. **Relaunches re-briefed from the top.** The law said resume-never-restart,
   but there was no METHOD for writing a resume brief. Fix:
   `lane-ops/resume_brief.md` — quote the checkpoint's exact next step,
   count the disk state yourself, list what is DONE and forbidden to redo.
5. **"Loaded OK" checks passing visible defects.** The identity audit (2026-11-10)
   proved it: Melanie/Kasumi shipped broken while numeric checks passed.
   Fix: `visual-qa/` — the machine gathers numbers + heatmaps; the agent's
   eyes judge the same frames. A visual claim without a pair-compare is a claim.
6. **Dirty/stale local clone.** The realism coordinator found the PP clone stale
   + dirty with v71 leftovers. Fix: `lane-ops/repo_preflight.sh` before any
   branch is cut.
7. **Duplicate-runner race on relaunch.** Life Cut v2.2 capture: a second
   runner appeared on EACH VM-restart relaunch and had to be killed by hand.
   Fix: `lane-ops/run_guarded.sh` (flock) — a relaunch can never start a
   second copy.

## The kit

| Piece | What it does | How to use |
|---|---|---|
| `visual-qa/pair_compare.py` | SSIM + pixel-diff + heatmap for a before/after pair; `--expect same\|different` mechanical verdict | `python3 pair_compare.py before.png after.png --expect different --out dir/` |
| `visual-qa/frame_set_gate.py` | Frame-set gate: contiguity, zero-byte/truncation + PIL decode, frozen sha-identity vs manifest, optional mp4 full-decode + frame count | `python3 frame_set_gate.py frames/ --expect 3132 --manifest frames-sha256.txt --video film.mp4 --out dir/` |
| `research-verify/verify_sources.py` | Deterministic pull check per source: `git ls-remote` for repos, capped GET with 429 retry for http; licence verdict required; RETRY-LATER queue | `python3 verify_sources.py sources.json --out dir/` then `--retry-queue dir/verify-queue.jsonl` |
| `lane-ops/run_guarded.sh` | flock wrapper — a long-lived command can never be started twice | `run_guarded.sh runner.lock -- ./run-capture.sh` |
| `lane-ops/repo_preflight.sh` | Clean-tree + fresh-fetch gate before cutting a branch | `repo_preflight.sh /path/to/repo main` |
| `lane-ops/resume_brief.md` | Template for relaunching a dead lane from its checkpoint | Fill in, quote the exact next step |

## Round 2 — SEE BETTER (2026-11-16, owner order ~09:43 EST: "see better think
better and work better... you don't always look at things... being lazy")
The predecessor lane built these untested and died; the successor tested every
one on real cases (see `visual-qa/TEST-LOG.md` — the first test run caught
five calibration defects and one checklist bug, all fixed in the log).

| Piece | What it does | How to use |
|---|---|---|
| `visual-qa/color_light_check.py` | Washout / clipping / colour-cast / unnatural-hue check on a single render (alpha-aware subject stats; `--crop` for one panel of a plate) | `python3 color_light_check.py render.png` |
| `visual-qa/pose_check.py` | Silhouette T-pose + detached-parts + framing gate (full-body only; headshots refuse honestly). OpenPose hook: weights not fetchable from this box, prototxt present | `python3 pose_check.py render.png --out dir/` |
| `visual-qa/face_check.py` | Haar face + eye detection, eye-line geometry, likeness vs a reference portrait (aligned SSIM + ratio deltas) | `python3 face_check.py render.png --ref portrait.png` |
| `visual-qa/video_probe.py` | Samples a video, runs colour checks per sample, measures motion, flags frozen stretches + black/blown frames, writes a contact sheet. `--film` for busy film frames (colour reported, not failed) | `python3 video_probe.py film.mp4 --every 60 --film --out dir/` |
| `visual-qa/turntable_proof.py` | Multi-angle proof: images mode checks coverage vs expected angles + contact sheet; video mode proves a turntable actually turns (aspect spread) | `python3 turntable_proof.py --images front.png q34.png profile.png back.png` |
| `visual-qa/depth_check.py` | Depth Anything V2 small (ONNX) depth map: subject depth variation + subject/background separation — catches flat cards and pasted cutouts | `python3 depth_check.py render.png --out dir/` |
| `visual-qa/reference_compare.py` | Our render vs a top reference, side by side: side-by-side sheet + BELOW / MEETS / ABOVE bands (reference = floor, not ceiling) | `python3 reference_compare.py --ours ours.png --ref-id sintel-face --out dir/` |
| `visual-qa/pre_delivery_checklist.py` | FORCES the own-eyes check: hashes the deliverable, runs the kit, REQUIRES `--seen "..."` attestation; DELIVERY-READY YES only with checks passing + eyes attested. `--allow-frozen` for intentional film holds | `python3 pre_delivery_checklist.py --deliverable film.mp4 --claim "..." --seen "viewed ..."` |
| `reference/` | The reference library — top of each field, manifest.json (title, source, licence, why-top, sha256). Gaps named in the manifest | Additions: FETCH-VERIFIED only, or BROWSER-GATED on `BROWSER-QUEUE.md` |
| `BROWSER-QUEUE.md` | Live-browser checks the kit cannot do (login/JS/download buttons) | Exact URL + what to confirm; parent runs it |

## Evidence labels (use these exact words in every research report)

- **FETCH-VERIFIED** — bytes were fetched in this run (or `git ls-remote`
  answered). File size + sha256 recorded in the verify log.
- **SEARCH-VERIFIED** — page text was seen via search/fetch of a page, but no
  artifact bytes were pulled. Never ranked as pullable; never presented as
  "we have it".
- **UNVERIFIED** — fetch failed. The exact error is recorded. Goes on the
  verify-later queue, never into the ranked list.
- **BROWSER-GATED** — needs a live-browser check (login, JS, download button).
  Goes on `BROWSER-QUEUE.md` for the parent. Never left as "unverified" forever.
- A source enters a ranked list only as FETCH-VERIFIED with a licence verdict
  present. No verdict → NOT-RANKABLE.

## Rules these tools enforce (also in ~/AGENTS.md)

- EVIDENCE-LABEL LAW, VERIFY-LATER-QUEUE LAW, BROWSER-QUEUE LAW,
  RESUME-BRIEF METHOD, VISUAL-QA-BEFORE-CLAIM LAW, NO-LISTS-WITHOUT-PULLS LAW.
  Read them in ~/AGENTS.md — the scripts are the enforcement, the rules are
  the requirement.

## Dependencies

Python 3 + PIL + numpy + scikit-image (all already on this box, 2026-11-16).
`ffmpeg`/`ffprobe` for the video check in frame_set_gate (already present).
`git` + `curl`-equivalent (urllib, stdlib) for verify_sources. No installs.
Round 2 adds: `onnxruntime` 1.30.0 (already on the box — depth_check only) +
model files in `visual-qa/models/` (all data files, fetched, never installed):
Haar cascades (opencv GitHub), OpenPose prototxt (46,372 B; the caffemodel
weights are NOT fetchable from this box — CMU empty reply, mirrors dead),
Depth Anything V2 small ONNX (99,060,839 B, HuggingFace onnx-community).
MediaPipe is BROKEN (numpy 2 incompatibility) and torch is NOT installed —
no MediaPipe pose, no CLIP. Those need an install decision by the parent,
not by a lane.

## Wiring notes (added 2026-11-16, WIRE-IT-EVERYWHERE run)

- Canonical home: `mhvnsnt/physics-playground-pwa`,
  `docs/build-a-bitch/tools/self-improve/`. This workspace copy is a working
  mirror. Improvements land in the canonical home first (PR + full readback),
  then the mirror is re-synced. Other active repos carry the methods rules in
  their AGENTS.md plus a pointer at the canonical home — never a kit fork.
- **`.gitignore` media catch (PP, found live):** a repo root `.gitignore`
  with `*.jpg` / `*.webm` silently drops the reference library's media files
  on `git add` — the commit lands with the manifest but no reference files,
  and nothing errors. After every `git add` of kit files, count:
  `git ls-tree -r --name-only HEAD -- <kit-dir>` must equal the kit file list.
  The 8 pinned reference files are force-added (`git add -f`) with the
  exception documented in the commit message — pinned, manifest-hashed
  references only, never lane output.
- **Instruction-gated PRs (western-heart, found live):** some repos require
  the 6-section PR body or the merge is blocked (`instruction-gate`). Use
  `lane-ops/pr_body_template.md` for every PR body from the start — a plain
  paragraph body fails the gate and costs a re-run.

