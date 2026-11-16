# Stage-as-it-lands: tmpfs render-output loss (001R 6B, twice)

- **Date:** 2026-11-15 ~23:15 EST (continuous-friction-research pass)
- **Index:** [[RESEARCH-PULLIN-INDEX]] (entry added by this pass)
- **Status:** researched + two tools wired and tested (see below); lane adoption queued
- **Dedupe:** `research-check.sh "tmpfs"` — only prior hits are the loss record
  itself (`CUT001R-6B-VM-RESTART-LOSS-20261115.md`), the 2026-11-09 note that
  "/tmp is a 512 MB tmpfs — never stage transfers there", and the 2026-10-19
  resilient-transfer cluster (gh retry, 100 MB standard — different problem).
  No prior pass built a stager or an output-path guard. `research-check.sh
  "stage-as-it-lands"` — zero hits. This is new.

## TL;DR

The Dream Girl 001R 6B render lost 69 finished character frames **twice** on
2026-11-15 because its output dir was `/var/tmp/cut001r` — tmpfs, wiped on
every VM restart. The owner rule since then is "stage finished pieces as
they land", but no tool enforces it: the re-render rebuilt in `/var/tmp`
**again the same night**, and Blender 5.2.4 itself (1.2 GB download) sits on
tmpfs too. Two zero-drama tools close the gap:

- **`tmpfs-guard.sh`** — refuses (exit 2) any output path on tmpfs. Render
  scripts call it on their OUT dir before frame one.
- **`stage-as-it-lands.sh`** — watches an output dir and runs the lane's
  stage command on each file the moment its size goes stable, with a
  restart-safe state file. Polling, zero dependencies.
- **`entr` 5.9 (ISC)** — built from source on this VM and installed at
  `~/.local/bin/entr`: the event-driven upgrade for lanes that want it.
  **Operational catch found in testing: entr needs `-n` in non-TTY sessions**
  (all our exec/cron sessions); without it, it dies with "unable to get
  terminal attributes".

## 1. Evidence (live, this pass)

| Fact | Value |
|---|---|
| /tmp | tmpfs, 512 MB, 67% used at 23:06 EST |
| /var/tmp | tmpfs, ~2 GB (wiped on restart; 0% used right after the 20:53 EST restart) |
| 6B loss, round 1 | ~19:00 UTC: VM restart wiped /var/tmp/cut001r — 69 frames, gate script, logs, checkpoint addendum (loss record, §"What happened") |
| 6B loss, round 2 | 19:49–20:00 UTC: full re-render lost the same way (alignment synthesis) |
| Re-render tonight | `gate_and_run_6b.sh` (PID 106385, since 22:24) running, OUT=`/var/tmp/cut001r` — **still tmpfs**. Layers dirs exist, 0 frames yet; gate waiting (mem ~2.1 GB < 3 GB bar, no Blender process). Nothing lost *yet* — the hazard is live, not historical. |
| Blender 5.2.4 | `/var/tmp/bl524/blender-5.2.4-linux-x64/blender` — the binary itself is on tmpfs; next restart re-downloads 1.2 GB. Durable Blender on disk is 4.2.23 in `_cd2-tools/` (guardian log). |
| Gate script's own comment | Line 14: "/var/tmp is tmpfs, NOT durable — staging IS the save." The lane knows; it stages per batch to the dream-girl branch (`stage_batch` to `episodes/ep01/cut001r-proof/layers/character`). What is NOT staged: the gate script itself, its log, and any in-flight batch at restart time. |
| Memory update tonight | Owner rule added 2026-11-14: "any final he approves goes into the repo/releases the SAME day" (after the Cape Jones v2 dance mixes were found lost — local-only, never stored; JP mix recovered from his phone 2026-11-15). Same failure family, third data point. |

## 2. Candidates (license + honest verdict)

| Tool | Source | License (verified) | Verdict |
|---|---|---|---|
| **entr 5.9** | eradman/entr (GitHub, 5,731★, pushed 2026-10-16) | **ISC** (LICENSE file read live; GitHub SPDX field says NOASSERTION, the file text is ISC) | ✅ **WIRED** — built from source on this VM (`./configure` + `make`, cc, no deps), installed at `~/.local/bin/entr`. Smoke-tested: modify listed file → hook runs; `-d` exits on new file (documented). **Requires `-n` in non-TTY sessions** — without it, dies immediately ("unable to get terminal attributes"). Pattern for lanes: `while true; do find "$OUT" -type f \| entr -nd stage-one.sh; done` — `-d` exits when a new file appears, the loop re-lists and stages it. |
| **inotify-tools** (inotifywait) | inotify-tools/inotify-tools | **GPL-2.0** (GitHub API) | 📄 documented, not installed — the `-m -e close_write` streaming form is the ideal stager trigger, but apt is broken on this VM and a source build needs autotools (`autoconf` absent). entr covers the same slot with a plain `cc` build. Revisit only if a lane needs `-m` streaming. |
| **lsyncd** | axkibe/lsyncd | **GPL-2.0** (GitHub API) | ❌ excluded on fit — live-sync daemon (inotify + rsync) built for mirroring trees between hosts; needs **lua** (absent on this VM) and a sync target. Our staging target is a repo/release API call, not rsync to a host. |
| **fswatch** | emcrisostomo/fswatch | **GPL-3.0** (GitHub API) | ❌ excluded on fit — cross-platform watcher, cmake present so a build is plausible, but it is a large C++ build for a job entr (41 KB) already does. No advantage on this box. |
| **Python watchdog** | gorakhargosh/watchdog | **Apache-2.0** (GitHub API) | 📄 documented, not installed — the natural choice for a Python lane (observer API, inotify backend). `pip install --user watchdog` untested this pass (system pip is PEP 668-blocked; `uv` exists at `~/.local/bin/uv`). A lane that wants it installs it; the polling script below needs nothing. |
| **Polling stager (own glue)** | this pass | — (own code) | ✅ **WIRED** — `stage-as-it-lands.sh` (see §3). Polling is deliberate: zero deps, works in every exec/cron session, survives restarts via its state file. Latency is one poll interval (default 5 s) — irrelevant next to ~40 s/frame renders. |
| rclone `--watch`/mount | rclone 1.75.2 (already on box) | MIT | ❌ excluded — rclone has no local→remote watch mode; `copy` is one-shot (and 2026-11-09 proved it does not resume across invocations). It is the transport, not the trigger. |
| syncthing | syncthing/syncthing | MPL-2.0 | ❌ excluded — continuous sync between *peers*; our staging target is a repo/release, and there is no peer to sync to. Wrong shape. |
| git-annex / borg / kopia | — | — | ❌ already excluded 2026-10-19 (per index). Not re-litigated. |

## 3. What was wired + test evidence (this pass, scratch only)

**`tmpfs-guard.sh`** (in this dir) — `stat -f -c %T` with a `df -T`
fallback; checks the nearest existing parent for not-yet-created paths.
Tested live: `/var/tmp` → UNSAFE rc 2; `/tmp` → UNSAFE rc 2;
`~/workspace` → ok (btrfs) rc 0; `/var/tmp/cut001r/not-yet` → UNSAFE rc 2.

**`stage-as-it-lands.sh`** (in this dir) — `--watch DIR --stage CMD`
(`--once` one sweep, `--drain` repeat until quiet, default daemon).
Finished = size unchanged across two polls `--stable` seconds apart;
staged files recorded in a state file (size + mtime + path) so a restart
skips them; a failed stage is retried, never recorded.
Tested end-to-end in scratch with a slow producer (4 × 200 KB files,
written via `.tmp` + rename, 2 s apart) and a copy-and-verify stage
command: **4/4 staged, sha256 match on all 4, second drain staged 0**
(idempotent). Two bugs found *by the test* and fixed in the script:
(1) `--once` is a single sweep, not a drain — documented as such;
(2) `--drain` first exited on its first zero-stage sweep while the
producer was still writing — fixed: drain now stops only when a sweep
stages nothing **and** nothing is still being written.

**`entr` 5.9** — `~/.local/bin/entr` (41 KB, built 23:09 EST from
`eradman/entr` @ 5.9, `./configure` + `make`). Verified: modify listed
file → hook ran; `-d` exit on new file confirmed; bare `entr` in a
non-TTY session dies on terminal attributes — **`-n` is mandatory** in
our sessions (documented in the script header so the next lane does not
re-discover it).

No live lane touched: the 6B gate script (PID 106385) was only read, never
modified, restarted, or killed. No frames staged by this pass (none exist
yet). Scratch test dirs live in `~/workspace/_friction-20261115-scratch/`
(render-out/, durable/, watch-test/) — disposable, not in any repo.

## 4. Recommended (lane owners apply)

1. **6B lane (urgent, while the re-render is still gated):** move Blender
   5.2.4 out of /var/tmp to durable disk (or use the `_cd2-tools` Blender),
   move `gate_and_run_6b.sh` + its log to durable disk (or the dream-girl
   branch — the script is currently tmpfs-only and reconstructible only
   from the checkpoint's recorded gate behavior), and add
   `tmpfs-guard.sh "$OUT" || exit 2` at gate start. The per-batch staging
   already in the gate script is the right pattern — keep it.
2. **Render lanes generally:** adopt `stage-as-it-lands.sh` (daemon mode
   alongside the render, or `--drain` when it finishes) for any output
   the render script does not stage itself; or copy the 6B gate script's
   per-batch staging. Either way, finished pieces leave tmpfs within one
   poll interval.
3. **Checkpoint protocol (agent-ops follow-up):** add an output-path
   tmpfs check at lane start — a lane whose OUT dir fails `tmpfs-guard`
   does not start rendering until the path is fixed. Cheap, kills this
   whole failure class at the root.
4. **entr as the event-driven upgrade:** lanes that want sub-second
   staging latency use the `find | entr -nd` loop pattern from §2; the
   polling script stays the default (no new binary to keep alive).

## 5. Blocked / not done here

- 6B lane changes (owner: the lane is live and gated; its owner moves the
  paths, this pass only researched + built the tools).
- Python `watchdog` install (untested; a lane can `pip install --user` it
  or use `uv`).
- inotify-tools source build (needs autotools; entr covers the slot).
- No VM-restart behavior was changed; /tmp and /var/tmp remain tmpfs by
  design (512 MB / ~2 GB) — the fix is never pointing durable work at
  them, not resizing them.
