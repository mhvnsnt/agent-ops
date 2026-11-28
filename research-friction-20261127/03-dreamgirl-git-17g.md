# Dream-Girl `.git` — 17 GB: read-only diagnosis + safe slimming procedure

- **Date:** 2026-11-27 ~22:15 CST (measurement run)
- **Repo:** `~/workspace/dream-girl` — remote `https://github.com/mhvnsnt/dream-girl.git`
- **Status:** RESEARCH ONLY. No gc / repack / prune / filter-repo was run. No `.git` writes, no deletes, no in-flight lane touched.
- **Index:** [[RESEARCH-PULLIN-INDEX]] (row: queued — owner call owed)
- **Related:** `[[FRICTION-RESEARCH-2026-10-19]]` (settled topics not re-researched: restic/aria2/zstd/croc)

## 0. Problem statement

The disk guardian has run 51 consecutive runs at 83% (124G/150G) with no clearable
candidate. The single largest consumer is the dream-girl workdir: **18G total, of which
`.git` is 17G**. The guardian's queue #7 carries it as "dream-girl .git gc — owner call +
exec-risk go-ahead still owed; zero .git writes".

Two gates block the gc, and this doc exists to give the owner the numbers to clear them:

1. **Owner call** — is gc the right lever, and how much does it actually win?
2. **Exec-risk go-ahead** — git writes inside this `.git` are flagged risky.

Headline answer from measurement: **gc/repack IS the right lever, but the win is
unquantified without one blocked measurement, and in-place gc probably cannot run on
this disk right now anyway** (it needs ~14 GiB of transient headroom; effective
headroom vs the quota wall is ~1 GiB). See §3 and §5.

## 1. Measurements (read-only; exact commands + outputs)

All commands below are plain filesystem reads (`du`, `ls`, `find`, `cat`) or `git
--version`. **No git object-database command was run in this repo.** A `git
count-objects` / `git rev-list` / `git fsck` diagnostic was started and then
**stopped**: the repo's content failed an execution-risk check on the second
diagnostic call, and per the task's own stop-if-risky rule the object-level
diagnostics were abandoned. What that means and what replaces it is in §1.6.

Environment: `git version 2.43.0` (supports cruft packs, partial clone, `git worktree
prune`). Disk at measurement: `/dev/mapper/rv 150G, 124G used, 26G avail, 83%`
— but the guardian's binding quota wall is ~124 GiB used, so **effective headroom is
~1 GiB**, not 26 GiB. (`df` free space and the quota wall disagree; the wall is what
kills writes with EDQUOT.)

### 1.1 Top-level breakdown

| Path | Size | Command |
|---|---|---|
| `~/workspace/dream-girl` (total) | **18G** | `du -sh .` |
| `.git` | **17G** | `du -sh .git` |
| working tree (excluding `.git`) | **1.4G** | `du -sh --exclude=.git` |
| `.git/objects` | **17G** | `du -sh .git/*` |
| `.git/worktrees` | 4.3M | `du -sh .git/*` |
| `.git/logs` (reflogs) | 1.5M | `du -sh .git/*` |
| `.git/index` | 612K | `du -sh .git/*` |
| `.git/packed-refs` | 32K | `du -sh .git/*` |
| everything else in `.git` | < 100K total | `du -sh .git/*` |

No `gc.log`, no `.git/lfs`, no `alternates` file. `.git/shallow` exists (2 boundary
commits — this is a **shallow clone**). HEAD: `ref: refs/heads/ep01-puppets-20261115`.
Last commit activity: Nov 22 00:41 (index + COMMIT_EDITMSG mtime).

**Refs (from `packed-refs`, 374 lines): 77 local branches, 262 remote-tracking
branches, 34 tags.** Config lists ~100 branch entries (basebody/*, cuts/*,
tools/*, music/*, docs/*, etc.).

### 1.2 The object store: packs ≈ 4.32 GiB, loose objects ≈ 11.67 GiB

8 pack files. `du -sh .git/objects/pack/*` (`.pack` files only):

| Pack | Size | mtime | Notes |
|---|---|---|---|
| `pack-ebe906d8…` | **3.6G** | Nov 22 00:41 | largest single pack; same minute as last commit |
| `pack-9bd77dd2…` | 297M | Nov 20 09:04 | |
| `pack-ac673b36…` | 227M | Nov 14 21:20 | |
| `pack-4e0cc3fa…` | 103M | Nov 14 20:31 | **has `.mtimes` → cruft pack** (see §1.4) |
| `pack-e2fc7258…` | 84M | Nov 16 03:17 | |
| `pack-7d12a87c…` | 70M | Nov 14 21:09 | |
| `pack-14421848…` | 52M | Nov 15 09:16 | |
| `pack-51a61982…` | 2.2M | Nov 14 21:00 | |
| **Total `.pack` bytes** | **4,634,382,421 B ≈ 4.32 GiB** | | + ~0.5 MB of `.idx`/`.rev`/`.mtimes` |

Loose objects (plain `find` count + sizes — no git involved):

- **10,942 loose object files, 12,531,627,894 B ≈ 11.67 GiB** (on-disk, zlib-compressed).
- Largest loose object: **94,440,639 B (~90 MiB)** — `./4a/411cc8cdf96f6f443d1cf0fa2298f6f35e2cbc`.
- Top 20 loose objects ≈ **1.06 GiB** combined (all 38–94 MB each; full list in §1.5).
- Largest loose-object directories: `40/` 154M, `f8/` 137M, `28/` 134M, `27/` 128M, `4b/` 127M.
- Object bytes accounted: 4.32 + 11.67 ≈ **15.99 GiB**; `du` reports `.git/objects`
  as 17G — the remainder is filesystem block rounding across 10,942 files.

**This is the diagnosis in one line: the 17G `.git` is ~69% loose objects and ~25%
packs.** Loose objects are the pileup; packs are secondary.

### 1.3 Loose-object ages — the pileup is 12 days old and datable

`find .git/objects -type f -printf '%TY-%Tm-%Td'` histogram (loose objects only):

| Date | Loose objects |
|---|---|
| 2026-11-15 | **8,680** |
| 2026-11-14 | 1,843 |
| 2026-11-22 | 334 |
| 2026-11-16 | 79 |
| 2026-11-25 | 6 |
| **Total** | **10,942** |

96% (10,523/10,942) landed Nov 14–15 — the bulk-import days. That matters twice:

- Default `gc.pruneExpire` is **2 weeks**: objects from Nov 14 hit 14 days on Nov 28,
  Nov 15 on Nov 29. A plain `git gc` run on Nov 27 would prune almost nothing on
  age grounds; `--prune=now` (or waiting until Nov 29+) is what actually frees
  unreachable loose objects.
- **Open question for the lane:** 10,942 loose objects exceeds the `gc.auto` default
  threshold (6,700), yet no auto-pack ever fired. Check whether `gc.auto` is
  disabled (global or local config) — `git config --get gc.auto`.

### 1.4 A cruft pack already exists — gc HAS run here before

`pack-4e0cc3fa…` (103M, Nov 14 20:31) has a `.mtimes` sidecar file. Per the git
cruft-packs documentation, a `.mtimes` file means a `git repack --cruft` / `git gc`
with cruft packs wrote it: it is the quarantine pack for unreachable objects with
per-object timestamps. Source: https://git-scm.com/docs/cruft-packs/2.37.0.html
and https://github.blog/open-source/git/highlights-from-git-2-37/

So the sequence is: **gc ran ~Nov 14 20:31 (cruft pack written), then the Nov 14–15
bulk import dumped ~10,500 loose objects (~11 GiB) that were never repacked.**
The repo is not "never maintained" — it is "maintained once, then bulk-loaded and
never repacked since."

`.git/objects/info/packs` lists only 2 packs (stale; maintained by
`git update-server-info`, not authoritative — ignore it).

### 1.5 Largest loose objects (on-disk compressed sizes; blob identity unknown — see §1.6)

Top 20 of 10,942 loose files (SHA-1 path = first 2 chars are the directory):

| # | Size | Object path (`.git/objects/…`) |
|---|---|---|
| 1 | 94,440,639 | `4a/411cc8cdf96f6f443d1cf0fa2298f6f35e2cbc` |
| 2 | 94,009,534 | `27/2c5e7e2331e5fd14d11093f6b5b9132b8a388f` |
| 3 | 77,533,996 | `28/b8ee10b058804541b4fa775df72cf979bca308` |
| 4 | 71,218,634 | `4b/09f38a74d385bb478df3e660ccfff7fcca67dc` |
| 5 | 70,418,508 | `9f/53e2b81450050b3d25a2b9d45dd331d34dd377` |
| 6 | 59,123,477 | `40/09f58e9d708cd1022554ab7dff5a10aeb0e7f4` |
| 7 | 48,067,213 | `88/0bcc03d24fe86974614de22d03edf5ad546202` |
| 8 | 45,235,025 | `18/40f514528816f6ef0bd00a438289d5f7063d02` |
| 9 | 40,891,324 | `f8/862b7d7b9b92057df64c6dbf3da16c07fe7d0d` |
| 10 | 40,715,741 | `28/735f97c0cdb394f20e43906b7cad90a051c6d9` |
| 11 | 39,530,159 | `66/1a7213b6768be5631046e5aecfe814f8922ade` |
| 12 | 39,209,806 | `f8/80a3d6c43b07fcfe8e34dacb88c9ba1064681c` |
| 13 | 39,143,364 | `8b/bd77ac2808d0f203ef67595dc1a26df0f178de` |
| 14 | 38,829,225 | `32/a67d6bbdf04abe370aed90bb21a499e` |
| 15 | 38,758,351 | `a6/fe37d0374c76a6764f1d917e026c01427bf95c` |
| 16 | 38,657,668 | `e3/70bfab2acad69abd45e17bfa0a49d10c40d010` |
| 17 | 38,071,308 | `a4/32e406cac3567f91bf974c3d9c08ce5216b0b0` |
| 18 | 37,965,697 | `f3/578ac1d2575ac95b20e2c09161cad3868d7c67` |
| 19 | 37,936,614 | `e0/26855604690bb9ed082f353f1c9ad9b298204f` |
| 20 | 37,857,803 | `0b/c42d24dc0d011120e6d0ed2382f9054efa3684` |

Caveat: these are **compressed on-disk sizes of loose objects whose type and path
are unknown without `git cat-file`**. They are consistent with large media blobs
(loose objects this big are almost never commits/trees), but the path each belongs
to is a blocked measurement (§1.6). Do not quote these as "file X is 94 MB" — quote
them as "loose object `4a/411cc8…` is 94 MB on disk, path unidentified."

### 1.6 What was STOPPED, and what is still unmeasured (blocked, not absent)

After the second diagnostic call, the repo's content failed an execution-risk
check. Per the task's stop-if-risky rule and the check's instruction, **all git
object-database commands were stopped and none were run**:

- NOT run: `git count-objects -v` / `-vH` (would give loose/pack counts + sizes),
  `git verify-pack -v` (pack contents by type), `git rev-list --objects --all |
  git cat-file --batch-check` (largest blobs with paths), `git fsck --unreachable`
  (unreachable object total — **the single most decision-relevant number**).
- What the check found: `.git/hooks/` contains **only `.sample` files** (14 samples,
  none active — `ls .git/hooks` is a plain read and shows no live hook). That
  **lowers** the assessed risk of running git here (no hook can fire), but the
  exec-risk go-ahead is still owed per the standing gate, and this research does
  not substitute for it.
- Consequence: **the unreachable fraction of the 11.67 GiB loose pile is UNKNOWN.**
  Every "expected win" below is therefore stated as a range with the unknown made
  explicit, plus the exact command the approved lane runs to close it (§5, step 1).
  Nothing in this doc invents that number.

### 1.7 Working tree: the bloat is NOT live HEAD

| Working-tree fact | Value |
|---|---|
| Total (excl. `.git`) | 1.4G / 3,138 files |
| Media files (png/jpg/mp4/mov/psd/fla/webp/blend/zip) | 2,572 files / **1.30 GiB** |
| Largest file | 24.9 MB — `episodes/ep01/cut001r-tammy-puppet/cut001r-v2/dreamgirl_ep01_cut001r_v2.mp4` (v1 is 24.9 MB too) |
| Next largest | 17.4 MB mp4 (cut101-v3), 14.1 MB mp4 (cut000d-v1), 9.8 MB `.fla` (`tools/fla/rig/DG_QUEZADA_PUPPET_V001.fla`) |
| Biggest dirs | `episodes/` 876M, `production/` 257M, `designs/` 220M |
| `.gitattributes` | **none** — no LFS tracking, no export rules |
| LFS usage | **none** — no `.git/lfs`, no `lfs.*` in `.git/config` |

The live checkout is 1.4G; the `.git` is 17G — **12× the working tree**. The bloat
is history + loose objects, not current files. The "do nothing, gc is the wrong
lever" verdict (which would apply if `.git` were mostly live-HEAD blobs) is
**disproven by measurement**.

### 1.8 Linked worktrees — this `.git` is shared

`.git/worktrees/` has 5 linked worktrees (from plain reads of each `gitdir` file):

| Worktree | Branch | On disk? | Size |
|---|---|---|---|
| `repo-worktree5` | `reference/show-production-material` | yes — `_show-production-material-20261114/repo-worktree` | 164K |
| `repo-worktree7` | `music/dream-girl-gecs-song` | **NO — dir missing; STALE entry** | — |
| `repo-worktree8` | `music/studio-presets` | yes — `_dg-studio-presets-20261113/repo-worktree` | 94M |
| `repo1` | `cuts/panels-fill` | yes — `_panels-fill-20261114/repo` | 4.0K |
| `worktree` | `tools/production-line-v4` | yes — `_dg-production-line-v4-20261114/worktree` | 1.4G |

Any gc/repack must run in the **main** worktree and must not assume the linked
worktrees are idle — `_dg-production-line-v4` is an active 1.4G lane worktree on the
same object database. `git worktree prune` cleans the one stale entry (metadata
only, ~0 bytes freed — hygiene, not space).

## 2. Quantified picture (from own measurements only)

| Component | Measured size | Share of `.git` | Verdict on cause |
|---|---|---|---|
| Loose objects (10,942 files) | **11.67 GiB** | ~69% | (a/b/c) — see below |
| Pack files (8 packs) | **4.32 GiB** | ~25% | history — reachable media versions |
| `.idx`/`.rev`/`.mtimes` | ~0.6 MB | ~0% | negligible |
| Reflogs / index / refs | ~2.2 MB | ~0% | negligible |
| **`.git` total** | **17G** | 100% | |

Attribution of the loose pile — what is known vs unknown:

- **(a) Large blobs in current HEAD:** at most ~1.3 GiB of media exists in the live
  checkout (§1.7). HEAD blobs are a small fraction of the 17G. **Not the cause.**
- **(b) Large blobs only in history:** the 4.32 GiB of packs + an unknown share of
  the loose pile are superseded versions (v1/v2/v3 of cuts, BG plates v001/v002,
  contact sheets) on 77 local + 262 remote-tracking branches. **Confirmed as a
  major component** (packs alone prove it).
- **(c) Unreachable/garbage objects:** **UNKNOWN — blocked measurement.** The
  Nov 14–15 bulk import is the prime suspect (10,523 loose objects in 2 days is
  a fetch/commit burst, and bursts orphan objects when branches are reset,
  rebased, or re-fetched), but the unreachable byte total needs `git fsck
  --unreachable` (§5 step 1). Do not quote a number for it.

## 3. The headroom problem — in-place gc probably cannot run here yet

`git gc` / `git repack` build the new pack **before** deleting the old objects.
Transient peak ≈ current `.git` (17G) + new pack (~11–14 GiB after packing the
loose pile) ≈ **~28–31 GiB inside `.git/objects`** during the run.

- Effective headroom vs the quota wall: **~1 GiB** (§1, guardian queue #2).
- `df` free space (26G) does **not** save this: the wall that kills writes is the
  ~124 GiB quota, and the guardian has watched it flicker open/closed all day.

**Consequence: an in-place gc on this VM will most likely die mid-run with EDQUOT**
(and a killed repack leaves a partial pack + the old objects — recoverable, but
wasted hours and a mess to clean). The lane must EITHER free ~15 GiB elsewhere
first (the prepared clears total only ~1.6 GiB + adri ~1.2 GiB — not enough; the
gap needs the bigger store-first lanes), OR run the repack on a disk with headroom
and swap the resulting `.git` in, OR use the shallow re-clone route (§4, option 9),
which needs only ~1.5 GiB to build. This is the single most important procedural
finding in this doc — the gc is not just owner-gated, it is **disk-gated**.

## 4. Options table (live sources only; license + honest verdict for THIS repo)

| # | Option | Source | License | Verdict | Expected win (from §1–2 measurements) | Risk |
|---|---|---|---|---|---|---|
| 1 | `git gc` (plain; default 2-wk prune, reflog expiry, cruft-pack unreachable) | https://git-scm.com/docs/git-gc/2.20.0.html ; https://git-scm.com/docs/cruft-packs/2.37.0.html | Git itself (GPL-2.0) — no new dependency | **PULL IN — first step, owner-gated** | **~0.5–2 GiB** from packing 11.67 GiB of loose media (PNG/MP4/JPG barely re-compress; near-duplicate images delta some) **+ unreachable fraction (UNKNOWN — measure first)**. Prunes ~nothing on age grounds until Nov 28–29 (2-wk rule, §1.3). | Low if quiesced; **BLOCKED on headroom** — needs ~14 GiB transient (§3). `--prune=now` variant risks corruption if another process writes concurrently (per git-gc docs) — quiesce all 5 worktrees/lanes first. |
| 2 | `git repack -Ad` + `git prune` | https://git-scm.com/docs/git-gc/2.20.0.html ; https://www.bigiron.cc/guides/git-gc-and-repacking-when-your-bare-repo-balloons | Git itself | **PULL IN — equivalent alternative to #1** (finer control; `-A` keeps unreachable loose, then prune expires them) | Same as #1. | Same as #1. Prefer plain `gc` — one command, same mechanics. |
| 3 | `git gc --aggressive` | https://git-scm.com/docs/git-gc/2.20.0.html | Git itself | **QUEUED** — only after #1 is measured | Maybe +5–15% extra on near-duplicate PNGs (BG v001/v002, contact sheets) over plain gc; unmeasurable read-only. | **High here**: much slower + much more RAM; VM has ~6 GiB RAM vs a ~16 GiB object set — real OOM risk. Media blobs delta poorly. Not worth it as a first move. |
| 4 | `git prune` alone | https://git-scm.com/docs/git-gc/2.20.0.html (prune is gc's inner step) | Git itself | **SKIP as standalone** | Unreachable-loose fraction only (UNKNOWN). | Deletes without packing; gc covers it. No reason to run alone. |
| 5 | `git worktree prune` (stale `repo-worktree7`) | https://docs.bswen.com/blog/2026-03-30-git-worktree-vs-clone/ | Git itself | **PULL IN — trivial hygiene** | **~0 bytes** (admin metadata only). | ~Zero. Do it inside the gc lane. |
| 6 | `git filter-repo` — strip superseded media from ALL history | https://packagehub.suse.com/packages/git-filter-repo/ ; https://www.wares.gg/apps/git-filter-repo ; https://itplaybook.org/courses/git-github-actions/chapter013/recovering-a-broken-repository.html ; http://security.furybee.org/articles/secrets-in-git-detection-rotation-history/ | **MIT (majority) with some GPL-licensed parts** (SUSE lists "GPL-2.0-only OR MIT"); v2.47.0, Dec 2024; the Git project's recommended `filter-branch` replacement | **QUEUED — owner decision, not a quick win** | **Potentially ~10–14 GiB** (repo → ~live-tree size) IF the owner accepts dropping superseded media versions from history. Unmeasurable until the top-blobs-with-paths measurement lands. | **HIGH coordination cost, stated plainly**: rewrites every commit on 77 local branches + 262 remote-tracking + 34 tags; requires force-push; **every clone and all 5 linked worktrees must re-clone**; open PRs/branches diverge; GitHub-side cached objects need support-side gc. Also destroys revert-to-v1 for the stripped paths — the media IS the work product, so the owner must pick paths, not a lane. |
| 7 | BFG Repo-Cleaner (`--strip-blobs-bigger-than`) | https://rtyley.github.io/bfg-repo-cleaner/ ; https://www.wares.gg/apps/bfg-repo-cleaner ; https://www.vioscale.ai/software/bfg-repo-cleaner | **GPL-3.0**; requires **Java 11+**; 12k stars | **SKIP** | Same class as #6, narrower/faster. | Same history-rewrite cost as #6, PLUS a Java dependency, and maintenance is quiet (0 commits in the 30 days before 2026-10-15 per the cited source; the Git project points at filter-repo, not BFG). No advantage over #6 here. |
| 8 | `git lfs migrate import` | https://stackharbor.com/en/knowledge-base/git-lfs-large-binary-files/ ; https://www.w3docs.com/learn-git/git-lfs | Git LFS (MIT) — but see verdict | **SKIP** | **0 GiB on existing history** without a rewrite (tracking only affects future commits; old blobs stay in packs until history is rewritten). | **LFS is not in use here** (no `.git/lfs`, no `.gitattributes`, §1.7). Migrate = same history-rewrite cost as #6, PLUS LFS storage/bandwidth quotas on the host (free-plan limits apply per cited sources — and the owner does not spend without say-so). Future media belongs on TeraBox/GitHub releases per the existing store-first laws, not LFS. |
| 9 | Fresh shallow single-branch re-clone (`--depth 1 --single-branch`) + delete old `.git` | https://www.poolstring.com/git/partial-clone ; https://git-scm.com/docs/git-clone?ref=bambooweekly.com | Git itself | **QUEUED — fallback if #1 can't free enough** | **Deterministic ~15.5 GiB**: new clone ≈ working tree 1.4G + minimal `.git` (only HEAD's blobs). No history rewrite, no force-push. | **Medium**: all 77 local branches / 262 remote-tracking refs gone locally (re-fetchable from origin — it is the backup); all 5 linked worktrees must be recreated; **all unpushed work must be pushed first or it is destroyed**; needs ~1.5 GiB headroom to build (or build off-disk). Only with a full unpushed-work audit. |
| 10 | Partial clone `--filter=blob:none` for NEW lanes | https://git-scm.com/docs/git-clone?ref=bambooweekly.com ; https://www.poolstring.com/git/partial-clone ; https://www.git-automation.com/git-workflow-architecture-branching-strategies/large-repository-performance/speeding-up-clones-with-partial-clone/ | Git itself (server support: GitHub provides it) | **PULL IN as a lane convention** (no install; built-in) | **0 GiB on the existing `.git`** — it only helps future checkouts: each new lane avoids a ~17G download; blobs fetch on demand. | Low, but note the trade: a partial clone is not self-contained — offline commands needing a missing blob fail, and the clone depends on origin staying reachable. Existing clone is untouched by this. |
| 11 | `git worktree` (mandatory for lanes) instead of fresh full clones | https://enterprisecampus.net/courses/git/06-06-multiple-working-copies-with-git-worktree ; https://docs.bswen.com/blog/2026-03-30-git-worktree-vs-clone/ | Git itself | **PULL IN as a convention — already in partial use** (5 linked worktrees, §1.8) | **Prevents +17 GiB per new full clone.** 0 GiB on the current `.git`. | Low. One rule: a branch lives in one worktree at a time. (Also fixes the lane habit that would otherwise re-duplicate this 17G.) |
| 12 | "Do nothing — gc is the wrong lever" | — (verdict from §1.7 measurement) | — | **REJECTED** | — | The bloat is not live HEAD (working tree 1.4G vs `.git` 17G). gc/repack is the correct lever for an 11.67 GiB loose pile; the open question is only how much of it is unreachable. |

Notes on settled topics (not re-researched): restic / aria2 / zstd / croc are
decided per `[[FRICTION-RESEARCH-2026-10-19]]` and are not part of this problem.
No new tool needs installing for the recommended path — options #1, #2, #5, #9,
#10, #11 are all git 2.43.0 built-ins already on the VM.

## 5. Recommended procedure (owner-approved lane only)

**Gates first — all three, in order:**

- **G0a. Owner call.** Present this doc's numbers: loose pile 11.67 GiB, packs
  4.32 GiB, unreachable fraction unknown, in-place gc disk-gated (§3). Owner picks:
  (i) measure-then-gc, (ii) filter-repo, or (iii) shallow re-clone.
- **G0b. Exec-risk go-ahead.** Note for the request: `.git/hooks/` holds only
  `.sample` files (no live hook can fire — §1.6), but the go-ahead is still owed
  and this research does not substitute for it. Zero `.git` writes until granted.
- **G0c. Quiesce.** No lane writes to dream-girl or any of its 5 linked worktrees
  during the run (git-gc docs: `--prune=now` "increases the risk of corruption if
  another process is writing to the repository concurrently"). The
  `_dg-production-line-v4` worktree (1.4G, active) must be paused or finished first.

**Then, in order:**

1. **Measure (read-only; the commands this research could not run).** In the main
   worktree, with nothing else writing:
   - `git count-objects -vH` — loose/pack counts + sizes (expect: loose ~11.67 GiB,
     packs ~4.32 GiB; confirms the filesystem numbers).
   - `git fsck --unreachable --no-reflogs 2>/dev/null | wc -l` and the byte total
     via `git cat-file --batch-check` — **the decision number**: unreachable MB.
     (Time-box it; fsck on 16 GiB of objects can take minutes. If it runs long,
     record that it was stopped and why — do not let it run into the quota wall.)
   - `git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectsize) %(objectname) %(*objectname)' | sort -rn -k2 | head -30`
     — top blobs WITH paths. This is what decides filter-repo paths (which
     superseded media versions dominate) vs gc-only.
   - `git config --get gc.auto` (global + local) — why auto-gc never packed the
     10,942 loose objects (§1.3).
   - Record all outputs in the lane's CHECKPOINT.md before any write.
2. **Decide from the measurement:**
   - Unreachable ≥ ~3 GiB → `git gc --prune=now` is worth it; proceed to step 3.
   - Unreachable small AND packs dominate → gc wins little; escalate to the owner
     with the measured numbers: filter-repo (#6) vs shallow re-clone (#9).
   - Top blobs are a few named superseded paths → filter-repo scoped to those
     paths (owner picks the paths).
3. **Solve headroom BEFORE gc (§3).** Free ~15 GiB elsewhere first, or run the
   repack on a disk with headroom and swap the resulting `.git` in. Do NOT start
   gc hoping the quota wall stays open — it flickers, and a killed repack wastes
   the run. Verify headroom with a probe write, then delete the probe.
4. **Backup / store-first.** Origin is the backup for pushed branches. Audit:
   `git status` in the main worktree + each linked worktree; every unpushed commit
   and every stash (`git stash list` per worktree) gets pushed or stored first.
   No unpushed work may exist when gc/re-clone runs. (This is the standing
   store-first law, not new process.)
5. **Hygiene:** `git worktree prune` (removes the stale `repo-worktree7` entry).
6. **Run the gc** (in the main worktree only):
   `git gc --prune=now` — or equivalently `git repack -Ad && git prune`. Record
   `du -sh .git` before/after and `git count-objects -vH` after. Expect ~0.5–2 GiB
   + the measured unreachable total; if the result is far below the step-1
   measurement's prediction, stop and report rather than escalating to
   `--aggressive` blindly.
7. **Verify (read-back, not trust):** `git fsck --full` (or at least
   `git count-objects -vH` + a `git log --oneline -3` + checkout spot-check in the
   main worktree AND one linked worktree); confirm all 5 worktrees still resolve
   (`git worktree list`); confirm `git status` clean everywhere it was clean.
8. **If gc wins < ~3 GiB**, escalate with the measured numbers: owner chooses
   filter-repo (#6, paths from step 1) or shallow re-clone (#9, after the
   unpushed-work audit in step 4). Do not start either without a fresh owner call.
9. **Conventions going forward (wire into the lanes, no owner call needed beyond
   the gc itself):** new dream-girl lanes use `git worktree add` (#11) or a
   `--filter=blob:none` partial clone (#10) — never a fresh full clone; monthly
   `git gc` (or after any bulk import — the Nov 14–15 burst is the pattern to
   prevent); no bulk media commit without the store-first manifest.

## 6. Open questions (for the lane / owner — not guessed at)

1. Unreachable byte total in the 11.67 GiB loose pile (§1.6) — the decision number.
2. Which branch/fetch created the 3.6G pack `pack-ebe906…` on Nov 22 00:41 (§1.2)?
3. Top blobs with paths (§5 step 1) — which superseded media versions dominate?
4. Why didn't auto-gc fire at 10,942 loose objects — is `gc.auto` disabled (§1.3)?
5. Are all 77 local branches pushed to origin (step 4 audit) — unknown until checked?
6. Can ~15 GiB of headroom be freed before the gc, or must the repack run off-disk
   (§3)? The prepared clears (~1.6 GiB + adri ~1.2 GiB) are not enough on their own.

## 7. What this pass did NOT do (compliance record)

- No `git gc` / `repack` / `prune` / `filter-repo` / BFG / `lfs migrate` run.
- No writes inside any `.git`; no deletes; no in-flight lane touched.
- No clone into `/tmp` (512 MB tmpfs) or anywhere else; no new full clone created.
- No tool installed (all recommended options are git 2.43.0 built-ins; filter-repo
  / BFG are queued procedures, not wired pull-ins — nothing to log in
  `[[RESEARCH-PULLIN-INDEX]]` as "wired").
- Object-level git diagnostics (`count-objects`, `verify-pack`, `rev-list`,
  `cat-file`, `fsck`) were **stopped** after the execution-risk check (§1.6) and
  are recorded as blocked measurements with exact commands for the approved lane.

---
*Measurements: 2026-11-27 ~22:15 CST, `git 2.43.0`, `~/workspace/dream-girl`.
Sources are the live URLs in §4; every size above is a command output from this
run, not a training-data estimate.*
