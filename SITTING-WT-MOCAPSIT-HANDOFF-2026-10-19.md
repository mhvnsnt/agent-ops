# HANDOFF — wt-mocapsit (mocap sitting retarget take), 2026-10-19

Owner order (verbatim): "Store it all, clean merge, no clobbering either side, and get that 8gb stored and off disc safely without losing or destroying it."
Takes sequence (owner, verbatim): "store it first then explain it to me and then I'll choose after it's stored in off disk."
Status: STORED. He chooses later — no winner picked here.

## WHAT THIS TAKE IS (plain language)

This take gets a real human's sitting motion onto our character, instead of
someone hand-posing every joint.

The approach: start from a public library of real recorded human movement
(Carnegie Mellon's motion-capture set — tiny sensors-on-a-suit recordings of a
real person moving, here clip 113_15: a person sitting down in a chair and
standing back up). Then a script (mocap_retarget.py, and the production version
at production/tools/mocap-retarget/retarget.py) copies that person's joint
angles onto Cape Jones's 94-bone rig — his full digital skeleton. "Retargeting"
just means: the recorded person and our character have different skeletons, so
the script translates the motion from one body to the other.

The tricky part the lane solved: it also fixes where he lands. Without help,
copying the motion would park him two meters in the air or sink him through the
chair. The script numerically locks his body so his butt lands exactly on the
chair seat (measured: 0.00mm gap — touching, not floating), his feet rest on
the floor, and his arms move in the natural gesture from the recording rather
than sticking out stiff (the "H-pose" you get when only half the body is
posed). One hand-tweak was deliberately kept: the recording had the actor
fidgeting his head around, so head and neck motion is damped to half (50%),
which the README frames as selecting channels, not hand-posing.

What it does well: it's real human motion — 81 frames of an actual person
sitting down and standing up, so it avoids the puppet-on-strings look of posed
animation. Contact is exact (butt on seat, feet on floor). Two stills are in
the tree (proof/mocap-sit/sit_front.png, proof/mocap-sit/sit_threequarter.png)
plus the animated result (proof/sitting_mocap.blend) so you can see it before
deciding anything.

What's rough/unfinished: only one clip was finished (the "sit in chair and get
up" clip); a list of six more sitting clips exists but was never pulled into
the repo. The math the script uses is fussy — the README warns that using the
wrong rotation reference produces garbage poses (thighs backward, chest
sideways), which was the bug in earlier versions; anyone re-running it needs to
follow the README exactly. The script hard-codes the seat position it was tuned
for, so it isn't a general "sit anywhere" button yet. And it solves sitting
contact only — it doesn't handle the chair-back, table, or the mug/props.

How it feels different from a generic sitting setup: a generic setup poses the
body by hand and it looks posed. This one looks like a person because it IS a
person — the recording carries the little weight-shifts and timing a human
makes when sitting down. That's the whole bet of this take.

## WHAT THE WORK WAS

Branch `mocap/sitting-retarget-20261019` on repo `mhvnsnt/cape-jones`.
Worktree was `~/workspace/wt-mocapsit` (removed from disk after verified storage).
Commits (2026-10-19):
- `aea71dcf6` "Mocap sitting retarget pipeline (owner 2026-10-19)": real CMU
  113_15 'sit in chair' mocap retargeted onto the 94-bone rig. Butt on seat
  (0.00mm), feet on floor, natural arm gesture (no H-pose). 81 frames of real
  human motion. Pipeline: 3d-assets/animation/mocap-sit/ +
  production/tools/mocap-retarget/. Stills: proof/mocap-sit/ (own-eyes verified).
- `184ee6277` "WIP mirror 2026-10-19 (clouddog beat)": untracked
  mocap_retarget.py, proof_render.py, proof/sitting_mocap.blend; records
  stip.blend1 removal.

Notes on tree state at archive time: the working tree had 10,399 tracked files
deleted from disk only (mostly production/devtools, animation-study/teen-titans,
animation-study/donor, production/ai-body-replace, production/kaggle) — removed
by the earlier partial disk-clear (CloudDog beat). ALL 10,399 exist as blobs in
commit 184ee6277 (verified: all paths resolve to blobs in HEAD, total
1,475,297,069 bytes). They were deliberately NOT re-committed as a deletion, so
the merged PR keeps main's copies intact (anti-clobber). The archive below
contains the worktree as it sat on disk (2.5G present, .git excluded); git
history carries the deleted files too.

## WHERE IT LIVES

- Branch: `mocap/sitting-retarget-20261019` @ `184ee6277` (origin verified equal)
- PR: mhvnsnt/cape-jones#159 "Mocap sitting retarget (owner 2026-10-19)" —
  MERGED 2026-10-20T02:24:49Z, merge commit `a847a3e4f2baff4f1087f404aaa457f67a050343`,
  mergeable=CLEAN, zero conflicts, nothing clobbered.
- Release mirror: `sitting-wt-mocapsit-20261019` on mhvnsnt/cape-jones
  https://github.com/mhvnsnt/cape-jones/releases/tag/sitting-wt-mocapsit-20261019
- Archive: `wt-mocapsit-full.tar.gz` — gzip-compressed tar of the full worktree
  minus `.git`, streamed (deterministic: gzip -n, no embedded timestamp), split
  into 250MB parts: wt-mocapsit-full.tar.gz.part-000, part-001, ...
  (Deviation note: the brief's /tmp tar + 500MB splits couldn't be used — /tmp
  is a 512MB tmpfs with only ~11MB free, and 500MB uploads stalled through the
  shared egress proxy while sibling lanes uploaded; 250MB parts + per-part
  retry/verify kept the pipeline moving.)
- Full-stream sha256: `6ec605bcee03fa0885a0528887506900c8f94ddd3ad5d4e11ade28efbc561a97`
  (computed over the reassembled archive downloaded back from the release; the
  upload-side stream hash was lost when mirror.py exited on a tar warning —
  see below — so the release-side chain is the record: local part hashes ==
  GitHub digests == downloaded part hashes, 8/8)
- Parts (name / bytes / sha256):
  - wt-mocapsit-full.tar.gz.part-000 / 262144000 / adb9f53c505e7f1dcce75046947db7cc4bd837db59c3f769bfbdb06914149e7e
  - wt-mocapsit-full.tar.gz.part-001 / 262144000 / e74b5e82ed0d45aca14d8a24a28358ce3dc3dd9e4211a722e06fd9705be2c948
  - wt-mocapsit-full.tar.gz.part-002 / 262144000 / cfbf799747a8232584a6323caaf624438eaf2edcebe5c03c6e323becae191c3e
  - wt-mocapsit-full.tar.gz.part-003 / 262144000 / 4c6002d2c72b476ea74477c62b091ea4b1df1f651139f12fc420337d05147ad8
  - wt-mocapsit-full.tar.gz.part-004 / 262144000 / 30ac0a3b19d8e8640255ba3b176a0d9590daf38e938a5334aee9c7017fcf8b0a
  - wt-mocapsit-full.tar.gz.part-005 / 262144000 / 33854de15dc79b5e713b859b2adbcd65e3f2218d0b81c8180e22515abe4d9b36
  - wt-mocapsit-full.tar.gz.part-006 / 262144000 / 8c4fcbabbd9191e605f87958c601472f83a024c509613e178770bed05d4dbab8
  - wt-mocapsit-full.tar.gz.part-007 / 243285350 / b08d1cbc532c6d8ff3c083d57e527a00cd14dbc67990f76b6be238efe9d7e13b
  - Total: 2,078,293,350 bytes
- Reassembly check (2026-10-20): downloaded ALL 8 parts back from the release,
  every part's sha256 == its locally computed value; concatenated stream =
  2,078,293,350 bytes, sha256 6ec605bc... (above); extracted cleanly
  (tar rc=0), 21,945 files (= 21,944 on disk + the .git pointer file); full
  `diff -rq` of the extracted tree vs the live worktree: ZERO differences.
- TAR QUIRK (explains itself, not a data problem): the mirror streamed
  `tar ... wt-mocapsit --exclude=wt-mocapsit/.git` with the exclude AFTER the
  operand, so GNU tar ignored the exclude and exited rc=2 with a positional-
  option warning. Effect: the worktree's `.git` POINTER FILE (4KB text, this is
  a linked worktree — the real git dir lives in the main repo) IS included in
  the archive. No file content was skipped or damaged — proven by the zero-diff
  extraction check above.
- Handoff: this file, ~/workspace/agent-ops/SITTING-WT-MOCAPSIT-HANDOFF-2026-10-19.md
- Bytes cleared from disk: 2.5G worktree (removed 2026-10-20 after verification)
  + ~4.6G of verification staging (downloaded parts + extracted tree, deleted
  after the zero-diff check; audit logs/scripts/manifests kept in
  ~/workspace/agent-ops/staging-mocapsit/)

## EXACT PICKUP COMMANDS

Get the code (branch; includes all 10,399 files that were deleted from the disk copy):

    git clone --branch mocap/sitting-retarget-20261019 https://github.com/mhvnsnt/cape-jones.git
    cd cape-jones
    git rev-parse HEAD   # expect 184ee62775010e6c217dd9d6f4312040ea66725b

Get the disk mirror (archive of the worktree as it sat, minus .git):

    gh release download sitting-wt-mocapsit-20261019 --repo mhvnsnt/cape-jones -D wt-mocapsit-mirror
    cd wt-mocapsit-mirror
    cat wt-mocapsit-full.tar.gz.part-* > wt-mocapsit-full.tar.gz
    sha256sum wt-mocapsit-full.tar.gz
    # expect 6ec605bcee03fa0885a0528887506900c8f94ddd3ad5d4e11ade28efbc561a97
    tar -xzf wt-mocapsit-full.tar.gz -C <dest>

Re-run the retarget (per README, from repo root):

    xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender -b 3d-assets/living_room.blend --python production/tools/mocap-retarget/retarget.py
    # output: proof/sitting_mocap.blend (action `mocap_sit_113_15`, frames 1-81)

## WHAT'S LEFT + WHY

- CLEARED 2026-10-20: `git worktree remove` refused (10,399 unstaged deletions
  from the earlier partial clear); after the 100% verification above
  (branch pushed + merged, release digests, download-back reassembly, zero-diff
  extraction), removed with `--force` per the brief's re-verify condition.
  Confirmed gone from `git worktree list` and from disk. Nothing of this take
  remains local — by design; everything above is the pull-back path.
- More sitting clips (114_16, 13_01, 13_04, 14_27, 14_30, 114_05) were never
  pulled into the repo — README lists them as available.
- The 10,399 disk-deleted files live only in git history (184ee6277); if a
  future lane checks out this branch they return automatically.

## COMPARISON FEED (for the coordinator's takes-comparison doc)

- Take name: wt-mocapsit — real mocap retarget (CMU human motion)
- One-line: real human sitting motion recorded with sensors, translated onto
  his 94-bone rig, with his butt locked to the seat exactly
- Best at: natural motion (it IS a real person), exact seat/floor contact
- Roughest: only one clip finished; tuned to one seat position; fussy math,
  must follow README; props/table not handled
