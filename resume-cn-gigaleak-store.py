#!/usr/bin/env python3
"""SUPERSEDED 2026-10-14 ~03:15 EDT by disk-space-guardian 03:01 run — DO NOT RUN.
Drive had only ~2.86GB free of 15GB quota; remaining 46 chunks (4.7GB) could not
fit. The tail (bytes 5242880000..10160814079) was instead uploaded as 3 assets
to GitHub release cn-gigaleak-work-automigrate-2026-10-14 on mhvnsnt/google-drive-repo.
See STORAGE-MANIFEST.json entry cn-gigaleak-work-automigrate-2026-10-14 (mixed
Drive 50 chunks + GitHub 3 assets) and disk-cleanup-log.md. Original docstring:

Resume interrupted store of cn-gigaleak-work-automigrate-2026-10-14.

The 2026-10-14 00:20 EDT guardian run tarred the gigaleak work dir into
.store-staging/store_cn-gigaleak-work-automigrate-2026-10-14.tar (9.5G),
uploaded chunks part_000..part_006, then died. The source dir is gone from
disk (lane cleaned it) — the staging tar is the ONLY copy. This script
uploads the remaining chunks, verifies on Drive, updates the manifest,
and only then deletes staging.
"""
import json, os, sys, subprocess, datetime, time

STAGE = os.path.expanduser("~/workspace/agent-ops/.store-staging")
NAME = "cn-gigaleak-work-automigrate-2026-10-14"
TAR = os.path.join(STAGE, f"store_{NAME}.tar")
PROG = os.path.join(STAGE, f".{NAME}.progress.json")
CHUNK = 100 * 1024 * 1024
MANIFEST = os.path.expanduser("~/workspace/agent-ops/STORAGE-MANIFEST.json")
LOG = os.path.expanduser("~/workspace/agent-ops/disk-cleanup-log.md")

def log(msg):
    line = f"{datetime.datetime.now().isoformat()} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def drive_upload(local, remote_name):
    r = subprocess.run(
        ["hatch_gws_cli", "drive", "+upload", local, "--name", remote_name],
        capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        return None
    try:
        data = json.loads(r.stdout)
        if isinstance(data, dict) and "id" in data:
            return data["id"]
    except Exception:
        pass
    for line in reversed(r.stdout.strip().split("\n")):
        if line.strip():
            return line.strip()
    return None

def main():
    size = os.path.getsize(TAR)
    nchunks = (size + CHUNK - 1) // CHUNK
    prog = json.load(open(PROG))
    parts = prog.get("drive_ids", [])
    start = len(parts)
    log(f"[resume] {NAME}: tar {size} bytes, {nchunks} chunks, resuming at chunk {start}")
    with open(TAR, "rb") as f:
        f.seek(start * CHUNK)
        for idx in range(start, nchunks):
            data = f.read(CHUNK)
            if not data:
                break
            part_path = f"{TAR}.part_{idx:03d}"
            with open(part_path, "wb") as pf:
                pf.write(data)
            fid = None
            for attempt in range(3):
                fid = drive_upload(part_path, f"{NAME}.part_{idx:03d}")
                if fid:
                    break
                log(f"[resume] chunk {idx} attempt {attempt+1} failed, retrying in 10s")
                time.sleep(10)
            try:
                os.remove(part_path)
            except OSError:
                pass
            if not fid:
                json.dump({"drive_ids": parts}, open(PROG, "w"))
                log(f"[resume] chunk {idx} FAILED after 3 attempts — progress saved, rerun to resume.")
                sys.exit(1)
            parts.append(fid)
            json.dump({"drive_ids": parts}, open(PROG, "w"))
            log(f"[resume] chunk {idx}/{nchunks-1} ok ({fid})")

    # verify on Drive before touching anything
    log("[resume] all chunks uploaded, verifying on Drive...")
    r = subprocess.run(
        ["hatch_gws_cli", "drive", "files", "list", "--params",
         json.dumps({"q": f"name contains '{NAME}'",
                     "fields": "files(id,name,size)", "pageSize": 200})],
        capture_output=True, text=True, timeout=120)
    files = json.loads(r.stdout).get("files", [])
    byname = {x["name"]: int(x["size"]) for x in files}
    ok = True
    for idx in range(nchunks):
        nm = f"{NAME}.part_{idx:03d}"
        want = CHUNK if idx < nchunks - 1 else size - (nchunks - 1) * CHUNK
        got = byname.get(nm)
        if got != want:
            log(f"[resume] VERIFY FAIL: {nm} want {want}, got {got}")
            ok = False
    if not ok or len(parts) != nchunks:
        log(f"[resume] verification failed — staging kept. parts={len(parts)} expected={nchunks}")
        sys.exit(2)
    log(f"[resume] verified {nchunks} chunks on Drive, sizes match.")

    m = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {"items": {}}
    m["items"][NAME] = {
        "type": "drive",
        "description": ("CN gigaleak work dir (w-fosters, ed-edd-n-eddy, etc.), "
                        "tarred 2026-10-14; source cleaned from disk by gigaleak lane, "
                        "staging tar was sole copy; upload resumed+completed by "
                        "disk-space-guardian. Tar root arcname: work/"),
        "restore_path": "cn-gigaleak-work.tar",
        "size": f"{size/1e6:.1f}MB",
        "bytes": size,
        "stored_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "chunked": True,
        "drive_ids": parts,
    }
    m["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(m, open(MANIFEST, "w"), indent=1)

    # only now delete staging
    os.remove(TAR)
    for fn in os.listdir(STAGE):
        if fn.startswith(f"store_{NAME}.tar.part_"):
            os.remove(os.path.join(STAGE, fn))
    os.remove(PROG)
    log(f"[resume] DONE — staging deleted, {size/1e9:.2f}GB freed. Manifest updated.")

if __name__ == "__main__":
    main()
