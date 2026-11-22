#!/usr/bin/env python3
"""merge-law-ci-watch run 2026-10-23 04:57 CDT: check body PRs, merge OPEN+CLEAN only."""
import json
import subprocess
import time

PR_FILE = "/home/hatch/workspace/agent-ops/pr-watch-body-2026-10-23.tsv"
OUT = "/home/hatch/workspace/agent-ops/merge-law-ci-watch-results-2026-10-23.jsonl"
REPORT = "/home/hatch/workspace/agent-ops/merge-law-ci-watch-2026-10-23.md"

def gh_view(repo, num):
    p = subprocess.run(
        ["gh", "pr", "view", num, "--repo", repo,
         "--json", "mergeStateStatus,state,title",
         "--jq", '{"state":.state,"ms":.mergeStateStatus,"title":.title}'],
        capture_output=True, text=True, timeout=90)
    if p.returncode != 0:
        return {"error": (p.stderr or p.stdout).strip()[:300]}
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"error": "bad json: " + p.stdout[:150]}

def gh_merge(repo, num):
    p = subprocess.run(
        ["gh", "pr", "merge", num, "--repo", repo, "--merge"],
        capture_output=True, text=True, timeout=180)
    return p.returncode == 0, (p.stdout or p.stderr).strip()[:600]

prs = [tuple(l.strip().split(",")) for l in open(PR_FILE) if l.strip()]
results = []
for i, (repo, num) in enumerate(prs, 1):
    r = {"repo": repo, "num": num}
    d = gh_view(repo, num)
    if "error" in d:
        r["status"] = "CHECK_ERROR"
        r["error"] = d["error"]
    else:
        r["status"] = d.get("state")
        r["ms"] = d.get("ms")
        r["title"] = d.get("title")
        if r["status"] == "OPEN" and r["ms"] == "CLEAN":
            ok, msg = gh_merge(repo, num)
            r["merge"] = "MERGED" if ok else "MERGE_FAILED"
            r["merge_msg"] = msg
        elif r["status"] == "OPEN":
            r["merge"] = "SKIPPED_NOT_CLEAN"
        else:
            r["merge"] = "SKIPPED_NOT_OPEN"
    results.append(r)
    print(f"[{i}/{len(prs)}] {repo}#{num} {r.get('status')} {r.get('ms','')} {r.get('merge','')}", flush=True)
    time.sleep(0.2)

with open(OUT, "w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")

merged = [r for r in results if r.get("merge") == "MERGED"]
merge_failed = [r for r in results if r.get("merge") == "MERGE_FAILED"]
open_prs = [r for r in results if r.get("status") == "OPEN"]
closed = [r for r in results if r.get("status") in ("MERGED", "CLOSED")]
errors = [r for r in results if r.get("status") == "CHECK_ERROR"]

lines = []
lines.append("# merge-law-ci-watch run 2026-10-23 04:57 CDT")
lines.append("")
lines.append(f"total={len(results)} merged_this_run={len(merged)} merge_failed={len(merge_failed)} "
             f"still_open={len(open_prs)} already_closed={len(closed)} check_errors={len(errors)}")
lines.append("")
lines.append("## Merged this run")
if merged:
    for r in merged:
        lines.append(f"- {r['repo']}#{r['num']} — {r.get('title','')}")
else:
    lines.append("- none")
lines.append("")
lines.append("## Merge failed (were CLEAN at check)")
if merge_failed:
    for r in merge_failed:
        lines.append(f"- {r['repo']}#{r['num']} — {r.get('merge_msg','')}")
else:
    lines.append("- none")
lines.append("")
lines.append("## Still OPEN (not CLEAN — left alone)")
if open_prs:
    for r in open_prs:
        lines.append(f"- {r['repo']}#{r['num']} [{r.get('ms')}] — {r.get('title','')}")
else:
    lines.append("- none — watch list is CLEAR")
lines.append("")
lines.append("## Check errors")
if errors:
    for r in errors:
        lines.append(f"- {r['repo']}#{r['num']} — {r.get('error','')}")
else:
    lines.append("- none")
lines.append("")
lines.append("## Already closed/merged before this run")
lines.append(f"- count: {len(closed)}")
lines.append("")
with open(REPORT, "w") as f:
    f.write("\n".join(lines))

print("\nSUMMARY: " + lines[2])
print("Report:", REPORT)
