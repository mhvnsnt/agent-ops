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

---

## 2026-10-25 — Continuous friction-research pass (deploy block + 126s load + gate failures)

Owner standing order 2026-10-19 ~23:03 CDT. Problems picked from the last few
days of `~/MEMORY.md`, `~/memory/2026-10-25.md`, and
`~/workspace/agent-ops/disk-cleanup-log.md` (failures/stalls/retries Oct 23–25),
excluding everything settled in the 2026-10-19 sweep (restic/aria2/zstd/croc,
releases-as-store, CI minute-diet — the last one LANDED 2026-10-23 as
agent-ops #35, concurrency-cancel + timeout-minutes now on the western-heart
gate workflows) and the 2026-10-22 pass above. Two researchers fanned out in
parallel; a third friction (instruction-gate body failures) was checked by the
parent run directly. Research + docs only — no game code touched, no lanes
touched, nothing deleted.

### Problem 1 — Deploy blocked: 5,969 MB vs GitHub Pages 1 GB limit

**Cost:** live site `https://mhvnsnt.github.io/western-heart/` frozen on the
Oct 24 build; owner decision pending ("what gets cut").

**Doc:** `research-friction-20261025/01-deploy-pages-limit.md`.

**Verified live (2026-10-25/26):** Pages 1 GB published-site cap confirmed
from GitHub's own docs (5,969 MB is 5.8× over — the full set can never ship
on Pages). GitHub Release assets send **NO CORS headers** (curl-probed:
302 → `release-assets.githubusercontent.com`, 200, no `Access-Control-Allow-Origin`,
signed URL ~1 h expiry) — direct in-game `fetch()` from Releases FAILS, so
releases stay the store, not the runtime CDN. jsDelivr serves repo files
≤20 MB with CORS `*` + correct `model/gltf-binary` (live probe) and 403s an
86 MB GLB (documented 20 MB/file cap). Repo tree measured via the git-trees
API: 176 GLBs >20 MB hold 5,914 MB (73% of GLB bytes); 98 GLBs >25 MiB
(4,178 MB). Shell-only floor ≈ 70–170 MB (code ~10 MB + UI/portraits ~7.5 MB
+ 1 stage + 2 fighters + movesets/music). `game/netlify.toml` on main
verified: publishes `game/`, proxies `/roster/*` etc. to Pages (so Netlify
currently inherits the Pages problem).

**Recommended (1st choice, $0):** shell on Pages (~70–170 MB) + all GLBs on
Cloudflare R2 free tier (whole set fits 10 GB, $0 egress, CORS-configurable).
itch.io HTML5 shell + R2 lazy-load as the money path (shell fits the 500 MB /
1,000-file caps; HTML5 = donations only, selling needs a Downloadable build;
payouts Direct to PayPal/Stripe or Collected, $5 min). jsDelivr as the
small-file fast path (optional). Cloudflare Pages as shell-only host
(unlimited bandwidth) or Netlify free as shell mirror (bandwidth figure
uncertain under the 2025 credit system — verify at signup).

**Excluded:** full set on Pages, releases as runtime CDN, Cloudflare Pages
full set (25 MiB/file cap on all plans), Vercel Hobby (non-commercial clause),
git LFS / Actions artifacts (already excluded 2026-10-19).

**Blocked:** owner decision (split hosting vs cutting content — the
recommendation makes cutting unnecessary); R2 signup (may ask for a payment
method — owner-only per card rules); itch.io account + payout setup
(owner phone-only).

### Problem 2 — Fight goes live +126s after stage confirm (play-verify run 18)

**Cost:** owner previously called the game unplayable; the 2-min load is part
of that. 4 missing assets (404s) in the same run.

**Doc:** `research-friction-20261025/02-load-time-126s.md`.

**Verified live (2026-10-26 ~04:09 UTC):** `deploy-manifest.json` on the live
site is summary-only (7,181 files / 5,647,298,304 B — no per-file list, no
hashes), so no manifest check can run until `build_pages.py` emits a per-file
manifest. HTTP Range works on Pages (live 206 + `accept-ranges: bytes`).
Pages serves `cache-control: max-age=600` — the browser HTTP cache only holds
assets 10 minutes. three.js latest 0.186.1 (MIT); r186 release notes contain
zero KTX2/GLTFLoader entries.

**Recommended sequence (measure first, then cut):** (1) own instrumentation
in `game/js/loadperf.js` + `?loadreport` FIRST — the 126s is unmeasured and
no three.js load profiler exists to pull (stats-gl, MIT, is a dev-only frame
overlay). (2) Kill the 404s: per-file `asset-manifest.json` from
`build_pages.py` + ~100-line boot verifier (HEAD + size check, named failure,
3× retry); SRI does not apply to `fetch()`/GLB, and no lib exists for this.
(3) If network-bound: KTX2/BasisU via existing gltfpack `-tc` (ETC1S color /
UASTC normal, POT resize, own-eyes compare per fighter) + one shared
`KTX2Loader` in `game/js/assets.js`; preload next fight during the current
fight; Workbox SW + Cache Storage (Apache-2.0; its precache manifest doubles
as the §4 verifier). (4) Draco: SKIP — meshopt already wired and decodes
faster (1–3 GB/s SIMD). (5) Needle gltf-progressive (MIT): EVALUATE for
stages only (17.4 MB → 715 KB first paint is real, but needs LOD-processed
assets and buys nothing for fighters).

**Correction (parent pass, 2026-10-25):** the research doc's first draft said
the 4 missing assets were "unnamed in the handoff" — wrong. They are named in
the run-18 HTTP log (`~/workspace/_playverify-20261025/http8123.log`) and in
memory: `roster/demonio/anatomy/anatomy-layers.json`,
`game-src/js/intro-interactions.js`, `customization/parts/no-mercy/glb/body_parts/model_1171.glb`,
`customization/eye-library/eye-classic-original.png`. `game-src/js/...` looks
like a wrong-path bug (`game-src/` vs `game/js/`) — a game-lane fix. Doc
corrected before this PR.

**Blocked:** nothing above is proven to fix the 126s until the instrumentation
runs. Do not start the KTX2 re-encode of all fighters before the measurement.
Needle Cloud asset generation is a third-party service step (free tier: 30
optimizations) — owner call before any fighter GLB is uploaded to it.

### Problem 3 — Instruction-gate body failures keep recurring (parent check)

**Cost:** AO #111 and #113 (queue syncs) plus WH #1085/#1092/#1086–#1089 failed
the instruction gate on body format (missing sections, short "## Proof"
heading, deviations "None." ×5 with specified≠used, proof backticks resolving
as refs) — each failure burns a CI run and a lane round-trip.

**Verified this pass (2026-10-25):** the local gate script
`agent-ops/queue-work/instruction_gate-main.py` is **byte-identical** to the
live gate on western-heart main (`.github/scripts/instruction_gate.py`,
221 lines, `diff` clean against commit `04bbd28`); both copies in queue-work/
are identical. The PR template on main already contains all 6 required
sections with guidance. The merge-queue runs already use the local check
("Gate-format body verified 0 errors locally" appears in MERGE-QUEUE.md).
The gap is adoption: lanes that open PRs outside the queue flow never run the
check first, and neither `RESUME_BRIEF_TEMPLATE.md` nor `CHECKPOINT_PROTOCOL.md`
mentions it.

**Wired (this PR):** one standing-law line in `RESUME_BRIEF_TEMPLATE.md` —
run the local gate check on the PR body before opening the PR (pattern:
`agent-ops/queue-work/check1146.py`, `check(body, changed_files, repo_root,
labels, author)`; empty list = pass; the queue-work copy is verified identical
to live). Docs-only, no behavior change.

### Tooling-involvement note (reporting rule)

No aider/copilot/gemini CLI involvement in this pass (not installed on this VM;
verified absent). Codex not used. All research via live web sources cited in the
two docs above; all wire-ups are own-code (docs) or adopted research output,
tested as recorded. The two researchers ran in parallel as subagents; both
docs were read and verified by the parent run before this PR (including the
404-names correction above and a misread-diff check on
RESEARCH-PULLIN-INDEX.md — the file was confirmed intact, no clobber).

## 2026-10-27 — No-card fallback asset host (if Cloudflare R2 doesn't work out)

**Doc:** `research-friction-20261025/03-no-card-fallback.md` (research only, no accounts created, no cards entered).
**Problem targeted:** R2 signup stalled 2026-10-27 ~09:47 CDT at the "Add R2 subscription" step (Total Due Now $0.00, but auto-renews and bills a payment method on file); owner ordered a no-card fallback be found, plus a free-tier guard that is actually set up and saved.
**What was verified live (2026-10-27):** **Backblaze B2 is the recommended fallback** — no card at signup (name + email only; card only needed past 10 GB), 10 GB free storage (set is 5.33 GB), 5 GB single-PUT max file (largest WH file ~90 MB), per-bucket CORS rules (official docs), free egress 3x stored volume ≈ 16 GB/mo ≈ ~160 full loads/mo (Backblaze's own page). **Key finding: B2's no-card state IS a hard cap** — uploads block at 10 GB (`storage cap exceeded`, first-hand + MSP360 KB 2026-10-16), daily download/transaction caps 403 for non-paying accounts (B2 API docs), email alerts at 75%/100%; adding a card flips every cap to "No Cap", so never add one to "fix" a cap hit. **Cloudflare has NO hard cap** (official budget-alerts docs: "informational only. They do not pause or cap usage"; usage-based alerts also notify-only and can't even be created on this account yet) — the real R2 guard is size discipline (5.33 GB vs 10 GB free) + a $0.01/$1 budget alert once subscribed + weekly usage checks. Also verified: Tebi closed 2026-03-31 (dead); Scaleway needs a card to create a bucket despite 75 GB free; Oracle needs a card (own FAQ); IDrive e2's free tier is disputed (permanent-free vs trial allowance + 1 TB minimum — verify before use); Bunny.net is 14-day trial only ($1/mo minimum after); Tigris/Filebase fail on size (5 GB < 5.33 GB); Supabase 1 GB, Firebase needs Blaze/card, Storj 30-day trial + Chapter 11.
**Pulled in:** nothing (research only, per task). **Recommended:** B2 as the fallback with exact setup steps in the doc (bucket `western-heart-assets`, public, CORS `["https"]` rule, Caps & Alerts recorded in-repo); R2 stays 1st choice for its unlimited $0 egress.
**Blocked:** owner decision 2026-10-27 ~10:04 CDT: WAIT for the no-card fallback — do NOT accept R2 subscription/preauthorization terms; R2 untouched. No B2 account created — standing up B2 needs his word (research task forbade signups).
