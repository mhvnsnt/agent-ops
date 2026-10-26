# Resume Brief Template

You are resuming a task that was interrupted by a machine/daemon restart.
The previous worker is gone. Its checkpoint is your only source of truth.

## Step 1 — Read these first, in order

1. Your checkpoint: `~/workspace/agent-ops/checkpoints/<TASK_ID>.json`
2. This template (you're reading it)
3. `~/workspace/agent-ops/IDEMPOTENCY.md` — the write rules. Follow them.

## Step 2 — Reconstruct state

From the checkpoint, extract:
- **Goal**: what the task was trying to achieve
- **Completed steps**: already done. DO NOT REDO THESE. Verify cheaply
  (e.g. `ls` the output files, `git log --oneline -3`) instead of re-running.
- **Next steps**: where to continue
- **Key paths**: files and directories the work lives in
- **Decisions**: constraints from earlier in the task. These are binding
  unless the parent agent explicitly overrides them.

## Step 3 — Verify before continuing

- Check the repo state: `git status --short`, `git log --oneline -5`
- Check that output files the checkpoint claims exist actually exist
- If the checkpoint says a step was done but its outputs are missing,
  treat that step as NOT done and redo it (the restart may have eaten it)

## Step 4 — Claim the task, then continue with checkpointing

- **Claim first**: `checkpoint.sh claim <TASK_ID> <your-agent-id>` — this
  bumps the fencing epoch and prints `EPOCH=N`. From now on pass
  `--epoch N` on **every** checkpoint write. If a write comes back
  `FENCED` (exit 3), someone else claimed the task after you — stop and
  report to the parent; do not force your way in. (Full contract:
  `LANE-RESILIENCE-SOP.md`.)
- Update your checkpoint as you work:
  - `checkpoint.sh beat <TASK_ID> --epoch N` at least every 10 minutes during long runs
  - `checkpoint.sh step <TASK_ID> "..." --epoch N` after each completed unit of work
  - `checkpoint.sh next <TASK_ID> "..."` when the plan changes
  - `checkpoint.sh decide <TASK_ID> "..."` for any decision a future
    resume needs to know
- When finished: `checkpoint.sh status <TASK_ID> completed`
- If blocked: `checkpoint.sh status <TASK_ID> stalled` and record why in
  `next_steps`

## Rules

- Never re-push, re-send, or re-publish anything the checkpoint says is done
  without first verifying it actually landed (check the remote/repo, not memory).
- If the checkpoint is missing or unreadable, do NOT guess at prior state.
  Report that to the parent agent and ask for direction.
- Your final report to the parent must state: what was already done before
  the restart, what you did after resuming, and what remains.

## Standing Laws (apply to every resume)

- **RESEARCH-BEFORE-ANSWER**: If you need to answer "what's the best X", run `python3 ~/workspace/tools/research.py compare "<topic>"` first. Don't guess from training data.
- **NO-SILENT-FAILURE**: If you discover something failed, report it immediately. Never let the owner discover a failure by asking.
- **PHONE-BRIDGE**: The owner is phone-only. If something needs a browser/computer, do it yourself. Don't hand him manual homework.
- **PULL-STRAIGHT-TO-STORE**: Clone directly into repo checkouts, wire up there, push. Don't stage on local disk.
- **RESPOND-FAST**: Acknowledge fast, work async. Don't chain tool calls in silence.
- **CHECK-PR-BODY-LOCALLY**: Before opening a PR, verify its body with the local instruction-gate check — the queue's copy at `agent-ops/queue-work/instruction_gate-main.py` is verified byte-identical to the live gate (`.github/scripts/instruction_gate.py` on western-heart main). Pattern: `agent-ops/queue-work/check1146.py` — `check(body, changed_files, repo_root, labels, author)` returns the error list; empty = pass. A body that fails locally fails CI too, so check before pushing, not after.
