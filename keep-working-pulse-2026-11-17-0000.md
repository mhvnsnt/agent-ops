# Keep-working pulse — 2026-11-17 00:00 EST

## Moving
- Disk 80% (119G/150G, 31G avail) — below the 85% threshold. Guardian's 00:01 EST run: target NOT reached, nothing safely clearable at scale; every remaining large consumer is dirty/active-lane/tooling/unmirrored.
- Dream Girl 6B lane: gate runner pid 29903 ALIVE, gate log advancing at ~60s cadence (last write 00:02:10 EST, blender PRESENT). 51st successor completed ~23:57 EST (cut short by cron execution timeout in resolve phase); watchdog owns the 52nd spawn.
- W10 FSMP finisher (c4932b65), Mae knee-black-patch lane (1afc6dd7) — running, activity seconds ago.
- Overnight pipeline: 04:44Z run started 23:44 EST, mid-run at pulse time. Previous 22:44Z run verified 8 PPWA PRs landed (#219–#226: W18C joints-fans, secondary controllers, W17 physics roll-out, presets path fix, W17 knee-fix #223, W10 FSMP #224, P1 served-Megami repair #225, W10 FSMP hook fix #226). New queue item PPWA #227 (canon PR, checks unreadable + Vercel pending). Queue: 70 open, 16 blocked >72h carried.
- Dreamgirl-dark-feminine delta pull-back RUNNING (pullback-r5.sh pid 68292 + curl downloading part-09 to the 150G disk, per guardian 00:01 log). Blender proof renders live (megami-v25, pids 74980/74997).

## NEW — needs attention (flagged, not actionable from this run)
1. **Pokemon wave-1 pull-back verification STALLED** (guardian 00:01 log): `gh release download` pid 62097 gone; PokePark 2 rvz stuck at 884,805,632 bytes since 23:43:53 EST (expected ~951M, incomplete). Cause: /var/tmp tmpfs 100% FULL (2.0G used, 0 avail) — /var/tmp/bl524 holds a 1.2G extracted Blender 5.2.4 install + pb-pokemon 844M. Guardian did NOT delete bl524: cut001r gate (pid 29903) is alive and may reference it; /var/tmp is tmpfs, not the 150G disk. Partial rvz NOT deleted, download NOT restarted (lane-owned verification; `gh release download` does not resume partials — a restart re-pulls 951M). The release itself is verified on the store (mhvnsnt/pokemon-arena-3d, 4 assets); only the local pull-back check is stalled. Watch item for the lane owner: free tmpfs once the cut001r gate exits, or point the pull-back at the 150G disk, then re-run verification.
2. **V25 elbow successor (a6fe0030) went quiet**: last activity ~70 min ago (was "seconds ago" at the 22:50 pulse). Chat-owned (3bbcfe70) — cannot resume from a scheduled run. Flag for the parent chat.
3. **Megami proof-quality lane (d8fdd131) went quiet**: last activity ~39 min (was ~18 min at 22:50). Chat-owned — cannot resume from here. Flag for the parent chat.
4. **ROUND-6 disk-staging coordinator (26960c5d) still stale**: checkpoint last write 21:44 EST (~2h20m), agent last activity ~3h. Upload side now quiet (no upload-part.sh alive at 00:02; the quiet1 worker uploading part-19 at 22:50 is gone), pull-back side still active (see above). Same call as prior pulses: no duplicate spawn — chat-owned, pipeline between phases, only the coordinator's own checkpoint is quiet.

## Already-handled failures (no action)
- V25 elbow predecessor (7a8714a7) failed on sqlx pool timeout — successor a6fe0030 already running (now quiet, see #2).
- W10 predecessor (80c78761) died in a daemon restart — finisher c4932b65 already running, active.

## Carried stale lanes (unchanged, flagged in prior pulses)
- Bun-refinement lane (6e749d83, chat 3bbcfe70): last activity Nov 14 21:56 (~50h idle).
- Wizard Gang coordinator (8cc21457, chat 7d0fd043): last activity Nov 13 18:00 (~78h idle).
- Two older stored entries (c01c7d1a, adc07ec6): idle for weeks.

## PRs
- DG #91 (canon-sync): still OPEN, MERGEABLE, UNSTABLE, updated 23:01 EST — DG CI validate red on main (pre-existing). Needs a fix/review before merge. Unchanged in substance since 22:20.
- PPWA #227 (canon-sync-20261117): NEW, mergeable=true, checks unreadable (403) + Vercel pending, NOT merged.
- Overnight pipeline: no green+mergeable non-draft non-excluded PR at last sweep. 16 blocked >72h carried unchanged.

## Grokbot
No new proof file in ~/workspace/agent-ops/. GROK_CAPABILITY_STUDY.md (Oct 8) and HOW-GROKBOT-WORKS.md (Nov 6) unchanged; grokbot-handoffs/ has no new items; proofs/ newest is Nov 3.
