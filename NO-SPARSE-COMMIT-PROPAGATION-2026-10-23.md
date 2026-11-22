# NO-SPARSE-COMMIT LAW propagation run — 2026-10-23

Run by overnight pipeline subagent. PR #43 ("NO-SPARSE-COMMIT LAW") merged in
mhvnsnt/agent-ops 2026-10-23; this run checked the 7 game repos for propagation.

## Canonical text (mhvnsnt/agent-ops AGENTS.md, main, lines 24–25 — copied verbatim from the contents API)

> ### NO-SPARSE-COMMIT LAW (2026-10-23 — the cape-jones #219 main wipe)
> NEVER commit or push from a sparse/partial checkout. On 2026-10-23 the overnight pipeline committed PR #219 from a sparse checkout that materialized only docs/ — the merge DELETED the other 21 root entries from cape-jones main. A sparse checkout that looks complete can silently carry deletions. RULE: before any commit from a non-full clone, verify the working tree against the branch's real tree (diff the root listing, or compare tree SHAs). Default recovery path for a bad merge: revert the merge commit (-m 1) and re-add the branch's real payload — nothing lost on either side. When in doubt, build the commit via the Git Data API from verified tree SHAs instead of a local checkout. GOTCHA: gh's `-f content=@file` does NOT expand @file for the blobs API — base64 the content explicitly or the blob will contain the literal path string.

## Per-repo outcome: all 7 SKIPPED — already present on main

Verified via `gh api repos/mhvnsnt/<repo>/contents/AGENTS.md` (contents API, i.e. main branch) on 2026-10-23 ~15:45 CDT. Per task rules, any existing wording counts as present.

| Repo | Status | AGENTS.md line | Wording |
|------|--------|---------------|---------|
| mhvnsnt/western-heart | skipped-already-present | L84 | Variant wording: "## NO-SPARSE-COMMIT LAW (owner 2026-10-23 — the cape-jones #219 main wipe)" + numbered rules; own phrasing but the same law |
| mhvnsnt/cape-jones | skipped-already-present | L151 | Verbatim canonical text (### heading variant) |
| mhvnsnt/Bannon | skipped-already-present | L61 | Law present (### NO-SPARSE-COMMIT LAW, owner 2026-10-23 heading variant) |
| mhvnsnt/brutal-fist | skipped-already-present | L858 | Variant wording: "## NO-SPARSE-COMMIT LAW (owner 2026-10-23 — the cape-jones #219 main wipe)" + numbered rules; own phrasing, same law |
| mhvnsnt/wrestling-game | skipped-already-present | L32 | Verbatim canonical text (### heading variant) |
| mhvnsnt/game-reverse-engineering | skipped-already-present | L43 | Verbatim canonical text (### heading variant) |
| mhvnsnt/ConcreteDragon | skipped-already-present | L78 | Variant wording: "## NO-SPARSE-COMMIT LAW (owner 2026-10-23 — the cape-jones #219 main wipe)"; own phrasing, same law |

## Actions taken

- None. No commits, no PRs, no merges — all 7 repos already carry the law in AGENTS.md on main (verbatim in cape-jones, wrestling-game, game-reverse-engineering; same-law variant phrasing in western-heart, Bannon, brutal-fist, ConcreteDragon).
- This file created as the run report per task instruction.

## Notes / follow-ups

- Wording differs across repos (### vs ## heading; "owner 2026-10-23" vs "2026-10-23" date tag; numbered-rules variants vs single-paragraph). All carry the operative rule (never commit/push from a sparse/partial checkout, verify tree / use Git Data API). No action required unless the owner wants verbatim harmonization — flag as a question, not a blocker.
- cape-jones has the law verbatim; the #219 incident that created the law occurred there, so no further work needed there.
