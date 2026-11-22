#!/usr/bin/env python3
"""Transplant the 15 main-missing files from fixes/audit-pipeline-kaggle-20261017
onto a fresh branch off CURRENT main, referencing the branch's own blob SHAs
(byte-exact, no re-upload). docs/research/EXPANSION-4.md is deliberately
EXCLUDED: it exists on main with different content and needs a
keep-both-sides reconciliation, queued separately."""
import json, subprocess, sys

REPO = "mhvnsnt/cape-jones"
SRC = "fixes/audit-pipeline-kaggle-20261017"
NEW = "land/audit-pipeline-kaggle-20261017"

FILES = [
    "AUDIT-FIXES.md",
    "docs/KAGGLE-FIXES.md",
    "docs/RESEARCH-INDEX-PATCH-NOTES.md",
    "docs/STALE-DOC-CANDIDATES.md",
    "docs/TOONCRAFTER-PATCH-V5.md",
    "docs/WIRING-STUBS.md",
    "production/kaggle/tooncrafter/fp16_patch_cell_v5.py",
    "production/kaggle/tooncrafter/kernel-metadata.json",
    "production/kaggle/tooncrafter/re_push_tooncrafter.sh",
    "production/pipeline/example_manifest.json",
    "production/pipeline/ingest_queue.py",
    "production/pipeline/instance_animator_wrapper.py",
    "production/pipeline/ldf_vfi_wrapper.py",
    "production/pipeline/pupil_gag.py",
    "production/pipeline/scene_assembler.py",
]

def gh(args, inp=None):
    r = subprocess.run(["gh", "api"] + args, input=inp, capture_output=True)
    if r.returncode != 0:
        sys.exit(f"FAIL {' '.join(args)}: {r.stderr.decode()[:300]}")
    return json.loads(r.stdout.decode())

head = gh([f"repos/{REPO}/git/ref/heads/main"])["object"]["sha"]
base_tree = gh([f"repos/{REPO}/git/commits/{head}"])["tree"]["sha"]
print("main head:", head)

# harvest blob sha + mode for each file from the SOURCE branch trees
src_head = gh([f"repos/{REPO}/git/ref/heads/{SRC}"])["object"]["sha"]
src_tree = gh([f"repos/{REPO}/git/commits/{src_head}"])["tree"]["sha"]

def tree_entries(tree_sha):
    return {e["path"]: e for e in gh([f"repos/{REPO}/git/trees/{tree_sha}"])["tree"]}

def find(tree_sha, parts):
    e = tree_entries(tree_sha)[parts[0]]
    if len(parts) == 1:
        return e
    return find(e["sha"], parts[1:])

entries = []
for path in FILES:
    e = find(src_tree, path.split("/"))
    assert e["type"] == "blob", (path, e["type"])
    entries.append({"path": path, "mode": e["mode"], "type": "blob", "sha": e["sha"]})
    print("entry:", path, e["mode"], e["sha"][:10])

tree = gh([f"repos/{REPO}/git/trees", "--method", "POST", "--input", "-"],
          inp=json.dumps({"base_tree": base_tree, "tree": entries}).encode())
commit = gh([f"repos/{REPO}/git/commits", "--method", "POST", "--input", "-"],
            inp=json.dumps({
                "message": "Land stranded 2026-10-17 audit pipeline files (15 files missing on main)",
                "tree": tree["sha"], "parents": [head]}).encode())
gh([f"repos/{REPO}/git/refs", "--method", "POST", "--input", "-"],
   inp=json.dumps({"ref": f"refs/heads/{NEW}", "sha": commit["sha"]}).encode())
print("branch:", NEW, "commit:", commit["sha"], "files:", len(entries))
