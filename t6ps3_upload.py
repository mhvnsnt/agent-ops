#!/usr/bin/env python3
"""
Chunk-upload TEKKEN.psarc (4.83GB) to GitHub release tekken6-ps3-full-v1.
Resumable: skips chunks already uploaded. One chunk at a time (disk-safe).
Run: python3 /home/hatch/workspace/agent-ops/t6ps3_upload.py
"""
import os, sys, subprocess, json

SRC = "/home/hatch/workspace/game-reverse-engineering/tekken6-ps3/iso/PS3_GAME/USRDIR/TEKKEN.psarc"
REPO = "mhvnsnt/western-heart"
RELEASE = "tekken6-ps3-full-v1"
CHUNK = 524288000  # 500MB
TMPDIR = "/home/hatch/workspace/agent-ops/staging-t6ps3"
STATE = "/home/hatch/workspace/agent-ops/checkpoints/t6ps3-upload-state.json"
LOG = "/home/hatch/workspace/agent-ops/disk-cleanup-log.md"

def split_suffix(i):
    return "part_" + chr(97 + i // 26) + chr(97 + i % 26)

def log(msg):
    print(msg, flush=True)
    with open(LOG, "a") as f:
        f.write(f"{msg}\n")

def gh(args):
    p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=1800)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

def get_uploaded():
    rc, out, _ = gh(["release", "view", RELEASE, "--repo", REPO, "--json", "assets",
                     "--jq", ".assets[] | \"\\(.name) \\(.size)\""])
    uploaded = {}
    if rc == 0:
        for line in out.splitlines():
            parts = line.rsplit(" ", 1)
            if len(parts) == 2:
                uploaded[parts[0]] = int(parts[1])
    return uploaded

def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"done": [], "total": 0}

def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, "w"), indent=2)

def main():
    fsize = os.path.getsize(SRC)
    nchunks = (fsize + CHUNK - 1) // CHUNK
    log(f"[t6ps3] File: {fsize} bytes, {nchunks} chunks of {CHUNK}")

    state = load_state()
    state["total"] = nchunks
    uploaded = get_uploaded()
    log(f"[t6ps3] Already on GitHub: {sorted(uploaded.keys())}")

    os.makedirs(TMPDIR, exist_ok=True)

    for i in range(nchunks):
        name = f"TEKKEN.psarc.{split_suffix(i)}"
        expected = min(CHUNK, fsize - i * CHUNK)
        if name in uploaded and uploaded[name] == expected:
            log(f"[t6ps3] Chunk {i+1}/{nchunks} ({name}) already uploaded, skipping")
            if name not in state["done"]:
                state["done"].append(name)
                save_state(state)
            continue

        chunk_path = os.path.join(TMPDIR, name)
        log(f"[t6ps3] Extracting chunk {i+1}/{nchunks} ({name})...")
        rc = subprocess.run(
            ["dd", f"if={SRC}", f"of={chunk_path}", f"bs={CHUNK}",
             f"skip={i}", "count=1", "status=none"],
            timeout=180).returncode
        if rc != 0:
            log(f"[t6ps3] ERROR extracting chunk {i+1}")
            sys.exit(1)

        csize = os.path.getsize(chunk_path)
        # Retry up to 3 times with backoff
        uploaded_ok = False
        for attempt in range(3):
            log(f"[t6ps3] Uploading {name} ({csize} bytes), attempt {attempt+1}/3...")
            rc, out, err = gh(["release", "upload", RELEASE, chunk_path,
                               "--repo", REPO, "--clobber"])
            if rc == 0:
                uploaded = get_uploaded()
                if name in uploaded and uploaded[name] == csize:
                    uploaded_ok = True
                    break
            log(f"[t6ps3] Attempt {attempt+1} failed: {err[:200]}")
            if attempt < 2:
                import time; time.sleep(30)
        if not uploaded_ok:
            log(f"[t6ps3] ERROR uploading {name} after 3 attempts, keeping chunk")
            sys.exit(1)

        # Verify (already done in retry loop)
        if uploaded_ok:
            log(f"[t6ps3] VERIFIED {name} ({csize} bytes)")
            os.remove(chunk_path)
            state["done"].append(name)
            save_state(state)
        else:
            log(f"[t6ps3] VERIFY FAILED for {name}, keeping chunk for retry")
            sys.exit(1)

    log(f"[t6ps3] ALL {nchunks} CHUNKS UPLOADED AND VERIFIED")
    manifest = "# TEKKEN.psarc split manifest\n# sha256: c98fb02602d58564ef4e80d386310cb3c48634566990a5050ef20ef2a4afd340\n"
    for i in range(nchunks):
        manifest += f"TEKKEN.psarc.{split_suffix(i)}\n"
    mp = os.path.join(TMPDIR, "TEKKEN.psarc.manifest.txt")
    open(mp, "w").write(manifest)
    gh(["release", "upload", RELEASE, mp, "--repo", REPO, "--clobber"])
    os.remove(mp)
    log("[t6ps3] Manifest uploaded, done")

if __name__ == "__main__":
    main()
