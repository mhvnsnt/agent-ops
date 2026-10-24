# agent-ops — restart resilience for agent work

The machine/daemon restarts without warning and kills running workers.
**This system cannot stop that.** It makes restarts survivable: workers
checkpoint as they go, and after a restart the supervisor tells the parent
agent exactly what died and how to re-spawn it.

## Files

| File | Purpose |
|---|---|
| `checkpoint.sh` | Worker checkpointing CLI (canonical tool) |
| `supervisor.sh` | Post-restart triage: flags stale/dead tasks, prints re-spawn briefs |
| `CHECKPOINT_PROTOCOL.md` | The schema + rules workers follow |
| `RESUME_BRIEF_TEMPLATE.md` | What a re-spawned worker must do, step by step |
| `IDEMPOTENCY.md` | How to write work so re-runs can't duplicate or corrupt it |
| `docs/MERGE-IT-YOURSELF-LAW.md` | Canonical owner law: merge clean green PRs yourself, never leave them for the owner |
| `checkpoints/` | One JSON per task: `<task_id>.json` |
| `attic/` | Deprecated alternate tooling (reference only) |

## For the parent agent

**Spawning a worker on a long task** — include this in the brief:

> Checkpoint your progress with `~/workspace/agent-ops/checkpoint.sh`:
> `init` first with `--goal` and `--resume-prompt`, then `beat` every
> ~10 min and `step` after each unit of work. Read
> `~/workspace/agent-ops/IDEMPOTENCY.md` and follow it.

**After a restart** — run the supervisor:

```
~/workspace/agent-ops/supervisor.sh            # stale threshold: 30 min
~/workspace/agent-ops/supervisor.sh --stale-minutes 10
```

It prints a ready-to-paste re-spawn brief per dead task. Paste each into a
fresh subagent. The brief tells the worker to read its checkpoint and the
resume template — not to redo completed steps.

## For workers

1. First action: `checkpoint.sh init <task_id> --goal "..." --resume-prompt "..."`.
2. Work in units. After each unit: `checkpoint.sh step <task_id> "what you did"`.
3. Long silent stretches: `checkpoint.sh beat <task_id>` every ~10 min.
4. Decisions the next worker must honor: `checkpoint.sh decide <task_id> "..."`.
5. Blocked: `checkpoint.sh block <task_id> "why"`. Unblocked: `unblock`.
6. Done: `checkpoint.sh status <task_id> completed`.

Write outputs per `IDEMPOTENCY.md` (deterministic names, done-manifests,
temp-then-move, no force-pushes).

## Honest limits

- Heartbeat staleness is a heuristic. A worker inside one long tool call can
  look stale while alive; a dead worker can look fresh if it beat right before
  dying. The supervisor **reports**; the parent agent decides.
- Checkpoints live on this machine's disk. If the whole VM is wiped (not just
  restarted), checkpoints die with it — which is why important work also gets
  committed to its repo early and often.
- A re-spawned worker must still **verify** checkpoint claims against reality
  (files exist? repo state matches?) before continuing. Trust, then verify.

## Muse training pack
Muse/Ashes and every agent: read the [Muse training pack](https://github.com/mhvnsnt/money-machine-hq/tree/main/docs/muse-training-pack) (instructions, pre-flight checklist, real before/after examples, right-way videos) before every job.
