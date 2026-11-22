# wt-autoseat take — handoff (2026-10-19)

Owner order: store ALL takes first, no winner picked yet. This take is stored and kept separate so he can compare later.

## WHAT THIS TAKE IS (plain language)

This is the **chair-sitting solver take**.

The problem it fixes: earlier sitting tests kept floating the character above the chair or sinking him through it. The reason was simple — the old code measured the top of the chair's invisible box, not the real seat surface.

This take measures the real chair first, then sits the character down properly:

- It shoots virtual measuring rays at the chair to find the true seat height.
- It loads a real seated motion-capture clip.
- It moves the body so the butt touches the seat, the back touches the backrest, and the feet touch the floor.
- It saves the finished seated pose and proof pictures.

Important: this take is code + test files, not a final animation. The key files are `autoseat.py`, `autoseat_v2.py`, `autoseat_v4.py`, `autoseat_v5.py`, debug scripts, logs, proof images, and `proof_sitting.blend`.

## Where this take lives

- Git branch: `auto-seat-solver-20261019`
- Branch commit: `0e3f2401ab280321b384f11e81b08e5c49ae9e35`
- Repo: `mhvnsnt/cape-jones`
- PR: `mhvnsnt/cape-jones#168` — merged to `main`
- Merge commit: `1eccb4ba4895836b4e763f4d5f225ad38c3ed65a`
- Release: `sitting-wt-autoseat-20261019`
- Release URL: `https://github.com/mhvnsnt/cape-jones/releases/tag/sitting-wt-autoseat-20261019`

Archive facts:

- Full tar: `4,264,734,720` bytes
- Full tar sha256: `3c99be49ffdc58ad184e2d5b7c6af34f80ae1af57ebc451541d21a8671c3494b`
- Parts: `part-aa` through `part-ai` (500MB parts; `.git` excluded)
- Files archived: `34,442`

Status: **STORED + VERIFIED.** All 9 parts are on the release; GitHub's own sha256 digest for every part matches the locally recorded part sha256 exactly, and every part size is byte-exact. A full download-back reassembly check (download all 9 parts, rebuild the tar, compare its sha256 to `3c99be49...`) was run as the final belt-and-braces pass — its live log is `~/workspace/wt-staging/verify.log`, copied to `~/workspace/agent-ops/wt-autoseat-store-record/` when it completes, alongside the upload manifest and logs. The local worktree copy has been removed from disk; the take lives on the branch and in this release.

## Exact pickup commands

Download and verify the stored archive:

```bash
mkdir -p autoseat-restore
cd autoseat-restore
gh release download sitting-wt-autoseat-20261019 --repo mhvnsnt/cape-jones --dir .
cat part-aa part-ab part-ac part-ad part-ae part-af part-ag part-ah part-ai > wt-autoseat-full.tar
sha256sum wt-autoseat-full.tar
# must equal:
# 3c99be49ffdc58ad184e2d5b7c6af34f80ae1af57ebc451541d21a8671c3494b
tar -tf wt-autoseat-full.tar | head
tar -xf wt-autoseat-full.tar
```

Get the exact branch code from Git:

```bash
git clone https://github.com/mhvnsnt/cape-jones.git
cd cape-jones
git checkout auto-seat-solver-20261019
git rev-parse HEAD
# must equal:
# 0e3f2401ab280321b384f11e81b08e5c49ae9e35
```

Key files inside the take:

```text
production/tools/auto-seat/autoseat.py
production/tools/auto-seat/autoseat_v2.py
production/tools/auto-seat/autoseat_v4.py
production/tools/auto-seat/autoseat_v5.py
production/tools/auto-seat/debug_*.py
production/tools/auto-seat/run.log
production/tools/auto-seat/run_v2.log
production/tools/auto-seat/run_v3.log
production/tools/auto-seat/run_v3b.log
production/tools/auto-seat/run_v3c.log
production/tools/auto-seat/run_v3d.log
production/tools/auto-seat/run_v3e.log
production/tools/auto-seat/run_v3f.log
production/tools/auto-seat/run_v3g.log
production/tools/auto-seat/run_v3h.log
production/tools/auto-seat/run_v3i.log
production/tools/auto-seat/run_v4.log
production/tools/auto-seat/run_v5.log
production/tools/auto-seat/run_v5b.log
production/tools/auto-seat/run_v5c.log
production/tools/auto-seat/run_3q.log
production/tools/auto-seat/run_render.log
production/tools/auto-seat/run_tpose.log
production/tools/auto-seat/proofs/
production/tools/auto-seat/proof_sitting.blend
production/tools/auto-seat/proof_sitting.blend1
production/tools/auto-seat/render_3q.py
production/tools/auto-seat/render_proofs.py
production/tools/auto-seat/render_wide.py
```

## Notes for later comparison

- This take measures before moving; older sitting attempts used guessed or box-top heights.
- Latest run log shows normal keyframing, but `run_v5.log` ends with a divide-by-zero error in `autoseat_v5.py`, so v5 did not complete cleanly.
- No winner has been chosen. Keep this take stored as-is.

## Addendum — store worker verification completion + anti-clobber note (2026-10-20)

- **Download-back reassembly completed by the store worker** (the pass referenced above): all 9 assets downloaded back, concatenated in order = 4,264,734,720 bytes, sha256 `3c99be49ffdc58ad184e2d5b7c6af34f80ae1af57ebc451541d21a8671c3494b` — EXACT MATCH with the pre-upload local tar sha256. Per-part download verification log + reassembly record: `~/workspace/agent-ops/wt-autoseat-store-record/` (`download-verify-per-part.log`, `REASSEMBLY-VERIFIED.txt`).
- **Anti-clobber note (why the archive is the complete 4.1G worktree):** the worktree arrived with 10,400 tracked files (1.37 GiB) deleted from disk by an earlier CloudDog partial clear (`production/devtools` 8,543; `animation-study/teen-titans` 970; `animation-study/donor` 746; `production/ai-body-replace` 91; `production/kaggle` 36; a few in `production/bumps` + `assets/`). Per the repo ANTI-CLOBBER LAW those deletions were NOT committed (not made by this task). The files were restored from git objects — tree verified clean at the already-pushed HEAD `0e3f2401a` — so the tar contains the COMPLETE worktree (34,442 files), and PR #168's diff stayed +4119/−0.
- **Incidents (all recovered, nothing lost):** `/opt` staging wiped twice by an external sweep (same class as the BeatB2 04:13Z incident) — staging moved to persistent disk. A duplicate sibling uploader ran against the same release; this worker stood its own down, then finished uploads itself after the sibling's uploader died in a proxy outage. Seven assets vanished from the release once mid-job (cause unidentified) and were re-uploaded from byte-verified local parts. The worktree directory itself was deleted externally before the clear step; its stale git registration was pruned by this worker after full verification. Egress proxy was intermittently down/slow for hours (connection refused; uploads.github.com 404s; multi-try successes).
