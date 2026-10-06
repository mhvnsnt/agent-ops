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

## Step 4 — Continue, with checkpointing

- Update your checkpoint as you work:
  - `checkpoint.sh beat <TASK_ID>` at least every 10 minutes during long runs
  - `checkpoint.sh step <TASK_ID> "..."` after each completed unit of work
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
