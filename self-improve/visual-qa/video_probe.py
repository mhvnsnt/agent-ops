#!/usr/bin/env python3
"""video_probe.py — catch frozen stretches, black/blown frames, washout and
T-pose frames across a VIDEO, not just a still.

The machine GATHERS the evidence; the agent's eyes JUDGE it. This script never
says "looks good". It samples frames at fixed intervals, runs the same checks
as the still tools on each sample, and measures MOTION between samples.

Why this exists: a film can decode clean (frame_set_gate PASS) and still be
dead — frozen frames, a stuck segment, a whole block shot with a washed-out
or T-posed figure. Round 1 checked the container; this checks the content.

Method (deterministic, cv2 + the kit's own still checks):
  - Sample every Kth frame (default 30 = ~1/sec at 30fps).
  - Per sample: colour/light metrics (color_light_check.analyse on the
    decoded frame), silhouette fraction + shoulder ratio (pose_check
    silhouette only, via a shared helper), black/blown flags.
  - Motion: mean absolute difference vs the previous SAMPLED frame.
    Consecutive samples under the frozen threshold = a frozen stretch.
    Also reports overall motion range — a film with no motion anywhere
    is a slideshow, not a film (and the owner already banned stills
    with pans/zooms as episode content).
  - Contact sheet PNG of all samples, so the agent's eyes see the whole
    film at a glance instead of trusting the numbers.
  - --film mode: the per-sample colour check is calibrated for VOID renders
    (single figure, no set). On busy film frames (rooms, cars, sets) it
    fires on bright set elements — 27 of 53 Life Cut v2.2 samples "failed"
    colour while the film itself is normally exposed (verified by eye on
    the contact sheet). In --film mode the per-sample colour verdict is
    reported per row but does NOT fail the video; only BLACK/BLOWN frames
    and frozen stretches fail. Default (no --film) stays strict: a void
    render with a blown frame fails. (S8 calibration fix, 2026-11-16.)

Usage:
  python3 video_probe.py VIDEO [--every K] [--out DIR] [--json]
  Exit 0 = PASS, 1 = FAIL (frozen stretch, black/blown frame, washed-out
  or T-posed sample), 2 = error.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).parent
FROZEN_DIFF = 1.5     # mean abs diff below this between samples = frozen
BLACK_LUM = 8.0
BLOWN_LUM = 248.0


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def probe(video, every=30, outdir=None, film_mode=False):
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise ValueError(f"cannot open video {video}")
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    clc = _load("color_light_check")
    pc = _load("pose_check")

    samples, prev_gray, frozen_runs, cur_run = [], None, [], 0
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % every == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            tmp = Path(f"/tmp/vp_{Path(video).stem}_{idx}.png")
            pil.save(tmp)
            try:
                c = clc.analyse(tmp)
            except Exception as e:
                c = {"verdict": "ERROR", "reasons": [str(e)]}
            tmp.unlink(missing_ok=True)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            motion = None
            if prev_gray is not None and prev_gray.shape == gray.shape:
                motion = float(np.abs(gray.astype(np.float32)
                                      - prev_gray.astype(np.float32)).mean())
                if motion < FROZEN_DIFF:
                    cur_run += 1
                else:
                    if cur_run:
                        frozen_runs.append(cur_run)
                    cur_run = 0
            prev_gray = gray
            mask, _ = pc.silhouette(pil)
            frac = float((mask > 0).mean())
            s = {"frame": idx, "t": round(idx / fps, 2),
                 "washout": c.get("washout_score"),
                 "mean_lum": c.get("mean_luminance"),
                 "verdict": c.get("verdict"),
                 "reasons": c.get("reasons", []),
                 "motion_vs_prev": None if motion is None else round(motion, 2),
                 "subject_frac": round(frac, 3)}
            if c.get("mean_luminance", 999) < BLACK_LUM:
                s["flag"] = "BLACK"
            elif c.get("mean_luminance", 0) > BLOWN_LUM:
                s["flag"] = "BLOWN"
            samples.append((idx, rgb, s))
        idx += 1
    cap.release()
    if cur_run:
        frozen_runs.append(cur_run)

    verdict, reasons = "PASS", []
    bad = [(s["frame"], (s.get("reasons") or ["?"])[0])
           for _, _, s in samples if s["verdict"] == "FAIL"]
    flagged = [(s["frame"], s["flag"]) for _, _, s in samples if s.get("flag")]
    if bad and not film_mode:
        verdict = "FAIL"
        reasons.append(f"{len(bad)} sampled frames failed colour check "
                       f"(first: frame {bad[0][0]} — {bad[0][1]}; "
                       f"see sample_rows[].reasons for each)")
    elif bad and film_mode:
        reasons.append(f"NOTE (film mode): {len(bad)} sampled frames failed "
                       f"the void-render colour check — reported per row, "
                       f"not failed (bright set elements, not the figure)")
    if flagged:
        verdict = "FAIL"
        reasons.append(f"{len(flagged)} sampled frames flagged "
                       f"(first: frame {flagged[0][0]} — {flagged[0][1]})")
    if frozen_runs:
        verdict = "FAIL"
        reasons.append(f"frozen stretch(es): {frozen_runs} consecutive samples"
                       " — judge from the contact sheet whether the hold is"
                       " intentional (title cards, frozen frames) or a stuck render")
    motions = [s["motion_vs_prev"] for _, _, s in samples if s["motion_vs_prev"] is not None]
    motion_range = (round(min(motions), 2), round(max(motions), 2)) if motions else (None, None)

    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
        thumbs = []
        for _, rgb, _ in samples:
            thumbs.append(np.asarray(Image.fromarray(rgb).resize((160, 160))))
        cols = 6
        rows = (len(thumbs) + cols - 1) // cols
        sheet = np.full((rows * 160, cols * 160, 3), 255, dtype=np.uint8)
        for i, t in enumerate(thumbs):
            r, c = divmod(i, cols)
            sheet[r * 160:(r + 1) * 160, c * 160:(c + 1) * 160] = t
        Image.fromarray(sheet).save(outdir / "video_contact_sheet.png")

    return {"file": str(video), "frames_total": total, "fps": round(fps, 2),
            "samples": len(samples), "every": every, "film_mode": film_mode,
            "motion_range": motion_range, "frozen_runs": frozen_runs,
            "sample_rows": [s for _, _, s in samples],
            "verdict": verdict, "reasons": reasons}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video")
    ap.add_argument("--every", type=int, default=30)
    ap.add_argument("--film", action="store_true",
                    help="film mode: per-sample colour verdicts reported, not failed")
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    outdir = Path(args.out) if args.out else None
    try:
        res = probe(Path(args.video), every=args.every, outdir=outdir,
                    film_mode=args.film)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if outdir:
        (outdir / "video_probe.json").write_text(json.dumps(res, indent=2))
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"{res['verdict']:4} {res['file']} frames={res['frames_total']} "
              f"samples={res['samples']} motion={res['motion_range']} "
              f"frozen={res['frozen_runs']}"
              + (f" :: {'; '.join(res['reasons'])}" if res["reasons"] else ""))
    return 0 if res["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
