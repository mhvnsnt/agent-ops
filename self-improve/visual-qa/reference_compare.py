#!/usr/bin/env python3
"""reference_compare.py — compare OUR render against a TOP reference side by
side, the way the owner learns what's good.

The machine GATHERS the evidence; the agent's eyes JUDGE it — and the OWNER's
eyes judge it too. This script never says "looks good". It builds the
side-by-side sheet (ours | reference, same framing) and a metrics table
comparing ours against the reference's band, so the verdict is "this looks
like industry standard" or "this doesn't" — never a guess, never a number
alone.

Why this exists (owner 2026-11-16 ~09:45-09:47 EST): the way to learn what's
good is to study the TOP-ACCLAIMED, highest-approved, industry-standard work
— work DOWN THE LIST FROM THE TOP — and look at that AND our work side by
side. And the references get shown to HIM every turn so HE CAN APPROVE them —
TWO PAIRS OF EYES. The side-by-side sheet this script writes IS that
presentation artifact.

The reference is the FLOOR, not the ceiling (owner ~09:46 EST): after
matching the top standard, do BETTER than them. So the verdict bands are:
  BELOW  — a key metric is worse than the reference band (must fix)
  MEETS  — at the reference band (industry standard reached)
  ABOVE  — better than the reference band in the good direction (the goal)
Metrics compared (direction in brackets): washout [lower better],
contrast [higher better], saturation [within band], clipping [lower better],
colour cast [lower better], shoulder ratio [within band — arms down, not T].

Usage:
  python3 reference_compare.py --ours OUR.png --ref REF.png [--ref-id ID]
      [--manifest manifest.json] [--out DIR] [--json]
  --ref-id looks the reference up in the library manifest (title, source,
  licence, why it's the top of its field). --ref gives a bare path.
  Writes DIR/side_by_side.png + DIR/reference_compare.json.
  Exit 0 = MEETS or ABOVE, 1 = BELOW, 2 = error.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).parent
REFDIR = HERE.parent / "reference"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sheet(ours_path, ref_path, out_path, height=600):
    a = Image.open(ours_path).convert("RGB")
    b = Image.open(ref_path).convert("RGB")
    def scale(im):
        w, h = im.size
        return im.resize((int(w * height / h), height))
    a, b = scale(a), scale(b)
    w = a.width + b.width + 12
    canvas = Image.new("RGB", (w, height + 36), (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    canvas.paste(a, (0, 36))
    canvas.paste(b, (a.width + 12, 36))
    d.text((8, 10), "OURS", fill=(200, 0, 0))
    d.text((a.width + 20, 10), "REFERENCE (top of field)", fill=(0, 120, 0))
    canvas.save(out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ours", required=True)
    ap.add_argument("--ref", default=None)
    ap.add_argument("--ref-id", default=None)
    ap.add_argument("--manifest", default=str(REFDIR / "manifest.json"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    ref_path, ref_meta = args.ref, {}
    if args.ref_id:
        man = json.loads(Path(args.manifest).read_text())
        hit = [m for m in man.get("references", []) if m["id"] == args.ref_id]
        if not hit:
            print(f"ERROR: ref-id {args.ref_id} not in manifest", file=sys.stderr)
            return 2
        ref_meta = hit[0]
        ref_path = str(REFDIR / ref_meta["file"])
    if not ref_path or not Path(ref_path).exists():
        print("ERROR: reference image not found", file=sys.stderr)
        return 2

    clc = _load("color_light_check")
    pc = _load("pose_check")
    ours_c = clc.analyse(Path(args.ours))
    ref_c = clc.analyse(Path(ref_path))
    ours_p = pc.analyse(Path(args.ours))
    ref_p = pc.analyse(Path(ref_path))

    # Band comparisons. Reference = floor — BUT the band is the reference's
    # GOOD RANGE, not its exact number (S8 calibration fix, 2026-11-16).
    # The first version compared exact values with a tight tolerance, so a
    # washout of 7 vs the reference's 0 counted as BELOW even though both
    # are far inside the good range, and a face render's saturation (102)
    # "failed" against a fire-lit film still (193) — different content,
    # not a quality gap. BELOW now means: ours is in the BAD range while
    # the reference is good. MEETS = ours is in the good range. ABOVE =
    # ours beats the reference's own value in the good direction.
    # Good-range floors come from color_light_check's own thresholds
    # (washout WARN 40 / FAIL 60, clip FAIL 5, cast FAIL 28).
    def band(ours_v, ref_v, metric):
        if ours_v is None or ref_v is None:
            return "n/a"
        if metric == "washout_score":      # lower better; good < 40
            if ours_v < ref_v - 5:
                return "ABOVE"
            return "MEETS" if ours_v <= 40 else "BELOW"
        if metric == "contrast_std":       # higher better; good >= 20
            if ours_v > ref_v + 5:
                return "ABOVE"
            return "MEETS" if ours_v >= 20 else "BELOW"
        if metric == "mean_saturation":    # plausible band, not a race
            if ours_v > ref_v + 10:
                return "ABOVE"
            return "MEETS" if 20 <= ours_v <= 220 else "BELOW"
        if metric == "clip_high_pct":      # lower better; good <= 5
            if ours_v < ref_v - 1:
                return "ABOVE"
            return "MEETS" if ours_v <= 5 else "BELOW"
        if metric == "colour_cast":        # lower better; good <= 28
            if ours_v < ref_v - 5:
                return "ABOVE"
            return "MEETS" if ours_v <= 28 else "BELOW"
        if metric == "shoulder_ratio":     # within band only; any wide
            # deviation is bad (a T-pose has a HIGHER ratio — never ABOVE)
            return "MEETS" if abs(ours_v - ref_v) <= 0.15 else "BELOW"
        return "n/a"

    rows = [
        {"metric": "washout_score", "ours": ours_c["washout_score"],
         "reference": ref_c["washout_score"],
         "band": band(ours_c["washout_score"], ref_c["washout_score"], "washout_score")},
        {"metric": "contrast_std", "ours": ours_c["contrast_std"],
         "reference": ref_c["contrast_std"],
         "band": band(ours_c["contrast_std"], ref_c["contrast_std"], "contrast_std")},
        {"metric": "mean_saturation", "ours": ours_c["mean_saturation"],
         "reference": ref_c["mean_saturation"],
         "band": band(ours_c["mean_saturation"], ref_c["mean_saturation"], "mean_saturation")},
        {"metric": "clip_high_pct", "ours": ours_c["clip_high_pct"],
         "reference": ref_c["clip_high_pct"],
         "band": band(ours_c["clip_high_pct"], ref_c["clip_high_pct"], "clip_high_pct")},
        {"metric": "colour_cast", "ours": ours_c["colour_cast_r_minus_b"],
         "reference": ref_c["colour_cast_r_minus_b"],
         "band": band(ours_c["colour_cast_r_minus_b"], ref_c["colour_cast_r_minus_b"], "colour_cast")},
        {"metric": "shoulder_ratio", "ours": ours_p.get("shoulder_ratio"),
         "reference": ref_p.get("shoulder_ratio"),
         "band": band(ours_p.get("shoulder_ratio"), ref_p.get("shoulder_ratio"), "shoulder_ratio")},
    ]
    bands = [r["band"] for r in rows if r["band"] != "n/a"]
    verdict = "BELOW" if "BELOW" in bands else ("ABOVE" if all(b == "ABOVE" for b in bands) else "MEETS")
    res = {"ours": str(args.ours), "reference": str(ref_path),
           "reference_meta": ref_meta, "rows": rows, "verdict": verdict,
           "note": "Reference is the FLOOR. MEETS = industry standard reached. "
                   "ABOVE = better than the top. BELOW = fix before delivery. "
                   "The side-by-side sheet is for the owner's eyes — he judges."}
    outdir = Path(args.out) if args.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
        sheet(args.ours, ref_path, outdir / "side_by_side.png")
        (outdir / "reference_compare.json").write_text(json.dumps(res, indent=2))
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"{verdict:5} ours={args.ours} ref={ref_path}")
        for r in rows:
            print(f"  {r['band']:5} {r['metric']:18} ours={r['ours']} ref={r['reference']}")
    return 0 if verdict in ("MEETS", "ABOVE") else 1


if __name__ == "__main__":
    sys.exit(main())
