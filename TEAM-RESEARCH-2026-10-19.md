# WHOLE-TEAM RESEARCH — 2026-10-19

**Owner order:** 2026-10-19 ~20:00 CDT — use all free resources, all agents/IDEs, keep upgrading CloudDog, keep cleaning disk, figure out what else is priority, get the whole team researching.
**Method:** four independent researchers, read-only, no code changes, no deletes. Findings verified against real docs/repos/commands, not single sources.
**Freshness:** disk/process figures gathered ~20:27–20:45 CDT 2026-10-19. Things move fast — re-check numbers before acting.
**Note:** the priority-scan worker was killed by a daemon restart mid-delivery; its findings were recovered verbatim from its session log. Nothing was altered.

---

## PART 1 — PRIORITIES, ranked by impact-per-effort

### P1. 🔴 Disk at 93% and climbing — cleanup is losing to concurrent writers
- `df`: 100G total, **91G used, 7.9G free, 93%** (up from 89% at 20:06). Guardian logged **+15G growth since 16:00**, "entirely from ACTIVE work," and found **zero safe-clear targets**; CloudDog enforce ran `--apply` 3× tonight and reaped **0 bytes** (registry empty of eligible entries).
- Top consumers: `cape-jones` 6.9G, `western-heart-main` 5.0G, **`wt-autoseat` 4.1G + `wt-sitcanon` 3.9G + `wt-mocapsit` 3.9G = 11.9G in three parallel sitting-lane worktrees**, `viggle-inputs` 3.1G, `agent-ops` 3.0G, `star-rig-work` 2.9G, `game-reverse-engineering/tekken5` 4.2G (game file — protected), `tripo-downloads` 1.1G.
- **Biggest immediate swing (addendum):** `~/workspace/.tmp-srw` (2.9G: `star-rig-work.tar.00`–`.05` + MANIFEST + SHA256SUMS) is the upload source for the in-flight `gh release upload star-rig-work-archive-20261019`. Once that upload verifies, **both** `.tmp-srw` and the source `star-rig-work` (2.9G) become clearable — **~5.8G in one move** via delete-as-you-go. Lane A: watch for the upload's exit and reap both immediately.
- **Fastest structural recovery:** when one sitting take wins, the other two worktrees (~8G) become reapable in one move. **Needs the owner's pick** (PR #159 sign-off pending) — lane A cannot decide this.
- `~/workspace/terabox-staging` (711M: `game-re/` 704M, `probe/` 5M) = leftover browser-upload staging, files dated Oct 14–18, likely unaudited. Lane A: audit against TeraBox receipts before reaping — staged-but-not-uploaded files must NOT be treated as mirrored.
- Structural note: `du -sh ~/workspace` = 99G vs df 91G — many full local clones/worktrees of the same repos (cape-jones `.git` alone is a 4.7G partial clone) inflate the footprint. Fewer, shallower clones is a standing fix.

### P2. 🔴 TeraBox Premium trial expires TOMORROW (2026-10-20)
- Trial ($0.50/7d, 5TB) expires 2026-10-20; owner's plan was to upgrade **today (2026-10-19)**. Unverifiable read-only from here — needs a browser/account check.
- If it lapses, CloudDog's verify-then-delete, the continuous mirror, and every pending clear lose their 5TB home — cleanup stalls at the verify step while disk sits at 93%.
- **Action: confirm with Real tonight; if not done, run the browser lane to complete the upgrade.** This is the single highest-leverage owner action on the board.

### P3. 🟠 In-flight work healthy, but three disk-hungry lanes writing on a 93% disk
- `ps aux`: 36 processes, zero defunct. Healthy: `gh release upload star-rig-work-archive-20261019` (8+ min), `pull_lane2.py` (40 min, now chunking a **7.2GB `nick.7z`**, 69 chunks), Blender `star_twerk.blend` render (13 min in), Doc Frank A4 decimate, watermark-removal + ffmpeg pipeline, CloudDog dashboard on :8911.
- No intervention (NEVER-KILL law) — monitor only. Any one failing on a full disk corrupts a chunk/render. Lane A: star-rig-work's clear must wait for upload verification.

### P4. 🟠 merge-law-ci-watch: 75 PRs stuck, but only ONE real code conflict — the watch doc is stale
- 19:57 run: 114 PRs checked → 39 merged, **71 OPEN UNSTABLE (CI runner outage), 3 BLOCKED, 1 DIRTY, 0 CLEAN**.
- **Only real blocker:** `Physics-sandbox-playground #5` — DIRTY/conflicting, needs manual resolution.
- BLOCKED: `BioMechania #26`, `ConcreteDragon #59` (branch protection), `ConcreteDragon #61`.
- **Duplicate:** ConcreteDragon has TWO open anti-clobber PRs — #60 (not on watch list) and #61. One is redundant; closing needs a parent/owner call.
- **Stale doc:** cron file still lists western-heart #234/#253/#263/#265/#268/#271/#273/#275/#291/#295 and GMSS #31 as pending — all MERGED (GMSS 1311-file recovery landed ✅). Suggest pruning the doc to the 75 in `remaining.txt`.
- Caveat: PAT lacks `checks:read`; judged by `mergeStateStatus` only.

### P5. 🟡 One CI failure is NOT the outage — western-heart instruction-gate
- `mhvnsnt/western-heart`, run 2026-10-20 01:14 UTC, branch `feat/stream4-modes-menus-20261019`: only failing job is `instruction-gate` ("Check PR body against the instruction gate") — a PR-body policy failure, independent of the outage. Check the gate log if its PR is still live. Everything else CI-red is outage noise — don't chase CI until the outage clears.

### P6. 🟡 Paused lanes holding uncommitted work — at risk from aggressive reaps
- `charfix-worker-batch3` (PAUSED): 4 of 5 repaired GLBs **modified-but-uncommitted** — a worktree reap would silently lose them. Commit/stash first (small, do first).
- `concrete-dragon-improve-loop` (PAUSED): loop not running; its PRs #59/#61 are in the BLOCKED trio. Resume or formally park.
- `tekken5-teardown` (RUNNING, healthy): ISO 100% downloaded, archive mapping ~40%, decrypt 0% — on track.
- `wh-ttt2-100` (RUNNING, sequenced behind disk): needs to re-pull 13.3GB TTT2 7z from release `ttt2-7z-v1` — can't start until P1 frees ~14G.

### P7. ⚪ Bannon PR rot — real, lowest leverage tonight
- #22 (104 days), #38 (76d), #39 (48d), drafts #43/#44, #48/#49 (11d). #78 correctly untouched (stays draft). One triage pass could close ~5; nothing blocks on it tonight.

---

## PART 2 — TOOLING PULL-INS (for CloudDog / the operation)

Already wired: rclone, dust, fclones, libtorrent. Licenses verified against each project's own repo.

**PULL IN:**
| Tool | License | Fills the gap |
|---|---|---|
| **restic** | BSD-2-Clause | Snapshot/backup layer — the only candidate whose backend is **rclone itself** (TeraBox route included); `restic check` gives CloudDog a real integrity-verification primitive. Single static Go binary, no root/daemon, v0.19.1 (Jul 2026) |
| **aria2** | GPL-2.0 | Segmented multi-connection HTTP fetch — CloudDog's download side is libtorrent (torrents) + rclone (cloud); neither does multi-connection HTTP for throttled mirrors (game ISOs, release assets). Invoke as external binary (no GPL code mixing) |
| **zstd** | BSD-3-Clause (dual BSD/GPLv2 — take BSD) | Staging compressor everywhere tarballs/chunks are staged — best speed/ratio in class, and it's already the codec inside restic/kopia/borg, so one format end-to-end |
| **croc** (narrow) | MIT | Ad-hoc encrypted VM↔device transfer without a cloud hop, resumable. Self-host `croc relay` for sensitive payloads (default relay is third-party) |

**SKIP (honest reasons):**
| Tool | Why not |
|---|---|
| kopia | Same job as restic, **no rclone backend** — disqualifying in this stack |
| borgbackup | Local/SSH only; cloud needs rclone-mount workaround; single-threaded |
| bup | No encryption, no cloud backends, near-dormant maintenance |
| git-annex | Interesting registry idea, but AGPL/GPL-3+ core + heavy Haskell + steep ops; CloudDog's registry already covers it |
| rmlint / rdfind | Pure overlap with fclones (already wired and faster) |
| duperemove | **Hard dealbreaker:** kernel dedup only works on btrfs/XFS — reclaims nothing on a standard ext4 VM volume |
| pixz / lbzip2 | Legacy formats; zstd beats both on speed and ratio |
| syncthing | Daemon-only continuous two-way sync **fights** the disk-as-cache / verify-then-delete doctrine; rclone bisync already covers scheduled sync |

---

## PART 3 — SCALE / EXPAND (ranked by payoff-per-effort, 2026 sources)

1. **Cloudflare free stack as edge/distribution** (S–M effort / L payoff) — Pages (unlimited static), Workers (100k req/day), **R2: 10GB, zero egress ever**, D1/KV/Workers AI. $0 egress is the killer feature vs S3 (~$90/TB). Free public download hub for Western Heart builds + asset packs; Workers cron for job queues. No card required.
2. **Hugging Face Spaces as demo storefront** (S / M) — 2 free ZeroGPU Gradio Spaces (H200, ~3.5–5 min/day) + unlimited Static Spaces; free public model/dataset hosting. Visibility, not compute (cpu-basic now paywalled; quotas tiny).
3. **itch.io page for Western Heart demos** (S / M) — free publishing, 0%-optional rev share. Audience-building + PWYW tips; HTML5 games can only take donations (must be Downloadable to charge).
4. **YouTube pipeline for Wizard Gang** (S–M / M–L) — **closest to the next real dollar.** YPP: 1k subs + 4k watch hours, or 500 subs for fan funding. He's already producing episodes/clips — repurposing is packaging, not new production. Flag: one 2026 source says thresholds rise Feb 1 2027 (8k hrs / 20M Shorts) — unconfirmed, treat as "get in before Feb 2027."
5. **Oracle Cloud Always Free as permanent second box** (M / M) — 2 OCPU/12GB ARM (halved Jun 2026 — old "4/24" guides wrong), 200GB block, **10TB/mo egress**, free forever. Home for cron workers/build queues/mirrors. Catches: ARM capacity errors, idle reclaim, **card required at signup**.
6. **Modal $30/mo recurring GPU credits** (M / M) — ~50 T4-hrs/mo, scale-to-zero, Python-native. **Catch: payment method required to use at all — opt-in only, his call, never automatic.**
7. **Kaggle public datasets as publishing channel** (S / M) — cleaned teardown *derivatives* (metadata, rig mappings, format docs), never raw proprietary assets (steal-like-an-artist boundary).
8. **Fab (Epic marketplace) for original 3D asset packs** (M–L / M) — **88% creator share** (best in industry); his Tripo/superhero piece library is a real product line. Sell original/transformed work only.

**Combos that multiply:** Oracle ARM + self-hosted GitHub Actions runner → free CI again (bypasses the maxed 2,000-min cap); R2 as zero-egress origin behind itch/HF demos; funnel **YouTube → itch.io → Fab** on $0 platform costs.
**Hype vs real:** Lightning AI = one-time ~54 T4-hrs, not a pipeline (skip wiring); Colab free = manual overflow tab, not infrastructure; Paperspace = skip (Kaggle strictly better); GitHub Actions = **maxed 2,000/2,000 min** (constraint, not resource); Vercel Hobby = non-commercial only (Cloudflare Pages is the free answer for anything that sells).
**Biggest blocker across all of it: distribution is on him.** Every free platform gives hosting, zero traffic.

---

## PART 4 — HONEST CAPABILITY AUDIT (what the team can actually do right now)

**Corrections to old ground truth:**
- **Codex works** — via `-p kilo-code` anonymous free-lane profile (verified live: returned OK). Old "codex hangs" claim is outdated. Default profile still 401s (needs `codex login` on his machine or OPENAI_API_KEY in vault — nobody attempts from the VM).
- **`local_composio_tools` skill is stale/broken** — claims `composio_core 0.7.21` in `~/workspace/toolkit-venv`; directory doesn't exist, not importable. Not a real capability until reinstalled.

| Agent/IDE | Verdict | Unblock |
|---|---|---|
| Subagent lanes | **REAL** | — |
| Browser (via parent delegation) | **REAL** | — |
| gh CLI (as mhvnsnt) / GitHub connector | **REAL** | — |
| Node 24 + npm | **REAL** | — |
| ~60 system connectors + custom (gemini/groq/mistral/elevenlabs/ai-horde/torbox/terabox) | **REAL** as agent-called vault APIs | — |
| Gemini as API (custom connector + vault cred) | **REAL** (one-turn image edit/gen) | — |
| Aider | VAPORWARE | install + provider API key (owner supplies) |
| GitHub Copilot CLI | VAPORWARE | `gh extension install github/gh-copilot` + subscription (owner billing) |
| Gemini CLI | VAPORWARE (API is real, see above) | — |
| OpenCode | NOT INSTALLED (scaffold only) | `npm i -g opencode` + API key |
| Cline | INSTALLED BUT UNUSABLE (extension, no code-server host) | install code-server + provider key |
| Cursor / Goose / Claude CLI / qwen / ollama | VAPORWARE | — |
| Colab | NOT DRIVABLE | — |

**Suggested honesty-rule update:** replace "codex hangs" with "codex works via `-p kilo-code` free lane; default profile needs OpenAI auth (401); aider/copilot/gemini-CLI not installed; Cline extension present but code-server missing."

---

## OWNER DECISIONS NEEDED (the short list)

1. **TeraBox renewal** — trial expires 2026-10-20; confirm tonight or run the browser upgrade lane. (Blocks all cleanup verification if it lapses.)
2. **Sitting-take pick** — choose the winning take so ~8G of losing worktrees can be stored-then-cleared. (Fastest disk recovery on the board.)
3. **ConcreteDragon PR #60 vs #61** — one anti-clobber PR is redundant; say which to close.
4. **Modal $30/mo credits** — requires card on file; opt-in only, never automatic.
5. **Oracle Cloud signup** — card required; approve before anyone touches it.
