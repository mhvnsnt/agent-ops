# merge-law-ci-watch run 2026-10-23 09:30 CDT

total=113 merged_this_run=0 merge_failed=0 still_open=66 already_closed=47 check_errors=0

Open-state breakdown: 62 unstable, 3 blocked (ConcreteDragon#59, BioMechania#26, ConcreteDragon#61), 1 dirty (Physics-sandbox-playground-#5).
All 47 closed PRs verified merged=true via `gh api ... --jq .merged` — zero closed-unmerged in the watch list.

## Merged this run
- none (zero PRs were OPEN + CLEAN)

## Landed since the 04:57 CDT run (8, merged by CI recovery / another lane — not this run)
- mhvnsnt/Bannon#83 — docs: add MERGE-IT-YOURSELF LAW (owner 2026-10-15)
- mhvnsnt/Bannon#88 — docs: land render-orientation method + tpose render tools
- mhvnsnt/game-reverse-engineering#6 — docs: add MERGE-IT-YOURSELF LAW (owner 2026-10-15)
- mhvnsnt/game-reverse-engineering#11 — docs: land render-orientation method + tpose render tools
- mhvnsnt/game-reverse-engineering#13 — ANTI-CLOBBER LAWS (owner 2026-10-17 — the DXMMII 54k-file wipe)
- mhvnsnt/wrestling-game#10 — docs: land render-orientation method + tpose render tools
- mhvnsnt/wrestling-game#12 — ANTI-CLOBBER LAWS (owner 2026-10-17 — the DXMMII 54k-file wipe)
- mhvnsnt/God-Molecule-Show-Studio#31 — CLOBBER RECOVERY: recover 1311 files wiped by e7d67450 (the "most important open PR in the set")

## Merge failed (were CLEAN at check)
- none

## Still OPEN (not CLEAN — left alone)
UNSTABLE (62): agent-ops#27, agent-ops#31, agent-ops#32, money-machine-hq#29, money-machine-hq#31,
AshLanev2#46, AshLanev2#48, Brutal-Fist#32, Brutal-Fist#35, Physics-sandbox-playground-#4, Physics-sandbox-playground-#7,
physics-playground-pwa#20, game-reverse-engineering#6(n/a-merged), AshLane-prototype#6, atlas#13, bolt.diy-M#2,
Forge3D#11, GAME-Emulator#4, Lyra#3, M-Hero-Simulator-#7, M-OS-Daywalker-private#3, M.-Engine-#21,
Mochiichao-Diamond-Version-2d-#3, Moneymachine-private#3, mystery-coast-ghosted#10, Neon-App-Builder#3,
NightSkyEngine#3, QuantumBlur#3, SMOKE-MIRROR-S-#6, SchwarzerblitzEngine#3, TRIPPEDD-Animation-Studio#8,
TRIPPEDD-Production-studios-#272, TRIPPEDD-Production-studios-#274, Tekken3Recompiled-private#3, URBAN-MAYHEM-#9,
Wrestli6game-3#5, animation-research-library#9, blend-physics-playground#10, box-orphans#2, box-storage#3,
brutalfist11#4, brutalfistgrokversion#4, brutalfistgrokversionfour#4, brutalfistgrokversionfive#4,
brutalfistgrokversionsix#4, brutalfistgrokversionseven#4, brutalfistgrokversionten#42, brutalfistgrokversiontenpointfive#4,
brutalfistgrokversionthree#4, brutalfistgrokversiontwo#4, cape-jones#105, chimera-emulator-hub#7, chimera-rom-nomercy#3,
chimera-roms#5, cn-gigaleak-* (19 repos), code-doctor#3, dispossessory-case#4, drive-storage#20, font-wizard#16,
google-drive-repo#6, homefront#3, os-harvest#3, pocket-studio#6, ragdoll-wrestler#8, steal-like-artist-archive#3,
texture-customizer#3, theyard#5, western-heart#235, wizard-gang-storage#5, wizard-gang-voice-pipe#6, wwe-wrestler-models#5
DIRTY (1): Physics-sandbox-playground-#5 (docs: land render-orientation method + tpose render tools)
BLOCKED (3): ConcreteDragon#59, BioMechania#26, ConcreteDragon#61 (all anti-clobber-law docs)

Full per-PR state table: /tmp/ci-rest.tsv (repo, number, "state mergeable_state").

## Notes
- Initial GraphQL check loop (`gh pr view --json mergeStateStatus`) mass-EOF'd: `Post "https://api.github.com/graphql": EOF` on ALL calls in sustained bursts (both backgrounded and foreground chunks), while isolated single calls succeeded and the token's GraphQL rate limit was untouched (4985/5000). Same burst behavior observed with retries + sleep. Fell back to REST `GET /repos/{o}/{r}/pulls/{n}` (`mergeable_state` field), which tolerated full bursts; cross-checked: agent-ops#31 → GraphQL "OPEN UNSTABLE" == REST "open unstable". Equivalence confirmed on samples before trusting the REST pass for all 113 (0 check failures).
- CI appears to be partially recovering: 8 PRs landed since the 04:57 run. Remaining open PRs are almost all UNSTABLE (checks not passing / still provisioning), so the merge gate stays on schedule.
- The western-heart model/content PRs on the watch list (234, 253, 263, 265, 268, 271, 273, 275, 281, 291, 295, 235) are all merged now — only agent-ops#27, agent-ops#31, agent-ops#32 remain open in that line, plus the western-heart ones aren't open anymore.
