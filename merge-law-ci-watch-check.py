#!/usr/bin/env python3
"""Check merge-law-ci-watch PRs: state + mergeStateStatus."""
import json
import subprocess
import sys
import time

PR_FILE = "/home/hatch/workspace/agent-ops/merge-law-ci-watch-prs.tsv"
OUT_FILE = "/home/hatch/workspace/agent-ops/merge-law-ci-watch-results.jsonl"

def check(repo, num):
    cmd = ["gh", "pr", "view", str(num), "--repo", repo,
           "--json", "mergeStateStatus,state,url", "--jq",
           '{"state":.state,"ms":.mergeStateStatus,"url":.url}']
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        return {"repo": repo, "num": num, "error": (p.stderr or p.stdout).strip()[:200]}
    try:
        d = json.loads(p.stdout)
    except Exception as e:
        return {"repo": repo, "num": num, "error": f"bad json: {p.stdout[:100]}"}
    d.update({"repo": repo, "num": num})
    return d

results = []
with open(PR_FILE) as f:
    lines = [l.strip() for l in f if l.strip()]

total = len(lines)
for i, line in enumerate(lines, 1):
    repo, num = line.split(",")
    r = check(repo, num)
    results.append(r)
    state = r.get("state", "?")
    ms = r.get("ms", r.get("error", "?")[:40])
    print(f"[{i}/{total}] {repo}#{num}: {state} {ms}", flush=True)
    time.sleep(0.15)

with open(OUT_FILE, "w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")

open_cnt = sum(1 for r in results if r.get("state") == "OPEN")
clean_cnt = sum(1 for r in results if r.get("state") == "OPEN" and r.get("ms") == "CLEAN")
merged_cnt = sum(1 for r in results if r.get("state") == "MERGED")
closed_cnt = sum(1 for r in results if r.get("state") == "CLOSED")
err_cnt = sum(1 for r in results if "error" in r)
print(f"\nSUMMARY: total={total} open={open_cnt} open_clean={clean_cnt} merged={merged_cnt} closed={closed_cnt} errors={err_cnt}")
