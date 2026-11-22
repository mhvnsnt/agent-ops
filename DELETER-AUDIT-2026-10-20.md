# DELETER AUDIT — 2026-10-20

Status: COMPLETE (audit run 2026-10-20 ~10:20–10:45 CDT, resumed after two runtime restarts; findings appended as verified throughout).

## Context (from task brief)
- Overnight investigation (disk-cleanup-log.md ~04:05 CDT entry) RESOLVED the "rogue sweeper" question: NO rogue lane. Deletions were (1) main agent's authorized hand-clear, (2) VM/overlay reset of ephemeral /opt/wt-staging, (3) mirror lane's legitimate delete-after-verify.
- One genuine casualty: 4 intermediate .blends (bake_test.blend, cs_test.blend, pipeline2_in.blend, proof_before.blend) deleted ~03:59-04:00Z unstored/unjournaled via the pre-PR#45 daemon --apply path. Gate merged in PR #45, repo mhvnsnt/CloudDog-Muse-Storage-Disc-Assistant main 3e64090.
- This audit does NOT re-hunt a rogue. It is the census + proof of what can delete now.

## Verdict in one paragraph
Every AUTOMATED deleter currently running on this box is either (a) routed through the PR #45 delete gate (`clouddog.delete_gate.check_delete_gate`), or (b) an accountable verify-then-delete lane that journals actor + proof + pull-back to disk-cleanup-log.md. The 24/7 daemon — the actor that caused the 03:59Z casualty — is now DRY-RUN (heartbeat `dry_run: true`, `cleared: 0`; supervise.sh has --apply explicitly revoked 2026-10-20). NO currently-running process was found that can delete with neither gate nor journal. The residual risk is NOT a hidden program: it is (1) agent-level ad-hoc deletion (the guardian cron and any interactive agent can `rm` on prompt discipline alone — no code gate exists for that surface), and (2) latent pre-gate code paths that are not scheduled or running but still exist on disk (legacy `cmd_reap` v1, a dormant pre-gate checkout). Both are itemised below with dispositions.

---

## 1. Census — scheduled jobs (authoritative: cron.list, 2026-10-20)

51 schedules returned (incl. disabled + runtime system jobs). Delete-capable among them:

| Actor | Schedule | What it can delete | Class | Journal evidence |
|---|---|---|---|---|
| disk-space-guardian | interval 10m, enabled, timeout 1800s | Ad-hoc: pushed-clean git clones (`rm -rf`), venvs, verified bulk; spawns `cloud_dog.py enforce --apply`; spawns mirror lanes | ACCOUNTABLE-by-instruction / ROGUE-RISK surface (see §4.1) — its own clears are governed only by its prompt (verify + log), no code gate | disk-cleanup-log.md — entries are detailed (actor, sizes, HEADs, pull-back) in every sampled run |
| cloud-dog-daemon-keepalive | interval 5m, enabled | Nothing. Restarts daemon via supervise.sh when heartbeat stale/dead | Not a deleter | Restart lines in disk-cleanup-log.md |
| overnight-idle-pipeline | interval 30m, enabled | Its own lock file only; body explicitly: "NEVER delete anything. Only the disk-space-guardian's existing rules may delete" | Not a deleter | overnight-log.md |
| worker-watchdog (15m), keep-working-pulse (10m) | enabled | No deletion instructions (resume checkpoints; stale-lock handling only) | Not deleters | — |
| All other ~45 schedules (incl. goal crons under ~/workspace/goals/*/crons/) | various | grep for cloud_dog/delete/rm/guardian matched only the jobs above plus gigaleak-pikpak-pull-loop, torbox-magnet-retry, continuous-friction-research, watermark-removal-watch, fosters-v2-terabox-retry — all pull/retry/watch jobs; none carries a workspace delete path | Not deleters | — |
| Runtime system jobs (feed-pulse-00..23, deterministic-doctor, profile-image) | system | Bodies are runtime-managed, not inspectable from workspace files; no evidence in any log of workspace deletion by them | Uninspectable — no adverse evidence | — |

### Duplicate-guardian question — RESOLVED, no duplicate schedule
- `cron.list` shows exactly ONE `disk-space-guardian` job: interval@10m, enabled.
- Three older definitions (interval@15m, @30m, @6h) exist ONLY under `~/workspace/cron.d/_archive/` and are absent from the scheduler list — archived, not live.
- Explanation for the ~1-min-apart guardian invocations a run flagged (04:03 / 04:04:40 CDT log entries): the job's timeout is 1800s against a 600s cadence, so a long run and the next scheduled run can overlap in wall-clock logging; the 04:15 CDT run itself noted the sibling run and avoided duplicating its work. Overlap is possible by configuration; a duplicate *schedule* does not exist. Recommendation: none required; if tighter accounting is wanted, the fix is a run-lock in the guardian body, not schedule surgery.

## 2. Census — running processes (sampled 2026-10-20 ~10:20 and ~10:31 CDT)

| Actor | State at audit | What it can delete | Class | Evidence |
|---|---|---|---|---|
| CloudDog daemon `python3 -m clouddog.cli daemon --interval 600 --roots /home/hatch/workspace` (src/clouddog) | RUNNING (pid 25288, restarted as 3041 after VM restart during this audit) | In --apply posture it would delete only via gate; **currently deletes nothing** | **GATED + currently inert** | heartbeat.json: `dry_run: true, stored 0, verified 0, cleared 0, skipped_sacred 199`; supervise.sh carries the 2026-10-20 "AUTONOMY REVOKED" note — no `--apply` flag; daemon.py:35 imports check_delete_gate, calls it at :409/:539; reaper.py:334 and streamer.py:714 likewise |
| Guardian-spawned `python3 ~/workspace/cloud-dog/cloud_dog.py enforce --apply` | RUNNING at first sample (pid 19085) | Registry entries only | **ACCOUNTABLE** (not gate-module — see §4.2) | cmd_enforce → cmd_reap_v2: V1 `evaluate()` front-decider (SACRED blocked, KEEP_LOCAL/STORE skipped, game files strict) → `decide_delete` laws engine → live per-store verify → delete → `audit_log("reap", …)` + registry status + disk-cleanup-log line. Repeated log lines this morning: `enforce: reaped=0` (registry empty of pending) |
| Mirror/upload lanes: tk5 `upload_release.sh`, take2 `.take2-mirror/final-verify.sh`, `gh release upload` (clouddog-20261020-twerk, tekken5-e7-extract-v1), tekken5 ISO curl download | RUNNING / IN-FLIGHT | Delete-as-you-go of own verified parts only | **ACCOUNTABLE** | Per-lane logs in disk-cleanup-log.md with sizes/sha256/pull-back. **UNTOUCHED by this audit per NEVER-KILL-IN-PROGRESS law** |
| Everything else in `ps aux` (blender renders, ffmpeg, git fetches, playwright, http.server) | RUNNING | No delete path observed | Not deleters | — |

## 3. Census — scripts on disk

### 3a. GATED (route through `clouddog.delete_gate.check_delete_gate`)
| Script/module | Delete path | Notes |
|---|---|---|
| `~/workspace/cloud-dog/src/clouddog/daemon.py` | gated at :409/:539 | Live daemon engine; dry-run posture above |
| `~/workspace/cloud-dog/src/clouddog/reaper.py` | gated at :328-334 | Registry reap for the v1 engine |
| `~/workspace/cloud-dog/src/clouddog/streamer.py` | gated at :708-714 | Stream/delete-as-you-go; claims leg consults work-claims table (:493) |
Gate legs (delete_gate.py:77): policy verdict + registry/store proof + claims + journal — fail-closed (`GateBlock`). PR #45 commits verified in `~/workspace/cloud-dog` git log: 041f0b7 (gate module), 6810c00 (daemon routed), ff2b0e1 (reaper/streamer routed), f8ff789 (claims fail-closed), merge 3e64090.

### 3b. ACCOUNTABLE (own verify + journal naming actor + proof + pull-back; no gate module)
| Script | Verify before delete | Journal |
|---|---|---|
| `cloud_dog.py` cmd_reap_v2 / cmd_enforce | V1 evaluate + laws decide_delete + live store verify; game-file strict bar runs an actual pull-back prover | audit.jsonl + registry + cleanup-log |
| `cloud_dog.py` cmd_dedup (:2589) | full hash equality vs kept copy + decide_delete | audit_log("dedup") + cleanup-log |
| `cloud_dog.py` cmd_mirror parts (:1832/:1884/:2103) | per-part upload+verify before unlink; manifest retained | mirror manifest + audit |
| `agent-ops/mirror-one.sh` | per-part remote **size** verify (3 attempts), original deleted only if ALL parts verified; failure leaves everything | cleanup-log line with pull-back command |
| `agent-ops/mirror-wh-work-20261020.sh` (MIRROR-WW) | per-part size verify, delete-as-you-go; source `rm -rf` only after full re-download stream sha256 verify | MIRROR-WW lines in cleanup-log. **Fail-closed proof in the wild:** 04:49 CDT re-download sha256 MISMATCH on moveset-cluster-b-t7 → "local dir KEPT" |
| `agent-ops/guardian-mirror-20261020-0744.sh`, `mirror` lanes (`.take2-mirror/`, tk5 `upload_release.sh`) | same split/upload/verify pattern | cleanup-log |
| `tools/fetch/store` (`--delete-local`) | upload-verify before delete; updates STORAGE-MANIFEST.json | manifest + log |
| `agent-ops/stream_store.py`, `stream_chunk_upload.py`, `resume-cn-gigaleak-store.py`, `t6ps3_upload.py`, `gh-upload-cn-work.sh`, `jt-archive-lane.sh`, `doa4-verify-reap.sh`, `ep01-master-upload.sh`, `ep01-fixed-master-upload.sh`, `wg-chunks-upload.sh`, `ttt2_chunk_upload6.sh`, `bakeoff-offload.sh` | per-chunk/part verify-then-unlink pattern (grep-located; same lane family) | lane logs / cleanup-log |
| `agent-ops/disk-guardian-offload-20261015.sh` (2026-10-15 one-off) | download-back sha256 per part; source deleted only after EVERY part verified; checkpointed | cleanup-log + checkpoint json. **Read in full during this audit — earlier suspicion of an unguarded `rm -rf $3` was refuted: the rm sits behind the verify gate in code** |
| `agent-ops/offload-triple-xxx.sh` (2026-10-14 one-off) | remote size verify per tar; on any failure logs "NOT deleted" and deletes nothing | cleanup-log + STORAGE-MANIFEST.json entries with sha256 |
| `agent-ops/loti-verify-run.sh`, `vft-verify-run.sh` | verify-run pattern; vft also `gh release delete`s its own backup release at end-of-lane (by design, after local verify) | lane logs |
| `cloud-dog/stream_blob_reaper.py` | deletes ONLY on local sha256 == remote hash; writes manifest entry | manifest.json (weakest journal in this class — no cleanup-log line, no gate). Standalone helper; no live lane found invoking it during this audit |

### 3c. ROGUE-RISK (can delete with neither gate nor journal)
| Item | Running/scheduled? | Disposition |
|---|---|---|
| **Ad-hoc agent shell deletion** — the guardian agent's own prompt-authorised clears (pushed-clean clones, venvs, "documented" model weights) and any interactive agent's `rm` | Guardian runs every 10m by design | **Cannot be code-gated from this lane; NOT touched (owner law + it is the owner's own standing cleanup order).** Recommendation in §6 |
| **`cloud_dog.py` cmd_reap (v1, :959)** — direct `cloud_dog.py reap --apply` path: policy-leg + GitHub verify only; bypasses laws `decide_delete` AND the delete_gate claims leg | Not scheduled (guardian calls `enforce`, which dispatches to v2), not running | **Latent. NOT hot-patched by this audit** — the engine is live (an enforce process was mid-run) and repo rules require branch→PR→green tests for engine changes. Recommendation in §6 |
| **`cloud_dog.py` cmd_daemon (legacy, :2389)** — standalone daemon inside cloud_dog.py | Not running; supervisor launches `clouddog.cli` (src) instead | Latent; same recommendation |
| **Dormant pre-gate checkout `~/workspace/CloudDog-Muse-Storage-Disc-Assistant`** at daf88af (PR #40 — predates the gate) | Nothing references it: supervise.sh and the guardian both use `~/workspace/cloud-dog` (at 3e64090, gate merged) | Latent; **not deleted by this audit** (audit deletes nothing; also a repo checkout). Recommendation: pull it to main or remove the checkout so no future lane can run pre-gate code from it by mistake |
| `/tmp` + `/opt` ephemeral trees (e.g. /opt/wt-staging) | VM/overlay resets delete these with no journal by platform design | Out of gate reach by construction — nothing irreplaceable may live there; already the standing lesson of the overnight resolution |

**Actions taken by this audit: NONE destructive.** No process killed, no file deleted, no script edited. The two one-off scripts initially suspected (§3b, last-but-two rows) were read in full and cleared. All other dispositions are recommendations for the parent/owner, because the remaining rogue-risk items are either (a) the owner's own authorised agent behaviour, or (b) live-engine code whose fix must go through the repo's branch→PR→test path.

---

## 4. Notes on the two structural findings

### 4.1 The guardian is accountable by instruction, not by construction
Its log discipline is genuinely good (sampled entries name actor, byte counts, HEADs, stash state, pull-back). But nothing *prevents* a guardian run from deleting on a mistaken "pushed-clean" judgement — the same failure shape as the historical incidents, one level up. The gate+journal design goal is met for the *engine* paths the guardian invokes (`enforce --apply`), not for the guardian's own hands.

### 4.2 `enforce --apply` is not the gate module
`cloud_dog.py` contains zero references to `delete_gate`. Its v2 reap is a parallel implementation of the same invariant (policy front-decider + laws + live verify + audit journal) and fails closed when the policy engine cannot import. It is honestly classed ACCOUNTABLE, not GATED. Unifying it onto `check_delete_gate` (so the claims leg also binds registry reaps) is the single highest-value hardening left.

### 4.3 Journal integrity quirk (minor)
During this audit, `~/.clouddog/heartbeat.json` was briefly overwritten by a pytest daemon instance (roots=/tmp/pytest-of-root/…, pid 4080) — test runs share the production heartbeat path. A keepalive reading that heartbeat could misjudge daemon health. No deletion resulted. Worth a test-isolation fix in the engine repo.

---

## 5. sf-tools.tar — VERDICT: NOT LOST. Fully recoverable locally; simply never stored.

Own-eyes evidence (2026-10-20 ~10:35 CDT):
- `~/workspace/_sf-scratch/sf-tools/` — source dir INTACT (188M).
- `~/workspace/_sf-scratch/sf-tools.tar` — INTACT, 196,249,600 bytes, sha256 `6891176bf54d561c2936486228d6acbb65cf9177bc1e3e7440b0aa6e7b949ca4`.
- `sf-tools.tar.part-aa` (104,857,600) + `sf-tools.tar.part-ab` (91,392,000) — present; concatenated sha256 == tar sha256 exactly (verified this audit). Parts are byte-perfect splits of the tar.
- Store side: `gh release view scratch-mirror-20261020 --repo mhvnsnt/clouddog-storage` lists 23 assets (pipeline_wk, pipeline2_wk, ex-plus-alpha, MUS, MOV, pipeline_out, weld_applied, bake_test_out parts) — **zero sf-tools assets**. `wh-work-mirror-20261020` also has zero sf-tools assets.
- Correction to the record: the 04:15 CDT guardian note "no sf-tools files locally" was wrong (or looked only in meshrepair-scratch). The files were in `_sf-scratch` the whole time; timestamps (tar 07:59Z, parts 08:00Z) predate the 03:27 CDT lane death — the lane died mid-UPLOAD, and its delete-as-you-go never fired because no part ever verified on the store. The fail-closed design worked; the watch item can close.
- Remaining action (not this audit's to run): mirror `_sf-scratch/sf-tools.tar` via mirror-one-style lane, verify, then clear per ONE-STORE. Until then it is unstored-but-safe locally, ~196MB + 188M source.

## 6. wt-verify — unattributed disappearance; what can and cannot be established

Established:
- `~/workspace/wt-verify/` (3.9G, parts part-aa..ai downloaded from cape-jones release assets, all DLV-OK per its dl2-progress.log) vanished ~04:06–04:12 CDT 2026-10-20. Directory still absent at this audit.
- Zero entries in BOTH CloudDog journals (`~/.clouddog/audit.jsonl`: 0 matches; `~/workspace/agent-ops/cloud-dog-audit.jsonl`: 0 matches), no disk-cleanup-log entry, no surviving checkpoint/process/script attributing the deletion (grep across agent-ops *.md/*.log, checkpoints, and both daily memory files found only the anomaly reports themselves).
- The data is safe: it was download-verified copies of cape-jones release assets; restorable from the releases. No data loss.

Cannot be established: who/what deleted it, or the exact mechanism. The overnight best hypothesis (the verify lane self-cleaned its staging after completion) remains unproven either way. This audit found no new attribution evidence and does not manufacture any.

Which NEW mechanism would have caught a recurrence:
- **Gate journal** — would NOT have caught it if the deleter was an agent shell (gate binds engine code paths only). Would have caught it if any engine path (daemon/reaper/streamer/enforce) had done it: every gated delete now writes an audit event with path + verdict legs.
- **Claims** — a live work-claim on wt-verify would have made the gate BLOCK an engine deletion and would have named the owning lane in the claims table, attributing the work even if a non-engine actor removed the files.
- **Mirror log** — a delete-as-you-go lane deleting its own verified parts writes cleanup-log lines per part (as MIRROR-WW and mirror-one do); a 3.9G self-clean would have left ~35 part lines. Their absence is itself evidence the deleter was none of the accountable lanes.
- Net: a recurrence is attributable by construction ONLY if the dir is (a) under a work-claim and (b) deleted by an engine path or an accountable lane. An unclaimed dir deleted by an ad-hoc agent shell remains unattributable — that is residual risk §7.1, and the practical fix is claiming staging dirs at lane start.

## 7. Residual risk list
1. **Agent ad-hoc deletion is ungated by construction.** Any agent (guardian included) can `rm` outside every journal. Mitigations in place: prompt law + cleanup-log discipline (observed working). Not fully closable without an OS-level control.
2. **Legacy `cloud_dog.py` reap v1 + legacy daemon** bypass the gate module (v1 reap: policy+verify only). Not scheduled/running. Fix path: route cmd_reap → cmd_reap_v2 semantics / check_delete_gate, via branch→PR→pytest in the CloudDog repo.
3. **`enforce --apply` ≠ gate module** (§4.2): registry reaps don't consult the claims leg. Unify onto `check_delete_gate`.
4. **Dormant pre-gate checkout** `~/workspace/CloudDog-Muse-Storage-Disc-Assistant` @ PR #40. Pull to main or remove before a future lane runs it by mistake.
5. **Daemon --apply is revoked by a comment + flag absence in supervise.sh**, not by an engine-enforced trust state. One mistaken edit re-arms it (though the gate would then bind every delete — the invariant holds; only the autonomy posture would change).
6. **Heartbeat path shared with tests** (§4.3) — keepalive health judgements can be spoofed by a test run.
7. **Guardian run overlap** (timeout 1800s > cadence 600s): two runs can interleave log entries and duplicate relaunch decisions (observed 04:03/04:15 — mirror lane relaunched twice, harmlessly because lanes are idempotent). A run-lock would make attribution cleaner.
8. **sf-tools (and _sf-scratch generally) is unstored**: safe today, single-copy. Mirror it before any future disk crunch tempts a hand-clear.

## 8. Census counts
- Scheduled jobs reviewed: 51 (cron.list, incl. disabled + system). Delete-capable scheduled actors: 2 (disk-space-guardian; cloud-dog-daemon-keepalive as daemon restarter only).
- Running delete-capable processes found: 3 families (daemon — gated/inert; enforce --apply — accountable; mirror/upload lanes — accountable, in-flight, untouched).
- Script families classified: GATED 3 modules (+ gate itself); ACCOUNTABLE 20+ scripts/lanes; ROGUE-RISK 4 items (1 structural/agent-surface, 2 latent legacy code paths, 1 dormant checkout) + ephemeral /tmp//opt by-design.
- Rogue-risk items shut down/patched on the spot: **none** — each remaining item is either owner-authorised agent behaviour (cannot shut down without countermanding the owner's standing order) or live-engine code (fix belongs in a tested PR, not an audit hot-patch). All are itemised with recommendations above rather than silently left.
