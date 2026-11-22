#!/usr/bin/env python3
"""Snapshot ~/MEMORY.md into the private GitHub repo mhvnsnt/agent-memory.

Owner order 2026-11-02: MEMORY.md is always backed up in the agent-memory
repo so it can never be lost again (it was truncated to 0 bytes on
2026-11-02 and rebuilt from the memory index, fragments, and daily logs).

Safety guard: if the live file is missing or suspiciously small (<10 KB),
REFUSE to snapshot (exit 2) so a truncation can never overwrite the good
backup. Exit 0 = pushed or already current. Exit 1 = other failure.
"""
import subprocess, base64, json, hashlib, sys, datetime, os

REPO = "mhvnsnt/agent-memory"
SRC = os.path.expanduser("~/MEMORY.md")
MIN_BYTES = 10_000


def gh(*args, inp=None):
    return subprocess.run(["gh", "api", *args], input=inp,
                          capture_output=True, text=True)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main() -> int:
    if not os.path.exists(SRC):
        print("GUARD: ~/MEMORY.md missing — refusing to snapshot")
        return 2
    data = open(SRC, "rb").read()
    if len(data) < MIN_BYTES:
        print(f"GUARD: ~/MEMORY.md is only {len(data)} bytes "
              f"(< {MIN_BYTES}) — refusing to snapshot a likely truncation")
        return 2

    r = gh(f"repos/{REPO}/contents/MEMORY.md", "--jq", ".sha")
    remote_sha = r.stdout.strip() if r.returncode == 0 else None
    if remote_sha and remote_sha == blob_sha(data):
        print("NOCHANGE: repo copy already matches live MEMORY.md "
              f"({len(data)} bytes)")
        return 0

    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M %Z")
    payload = {"message": f"Snapshot MEMORY.md {stamp} ({len(data)} bytes)",
               "content": base64.b64encode(data).decode()}
    if remote_sha:
        payload["sha"] = remote_sha
    r = gh(f"repos/{REPO}/contents/MEMORY.md", "-X", "PUT",
           "--input", "-", inp=json.dumps(payload))
    if r.returncode != 0:
        print("PUSH FAILED:", r.stderr[:300])
        return 1

    r = gh(f"repos/{REPO}/contents/MEMORY.md", "--jq", ".content")
    remote = base64.b64decode(r.stdout.replace("\n", ""))
    if remote != data:
        print("VERIFY FAILED: read-back does not match live file")
        return 1
    print(f"PUSHED+VERIFIED: MEMORY.md snapshot {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
