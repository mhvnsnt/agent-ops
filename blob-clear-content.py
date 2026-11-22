#!/usr/bin/env python3
"""Content-hash clear (v2, 2026-11-08): delete a file iff its git blob sha exists
ANYWHERE in the fetched GitHub trees (path-independent). Records a GitHub path
holding the same bytes so the file can be pulled back. Never touches .git dirs.
Fixes over the /tmp v1 (2026-11-08, died to /tmp ENOSPC + /tmp wipe):
 - output list goes to ~/workspace/agent-ops/ (home disk, durable), NOT /tmp
 - line-buffered output (buffering=1): every record lands before the next delete,
   so a crash can never lose buffered deletion records
 - out path is per-run: pass it as the last arg, or it defaults to
   ~/workspace/agent-ops/deleted-blob-clear-content-<yyyymmdd-hhmm>.txt
Usage: blob-clear-content.py <target-dir> <tree1.tsv> [tree2.tsv ...] [out-path]
NOTE: empty (0-byte) files match GitHub's empty blob and delete first; they
free 0 bytes. That is correct behaviour, not a bug — just expect it."""
import hashlib, os, sys, datetime

def blob_sha(path):
    h = hashlib.sha1()
    size = os.path.getsize(path)
    h.update(b"blob %d\0" % size)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def main():
    args = sys.argv[1:]
    out_path = None
    if args and args[-1].endswith(".txt"):
        out_path = args.pop()
    if not out_path:
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        out_path = os.path.expanduser(
            f"~/workspace/agent-ops/deleted-blob-clear-content-{stamp}.txt")
    target = args[0]
    tree_files = args[1:]
    sha_to_paths = {}
    for tf in tree_files:
        n = 0
        with open(tf) as f:
            for line in f:
                line = line.rstrip("\n")
                if not line:
                    continue
                p, s = line.split("\t", 1)
                sha_to_paths.setdefault(s, []).append(p)
                n += 1
        print(f"tree {tf}: {n} blobs, {len(sha_to_paths)} unique shas", flush=True)
    deleted, kept, skipped = 0, 0, 0
    freed = 0
    out = open(out_path, "a", buffering=1)
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, target)
            if not os.path.isfile(full) or os.path.islink(full):
                skipped += 1
                continue
            try:
                sha = blob_sha(full)
            except OSError as e:
                print(f"READ-FAIL {rel}: {e}", flush=True)
                kept += 1
                continue
            gh = sha_to_paths.get(sha)
            if gh:
                size = os.path.getsize(full)
                try:
                    os.remove(full)
                except OSError as e:
                    print(f"DEL-FAIL {rel}: {e}", flush=True)
                    kept += 1
                    continue
                out.write(f"{size}\t{target}\t{rel}\t{gh[0]}\n")
                deleted += 1
                freed += size
            else:
                kept += 1
    out.close()
    print(f"DELETED {deleted} files, freed {freed} bytes ({freed/1048576:.1f} MiB)", flush=True)
    print(f"KEPT {kept} files (content not on GitHub), SKIPPED {skipped}", flush=True)
    print(f"records: {out_path}", flush=True)

main()
