#!/usr/bin/env python3
"""stream_chunk_upload.py — read stdin in fixed chunks, upload each to a gh
release with download-back sha256 verification, delete temp immediately.

Sequential, one chunk on disk at a time. Safe to run at high disk usage.
Exits 0 only when every chunk is digest-verified; digests written to
--digest-file (one line per chunk: "<name> <sha256> <bytes>").

Usage:
  tar cf - <dir> | stream_chunk_upload.py --tag TAG --repo OWNER/REPO \\
      --prefix NAME --digest-file DIGESTS
  stream_chunk_upload.py --tag TAG --repo OWNER/REPO --prefix NAME \\
      --digest-file DIGESTS < bigfile.mp4
"""
import sys, os, subprocess, hashlib, datetime, argparse

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', required=True)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--prefix', required=True)
    ap.add_argument('--chunk-bytes', type=int, default=200 * 1024 * 1024)
    ap.add_argument('--digest-file', required=True)
    ap.add_argument('--stage-dir',
                    default=os.path.expanduser('~/workspace/agent-ops/.store-staging'))
    ap.add_argument('--retries', type=int, default=3)
    args = ap.parse_args()
    os.makedirs(args.stage_dir, exist_ok=True)

    def log(msg):
        print(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()} {msg}",
              flush=True)

    total = 0
    idx = 0
    digests = []
    while True:
        data = sys.stdin.buffer.read(args.chunk_bytes)
        if not data:
            break
        name = f"{args.prefix}{idx:02d}"
        tmp = os.path.join(args.stage_dir, name)  # asset name == basename
        with open(tmp, 'wb') as f:
            f.write(data)
        local_dig = hashlib.sha256(data).hexdigest()
        sz = len(data)
        ok = False
        for attempt in range(1, args.retries + 1):
            r = sh(['gh', 'release', 'upload', args.tag, tmp,
                    '--repo', args.repo, '--clobber'])
            if r.returncode != 0:
                log(f"{name} upload attempt {attempt} FAILED: "
                    f"{(r.stderr or '')[-300:]}")
                continue
            vtmp = tmp + '.verify'
            r = sh(['gh', 'release', 'download', args.tag, '--repo', args.repo,
                    '-p', name, '--clobber', '-O', vtmp])
            if r.returncode != 0:
                log(f"{name} download-back attempt {attempt} FAILED: "
                    f"{(r.stderr or '')[-300:]}")
                continue
            with open(vtmp, 'rb') as f:
                remote_dig = hashlib.sha256(f.read()).hexdigest()
            os.remove(vtmp)
            if remote_dig == local_dig:
                ok = True
                break
            log(f"{name} DIGEST MISMATCH attempt {attempt}: "
                f"local={local_dig[:16]} remote={remote_dig[:16]}")
        os.remove(tmp)
        if not ok:
            log(f"{name} FAILED after {args.retries} attempts — ABORTING")
            sys.exit(2)
        digests.append((name, local_dig, sz))
        total += sz
        log(f"{name} DIGEST-VERIFIED {local_dig[:16]} {sz}B (chunk {idx})")
        idx += 1
    with open(args.digest_file, 'w') as f:
        for name, dig, sz in digests:
            f.write(f"{name} {dig} {sz}\n")
    log(f"DONE: {idx} chunks, {total} bytes total, digests -> {args.digest_file}")

if __name__ == '__main__':
    main()
