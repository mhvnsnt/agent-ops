#!/usr/bin/env python3
"""Asset validation gates for game repos — stdlib only, no dependencies.

Fails the PR (exit 1) on:
  - files over per-extension size caps (catches accidental 2GB .blend commits)
  - banned extensions / paths (sources or secrets where they don't belong)
  - GLB files that don't parse (bad magic, bad JSON chunk, wrong version)
  - duplicate filenames differing only by case (breaks Windows/macOS checkouts)

Warns (exit 0) on:
  - textures over the dimension cap (reads PNG/JPEG headers only, no decode)

Usage: python3 scripts/asset_gates.py [root]  (default: repo root)
"""
import json
import os
import struct
import sys

SIZE_CAPS = {
    ".blend": 500 * 1024 * 1024,
    ".glb": 200 * 1024 * 1024,
    ".fbx": 200 * 1024 * 1024,
    ".png": 50 * 1024 * 1024,
    ".wav": 200 * 1024 * 1024,
    ".mp4": 500 * 1024 * 1024,
}
BANNED_EXTS = {".psd", ".pem", ".key", ".pyc", ".DS_Store"}
BANNED_PATH_PARTS = {".git", "node_modules", "__pycache__"}
TEXTURE_DIM_CAP = 4096  # warn above this

errors, warnings = [], []


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read(1 << 20)
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker == 0xD9:
            break
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg_len
    return None


def check_glb(path):
    with open(path, "rb") as f:
        head = f.read(20)
    if len(head) < 12 or head[:4] != b"glTF":
        return "bad magic (not a GLB)"
    version = struct.unpack("<I", head[4:8])[0]
    if version != 2:
        return f"unsupported glTF version {version}"
    total = struct.unpack("<I", head[8:12])[0]
    if os.path.getsize(path) < total:
        return "truncated (file smaller than header length)"
    with open(path, "rb") as f:
        f.seek(12)
        chunk = f.read(8)
    if len(chunk) < 8:
        return "missing JSON chunk header"
    clen, ctype = struct.unpack("<II", chunk)
    if ctype != 0x4E4F534A:
        return "first chunk is not JSON"
    with open(path, "rb") as f:
        f.seek(20)
        try:
            json.loads(f.read(clen).decode("utf-8"))
        except Exception as e:
            return f"JSON chunk does not parse: {e}"
    return None


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    seen = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in BANNED_PATH_PARTS]
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root)
            ext = os.path.splitext(fn)[1].lower()

            if ext in BANNED_EXTS:
                errors.append(f"banned extension: {rel}")
            cap = SIZE_CAPS.get(ext)
            if cap:
                size = os.path.getsize(path)
                if size > cap:
                    errors.append(f"over size cap ({size} > {cap}): {rel}")

            key = rel.lower()
            if key in seen and seen[key] != rel:
                errors.append(f"case-colliding duplicate: {rel} vs {seen[key]}")
            seen.setdefault(key, rel)

            if ext == ".glb":
                problem = check_glb(path)
                if problem:
                    errors.append(f"GLB invalid ({problem}): {rel}")
            elif ext in (".png", ".jpg", ".jpeg"):
                dims = png_size(path) if ext == ".png" else jpeg_size(path)
                if dims and max(dims) > TEXTURE_DIM_CAP:
                    warnings.append(f"texture > {TEXTURE_DIM_CAP}px: {rel} {dims[0]}x{dims[1]}")

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"FAIL: {e}")
    print(f"asset_gates: {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
