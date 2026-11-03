# Xod parts — vendored + patterns

Source: github.com/CloudCorpRecords/xod, MIT (LICENSE.xod in this
folder), pinned at **v0.9.23, commit
6e5ebd4a0113bcf68800b6e034aa3d88e9b1f877**. Security audit:
`docs/research/cloudcorp-2026-11-02/audits/xod-parts.md` —
CLEAN-WITH-NOTES. Xod the app is NOT adopted (duplicates Muse;
Mac-first); these are the parts that upgrade our own systems.

## Vendored here

| File | What it is | Our use |
|---|---|---|
| `sentinel.py` | Provenance/injection gate: everything read from pages/files/apps is "untrusted", only user-typed text is "asked"; before any send/run/change it holds secret-out, page-sourced recipients, page-embedded instructions, download-and-run commands, and unasked deletes as approval cards with the rule named | agent-ops gate for outbound actions across lanes. Use the deterministic core (`begin`/`saw`/`review`); `review_message()` delegates to a host-configured LLM — wire deliberately or leave unhooked |
| `run_sentinel_test.py` | Upstream smoke test for the sentinel (stdlib only) | Proof it works — see TEST-RUNS.md |
| `benchmark.py` | Honest-grading harness: real requests verified against disk in a throwaway folder, published RELIABILITY.md scoreboard format | Proving Ground grading template |

## Patterns documented, not vendored (pull from the pinned commit when a lane builds them)

- **Scorecard** (`app/services/scorecard.py`) — CLEAN, read-only:
  turn self-checks, usage ledger, crew outcomes, routing evals over
  rolling windows. Pattern for Proving Ground scoring.
- **Missions verdicts** (`app/services/missions.py`) — claimed status
  kept apart from verified status, verdicts re-checked against disk
  at verdict time; approval waits exempt from timeouts. Pattern for
  lane handoffs: never report claimed as verified.
- **Board seat record** (`app/services/harness.py`) — a board job
  records the seat: model requested, model that actually ran, and
  how that is known (plainly "unknown" when unproven). Pattern for
  our agent board meetings. Note from audit: the seat record itself
  is created in crew.py, and harness.py also carries a separate
  family-relay tier that was NOT audited — take the seat-record
  pattern only.
- **Worktrees** (`app/services/worktrees.py`) — one git worktree +
  branch `xod/<job>` per job, review then merge/PR. Matches our lane
  isolation. Note: its `pull_request()` pushes to origin and its
  commits use `--no-verify` — review before adopting verbatim.
- **Agent CLI registry** (`app/services/agent_clis.py`) — headless
  run forms for Muse (`muse exec`), Claude Code (`claude -p`),
  Codex, Gemini CLI, Aider, opencode, Goose, Cursor, Amp; sign-in
  detected by file existence only; refuses
  `--dangerously-skip-permissions` / `--yolo` / `--yes-always`
  (UNSAFE_FLAGS, enforced). **EXCLUSION:** its `install()` helper
  runs hardcoded vendor curl|sh installers through a shell with the
  approval gate outside the function — do NOT port `install()`;
  registry + refusal rules only.
