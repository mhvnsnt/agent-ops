# HANDOFF — Agent Ops

**Last updated: 2026-11-22 (America/New_York).**
**Repo:** `mhvnsnt/agent-ops` (PUBLIC), default branch `main`.
**Purpose of this file:** any agent that picks up work here reads this FIRST, then the linked docs. It states what we've done, where we're at, and what we're working toward — so the owner can say "go to this repo, pick up the work" and you just know. Update this file in the same PR whenever the state changes (add, don't delete).

## 1. What this repo is

Agent operations: checkpoints, watchdog, Proving Ground, the overnight pipeline, and the merge-queue sync. This is the ops home — the machinery that keeps all the other repos' lanes moving, synced, and verified. If a lane's checkpoint, queue state, or cleanup log lives anywhere, it lives here (or points here).

Two files every lane should know: the teardown-idle queue (`TEARDOWN-IDLE-QUEUE.md`) and the disk cleanup log (`disk-cleanup-log.md`). The idle queue is where unfinished teardowns get logged before any game file is cleared; the cleanup log records every deletion + backup location.

## 2. Where we're at

### DONE
- **Overnight pipeline queue sync — running daily (2026-11-22).** Merge queue syncs #1003 (58d5a6f) and #1004 (0f3f374, merge-queue-sync-20261122T1144Z) landed today; the overnight pipeline keeps the cross-repo queue current.
- **Releases:** `wave2-proofs-backup-20261030` (2026-10-31); `lane-archive-stepwave-work-20261120` (draft).

### IN PROGRESS
- **Queue sync addendum (open PR #952).** Overnight pipeline 2026-11-20T05:44Z: queue sync addendum. Open since 2026-11-20, not merged.

### BLOCKED
- **Nothing blocked.** The ops pipeline is running. The known cross-repo blockers live in their own repos' HANDOFF.md files (Bannon #309–#311 conflicts, physics-playground #246 e2e, pokemon-arena-3d GFPAK-OPEN safety stop) — this repo tracks them, it doesn't own them.

## 3. What we're working toward

**The goal:** every lane checkpointed, every queue synced, every deletion logged, nothing ever lost. The ops repo is the save system for the whole operation: a lane that dies leaves a resume point, not a mystery.

**The bar:** the checkpoint-and-save law, enforced everywhere. Disk is a cache, not storage — everything on disk must also live in a store (GitHub or TeraBox) AND remain reachable/usable for work, with pull-back commands recorded. Staging into the repos is still the bottleneck; finished work goes into the repo the same day it lands.

## 4. Standing rules that apply here

- **Branch → PR → merge, always.** Never push to main directly. Add-only, zero-conflict PRs, no force pushes.
- **Checkpoint-and-save law (owner, 2026-11-09):** CHECKPOINT.md FIRST, before any substantive work, updated after EVERY meaningful step — what's done, every artifact's path + size/hash, results/numbers, and the EXACT next step. The repo is the save: payloads push to the PR branch INCREMENTALLY as each piece completes. Resume, never restart.
- **No-temp-storage law (owner, 2026-11-21):** nothing in /tmp or any wipeable location, ever. /tmp is a 512 MB tmpfs and a VM restart wipes it to zero — it destroyed a checkpoint, worktree, proof shots, and a capture driver in one wipe. Everything goes straight into the repo or a durable folder the second it exists.
- **No-gaps / solve-it law:** a gap or block is never the end of the work — route-switch until it's done or every reasonable route is exhausted with exact errors recorded.
- **Disk laws (owner):** safe-storage-first; disk storing/moving, never disk clearing; continuous mirror — upload new arrivals incrementally WHILE work is mid-download/mid-upload/unverified. One-store rule: a file may be cleared from local disk only when verified 100% byte-identical (hash/size) on GitHub OR TeraBox, with retrievability proven (pull-back actually works — a listing alone is not proof), no teardown actively in progress on it, unfinished teardowns logged on the idle queue FIRST, and every deletion logged to `disk-cleanup-log.md`.
- **Never-kill-in-progress law (owner, 2026-10-15):** never kill, stop, delete, or interrupt anything in progress — downloading, uploading, loading, processing, rendering, extracting — without his explicit approval. Especially when close to done.
- **Never-delete-game-files (guarded path):** game files go through the same store → verify → clear pipeline with the STRICTEST bar (100% byte-identical verified, retrievability proven, store surfaced to him, never silent).
- **No hand-tooling:** use the full systems (Ghidra, MCP, existing RE frameworks and pipelines), not one-off scripts guessing at formats.
- **Sign-in standing approval:** Google/Gmail (fmmg.mars@gmail.com) and GitHub (mhvnsnt) are blanket-approved forever. Never ask him to do sign-in steps himself.

## 5. Key files and paths

| What | Where |
|---|---|
| Teardown idle queue | `TEARDOWN-IDLE-QUEUE.md` (log unfinished teardowns here BEFORE clearing any game file) |
| Disk cleanup log | `disk-cleanup-log.md` (every deletion + backup location) |
| Checkpoints / watchdog / Proving Ground | Ops directories in repo (see README) |
| Overnight pipeline / queue sync | Pipeline configs + sync commits (e.g. #1003 / #1004) |
| Releases | `wave2-proofs-backup-20261030`, `lane-archive-stepwave-work-20261120` (draft) |
| Open PRs | #952 Overnight pipeline 2026-11-20T05:44Z: queue sync addendum |

## 6. Open decisions needing the owner

- **PR #952 (queue sync addendum):** merge, or hold? His call if it needs one — it is a sync addendum, and the syncs around it already landed.
- **Disk pressure calls:** when disk hits 80–85%, the move is store-first then clear per the one-store rule. Any deletion of a game file that is NOT 100% verified on a store needs his explicit go-ahead — lanes never decide that alone.

## 7. How to pick up

1. Read this HANDOFF.md first, then the README in the repo.
2. Check what other agents are already doing before starting anything (never start a duplicate session).
3. Resume from the stated next step — the overnight pipeline and queue sync are the heartbeat; PR #952 is the only open item. Never restart, never re-derive finished work.
4. Land work branch → PR → merge, add-only. Never push to main directly, never force.
5. Update this HANDOFF.md in the same PR when the state changes. Log every deletion. A lane that dies leaves a resume point, not a mystery.
