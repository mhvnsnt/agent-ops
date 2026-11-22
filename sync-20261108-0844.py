#!/usr/bin/env python3
"""Overnight queue sync 2026-11-08T08:44Z: blobs -> tree -> commit -> branch -> PR."""
import base64, hashlib, json, subprocess, sys

REPO = "mhvnsnt/agent-ops"
MAIN = "c58606226ce579b6d0772247be0bb1ea3e611a12"  # AO main tip verified this run (#635 sync merge)
FILES = ["MERGE-QUEUE.md", "overnight-handoff.md"]
BASE = "/home/hatch/workspace/agent-ops"
TMP = "/tmp/ao-sync-0844"

def gh(*args, input_file=None):
    cmd = ["gh", "api"] + list(args)
    if input_file:
        cmd += ["--input", input_file]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        print("GH-FAIL", " ".join(cmd[:6]), out.stderr.strip()[:300])
        sys.exit(1)
    return out.stdout.strip()

def git_blob_sha(path):
    data = open(path, "rb").read()
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    return h, base64.b64encode(data).decode()

import os
os.makedirs(TMP, exist_ok=True)

main_tree = gh(f"repos/{REPO}/git/commits/{MAIN}", "--jq", ".tree.sha")
print("main tree:", main_tree)

blob_shas = {}
for f in FILES:
    local_sha, b64 = git_blob_sha(f"{BASE}/{f}")
    pf = f"{TMP}/blob-{f}.json"
    json.dump({"content": b64, "encoding": "base64"}, open(pf, "w"))
    created = gh(f"repos/{REPO}/git/blobs", "--jq", ".sha", input_file=pf).strip().strip('"')
    print(f, "local", local_sha[:7], "created", created[:7],
          "MATCH" if created == local_sha else "MISMATCH")
    assert created == local_sha, f"blob mismatch for {f}"
    blob_shas[f] = created

tree_payload = {"base_tree": main_tree, "tree": [
    {"path": f, "mode": "100644", "type": "blob", "sha": blob_shas[f]} for f in FILES]}
tf = f"{TMP}/tree.json"
json.dump(tree_payload, open(tf, "w"))
tree_sha = gh(f"repos/{REPO}/git/trees", "--jq", ".sha", input_file=tf).strip().strip('"')
print("new tree:", tree_sha)

commit_payload = {
    "message": "Overnight pipeline 2026-11-08T08:44Z: queue sync — 0 merged, 0 landed by other lanes, queue 40 open",
    "tree": tree_sha, "parents": [MAIN]}
cf = f"{TMP}/commit.json"
json.dump(commit_payload, open(cf, "w"))
commit_sha = gh(f"repos/{REPO}/git/commits", "--jq", ".sha", input_file=cf).strip().strip('"')
print("new commit:", commit_sha)

ref_out = subprocess.run(["gh", "api", f"repos/{REPO}/git/ref/heads/merge-queue-sync",
                          "--jq", ".object.sha"], capture_output=True, text=True)
if ref_out.returncode == 0:
    cur = ref_out.stdout.strip()
    print("branch currently at:", cur)
    cmp_status = gh(f"repos/{REPO}/compare/{cur}...{commit_sha}", "--jq", ".status")
    print("compare status:", cmp_status)
    assert cmp_status == "ahead", f"not fast-forward ({cmp_status}); refusing to move branch"
    subprocess.run(["gh", "api", f"repos/{REPO}/git/refs/heads/merge-queue-sync",
                    "-X", "PATCH", "-f", f"sha={commit_sha}", "--jq", ".object.sha"],
                   check=True, capture_output=True, text=True)
    print("branch merge-queue-sync updated to", commit_sha)
else:
    subprocess.run(["gh", "api", f"repos/{REPO}/git/refs", "-f", "ref=refs/heads/merge-queue-sync",
                    "-f", f"sha={commit_sha}", "--jq", ".object.sha"],
                   check=True, capture_output=True, text=True)
    print("branch merge-queue-sync created at", commit_sha)
print("COMMIT", commit_sha)
