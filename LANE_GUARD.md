# Lane Guard — crash-resilient + collision-proof lanes

Two recurring failures (both happened on 2026-10-19):

1. **Daemon restarts kill lanes mid-work.** A restart is a given. This is
   already survivable via `checkpoint.sh` + `supervisor.sh` (see
   `CHECKPOINT_PROTOCOL.md`, `RESUME_BRIEF_TEMPLATE.md`, `IDEMPOTENCY.md`).
   Nothing here replaces that protocol — lane-guard adds the missing pieces.
2. **Shared-checkout hazards.** Multiple lanes working in ONE git checkout
   clobbered each other: a gap-audit lane committed onto another lane's
   branch; one lane's uncommitted work was stashed/restored by another.
3. **Cleanup lanes deleting live work.** A cleanup lane deleted a
   93%-complete Tekken 5 ISO download and trampled in-progress state.

## The toolkit (all in agent-ops, all additive)

| Tool | Solves |
|---|---|
| `lane-worktree.sh` | One git worktree + one branch per lane; a lanes registry; refuses cross-lane writes |
| `lane-ckpt.sh` | Thin wrapper over `checkpoint.sh`: `begin`, `beat`, `step`, plus `resume` (reads checkpoint, verifies key paths, prints the resume plan) |
| `guard-paths.sh` | Protected-paths registry + `check` / `check-tree` that every reaper (CloudDog, disk janitors, ad-hoc cleanup) must call before touching a path |
| `lanes.json` | Registry of active lanes (id, repo, worktree, branch, agent id, status) |
| `protected-paths.json` | Registry of protected paths (in-progress downloads, sacred manifests, active worktrees) |

Registry state dir defaults to the agent-ops directory; override with
`LANE_GUARD_STATE_DIR` (tests use a temp dir). Registry writes are atomic
(tmp file + rename).

## The lane workflow (use it in every lane brief)

1. **Spawn** — get your own worktree. Never work inside another lane's dir,
   and never work directly in the primary checkout of a repo another lane
   might touch.
   ```
   lane-worktree.sh spawn <lane-id> --repo <path-or-url> --branch lane/<lane-id>
   ```
   (Worktrees land in `~/workspace/agent-ops-worktrees/<lane-id>` by default.)
2. **Checkpoint** — first action in the lane, using `lane-ckpt.sh begin`
   (it is `checkpoint.sh init`): `--goal` and `--resume-prompt` are not
   optional. Then `beat` at least every ~10 min and `step` after every unit
   of work.
3. **Guard before writing** — before writing into any directory you did not
   spawn, run:
   ```
   lane-worktree.sh check <dir> --lane <lane-id>    # exit 1 = not yours, stop
   ```
   Or run commands inside your own worktree via
   `lane-worktree.sh exec <lane-id> -- <cmd...>`.
4. **Protect live state** — downloading, extracting, uploading, or otherwise
   "in progress" files must be registered the moment the lane starts them:
   ```
   guard-paths.sh add <file-or-dir> --kind download-in-progress --owner <lane-id>
   ```
   An active worktree is auto-registered on spawn and unregistered on release.
5. **Release** — when the lane is done and its branch is pushed:
   `lane-worktree.sh release <lane-id>`. Release refuses to remove a worktree
   with uncommitted work; resolve manually, never with `--force`.
6. **After a restart** — `supervisor.sh` tells the parent which lanes went
   stale. The re-spawned lane runs `lane-ckpt.sh resume <task-id>`: it reads
   the checkpoint, verifies each key path exists, lists steps already done
   (do NOT redo them) and the next steps. Missing checkpoint or missing
   paths → report to the parent, never guess. Full contract:
   `RESUME_BRIEF_TEMPLATE.md`.

## Reaper contract (CloudDog and every cleanup lane)

Before deleting, quarantine-moving, or "tidying" ANY path, a reaper MUST run:

```
guard-paths.sh check-tree <path>     # exit 1 = PROTECTED: hands off, log, skip
```

Exit 1 prints the kind, the owning lane, and the note. There is no override
flag, by design: the only way to free a protected path is for the owning
lane to `guard-paths.sh remove` it (or finish and release its worktree).

## Research notes (2026-10-20, web search — durable execution literature)

Confirmed patterns, and where lane-guard implements them:

- **"An agent run is a job, not a request."** Run id, named steps,
  checkpoint after every step, resume by name, idempotency key on every
  side effect. → `checkpoint.sh` already does this; `lane-ckpt.sh resume`
  is the resume-by-name entry point. (ekofyi.com, "Your AI Agent Is a Job,
  Not an HTTP Request", 2026-09-04)
- **Leases + heartbeats.** A worker claims a job with a lease it renews via
  heartbeat; on lease expiry another worker reclaims and resumes from the
  checkpoint — at-least-once delivery makes idempotent steps mandatory.
  → Heartbeat = `checkpoint.sh beat`; staleness is measured by
  `supervisor.sh`. Lane-guard treats the CHECKPOINT_PROTOCOL (beat every
  ~10 min, stale at 30 min) as the lease. No new lease system was invented.
  (dev.to, "long-running AI agents: Efficient Asynchronous Workflow
  Strategies"; dev.to, "Checkpoint Your Agent Jobs So Crashes Don't Mean
  Starting Over")
- **Durable execution (LangGraph-style).** Checkpointer with a stable
  thread id; durability should be *synchronous* when a missed checkpoint
  means a duplicated side effect; assume steps re-execute on resume, so
  verify reality on every wake. → `IDEMPOTENCY.md` rules 1–3, 6 +
  `lane-ckpt.sh resume`'s per-path verification. (vadim.blog, "Durable
  Execution in LangGraph")
- **Supervision layering.** systemd `Restart=on-failure` + `WatchdogSec`
  (sd_notify) is the canonical native supervisor, with restart-burst limits
  so a crashing unit doesn't storm. On this VM, the Muse daemon restart is
  what kills lanes and the daemon is outside our control — so the surviving
  pattern is exactly: checkpoint (file state) + external watchdog
  (`supervisor.sh`) + re-spawn briefs. If a lane ever runs as a raw shell
  job under tmux, its tmux session must still drive `lane-ckpt.sh beat`;
  tmux alone preserves the terminal, not the work. (dev.to, "Self-Healing
  Services: systemd + Crontab + Watchdog Patterns")
- **One worktree per agent.** The 2026 practitioner consensus for parallel
  coding agents: `git worktree` gives one branch + one directory per agent,
  physically preventing the branch-switch/stash collisions a shared checkout
  guarantees; integrate by merging branches, not by sharing files. Isolate
  only what mutates — readers may share a checkout, writers never.
  (dev.to: "Three AI Agents, One Laptop: The Git Worktree Trick...",
  "Running Coding Agents in Parallel with Git Worktrees",
  "A worktree per agent, so they never step on each other";
  shipwithai.io, "Claude Code + Git Worktrees")

## What changed vs. the existing protocol

Nothing removed, nothing rewritten. `CHECKPOINT_PROTOCOL.md`,
`IDEMPOTENCY.md`, `checkpoint.sh`, `supervisor.sh` stay byte-identical.
Lane-guard adds only: per-lane worktree allocation + registry, a resume
verifier on top of `checkpoint.sh`, and a protected-paths check reapers
can call. Gaps it closes that the old protocol did not cover: worktree
ownership (registry), cross-lane write refusal, and a callable
"hands off this path" signal for cleanup tooling.

Related: `FRICTION-RESEARCH-2026-10-19.md` diagnosed the T5 ISO deletion
mechanism (paused/resumable download older than 5 min slipped through
CloudDog's `is_inflight()`; proposed fix: claims table + hard gates in
reap paths). `guard-paths.sh check-tree` is the callable gate every reaper
— CloudDog included — should call on every candidate path. A lane
downloading anything big should also `guard-paths.sh add <file> --kind
download-in-progress` so even a reaper without the claims table sees the
protection.
