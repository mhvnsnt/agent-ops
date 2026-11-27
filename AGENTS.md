# AGENTS.md

# ANTI-CLOBBER LAWS (owner 2026-10-17 — the DXMMII 54k-file wipe)

On 2026-10-17, commit cd3bf38 ("DXMMII limb system", PR mhvnsnt/western-heart#221) deleted 54,456 files against 105 additions. The commit message said nothing about deletions. Nobody read the deletion list before merging. The repo was 99.996% gone. These laws exist so that never happens again. Every agent, every repo, every commit, every merge.

1. DELETION CHECK — before every commit, read `git status` and the diff stat. Every deleted file in the diff must be something your task intended to delete. A deleted file your task did not delete on purpose means STOP: do not commit, do not push, report what you found. The working tree is wrong, not the task.

2. OWN THE TREE — never `git add -A` or `git commit -a` in a working tree you did not fully populate yourself. Before committing, verify the tree is complete: file counts match the remote branch you branched from (your task's own additions and changes aside). A tree missing files you didn't delete is damaged — don't sweep it into history.

3. CIRCUIT BREAKER — if a commit would delete more than a handful of files outside your task's scope, STOP and report instead of committing. A big deletion count is a hard stop, not a warning to scroll past. Committing unexplained deletions "and letting someone else figure it out" is the failure.

4. SAY THE DELETIONS — the commit message names every deletion. One deleted file gets one line; many deleted files get a count plus what category went. A commit whose message and diff disagree is a hard failure — don't push it.

5. MERGE GATE — the merger reads the PR's deletion list against the task description before merging. Unexplained deletions block the merge. "CI is green" does not excuse a deletion list the task never asked for. A red, conflicting, or lossy PR stays open with a comment naming the blocker.

(Co-authored with Aider and Copilot per the ALL-AGENTS-WORKFLOW LAW. Cline's seat stays open — its free-tier API was down during drafting.)

Instructions for every AI agent working in this repo.

## PRE-MADE PARTS FIRST

PRE-MADE PARTS FIRST (Mars, 2026-11-20): Don't hand-build what already exists and works well. Before decoding, decrypting, reverse-engineering, or building anything from scratch, go get the pre-made part from wherever it already exists and work FROM it. Sources: commercial games, open source, closed-source teardowns (study from public sources, rebuild equivalents), the fan translation / ROM hacking scene, the modding community, fan-made tools and docs, decompilations (decomps) and recompilations (recomps), community knowledge (Xentax/ZenHAX, TCRF, wikis, FAQs, archive.org). Like building a machine: you don't build a battery or a cog from scratch, you order the pre-made part and keep building. Spend the work on the innovative parts, not on re-doing what's already well-built. Only build from scratch what nobody has already built.

## No-data-loss rules (MANDATORY)
Read and follow [`docs/NO-DATA-LOSS-RULES.md`](docs/NO-DATA-LOSS-RULES.md) (canonical: mhvnsnt/agent-ops). No force-push, no rebase/amend of pushed work, no history rewrite, no branch/asset deletion without backup + owner approval, PRs only, empty D-filter + gitleaks + green CI before merge, push incrementally, keep WORKLOG, back up and sha256-verify before disk cleanup, never touch other agents' or Muse's work.

### NO-SPARSE-COMMIT LAW (2026-10-23 — the cape-jones #219 main wipe)
NEVER commit or push from a sparse/partial checkout. On 2026-10-23 the overnight pipeline committed PR #219 from a sparse checkout that materialized only docs/ — the merge DELETED the other 21 root entries from cape-jones main. A sparse checkout that looks complete can silently carry deletions. RULE: before any commit from a non-full clone, verify the working tree against the branch's real tree (diff the root listing, or compare tree SHAs). Default recovery path for a bad merge: revert the merge commit (-m 1) and re-add the branch's real payload — nothing lost on either side. When in doubt, build the commit via the Git Data API from verified tree SHAs instead of a local checkout. GOTCHA: gh's `-f content=@file` does NOT expand @file for the blobs API — base64 the content explicitly or the blob will contain the literal path string.

---

## MERGE QUEUE — COMING SOON (owner-ordered briefing, 2026-10-24)

Read this if you work on western-heart or agent-ops. Nothing changes today. This is advance notice only.

**What is changing:** soon, pull requests will merge one at a time, in a line, instead of every lane merging whenever it wants. Each PR in the line gets checked against the newest main before it goes in. That is called a merge queue.

**Why:** two lanes merged at almost the same time and one wiped out the other's work. The line stops that happening.

**What changes for your lane, once the flip happens:**
- Merging a PR directly will stop working. GitHub will reject a direct merge.
- Instead you add your PR to the queue. GitHub merges it when its turn comes, after re-checking it against the newest main.
- If the queue asks you to update your branch (because main moved under you), update it and it goes back in line. Do not force-push. Do not merge main into your branch by hand to get around it.
- The merge method stays "merge". Never squash, never rebase. Same as now.

**When:** NOT YET. The flip happens only after every active lane has confirmed it knows. This briefing is the advance notice — today, merging works exactly the way it always has.

**How to confirm:** reply "merge-queue briefing confirmed" in your chat, or drop that line as a comment on your PR, or tell the merge coordinator at your next check-in. Confirmations are tracked in mhvnsnt/agent-ops at `MERGE-QUEUE-BRIEFING-CONFIRMATIONS-2026-10-24.md`.

**Status 2026-10-24:** the queue plumbing is ready on both repos (western-heart PR #742 and agent-ops PR #39 both merged the merge_group triggers). The flip itself has NOT happened. No branch protection has changed.

## NO-TEMP-STORAGE LAW (owner 2026-11-21 ~16:33 EST — "why are u storing things in temporary where they can get wiped anyway?")
NEVER store work in /tmp or any temporary location that can be wiped. /tmp is a 512 MB tmpfs and a VM restart wipes it to zero — on 2026-11-21 it destroyed the Pyrite checkpoint, worktree, 8 proof shots, capture driver, suite log, and the Colosseum M2 extracts. That loss is the proof: anything stored in temp is already lost, it just doesn't know it yet.
1. EVERYTHING goes straight into the repo or a durable workspace directory the second it exists — checkpoints, captures, scripts, extracts, logs, proofs. Finished work belongs in the repo; nothing finished ever sits only in /tmp or only on local disk.
2. /tmp is for truly disposable scratch ONLY — something that can be regenerated in seconds and whose loss costs nothing. If losing it would cost even one minute of rework, it does not go in /tmp.
3. Any lane caught staging work in /tmp has violated the order — same as staging on local disk. Parents verify: no checkpoint, capture, script, or extract path in any brief points at /tmp.
4. Recovery from a wipe is re-derivation from the repo/release, never a shrug — the work survives because it was pushed, the temp copy is gone and stays gone.
Strengthens DIRECT-TO-REPO + CHECKPOINT-AND-SAVE: the repo is the save, temp is not storage.

## PULL-IN-FIRST LAW (owner order, Nov 27 2026)
Never hand-tool or build from scratch anything that already exists. Before writing new code, assets, rigs, animations, tools or pipelines, search for and pull in complete existing work in full: commercial/industry-standard tools the owner owns (e.g. Toon Boom Harmony), open-source engines, templates, kits and add-ons, mocap/animation libraries, and already decoded or deciphered formats and data (the owner's reverse-engineering and teardown repos, Tekken 7 Steam files, community modding tools). Wire them in instead of rebuilding. Hand-building is allowed only for the parts nothing existing covers, and the PR must say what was searched. Licensing: decoded commercial game data stays in private repos for reference; anything shipped or sold must use owned, licensed or open-licensed pieces.

## OWNER FOCUS (Nov 27 2026): models, animations, promo clips from extracted game data

Main focus set by the owner 2026-11-27: perfect Bannon and Western Heart character models and animations from the already extracted commercial game data (WWE 2K26 and other wrestling games for Bannon; Tekken 7/3, DOA, VF5 and the rest for Western Heart), then capture in-game stills, clips and promo videos that show them working. MoneyManBusch (Grok Bot) owns the Western Heart model/anim/promo lane and coordinates the Bannon model/anim/promo push; Claude keeps the Bannon engine lane; Muse and the others continue their lanes. Private projects: commercial data is the base, nothing sold yet. Pull-in-first, never hand-build. Full section: `HANDOFF.md`.
