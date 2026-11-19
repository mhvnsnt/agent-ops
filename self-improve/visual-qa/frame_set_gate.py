#!/usr/bin/env python3
"""frame_set_gate.py — deterministic frame-set gate for a film/render lane.

The machine GATHERS the evidence; the agent's eyes JUDGE the frames.
Run BEFORE any ffmpeg assembly and BEFORE any "capture complete" claim.

Checks (all mechanical, all with numbers):
  1. Contiguity: frames f00000.png..fNNNNN.png present, zero gaps.
     (ffmpeg image2 stops silently at the first gap — a count alone is NOT proof.)
  2. Truncation: zero zero-byte frames; every PNG decodes via PIL; report
     the smallest file (an outlier small file is a truncated frame).
  3. Frozen byte-identity: if a sha256 manifest is given, every frame listed
     in it must hash EXACTLY (the untouched range of a fix pass).
  4. Optional: full-decode check of an assembled mp4 (ffmpeg, zero errors)
     and ffprobe frame count.

Usage:
  python3 frame_set_gate.py FRAMES_DIR --expect N
      [--manifest SHA256_FILE] [--video MP4] [--out DIR]
  Writes DIR/gate.json, prints one JSON line. Exit 0 = all checks pass.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

FRAME_RE = re.compile(r"^f(\d+)\.png$")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("frames_dir")
    ap.add_argument("--expect", type=int, required=True)
    ap.add_argument("--manifest")
    ap.add_argument("--video")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    frames_dir = Path(args.frames_dir)
    checks, failures = {}, []

    frames = {}
    for p in frames_dir.iterdir():
        m = FRAME_RE.match(p.name)
        if m and p.is_file():
            frames[int(m.group(1))] = p
    checks["frames_found"] = len(frames)

    # 1. Contiguity
    missing = [i for i in range(args.expect) if i not in frames]
    checks["contiguity_missing"] = missing[:20]
    checks["contiguity_missing_count"] = len(missing)
    if missing:
        failures.append(f"contiguity: {len(missing)} missing frames "
                        f"(first: {missing[:5]})")

    # 2. Truncation / decode
    zero_byte, undecodable, sizes = [], [], []
    for i in sorted(frames):
        p = frames[i]
        sz = p.stat().st_size
        sizes.append(sz)
        if sz == 0:
            zero_byte.append(i)
            continue
        try:
            with Image.open(p) as im:
                im.load()
        except Exception as e:
            undecodable.append([i, str(e)[:120]])
    checks["zero_byte"] = zero_byte[:20]
    checks["zero_byte_count"] = len(zero_byte)
    checks["undecodable"] = undecodable[:10]
    checks["undecodable_count"] = len(undecodable)
    checks["smallest_bytes"] = min(sizes) if sizes else 0
    if zero_byte:
        failures.append(f"truncation: {len(zero_byte)} zero-byte frames")
    if undecodable:
        failures.append(f"truncation: {len(undecodable)} undecodable PNGs")

    # 3. Frozen byte-identity vs manifest (format: "<sha>  <filename>" or
    #    "<sha> *<filename>", one per line; filename matched by basename)
    if args.manifest:
        manifest = {}
        for line in Path(args.manifest).read_text().splitlines():
            parts = line.split()
            if len(parts) >= 2:
                manifest[Path(parts[1].lstrip("*")).name] = parts[0]
        matched, mismatched, absent = 0, [], []
        for name, want in manifest.items():
            p = frames_dir / name
            if not p.exists():
                absent.append(name)
                continue
            got = sha256_file(p)
            if got == want:
                matched += 1
            else:
                mismatched.append(name)
        checks["manifest_total"] = len(manifest)
        checks["manifest_matched"] = matched
        checks["manifest_mismatched"] = mismatched[:20]
        checks["manifest_absent"] = absent[:20]
        if mismatched or absent:
            failures.append(f"frozen identity: {len(mismatched)} changed, "
                            f"{len(absent)} absent of {len(manifest)}")

    # 4. Optional assembled-video decode check
    if args.video:
        vp = Path(args.video)
        if not vp.exists():
            failures.append(f"video: {vp} does not exist")
            checks["video"] = "missing"
        else:
            dec = subprocess.run(
                ["ffmpeg", "-v", "error", "-i", str(vp), "-f", "null", "-"],
                capture_output=True, text=True)
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-count_frames",
                 "-select_streams", "v:0",
                 "-show_entries", "stream=nb_read_frames",
                 "-of", "csv=p=0", str(vp)],
                capture_output=True, text=True)
            nframes = probe.stdout.strip()
            checks["video_decode_stderr"] = dec.stderr.strip()[:500]
            checks["video_nb_frames"] = nframes
            if dec.returncode != 0 or dec.stderr.strip():
                failures.append("video: ffmpeg decode errors")
            elif nframes and nframes != str(args.expect):
                failures.append(f"video: ffprobe frames {nframes} != "
                                f"expected {args.expect}")

    verdict = {
        "frames_dir": str(frames_dir),
        "expect": args.expect,
        "checks": checks,
        "failures": failures,
        "verdict": "PASS" if not failures else "FAIL",
    }
    (outdir / "gate.json").write_text(json.dumps(verdict, indent=2))
    print(json.dumps(verdict))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
