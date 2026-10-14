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
| Repo Co Dev | AshLanev2 PR #38 + #42 (crash fix / visual tests) | ashlanev2/pr-38-42 | 2026-10-14 15:23 | active |
| Repo Co Dev | western-heart Godot Lab 1v1 + T6/TTT2 importers | western-heart/lab-1v1 | 2026-10-14 15:23 | active |
| Repo Co Dev | Shared creation suite + jiggle physics (western-heart docs/creation-suite) | western-heart/creation-suite | 2026-10-14 15:23 | active |
| Repo Co Dev | Brutal-Fist all-character model audit + Tripo intake pipeline | brutalfist/model-audit-tripo | 2026-10-14 15:23 | active |
| Repo Co Dev | Cloudflare Pages deploys (bannon / brutalfist / ashlane-1aa) | cf-pages-deploys | 2026-10-14 15:23 | active |
| Repo Co Dev | Playtest + gameplay/animation fixes: AshLane, western-heart Lab, Brutal-Fist (not Kobra models) | playtest/2026-10-14 | 2026-10-14 15:58 | active |
| Grok Bot | western-heart per-character height/scale metadata applied at runtime (owner rule c); data file + loader only, no Lab engine edits beyond a scale hook | grok/wh-height-scale | 2026-10-14 16:45 | PR western-heart #120 (open, waits on owner OK of T7/T8 heights) |
| Grok Bot | western-heart menu/UI/HUD system (title, modes, char select, VS, HUD, pause, results); no physics / creation-suite physics / model-wiring files | grok/wh-menu-ui | 2026-10-14 16:57 | active |
