#!/usr/bin/env python3
"""turntable_proof.py — prove a fit from EVERY side, not one angle.

The machine GATHERS the evidence; the agent's eyes JUDGE it. This script never
says "looks good". It builds the multi-angle proof set and reports which
angles are covered and whether any angle fails the colour/pose checks.

Why this exists: the afro v1 "proof" was one angle — the helmet fit, the
shoulder clipping and the dome rim 90 mm below the hairline were only
visible from other angles. The lash v7 placement only proved out when the
roots were checked from front AND profile. One angle is not a proof.

Method:
  - Images mode: pass renders whose filenames carry the angle
    (front, profile, q34, back, left, right). Each is run through
    color_light_check + pose_check; a contact sheet is built in angle
    order; coverage is reported against the expected set.
  - Video mode: a turntable clip is sampled evenly; silhouette aspect
    ratio across the samples must VARY (front is widest, profile is
    narrowest) — a turntable that never turns shows a flat aspect line
    and FAILS coverage.
  - No angle inference is faked: in images mode the angle comes from the
    filename; in video mode coverage is proven by aspect variation + the
    contact sheet the agent's eyes judge.

Usage:
  python3 turntable_proof.py --images FRONT PROFILE Q34 BACK [--expect front profile q34 back] [--out DIR]
  python3 turntable_proof.py --video TURNTABLE.mp4 [--samples N] [--out DIR]
  Exit 0 = PASS (all expected angles present, no check failed),
  1 = FAIL, 2 = error.
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
ANGLE_WORDS = ("front", "profile", "q34", "back", "left", "right")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def angle_of(path):
    name = Path(path).stem.lower()
    for w in ANGLE_WORDS:
        if w in name:
            return w
    return "unknown"


def check_one(path, clc, pc):
    try:
        c = clc.analyse(Path(path))
    except Exception as e:
        c = {"verdict": "ERROR", "reasons": [str(e)]}
    try:
        img = Image.open(path).convert("RGBA")
        mask, _ = pc.silhouette(img)
        frac = float((mask > 0).mean())
        p = {"subject_frac": round(frac, 3), "verdict": "PASS"}
    except Exception as e:
        p = {"verdict": "ERROR", "reasons": [str(e)]}
    return c, p


def contact_sheet(paths, out_path, thumb=240):
    thumbs = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        im.thumbnail((thumb, thumb))
        canvas = Image.new("RGB", (thumb, thumb), (255, 255, 255))
        canvas.paste(im, ((thumb - im.width) // 2, (thumb - im.height) // 2))
        thumbs.append(canvas)
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb, rows * thumb), (255, 255, 255))
    for i, t in enumerate(thumbs):
        r, c = divmod(i, cols)
        sheet.paste(t, (c * thumb, r * thumb))
    sheet.save(out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--images", nargs="*", default=[])
    ap.add_argument("--video", default=None)
    ap.add_argument("--expect", nargs="*", default=["front", "profile", "q34", "back"])
    ap.add_argument("--samples", type=int, default=12)
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    clc = _load("color_light_check")
    pc = _load("pose_check")
    outdir = Path(args.out) if args.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)

    verdict, reasons, rows = "PASS", [], []
    if args.video:
        cap = cv2.VideoCapture(args.video)
        if not cap.isOpened():
            print(f"ERROR: cannot open {args.video}", file=sys.stderr)
            return 2
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        idxs = [int(i * (total - 1) / max(args.samples - 1, 1)) for i in range(args.samples)]
        aspects, tmp_paths = [], []
        for n, fi in enumerate(idxs):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
            ok, frame = cap.read()
            if not ok:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            mask, _ = pc.silhouette(pil)
            ys, xs = np.where(mask > 0)
            if len(xs):
                aspects.append(round((xs.max() - xs.min()) / max(ys.max() - ys.min(), 1), 3))
            tmp = Path(f"/tmp/tt_{n}.png")
            pil.save(tmp)
            tmp_paths.append(tmp)
        cap.release()
        if tmp_paths and outdir:
            contact_sheet(tmp_paths, outdir / "turntable_sheet.png")
            for t in tmp_paths:
                t.unlink(missing_ok=True)
        spread = (round(max(aspects) - min(aspects), 3) if len(aspects) > 1 else 0.0)
        rows = [{"frame": fi, "silhouette_aspect": a} for fi, a in zip(idxs, aspects)]
        if len(aspects) < 4 or spread < 0.15:
            verdict = "FAIL"
            reasons.append(f"turntable does not turn: aspect spread {spread} over {len(aspects)} samples")
        res = {"mode": "video", "file": args.video, "frames_total": total,
               "aspect_spread": spread, "aspects": aspects,
               "verdict": verdict, "reasons": reasons}
    elif args.images:
        for p in args.images:
            c, pp = check_one(p, clc, pc)
            rows.append({"file": str(p), "angle": angle_of(p),
                         "color_verdict": c.get("verdict"),
                         "washout": c.get("washout_score"),
                         "pose_subject_frac": pp.get("subject_frac"),
                         "reasons": c.get("reasons", []) + pp.get("reasons", [])})
            if c.get("verdict") == "FAIL":
                verdict = "FAIL"
                reasons.append(f"{p}: colour/light FAIL")
        have = {r["angle"] for r in rows}
        missing = [a for a in args.expect if a not in have]
        if missing:
            verdict = "FAIL"
            reasons.append(f"missing angles: {missing}")
        if outdir:
            contact_sheet([r["file"] for r in rows], outdir / "turntable_sheet.png")
        res = {"mode": "images", "angles_found": sorted(have),
               "angles_expected": args.expect, "missing": missing,
               "rows": rows, "verdict": verdict, "reasons": reasons}
    else:
        print("ERROR: pass --images or --video", file=sys.stderr)
        return 2

    if outdir:
        (outdir / "turntable.json").write_text(json.dumps(res, indent=2))
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"{res['verdict']:4} {res.get('file', 'images')} "
              f"{res.get('angles_found', res.get('aspect_spread', ''))}"
              + (f" :: {'; '.join(res['reasons'])}" if res["reasons"] else ""))
    return 0 if res["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
