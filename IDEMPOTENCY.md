# Idempotency Rules — write work so a re-run can't duplicate or corrupt it

Restart-resilience only works if resumed work doesn't trample itself.
These rules are for every worker doing multi-step or batch work.

## 1. Outputs are keyed by input, not by run

- Name output files deterministically from their inputs
  (e.g. `judas-classic.webp` from `JUDAS_classic.glb`, never `output-3.webp`).
- A re-run of the same step must produce the same filename. If the file
  already exists and is valid, skip the step.

## 2. Keep a done-manifest for batch work

For any loop over N items (cards, models, clips, files), maintain a manifest
next to the outputs, e.g. `~/workspace/<task>/done.json`:

```json
{ "completed": ["judas-classic", "judas-painmaker"], "failed": [] }
```

- Check the manifest before starting each item. Skip completed ones.
- Append to the manifest AFTER the item's outputs are fully written and verified.
- The manifest is the resume point. The checkpoint's `steps_completed`
  is the human-readable summary; the manifest is the machine truth.

## 3. Write temp, then move

- Never write directly over a final output path. Write to
  `<output>.tmp-<pid>` then `os.replace()` / `mv` into place.
- A restart mid-write leaves a `.tmp` file, never a half-written final file.
- On resume, delete stale `*.tmp-*` files before starting.

## 4. Git is a checkpoint too

- Commit working states on natural boundaries (per character, per batch).
  `git log` is a second resume source if the JSON checkpoint is lost.
- Before pushing, check `git log origin/<branch> --oneline -5` — if your
  commits are already there, don't push again.
- Never `git push --force` from a resumed worker. If history diverged,
  stop and report.

## 5. Separate scratch per task

- Each task gets its own working directory: `~/workspace/<task-slug>/`.
- Never share scratch paths between tasks. Two workers writing to `/tmp/x`
  will corrupt each other after a restart reshuffles scheduling.
- Ephemeral intermediates go in the task dir, not `/tmp`, unless they are
  truly disposable single-command artifacts.

## 6. Record-then-act for irreversible steps

For anything irreversible (push, publish, send, delete):
1. Verify the precondition (does the remote already have it?).
2. Do the action.
3. Record it in the checkpoint (`step`) AND the done-manifest immediately.

If the restart lands between 2 and 3, the resume verification in
`RESUME_BRIEF_TEMPLATE.md` step 3 catches it — which is why step 1 matters.

## 7. Heartbeats during long loops

- `checkpoint.sh beat <TASK_ID>` at least every 10 minutes.
- In batch loops, beat (or record a `step`) after each item, not just at the end.
- A 3-hour batch with one checkpoint at the end is the same as no checkpoint.

## 8. Decisions go in the checkpoint, not just chat

Anything the parent/user decided mid-task ("keep all attires", "use X not Y")
goes in `checkpoint.sh decide`. Chat history does not survive a restart;
the checkpoint file does.
