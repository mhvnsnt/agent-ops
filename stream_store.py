#!/usr/bin/env python3
"""stream_store — stream a directory as tar into 100MB Drive chunks without
writing the full tar to disk (avoids disk spike at high usage).
Usage: stream_store.py <dir> --name <name> [--delete-local]
Replicates ~/workspace/tools/fetch/store manifest schema for chunked uploads.
"""
import json, os, sys, subprocess, datetime, shutil

MANIFEST = os.path.expanduser("~/workspace/agent-ops/STORAGE-MANIFEST.json")
WORKSPACE = os.path.expanduser("~/workspace")
STAGE = os.path.expanduser("~/workspace/agent-ops/.store-staging")
CHUNK = 100 * 1024 * 1024


def load_manifest():
    return json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {"items": {}, "updated_at": None}


def save_manifest(m):
    m["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(m, open(MANIFEST, "w"), indent=1)


def drive_upload(local, remote_name):
    for attempt in range(3):
        r = subprocess.run(
            ["hatch_gws_cli", "drive", "+upload", local, "--name", remote_name],
            capture_output=True, text=True, timeout=1200)
        if r.returncode == 0:
            try:
                data = json.loads(r.stdout)
                if isinstance(data, dict) and "id" in data:
                    return data["id"]
            except Exception:
                pass
            for line in reversed(r.stdout.strip().split("\n")):
                if line.strip():
                    return line.strip()
        print(f"  chunk upload attempt {attempt+1} failed", flush=True)
    return None


def main():
    args = sys.argv[1:]
    path = os.path.abspath(os.path.expanduser(args[0]))
    name = None
    delete_local = False
    i = 1
    while i < len(args):
        if args[i] == "--name" and i + 1 < len(args):
            name = args[i + 1]; i += 2
        elif args[i] == "--delete-local":
            delete_local = True; i += 1
        else:
            i += 1
    if not name or not os.path.isdir(path):
        print("need <dir> --name <name>"); sys.exit(1)
    os.makedirs(STAGE, exist_ok=True)
    progress_file = os.path.join(STAGE, f".{name}.progress.json")
    parts = []
    start_idx = 0
    if os.path.exists(progress_file):
        try:
            prog = json.load(open(progress_file))
            parts = prog.get("drive_ids", [])
            start_idx = len(parts)
            print(f"Resuming from chunk {start_idx}", flush=True)
        except Exception:
            pass

    parent = os.path.dirname(path)
    base = os.path.basename(path)
    tar = subprocess.Popen(["tar", "-cf", "-", "-C", parent, base],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    # skip already-uploaded bytes on resume
    to_skip = start_idx * CHUNK
    while to_skip > 0:
        data = tar.stdout.read(min(to_skip, 8 * 1024 * 1024))
        if not data:
            break
        to_skip -= len(data)

    idx = start_idx
    total = 0
    while True:
        data = tar.stdout.read(CHUNK)
        if not data:
            break
        part_path = os.path.join(STAGE, f".stream_{name}.part_{idx:03d}")
        open(part_path, "wb").write(data)
        fid = drive_upload(part_path, f"{name}.part_{idx:03d}")
        os.remove(part_path)
        if not fid:
            json.dump({"drive_ids": parts}, open(progress_file, "w"))
            print(f"Chunk {idx} failed — progress saved.", flush=True)
            tar.kill(); sys.exit(1)
        parts.append(fid)
        total += len(data)
        json.dump({"drive_ids": parts}, open(progress_file, "w"))
        idx += 1
        print(f"  chunk {idx} ok ({total/1e6:.0f}MB)", flush=True)
    tar.wait()
    if os.path.exists(progress_file):
        os.remove(progress_file)

    m = load_manifest()
    rel = os.path.relpath(path, WORKSPACE)
    m["items"][name] = {
        "type": "drive", "description": rel, "restore_path": rel + ".tar",
        "size": f"{total/1e6:.1f}MB", "bytes": total,
        "stored_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "chunked": True, "drive_ids": parts,
    }
    save_manifest(m)
    print(f"Stored {name}: {len(parts)} chunks, manifest updated.", flush=True)
    if delete_local:
        m2 = load_manifest()
        if name in m2["items"]:
            shutil.rmtree(path)
            print(f"Local deleted: {path}", flush=True)


if __name__ == "__main__":
    main()
