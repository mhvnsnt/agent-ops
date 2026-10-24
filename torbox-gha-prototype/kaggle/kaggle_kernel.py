#!/usr/bin/env python3
"""
Kaggle variant of the same trick — SAME range_list.py, different secret store.

Setup (all in Kaggle's own UI, by a human in a browser — nothing via chat):
  1. Notebook -> Add-ons -> Secrets: add SOURCE_URL (the CDN/debrid link)
     and, if the target release is in a private repo, GH_PAT
     (fine-grained, that repo only, Contents: Read and write).
  2. Notebook settings: Internet = ON. Accelerator = None (CPU is enough;
     do NOT burn the 30 GPU-hours/week quota on byte moving).
  3. Put range_list.py where the kernel can see it: clone the public
     runner repo (code only, no secrets in it) in the first cell, or add
     it as a Kaggle Dataset / utility script.

Limits that shape this variant (see ../../torbox-lane4-compute.md):
  ~9 h max session, /kaggle/working output capped ~20 GB — irrelevant here
  because everything streams OUT to GitHub; nothing is staged locally.
  CPU kernels are the right tier; a batch ("Save Version -> Run All")
  kernel runs unattended, an interactive one idles out.

Run as a script kernel, or paste main() into cells.
"""
import os
import sys

try:
    from kaggle_secrets import UserSecretsClient
    _s = UserSecretsClient()
    os.environ["SOURCE_URL"] = _s.get_secret("SOURCE_URL")
    try:
        os.environ["GH_TOKEN"] = _s.get_secret("GH_PAT")
    except Exception:
        pass  # only needed for upload steps, not for `list`
except Exception as e:
    print(f"Kaggle Secrets not available ({e}); falling back to env vars")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
import range_list  # noqa: E402  (the prototype next to this file's parent)

if __name__ == "__main__":
    # Smoke test first: costs only the zip tail + central directory bytes.
    raise SystemExit(range_list.cmd_list(os.environ["SOURCE_URL"],
                                         out="/kaggle/working/manifest.json",
                                         limit=20))
    # Then, per file: range_list.cmd_extract_one(url, "<suffix>", "-")
    # piped to an uploads.github.com POST exactly as in the GHA workflow,
    # or range_list.cmd_slice(...) for raw re-chunking.
