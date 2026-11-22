# Free AI Coding Agents — Research & Setup (2026-10-16)

**STATUS: All 3 CLIs installed on the VM. Auth pending — needs parent browser delegation (see "AUTH STEPS NEEDED").**
- `agy` v1.4.0 at `~/.local/bin/agy` (add to PATH: `export PATH="$HOME/.local/bin:$PATH"`)
- `codex` 0.149.0 (global npm)
- `copilot` 1.0.98 (global npm)

Owner: Real. Account: fmmg.mars@gmail.com (Google sign-in blanket permission).
GitHub: mhvnsnt. Goal: multiple free AI agents working Western Heart + other repos in parallel.

**FIRST TEAM MISSION (owner 2026-10-16):** SF EX vertex decoding — Arika's custom
vertex format in PAC section 2 (SF EX Plus Alpha / EX2 Plus / EX3, PS1). File format
reverse-engineered, character files identified, but the 3D vertex geometry encoding is
NOT yet cracked. Findings: western-heart branch `feat/sfex-teardown-ex-plus-alpha`.
We need agents that do real RE research + teamwork, not code completion.

---

## Research findings (real 2026 data, verified 2026-10-16)

### TIER 1 — Set up (best fit for the mission)

#### 1. Google Antigravity CLI (`agy`) — PRIMARY PICK
- **Free:** Yes — Individual plan $0/mo, no credit card. Unlimited tab completions;
  agent requests on a weekly rate limit (free tier); higher quotas on Google AI Pro/Ultra.
- **Google sign-in:** Native — it IS Google's tool. First run opens browser OAuth;
  remote/SSH sessions print an authorization URL, you sign in and paste back the code.
- **Models:** Gemini 3.8 Flash / 3.1 Pro, Claude Sonnet 5 / Opus 5 (Pro+), gpt-oss-120b.
- **Parallel agents:** YES — built for it. Background agents (`agy run`, `agy list`,
  `agy attach`), Manager surface for orchestrating multiple agents across workspaces.
- **GitHub:** Works on local clones; `gh` CLI already on this VM for push/PR/merge.
- **RE fit:** Excellent — terminal-native, runs Python/scripts, reads binary formats,
  and the agent loop is plan-act-verify with artifacts (diffs, test runs, screenshots).
- **Install:** `curl -fsSL https://antigravity.google/cli/install.sh | bash`
  → `~/.local/bin/agy`. Go binary, SSH-friendly, headless-capable.
- **Status on this VM:** INSTALLING (see Setup log below).

#### 2. OpenAI Codex CLI — SECONDARY PICK
- **Free:** ChatGPT Free plan includes Codex with a limited trial (local tasks only,
  no cloud). No credit card. ChatGPT supports Google sign-in.
- **Parallel:** Cloud parallel tasks need Plus ($20/mo); locally, multiple CLI
  sessions can run in separate git worktrees.
- **GitHub:** Codex reads/modifies repos, runs tests, creates PRs (cloud PR review
  needs paid tier; local `gh` CLI covers PRs here).
- **RE fit:** Good — GPT-5.6-Codex family is strong at RE-style reasoning; open-source CLI.
- **Install:** `npm install -g @openai/codex`
- **Status on this VM:** INSTALLING (see Setup log below).

#### 3. GitHub Copilot CLI — TERTIARY PICK
- **Free:** Copilot Free — 2,000 completions/mo + 50 agent chats/mo. GitHub-native.
- **Sign-in:** GitHub account (mhvnsnt) via device flow in browser — no Google needed,
  but the GitHub account is already connected on this VM via `gh`.
- **Parallel:** One session per terminal; run several in separate worktrees.
- **RE fit:** Decent for code tasks; weaker than the above for open-ended RE research.
- **Install:** `npm install -g @github/copilot`
- **Status on this VM:** INSTALLING (see Setup log below).

### TIER 2 — Evaluated, not set up (reasons)

| Tool | Free tier | Verdict |
|---|---|---|
| Cursor (Hobby) | Free, no card | Desktop IDE only — no headless/VM story. Skip. |
| Windsurf → Devin Desktop | Free light quota (daily/weekly), unlimited completions | Desktop IDE only; company churn (Cognition). Skip. |
| Replit Agent | Starter free has daily credits but Agent 3 paywalled ($25/mo Core) | Real agent work needs paid plan. Skip. |
| Kiro CLI | Free 50 credits/mo incl. Claude Sonnet 4.5 | AWS Builder ID sign-in (not Google); quota thin. Backup option. |
| Aider / OpenCode / Cline / Roo | Free software, BYOK | Need paid API keys — violates free constraint unless paired with Gemini API free tier. Backup option. |
| Bolt.new / v0 / Lovable | Free tiers | Prompt-to-app builders, not repo agents. Wrong tool for RE work. |
| Google AI Studio (Gemini) | Free API tier | API key via browser; could power Aider/OpenCode free. Backup option. |

### Key 2026 landscape notes
- Gemini CLI is DEAD for free users (Google cut free access 2026-06-18, migrated to Antigravity CLI).
- Windsurf was acquired by Cognition, rebranded Devin Desktop (2026-06-02).
- Cursor is now part of SpaceX (2026-08-14).
- Codex is bundled with every ChatGPT plan including Free (limited).

---

## Setup log

### Antigravity CLI — INSTALLED
- Binary: `~/.local/bin/agy` v1.4.0 (211MB, checksum-verified by Google's installer)
- Verified: `agy --version` → 1.4.0; `agy --help` shows full agent flags
  (`--agent`, `--mode`, `--effort`, `-p/--print` non-interactive, background agents)
- **Auth flow captured:** `agy` prints a Google OAuth URL and waits 60s for either
  browser callback or a pasted authorization code:
  `https://accounts.google.com/o/oauth2/auth?...client_id=1071006060591-...apps.googleusercontent.com...`
  Scopes: cloud-platform, userinfo.email, userinfo.profile, cclog,
  experimentsandconfigs, aicode, openid. No credit card, no 2FA in the flow itself.
- **To complete (needs parent browser delegation):** run `agy` on the VM in a
  background PTY, capture the FRESH auth URL from output (the `state` param expires
  per-session — do not reuse a stale URL), open it in the browser task, sign in as
  fmmg.mars@gmail.com (blanket permission), copy the authorization code from the
  redirect page, feed it to the waiting process via stdin. Then verify with
  `agy -p "say hello"`.

### Codex CLI — INSTALLED
- `npm install -g @openai/codex` → codex-cli 0.149.0
- **To complete (needs parent browser delegation):** run `codex`, choose
  "Sign in with ChatGPT" → "Sign in with Google" → fmmg.mars@gmail.com in browser.
  Free tier = limited local tasks (enough to evaluate; cloud parallel tasks need Plus).

### Copilot CLI — INSTALLED
- `npm install -g @github/copilot` → GitHub Copilot CLI 1.0.98
- **To complete (needs parent browser delegation):** run `copilot`, follow the
  GitHub device flow: open github.com/login/device, enter the shown code while
  signed in as mhvnsnt. Free tier: 2,000 completions + 50 agent chats/mo.

## AUTH STEPS NEEDED (require browser — parent agent to delegate)

None of the CLIs can complete OAuth without a browser step. For each:

1. **Antigravity (`agy`):** Run `agy` on the VM → it prints an authorization URL →
   open in browser, sign in with fmmg.mars@gmail.com (blanket permission covers this) →
   paste the returned code back into the terminal. No credit card, no 2FA expected
   (if Google demands phone verification, STOP and tell the owner).
2. **Codex:** `codex` → sign in with ChatGPT → "Sign in with Google" →
   fmmg.mars@gmail.com in the browser.
3. **Copilot:** `copilot` → GitHub device flow → open github.com/login/device,
   enter the shown code while signed in as mhvnsnt.

## How to assign them work (once authed)

- **Antigravity (primary):** `cd <repo> && agy run "task brief"` per mission;
  `agy list` / `agy attach <session>` to manage parallel agents. Give each agent its
  own git worktree (`git worktree add`) so parallel RE experiments never clobber.
- **Codex:** `codex "task"` per worktree; local only on Free tier.
- **Copilot:** `copilot` interactive per worktree.

## Recommended team shape for the SF EX vertex mission

1. **Antigravity agent A:** PAC section 2 format deep-dive — map every byte of the
   vertex records, compare across the 3 games' character files.
2. **Antigravity agent B:** Cross-reference — how do other Arika PS1 games / PS1
   SDK docs describe vertex encoding? (GTE fixed-point formats, TIM/TMD parallels.)
3. **Antigravity agent C:** Empirical brute-force — write decoders for candidate
   formats (s16 variants, fixed-point scales), render, score for humanoid coherence.
4. **Codex/Copilot:** Docs + harness — keep the teardown docs current, maintain the
   test scripts, verify each hypothesis against known-good TMD extractions.

All on branch `feat/sfex-teardown-ex-plus-alpha`, separate worktrees, commits pushed
per hypothesis. Owner's law: verify with own eyes (render it), never claim solved
without a coherent mesh.
