# DISK CENSUS — cleanup sweep 2026-10-21 ~11:58 CDT (owner order 11:55 CDT)

## Baseline
- `/home/hatch`: 100G total, 96G used, **2.8G free, 98%** at sweep start (16:58 UTC).
- `~/workspace` du total: 107G (overcounts — git objects hardlinked across many worktrees; df is ground truth).
- / (overlay): 7.5G, 3% — not the problem.

## LIVE — HANDS OFF (running processes and/or writes in last 60 min)
Processes observed: CloudDog daemon (pid 1745, interval 600); aria2c downloading WWE All Stars into `agent-ops/w1-allstars-work` (pid 43536); `upload_driver.py` in `agent-ops/viggle-mirror-20261021` (pid 1885, delete-as-you-go mirror); `longtail_pull.py` + `at-inflate2.py` in `agent-ops/triage-scratch` (pids 6082/32592); `batch6.py` in `_doa4p2-scratch` (pid 2189); `test_embedded.py` in `_w7a-work` (pid 35119, Tekken 6 decrypt); Blender renders running from `rigwork-tmp` (personality remainder lane) and `scii-work/p8r`; `_docfrank-fix` proofshot + http servers; tripo-pull into `_zen-combined-work` (pid 45170); a CloudDog scan process sweeping tools/_wh-work/rigwork-tmp/cape-jones/_cornerstone-work.

Recent-writes live trees: `_w3b-work`, `_w7b-wh`, `_w7b-work`, `_wh-work` (t3-crash-fix + pantera-lk-scratch + pantera-leopard-king), `_kinpo-a1-repair`, `_cornerstone-work`, `_doa4p5-clone`, `_cs-round2-work`, `_csui-v2-work`, `_t6r4-work`, `_w5c-work`, `_zen-spirit-work`, `_fighter-completeness`, `yuyu-hakusho-w2/work` (also GAME FILES — strictest bar), `agent-ops/storeoff-20261021` (2.3G, an active store-off lane), `agent-ops/w1-allstars-work` (1.9G, active download), `rigwork-tmp` (11G), `_docfrank-fix` (1.7G).

Never-clear regardless: `~/workspace/your_files` (1.1G, owner deliverables), `~/workspace/user` (448M, owner's own files).

## Top-level sizes (du -sh, sorted)
| dir | size | class |
|---|---|---|
| tools | 13G | infrastructure — Blender in active use by running renders; HOLD |
| _wh-work | 12G | mixed live/dead lane dirs — per-subdir |
| rigwork-tmp | 11G | LIVE (Blender render running) |
| cape-jones | 6.9G | repo, dirty tree (uncommitted deletions) — .git gc candidate only |
| _cornerstone-work | 5.3G | LIVE (writes last hour) |
| wh-pose-survey | 3.8G | owner lane terminated — VERIFY |
| _w7b-work | 3.7G | LIVE |
| _anim-bank-work | 3.5G | no writes 60m+, 52 uncommitted files this AM — VERIFY (push, never delete) |
| agent-ops | 3.4G | mostly LIVE subdirs (storeoff 2.3G, allstars 1.9G) — per-subdir |
| _t6r4-work | 2.6G | LIVE |
| yuyu-hakusho-w2 | 2.3G | LIVE + game files |
| _docfrank-fix | 1.7G | LIVE |
| _docfrank-facing | 1.7G | no writes 60m+; sibling lane superseded it? — VERIFY |
| _w3b-work | 1.6G | LIVE (39k files/hr) |
| _doa4p2-scratch | 1.6G | LIVE (extraction running) |
| _w7a-work | 1.5G | LIVE |
| _w3-work | 1.2G | quiet 60m+ — VERIFY |
| _w7b-wh | 1.1G | LIVE |
| wh-pose-work | 746M | VERIFY |
| viggle-inputs | 686M | mirror lane in-flight (self-clearing) — HOLD |
| autorig-work | 683M | VERIFY |
| tripo-recovery | 599M | Tripo originals — VERIFY per-file vs releases |
| _j3-work | 582M | VERIFY |
| wh-lane2-fighters | 576M | VERIFY |
| tripo-sitting-pull | 575M | VERIFY |
| reskin-fix-work | 547M | VERIFY |
| trippedd-copylane | 518M | VERIFY |
| ratedm | 512M | VERIFY |
| lane2-work | 503M | VERIFY |
| tpose-staging | 482M | VERIFY |
| render-work | 479M | VERIFY |
| reskin-wave | 453M | VERIFY |
| services | 437M | VERIFY |
| wh-lane3-movesets | 393M | VERIFY |
| tripo-decoded | 389M | VERIFY |
| fingertip-fix | 389M | VERIFY |
| Forge3D | 387M | repo clone — VERIFY |

## Method
Per candidate: latest-mtime check → git status/HEAD-vs-origin (or release verification for binaries) → push/upload anything unstored → clear → log to disk-cleanup-log.md with pull-back command → df re-measure. Game files: strictest bar + TEARDOWN-IDLE-QUEUE entry before any clear; in doubt = HOLD.
