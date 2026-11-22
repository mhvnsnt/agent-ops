# CUT 001R — 6B lane — VM RESTART LOSS RECORD (2026-11-15)

**Written by the eleventh-successor watcher after the VM restarted mid-watch.
This file is the durable resume record. The live checkpoint
(`CHECKPOINT-ADDENDUM-6B-10TH.md`) lived ONLY in /var/tmp + a /tmp mirror —
both tmpfs, both wiped. Do not keep checkpoints or render output on tmpfs again.**

## What happened

- ~18:57 UTC (13:57 EST) the watcher sleep-check command (proc_d21c4a100695)
  was killed by SIGTERM (exitSignal 15). Its checkpoint append + mirror had
  completed ("mirrored"); only the sleep + status check was lost.
- ~19:00 UTC the VM was confirmed restarted: `uptime` = 2 min, load 9.10,
  `/var/tmp` 0% used (2.0G free), `/tmp` wiped. Both are tmpfs.
- Waiter v4 pid 20553 DEAD. Blender pid 42235 DEAD. No Blender process remains.
- `/var/tmp/cut001r/` is GONE in full: gate_and_run_6b.sh, gate log,
  step1_character.log, step2_fx.log, layers/character (69 frames),
  layers/fx, comp_frames, probe frames, checkpoint addendum. NOTHING of the
  6B run survives on disk.

## Last known good state (verified by own-eyes checks)

- 13:10 EST (18:09 UTC): step 1 character pass 43/96 frames (f43 saved 29:39
  into render, ~41s/frame). MemAvailable 2,837,532 kB. /var/tmp 726M free.
- 13:30 EST (18:28 UTC): step 1 at 66/96 (f66 saved 47:44). MemAvailable
  1,656,336 kB (dip under render load, normal). /var/tmp 65%, 726M free.
- 13:38 EST (18:38 UTC): step 1 at 69/96 (f69 saved 55:41). MemAvailable
  2,262,284 kB. Pace note: f43->f66 ~47s/frame long-run, but f66->f69 took
  ~7:57 for 3 frames (~159s/frame) — possible slowdown, unconfirmed.
- Step 0 probe DONE before step 1: frames f61 + f80 rendered; gate log showed
  `STEP 0 probe DONE`, `GATE READY (step1) mem=4516388kB`, `STEP 1 character
  pass 96f starting` at 2026-11-15T17:39:31Z.
- fx 0/96, comp 0/96 throughout. No DONE/FAILED marker ever appeared.
- Earlier interrupted command proc_3df6d36cfd60 (runtime restart ~18:38 UTC):
  its append + mirror DID complete; only its sleep/check was lost. No
  duplicate entries were made. Its exec log survives at
  `~/workspace/agents/43404bb7-7bef-4e98-899c-345879701400/exec-logs/proc_3df6d36cfd60.log`.

## What survives (durable disk, /home/hatch — 122G used / 28G free, 82%)

- `~/workspace/dream-girl` repo, branch `cuts/001r-002r-production`
  (episodes/ep01/cut001r-002r/ — layer map, hybrid method, drawing counts,
  transition timesheet, transition frames). Last commits are transition work,
  not the 6B render.
- `~/workspace/_deepwire-cut001r-20261111/` — earlier 001R render scripts
  (cut001r_render.py, assemble_fixed.py), outputs/cut001r-tammy-idle-96f.mp4,
  frames, CHECKPOINT.md (no mention of 6B/gate_and_run).
- `~/workspace/_cut001r-gate/` — cut001r-tammy-idle-96f.mp4, frame-00.png,
  frame-blink.png, frame-end.png.
- `~/workspace/_cut001r-redo-20261111/`, `~/workspace/_cut001r-gate-20261111/`.

## What is LOST and must be reconstructed to resume

1. **All 69 rendered character frames** — no copy on durable disk found.
   (Not verified whether any were pushed to a repo/release — check before
   assuming a full re-render is needed.)
2. **gate_and_run_6b.sh + step scripts** — not found in the dream-girl repo
   or workspace by quick search. The 6B lane's exact blend file, render
   command, and gating parameters are UNKNOWN from surviving records.
3. **The checkpoint addendum history** — this file + the check summaries
   above are the only record of the 6B run's progress.

## Resume steps for the successor lane

1. Find the 6B lane's source: its blend, scripts, and branch (ask the parent
   / check lane handoffs — NOT in the locations searched above).
2. Verify whether any step-1 frames were staged to a repo/Release/TeraBox
   before the restart; if yes, resume from frame 70. If no, re-render step 1
   from frame 1 (96f character pass, then step 2 FX, then comp).
3. Re-create the waiter/gating from the recorded gate behavior (3x quiet
   checks, mem gate ~4.5GB, step sequencing in the gate log lines above).
4. Keep ALL checkpoints, scripts, and render output on durable disk
   (~/workspace or the repo branch) with incremental pushes — NEVER /var/tmp
   or /tmp alone. tmpfs does not survive a VM restart; this loss is the proof.
5. Re-establish the watch: 20-minute checks, checkpoint after every check.

## Open questions for the parent

- Where did the 6B lane's blend + gate_and_run_6b.sh come from? (Not in the
  surviving workspace locations searched.)
- Were any step-1 frames pushed anywhere before the restart?
- Should the 6B render restart from scratch, or is there a newer/better
  route (the 13:38 pace slowdown was unconfirmed)?

## CORRECTION — QUALITY LOOP RUN 126 (2026-11-15 ~14:30 EST, evaluator 0a15250d)
- The "inputs not identifiable / blend+scripts UNKNOWN" claim above is WRONG. Verified own-eyes: the full 6B prep survives on home disk in `~/workspace/_dg-production-line-v4-20261114/cut001r-proof/` — `cut001r_v2_blinkfix.blend` (133,161 B), `render_character_pass.py`, `merge_fx_stars.py`, `COMPOSITE-DRIVER.sh`, `GATE-CLAIMS-DRAFT.md`, `HEAD_CLOSED_TRUE.png`, `evidence/` (blinkfix f73/f80/f85), `layers/` (bg_001r_1920.png, book/ 96 stills, stars_1920.png). The 11th successor searched the dream-girl repo and `_deepwire`/`_cut001r-gate` dirs but missed the production-line workdir.
- Genuinely lost: only `gate_and_run_6b.sh` itself (lived only in `/var/tmp/cut001r/`); reconstructible from the checkpoint's recorded gate behavior.
- Open question #1 above ("where did the blend + gate script come from?") is therefore ANSWERED. Question #2 (were any frames pushed anywhere?) remains open — no 6B frames found staged to any branch.
- 12th successor already rebuilding (observed 19:27–19:28 UTC): Blender 5.2.4 downloading to /var/tmp/bl524, /var/tmp/cut001r/ recreated with the _6b run scripts. Do NOT spawn a duplicate.
