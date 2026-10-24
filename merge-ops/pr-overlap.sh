#!/usr/bin/env bash
#
# pr-overlap.sh — flag merge-order hazards before merge batches (read-only)
#
# STATUS (2026-10-22, friction-research task C): quick-win wire-up.
# Lists open PRs with their changed files, pairwise file overlaps, and each
# PR's mergeable state — so a reviewer/lane can order merges instead of
# discovering the conflict after landing. (2026-10-22: PR #497 carried old
# geometry vs merged PR #508's fix — this script flags exactly that class.)
#
# Zero repo-setting changes, zero cost, read-only gh calls. It does NOT enforce
# serialization; enforcement is the merge-queue pilot (owner approval needed).
#
# USAGE: pr-overlap.sh [OWNER/REPO]   (default: repo of current directory)
#
set -u

REPO="${1:-}"
ARGS=(pr list --state open --limit 100
      --json number,title,headRefName,mergeable,mergeStateStatus,files
      --jq '.')
[[ -n "$REPO" ]] && ARGS+=(--repo "$REPO")

DATA="$(gh "${ARGS[@]}")" || { echo "pr-overlap: gh pr list failed" >&2; exit 2; }

python3 - "$DATA" <<'PYEOF'
import json, sys
prs = json.loads(sys.argv[1])
if not prs:
    print("no open PRs"); sys.exit(0)
files_of = {}
for pr in prs:
    fs = sorted({f["path"] for f in pr.get("files", []) if "path" in f})
    files_of[pr["number"]] = (pr, fs)
    m1 = pr.get("mergeable", "?"); m2 = pr.get("mergeStateStatus", "?")
    print("PR #%d [%s/%s] %s: %s (%d files)" % (
        pr["number"], m1, m2, pr["headRefName"], pr["title"][:72], len(fs)))
print()
nums = sorted(files_of)
hazards = 0
for i, a in enumerate(nums):
    pra, fa = files_of[a]
    for b in nums[i+1:]:
        prb, fb = files_of[b]
        shared = sorted(set(fa) & set(fb))
        if shared:
            hazards += 1
            print("OVERLAP: PR #%d <-> PR #%d (%d shared files):" % (a, b, len(shared)))
            for f in shared[:20]:
                print("    " + f)
            if len(shared) > 20:
                print("    ... +%d more" % (len(shared) - 20))
            ma, mb = pra.get("mergeable"), prb.get("mergeable")
            first, second = (a, b) if a < b else (b, a)
            if ma == "CONFLICTING" or mb == "CONFLICTING":
                print("    !! already CONFLICTING - rebase order required before merge")
            else:
                print("    -> suggested order: merge #%d first (older), then rebase #%d onto it" % (first, second))
            print()
if hazards == 0:
    print("no file overlaps between open PRs")
else:
    print("%d overlapping pair(s) - order merges, do not land in parallel" % hazards)
PYEOF
