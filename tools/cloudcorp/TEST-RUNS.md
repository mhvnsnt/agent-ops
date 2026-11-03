# Test-run results — CloudCorp pull-in, 2026-11-02

Rule: a tool is only "wired" if it was audited AND run against our
own material, or is honestly marked NOT-RUN with the reason.

## Environment blocker (affects most npm tools)

This VM drops shell-written network-fetched content: `npm install`
of the fleet completed its download ("added 350 packages in 4m" for
a 7-tool combined install, registry fetches 200 OK, 68 MB npm cache
persisted) but the extracted `node_modules/` did not persist on
disk, and `git clone`/tarballs fail the same way. Files persisted
via file tools DO persist. So npm tools were test-run only where a
file-tool-persisted route existed (agentsfile, below). Everything
else is marked NOT-RUN (VM) — not claimed as working. Unblock: run
the pinned `npx` commands from `mcp.json` on any normal host or CI
runner where npm installs persist; agentsfile's run proves the
pattern once files are on disk.

## Ran for real

### Xod sentinel.py (vendored, pinned 6e5ebd4, blob-hash verified)
- Command: `python3 tests/smoke/run_sentinel_test.py` (scratch copy
  of the vendored files + documented stubs for non-vendored Xod app
  plumbing; all review/hold decisions are the real vendored code)
- Output: **32 ✓, 0 ✗** across every rule family — injection 3/3,
  not_from_you 7/7, secret 3/3, remote_run 4/4, not_asked 5/5,
  exemptions 2/2, hold→approve→model-check 8/8. Exit code 1 comes
  solely from section S8, which tests a Xod researcher module that
  is NOT part of this pull-in (left as an honest stub, not faked).
- Verdict: **USEFUL** — adopt the sentinel core as the agent-ops
  provenance/injection gate.

### agentsfile 0.1.0 (byte-size-verified source, dist hand-stripped
from the verified TS because tsc/tsx cannot persist on this VM;
logic unchanged, CLI path imports only its own core)
- `node dist/cli.js --version` → `0.1.0`, exit 0
- `node dist/cli.js check ~/workspace/agent-ops` → exit 1, verdict
  **MISSING** — factually correct: that checkout has no root
  AGENTS.md/CLAUDE.md to validate.
- `node dist/cli.js check ~/AGENTS.md` → exit 1, verdict **DRIFT** —
  9 findings; correctly flagged that the home AGENTS.md still
  references paths under the `tools/` tree that was archived away
  2026-10-31 (plus several context-noise hits: it is a global file,
  so per-repo runs are the right use).
- Verdict: **USEFUL, narrowly** — run per-repo against root guides,
  not against global files. Fully offline, deterministic.

## Not run on this VM (audited + wired; execution blocked by the VM, see above)

greenlight, injectcheck, hookcheck, actionpin, depguard, flowcheck,
cidiff, mcpvet, mcpaudit, shipcheck, skillcheck, testdelta,
logdigest, readmeaudit, commitcheck, agent-evals, prodforge,
muse-marketplace, specforge, scenemodel, videokit, audioport,
imageport — **NOT-RUN (VM)**. No NOT-WORTH-IT verdicts are claimed
for tools we could not execute; that judgment waits for the first
run on a working host. Priority order for that first run (highest
value first): injectcheck (planted-injection vs clean PR body),
hookcheck (our settings/workflows), mcpaudit against agentsfile's
MCP surface, shipcheck on a greenlight release, videokit probe on a
real mp4 (ffmpeg is present on hosts; its arg-array core was
audited CLEAN), scenemodel protocol check (needs the blender-mcp
addon running — none was running during this lane).

muse-farm 0.5.1 — NOT-RUN: it supervises Muse sessions
(~/.local/share/muse/sessions) and this lane did not start farm
supervision against live sessions. Its farm.py was audited in full
(CLEAN-WITH-NOTES). First run should be a dry-run on one lane.

## NOT-WORTH-IT / excluded

- Xod `agent_clis.install()` — EXCLUDED at audit: runs hardcoded
  vendor curl|sh installers. Registry + refusal rules only.
- Greenlight `--via-api` / `auth login` — EXCLUDED from our wiring
  by policy (author-hosted claim API + token storage). Direct
  GitHub mode only.
- scenemodel/videokit/audioport/imageport GHCR images — do not use
  (no ffmpeg/ImageMagick/Blender addon inside). Host installs only.
