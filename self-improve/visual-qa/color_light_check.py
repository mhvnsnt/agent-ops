#!/usr/bin/env python3
"""color_light_check.py — catch washout, bad exposure, lighting and colour junk
in a render BEFORE it reaches the owner.

The machine GATHERS the evidence; the agent's eyes JUDGE it. This script never
says "looks good". It reports colour/light numbers + a verdict on the one
question it can answer: is this image washed out, clipped, or colour-broken?

Why this exists: the Megami live proof (2026-11-07) shipped pale, tiny,
back-to-camera, on the ground — root cause junk vertex colours + fight-stack
lighting — while numeric "loaded OK" checks passed. A render can parse fine
and still be visibly washed out. This check measures what the eye sees:
luminance, saturation, contrast, clipping, colour cast.

Method (deterministic, PIL/numpy/cv2 only):
  - Subject stats: if the image has an alpha channel, stats run on
    non-transparent pixels ONLY (the subject, not the white void background).
    Without alpha, stats run on the whole frame and on a centre crop.
  - Washout score 0-100 from three signals that all fire together in a
    washed-out render: high mean luminance, low mean saturation, low contrast.
  - Clipping: % of pixels pinned at 0 or 255 per channel.
  - Colour cast: grey-world deviation (mean R vs mean B) on NEAR-NEUTRAL
    pixels only (sat < 40) — skin is warm by nature, so measuring cast on
    skin is a false positive; whites/grays reveal a real lighting cast.
  - Clipping: only BLOWN areas count — connected clipped regions >= 0.5%
    of the subject. Isolated specular dots on glossy skin are normal.
  - Junk-colour proxy: share of subject pixels in unnatural hue bands
    (extreme magenta/green) at non-trivial saturation — vertex-colour junk
    shows up as blotches the eye reads as "wrong colour", not as a cast.

Usage:
  python3 color_light_check.py IMAGE [IMAGE ...] [--out DIR] [--json]
      [--crop X0 Y0 X1 Y1]   # one panel of a side-by-side plate, fractions
  Exit 0 = PASS (no washout, no clipping, no cast), 1 = FAIL, 2 = error.
  SCOPE: single renders on void backgrounds, or one panel of a plate via
  --crop. A whole side-by-side plate (source photo + render + caption bar)
  is NOT one subject — the background mask is meaningless on it.
  Thresholds are calibrated on real cases in TEST-LOG.md; they are a floor,
  not a taste test — a PASS here never means "looks good".
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

WASHOUT_FAIL = 60.0
WASHOUT_WARN = 40.0
CLIP_FAIL = 5.0      # % of subject pixels pinned at 0 or 255
CAST_FAIL = 28.0     # grey-world |mean R - mean B| on 0-255 scale
JUNK_FAIL = 3.0      # % of subject pixels in unnatural hue bands


def subject_pixels(img):
    """Return (rgb array of subject pixels, method, 2D subject mask or None).
    Alpha first; without alpha, exclude near-background pixels
    (corner-median colour) so a white void background is not counted as
    clipped highlights on the subject."""
    import numpy as _np
    arr = _np.asarray(img.convert("RGBA"))
    alpha = arr[:, :, 3]
    if alpha.min() < 250 and (alpha < 250).sum() > 100:
        mask = alpha > 128
        return arr[:, :, :3][mask], "alpha", mask
    rgb = _np.asarray(img.convert("RGB"))
    h, w = rgb.shape[:2]
    corners = _np.concatenate([
        rgb[:8, :8].reshape(-1, 3), rgb[:8, -8:].reshape(-1, 3),
        rgb[-8:, :8].reshape(-1, 3), rgb[-8:, -8:].reshape(-1, 3)]).astype(_np.int16)
    bg = _np.median(corners, axis=0)
    dist = _np.abs(rgb.astype(_np.int16) - bg).max(axis=2)
    mask = dist > 40
    if mask.sum() < 100:
        return rgb.reshape(-1, 3), "whole-frame", None
    return rgb[mask], "background-distance", mask


def analyse(path, crop=None):
    """crop: optional (x0, y0, x1, y1) fractions — analyse one panel of a
    side-by-side plate (e.g. 0.5 0 1 0.9 = the render half, minus the
    caption bar). Without it, the whole image is one subject."""
    img = Image.open(path)
    if crop is not None:
        w, h = img.size
        x0, y0, x1, y1 = crop
        img = img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    px, method, smask = subject_pixels(img)
    if len(px) == 0:
        raise ValueError("no subject pixels found")
    pxf = px.astype(np.float64)
    r, g, b = pxf[:, 0], pxf[:, 1], pxf[:, 2]
    mx = pxf.max(axis=1)
    mn = pxf.min(axis=1)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    sat = np.where(mx == 0, 0.0, (mx - mn) / np.maximum(mx, 1e-6)) * 255.0

    mean_lum = float(lum.mean())
    std_lum = float(lum.std())
    mean_sat = float(sat.mean())
    pct_gray = float((sat < 15).mean() * 100.0)
    # Clipping: only BLOWN areas count — connected clipped regions of
    # >=0.5% of the subject. Isolated specular dots on glossy skin are
    # normal in a render and do not count. Falls back to raw % when no
    # 2D mask exists (whole-frame mode).
    clip_hi_raw = float(((pxf >= 254).any(axis=1)).mean() * 100.0)
    clip_lo_raw = float(((pxf <= 1).any(axis=1)).mean() * 100.0)
    clip_hi, clip_lo = clip_hi_raw, clip_lo_raw
    if smask is not None:
        import cv2
        rgb_full = np.asarray(img.convert("RGB"))
        floor = 0.005 * len(pxf)

        def blown_pct(channel_test):
            n, labels, stats, _ = cv2.connectedComponentsWithStats(
                (channel_test & smask).astype(np.uint8), connectivity=8)
            blown = sum(int(stats[i, cv2.CC_STAT_AREA]) for i in range(1, n)
                        if stats[i, cv2.CC_STAT_AREA] >= floor)
            return float(blown / max(len(pxf), 1) * 100.0)

        clip_hi = blown_pct(rgb_full.max(axis=2) >= 254)
        clip_lo = blown_pct(rgb_full.min(axis=2) <= 1)
    # Colour cast: grey-world on NEAR-NEUTRAL pixels only. Skin is warm
    # by nature (R-B ~30-50 is normal) — measuring cast on skin is a false
    # positive. Whites/grays in the image reveal a real lighting cast.
    neutral = sat < 40
    if neutral.sum() >= max(100, 0.01 * len(pxf)):
        cast = float(abs(r[neutral].mean() - b[neutral].mean()))
    else:
        cast = 0.0

    # Unnatural hue bands (magenta/green blotches) at real saturation.
    # CALIBRATION FIX (S8, 2026-11-16): the first band was h > 280, which
    # catches CRIMSON (280-360) — legitimate red hair and lips. Sintel's
    # red hair scored 6.3% "junk" and the reference failed its own check.
    # True magenta/violet is 290-330; crimson/red (330-360, 0-20) is real
    # hair/lip colour and is excluded. Green 80-160 stays: green blotches
    # on skin are vertex-colour junk (the Megami case), not a real colour.
    import colorsys  # noqa: F401  (kept for clarity; computed vectorised below)
    hsv_sat = sat / 255.0
    hue = np.zeros(len(pxf))
    # vectorised hue via max-channel routing
    cmax = mx
    cmin = mn
    delta = cmax - cmin
    with np.errstate(divide="ignore", invalid="ignore"):
        h = np.where(cmax == r, ((g - b) / np.where(delta == 0, 1, delta)) % 6,
            np.where(cmax == g, (b - r) / np.where(delta == 0, 1, delta) + 2,
                     (r - g) / np.where(delta == 0, 1, delta) + 4)) * 60.0
    h = np.where(delta == 0, 0.0, h)
    junk = float((((h > 290) & (h < 330) | ((h > 80) & (h < 160))) & (hsv_sat > 0.25)).mean() * 100.0)

    # Washout score: all three signals must fire together.
    lum_part = max(0.0, (mean_lum - 170.0) / 85.0) * 40.0
    sat_part = max(0.0, (45.0 - mean_sat) / 45.0) * 35.0
    con_part = max(0.0, (30.0 - std_lum) / 30.0) * 25.0
    washout = float(min(100.0, lum_part + sat_part + con_part))

    verdict = "PASS"
    reasons = []
    if washout >= WASHOUT_FAIL:
        verdict = "FAIL"
        reasons.append(f"washout {washout:.1f} >= {WASHOUT_FAIL}")
    elif washout >= WASHOUT_WARN:
        verdict = "WARN"
        reasons.append(f"washout {washout:.1f} (watch)")
    if clip_hi >= CLIP_FAIL or clip_lo >= CLIP_FAIL:
        verdict = "FAIL"
        reasons.append(f"clipping hi {clip_hi:.1f}% / lo {clip_lo:.1f}%")
    if cast >= CAST_FAIL:
        verdict = "FAIL"
        reasons.append(f"colour cast {cast:.1f} >= {CAST_FAIL}")
    if junk >= JUNK_FAIL:
        verdict = "FAIL"
        reasons.append(f"unnatural hue blotches {junk:.1f}% >= {JUNK_FAIL}")

    return {
        "file": str(path),
        "subject_method": method,
        "subject_pixels": int(len(px)),
        "mean_luminance": round(mean_lum, 2),
        "contrast_std": round(std_lum, 2),
        "mean_saturation": round(mean_sat, 2),
        "pct_near_gray": round(pct_gray, 2),
        "clip_high_pct": round(clip_hi, 2),
        "clip_low_pct": round(clip_lo, 2),
        "colour_cast_r_minus_b": round(cast, 2),
        "unnatural_hue_pct": round(junk, 2),
        "washout_score": round(washout, 2),
        "verdict": verdict,
        "reasons": reasons,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--crop", nargs=4, type=float, default=None,
                    metavar=("X0", "Y0", "X1", "Y1"),
                    help="analyse only this fractional region (one panel of a plate)")
    args = ap.parse_args()

    results = []
    worst = 0
    for p in args.images:
        try:
            res = analyse(Path(p), crop=args.crop)
        except Exception as e:
            print(f"ERROR {p}: {e}", file=sys.stderr)
            return 2
        results.append(res)
        if res["verdict"] == "FAIL":
            worst = 1
    if args.out:
        outdir = Path(args.out)
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "color_light.json").write_text(json.dumps(results, indent=2))
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['verdict']:4} {r['file']} washout={r['washout_score']:.1f} "
                  f"lum={r['mean_luminance']:.0f} con={r['contrast_std']:.0f} "
                  f"sat={r['mean_saturation']:.0f} clip={r['clip_high_pct']:.1f}/{r['clip_low_pct']:.1f} "
                  f"cast={r['colour_cast_r_minus_b']:.0f} junk={r['unnatural_hue_pct']:.1f}"
                  + (f" :: {'; '.join(r['reasons'])}" if r["reasons"] else ""))
    return worst


if __name__ == "__main__":
    sys.exit(main())
