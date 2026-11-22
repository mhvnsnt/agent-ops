# FRICTION RESEARCH — recurring problems, real fixes

**Owner order:** 2026-10-19 ~23:03 CDT — keep researching what helps with the problems we keep running into; pull open-source/free/industry-standard stuff; whole team working; faster, more optimized, higher quality, fewer stalls and hiccups.
**Method:** six independent researchers, one per problem cluster. Live docs/repos/issues only — nothing from training guesses. All six cluster docs: `~/workspace/agent-ops/research-friction-20261019/01–06-*.md`. Index: [[RESEARCH-PULLIN-INDEX]].
**Wiring status (honest):** all six clusters delivered research + concrete wire-up plans, no PRs opened by researchers — the code targets (CloudDog repo, agent-ops lanes) have a live straight-to-store build lane and running daemons in them tonight; opening code PRs blindly would collide. Findings are entered in the index as **queued pull-ins with named owners** per the research conventions — the integration lane wires them after check-before-start.

---

## 1. Flaky egress proxy — resilient transfer

**What we hit:** connection refusals, empty responses, transient gh 401s, stream CANCELs. All uploads >485MB failed; 100MB-via-curl proven working; lanes die on flakes instead of riding through.

**What research found** (`01-resilient-transfer.md`):
- **`gh` CLI does NOT retry transient failures** (no `--retry` flag; go-gh single-attempt client). The whole ecosystem wraps it — so CloudDog's `_run_gh` *is* the retry layer and it's too weak (3× fixed 2s, misses connrefused/429).
- **The backend pushes the wrong size class:** `github.py` splits at 2GiB while our own evidence says >485MB dies and 100MB works. Fix = drop `SPLIT_BYTES` to 100MB.
- aria2's deeper flags were mapped (`--retry-wait=10 --max-tries=0 --auto-save-interval=30 --always-resume=true --conditional-get=true`); rclone flag bundle (`--retries 10 --retries-sleep 30s --low-level-retries 20 --timeout 300s`); curl stall-killer template (`--retry-all-errors --retry-connrefused --speed-limit/--speed-time` → stall becomes exit 28 → retry, not lane death).
- Proxy-env hygiene: the `no_proxy` IPv6-literal quirk in `~/TOOLS.md` explains one "empty response" class — a `_proxy_env()` sanitizer for all subprocess spawns.
- Skipped as dependencies: tenacity, backoff, wget, Go retry libs — CloudDog's stdlib-only law stands; port the patterns (new stdlib `retry.py`: exponential + jitter + transient/permanent classifier + `max_elapsed` storm bound), not the packages. tus protocol skipped (no tus server on the GitHub side) — but our 100MB+sha256+manifest *is* the tus shape.

**Wire-up plan (W1–W6):** stdlib `retry.py` → beef up `_run_gh` (8 attempts, exponential+jitter, give-up on true 401) → 100MB `SPLIT_BYTES` → aria2 flags in `_aria2c_fetch` → `_proxy_env()` everywhere → terabox/drive subprocess wrapping → curl template in verify/download paths.
**Owner / status:** queued — CloudDog integration lane (check in-flight lanes first).

## 2. GitHub API limits — big artifacts

**What we hit:** blob API 422s above ~10MB; `gh release upload` silently renames dotfiles; signed URLs expire mid-stream; manifest-less final trees caused the Scooby empty-tree 422.

**What research found** (`02-github-limits.md`):
- **Releases are the right store — GitHub's own docs:** <2GiB/asset, up to 1000 assets/release, and *"no limit on the total size of a release, nor bandwidth usage."* Our 100MB-chunk pattern has no documented ceiling against it.
- **git-lfs is a hard NO — cost math:** 10GiB storage + 10GiB/month bandwidth included, then $5/50GB pack, metered on *every download*. Our law requires download+hash retrievability proofs — a few dozen 4.8GB proofs burn the free quota; metered forever on reads. Releases are unmetered. Also LFS per-file 2GB cap blocks our biggest ISOs.
- gh-large-releases (ading2210) is the industry reference for chunk+manifest+verify — adopt the *pattern*, not the code (license unverified).
- CloudDog's re-resolve-on-403 matches the documented asset-download contract (re-hit API endpoint per fetch, never cache redirect). Validated — keep.
- Blob API docs claim 100MB; our lanes 422 above ~10MB — treat our figure as real, docs as aspirational. Skip the blob API for parts.
- Rate-limit budget: ~2–3 API calls per 100MB part; 100GB ≈ 3,000 calls fits the 5,000/hr personal budget but the daemon shares the token with other lanes — throttle to ≤8 concurrent uploads, never tight-loop retries.

**Wire-up plan:** manifest.json as release asset + manifest-first finalization (Scooby lesson into law) → unify 100MB chunk quantum across store()/mirror → bounded-parallel part uploads with chunk-level resume → explicit 403-re-resolution wrapper → adopt gh-large-releases manifest schema → per-part verify shortcut.
**Owner / status:** queued — CloudDog integration lane. Two open questions for parent: (1) 100MB as single standard for both store() and mirror? (2) full re-download verify vs part-manifest shortcut?

## 3. CI pain — maxed minutes + flakes

**What we hit:** Actions maxed at 2,000/2,000 min; runner flakiness; one real recurring flake: sqlite "database is locked" in `test_concurrent_upserts_are_safe`; 75+ PRs stuck.

**What research found** (`03-ci-flakes.md`):
- **Root cause of the sqlite flake (read in the actual code):** WAL + busy_timeout=30000 already set — the naive fix is exhausted. Python's sqlite3 starts DEFERRED transactions; a DEFERRED read upgrading to write returns `SQLITE_BUSY` *immediately, bypassing busy_timeout* (deadlock avoidance). Plus `_open_db()` runs schema DDL on **every fresh connection** — the 20-thread test stampedes DDL. Fix: `BEGIN IMMEDIATE` on write paths + app-level retry with backoff + serialized schema init. **Do NOT add pytest-rerunfailures** — the flake mirrors a real daemon race; hiding it hides a production bug.
- **CI minute diet (zero-risk YAML):** concurrency-cancel on PRs, timeout-minutes 15 (default 360 is a billing hazard), path filters, matrix trim to nightly, caching, retention 7d. Pure YAML, staged on highest-burn repos first.
- **Self-hosted runner: $0/min for private repos** (planned $0.002/min postponed, not in effect). Oracle ARM box as host: 2 OCPU/12GB (halved June 2026 — old guides wrong), 200GB block, 10TB egress, free forever — **but:** card required at signup, idle reclaim (95th-pct CPU+net+mem <20% over 7 days — a mostly-idle CI runner is genuinely at risk), chronic ARM capacity errors, home region locked forever, unexplained signup rejections. Ephemeral-per-job, private-repos-only, kill-switch back to hosted.
- Skipped: SourceHut (paid), Cirrus/Codeberg (OSS/FLOSS only), CircleCI (still metered), GitLab/Jenkins/Woodpecker-hosted (migration tax, no win), StarSling (per-minute is the wrong direction), FlakeFighters (minutes-expensive, root cause known).

**Wire-up plans:** Plan A = CloudDog sqlite flake fix (proof: 20/20 stress-loop green); Plan B = minute-diet YAML via merge-law-ci-watch lane; Plan C = self-hosted runner, **blocked on OWNER decision** (card required — never auto-signup).
**Owner / status:** A queued — CloudDog integration lane; B queued — merge-law-ci-watch lane; C blocked on owner.

## 4. Lane resilience — restarts kill work

**What we hit:** daemon/runtime restarts kill lanes mid-work; stale checkpoints; resume duplicates or misses work; the worker-watchdog can't tell "dead" from "slow."

**What research found** (`04-lane-resilience.md`):
- **Delivery model decision: at-least-once with idempotent units.** True exactly-once for agent side-effects isn't achievable without a transactional coordinator spanning every tool; the survivable side is never-lose-work + idempotent units. Write it into `CHECKPOINT_PROTOCOL.md`.
- **Core gap = liveness is not progress.** Fix: `progress_seq`/`last_progress_at` checkpoint fields + a STUCK bucket in supervisor.sh (heartbeat fresh, progress frozen) — surface STUCK, re-spawn only DEAD.
- **Fencing tokens (Kleppmann)** — the single highest-value change: monotonic `epoch` in checkpoints; any write carrying an older epoch is rejected. Kills the paused-agent-wakes-and-overwrites corruption class outright.
- **systemd user units VERIFIED UNAVAILABLE on this VM** ("Failed to connect to bus") — skip; supervisord/s6/runit skipped on cost/benefit (PID-file + keepalive cron already covers the 90% case); Temporal/DBOS skipped (server/DB prerequisites absent — their semantics imported as patterns 1–4).
- Dead-man's switch inverted locally: worker-watchdog writes its own ok-ping; the disk guardian alerts if it goes stale. No external hosted monitor (lane metadata never leaves the box).

**Wire-up plan (W1–W6):** progress fields + STUCK bucket → `checkpoint.sh claim` with lease + fencing → watchdog claims before spawning → CloudDog daemon health = progress (cycle_seq advancement, not pid-alive) + restart backoff → append-only `journal.jsonl` per task → fsync hardening.
**Owner / status:** queued — checkpoint infra lane (agent-ops) + CloudDog daemon owner. Open question: claim-registry (cluster 5) and checkpoint claim are the same mechanism from two sides — integrate as ONE claim format.

## 5. Lane coordination — work claims (the T5 fix)

**What we hit:** a cleanup lane deleted an in-progress Tekken 5 ISO download. `is_inflight()` is a 5-min-mtime heuristic — a paused download slips through; `.DO_NOT_DELETE` markers are static; nothing machine-readable says "lane X owns this path."

**What research found** (`05-lane-coordination.md`):
- Adopt: `flock(2)` (kernel auto-release on fd close — no stale locks), Python `filelock` (public-domain per listing) for the reaper, `O_CREAT|O_EXCL` + PID-liveness stale-check rules (EPERM = alive), Kleppmann lease + fencing-token model, sqlite WAL as the store.
- Skip the tools, keep the models: etcd leases (no etcd in the shop), lockfile-progs (GPL), GitHub Actions/Jenkins/GitLab concurrency (pattern references only).

**Wire-up plan — `claims` table in the EXISTING sqlite v4 registry (no second registry):** `path` PK, `owner`, `action`, `claim_id` (uuid4, fencing anchor), monotonic `epoch`, `claimed_at`/`heartbeat_at`, `ttl_s` default 600 (heartbeat at TTL/3, etcd practice). API: `claim` / `heartbeat` / `release` / `is_claimed` (ancestor-prefix coverage) / `expire_sweep`, all claim_id-guarded. **Hard gates:** `reap_candidates()`/`cmd_reap` in `cloud_dog.py`, `Reaper._try_reap` in `src/clouddog/reaper.py:193`, the straight-to-store mode, plus `python -m clouddog.claims check <path>` CLI for non-CloudDog sweep lanes. Download lanes claim on start, heartbeat, release on completion. Fail closed if the registry is unreadable. Reapers defer/skip on a live claim — never wait, never delete.
**Owner / status:** queued — CloudDog integration lane. Design is the same claim format cluster 4 needs — integrate once.

## 6. Browser-transfer alternatives — pulling without the browser

**What we hit:** TeraBox .blend downloads failed 10/10 via the browser file-transfer tool. Lanes need files FROM TeraBox shares without the browser path.

**What research found** (`06-browser-transfer-alternatives.md`):
- **No native rclone TeraBox backend exists** — verified against rclone.org/tiers, pkg.go.dev (v1.64, v1.68.2), Batocera list. TeraBox publishes no OAuth API, no WebDAV, no export tool. Stop looking.
- **AList is the strongest find** (alist-org/alist, AGPL-3.0 — service use OK, never vendored): native TeraBox driver (cookie-based, jsToken validation) + PikPak/BaiduNetdisk/Quark; serves everything as WebDAV → rclone's Tier-1 WebDAV backend. Chain: TeraBox → AList → WebDAV → rclone → CloudDog stores.
- **rclone PikPak backend exists** (added v1.62, MIT): username/password, MD5, multipart, `backend addurl` for offline-download tasks. The gigaleak loop should document this as the reference pattern.
- **rclone is NOT installed on this VM** — the single highest-leverage quick win.
- Cookie-export → aria2 (`-c -x16 -s16 --load-cookies=cookies.txt`) is the production pattern for large authenticated pulls; cookies live in /tmp or the vault flow, never committed; fail-fast "refresh cookies" on expiry.
- yt-dlp (`-g`) + gallery-dl (`-g`) become the generic "give me the direct link" lane standard for non-TeraBox hosts — yt-dlp has no TeraBox extractor, honest limit.
- terabox-downloader (PyPI, MIT): unofficial scraper, watchlist. terabox-gateway: license unverified, cookie-rotation pattern worth copying. JDownloader2: skip (heavyweight).

**Wire-up plan:** install rclone ≥1.62 everywhere → AList→WebDAV→rclone bridge (Secure Vault cookies) → cookie→aria2 SOP script (`tools/dl/tb-pull.sh`) → document the PikPak loop → yt-dlp/gallery-dl as lane standards → delete-as-you-go discipline.
**Owner / status:** queued — CloudDog integration lane (rclone install + AList bridge need a lane with browser access for the cookie capture).

---

## Consolidated pull-in queue (status per research conventions)

| # | What | Where it lands | Owner | Status |
|---|---|---|---|---|
| 1 | stdlib `retry.py` + transient classifier | CloudDog `src/clouddog/` | CloudDog integration lane | queued |
| 2 | `_run_gh` retry hardening + `SPLIT_BYTES` → 100MB | CloudDog `src/clouddog/stores/github.py` | CloudDog integration lane | queued |
| 3 | aria2 resilience flags + `_proxy_env()` sanitizer | CloudDog `cloud_dog.py` + `src/clouddog/` | CloudDog integration lane | queued |
| 4 | manifest.json as release asset + manifest-first finalization | CloudDog `src/clouddog/stores/github.py` | CloudDog integration lane | queued |
| 5 | Bounded-parallel part uploads (4–8 workers, chunk-level resume) | CloudDog `src/clouddog/stores/github.py` | CloudDog integration lane | queued |
| 6 | 403-re-resolution wrapper on downloads | CloudDog `src/clouddog/stores/github.py` | CloudDog integration lane | queued |
| 7 | gh-large-releases manifest schema (pattern, not code) | CloudDog docs/manifests | CloudDog integration lane | queued |
| 8 | BEGIN IMMEDIATE + app retry + serialized schema init (sqlite flake) | CloudDog registry | CloudDog integration lane | queued |
| 9 | CI minute-diet YAML | highest-burn repos | merge-law-ci-watch lane | queued |
| 10 | Self-hosted runner on Oracle ARM | new infra | **owner decision** (card) | blocked |
| 11 | Checkpoint progress fields + STUCK bucket + fencing-epoch claims | agent-ops checkpoint infra | checkpoint infra lane | ✅ landed 2026-10-20 ~01:25 CDT — `checkpoint.sh` claims+fencing, `supervisor.sh` STUCK bucket, watchdog 9b step, SOP doc, 19 tests green |
| 12 | Append-only `journal.jsonl` + fsync hardening | agent-ops checkpoint infra | checkpoint infra lane | queued |
| 13 | `claims` table in CloudDog registry + reaper hard gates | CloudDog | CloudDog integration lane | queued |
| 14 | `clouddog claims check` CLI for non-CloudDog lanes | CloudDog | CloudDog integration lane | queued |
| 15 | Install rclone ≥1.62 on the VM + lane SOP | VM / agent-ops `tools/` | CloudDog integration lane | queued |
| 16 | AList → WebDAV → rclone bridge (TeraBox pull path) | infra (service) | CloudDog integration lane (+ browser lane for cookie) | queued |
| 17 | cookie→aria2 SOP script `tools/dl/tb-pull.sh` | agent-ops `tools/` | CloudDog integration lane | queued |
| 18 | yt-dlp/gallery-dl as lane-standard direct-link step | lane runbooks | any lane (SOP) | queued |

**Excluded with reasons (documented, not forgotten):** tenacity/backoff/resumable-upload as deps (stdlib-only law — patterns ported), wget (curl+aria2 cover it), git-lfs (metered bandwidth), Actions artifacts (90-day cap), blob API (proven 422s), gh extensions (none exist), pytest-rerunfailures as fix (hides a real bug), SourceHut/Cirrus/Codeberg/CircleCI/GitLab/Jenkins/Woodpecker-hosted (paid, OSS-only, or migration tax), supervisord/s6/runit (cost/benefit), systemd user units (unavailable on this VM), Temporal/DBOS (server/DB prerequisites), etcd (no etcd in the shop), lockfile-progs vendoring (GPL), Healthchecks tool (local inversion instead), kopia/borg/bup/git-annex (per earlier index), JDownloader2 (heavyweight), Ronnie7866 Spring downloader (heavyweight).

**Honestly blocked:** Oracle ARM signup + Modal credits (cards required — owner only); terabox-gateway license (unverified); gh-large-releases code license (unverified — pattern only); exact expiry time-of-day on TeraBox billing (account page shows date only).

**Cross-cluster note:** clusters 4 and 5 converged on the same mechanism — a claim record with TTL + heartbeat + fencing epoch. Integrate once, not twice. The straight-to-store CloudDog mode currently building should claim its destination path at start (it will write into the registry that already holds the claim table).
