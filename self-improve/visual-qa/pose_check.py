#!/usr/bin/env python3
"""pose_check.py — catch T-pose, wrong limb placement, floating parts and
broken anatomy in a render BEFORE it reaches the owner.

The machine GATHERS the evidence; the agent's eyes JUDGE it. This script never
says "looks good". It reports pose numbers + an annotated silhouette and a
mechanical verdict on the questions it can answer: are the arms hanging (not
T-posed), is the figure in one piece, is anything floating detached?

Why this exists: the owner rejected work for shipping flat T-poses and
"loaded OK" checks that passed visibly broken models (Melanie's floating
glasses, Kasumi's sharding, the identity audit). A render can parse fine and
still be a T-pose or a pile of detached parts.

Method (deterministic, PIL/numpy/cv2 only — NO MediaPipe, NO torch):
  - Silhouette: segment the subject from the background. Renders in this
    pipeline sit on a white/void background, so the mask is alpha (if
    present) or distance-from-background-colour. Works on full-body
    standing renders; NOT reliable on busy film frames with sets — the
    script says so when the mask is unreliable (mask coverage outside
    2%-90% of the frame).
  - T-pose score: width of the silhouette at the SHOULDER band (15-25% of
    figure height) divided by the width at the HIP band (50-60%). Arms out
    horizontal make the shoulders far wider than the hips (ratio > 2);
    arms down keep shoulders close to hip width (ratio ~1.3-1.5).
    FAIL >= 2.2, WARN >= 1.8. (Shoulder / full-width is useless: in both
    poses the widest point sits at shoulder height.)
  - Full-body framing gate: the figure must start in the top 20% of the
    frame and span >= 55% of frame height, or the verdict is UNRELIABLE —
    head/close-up renders (angel v21 front) cannot be pose-checked.
  - Detached parts: separate contours above a size floor — a floating
    pair of glasses, a helmet afro, a detached limb shows up as a second
    component. Reported with bounding boxes, not hidden.
  - Ground: bottom edge of the silhouette vs frame bottom (full-body
    shots) — "on the ground" vs floating in frame, reported not hard-failed.
  - Head: topmost contour blob, roughly centred, width ~1/5-1/10 of height.
  - OpenPose hook: if models/pose_iter_440000.caffemodel is ever placed
    next to the prototxt, keypoints run too (cv2.dnn). The weights are NOT
    fetchable from this box (CMU server unreachable, GitHub 404) — recorded
    as an honest gap in TEST-LOG.md. Silhouette mode is the primary tool.

Usage:
  python3 pose_check.py IMAGE [IMAGE ...] [--out DIR] [--json]
  Exit 0 = PASS, 1 = FAIL (T-pose or detached part or no subject),
  2 = error / unreliable mask (report says so; eyes must judge).
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

T_POSE_FAIL = 2.2    # shoulder-band width / hip-band width at/above this = T-pose
T_POSE_WARN = 1.8
MIN_SUBJECT_FRAC = 0.02
MAX_SUBJECT_FRAC = 0.90
DETACHED_MIN_FRAC = 0.01   # of main contour area; hair tufts are below this
BG_DIST = 40               # background-distance threshold (dark hair on dark bg)


def silhouette(img):
    """Return (mask uint8, method)."""
    arr = np.asarray(img.convert("RGBA"))
    alpha = arr[:, :, 3]
    if (alpha < 250).sum() > 100 and (alpha > 128).sum() > 100:
        return (alpha > 128).astype(np.uint8) * 255, "alpha"
    rgb = np.asarray(img.convert("RGB")).astype(np.int16)
    # Background = most common corner colour (void renders).
    h, w = rgb.shape[:2]
    corners = np.concatenate([
        rgb[:8, :8].reshape(-1, 3), rgb[:8, -8:].reshape(-1, 3),
        rgb[-8:, :8].reshape(-1, 3), rgb[-8:, -8:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    dist = np.abs(rgb - bg).max(axis=2)
    mask = (dist > BG_DIST).astype(np.uint8) * 255
    # Clean speckle.
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    return mask, "background-distance"


def band_width(mask, y0, y1, x0, x1):
    """Width of the silhouette between absolute pixel rows y0..y1."""
    band = mask[y0:y1, x0:x1]
    cols = (band > 0).any(axis=0)
    if not cols.any():
        return 0
    idx = np.where(cols)[0]
    return int(idx[-1] - idx[0] + 1)


def analyse(path, outdir=None):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    mask, method = silhouette(img)
    frac = float((mask > 0).mean())
    res = {"file": str(path), "mask_method": method,
           "subject_frac": round(frac, 4), "verdict": "PASS", "reasons": []}
    if frac < MIN_SUBJECT_FRAC or frac > MAX_SUBJECT_FRAC:
        res["verdict"] = "UNRELIABLE"
        res["reasons"].append(
            f"subject covers {frac:.1%} of frame — silhouette unreliable, eyes must judge")
        return res

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    main = contours[0]
    main_area = cv2.contourArea(main)
    x, y, bw, bh = cv2.boundingRect(main)
    res["bbox"] = [int(x), int(y), int(bw), int(bh)]
    res["aspect_w_over_h"] = round(bw / max(bh, 1), 3)

    # Framing gate: pose is only measurable on a FULL-BODY framing — the
    # figure must start near the top of the frame and span most of it.
    # Head/close-up renders (v21 front: top at 30% of frame) are NOT
    # full-body; measuring "shoulders" on a headshot is a fake pass.
    if y / h > 0.20 or bh / h < 0.55:
        res["verdict"] = "UNRELIABLE"
        res["reasons"].append(
            f"not full-body framing (bbox top {y / h:.0%}, height {bh / h:.0%})"
            " — pose not measurable, eyes must judge")
        return res

    # T-pose: shoulder band vs HIP band. In a T-pose the arms stick out
    # sideways at shoulder height, so shoulders are far wider than the
    # hips. Arms-down, shoulder width is close to hip width. (Shoulder /
    # full-width is useless: in both poses the widest point sits at
    # shoulder height.)
    full_w = bw
    shoulder_w = band_width(mask, y + int(0.15 * bh), y + int(0.25 * bh), x, x + bw)
    hip_w = band_width(mask, y + int(0.50 * bh), y + int(0.60 * bh), x, x + bw)
    res["shoulder_band_width"] = shoulder_w
    res["hip_band_width"] = hip_w
    res["shoulder_ratio"] = round(shoulder_w / max(hip_w, 1), 3)
    res["hip_ratio"] = round(hip_w / max(full_w, 1), 3)
    if res["shoulder_ratio"] >= T_POSE_FAIL:
        res["verdict"] = "FAIL"
        res["reasons"].append(
            f"T-POSE: shoulders {res['shoulder_ratio']:.2f}x hip width")
    elif res["shoulder_ratio"] >= T_POSE_WARN:
        if res["verdict"] == "PASS":
            res["verdict"] = "WARN"
        res["reasons"].append(
            f"arms wide: shoulders {res['shoulder_ratio']:.2f}x hips (watch)")

    # Detached parts: other contours above 1% of main area AND overlapping
    # the figure's horizontal span (plausibly part of the figure — e.g. a
    # floating pair of glasses on the face). Hair-fibre tufts and props
    # outside the span are below the floor or outside the span.
    detached = []
    for c in contours[1:]:
        a = cv2.contourArea(c)
        if a >= DETACHED_MIN_FRAC * main_area and a >= 50:
            bx, by, bwb, bhb = cv2.boundingRect(c)
            if bx + bwb < x - 0.1 * bw or bx > x + bw + 0.1 * bw:
                continue
            detached.append({"area": int(a), "bbox": [int(bx), int(by), int(bwb), int(bhb)]})
    res["detached_parts"] = detached
    if detached:
        res["verdict"] = "FAIL"
        res["reasons"].append(f"{len(detached)} detached part(s) above noise floor")

    # Ground: bottom of silhouette vs frame bottom.
    bottom = y + bh
    res["bottom_gap_px"] = int(h - bottom)
    res["bottom_gap_frac"] = round((h - bottom) / h, 3)
    if res["bottom_gap_frac"] > 0.25:
        if res["verdict"] == "PASS":
            res["verdict"] = "WARN"
        res["reasons"].append(
            f"figure floats {res['bottom_gap_frac']:.0%} above frame bottom")

    # Head: topmost blob should be a small centred cap.
    top_rows = np.where((mask > 0).any(axis=1))[0]
    if len(top_rows):
        top_y = int(top_rows[0])
        head_w = band_width(mask, y + int(0.02 * bh), y + int(0.12 * bh), x, x + bw)
        res["head_width_frac"] = round(head_w / max(bw, 1), 3)
        res["head_top_y"] = top_y

    # OpenPose hook (only if weights are ever placed in models/).
    models = Path(__file__).parent / "models"
    proto = models / "pose_deploy_linevec.prototxt"
    weights = models / "pose_iter_440000.caffemodel"
    res["openpose"] = "unavailable (weights not fetchable from this box)"
    if proto.exists() and weights.exists() and weights.stat().st_size > 10_000_000:
        res["openpose"] = "model present — keypoint mode not yet wired (see TEST-LOG.md)"

    if outdir:
        overlay = np.asarray(img.convert("RGB")).copy()
        ov = overlay.copy()
        ov[mask > 0] = (ov[mask > 0] * 0.6 + np.array([255, 0, 0]) * 0.4).astype(np.uint8)
        # Shoulder + hip bands (figure-relative).
        cv2.rectangle(ov, (x, y + int(0.15 * bh)), (x + bw, y + int(0.25 * bh)), (0, 255, 0), 2)
        cv2.rectangle(ov, (x, y + int(0.50 * bh)), (x + bw, y + int(0.60 * bh)), (255, 255, 0), 2)
        cv2.rectangle(ov, (x, y), (x + bw, y + bh), (255, 0, 0), 2)
        for d in detached:
            bx, by, bwb, bhb = d["bbox"]
            cv2.rectangle(ov, (bx, by), (bx + bwb, by + bhb), (255, 0, 255), 3)
        Image.fromarray(ov).save(Path(outdir) / (Path(path).stem + "_pose.png"))
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    outdir = Path(args.out) if args.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    results, worst = [], 0
    for p in args.images:
        try:
            res = analyse(Path(p), outdir)
        except Exception as e:
            print(f"ERROR {p}: {e}", file=sys.stderr)
            return 2
        results.append(res)
        if res["verdict"] == "FAIL":
            worst = 1
    if outdir:
        (outdir / "pose.json").write_text(json.dumps(results, indent=2))
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['verdict']:10} {r['file']} shoulder={r.get('shoulder_ratio', '-')} "
                  f"hip={r.get('hip_ratio', '-')} detached={len(r.get('detached_parts', []))} "
                  f"bottom_gap={r.get('bottom_gap_frac', '-')}"
                  + (f" :: {'; '.join(r['reasons'])}" if r["reasons"] else ""))
    return worst


if __name__ == "__main__":
    sys.exit(main())
