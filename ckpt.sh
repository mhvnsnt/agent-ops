#!/bin/bash
# ckpt.sh — atomic checkpoint writer for agent-ops/checkpoints/
# Usage: ckpt.sh <name.json> '<json-or-key=value pairs>'
# Validates schema, writes atomically (temp + rename), stamps updated_at.
#
# Schema: {"task": str, "status": str, "watchdog": bool, "repo": str,
#          "resume_brief": str, "updated_at": iso8601, "attempts": int, "notes": str}
# watchdog=true checkpoints get auto-resumed by the worker-watchdog cron.
set -euo pipefail
CKPT_DIR="${CKPT_DIR:-$HOME/workspace/agent-ops/checkpoints}"
name="$1"; shift
tmp="$(mktemp "$CKPT_DIR/.tmp.XXXXXX")"
now="$(date -u +%Y-%m-%dT%H:%M:%S.%6N+00:00)"
# Build JSON from key=value args via python for safety
python3 - "$tmp" "$now" "$@" <<'EOF'
import json, sys
tmp, now = sys.argv[1], sys.argv[2]
d = {}
for kv in sys.argv[3:]:
    k, v = kv.split("=", 1)
    if v in ("true", "false"):
        v = v == "true"
    elif v.isdigit():
        v = int(v)
    d[k] = v
d.setdefault("status", "running")
d.setdefault("watchdog", True)
d.setdefault("attempts", 0)
d["updated_at"] = now
# Schema validation
for req in ("task", "resume_brief", "repo"):
    if req not in d or not d[req]:
        sys.stderr.write(f"ckpt.sh: missing required field '{req}'\n")
        sys.exit(2)
if d["watchdog"] and d["status"] not in ("done", "complete", "cancelled", "needs_owner") and len(d["resume_brief"]) < 50:
    sys.stderr.write("ckpt.sh: watchdog checkpoint needs a real resume_brief (>=50 chars)\n")
    sys.exit(2)
with open(tmp, "w") as f:
    json.dump(d, f, indent=1)
print(f"checkpoint staged: {tmp}")
EOF
mv "$tmp" "$CKPT_DIR/$name"
echo "checkpoint saved: $CKPT_DIR/$name"
