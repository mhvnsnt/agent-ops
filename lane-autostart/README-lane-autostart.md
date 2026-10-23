# lane-autostart — restart-resilient lane supervisor (research task B, 2026-10-22)

Design proposal only. Nothing is scheduled, no lanes are registered, nothing
has been installed. See `CRONTAB-TEMPLATE.txt` for the wiring options (all
need owner approval).

## The problem

Long-lived lane processes die when the VM runtime restarts — and so do their
watchdogs (tonight: one lane died ~9 times; its own watchdog went absent too).
Prior research (cluster 04, 2026-10-19) skipped heavier supervisors because
"PID-file + keepalive cron covers the 90% case" — but that assumed the
supervisor survives. It doesn't always. This design makes the supervisor
restart-resilient instead of making it heavier.

Key environment facts verified on THIS VM (2026-10-22, not from training data):
- `systemd` user units unavailable ("Failed to connect to bus" — cluster 04).
- **No local cron daemon at all**: no `cron`/`crond` binary, no `/etc/crontab`,
  no crond process. The scheduler cron that runs the friction-research task
  is the runtime's, and it DOES survive restarts.
- `flock`, `setsid`, `nohup` all present (`flock from util-linux 2.39.3`).

## Research findings (live sources, 2026-10-22)

### 1. cron @reboot reliability

- `@reboot` fires **once per boot** via a marker file in `/run` (a tmpfs):
  `/run/cron.reboot` on cronie, `/run/crond.reboot` on Debian cron. Because
  `/run` is emptied at boot, a plain `service cron restart` does NOT re-fire
  `@reboot` jobs (older Vixie cron had a bug where restarts re-fired them —
  fixed upstream, Red Hat BZ#476972). Source:
  https://runwisp.com/blog/cron-reboot/ (crawled 2026-10-22, with a
  distro×daemon behavior table) and
  https://docs.redhat.com/pt-br/documentation/Red_Hat_Enterprise_Linux/5/html/5.8_technical_notes/vixie-cron
- `@reboot` does **not** wait for the network — anything network-dependent
  must retry internally. Same source.
- Gotchas that apply to anything launched from cron/@reboot: **no login
  shell, skeletal env** (typically `PATH=/usr/bin:/bin`), so set `PATH`/`SHELL`
  in the crontab and use absolute paths in scripts. Source:
  https://copyprogramming.com/t/run-shell-scripts-on-linux-boot-with-crontab
- Related: Debian cron and cronie start the next scheduled run even if the
  previous is still running; the canonical fix is `flock` per line. (BusyBox
  crond instead refuses to overlap.) Source:
  https://runwisp.com/blog/cron-implementations/

Verdict: `@reboot` is fine as a one-shot *supplement* (needs a local cron
daemon installed first — approval required), but it can never be the whole
supervisor: one shot at boot, no coverage for lanes that die later. The
every-5-min scheduler run is the real supervisor.

### 2. flock(1)-based leader election / single-instance autostart

- `flock(2)` locks are attached to the **open file table entry**, not the
  path. They are released when the holder's descriptors close — which the
  kernel does on process death and, obviously, on reboot. Quote: "If a lock
  is not held by any open file descriptors, you can always take it."
  Source: https://yakking.branchable.com/posts/flocking/
- "When the process is terminated, all the file locks established by him
  will be released, and ... flock will also be the same."
  Source: https://topic.alibabacloud.com/a/differences-between-fcntl--lockf-and-flock-in-linux-_-php-tutorial_1_34_33165537.html
- This is why `flock` beats PID-files across reboots: a stale PID-file can
  outlive a reboot and falsely block restart (classic trap discussed at
  https://community.unix.com/t/use-of-flock-command-for-whole-script/362747),
  while a stale *lock file* is harmless — the lock is gone, `flock -n`
  succeeds.
- Canonical pattern used in the design: `flock -n -E <code> <lockfile> <cmd>`
  — non-blocking; exactly one winner in a race, lock held for the command's
  whole lifetime. Options reference:
  http://www.tutorialspoint.com/unix_commands/flock.htm

Verdict: confirmed, no stale-lock hazard after unclean reboot. This is the
liveness authority in the design.

### 3. nohup / setsid daemonization for cron-launched lanes

- `nohup` = ignore `SIGHUP`, redirect output (default `nohup.out`), detach
  stdin. It does NOT detach from the terminal/session.
  Source: https://linuxize.com/post/linux-nohup-command/
- `setsid` = new session, **no controlling terminal at all** — SIGHUP from a
  TTY can never reach it. The util-linux `setsid(1)` forks when the caller
  is a process-group leader, so `setsid cmd` is safe from scripts.
  Sources: https://dev.to/gabrielanhaia/closing-a-terminal-sends-your-coding-agent-sighup-how-session-hosts-keep-it-alive-2p7j
  and https://www.ibm.com/support/pages/nohup-or-setsid-keep-process-running-after-user-disconnect
  (which calls setsid more reliable than nohup for keeping work alive).
- From a cron/scheduler launcher there is no TTY anyway; the design still
  uses `setsid` + `</dev/null` + explicit log redirects + `env -i` with an
  explicit PATH for full determinism.

Verdict: `setsid` + explicit redirects is the right launch primitive; `nohup`
is unnecessary here (kept as reference).

### 4. Lightweight supervisor alternatives — license + verdict

| Candidate | License (verified) | Verdict |
|---|---|---|
| supervisord | BSD-style (mature, ~27MB RSS) — https://www.webcodingcenter.com/linux/process-monitoring-and-keeping-programs-alive--pm2-a-systemd-unit-or-supervisord-choosing-one.html ; activity "Maintenance" per https://dev.to/empellio/process-manager-comparison-2026-pm2-systemd-supervisor-oxmgr-and-more-4e0p | **SKIP** — it must itself be bootstrapped after reboot (normally via a systemd unit, which is absent here). Adding a Python daemon does not solve the bootstrap problem; the flock + scheduler design covers it cheaper. |
| circus (circusd) | Apache 2.0, status "Maintenance" — same dev.to comparison | **SKIP** — declining maintenance, same bootstrap gap. |
| honcho / foreman | MIT (both) | **SKIP** — Procfile runners; no crash autorestart (a dead process just exits the runner). Not a supervisor. |
| overmind | MIT — https://pkg.go.dev/github.com/kris-libis/overmind@v1.0.3 ("Overmind is licensed under the MIT license") | **SKIP** — tmux-based *dev* session manager; dies with the tmux server, not a daemon supervisor. |
| s6 | ISC (skarnet suite) | **SKIP** — real supervision requires rooting the tree in PID 1 (https://git.skarnet.org/lists/supervision/1791.html); anything less is "probabilistic". Cost/complexity vs benefit unchanged since cluster 04. |
| runit | (not re-litigated) | **SKIP** — same PID-1/root argument as s6. |

No genuinely new evidence overturns cluster 04's cost/benefit skip. One NEW
data point worth tracking (not pulling in): **RunWisp** — an open-source,
single-binary cron replacement whose tasks support `run_on_start = "boot"`
(once per machine boot, tracked by boot ID, with retries). Mentioned at
https://runwisp.com/blog/cron-reboot/. Treat as vendor-promotional for now;
candidate for future evaluation only if the flock+scheduler design proves
insufficient. No dependency added today.

## Files in this directory

- `lane-autostart.sh` — the supervisor script (idempotent; safe to run by hand).
- `lanes.manifest` — lane registry; all lanes ship DISABLED.
- `CRONTAB-TEMPLATE.txt` — wiring options (scheduler cron recommended; @reboot
  template needs a local cron daemon installed first).
- `README-lane-autostart.md` — this file.

## Needs OWNER APPROVAL

1. Creating the scheduler-level cron job (every 5 min) that runs
   `lane-autostart.sh` — this is a durable scheduled-work change (main-agent
   `cron.add` capability). This is the recommended wiring.
2. Installing a local cron daemon (cronie/Debian cron via apt, needs root)
   if the @reboot supplement is ever wanted. NOT required for option 1.
3. Registering any actual lane in `lanes.manifest` (name, command, watchdog,
   restart cap) — flips work from "design" to "supervised".
