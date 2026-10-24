# FRICTION RESEARCH LOG

Dated sections, one per research pass. Conventions: [[RESEARCH-PULLIN-INDEX]].
Master consolidated report of the first sweep: `FRICTION-RESEARCH-2026-10-19.md`
(six clusters; restic/aria2/zstd/croc decided there — not re-researched).

---

## 2026-10-22 — Continuous friction-research pass (3 problems, 3 researchers)

Owner standing order 2026-10-19 ~23:03 CDT. Problems picked from the last few
days of `~/MEMORY.md`, `~/memory/2026-10-2*.md`, and
`~/workspace/agent-ops/disk-cleanup-log.md` (failures/stalls/retries Oct 20–22),
excluding everything settled in the 2026-10-19 sweep.

### Problem 1 — GitHub release upload write-timeouts persisting for DAYS

**Cost:** longtail lane lost `1981.zip`–`1985.zip` repeatedly Oct 20–22
("FAILED after 4 retries (TimeoutError)" / "Connection aborted / write operation
timed out"), one ~400MB whole-file upload at a time, no resume. Guardian
offload verify-downloads also failing (`FAIL download-back failed`), blocking
deletes while verify fails.

**New finding (not in cluster 01):** `gh release upload`'s retry is exactly
initial + 3 retries at a **constant 200ms** backoff, retrying only transport
errors/5xx, with **no low-speed stall detection** (verified in cli/cli trunk
`pkg/cmd/release/shared/upload.go` — the lane's "fails after 4 retries" symptom
matches to the attempt). A stalled POST hangs indefinitely. `gh` also uses
5-way concurrency and `--clobber` deletes the old asset BEFORE re-uploading.
Cluster 01's retry.py was wired into CloudDog only — and CloudDog's local copy
was removed by owner order 2026-10-21, so standalone lanes have nothing.

**Wired:** `lanes/resilient-gh-upload.sh` + `lanes/RESILIENT-GH-UPLOAD-SOP.md` +
`lanes/tests/test-resilient-upload.sh` (15/15 stubbed tests green):
split-to-exactly-100MB parts (owner standard; `RU_PART_SIZE` is tests-only),
sha256 manifest uploaded LAST (CloudDog-compatible schema),
curl direct-POST to `uploads.github.com` with `--speed-limit/--speed-time`
stall-kill (exit 28 → retry, never a multi-day hang), `-T` streaming,
sequential parts, 8-attempt exponential backoff + jitter, retry only
curl 7/28/52/55/56 + HTTP 5xx/429 (abort on 401/403/404/422),
idempotent resume (size-matched parts skipped; mismatched parts
DELETE-then-reuploaded — worst case re-sends 100MB), per-part size/digest
verify + final asset-list check.
Pattern adopted from ading2210/gh-large-releases — license verified **LGPL-3.0**,
so the pattern (naming/manifest/delete-then-reupload) is adopted, code is NOT
vendored. Stall-kill semantics from curl's documented `--speed-limit` (exit 28).

**Recommendations (not wired):** bring the longtail lane onto the 100MB
split+manifest convention (its whole-file uploads are the other half of the
failure); live-upload smoke test of the script against a scratch release
(stubbed tests only so far — no repo artifacts created by this pass).

### Problem 2 — VM runtime restarts kill lanes AND their watchdogs

**Cost:** TTT2 pull lane died ~9 times in one night; its own watchdog went
absent too; a coordinator died 8 min in with no checkpoint. Cluster 04 assumed
the supervisor survives — it doesn't always.

**New finding:** **this VM has no local cron daemon at all** (no
`cron`/`crond` binary, no `/etc/crontab`, no crond process — checked 2026-10-22),
so `@reboot` crontab entries are not installable without apt/root. The runtime
scheduler cron (which runs this task) DOES survive restarts — it is the only
restart-resilient loop available. systemd user units already verified
unavailable (cluster 04).

**Wired (design only — NOT scheduled, NOT installed):**
`lane-autostart/lane-autostart.sh` + `lanes.manifest` + `CRONTAB-TEMPLATE.txt` +
`README-lane-autostart.md`. flock(1) is the ONLY liveness authority (kernel
releases locks on death/reboot — no stale-lock hazard, verified from sources);
never kills live lanes; crash-loop guard (max restarts/hour → pause +
`state/<lane>.ESCALATE`); watchdogs supervised too (own lock + heartbeat file —
covers the dead-watchdog incident); `setsid` + `env -i` + explicit PATH launch
discipline; all lanes ship DISABLED. Supervisor alternatives re-checked:
supervisord (BSD-style) / circus (Apache-2.0) / honcho (MIT) / overmind (MIT) /
s6 (ISC) — all SKIP (bootstrap gap without systemd, or no autorestart, or
PID-1 rooting); no new evidence overturns cluster 04. Verified with my own
eyes: `bash -n` clean, single-instance across 4 supervisor runs (1 real lane,
"alive (lock held)" logs), crash-loop cap fired at max with ESCALATE written.

**Blocked on OWNER APPROVAL (not installed):** (1) creating the scheduler cron
entry (~5 min) that runs `lane-autostart.sh` — the recommended wiring;
(2) installing a local cron daemon if the `@reboot` supplement is ever wanted;
(3) registering any actual lane (flipping `no`→`yes` in the manifest).

### Problem 3 — Merge-order hazards with the PR pile-up

**Cost:** western-heart PR #497 carried old geometry while PR #508's fix merged
first — the #497 lane had to rebase preserving the fix; an in-flight A4 rig was
built on pre-#508 geometry. Cluster 03 covered CI minutes/runners, not ordering.

**Wired (no approval needed):** `merge-ops/pr-overlap.sh` +
`merge-ops/PR-OVERLAP-README.md`. Read-only `gh` calls: open PRs with file
lists, pairwise overlap detection, mergeable/mergeStateStatus, suggested merge
order. Live-tested against `mhvnsnt/agent-ops`: 17 open PRs listed, real
overlaps flagged (CLAIMS.md shared by #9/#10/#11/#24, several already
CONFLICTING). Makes the hazard visible; enforcement follows.

**Verdicts:** GitHub native merge queue — **RECOMMEND as pilot** ($0 for public
org repos; true serialization via `merge_group`; merge method must be "merge"
per owner law; needs branch protection + `merge_group` CI trigger).
Kodiak — SKIP (license verified **AGPL-3.0**, and it doesn't serialize).
bors-ng — SKIP (Apache-2.0, real serialization, setup tax too heavy for 135
repos). Mergify — CONDITIONAL power option (free for public repos,
`Depends-On` cross-repo chains; only after a native pilot proves out).
**Merge-queue enablement needs OWNER APPROVAL** (changes repo behavior).

### Tooling-involvement note (reporting rule)

No aider/copilot/gemini CLI involvement in this pass (not installed on this VM;
verified absent). Codex not used. All research via live web sources cited in the
docs above; all wire-ups are own-code (bash/python3 stdlib) or adopted research
output, tested as recorded.
