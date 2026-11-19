# Disk cleanup 2026-11-11

Time: 2026-11-11 15:56 CST (America/Chicago)
Owner approval: delete old copies that are fully pushed to GitHub.

## Before / after

- Before: 413 MiB free of 128G (432,758,784 bytes), 100% used
- After:  7.84 GiB free of 128G (8,415,186,944 bytes), 94% used
- Freed:  7.43 GiB (7,982,428,160 bytes) ≈ **7.4 GiB / 7.98 GB**

Eligibility for each top-level dir over ~400 MB: git repo/worktree with a remote, `git status --porcelain` empty, no stashes, every local branch HEAD commit present on origin (verified via `gh api repos/.../commits/<sha>`), no working-tree file mtime in the last 90 minutes. Worktrees removed with `git worktree remove` from the main repo. Never deleted: `/workspace/dream-girl`, `/workspace/dcc`, `/workspace/tools`, non-git folders, dirty/unpushed/recent work.

## Deleted

| Path | Kind | Repo URL | HEAD sha | Branch | Size |
|------|------|----------|----------|--------|------|
| /workspace/cjh | standalone clone | https://github.com/mhvnsnt/cape-jones | e4330c0ff89449d394d21554d8b664b6844b4876 | docs/show-production-status-20261105 | 3.14 GiB |
| /workspace/wt-matrix10 | worktree of /workspace/western-heart | https://github.com/mhvnsnt/western-heart | e3735b882e95d32011dd4016521d2ff685d05231 | grok/matrix-r10 | 1.72 GiB |
| /workspace/whpr | standalone clone | https://github.com/mhvnsnt/western-heart | 6614953e9526bdfcce99bf17fa900098eb7d9433 | docs/t7-0x64-pose-finding | 0.999 GiB |
| /workspace/wh-pantera | standalone clone | https://github.com/mhvnsnt/western-heart.git | 25c4f064b92f48a3580adbabc8071ad6b17dfb00 | grok/t7-flags-runtime-20261110 | 0.961 GiB |
| /workspace/wh-facecone | worktree of /workspace/western-heart | https://github.com/mhvnsnt/western-heart | d398d51b70d3c8f39e2fd972cc74e0227a6e5e54 | feat/face-cone-skin-weights | 0.569 GiB |

Worktree removals:

```
git -C /workspace/western-heart worktree remove /workspace/wt-matrix10
git -C /workspace/western-heart worktree remove /workspace/wh-facecone
```

Standalone clones were removed with `rm -rf` after the checks above. All local branch tips on the three standalone clones were confirmed present on GitHub (cjh: 3 branches; whpr: 4; wh-pantera: 10).

## KEEP (with reason)

Protected (never delete):

- `/workspace/dream-girl` (961M) — protected path
- `/workspace/dcc` (1.2G) — protected path
- `/workspace/tools` (4.5G) — protected path

Dream-girl worktrees (active / recent):

- `/workspace/dream-girl-p4` (592M, `cuts/cut001r-v2-cut002`) — current cut work, KEEP
- `/workspace/dg-rig` (348M, `rig/tammy-3d-anime`) — dirty (untracked `rig/tammy-3d/`, `tools/rig/`) and recently modified; sister workstream
- `/workspace/dream-girl-p1` (275M, `restore/881151f-designs`) — clean and pushed, but file mtime 14:27 CST (within 90 minutes)
- `/workspace/dream-girl-p2` (367M, `wiring/repo-setup`) — clean and pushed, but file mtime 14:33 CST
- `/workspace/dream-girl-p3` (410M, `cuts/cut001r`) — clean and pushed, but file mtime 14:34 CST

Git, dirty and/or recently touched — KEEP:

- `/workspace/western-heart` (21G) — dirty (67,274 paths)
- `/workspace/wt-sweep2` (13G, worktree) — dirty (74 paths)
- `/workspace/gre-wire` (5.8G) — dirty (15,095 paths)
- `/workspace/physics-playground-pwa` (4.7G) — dirty (3 paths) + recent
- `/home/box/wh-d-pipeline` (4.2G) — dirty (16 modified files)
- `/workspace/ppp-main` (3.1G, worktree) — dirty (34 paths) + recent
- `/workspace/mcg` (2.3G) — dirty (4 paths)
- `/workspace/wh-rma` (2.2G, worktree) — dirty
- `/workspace/wt-rm` (1.8G, worktree) — dirty (66,198 paths)
- `/workspace/wt-main` (1.8G, worktree, detached) — dirty (66,197 paths)
- `/workspace/mcg-land` (1.3G, worktree) — dirty
- `/workspace/mcg-colab` (1.2G, worktree) — dirty
- `/workspace/wh-moves` (791M, worktree) — dirty
- `/workspace/mmhq` (544M) — dirty (57 paths)

Non-git top-level dirs over ~400 MB — KEEP (not a git repo/worktree):

- `/workspace/unreal` (3.7G)
- `/workspace/cj3d` (2.8G)
- `/workspace/oss-anim-staging` (2.3G)
- `/workspace/scratch` (1.6G)
- `/workspace/oss` (1.6G)
- `/workspace/mchao` (1.6G)
- `/workspace/gb` (1.4G)
- `/workspace/sing` (1.1G)
- `/workspace/mocap-venv` (826M)
- `/workspace/cj-boards-alive` (797M)
- `/workspace/rv` (788M)
- `/workspace/pantera-t7-sources` (672M)
- `/workspace/steam` (670M)
- `/workspace/megami-lane` (602M)
- `/workspace/nioh` (496M)
- `/workspace/intro-movie` (470M)
- `/workspace/ashlane` (464M)

`/home/box` large non-git (dotdirs / toolchains) — KEEP: `.bun` 1.3G, `.dotnet` 579M, `chrome-profile` 546M, `.local` 485M.

## /workspace/sweep — listed for the owner, NOT deleted

13G, not a git working tree. Almost all of it is a bare repo at `/workspace/sweep/wh.git` (13G), plus `/workspace/sweep/mm.git` (688K), small logs (`L442.log`, `L718.log`, …), and helper scripts (`loop.sh`, `step1.sh`, `docres.sh`, TSVs, `money-machine-hq.json`). This is **not** "just logs already pushed somewhere." Leaving it for the owner to decide.

## Notes

- Recent-mtime checks used `find <dir> \( -path '*/.git' -o -path '*/.git/*' \) -prune -o -type f -mmin -90`.
- Unpushed check used GitHub API (`gh api repos/<owner>/<repo>/commits/<sha>`) rather than `git fetch`, as allowed.
- Other agents share this box; dirty or <90-minute-old trees were left untouched.
