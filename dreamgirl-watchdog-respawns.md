# Dream Girl Lane Watchdog — Respawn Ledger
Purpose: close the race window that caused the 2026-11-12 Janae beats2 double-spawn.
A successor spawned by one watchdog run can still be pending_init / invisible in
subagent.list when the next 5-min run checks. Future runs: read this ledger BEFORE
spawning and do NOT respawn a workdir listed here as in-flight unless its agent
shows done/interrupted/failed AND its checkpoint still says work is owed.

## In-flight respawns
- 2026-11-12 20:22 CT — Janae intro beats ROUND 2, workdir ~/workspace/_janae-intro-beats2-20261112/, original d7b07c34 (interrupted). Successor 5028d6bc. COMPLETED 02:54 CT (stopped on collision with 618a1934, a second successor spawned 42s later by the next watchdog run). Nothing staged; parent decision pending on which clip set stands. Do NOT respawn this workdir without the parent decision.
- 2026-11-12 20:22 CT — Ozzie transformation, workdir ~/workspace/_ozzie-transformation-20261112/, original 94b55d51 (failed). Successor 37e55cfd. Still running as of 02:54 CT.
