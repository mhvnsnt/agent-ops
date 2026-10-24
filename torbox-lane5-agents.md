# Lane 5 — All-Agents Tooling on TorBox BAD_TOKEN (2026-10-20)

Evidence dir: `torbox-lane5-agents/` (one file per agent, verbatim outputs).
Same review prompt was given to every runnable agent: review `tb_reqdl.py`,
`tb_mylist.py`, `tb_export.py`, `torbox_add_magnet.py`, `CONNECTOR.md`,
`zip_extract.py` for the requestdl `?token=` / BAD_TOKEN bug. No secrets printed
(COPILOT_GITHUB_TOKEN checked by existence/length only: present in ~/.bashrc, 93 chars).

## Inventory corrections to the brief
- `opencode` DID survive: `~/.local/bin/opencode` v1.19.3 — it was just missing
  from this shell's PATH (`~/.local/bin` not in PATH), so `which` missed it.
- `codex` v0.149.0 at /opt/hatch-image/bin/codex. `gh` 2.102.0, logged in as mhvnsnt.
- Copilot CLI and Kilo CLI binaries did NOT survive the VM swap (config/state did:
  ~/.copilot with mhvnsnt logged in, ~/.config/kilo + ~/.local/share/kilo).
  Both were reinstalled via npm during this lane.
- aider / cline / gemini: not on PATH (unchanged).

## What each agent ACTUALLY did

### 1. Copilot CLI — ✅ RAN, full review (`copilot.txt`)
Reinstalled: `npm i -g @github/copilot` → GitHub Copilot CLI 1.0.100 at /usr/bin/copilot.
Ran non-interactively with COPILOT_GITHUB_TOKEN sourced from ~/.bashrc (value never logged).
Findings:
- **Root cause (likely): tb_reqdl.py sends the authd surrogate to TorBox as if it
  were the API key** — lines 15–17 extract `entry["surrogate"]` and insert it into
  `?token=`, with no Authorization header and no credential exchange. A surrogate is
  a broker-specific substitute, not a TorBox key; with bearer_header registration,
  manually moving it into `token` is the bug. Fresh keys failing doesn't rule this
  out — the request still wouldn't contain the fresh key.
- Ranked the other hypotheses low: URL-encoding is correct (`quote(..., safe='')`),
  path/order fine, redirect refusal would traceback not BAD_TOKEN, UA already set
  (Cloudflare 1010 ≠ BAD_TOKEN), plan cap would not be an auth error.
- **New bug found: `torbox_add_magnet.py` imports `add_surrogate_to_request` but
  calls `url_with_surrogate_query_param(...)`, which is not imported or defined →
  NameError before any request.** (Verified by reading the file in this lane.)
- Diagnostic sequence: baseline via tb_mylist.py → retry requestdl through the
  broker's supported query_param placement → capture status/body/redirect with
  token redacted → only then check plan/caps. Do NOT regenerate the key as a diagnostic.
- Caveat it stated itself: zip_extract.py access was denied in its sandbox, so it
  made no finding on that file; diagnosis is "strong, not proof" without the
  dynamic_credentials helper source.

### 2. Codex — ⚠️ direct lane 401; ✅ full review via Kilo gateway (`codex.txt`, `codex-kilo.txt`)
- Direct OpenAI lane: still broken. Exact error (codex.txt):
  `failed to connect to websocket: HTTP error: 401 Unauthorized, url: wss://api.openai.com/v1/responses`
  and `unexpected status 401 Unauthorized: Missing bearer or basic authentication in header`.
  Retried 5× then fell back; run was cut at timeout with the 401 already definitive.
- Via Kilo Code free gateway (`codex -p kilo-code exec`, model openrouter/free,
  provider kilo-code): **worked** (sanity test `CODEX_KILO_OK`, then full review, 135,195 tokens).
  It read the actual `dynamic_credentials` module, so its diagnosis is the most specific:
- **Root cause confirmed by code: surrogate substitution only happens for the
  registered placement.** `custom.torbox` is bearer_header; Sentinel/authd substitutes
  `hsurr:...` only in `Authorization: Bearer`. tb_reqdl.py:17-18 puts the literal
  surrogate in `?token=` → TorBox sees the surrogate → BAD_TOKEN.
- **More bugs: tb_mylist.py:13, tb_export.py:12, torbox_add_magnet.py:34 all call
  `url_with_surrogate_query_param` on a bearer_header credential → predicted
  `DynamicCredentialError: credential is not query_param` at runtime** (i.e. the
  "working" helpers would crash before sending, unless the credential was re-registered).
- Fix A (preferred if requestdl accepts Bearer): use `add_surrogate_to_request`,
  drop `&token=`. Fix B (if ?token= truly required): register a second entry with
  `{"query_param": "token"}` placement and use `url_with_surrogate_query_param` everywhere.
- Diagnostic sequence with expected outcomes for each step (placement print →
  tb_mylist crash test → Bearer-surrogate requestdl test).

**Consensus: Copilot and Codex/Kilo independently converged on the same root cause**
(surrogate in ?token= never substituted for a bearer_header credential). That also
explains the "every fresh key dies as BAD_TOKEN" saga: the failing requests never
contained any real key.

### 3. Kilo — ⚠️ native CLI blocked; gateway contributed (`kilo.txt`, `codex-kilo.txt`)
Reinstalled: `npm i -g @kilocode/cli` → kilo 7.8.15 at /usr/bin/kilo (`kilo --help` works).
- Native `kilo run "<review prompt>"`: **Error: "You need to sign in to use this model."**
  It defaulted to `google/gemini-3-pro-image` (stale session/model state), not the
  kilo-free config in ~/.config/kilo (config.json defines kilo-free/openrouter/free,
  but Kilo 7.8 logs a V1-compat warning that drops the `providers` block).
- `kilo run -m kilo-free/openrouter/free "Reply exactly: KILO_OK"`: timed out at 90s, no output (EXIT:124).
- `kilo auth list`: timed out at 30s, no output.
- Workflow-law exception invoked for the NATIVE binary: evidence above. BUT Kilo did
  contribute — the entire Codex review above ran on **Kilo Code's free gateway**
  (api.kilo.ai, openrouter/free, 200 req/hr/IP per the 2026-10-16 arsenal doc).

### 4. OpenCode — ❌ binary OK, runs never complete (`opencode.txt`)
`~/.local/bin/opencode` v1.19.3; `--help`/`--version` fine. Three `opencode run`
attempts (full review prompt; short prompt with `-m opencode/big-pickle` ×2):
each starts (`> build · big-pickle`) and produces **no completion within 110–300s**,
killed by timeout (EXIT:124). No provider is configured in ~/.config/opencode/opencode.jsonc
(empty schema-only file). Workflow-law exception: binary present and launching, model
calls stall in this VM; no review output obtained. Evidence in opencode.txt.

### 5. CodeRabbit — ⚠️ triggered on PR #36, no review received yet (`coderabbit-pr.txt`)
- No open TorBox PR existed in mhvnsnt/agent-ops (17 open PRs checked, none TorBox).
- Created branch `docs/torbox-lane5-agent-review-20261020` (fresh /tmp clone — the
  local agent-ops checkout is dirty on another PR branch and was not touched),
  added `TORBOX-LANE5-AGENT-REVIEW-2026-10-20.md` with the consensus findings,
  opened **PR #36: https://github.com/mhvnsnt/agent-ops/pull/36** with
  `@coderabbitai review` in the body, plus an explicit `@coderabbitai review` comment
  (comment id 6296484877).
- After ~10 minutes: no CodeRabbit comment/review on the PR (only mhvnsnt's trigger
  comment; reviews list empty). No `.coderabbit.yaml` in the repo, and `gh pr checks`
  is blocked by PAT scope ("Resource not accessible by personal access token"), so
  CodeRabbit's app installation on this repo could not be verified from here.
  Honest status: trigger delivered, review not (yet) produced — likely the
  CodeRabbit GitHub App is not installed/enabled on mhvnsnt/agent-ops.

## Bottom line for the TorBox problem
Two independent agents, one of which read the credential-broker source, agree:
**stop putting the surrogate in ?token=.** Next step is the 3-step diagnostic in
the PR doc (placement print → tb_mylist crash test → Bearer-surrogate requestdl),
then Fix A or B depending on whether requestdl accepts Bearer.
