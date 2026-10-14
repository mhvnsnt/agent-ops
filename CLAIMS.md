# CLAIMS (prevents collisions)

Protocol:
1. **Before starting**, append a line to the table below and push it (branch plus PR, or include it in your first work PR): agent, task, branch, start time (CT).
2. Check the table first. If someone else holds the task or the files, pick another task or coordinate in TAG-TEAM.md.
3. When you're done, set the status to `done` with a PR link, or `released`.
4. Temp files must be unique per agent and job, e.g. `/tmp/<agent>-<task>-$(date +%s)-body.md`. **Never use a shared `/tmp/body.md`.** Same for scratch dirs and clones.

| Agent | Task | Branch | Started (CT) | Status |
|---|---|---|---|---|
| Grok Bot | TAG-TEAM board + process docs | docs/tag-team-board | 2026-10-14 15:20 | done |
| Grok Bot | Goodville postmortem / cutouts / timeline | (see TAG-TEAM #6) | 2026-10-14 | active |
| Grok Bot | CI fixes (TAG-TEAM #7) | per repo | 2026-10-14 | active |
| Grok Bot | Fiverr gig 1 (browser) | n/a | 2026-10-14 | active |
