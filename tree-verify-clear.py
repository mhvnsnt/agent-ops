#!/usr/bin/env python3
"""tree-verify-clear.py — ONE-STORE RULE verify-then-clear for plain build-output
trees (NOT git checkouts) against GitHub repo trees.

Method (per disk-cleanup-log 2026-11-06 11:10 pass): fetch the repo's recursive
git trees for given commits via `gh api`, hash every local file with
`git hash-object` (batch mode), and delete ONLY files whose local blob SHA
equals the blob SHA at the same repo-relative path on GitHub (any listed
commit). Files that differ (lane-modified) or are absent from GitHub STAY.

Safety:
  - Refuses if <local_dir>/.git exists (it's a checkout — use git, not this).
  - Refuses if any file was modified within --min-age-hours (default 6).
  - Skips symlinks (reported, never deleted, never followed).
  - Deletes regular files only, then prunes empty dirs (never the root).
  - Writes verified / mismatch / not-on-github lists under agent-ops/tree-verify/.

Usage:
  tree-verify-clear.py <local_dir> <owner/repo> <commit...> [--dry-run]
                       [--repo-prefix <path/>] [--min-age-hours N] [--label NAME]
"""
import json
import os
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
OUTDIR = os.path.join(HOME, "workspace", "agent-ops", "tree-verify")
# Local western-heart clone used ONLY as a read-only object store for ls-tree.
CLONE = os.path.join(HOME, "workspace", "_roster100-s8-20261105", "tree")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    repo_prefix = ""
    min_age_hours = 6.0
    label = None
    rest = []
    i = 0
    while i < len(args):
        if args[i] == "--repo-prefix":
            repo_prefix = args[i + 1].rstrip("/") + "/"
            i += 2
        elif args[i] == "--min-age-hours":
            min_age_hours = float(args[i + 1])
            i += 2
        elif args[i] == "--label":
            label = args[i + 1]
            i += 2
        else:
            rest.append(args[i])
            i += 1
    if len(rest) < 3:
        print("usage: tree-verify-clear.py <local_dir> <owner/repo> <commit...> "
              "[--dry-run] [--repo-prefix P] [--min-age-hours N] [--label NAME]")
        return 2
    local_dir, repo = rest[0], rest[1]
    commits = rest[2:]
    local_dir = os.path.abspath(os.path.expanduser(local_dir))
    label = label or os.path.basename(local_dir.rstrip("/"))
    if not os.path.isdir(local_dir):
        print(f"ABORT: not a dir: {local_dir}")
        return 2
    if os.path.exists(os.path.join(local_dir, ".git")):
        print(f"ABORT: {local_dir} contains .git — it is a checkout, not a plain "
              "build-output tree. Use git methods, not this script.")
        return 2

    # Freshness guard.
    now = time.time()
    newest = 0.0
    newest_path = ""
    for root, dirs, files in os.walk(local_dir):
        for f in files:
            p = os.path.join(root, f)
            try:
                m = os.lstat(p).st_mtime
            except OSError:
                continue
            if m > newest:
                newest, newest_path = m, p
    age_h = (now - newest) / 3600.0
    print(f"newest file: {newest_path} age {age_h:.1f}h")
    if age_h < min_age_hours:
        print(f"ABORT: tree has files newer than {min_age_hours}h — still active.")
        return 2

    # Fetch repo trees from a LOCAL clone (the GitHub recursive-tree API
    # truncates at ~57k blobs for this repo — own-eyes grade needs ls-tree).
    # <clone> must already contain the listed commits (fetch first).
    tree = {}  # repo path -> set of blob shas
    for c in commits:
        r = run(["git", "-C", CLONE, "ls-tree", "-r", c])
        if r.returncode != 0:
            print(f"ABORT: git ls-tree failed for {c}: {r.stderr.strip()}")
            return 2
        n = 0
        for line in r.stdout.splitlines():
            # "<mode> blob <sha>\t<path>"
            try:
                meta, path = line.split("\t", 1)
                parts = meta.split()
                if len(parts) == 3 and parts[1] == "blob":
                    tree.setdefault(path, set()).add(parts[2])
                    n += 1
            except ValueError:
                continue
        print(f"tree {c[:12]}: {n} blobs")

    # Walk local files.
    rels = []
    symlinks = []
    for root, dirs, files in os.walk(local_dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            p = os.path.join(root, f)
            if os.path.islink(p):
                symlinks.append(os.path.relpath(p, local_dir))
                continue
            rels.append(os.path.relpath(p, local_dir))
    print(f"local files: {len(rels)} (symlinks skipped: {len(symlinks)})")

    # Batch hash.
    hashes = {}
    if rels:
        inp = "\n".join(os.path.join(local_dir, r) for r in rels) + "\n"
        r = run(["git", "hash-object", "--stdin-paths"], input=inp)
        if r.returncode != 0:
            print(f"ABORT: git hash-object failed: {r.stderr.strip()[:500]}")
            return 2
        lines = r.stdout.splitlines()
        if len(lines) != len(rels):
            print(f"ABORT: hash count {len(lines)} != file count {len(rels)}")
            return 2
        for rel, h in zip(rels, lines):
            hashes[rel] = h.strip()

    verified, mismatch, missing = [], [], []
    vbytes = 0
    for rel in rels:
        repo_path = repo_prefix + rel.replace(os.sep, "/")
        shas = tree.get(repo_path)
        if shas is None:
            missing.append(rel)
        elif hashes[rel] in shas:
            verified.append(rel)
            vbytes += os.path.getsize(os.path.join(local_dir, rel))
        else:
            mismatch.append(rel)

    os.makedirs(OUTDIR, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M")
    for name, lst in (("verified", verified), ("mismatch", mismatch),
                      ("not-on-github", missing), ("symlink", symlinks)):
        with open(os.path.join(OUTDIR, f"{label}-{stamp}-{name}.txt"), "w") as fh:
            fh.write("\n".join(lst) + ("\n" if lst else ""))
    print(f"VERIFIED: {len(verified)} files, {vbytes/2**30:.2f} GiB")
    print(f"MISMATCH (on GitHub, different hash — lane-modified, STAYS): "
          f"{len(mismatch)}")
    print(f"NOT-ON-GITHUB (STAYS): {len(missing)}")
    print(f"SYMLINKS (untouched): {len(symlinks)}")
    print(f"lists: {OUTDIR}/{label}-{stamp}-*.txt")

    if dry:
        print("DRY RUN — nothing deleted.")
        return 0
    deleted, dbytes = 0, 0
    for rel in verified:
        p = os.path.join(local_dir, rel)
        try:
            sz = os.path.getsize(p)
            os.unlink(p)
            deleted += 1
            dbytes += sz
        except OSError as e:
            print(f"WARN: could not delete {rel}: {e}")
    # Prune empty dirs bottom-up (never the root).
    for root, dirs, files in os.walk(local_dir, topdown=False):
        if root == local_dir:
            continue
        try:
            os.rmdir(root)
        except OSError:
            pass
    print(f"DELETED: {deleted} files, {dbytes/2**30:.2f} GiB nominal")
    return 0


if __name__ == "__main__":
    sys.exit(main())
