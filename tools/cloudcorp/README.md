# CloudCorp tools — wired index

Pinned MCP wiring: `mcp.json` in this folder (merge into the MCP
client config of the lane that needs it). Every entry is pinned to
the exact audited version — **re-audit before bumping any pin**
(audits: `docs/research/cloudcorp-2026-11-02/audits/`).

Run pattern (all npm tools): one bin serves CLI + stdio MCP server.
- MCP: `npx -y @reneturcios/<name>@<version> mcp`
- CLI: `npx -y @reneturcios/<name>@<version> --help` (then the
  subcommand the lane needs)

## Agent / security / eval suite → agent-ops, all repos, Proving Ground

| Tool | Pin | Serves | Notes from audit |
|---|---|---|---|
| greenlight | 0.25.0 | Multi-lane PR work: CI pre-flight/triage, PR babysitting (western-heart backlog first) | Direct-GitHub mode ONLY. Never `--via-api`, never `auth login` (author-hosted claim API + token storage). Never run ci-prep/verify against untrusted repos |
| injectcheck | 0.1.19 | Every lane that reads external content (PR bodies, issues, docs) before acting on it | CLEAN. Zero egress |
| hookcheck | 0.1.18 | Audits our .claude/settings.json, workflow files, npm hooks for persistence patterns | CLEAN |
| actionpin | 0.1.8 | Pinning GitHub Actions to full SHAs across our 60+ repos' workflows | `fix` rewrites workflow files — use --dry-run first |
| depguard | 0.4.0 | PR-time dependency early warning on manifest/lockfile diffs | Offline by default; --online only deliberately |
| flowcheck | 0.1.2 | GitHub Actions workflow YAML audit | CLEAN, purely local |
| cidiff | 0.1.2 | "Yours vs pre-existing" CI failure split on PRs | Needs GITHUB_TOKEN (its job) |
| mcpvet | 0.2.1 | Gate BEFORE installing any MCP server/skill (including future CloudCorp promotions) | Only egress: npm metadata |
| mcpaudit | 0.1.2 | Live handshake/schema/bad-call audit of an MCP server | Run with a SCRUBBED env — it passes full host env to the target server |
| shipcheck | 0.2.0 | Release GO/NO-GO: git tag / GitHub release / npm / GHCR / MCP Registry must agree | Fits our GitHub+TeraBox verification discipline |
| agent-evals | 0.1.0 | Proving Ground grading: point at any agent (URL or MCP), get tool-use/accuracy/latency scores | LLM-judge cases call api.anthropic.com only if ANTHROPIC_API_KEY set |
| prodforge | 0.5.0 | Fleet catalog/installer: one merged MCP config + ship gate for the tools above | Generates config only; downloads nothing itself |

## Repo-hygiene suite → agent-ops CI / lane discipline

| Tool | Pin | Serves |
|---|---|---|
| agentsfile | 0.1.0 | Validates AGENTS.md/CLAUDE.md paths + scripts against repo reality (anti-rot) |
| skillcheck | 0.1.0 | SKILL.md link checker for our custom skills |
| readmeaudit | 0.1.0 | README claims vs repo reality |
| commitcheck | 0.1.0 | Commit convention + DCO sign-off over a history range |
| testdelta | 0.1.0 | Diff two test-result JSONs (what changed between runs) |
| logdigest | 0.1.0 | Summarize a CI log file into the signal |
| specforge | 0.1.0 | Fully local spec→plan→tasks trees for Proving Ground / job-sequence work |

## Muse platform tools → agent-ops

| Tool | Pin | Serves | Notes |
|---|---|---|---|
| muse-farm | 0.5.1 | Headless parallel/scheduled `muse exec` lanes (Python, stdlib only — NOT npm; run `python3 farm.py` from a clone of CloudCorpRecords/muse-farm pinned at v0.5.1) | Reads Muse session logs to supervise (its job); ntfy only if a topic is configured; self-update only on explicit invocation |
| muse-marketplace | 0.1.0 | Registry for Muse avatars/personas/voices/bundles with sha256 checksums + doctor | Install = verified local copy only, no network |

## Media / 3D tools → western-heart / Forge3D / cartoon factory (adoption there is the next step)

Host install ONLY — never their GHCR images (they bundle neither
ffmpeg/ImageMagick nor, for scenemodel, the Blender addon).

| Tool | Pin | Serves | Notes |
|---|---|---|---|
| scenemodel | 0.1.0 | Agent-driven Blender: scene/object info, Blender Python, viewport screenshots, PolyHaven, Hunyuan3D — rig/scene lanes + screenshot proof | Needs the upstream blender-mcp addon running (socket localhost:9876); screenshot tool returns a byte summary, not the image |
| videokit | 0.1.0 | ffmpeg probe/trim/transcode/frame+audio extract for clip + asset lanes | Arg-array exec, no shell |
| audioport | 0.1.0 | ffprobe metadata, convert, trim, loudnorm; transcription via an operator-set local command only | Set AUDIOPORT_TRANSCRIBER_COMMAND deliberately (e.g. whisper-cli) |
| imageport | 0.1.0 | ImageMagick metadata/resize/convert/crop/rotate for sprites/portraits | No AI, no network |

## Xod parts

See `tools/xod-parts/` — vendored sentinel.py + benchmark.py
(pinned to Xod v0.9.23, commit 6e5ebd4a0113bcf68800b6e034aa3d88e9b1f877),
plus the documented patterns for scorecard / worktrees / agent_clis /
harness board-seat record.
