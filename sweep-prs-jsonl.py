#!/usr/bin/env python3
"""Overnight pipeline PR sweep — reproduces sweep-YYYYMMDD-HHMM.jsonl format.
Usage: python3 sweep-prs-jsonl.py [HHMM]
Writes ~/workspace/agent-ops/sweep-<YYYYMMDD>-<HHMM>.jsonl, one JSON line per repo.
"""
import json, subprocess, sys, datetime, os

OWNER = "mhvnsnt"
REPOS = ["western-heart", "Bannon", "cape-jones", "physics-playground-pwa",
         "dream-girl", "pokemon-arena-3d", "ConcreteDragon2", "agent-ops",
         "game-reverse-engineering", "wrestling-game", "ConcreteDragon",
         "wizard-gang-storage"]

def gh(*args):
    r = subprocess.run(["gh", "api"] + list(args), capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"gh api {' '.join(args)} failed: {r.stderr.strip()[:300]}")
    return json.loads(r.stdout) if r.stdout.strip() else None

def pr_state(repo, number):
    """mergeStateStatus via gh pr view (GraphQL). The REST list endpoint
    returns mergeable_state='unknown' until each PR is fetched individually."""
    r = subprocess.run(["gh", "pr", "view", str(number), "--repo", f"{OWNER}/{repo}",
                        "--json", "mergeStateStatus,mergeable",
                        "--jq", r'"\(.mergeStateStatus) \(.mergeable)"'],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return "unknown", False
    ms, mg = r.stdout.strip().split()
    # gh 2.102 returns mergeable as an enum string (MERGEABLE/CONFLICTING/UNKNOWN),
    # not a boolean — accept both forms (fixed 2026-11-25: wholesale False bug).
    return ms.lower(), mg in ("true", "MERGEABLE")

def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    tag = sys.argv[1] if len(sys.argv) > 1 else now.strftime("%H%M")
    out = os.path.expanduser(f"~/workspace/agent-ops/sweep-{now.strftime('%Y%m%d')}-{tag}.jsonl")
    rows = []
    for repo in REPOS:
        try:
            br = gh(f"repos/{OWNER}/{repo}/branches/main")
            tip = br["commit"]["sha"][:7]
            tip_time = br["commit"]["commit"]["committer"]["date"]
        except Exception as e:
            rows.append({"repo": repo, "error": str(e)[:200], "open_count": -1})
            print(f"{repo}: TIP ERROR {e}", file=sys.stderr, flush=True)
            continue
        prs = gh(f"repos/{OWNER}/{repo}/pulls?state=open&per_page=100")
        items = []
        for p in prs:
            n = p["number"]
            try:
                runs = gh(f"repos/{OWNER}/{repo}/commits/{p['head']['sha']}/check-runs?per_page=100")
                checks = sorted({c.get("conclusion") for c in runs.get("check_runs", []) if c.get("conclusion")})
            except Exception:
                checks = []
            ms, mg = pr_state(repo, n)
            items.append({
                "number": n,
                "title": p["title"][:80],
                "draft": bool(p.get("draft")),
                "head": p["head"]["sha"][:7],
                "base": p["base"]["ref"],
                "mergeable_state": ms,
                "mergeable": mg,
                "checks": checks,
                "created": p["created_at"][:10],
            })
        rows.append({"repo": repo, "tip": tip, "tip_time": tip_time,
                     "open_prs": items, "open_count": len(items)})
        print(f"{repo}: tip {tip} open {len(items)}", file=sys.stderr, flush=True)
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    # All progress/summary output goes to stderr: the script writes the
    # jsonl itself, so redirecting stdout into that same file corrupts it
    # (2026-11-25 17:14Z run: WROTE/TOTAL lines spliced into the WH row).
    print(f"WROTE {out}", file=sys.stderr)
    print("TOTAL OPEN:", sum(r.get("open_count", 0) for r in rows if r.get("open_count", 0) > 0), file=sys.stderr)

if __name__ == "__main__":
    main()
