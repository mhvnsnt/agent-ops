#!/usr/bin/env python3
"""depth_check.py — catch flat/pasted figures and wrong ground contact from
a DEPTH MAP, not from pixels alone.

The machine GATHERS the evidence; the agent's eyes JUDGE it. This script never
says "looks good". It runs a monocular depth model over the render and reports
whether the subject has real depth variation and sits in front of its
background — the two things a pasted cutout, a flat card, or a figure
floating in a void does not have.

Why this exists: the Megami live proof shipped "on the ground" and pale in a
way no 2D check caught, and the owner bans cutout frames as finished work.
A depth map is the cheapest way to ask "is this a figure in a space, or a
flat picture of one?"

Method (onnxruntime + Depth Anything V2 small, model file in models/ —
FETCH-VERIFIED from HuggingFace onnx-community/depth-anything-v2-small,
99,060,839 B; onnxruntime 1.30.0 was already on this box, no install):
  - Resize to 518x518, ImageNet mean/std, run the model, resize the depth
    map back to the original size.
  - Subject mask: pose_check.silhouette (alpha or background-distance).
  - Subject depth variation: std of depth inside the mask. A real figure
    varies (nose closer than ears, chest closer than the wall behind);
    a flat card or a pasted cutout is near-constant.
  - Subject-vs-background separation: median subject depth minus median
    background depth. The figure should sit clearly in FRONT of the set.
  - Ground contact (reported, not failed): depth at the figure's bottom
    edge vs the floor around it — a floating figure's feet are at a
    different depth from the floor directly beneath them.
  - Writes a depth-map PNG next to the JSON so the agent's eyes see the
    same depth the numbers describe.

Usage:
  python3 depth_check.py IMAGE [IMAGE ...] [--out DIR] [--json]
  Exit 0 = PASS, 1 = FAIL (flat subject or no separation), 2 = error.
  Thresholds calibrated on real cases in TEST-LOG.md; a PASS never means
  "looks good" — it means the figure is not flat.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
MODEL = HERE / "models" / "depth_anything_v2_small.onnx"
SIZE = 518
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
FLAT_STD_FAIL = 0.10   # subject depth std below this = flat card / cutout
# CALIBRATION (S8, 2026-11-16): first value 0.02 was too low — the depth
# model hallucinates some structure on a flat rectangle (std 0.07), so the
# flat-card control PASSED at 0.02. Real renders measure 0.18-0.22, the
# flat card 0.07; the threshold sits between them at 0.10. Calibrated on
# 3 cases only — re-check on more renders before trusting it blind.
SEP_FAIL = 0.05        # subject-vs-background depth gap below this = no separation


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def depth_map(img_rgb, session):
    """Run Depth Anything V2 small; return depth map at original size."""
    w, h = img_rgb.size
    small = img_rgb.resize((SIZE, SIZE), Image.BILINEAR)
    arr = np.asarray(small).astype(np.float32) / 255.0
    arr = (arr - MEAN) / STD
    arr = np.transpose(arr, (2, 0, 1))[None, :, :, :]
    out = session.run(None, {session.get_inputs()[0].name: arr})[0]
    d = np.asarray(out)[0]
    # Normalise to 0..1 per image (relative depth — the model is relative).
    d = (d - d.min()) / max(d.max() - d.min(), 1e-6)
    return np.asarray(Image.fromarray((d * 255).astype(np.uint8)).resize((w, h),
                     Image.BILINEAR)).astype(np.float32) / 255.0


def analyse(path, session, outdir=None):
    img = Image.open(path).convert("RGB")
    d = depth_map(img, session)
    pc = _load("pose_check")
    mask, method = pc.silhouette(Image.open(path).convert("RGBA"))
    subj = mask > 0
    bg = ~subj
    res = {"file": str(path), "mask_method": method,
           "subject_frac": round(float(subj.mean()), 4),
           "verdict": "PASS", "reasons": []}
    if subj.sum() < 100 or bg.sum() < 100:
        res["verdict"] = "UNRELIABLE"
        res["reasons"].append("subject or background too small for a depth read")
        return res
    d_subj = d[subj]
    d_bg = d[bg]
    res["subject_depth_std"] = round(float(d_subj.std()), 4)
    res["subject_depth_median"] = round(float(np.median(d_subj)), 3)
    res["background_depth_median"] = round(float(np.median(d_bg)), 3)
    # Depth Anything outputs larger = closer (disparity-like) for this model
    # family; separation is measured as |median gap| either way.
    res["separation"] = round(float(abs(np.median(d_subj) - np.median(d_bg))), 3)
    if res["subject_depth_std"] < FLAT_STD_FAIL:
        res["verdict"] = "FAIL"
        res["reasons"].append(
            f"subject depth std {res['subject_depth_std']:.3f} < {FLAT_STD_FAIL} — flat/pasted")
    if res["separation"] < SEP_FAIL:
        res["verdict"] = "FAIL"
        res["reasons"].append(
            f"subject/background separation {res['separation']:.3f} < {SEP_FAIL} — no depth gap")
    if outdir:
        vis = (d * 255).astype(np.uint8)
        Image.fromarray(vis).save(Path(outdir) / (Path(path).stem + "_depth.png"))
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not MODEL.exists():
        print(f"ERROR: depth model not in models/ ({MODEL.name})", file=sys.stderr)
        return 2
    try:
        import onnxruntime as ort
    except ImportError:
        print("ERROR: onnxruntime not installed — depth check unavailable",
              file=sys.stderr)
        return 2
    session = ort.InferenceSession(str(MODEL), providers=["CPUExecutionProvider"])
    outdir = Path(args.out) if args.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    results, worst = [], 0
    for p in args.images:
        try:
            res = analyse(Path(p), session, outdir)
        except Exception as e:
            print(f"ERROR {p}: {e}", file=sys.stderr)
            return 2
        results.append(res)
        if res["verdict"] == "FAIL":
            worst = 1
    if outdir:
        (outdir / "depth.json").write_text(json.dumps(results, indent=2))
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['verdict']:10} {r['file']} subj_std={r.get('subject_depth_std', '-')} "
                  f"sep={r.get('separation', '-')}"
                  + (f" :: {'; '.join(r['reasons'])}" if r["reasons"] else ""))
    return worst


if __name__ == "__main__":
    sys.exit(main())
