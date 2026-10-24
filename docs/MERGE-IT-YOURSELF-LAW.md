# MERGE-IT-YOURSELF LAW (owner 2026-10-15) — canonical copy

> "Stop leaving things open for me to merge... I don't like to manually handle PRs."

When a PR satisfies ALL merge conditions (GitHub says MERGEABLE, CI green, no-deletion guard clean, gitleaks clean, build passes), MERGE IT — do not leave it open for the owner. He does not want to manually handle PRs.

The merge must be CLEAN and NON-DESTRUCTIVE: merge commits, never rebase/squash/force-push; resolve conflicts by keeping both sides' work — nothing lost, nothing clobbered, nothing destroyed on either side. Verify the merged result still builds and passes tests before calling it done.

A PR that is red, conflicting, or would lose work stays OPEN with a comment naming the blocker (existing rule) — but the default for a clean, green PR is MERGE, never "leave it for the owner."

This REPLACES the old "open PR, do NOT merge (owner merges)" instruction everywhere it appears: worker briefs, coordinator instructions, handoff docs, repo AGENTS.md copies. Update them.

Carve-outs (standing owner decisions, not overridden): never merge a DRAFT PR; never merge a PR the owner explicitly excluded (e.g. Bannon #78 stays draft per owner 2026-10-15).
