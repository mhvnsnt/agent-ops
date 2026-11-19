#!/usr/bin/env python3
"""pair_compare.py — deterministic visual evidence for a before/after pair.

The machine GATHERS the evidence; the agent's eyes JUDGE it. This script never
says "looks good". It reports numbers + a diff heatmap and a mechanical verdict
on the one question it can answer: did these two images change, and by how much.

Method (industry standard, see README):
  - SSIM (Wang et al. 2004, skimage) — structural similarity the way human
    vision works; forgiving of rendering noise, catches real change.
  - Mean absolute pixel difference + % of pixels over threshold — the
    pixelmatch-style raw signal.
  - Diff heatmap PNG (red = changed pixels) for the agent to look at.

Usage:
  python3 pair_compare.py BEFORE AFTER --expect same|different --out DIR
    --expect same      : FAIL if SSIM < 0.98 (a frozen frame must not move)
    --expect different : FAIL if SSIM >= 0.98 (a re-shot frame must actually
                         differ — catches "re-rendered but identical" fakes)
  Writes DIR/diff.png + DIR/verdict.json, prints one JSON line to stdout.
  Exit code 0 = mechanical verdict PASS, 1 = FAIL, 2 = usage/IO error.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SSIM_SAME = 0.98   # at/above this, the pair is effectively identical
DIFF_THRESH = 12   # per-channel abs diff above this counts as "changed pixel"


def load_gray(path):
    img = Image.open(path).convert("RGB")
    return np.asarray(img), np.asarray(img.convert("L"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--expect", choices=["same", "different"], required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    try:
        from skimage.metrics import structural_similarity as ssim
    except ImportError:
        print("ERROR: scikit-image is required (pip install scikit-image)",
              file=sys.stderr)
        return 2

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    try:
        a_rgb, a_gray = load_gray(args.before)
        b_rgb, b_gray = load_gray(args.after)
    except (OSError, ValueError) as e:
        print(f"ERROR: cannot read input image: {e}", file=sys.stderr)
        return 2
    if a_rgb.shape != b_rgb.shape:
        print(f"ERROR: size mismatch {a_rgb.shape} vs {b_rgb.shape}",
              file=sys.stderr)
        return 2

    s = float(ssim(a_gray, b_gray, data_range=255))
    absdiff = np.abs(a_rgb.astype(np.int16) - b_rgb.astype(np.int16))
    mean_abs = float(absdiff.mean())
    changed = (absdiff.max(axis=2) > DIFF_THRESH)
    pct_changed = float(changed.mean() * 100.0)

    # Heatmap: red where changed, original elsewhere (dimmed).
    heat = (a_rgb * 0.35).astype(np.uint8)
    heat[changed] = np.array([255, 0, 0], dtype=np.uint8)
    Image.fromarray(heat).save(outdir / "diff.png")

    if args.expect == "same":
        passed = s >= SSIM_SAME
        reason = ("identical within tolerance" if passed
                  else f"SSIM {s:.4f} < {SSIM_SAME}: frame moved, expected frozen")
    else:
        passed = s < SSIM_SAME
        reason = ("frames differ" if passed
                  else f"SSIM {s:.4f} >= {SSIM_SAME}: frame did not change, "
                       "expected a re-shot")

    verdict = {
        "before": str(args.before),
        "after": str(args.after),
        "expect": args.expect,
        "ssim": round(s, 5),
        "mean_abs_diff": round(mean_abs, 3),
        "pct_pixels_changed": round(pct_changed, 2),
        "diff_png": str(outdir / "diff.png"),
        "verdict": "PASS" if passed else "FAIL",
        "reason": reason,
    }
    (outdir / "verdict.json").write_text(json.dumps(verdict, indent=2))
    print(json.dumps(verdict))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
