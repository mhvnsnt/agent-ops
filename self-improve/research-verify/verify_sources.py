#!/usr/bin/env python3
"""verify_sources.py — deterministic pull check for a research source list.

A source is FETCH-VERIFIED only when bytes were actually fetched (or a git
remote answered ls-remote) in THIS run. Search-result text is NEVER fetch
proof. A 429 / timeout / DNS failure is recorded as RETRY-LATER with the
exact error and queued — not silently dropped, not upgraded to "verified".

Usage:
  python3 verify_sources.py sources.json --out DIR
  python3 verify_sources.py --retry-queue DIR/verify-queue.jsonl --out DIR

sources.json: [{"name": "...", "url": "https://...", "licence": "...",
                "kind": "git|http (auto if omitted)"}]
  - licence is REQUIRED. Empty/missing -> licence_verdict "MISSING" and the
    source is flagged NOT-RANKABLE (a ranked list may not contain it).
  - kind git: `git ls-remote <url> HEAD` must answer (proves the repo exists
    and is reachable without cloning).
  - kind http: GET with a 1 MiB probe cap; records status, content-length,
    bytes read, sha256 of bytes read.

Outputs in DIR: verify-log.jsonl (one record per source), summary.json,
verify-queue.jsonl (RETRY-LATER items, for --retry-queue).
Exit 0 = all sources FETCH-VERIFIED with a licence verdict.
Exit 1 = any source RETRY-LATER, FAILED, or licence MISSING.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROBE_CAP = 1 << 20          # 1 MiB probe read per http source
RETRY_DELAYS = [2, 15, 60]   # seconds between attempts on 429/5xx/network
USER_AGENT = "Muse-research-verify/1.0 (+research pull check)"


def git_check(url):
    """Returns (ok, detail). ls-remote answers = repo exists + reachable."""
    try:
        r = subprocess.run(["git", "ls-remote", url, "HEAD"],
                           capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False, "git ls-remote timed out after 120s"
    if r.returncode == 0 and r.stdout.strip():
        return True, r.stdout.strip().split()[0]
    return False, (r.stderr.strip() or "git ls-remote failed")[:300]


def http_check(url):
    """GET with retries. Returns (label, detail dict)."""
    last_err = ""
    for attempt, delay in enumerate([0] + RETRY_DELAYS):
        if attempt:
            time.sleep(delay)
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": USER_AGENT,
                              "Range": f"bytes=0-{PROBE_CAP - 1}"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read(PROBE_CAP)
                return ("FETCH-VERIFIED", {
                    "http_status": resp.status,
                    "content_length": resp.headers.get("Content-Length"),
                    "bytes_read": len(data),
                    "sha256_probe": hashlib.sha256(data).hexdigest(),
                    "final_url": resp.geturl(),
                    "attempts": attempt + 1,
                })
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code not in (429, 500, 502, 503, 504):
                return ("FAILED", {"http_status": e.code,
                                   "error": last_err,
                                   "attempts": attempt + 1})
        except Exception as e:  # timeout, DNS, TLS, connection reset
            last_err = f"{type(e).__name__}: {e}"[:200]
    return ("RETRY-LATER", {"error": last_err,
                            "attempts": len(RETRY_DELAYS) + 1,
                            "hint": "429/5xx/network — re-run with "
                                    "--retry-queue after a pause"})


def check_source(src):
    name, url = src.get("name", "?"), src.get("url", "")
    licence = (src.get("licence") or "").strip()
    kind = src.get("kind") or ("git" if url.endswith(".git")
                               or "github.com/" in url else "http")
    rec = {"name": name, "url": url, "kind": kind,
           "licence": licence or None,
           "licence_verdict": "PRESENT" if licence else "MISSING"}
    if not url:
        rec.update({"label": "FAILED", "detail": {"error": "no url"}})
    elif kind == "git":
        ok, detail = git_check(url)
        rec.update({"label": "FETCH-VERIFIED" if ok else "FAILED",
                    "detail": {"ls_remote_head": detail} if ok
                    else {"error": detail}})
    else:
        label, detail = http_check(url)
        rec.update({"label": label, "detail": detail})
    rec["rankable"] = (rec["label"] == "FETCH-VERIFIED"
                       and rec["licence_verdict"] == "PRESENT")
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sources", nargs="?")
    ap.add_argument("--retry-queue")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.retry_queue:
        srcs = [json.loads(l) for l in
                Path(args.retry_queue).read_text().splitlines() if l.strip()]
    elif args.sources:
        srcs = json.loads(Path(args.sources).read_text())
    else:
        print("ERROR: give sources.json or --retry-queue", file=sys.stderr)
        return 2

    log_path = outdir / "verify-log.jsonl"
    queue_path = outdir / "verify-queue.jsonl"
    records, queued = [], []
    with open(log_path, "w") as log:
        for src in srcs:
            rec = check_source(src)
            records.append(rec)
            log.write(json.dumps(rec) + "\n")
            log.flush()
            if rec["label"] == "RETRY-LATER":
                queued.append(src)
            print(f"{rec['label']:15s} {rec['name']} "
                  f"({'licence MISSING' if rec['licence_verdict'] == 'MISSING' else 'licence ok'})")
    queue_path.write_text("".join(json.dumps(s) + "\n" for s in queued))
    summary = {
        "total": len(records),
        "fetch_verified": sum(r["label"] == "FETCH-VERIFIED" for r in records),
        "retry_later": sum(r["label"] == "RETRY-LATER" for r in records),
        "failed": sum(r["label"] == "FAILED" for r in records),
        "licence_missing": sum(r["licence_verdict"] == "MISSING"
                               for r in records),
        "rankable": sum(r["rankable"] for r in records),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))
    return 0 if (summary["retry_later"] == 0 and summary["failed"] == 0
                 and summary["licence_missing"] == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
