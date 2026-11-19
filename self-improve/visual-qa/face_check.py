#!/usr/bin/env python3
"""face_check.py — catch missing faces, wrong face placement, and likeness
drift in a render BEFORE it reaches the owner.

The machine GATHERS the evidence; the agent's eyes JUDGE it. This script never
says "looks good". It reports face numbers + an annotated image and a
mechanical verdict on the questions it can answer: is there a face, where is
it, are the eyes level, and does it still look like the reference person?

Why this exists: the owner rejected assembled composites where the face was
wrong (bald head, afro floating above the scalp, lashes rooted on the wrong
seam) while "loaded OK" checks passed, and the GNM v3 face's only 3/4 evidence
frame carried a 4.00 mm residual. A face check that never looks at the face
is not a check.

Method (deterministic, cv2 Haar cascades only — NO MediaPipe, NO torch):
  - Haar frontal-face + eye cascades (XML data files in models/, fetched
    from the opencv repo — data, not an install). Works on front and 3/4
    views; profile views usually find no face — the script says
    UNRELIABLE then, and the agent's eyes must judge. That is honest, not
    a fake pass.
  - Geometry: face box, eye centres, eye-line angle (tilt), eye-distance
    / face-width, eye-height / face-height, face aspect, face centre in frame.
  - Likeness vs a reference portrait (--ref): align both faces by eye
    centres (affine: scale + translate), crop the face region, SSIM on
    grayscale crops + ratio deltas. Same person, same framing scores high;
    a drifted face scores low on BOTH signals. Thresholds are calibrated on
    the real angel-megami v21-v25 multi-angle sets in TEST-LOG.md.

Usage:
  python3 face_check.py IMAGE [IMAGE ...] [--ref REFERENCE] [--out DIR] [--json]
  Exit 0 = PASS, 1 = FAIL (face geometry out of band vs reference, or face
  expected but none found with --require-face), 2 = error / no face found
  (UNRELIABLE — eyes must judge).
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

MODELS = Path(__file__).parent / "models"
FACE_XML = MODELS / "haarcascade_frontalface_default.xml"
EYE_XML = MODELS / "haarcascade_eye.xml"
SSIM_SAME_PERSON = 0.55   # aligned face-crop SSIM at/above this = same person
RATIO_DELTA_FAIL = 0.15   # any geometry ratio delta at/above this = drift


def load_cascades():
    face = cv2.CascadeClassifier(str(FACE_XML)) if FACE_XML.exists() else None
    eye = cv2.CascadeClassifier(str(EYE_XML)) if EYE_XML.exists() else None
    if face is None or face.empty():
        return None, None
    return face, eye


def detect(gray, face_c, eye_c):
    faces = face_c.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                    minSize=(40, 40))
    if len(faces) == 0:
        return None
    # Largest face wins.
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    eyes = []
    if eye_c is not None and not eye_c.empty():
        roi = gray[y:y + h, x:x + w]
        found = eye_c.detectMultiScale(roi, scaleFactor=1.1, minNeighbors=5,
                                       minSize=(12, 12))
        for ex, ey, ew, eh in sorted(found, key=lambda e: e[0])[:2]:
            eyes.append((int(x + ex + ew / 2), int(y + ey + eh / 2)))
    return {"box": [int(x), int(y), int(w), int(h)], "eyes": eyes}


def geometry(face, img_w, img_h):
    x, y, w, h = face["box"]
    g = {"face_w": w, "face_h": h, "face_aspect": round(w / max(h, 1), 3),
         "face_center_x_frac": round((x + w / 2) / img_w, 3),
         "face_center_y_frac": round((y + h / 2) / img_h, 3)}
    eyes = face["eyes"]
    if len(eyes) == 2:
        (x1, y1), (x2, y2) = eyes
        import math
        g["eye_distance"] = round(math.hypot(x2 - x1, y2 - y1), 1)
        g["eye_dist_over_face_w"] = round(g["eye_distance"] / max(w, 1), 3)
        g["eye_line_angle_deg"] = round(math.degrees(math.atan2(y2 - y1, x2 - x1)), 1)
        g["eye_height_over_face_h"] = round(((y1 + y2) / 2 - y) / max(h, 1), 3)
    return g


def align_crop(gray, face, size=128):
    """Crop the face region aligned by eye centres; None if no eyes."""
    if len(face["eyes"]) != 2:
        return None
    (x1, y1), (x2, y2) = face["eyes"]
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    dist = max(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 1)
    # Crop 2.2 eye-distances wide, centred between the eyes, eyes at 40% height.
    side = int(dist * 2.2)
    x0, y0 = int(cx - side / 2), int(cy - side * 0.4)
    crop = gray[max(y0, 0):y0 + side, max(x0, 0):x0 + side]
    if crop.size == 0:
        return None
    return np.asarray(Image.fromarray(crop).resize((size, size)))


def analyse(path, face_c, eye_c, ref=None, outdir=None):
    img = Image.open(path).convert("RGB")
    gray = np.asarray(img.convert("L"))
    ih, iw = gray.shape
    face = detect(gray, face_c, eye_c)
    res = {"file": str(path), "verdict": "PASS", "reasons": []}
    if face is None:
        res["verdict"] = "UNRELIABLE"
        res["face_found"] = False
        res["reasons"].append("no frontal/3-4 face found — eyes must judge")
        return res
    res["face_found"] = True
    res.update(geometry(face, iw, ih))
    if ref is not None:
        from skimage.metrics import structural_similarity as ssim
        ref_gray = np.asarray(Image.open(ref).convert("L"))
        ref_face = detect(ref_gray, face_c, eye_c)
        if ref_face is None:
            res["verdict"] = "UNRELIABLE"
            res["reasons"].append("no face in reference portrait")
            return res
        c1, c2 = align_crop(gray, face), align_crop(ref_gray, ref_face)
        if c1 is None or c2 is None:
            res["reasons"].append("eyes not found in one face — no SSIM likeness")
        else:
            res["face_crop_ssim"] = round(float(ssim(c1, c2, data_range=255)), 3)
        rg = geometry(ref_face, ref_gray.shape[1], ref_gray.shape[0])
        deltas = {}
        for k in ("eye_dist_over_face_w", "eye_height_over_face_h", "face_aspect"):
            if k in res and k in rg:
                deltas[k] = round(abs(res[k] - rg[k]), 3)
        res["geometry_deltas_vs_ref"] = deltas
        worst = max(deltas.values()) if deltas else 0.0
        res["worst_geometry_delta"] = worst
        if res.get("face_crop_ssim") is not None and res["face_crop_ssim"] < SSIM_SAME_PERSON:
            res["verdict"] = "FAIL"
            res["reasons"].append(
                f"face-crop SSIM {res['face_crop_ssim']:.2f} < {SSIM_SAME_PERSON} — likeness drift")
        if worst >= RATIO_DELTA_FAIL:
            res["verdict"] = "FAIL"
            res["reasons"].append(f"geometry delta {worst:.2f} >= {RATIO_DELTA_FAIL}")
    if outdir:
        ann = np.asarray(img).copy()
        x, y, w, h = face["box"]
        cv2.rectangle(ann, (x, y), (x + w, y + h), (0, 255, 0), 3)
        for ex, ey in face["eyes"]:
            cv2.circle(ann, (ex, ey), 5, (255, 0, 0), -1)
        Image.fromarray(ann).save(Path(outdir) / (Path(path).stem + "_face.png"))
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("images", nargs="+")
    ap.add_argument("--ref", default=None)
    ap.add_argument("--require-face", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    face_c, eye_c = load_cascades()
    if face_c is None:
        print("ERROR: face cascade XML not found in models/ — fetch it first",
              file=sys.stderr)
        return 2
    outdir = Path(args.out) if args.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    results, worst = [], 0
    for p in args.images:
        try:
            res = analyse(Path(p), face_c, eye_c,
                          ref=Path(args.ref) if args.ref else None, outdir=outdir)
        except Exception as e:
            print(f"ERROR {p}: {e}", file=sys.stderr)
            return 2
        results.append(res)
        if res["verdict"] == "FAIL" or (args.require_face and not res.get("face_found")):
            worst = 1
    if outdir:
        (outdir / "face.json").write_text(json.dumps(results, indent=2))
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['verdict']:10} {r['file']} face={r.get('face_found')} "
                  f"ssim={r.get('face_crop_ssim', '-')} "
                  f"worst_delta={r.get('worst_geometry_delta', '-')}"
                  + (f" :: {'; '.join(r['reasons'])}" if r["reasons"] else ""))
    return worst


if __name__ == "__main__":
    sys.exit(main())
