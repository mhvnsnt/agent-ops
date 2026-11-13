# M. Engine supervisor dies ~every 2 h — diagnosis from its own log

- **Date:** 2026-11-12 ~22:20 CST (continuous-friction-research pass)
- **Index:** [[RESEARCH-PULLIN-INDEX]] (entry to be added by the merge lane)
- **Status:** diagnosed from the live log + code; fix recommended, not applied
  (the supervisor is M. Engine's live daemon and the watchdog owns it —
  a research pass does not restart or rewire a healthy-by-design daemon).
- **Dedupe:** restart supervision was researched 2026-10-28
  (`research-friction-20261028/02-restart-supervision.md`), which queued the
  scheduler-watchdog + relaunch-script pattern. This doc is NOT that: it is
  a diagnosis of one specific daemon's death pattern from its own log,
  which no prior pass had read.

## TL;DR

The M. Engine supervisor (`node server.js --port 8771`) has restarted
**300 times lifetime** (log count 2026-11-12). On 2026-11-12 it died
~10 times, roughly every 2 h, in two distinct modes:

- **166 lifetime graceful SIGTERM shutdowns** — the process catches SIGTERM,
  logs "supervisor shutting down (SIGTERM)", exits 0. Something sends it
  SIGTERM. It is NOT the watchdog: the watchdog's kill path ("PID alive but
  /health unreachable — restarting") appears only **4 times lifetime**
  (last 2026-11-10).
- **207 lifetime silent vanishes** — the PID file goes stale with no
  shutdown line at all. The process died without handling a signal
  (SIGKILL, OOM-kill, cell restart, or power loss).

The watchdog recovers it within ~5 min every time and the registry holds
0 workers, so nothing is lost — this is a health nuisance and an
observability gap, not a data-loss event. But 300 restarts with no
identified sender means the next real failure will also be unexplained.

## 1. Evidence (live log, `M.-Engine-/tools/supervisor/supervisor.log`)

| Fact | Value |
|---|---|
| "starting M. Engine supervisor" lines | 300 (lifetime) |
| "supervisor shutting down (SIGTERM)" lines | 166 (lifetime; each appears twice — the handler logs twice, a duplicate-log bug, not two signals) |
| "supervisor PID file stale (PID … not alive)" lines | 207 (lifetime) |
| "PID alive but /health unreachable — restarting" (watchdog kill) | 4 (lifetime; last 2026-11-10) |
| "ERROR: supervisor failed to start" | 6 (all Oct 19–21, none since) |
| Deaths on 2026-11-12 (UTC) | SIGTERM 09:28, 11:28, 13:48, 15:31, 19:30; stale-PID found 17:31, 19:23, 22:03, 00:04, 02:23 — roughly every 2 h, with one 7-minute outlier (restarted 19:23:53, SIGTERM 19:30:45) |
| Registry | 0 workers at every restart — nothing to lose, nothing to recover |

The 19:23→19:30 pair breaks any strictly-periodic theory: one instance
lived ~7 minutes. Deaths are mostly ~2 h apart but irregular — consistent
with an external lifecycle event (cell/VM recycle) plus an occasional fast
kill, not with a timer inside the supervisor.

## 2. What the code says

`watchdog.sh` (runs from cron every 5 min): checks PID file + `/health`;
restarts with `nohup node server.js --port "$PORT" >> "$LOG" 2>&1 &` +
`disown`. `nohup` blocks SIGHUP only — it does NOT protect against
SIGTERM, and it does NOT move the process into a new session. The
supervisor therefore stays in the cron exec session's process group.

`server.js` (408 lines): has SIGTERM/SIGINT handlers that log and
`process.exit(0)`; no self-termination timer, no idle shutdown, no
`setTimeout` exit. The only `process.kill(..., 'SIGTERM')` in the file
(line 194) targets *worker* PIDs, never itself. Nothing in the code
kills the supervisor on a schedule.

## 3. Candidate causes, ranked

| Cause | Fits? | Notes |
|---|---|---|
| VM/cell restart | ✅ fits the silent vanishes | Known restarts: 2026-10-26 15:12Z (killed all lanes), 2026-10-28 02:31 UTC, 2026-11-11 ~23:32 CST, 2026-11-12 ~20:22 CST. The 02:23 UTC Nov 13 restart lines up with the ~20:22 CST VM restart. A cell recycle kills without a shutdown line. |
| Runtime exec-session teardown SIGTERM | ⚠️ partial fit | The supervisor is started from a watchdog cron exec session and never leaves its process group (`nohup` ≠ `setsid`). If the runtime SIGTERMs a session's process group when the session ends, the supervisor would die — but it lives ~2 h, not minutes, so session teardown is not the usual killer. It remains a suspect for the fast (7-minute) death. |
| OOM-kill (SIGKILL) | ⚠️ unproven | VM has 6 GB shared; the supervisor is a small Node process with 0 workers. No OOM evidence in the log (no dmesg access from this cell to confirm). Fits the silent mode, but the process is too small to be the likely victim. |
| Watchdog health-kill | ❌ ruled out | Only 4 occurrences lifetime; the log line would precede the SIGTERM. None precedes the Nov 12 deaths. |
| Another cron / lane killing node processes | ❓ unproven | No evidence in the log either way. Worth one grep of the cron/schedule list for `pkill node` / `kill.*8771` — a 2-minute check for the M. Engine owner. |

Honest verdict: **the sender is not identified from the log alone.**
Two death modes + ~2 h cadence + one 7-minute outlier point at an
external lifecycle event (cell recycle) as the main killer, with session
teardown as the secondary suspect. The log as it stands cannot
distinguish them — it records the death, not the killer.

## 4. Recommended fix (M. Engine owner applies; not done here)

1. **Detach properly:** start the supervisor with `setsid nohup node
   server.js …` so it leaves the cron session's process group entirely.
   One-word change in `watchdog.sh`; removes the session-teardown suspect
   for good. If deaths stop, that was the killer; if they continue at the
   same cadence, it is the cell.
2. **Log the killer's fingerprint:** on each watchdog restart, record
   the dead PID's last-seen time, the death mode (SIGTERM-logged vs
   stale), and the supervisor's uptime (`/health` returns `uptimeSec` —
   capture it before declaring dead). Correlate death times with the
   known VM-restart times in the daily memory log. Two weeks of that
   table settles cell-vs-session.
3. **Fix the duplicate log line:** the SIGTERM handler logs twice per
   shutdown (two identical lines, same timestamp) — the handler is
   registered twice or the log call is duplicated. Cosmetic, but it
   inflates every count by 2× and confused this diagnosis until noticed.
4. **Do NOT add a second watchdog or a restart loop inside the
   supervisor** — the outer cron→watchdog→supervisor chain already
   recovers in ≤5 min, and a second recovery loop is how you get
   duelling restarts. The 2026-10-28 research already excluded
   supervisord/s6/systemd for the same reason (no init to root in).

## 5. Blocked / not done here

- No watchdog.sh or server.js change made (live daemon, owner lane).
- No `setsid` test run (would restart the live supervisor).
- No dmesg/OOM confirmation (no access from this cell).
- No cron-list grep for a node-killer (left for the owner; 2-minute check).
