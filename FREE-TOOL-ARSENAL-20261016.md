# FREE TOOL ARSENAL — 2026-10-16

Complete inventory of free/open-source coding agents, IDEs, RE tools, and MCP servers.
All verified working (or documented with blockers). Budget: $0, no credit cards.

## CODING AGENTS (CLI)

### ✅ Codex CLI + Kilo Code Free Gateway — WORKING NOW
- **What:** OpenAI's Codex CLI routed through Kilo's free gateway
- **Invoke:** `codex -p kilo-code exec --skip-git-repo-check "<prompt>"`
- **Auth:** None needed. No API key, no account, no card.
- **Limits:** 200 requests/hour per IP
- **Caveat:** Free tier prompts may be used for training (Kilo Code terms)
- **Status:** Verified working with real commands by prior agent

### ✅ Kilo Code CLI (native) — INSTALLED
- **What:** MIT-licensed AI coding agent (successor to Cline/Roo Code). VS Code, JetBrains, CLI, Cloud.
- **Version:** 7.8.12
- **Invoke:** `kilo run "<message>"` (non-interactive) or `kilo` (TUI)
- **Install:** `npm install -g @kilocode/cli`
- **Auth:** Needs sign-in for default models. Free gateway config attempted but needs correct format.
- **MCP:** Built-in — `kilo mcp add/list/auth`
- **Models:** 500+ via gateway, BYOK at zero markup, local via Ollama
- **Status:** Installed and working. Auth needs setup for free tier.

### ✅ OpenCode — INSTALLED
- **What:** MIT-licensed provider-agnostic coding agent. 202k GitHub stars.
- **Version:** 1.19.3
- **Invoke:** `opencode`
- **Install:** `curl -fsSL https://opencode.ai/install | bash`
- **Auth:** BYOK (bring your own key)
- **Status:** Installed and working. Needs API key for models.

### ✅ Copilot CLI — INSTALLED (needs auth)
- **What:** GitHub's CLI coding agent with sub-agents (Explore/Task/Code Review/Plan)
- **Version:** 1.0.98
- **Invoke:** `copilot`
- **Auth:** `copilot login --device-code` → visit github.com/login/device → sign in as mhvnsnt
- **Free tier:** 2,000 completions + 50 chats/month
- **Status:** Installed. Needs browser auth (parent can delegate).

### ✅ Codex CLI (ChatGPT) — INSTALLED (needs auth)
- **What:** OpenAI's Codex CLI with ChatGPT plan
- **Auth:** `codex login --device-auth` → visit auth.openai.com/codex/device → sign in with Google
- **Status:** Installed. Needs browser auth (parent can delegate).

### ❌ Antigravity CLI (`agy`) — BLOCKED
- **What:** Google's free AI coding agent CLI
- **Blocker:** Needs interactive TTY for auth. Tried direct, background, `script` PTY, `expect` — all failed.
- **Web:** Signed in ✅ (fmmg.mars@gmail.com, free Individual plan)
- **Status:** Web ready, CLI blocked on interactive login.

### ⏸️ Aider — SKIPPED (disk full)
- **What:** Apache-2.0 git-native CLI agent. 48k stars, 4.1M installs.
- **Blocker:** pip install failed (system package conflicts), venv failed (disk 89% full)
- **Note:** No commits since May 2026 — project may be dying
- **Status:** Skip for now. Revisit when disk frees up.

### ⏸️ Goose — NOT INSTALLED (disk)
- **What:** Apache-2.0 MCP-driven automation agent. 54k stars.
- **Status:** Worth installing when disk allows.

## REVERSE ENGINEERING TOOLS

### ✅ xverter — WORKING
- **What:** Xbox/Xbox 360 game format converter. Any format in, any format out.
- **Location:** `~/workspace/tools/xverter/xverter` (18MB)
- **Invoke:** `~/workspace/tools/xverter/xverter info <file>` or `convert`
- **Formats:** XGD1/2/3, ISO, GOD, ZAR, CHD, ZIP, 7z, extracted folders
- **Status:** Verified working on Linux. Does NOT recognize current doa4.iso (format issue — DOA4 agent investigating).

### ⏳ Ghidra — INSTALL IN PROGRESS (other agent)
- **What:** NSA's free reverse engineering suite. Disassembly, decompilation.
- **Status:** Another agent is handling installation.

### ✅ ghidra-mcp — PRESENT
- **What:** MCP server bridge for Ghidra
- **Location:** `~/workspace/tools/ghidra-mcp/`
- **Files:** bridge_mcp_ghidra.py, ghidra-mcp-plugin.zip, extension/
- **Status:** Present, needs Ghidra installed to activate.

### 🔍 XGDTool — WINDOWS ONLY
- **What:** Xbox Game Disc Tool. Extract/convert Xbox OG and 360 discs.
- **Repo:** github.com/wiredopposite/XGDTool
- **Blocker:** Only Windows binaries in releases. Would need to build from source.
- **Status:** xverter covers this on Linux.

## MCP SERVERS

### Kilo Built-in MCP
- **Invoke:** `kilo mcp add <name>`, `kilo mcp list`
- **Status:** Ready to configure once providers work.

### ghidra-mcp
- **Location:** `~/workspace/tools/ghidra-mcp/`
- **Status:** Ready, needs Ghidra.

## FREE API KEYS (to collect)

These all have legitimate free tiers. Keys go through Secure Vault, never in files/chat.

- **Groq** — Free tier, fast inference. groq.com
- **Mistral** — Free tier. mistral.ai
- **Google AI Studio** — Free Gemini API tier. aistudio.google.com
- **OpenRouter** — Free models available. openrouter.ai

**Action needed:** Parent should delegate browser tasks to sign up for these (Google blanket permission covers Google AI Studio).

## QUICK REFERENCE

| Tool | Command | Auth | Status |
|------|---------|------|--------|
| Codex+Kilo | `codex -p kilo-code exec` | None | ✅ Working |
| Kilo CLI | `kilo run` | Sign-in needed | ✅ Installed |
| OpenCode | `opencode` | BYOK | ✅ Installed |
| Copilot | `copilot` | Device flow | ⏳ Needs browser |
| xverter | `~/workspace/tools/xverter/xverter` | None | ✅ Working |
| Ghidra | (installing) | None | ⏳ Other agent |

## NEXT STEPS

1. Get free API keys (Groq, Mistral, Google AI Studio) via browser
2. Configure Kilo CLI with working free provider
3. Install Goose when disk allows
4. Wire MCP servers once Ghidra is up
5. Document everything in western-heart teardown/ docs
