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
**Correction 2026-10-27 (same day, ~11:09 CDT):** the doc's central claim was falsified live. Owner tapped "Stand up B2 now" (~10:20 CDT); the stand-up attempt found the account already existed (4 private buckets, Oct 9–10) and creating a **public** bucket demands payment: "A payment history is required, or pay a one-time fee ($1.00 + appl. taxes) that is credited to your account" — card fields + "Purchase and Make Bucket" button; no card entered, no bucket created. Backblaze's own help docs say the same. **Doc corrected (PR, this pass):** B2 verdict is now CONDITIONAL (public bucket needs the $1 card payment; private buckets card-free); new §4 documents the fully card-free path — **private B2 bucket + Cloudflare Worker proxy** (Worker holds the app key as an encrypted secret, signs requests, serves publicly with CORS; Backblaze's own docs; Workers Free 100,000 req/day hard stop; Bandwidth Alliance free-egress treatment for the Worker path NOT verified byte-for-byte — check B2 usage after stand-up). **IDrive e2 settled, SKIP:** IDrive's own e2 page prices "$6/TB/Month (Try with 10 GB Free)" — a trial allowance, not a permanent free tier; the "permanently free" claims describe IDrive's *backup* Basic plan, a different product. No accounts created, no cards entered in either pass.

## 2026-11-12 ~22:05–22:35 CST — Free headless image generation (all routes down) · M. Engine supervisor ~2 h deaths · 100 MB upload wrapper tested (continuous-friction-research)

**Docs:** `research-friction-20261112/01-free-headless-imagegen.md`,
`02-supervisor-deaths.md`, `03-release-upload-wrapper.md` +
`pollinations-imggen.sh` (tested) + `gh-release-upload-100mb.sh`
(tested) + live test evidence (`pol-*.png/jpg`, `cf-flux-*.json/txt`,
`upload-test-*`). Research + two tested tools only — no PRs opened by
this pass in the dirty workdir (3,024 modified entries on branch
`lindy-privacy-policy-20261107`; a clean-room clone PR is the merge
lane's step, per the 2026-10-31/11-03/11-06 precedent). No live lane
touched, nothing uploaded/deleted/restarted except the scratch test
release (created + deleted this pass). Dedupe checked via
`research-check.sh` + index (image-gen APIs, supervisor log, upload
wrapper all new; 100 MB standard, 408, starter-trap, aria2, dedup,
Kaggle-GPU-alternatives already decided — not re-researched).
**Problems targeted (from ~/memory/2026-11-11.md + 2026-11-12.md +
disk-cleanup-log, last ~24 h):** (1) every Dream Girl image-generation
route died at once — Gemini key revoked + zero image quota, Lightning
outage + CLI 403, HF ZeroGPU exhausted, Horde banned, OpenArt Turnstile
dead for human and automated clicks alike (~27 attempts); Valerie heads,
back-gap inpaint, clothed v2 all blocked; (2) M. Engine supervisor died
~10× on 2026-11-12, roughly every 2 h, 300 restarts lifetime, sender
unknown; (3) wgpl mirror lane's 1.99 GB `part00` upload stalled ~24 min
behind the egress proxy while disk sits at 80% — lanes keep using 1.9 GB
parts despite the owner 100 MB standard.
**Verified live this pass:** Pollinations anonymous text-to-image =
HTTP 200, real 512×512 JPEG in 6.0 s, own-eyes verified (anime black cat
on pink cushion; `pol-flux-test.png`, sha256 `c1e91816…ae8690e`);
Pollinations flux img2img (`?image=` param) = HTTP 200, real JPEG in
5.4 s (`pol-flux-img2img-test.jpg`); Pollinations `kontext` = HTTP 403
"isn't part of the Classic API. Use it with a pollen key"; Cloudflare
token valid (`cf_check.py` 200/200) but Workers AI call = HTTP 401 code
10000 (token-scope gap — Pages scope only); Leonardo free = web-only
(API is separate pay-as-you-go, zero free API access); Together AI free
tier gone in 2026 (deposit required); Replicate = no free tier; HF =
no token file, no HF env var on this VM; supervisor log counts: 300
starts, 166 SIGTERM-graceful, 207 stale-PID silent, only 4 watchdog
health-kills (last 2026-11-10) — the watchdog is NOT the killer;
`gh api rate_limit` core 4928/5000 (healthy); wgpl release now holds
`part01` uploaded (39,731,200 B) + MANIFEST, `part00` absent (stalled
1.9 GB POST left no trace); disk 119G/150G (80%) at 22:12 CST.
**Pulled in / wired:** (1) `pollinations-imggen.sh` — anonymous
Pollinations text-to-image + img2img with 45 s pacing, retries, and
image verification; tested live (pink diary prompt → real JPEG,
28,695 B, sha256 `b5cd302e…a8dc`). (2) `gh-release-upload-100mb.sh` —
100 MB splits, per-part state check (skip uploaded, delete `starter`,
never clobber verified), 3-attempt retry, verify by state+size+full
re-download sha256; tested live on a 120 MB file → 2 parts, both
VERIFIED (104,857,600 + 15,142,400 B, sha256 match after pull-back),
exit 0, ~5 min; scratch release `friction-test-20261112` created and
deleted after (404 confirmed), test file + parts removed.
**Recommended:** (1) lanes use Pollinations anonymous NOW for neutral
generations (intro scenes, Tammy/Janae drafts) — draft-grade Sana
quality + watermark, not a likeness tool; (2) create a free Pollinations
Pollen key (enter.pollinations.ai, signup, no card stated) → unlocks
Kontext, the likeness-holding edit route; helper already switches
endpoints on `POLLINATIONS_KEY`; (3) re-scope the Cloudflare token with
Workers AI permission → ~57 free FLUX images/day, no browser, no signup;
(4) fal.ai signup (email+GitHub) to test the $5–$20 one-time credit on
schnell + Kontext; (5) lanes adopt the upload wrapper / retire
`PART=1900000000` at the source; (6) supervisor: start with `setsid
nohup` (leaves the cron session's process group) + log death mode and
uptime per restart to correlate with cell restarts; fix the duplicate
SIGTERM log line.
**Excluded:** Leonardo free for headless use (web-only API terms);
Together AI (free tier gone); Replicate (no free tier); Stability AI
(25 credits, trivial); Gemini new-key loop (owner order 2026-11-11
19:48 CT — DEAD, not re-tested); OpenArt retry (network flagged);
supervisord/s6 second watchdog (already excluded 2026-10-28).
**Blocked / not done here:** Pollen key + Cloudflare re-scope + fal.ai
/ HF signup (account/dashboard steps, lane or owner); no Valerie spicy
image attempted through any new route (filters + visual embargo);
Gemini 08:00 CT Nov 12 quota-reset retry still has no recorded result;
no lane script modified; no in-flight upload touched; disk freed 0 by
design (nothing verified 100% yet); agent-ops docs left local pending
the clean-room clone PR (workdir dirty, 3,024 entries).

## 2026-11-15 ~23:15 EST — tmpfs render-output loss (001R 6B, twice) · zrok stable share 401 + futile restart loop (continuous-friction-research)

**Docs:** `research-friction-20261115/01-stage-as-it-lands.md`,
`02-zrok-401-restart-loop.md` + `tmpfs-guard.sh` + `stage-as-it-lands.sh`.
Research + two tested tools only — no PRs opened from the dirty workdir
(2,588 modified entries on branch `lindy-privacy-policy-20261107`); a
clean-room clone PR carries this pass, per the 2026-10-31/11-03/11-06/11-12
precedent. No live lane touched, nothing uploaded/deleted/restarted.
Dedupe checked via `research-check.sh` (tmpfs, stage-as-it-lands, zrok,
inotify — all new; 100 MB standard, gh-no-retry, 408, starter-trap, aria2,
supervisor-deaths already decided — not re-researched).
**Problems targeted (from ~/MEMORY.md + disk-cleanup-log + live state,
last ~24 h):** (1) Dream Girl 001R 6B render lost 69 finished character
frames TWICE to VM restarts because output lived in /var/tmp (tmpfs) —
and the re-render rebuilt in /var/tmp AGAIN the same night, with Blender
5.2.4 itself (1.2 GB) on tmpfs; (2) the stable live-view URL
fmmg-live.shares.zrok.io is down tonight (502) — the watchdog restarts
the zrok share every 5 min and every restart dies instantly with
`401 unauthorized; check the account token`.
**Verified live this pass:** /tmp tmpfs 512 MB (67% used), /var/tmp tmpfs
~2 GB (wiped by the 20:53 EST VM restart); 6B gate script (PID 106385,
since 22:24) running with OUT=/var/tmp/cut001r, 0 frames yet, gate waiting
(mem ~2.1 GB < 3 GB bar); gate script line 14 already says "/var/tmp is
tmpfs, NOT durable — staging IS the save" and stages per batch to the
dream-girl branch — the gap is the script + log + Blender binary on
tmpfs with no guard; `zrok2 list shares` → panic `[GET /shares][401]
listSharesUnauthorized` (live), `zrok2 list names` same 401,
`zrok2 status` shows the token SET but the controller rejects it;
zrok-share.log 03:37–04:12 UTC shows the restart→401 loop every 5 min;
`zrok-share-proxied.sh` has no 401 handling, no backoff, no stop
condition; localhost.run rotating tunnel is the working live-view path
tonight. Memory update tonight adds a third data point for the same
"lost finals" family: owner rule "any final he approves goes into the
repo/releases the SAME day" after the Cape Jones v2 dance mixes were
found lost (JP mix recovered from his phone 2026-11-15).
**Pulled in / wired:** (1) **entr 5.9** (ISC, LICENSE file read live;
5,731★) — built from source on this VM (`./configure` + `make`, cc),
installed at `~/.local/bin/entr`; smoke-tested (modify → hook runs;
`-d` exits on new file). **Found in testing: entr needs `-n` in
non-TTY sessions** (all exec/cron sessions) or it dies on terminal
attributes. (2) `tmpfs-guard.sh` — tested: /var/tmp + /tmp → UNSAFE
rc 2; ~/workspace → ok (btrfs) rc 0; nonexistent path under /var/tmp →
UNSAFE via parent check. (3) `stage-as-it-lands.sh` — polling stager
(stable-size check + restart-safe state file; --once/--drain/daemon);
tested end-to-end in scratch with a slow producer: 4/4 files staged,
sha256 match on all 4, second drain staged 0. **Two bugs found by the
test and fixed:** --once is a single sweep (documented), and --drain
first exited while the producer was still writing — now stops only when
a sweep stages nothing AND nothing is still being written.
**Recommended:** (1) 6B lane: move Blender 5.2.4 + gate script + log to
durable disk and add `tmpfs-guard.sh "$OUT" || exit 2` at gate start;
(2) render lanes adopt `stage-as-it-lands.sh` (or per-batch staging like
the 6B gate) for any output the render script does not stage itself;
(3) checkpoint protocol follow-up: tmpfs check on OUT dir at lane start;
(4) zrok: fresh enable token from the myzrok.io console → `zrok2
disable && zrok2 enable <token> --headless` (browser step — owner/main
agent), then verify `zrok2 list shares` clears 401; (5) live-view lane:
401-circuit-breaker in `zrok-share-proxied.sh` (on 401, stop restarting,
log NEEDS-REENABLE once, re-check hourly); after re-enable, check the
share count against the free 5-share limit and release stale ones from
the console if at the limit.
**Excluded:** inotify-tools (GPL-2.0 — apt broken, source build needs
autotools, absent; entr covers the slot); lsyncd (GPL-2.0 — needs lua,
absent; host-to-host sync, wrong shape); fswatch (GPL-3.0 — big C++
build for a 41 KB job); Python watchdog (Apache-2.0 — install untested);
rclone as stager trigger (no watch mode); syncthing (MPL-2.0 — needs a
peer); `zrok2 agent` as supervisor (cannot fix a dead token either);
deleting local zrok state blindly (the verified fix is disable +
re-enable); re-reserving the name `fmmg-live` (failure is auth, not the
name).
**Blocked / not done here:** 6B lane path moves + watchdog 401-breaker
(lane owners apply; both targets live); zrok re-enable (needs a fresh
console token — browser step; no token read/printed/recorded here);
Python watchdog install; inotify-tools source build. **Related finding
while verifying:** the `stream-stage.sh` PIPESTATUS bug (exit 1 after
upload under `set -u`, found 2026-11-15 ~03:35Z) is still present in the
local workdir copy — but that copy is **untracked local-only, never
committed**, so no repo PR can fix it; the overlay copy at
/opt/disk-stage-r3/ is already patched. NOT patched here: the disk-stage
round-3 lane is live and the file is its running script — lane owner to
commit-then-fix or patch in place. **Still queued from 2026-11-12:**
M. Engine supervisor `setsid nohup` fix was NOT applied (`watchdog.sh`
line 47 still plain `nohup`); deaths continue (restart 23:58:50 Nov 14).
Disk freed 0 by design (nothing verified 100%, nothing moved/deleted).
## 2026-11-18 — Live-view tunnels (zrok 401 loop, localhost.run throttled, cloudflared + localtunnel egress-blocked) · cobalt tested, FB reel still unfetched · /var/tmp adoption audit (7 hardcoded scripts)
**Docs:** `research-friction-20261118/01-live-view-tunnels.md`, `02-social-video-downloads.md`, `03-var-tmp-adoption-audit.md` + `var-tmp-audit.sh` (wired + tested, exit 1 on 7 hardcodes). Research + live tests only — no live lane touched, no tunnel restarted, no script edited.
**Problems targeted (all from the last few days, none re-researched):** (1) stable live-view URL still down — zrok 401 since Nov 15, watchdog still restarting every 5 min (~288 futile restarts/day, Nov 15 circuit-breaker never applied), and localhost.run died Nov 17 then recovered burst-throttled; (2) Júss Jåyy FB reel 1481081410582657 still has no video file after the full fallback chain v2, both TikTok candidates now confirmed DEAD in-browser; (3) /var/tmp hit 100% Nov 17 (bl524 1.2G + pb-pokemon 844M), killing the 6B gate (ENOSPC) + Pokemon pull-back, while the Nov 15 tmpfs-guard has zero lane adopters.
**Verified live this pass:** zrok stable → 502, 401 loop restarting 05:15:02 UTC; localhost.run ALIVE (registered 05:15:00 UTC, 9883eb052a5810.app.lhr.life, ssh PID 138199) but "Almost out of burst ... will be slowed"; bore already failed Nov 13 (deadline elapsed); cloudflared 2026.11.1 binary sha256-verified vs its own .deb (97bb3b02… identical) but quick tunnel fails — api.trycloudflare.com POST → HTTP 403 "Your request was blocked" through the egress proxy; localtunnel never issues a URL (server.localtunnel.me empty reply); cobalt co.wuk.sh POST times out 40 s / 0 bytes, api.cobalt.tools → HTTP 400 error.api.auth.jwt.missing; yt-dlp s5 stall process gone, FAILED.md written; /var/tmp 60% + /tmp 89% at audit time; audit: 7 HARDCODED + 3 OVERRIDABLE scripts.
**Pulled in / wired:** `var-tmp-audit.sh` — bounded *.sh sweep classifying /var/tmp use as HARDCODED / OVERRIDABLE / GUARDED / MENTION, exit 1 on hardcodes; tested live on agent-ops (7/3, exit 1, matches manual grep).
**Recommended:** (1) live-view lane: apply the Nov 15 401 circuit-breaker (queued a third day running); owner decision: zrok re-enable (free, fresh console token) vs localhost.run paid custom domain (stable + priority bandwidth); (2) this reel: run the queued signed-in browser DevTools network capture — no more downloader lanes; the gap is a cookie bridge (signed-in browser session → VM-side downloader), not a downloader; (3) quezada driver owner: PB env-override like pokemon's before the next pull-back (reassembled 2.4G vs 2G tmpfs by its own comment); 6B lane: move Blender/gate/log off /var/tmp (open since Nov 15); guardian: run var-tmp-audit.sh on cadence.
**Excluded:** cloudflared Quick Tunnel + localtunnel from this VM (egress-blocked, not vendor-broken — re-test if the egress allowlist changes); cobalt hosted API (unreachable / JWT-gated; self-host gated on the cookie bridge, and useless for this login-gated reel); bore (already failed Nov 13); gallery-dl / tikwm / Tikdown / fdown / Getfvid for this reel (already failed or same cookie wall); ngrok free (account + warning page, weaker than localhost.run).
**Blocked / not done here:** zrok re-enable (needs a fresh console token — browser step); no live-view script edited; no cloudflared binary installed persistently (blocked tool, 40 MB); no paid plan taken; no video file obtained (motion study stays blocked); no cookies read/exported; no lane script edited; no /tmp or /var/tmp contents deleted (/tmp 89% flagged, guardian owns it).
## 2026-11-21/22 — (RETRO NOTE, added 2026-11-24: this pass was never logged)

Docs exist but no log entry was written at the time:
`research-friction-20261121/01-live-view-tunnel.md`,
`02-chromium-headless.md` + `playwright-chromium-smoke.py` +
`tunnel-health-check.sh`. Summarized here from those docs only, not
re-researched: (1) live-view dead on BOTH routes — zrok 401 (token dead
~6 days, last successful serve 2026-11-15T19:07Z), localhost.run 502
relay-side; tunnl.gg tested live twice, FAILED (edge never forwards,
SSH dies in ~4 min) — do not wire; (2) "Chromium dead VM-wide" is
WRONG — Playwright's bundled Chromium 1243 launches headless, WebGL
1.0 via SwiftShader works, red-triangle screenshot verified with real
pixels counted; capture/proof lanes should use Playwright Chromium,
not a system binary. This retro note closes the log gap; the 11-21
findings themselves stand as documented in their files.

## 2026-11-24 ~23:05–23:55 EST — Manifest gap (guardian can't clear ~3.5G idle workdirs) · 52 UNSTABLE PRs = broken no-deletion-guard · Tailscale Funnel excluded (continuous-friction-research)

**Docs:** `research-friction-20261124/01-manifest-gap.md`,
`02-ci-unstable-guard.md`, `03-tailscale-funnel-excluded.md` +
`manifest-gen.sh` (wired + tested). Index updated
(RESEARCH-PULLIN-INDEX.md). No PR opened from the dirty agent-ops
workdir (standing precedent — clean-room clone PR carries it). No
live lane touched; nothing stored, moved, or deleted.
Dedupe checked via `research-check.sh` (manifest generator, tailscale
funnel, ci unstable pr checks — all new; restic/aria2/zstd/croc,
zrok 401 loop, tmpfs-guard, supervisor deaths already decided — not
re-researched).
**Problems targeted (from MEMORY.md + disk-cleanup-log + live state,
last few days):** (1) disk stuck at 72% (107G/150G) with ~3.5G of
idle lane workdirs that the guardian re-lists every 10 min and can
never clear — all BLOCKED on "no per-file stored manifest", which no
tool generates; (2) merge-law-ci-watch 2026-11-24 22:57 EST: 58 PRs,
ZERO CLEAN, 52 UNSTABLE — the watch lane can only see the word
UNSTABLE, never why; (3) stable live-view URL still down (zrok 401,
owner sign-in pending) — is Tailscale Funnel the untried stable
route?
**Verified live this pass:** disk 72% (107G/150G, 43G free) at
23:05 EST; guardian's blocked set unchanged (dream-girl 18G active,
`_adri-performance-v2-20261109` 353M/984 files unmirrored, ~3.5G cut
lanes, all no-manifest); guard manifest format read from
`disk-clear-guard.sh` (one relative path per line, .git excluded);
**rclone is GONE from this VM** (`~/workspace/tools/rclone/` absent,
`which rclone` finds nothing — tools/ archived 2026-10-31, never
restored; the index's "rclone LANDED" entry is stale); hashdeep /
git-annex not installed; stdlib sha256sum/sort/find all present
(sha256sum `-z`/`-c` supported). CI sample: no-deletion-guard fails
on EVERY pull_request run since ~Oct 15 in 4/4 sampled repos
(chimera-roms, box-storage, wizard-gang-storage,
Physics-sandbox-playground-), one success ever (box-storage Oct 14,
the PR that added the guard); workflow file unchanged since Oct 14;
chimera-roms #5 (1 file, 0 deletions) and #8 (1 file added, 0
deletions, MERGED) both fail it — the guard fails on deletion-free
PRs. Check-runs API 403s (PAT lacks checks:read), commit-status API
returns `pending` with zero statuses, job steps come back empty, job
logs 404 even for a 2-day-old run — the failure reason is not
retrievable from this VM. Genuine separate failures also found:
M.-Engine- #21 `build_and_verify` FAILURE; AshLanev2 Nov 22
validation / asset-validation (job `glb`) / Deploy-PWA failures.
Tailscale: binary present but `Not connected`, `funnel` subcommand
unrecognized, and the connector doc forbids the route by design
(client-only, "accepts none, hosts nothing", no upstream client).
**Pulled in / wired:** `manifest-gen.sh` — paths mode
(guard-compatible), `--hash` (sha256sum format), `--verify` (exit 0
clean / 1 tampered), atomic `--out` (temp+rename, quota-cut safe),
`.git` excluded by default, symlinks skipped with count, unreadable
files fail closed (exit 2, no manifest written). Tested live:
scratch tree correct incl. spaces/hidden/symlink/.git; `--verify`
exit 0 clean, exit 1 on tampered file; guard [manifest] leg PASSES
with its output (only [recency]+[git-dirty] blocked, correctly);
scale run on the real `_adri-performance-v2-20261109/` (353M):
984 lines in ~10.7s, stdout-only, no manifest file written; as
`nobody`, unreadable files → exit 2 with per-file reports. One bug
found by testing and fixed: unreadable *directory* used to die
silently (rc 1, no message) under `set -e`+`pipefail` — now a
`[ -r ] && [ -x ]` pre-check dies with a clear message (verified
live as `nobody`).
**Recommended:** (1) guardian lane: run `manifest-gen.sh --hash` on
each idle workdir, use the hash manifest as the basis for
store-verify (upload → pull-back → compare sha256), then the paths
manifest becomes a real `--stored-manifest` and the guard can finally
evaluate migrate/clear; (2) guard fix: open chimera-roms run
45039968566 in the browser and read the `guard` job log (the failing
step is the answer), or get a token with checks:read — the fix is
likely BASE/HEAD resolution or deleted-branch checkout handling, NOT
weakening the guard; after the fix, re-count the 52 UNSTABLE — a
large share may flip CLEAN with no code change; (3) rclone restore
from `tools-archive-2026-10-31` if any lane needs it (not required
for manifests); (4) Tailscale: do not re-research for live-view —
the connector doc settles it; stable URL stays zrok re-enable (owner
sign-in) vs localhost.run paid domain.
**Excluded:** hashdeep / git-annex (heavier than the job; stdlib
covers it); Tailscale Funnel (connector design limit); re-cloning
into /tmp for the guard reproduction (clone died ENOSPC — /tmp is
512 MB tmpfs; use durable disk or the compare API).
**Blocked / not done here:** no manifest file written for any real
workdir (only the guardian lane should bless one as a stored-manifest
basis); no guard workflow edited; no PR touched/labeled/merged; no
token minted; no zrok/live-view change; no rclone restored. Disk
freed 0 by design (nothing verified 100%, nothing moved/deleted).
