# /var/tmp adoption audit: the guard exists, nobody uses it — 7 scripts still hardcode tmpfs, quezada driver will exceed it

- **Date:** 2026-11-18 ~23:05–2026-11-19 ~00:45 EST (continuous-friction-research pass)
- **Index:** [[RESEARCH-PULLIN-INDEX]] (entry added by this pass)
- **Status:** researched + one tool wired and tested (`var-tmp-audit.sh`,
  this dir). No lane script edited — the fixes belong to the lane owners.
- **Dedupe:** `research-check.sh "var/tmp tmpfs"` — only prior hits are
  the loss record (`CUT001R-6B-VM-RESTART-LOSS-20261115.md`), the
  2026-11-09 note ("/tmp is a 512 MB tmpfs — never stage transfers
  there"), and the 2026-11-15 pass below. This is the adoption follow-up
  to that pass, not a re-research of tmpfs itself.

## TL;DR

The Nov 15 pass already built the fix for this failure class
(`tmpfs-guard.sh` + `stage-as-it-lands.sh` + `entr`), and Nov 17
proved the class is still live: /var/tmp hit 100% (Blender 5.2.4
extract 1.2G + pb-pokemon 844M), the 6B gate died on ENOSPC (gate log
stuck at 4096 B, partial line), the Pokemon pull-back stalled at
884M/951M, and the ~00:05 EST VM restart then wiped /var/tmp and
killed the gate runner (pid 29903). The Pokemon lane fixed its own
driver ad-hoc (env-overridable `PB`). But **adoption of the Nov 15
guard is zero**: no lane script anywhere in agent-ops calls
`tmpfs-guard.sh` (only MERGE-QUEUE.md and `.mq-main-tmp.md` mention
it). This pass ran the sweep the Nov 15 doc called for and wired it as
a script: **7 scripts hardcode a /var/tmp output dir, 3 more default
to it behind an env override.** Worst live item: the quezada stage
driver hardcodes `PB="/var/tmp/pb-quezada"` while its own comment
admits the reassembled file (up to 2.4G) **EXCEEDS** the 2G tmpfs —
a self-documented time bomb, same shape as the Nov 17 kill.

## 1. Evidence (live, this pass)

| Fact | Value |
|---|---|
| /var/tmp now | tmpfs, 2.0G, **60% used (1.2G)** at audit time (bl524 back) |
| /tmp now | tmpfs, 512M, **89% used (451M)** at audit time — nearly full, no action taken here (guardian owns it) |
| Nov 17 kill | /var/tmp 100% → 6B gate runner died (ENOSPC), Pokemon pull-back dead at 884,805,632/951M; VM restart ~00:05 EST wiped /var/tmp, gate runner pid 29903 gone; 52nd successor rebuilt the chain (Blender re-downloaded byte-exact) |
| Pokemon fix (lane) | `pokemon-stage-driver.sh:16` — `PB="${PB:-/var/tmp/pb-pokemon}"`, relaunched with PB on the 150G disk; its own comment still records "/var/tmp is a 2G tmpfs (1.5G used: bl524 1.2G + stale …)" |
| Quezada driver | `quezada-stage-driver.sh:17` — `PB="/var/tmp/pb-quezada"` **hardcoded**; line 93 comment: "stream parts in order into a running sha256 via a temp reassembled file in /var/tmp (tmpfs 2G — parts are 400M, reassembled is up to 2.4G: EXCEEDS tmpfs!)" |
| Guard adoption | `grep -rln "tmpfs-guard\|stage-as-it-lands"` across agent-ops (*.sh/*.py/*.md): hits only in `MERGE-QUEUE.md` + `.mq-main-tmp.md` (mentions) and the 20261115 tools themselves. **Zero lane scripts call the guard.** |
| Audit run | `var-tmp-audit.sh --root ~/workspace/agent-ops` → **HARDCODED: 7, OVERRIDABLE: 3, exit 1** (full output in §2) |

## 2. Audit results (`var-tmp-audit.sh`, tested live this pass)

| Script | Class | Detail |
|---|---|---|
| `disk-stage-20261110/pullback2.sh` | HARDCODED | `PB="/var/tmp/pb-$TAG"`, `RES=/var/tmp/pb-results.log`; comment: "Peak /var/tmp use = reassembled tar only (max 1.3G)" |
| `disk-stage-20261110/pb-queue-seq.sh` | HARDCODED | `QLOG="/var/tmp/pb-queue-seq.log"`, `export PB_DIR=/var/tmp`, `MARKDIR="/var/tmp/disk-stage-fix/markers"` |
| `disk-stage-20261110/stage3/pb-redo-cj-v6-work-20261112.sh` | HARDCODED | `PB=/var/tmp/pb-cj-v6-work-20261112`; its own comment: parts 1.44G fit, parts + reassembled tar 2.88G do NOT |
| `disk-stage-20261110/stage3/pb-braid-verify-20261112.sh` | HARDCODED | `PB="/var/tmp/pb-braid"`; comment: 5 parts 1.55G + reassembled tar 3.63G cannot fit |
| `disk-stage-20261113/stage-your-files/upload-part.sh` | HARDCODED | `TMPDIR=/var/tmp/stream-stage` |
| `disk-stage-20261113/stage4-queue.sh` | HARDCODED | `LOCKDIR=/var/tmp/disk-stage-fix` (locks only — low risk, still tmpfs) |
| `disk-stage-20261116/quezada-stage-driver.sh` | HARDCODED | `PB="/var/tmp/pb-quezada"`; reassembled up to 2.4G vs 2G tmpfs — **live, will fail** |
| `disk-stage-20261110/pullback-seq.sh` | OVERRIDABLE | `PB="${PB_DIR:-/var/tmp/pullback-$TAG}"` |
| `disk-stage-20261113/pullback-seq-stream.sh` | OVERRIDABLE | `PB="${PB_DIR:-/var/tmp/pullback-$TAG}"` |
| `disk-stage-20261116/pokemon-stage-driver.sh` | OVERRIDABLE | `PB="${PB:-/var/tmp/pb-pokemon}"` (fixed Nov 17; default still tmpfs) |
| `disk-stage-20261110/pb-queue.sh`, `disk-stage-20261113/stage-your-files/stream-stage.sh`, `disk-stage-20261113/watch-streams.sh` | MENTION | /var/tmp in comments/docs only |

Notes: the 20261110/20261113 scripts are older stage dirs — they are
reported as found, not claimed live; a lane reusing them hits the same
wall. The audit greps `*.sh` under the given root only (bounded: a
full-`~/workspace` grep takes 5+ minutes across the 18G dream-girl
tree). The 6B gate script itself lives in /var/tmp
(`gate_and_run_6b.sh`, pid 3355, `/var/tmp/cut001r` per the Nov 18
guardian passes) — outside any workspace root, so the audit cannot see
it; it is the known-live case from the Nov 15 doc §4.1, still unmoved.

## 3. What was wired + test evidence (this pass)

**`var-tmp-audit.sh`** (this dir) — `--root DIR` (default
`~/workspace/agent-ops`); classifies each `*.sh` hit as HARDCODED /
OVERRIDABLE / GUARDED / MENTION; exit 0 = no hardcodes, 1 = hardcodes
found, 2 = usage error. Skips `.git` and merge-queue worktrees
(mirrors, not live). Tested live: `--root ~/workspace/agent-ops` →
HARDCODED 7 / OVERRIDABLE 3 / exit 1, output matches the manual grep
exactly (same 7 + 3 files, same lines).

## 4. Recommended (lane owners apply)

1. **Quezada driver (urgent, live):** apply the pokemon driver's
   one-line pattern — `PB="${PB:-/var/tmp/pb-quezada}"` — and relaunch
   with PB on the 150G disk before the next pull-back. The 2.4G
   reassemble cannot fit 2G tmpfs by the driver's own math.
2. **6B lane (still open from Nov 15 §4.1):** move Blender 5.2.4,
   `gate_and_run_6b.sh`, and its log off /var/tmp; add
   `tmpfs-guard.sh "$OUT" || exit 2` at gate start. Still unmoved as
   of the Nov 18 guardian passes.
3. **Guardian / checkpoint protocol (still open from Nov 15 §4.3):**
   run `var-tmp-audit.sh` on its cadence (or at lane start) — a lane
   whose OUT dir fails the guard does not start until the path is
   fixed. Cheap, kills this whole failure class at the root.
4. **Legacy stage scripts (20261110/20261113):** any lane reusing them
   applies the same `PB_DIR` override first, or retires them — do not
   relaunch a hardcoded /var/tmp pull-back into a 60%-full tmpfs.

## 5. Blocked / not done here

- No lane script edited (live lanes + retired stage dirs — owners apply).
- No /var/tmp or /tmp contents deleted (guardian owns sweeps; /tmp at
  89% is flagged here, not acted on).
- No VM-restart behavior changed; /tmp and /var/tmp remain tmpfs by
  design — the fix is never pointing durable work at them.
