# RESUME BRIEF — template for relaunching a dead lane (RESUME, NEVER RESTART)

A successor lane's first act is reading the checkpoint + branch + staged files
and continuing from the EXACT next step. A re-brief from the top is a violation
of the CHECKPOINT-AND-SAVE LAW and is the "running in circles" the owner
called out on 2026-11-16. Fill this in from the dead lane's checkpoint —
never from memory, never from the top.

```
RESUME BRIEF — <lane name> (successor to <dead agent id>)
Source of truth: <workdir>/CHECKPOINT.md (read it fully first)
Branch: <branch name> — last commit <sha> — <pushed/unpushed>
Staged/landed so far: <files + sizes/hashes, what is DONE>
Verified disk state (counted by me, not trusted from the old brief):
  - <what exists on disk right now, with numbers>
Known dead-lane partial state (verify each piece yourself, trust none of it):
  - <what the dead lane may have half-done; how to check it>
EXACT NEXT STEP (quote the checkpoint's own "exact next step" line):
  > <quote>
DO NOT redo: <list of completed steps — these are done, do not re-derive>
Gates that still stand: <the lane's gates, unchanged>
STOP conditions: <when to stop and report instead of improvising>
```

Rules for the writer of a resume brief:
1. The brief MUST contain the checkpoint's exact next step, quoted verbatim.
2. The brief MUST contain a verified disk-state count the writer did
   THEMSELVES (file counts, frame counts, cache counts — never the dead
   lane's numbers).
3. The brief MUST list what is DONE and forbidden to redo.
4. If the checkpoint is missing or stale, the brief says so plainly and the
   first step is re-establishing the checkpoint from disk — not re-briefing
   the whole task from the top.
