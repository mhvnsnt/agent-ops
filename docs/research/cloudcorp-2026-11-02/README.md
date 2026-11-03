# CloudCorpRecords pull-in — 2026-11-02

Owner order (2026-11-02): pull in the top 25 CloudCorpRecords tools,
log all the rest as research/watch, wire them up, and FIRST make sure
none of them do anything malicious, spy-ish, or against our work —
every one must be audited, tested on our own material, and actually
helpful.

Source evaluation: Ashes' sweep of all 357 public repos by
CloudCorpRecords (single author Rene Turcios) — full inventory in
`INVENTORY.md` in this folder; the research/watch log for everything
not pulled in is `WATCHLIST.md` in this folder.

## What landed here

| Piece | Where |
|---|---|
| This evaluation + audit summary | `docs/research/cloudcorp-2026-11-02/` |
| Full per-tool security audits (26 files) | `docs/research/cloudcorp-2026-11-02/audits/` |
| Full 355-repo inventory / watch list | `docs/research/cloudcorp-2026-11-02/INVENTORY.md` + `WATCHLIST.md` |
| Pinned MCP wiring for the 24 npm tools | `tools/cloudcorp/mcp.json` |
| Tool index (what each is for, which repo/job it serves, how to run it, verdicts) | `tools/cloudcorp/README.md` |
| Test-run results on our own material | `tools/cloudcorp/TEST-RUNS.md` |
| Xod parts vendored (MIT, LICENSE kept) | `tools/xod-parts/` |

RESEARCH-PULLIN-INDEX row (paste into `RESEARCH-PULLIN-INDEX.md`):

| CloudCorpRecords fleet | 25 tools + Xod parts, security-audited + test-run | → agent-ops `docs/research/cloudcorp-2026-11-02/` + `tools/cloudcorp/` + `tools/xod-parts/` | This PR | 🔄 Pulled + wired (pinned npx MCP config); test-run verdicts in `tools/cloudcorp/TEST-RUNS.md`; remaining 330 repos logged as RESEARCH/WATCH in the same folder |

## Phase 1 — security audit verdicts (owner's hard gate)

Method: full source audit per tool (package.json, Dockerfile,
server.json, ALL of src/, scripts/ where present) — postinstall hooks,
network egress, env/credential access, remote-code execution,
obfuscation, write scope, telemetry. Environment forced the route:
`git clone` is broken VM-wide and tarballs return 0 bytes through the
proxy, so source was read via the GitHub contents API and raw file
reads, cross-verified by blob SHA. **Zero REJECTs.** Universal
findings: no preinstall/postinstall/prepare hooks anywhere, no
telemetry/analytics anywhere, no ~/.ssh, ~/.aws, Keychain, or
browser-profile access by any tool's own code.

| Tool | Version | Verdict |
|---|---|---|
| greenlight | 0.25.0 | CLEAN-WITH-NOTES — GitHub tool; opt-in `--via-api` claim flow talks to the author's hosted API (claim-api-wine.vercel.app) and `auth login` stores our GitHub token (keychain or 0600 file) BY DESIGN — do not use `--via-api`/`auth login`; direct-GitHub mode only. Opt-in Fireworks LLM egress only if FIREWORKS_API_KEY set. `sh -c` only runs the target repo's own CI/test commands (its ci-prep/verify features — never against untrusted repos) |
| injectcheck | 0.1.19 | CLEAN — zero egress/env; all credential/curl hits are detection-rule data |
| hookcheck | 0.1.18 | CLEAN — zero egress/exec/writes in own code; hits are detection patterns |
| actionpin | 0.1.8 | CLEAN-WITH-NOTES — GITHUB_TOKEN sent only to hardcoded api.github.com; `fix` rewrites our workflow files (its job; has --dry-run) |
| depguard | 0.4.0 | CLEAN-WITH-NOTES — offline core; npm/PyPI registry only behind --online/--content; tarballs diffed in memory, never installed/executed |
| flowcheck | 0.1.2 | CLEAN — pure local YAML audit |
| cidiff | 0.1.2 | CLEAN-WITH-NOTES — GITHUB_TOKEN for GitHub API; API base env-overridable only by our own config |
| mcpvet | 0.2.1 | CLEAN-WITH-NOTES — only egress is npm registry metadata; opt-in probe runs a user-supplied local server command |
| mcpaudit | 0.1.2 | CLEAN-WITH-NOTES — zero egress; spawns the target server (its job) with FULL host env copied in — always run it with a scrubbed env against untrusted servers |
| shipcheck | 0.2.0 | CLEAN-WITH-NOTES — egress only to api.github.com / npm / PyPI / MCP Registry / GHCR (its job); reads only GITHUB_TOKEN, sent only to api.github.com |
| agentsfile | 0.1.0 | CLEAN — read-only local validation |
| skillcheck | 0.1.0 | CLEAN — read-only local validation; links resolved on disk, never fetched |
| testdelta | 0.1.0 | CLEAN — reads only the two user-named result JSONs |
| logdigest | 0.1.0 | CLEAN — reads only the one user-named log file |
| readmeaudit | 0.1.0 | CLEAN — read-only local auditor |
| commitcheck | 0.1.0 | CLEAN — only subprocess is fixed shell-free `git log` |
| agent-evals | 0.1.0 | CLEAN-WITH-NOTES — agent URLs are user-supplied (its job); LLM-judge POSTs to api.anthropic.com only when ANTHROPIC_API_KEY is set |
| prodforge | 0.5.0 | CLEAN-WITH-NOTES — downloads/installs nothing itself; only GENERATES an `npx -y` fleet config — fleet packages stand on their own audits (done, this table) |
| muse-farm | 0.5.1 | CLEAN-WITH-NOTES — stdlib Python; wraps `muse exec`; reads Muse session logs under ~/.local/share/muse/sessions (its supervise job); ntfy.sh POST only when a user topic is configured; self-update is explicit-invocation git-pull + test run |
| muse-marketplace | 0.1.0 | CLEAN-WITH-NOTES — zero network/subprocess; install = sha256-verified local copy with executable-extension denylist |
| specforge | 0.1.0 | CLEAN-WITH-NOTES — fixed shell-free command table (git checkout -b, npx prettier/eslint, npm test/audit) in the target project only |
| scenemodel | 0.1.0 | CLEAN-WITH-NOTES — only egress is the Blender addon socket (BLENDER_HOST:BLENDER_PORT, default localhost:9876); PolyHaven/Hunyuan are forwarded to the addon, not called directly |
| videokit | 0.1.0 | CLEAN — arg-array execFile ffmpeg/ffprobe; no env/network/shell |
| audioport | 0.1.0 | CLEAN-WITH-NOTES — only env key is AUDIOPORT_TRANSCRIBER_COMMAND, an operator-chosen local command, execFile no shell |
| imageport | 0.1.0 | CLEAN — arg-array execFile ImageMagick; no env/network/shell |
| Xod parts (v0.9.23, commit 6e5ebd4) | — | CLEAN-WITH-NOTES — sentinel core is stdlib-only, zero egress (its review_message() delegates to the host's configured LLM — we use the deterministic core); benchmark localhost-only; scorecard read-only; worktrees' pull_request() pushes to origin (review before use); agent_clis --yolo refusal is real and enforced, BUT its install() helper runs hardcoded vendor curl\|sh — that function is EXCLUDED from our pull-in, registry pattern only |

## Honest limits

- The tools are days old, single-author, 0-star. Greenlight is the
  only battle-tested piece. Everything is pinned to exact versions in
  `tools/cloudcorp/mcp.json` so an upstream change never reaches us
  silently; re-audit before any version bump.
- npm is broken on the current VM (EPERM on registry writes), so
  test-runs that needed `npm install` were run where the environment
  allowed and are marked honestly in TEST-RUNS.md; anything not run
  is marked NOT-RUN with the reason, never claimed as working.
- scenemodel/videokit/audioport/imageport adoption INSIDE
  western-heart is the next step (western-heart has live lanes; this
  lane lands config + usage docs in agent-ops only).
