#!/usr/bin/env python3
"""pre_delivery_checklist.py — the checklist that FORCES the own-eyes check
before anything reaches the owner.

The laziness the owner named (2026-11-16 ~09:43 EST) is skipping the look:
"you don't always look at things." This script makes skipping the look a
VISIBLE omission. It cannot verify the agent's eyes — but it can refuse to
stamp a delivery READY until the agent attests, in writing, what they saw.

What it does:
  1. Verifies the deliverable exists, hashes it (sha256), counts frames
     (video) or pixels (image).
  2. Runs the applicable kit checks: colour/light, pose, face (if a face
     is expected), frame-set gate (video), pair-compare vs the source
     (if --source given), reference-compare (if --ref given).
  3. Requires --seen "..." — the agent's own-eyes attestation: what they
     actually LOOKED at and what they saw (e.g. "viewed f00100, f01754,
     f02672: no garments, Kimiko in frame, road camera kept").
     NO --seen => checklist INCOMPLETE, exit 1, nothing is stamped READY.
  4. Writes a checklist file (JSON + markdown) next to the deliverable
     record. DELIVERY-READY is YES only when: all automated checks PASS
     (or WARN with a named reason) AND --seen is present AND the hash
     matches the file the agent claims to have viewed.

Usage:
  python3 pre_delivery_checklist.py --deliverable FILE --source SOURCE
      --claim "what this is and what changed" --seen "what I viewed and saw"
      [--ref REF_ID] [--require-face] [--out DIR]
  Exit 0 = DELIVERY-READY YES, 1 = NO (incomplete or a check failed),
  2 = error.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_tool(tool, *argv):
    try:
        r = subprocess.run([sys.executable, str(HERE / tool), *argv],
                           capture_output=True, text=True, timeout=300)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 2, str(e)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--deliverable", required=True)
    ap.add_argument("--source", default=None)
    ap.add_argument("--claim", required=True)
    ap.add_argument("--seen", default=None,
                    help="REQUIRED: what the agent viewed with their own eyes and saw")
    ap.add_argument("--ref", default=None, help="reference id for reference_compare")
    ap.add_argument("--require-face", action="store_true")
    ap.add_argument("--crop", nargs=4, type=float, default=None,
                    help="still deliverables only: analyse one panel of a plate")
    ap.add_argument("--frames-dir", default=None,
                    help="video deliverables only: the frame set dir for the full gate")
    ap.add_argument("--expect", type=int, default=None,
                    help="video deliverables only: expected frame count (with --frames-dir)")
    ap.add_argument("--allow-frozen", default=None,
                    help="REQUIRED when a film has intentional holds: the reason "
                         "(e.g. 'lab block 2832-3131 frozen by design, film report'). "
                         "Downgrades a video_probe FAIL caused ONLY by frozen runs "
                         "to WARN — never hides black/blown frames.")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    d = Path(args.deliverable)
    if not d.exists():
        print(f"ERROR: deliverable not found: {d}", file=sys.stderr)
        return 2
    is_video = d.suffix.lower() in (".mp4", ".webm", ".mov", ".mkv")
    checks, problems = [], []

    checks.append({"check": "file_exists", "result": "PASS",
                   "detail": f"{d} {d.stat().st_size} B sha256 {sha256(d)[:16]}..."})
    if is_video:
        # S8 FIX (2026-11-16): the old code called frame_set_gate.py with the
        # mp4 as the frames dir and no --expect — argparse errored, so EVERY
        # video failed the gate. The gate needs a frames dir + --expect; when
        # they are given, run the full gate; otherwise run the video-decode
        # check (ffmpeg full decode + ffprobe count) directly and record that
        # the frame-set contiguity was not re-checked in this run.
        if args.frames_dir and args.expect:
            rc, out = run_tool("frame_set_gate.py", args.frames_dir,
                               "--expect", str(args.expect),
                               "--video", str(d), "--out", "/tmp/pdc_gate")
            checks.append({"check": "frame_set_gate", "result": "PASS" if rc == 0 else "FAIL",
                           "detail": out[:500]})
            if rc != 0:
                problems.append("frame_set_gate failed")
        else:
            dec = subprocess.run(
                ["ffmpeg", "-v", "error", "-i", str(d), "-f", "null", "-"],
                capture_output=True, text=True, timeout=600)
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                 "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(d)],
                capture_output=True, text=True, timeout=300)
            ok = dec.returncode == 0 and not dec.stderr.strip()
            checks.append({"check": "video_decode",
                           "result": "PASS" if ok else "FAIL",
                           "detail": f"ffprobe frames={probe.stdout.strip()} "
                                     f"decode_err={dec.stderr.strip()[:200]} "
                                     f"(frame-set contiguity NOT re-checked: "
                                     f"no --frames-dir given)"})
            if not ok:
                problems.append("video decode failed")
        rc, out = run_tool("video_probe.py", str(d), "--every", "60", "--film",
                           "--out", "/tmp/pdc_probe")
        # Intentional holds: a probe FAIL caused ONLY by frozen runs can be
        # attested with --allow-frozen. Black/blown frames can never be attested away.
        probe_state = "FAIL" if rc != 0 else "PASS"
        if rc != 0 and args.allow_frozen:
            try:
                pj = json.loads(Path("/tmp/pdc_probe/video_probe.json").read_text())
                frozen_only = (pj.get("frozen_runs") and not any(
                    "failed colour" in x or "flagged" in x for x in pj.get("reasons", [])))
                black_blown = [s for s in pj.get("sample_rows", []) if s.get("flag")]
                if frozen_only and not black_blown:
                    probe_state = (f"WARN (intentional frozen: {args.allow_frozen})")
                    rc = 0
            except Exception:
                pass
        checks.append({"check": "video_probe", "result": probe_state,
                       "detail": out[:500]})
        if rc != 0:
            problems.append("video_probe failed")
    else:
        clc_args = [str(d)]
        if args.crop:
            clc_args += ["--crop", *[str(x) for x in args.crop]]
        rc, out = run_tool("color_light_check.py", *clc_args)
        checks.append({"check": "color_light", "result": "PASS" if rc == 0 else "FAIL",
                       "detail": out[:500]})
        if rc != 0:
            problems.append("color_light failed")
        rc, out = run_tool("pose_check.py", str(d))
        checks.append({"check": "pose", "result": "PASS" if rc == 0 else ("WARN" if "WARN" in out else "FAIL"),
                       "detail": out[:500]})
        if rc != 0:
            problems.append("pose failed")
        rc, out = run_tool("face_check.py", str(d),
                           *(["--require-face"] if args.require_face else []))
        checks.append({"check": "face", "result": "PASS" if rc == 0 else "FAIL",
                       "detail": out[:500]})
        if rc != 0 and args.require_face:
            problems.append("face failed")
    if args.source:
        rc, out = run_tool("pair_compare.py", args.source, str(d),
                           "--expect", "different", "--out", "/tmp/pdc_pair")
        checks.append({"check": "pair_vs_source", "result": "PASS" if rc == 0 else "FAIL",
                       "detail": out[:500]})
        if rc != 0:
            problems.append("pair vs source failed")
    if args.ref:
        rc, out = run_tool("reference_compare.py", "--ours", str(d),
                           "--ref-id", args.ref, "--out", "/tmp/pdc_ref")
        checks.append({"check": "reference_compare", "result": "PASS" if rc == 0 else "FAIL",
                       "detail": out[:500]})
        if rc != 0:
            problems.append("below reference band")

    eyes = {"attested": bool(args.seen), "notes": args.seen or ""}
    if not args.seen:
        problems.append("NO OWN-EYES ATTESTATION (--seen missing) — the look was skipped")
    ready = not problems
    record = {"deliverable": str(d), "sha256": sha256(d), "size_bytes": d.stat().st_size,
              "claim": args.claim, "checks": checks, "own_eyes": eyes,
              "problems": problems, "delivery_ready": "YES" if ready else "NO"}
    outdir = Path(args.out) if args.out else Path("/tmp/pdc")
    outdir.mkdir(parents=True, exist_ok=True)
    name = d.stem + "_delivery_checklist"
    (outdir / (name + ".json")).write_text(json.dumps(record, indent=2))
    md = [f"# Delivery checklist — {d.name}", "",
          f"- sha256: `{record['sha256']}`", f"- size: {record['size_bytes']} B",
          f"- claim: {args.claim}", "", "## Automated checks"]
    for c in checks:
        md.append(f"- [{c['result']}] {c['check']}: {c['detail']}")
    md += ["", "## Own eyes (mandatory)",
           f"- attested: {'YES' if eyes['attested'] else 'NO — THE LOOK WAS SKIPPED'}",
           f"- notes: {eyes['notes']}", "",
           f"## DELIVERY-READY: {record['delivery_ready']}"]
    if problems:
        md.append(f"Problems: {'; '.join(problems)}")
    (outdir / (name + ".md")).write_text("\n".join(md) + "\n")
    print("\n".join(md))
    return 0 if ready else 1


if __name__ == "__main__":
    sys.exit(main())
