# MASTER TEARDOWN TRACKER
Owner directive 2026-10-13 19:13 EDT. Coordinator checkpoint: `teardown-master-coordinator.json`.
Last updated: 2026-10-13 23:16 UTC.

## Disk status
- **95% (5.1GB free)** — CRITICAL, above 88% hard ceiling. Disk cleanup worker active.

## TIER 1 — Small / immediate

| # | Game | Size | Target repo | Status | Worker |
|---|------|------|-------------|--------|--------|
| 1 | WWE 2K animation packs | 0.69GB | wrestling-game | ASSIGNED (pull running) | wwe2k-pull (parent) |
| 2 | WWE 2K14 | 1.26GB | wrestling-game | ASSIGNED (pull running) | wwe2k-pull (parent) |
| 3 | Def Jam: Fight for NY | 4.47GB | wrestling-game | **COMPLETE 01:22 UTC** — surgical range extraction (no full ISO download). 78 fighter sets, 7,948 CAW parts, 858 venue files, 141 motion triplets. PR #2 (wrestling-game) + PR #68 (western-heart ANIMATION-FINDINGS.md) merged. AKI engine lineage confirmed. Audio deferred (disk). | defjam-teardown (coordinator) |
| 4 | SF EX2 Plus | 198MB | western-heart/teardown/ | PARTIAL — orig 7z corrupt; alt 7z verified (198,666,400B) on disk; extraction+teardown deferred (disk 95%) | wh-sf-100 |
| 5 | SF EX Plus Alpha | 252MB | western-heart/teardown/ | **COMPLETE 2026-10-15** — pulled+verified, TEARDOWN.md + 165 move names + roster + 52 OVL overlays, PR #148 merged; TeraBox task staged | wh-sf-100 |
| 6 | SF EX3 | 669MB | western-heart/teardown/ | PARTIAL — .bin on disk verified (629,030,355B); PS2.DAT teardown deferred (disk 95%) | wh-sf-100 |

## TIER 2 — Large, TeraBox staging

| # | Game | Size | Target repo | Status | Worker |
|---|------|------|-------------|--------|--------|
| 7 | SFIV PC | 4.18GB | western-heart/teardown/ | NOT STARTED — not on disk/GH releases; blocked (disk 95%, needs ~5GB headroom) | — |
| 8 | SF X Tekken | 12.99GB | western-heart/teardown/ | NOT STARTED — not on disk/GH releases; blocked (disk 95%, needs ~14GB headroom) | — |
| 9 | Ultra SFIV | 16.61GB | western-heart/teardown/ | NOT STARTED — not on disk/GH releases; blocked (disk 95%, needs ~18GB headroom) | — |
| 10 | WWE 2K15–2K23 | 33–84GB ea | wrestling-game | CATALOG DONE, not started | — |

## TIER 3 — Existing lanes (do not duplicate)

| # | Game | Status | Lane |
|---|------|--------|------|
| 11 | TTT2 | Downloading (parts 01-06) | full-extraction-all-games + watchdog |
| 12 | Tekken 6 | EBOOT decrypted; IDX+data need PPSSPP memdump | full-extraction-all-games |
| 13 | Urban Reign audio | VGS decoded; ADX blocked on disk | teardown-100-percent (watchdog) |
| 14 | DOA4 | Downloading | doa-stepdown (watchdog) |

## TeraBox
- Master backup prep DONE (staging tarballs ready in ~/workspace/terabox-staging/).
- **Staging-prep worker COMPLETE 00:31 UTC** — 5 tarballs staged+verified (~3.1GB): teardown-batch-b (734MB, rebuilt — original was corrupt), teardown-batch-c (1.2GB), models-batch-a (1.1GB), western-heart-docs (54MB), wrestling-models (1.4MB).
- **BROWSER-TASKS.md written** (~/workspace/terabox-staging/BROWSER-TASKS.md) — exact upload specs per batch + GitHub Release download→TeraBox tasks.
- **terabox-inventory.md written** (~/workspace/agent-ops/terabox-inventory.md).
- **Worker flags:** Def Jam ISO partial (109MB, in-flight); WMXIX ISO symlink broken (GitHub release only); wwe2k14.rar in-flight (stage as batch-c2 later).
- **Parent action needed:** delegate browser upload tasks per BROWSER-TASKS.md. Subagents cannot spawn browser tasks.

## Rules
- One worker per game; check this tracker before spawning to avoid duplicates.
- Every game: download → extract (models, stages, audio, movesets, UI) → TEARDOWN.md → branch/PR/merge → originals staged for TeraBox.
- Wrestling models → mhvnsnt/wrestling-game. Fighting games → western-heart/teardown/<game>/.
- Def Jam: models → wrestling-game; animation/grappling findings → western-heart.
- Disk >88%: no large downloads without cleanup first. Verify safe storage before deleting.
