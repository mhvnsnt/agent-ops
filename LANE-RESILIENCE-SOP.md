# Lane Resilience SOP — the at-least-once contract for lane authors

Owner order 2026-10-19 ~23:33 CDT, pull-in 5/6 (lane resilience).
Research: `research-friction-20261019/04-lane-resilience.md`.
Companions: `CHECKPOINT_PROTOCOL.md` (schema), `IDEMPOTENCY.md` (write rules),
`RESUME_BRIEF_TEMPLATE.md` (resume flow).

## The delivery model — say it once, plainly

**Lane resume is at-least-once with idempotent work units. Exactly-once is
not achievable and nobody here has it.** A resumed worker *may* re-run a
step; the system is safe because every step is keyed, its outputs are
deterministic, and its completion is recorded before the next step starts.
Anyone who designs a lane assuming exactly-once rebuilds the duplicate-work
bug. Design for re-execution instead:

1. **Idempotent units.** Every unit of work follows `IDEMPOTENCY.md`:
   outputs named deterministically from inputs, done-manifest checked before
   starting an item, temp-then-rename writes, verify-before-retry on
   irreversible actions (push / publish / send / delete).
2. **Step keys.** `checkpoint.sh step` records a stable `step_key`
   (sha256 of `task_id + step text`) in the checkpoint and in the append-only
   journal `checkpoints/<task_id>.journal.jsonl`. On resume, the keys — not
   prose memory — say what already landed.
3. **Ack after work.** Record the step in the checkpoint only *after* the
   work is done and verified. A step recorded before it lands will be
   skipped by the resume — that is lost work, the failure mode at-least-once
   exists to prevent.

## Fencing — claims and epochs

- A checkpoint carries a monotonic `epoch`. `checkpoint.sh claim TASK_ID
  AGENT_ID` atomically bumps it and records `claimed_by` / `claimed_at` /
  `lease_expires_at` (default lease 30 min; `--lease-min` to change).
- **Every (re-)spawned worker claims first**, reads the printed epoch, and
  passes `--epoch N` on every mutating checkpoint write (`step`, `next`,
  `decide`, `block`, `unblock`, `status`, `agent`, `beat`, `path`).
- A write with a stale epoch — or no epoch once the task is claimed — is
  **rejected (exit 3, file untouched)**. This is what stops the nastiest
  resume failure: worker A stalls, the watchdog resumes the task as worker
  B, B finishes, then A wakes and overwrites B's state. A lease alone does
  not stop that; the epoch check at write time does.
- Legacy checkpoints at epoch 0 accept unfenced writes (backward
  compatibility) until their first claim. `beat` does **not** renew the
  lease; re-`claim` to take over/renew (you get a new epoch — use it).

## Liveness is not progress

- `beat` updates **only** `last_heartbeat` (the process existed recently).
- `step` is the **only** command that advances `progress_seq` and
  `last_progress_at`. Beat in long loops, but if no step lands, the lane is
  — correctly — indistinguishable from wedged.
- `supervisor.sh` triage: DEAD/STALE (no heartbeat → re-spawn brief),
  **STUCK** (heartbeat fresh, `progress_seq` frozen across 2 supervisor
  runs → **surfaced, never auto-re-spawned**), HEALTHY. A stuck lane gets a
  parent/human decision: wait, inspect, or claim + manual re-spawn (fencing
  makes that safe). Never wire an auto-respawn to STUCK.
- Ad-hoc supervisor runs should pass `--no-track` so they don't consume the
  tick cadence the watchdog relies on.

## Watchdog wiring

- The worker-watchdog cron (15m) runs `supervisor.sh --json` in its
  reality-check step: STUCK tasks are reported to the owner as stuck lanes;
  they are not resumed by the watchdog. DEAD/STALE tasks keep the existing
  claim-then-resume flow: claim first, put the epoch in the resume brief.
- Watchdog-schema checkpoints (`ckpt.sh`, `"watchdog": true`) predate this
  schema. supervisor.sh derives a best-effort progress proxy (recorded step
  count) for foreign schemas, but new lanes should use `checkpoint.sh` —
  the canonical schema — so fencing and progress are first-class.

## Not adopted (and why)

- systemd user units: verified unavailable on this VM (no user bus).
- supervisord / s6 / runit: the cron keepalive already covers the 90% case;
  revisit past ~3 long-lived daemons.
- Temporal / DBOS: need a server/Postgres we don't run, and lanes are agent
  sessions, not SDK processes. Their semantics are imported as the patterns
  above — that is the pull-in.
- Hosted dead-man's-switch services: implemented locally instead (the
  watchdog writes an ok-ping; the disk guardian alerts if it goes stale) —
  lane metadata never leaves the box. *(Ping wiring is tracked in the
  research doc as W4 remainder, CloudDog lane.)*
