# Free CLI Coding Agents — Setup Report 2026-10-16

## ✅ WORKING NOW (no auth needed)

### Codex CLI + Kilo Code Free Gateway — PRIMARY RECOMMENDATION
- **Status:** ✅ INSTALLED AND VERIFIED WORKING
- **Cost:** $0, no API key, no account, no credit card
- **How it works:** Codex CLI (already installed v0.149.0) pointed at Kilo Code's free gateway
- **Config:** `~/.codex/kilo-code.config.toml` (downloaded from awesome-free-ai-coding)
- **Usage:** `codex -p kilo-code exec --skip-git-repo-check "<prompt>"`
- **Verified:** Responded successfully to test prompt via kilo-code provider
- **Limits:** 200 requests/hour per IP (Kilo Code free tier)
- **Caveat:** Free models may train on prompts (per Kilo Code terms)
- **Models:** Rotating free lineup (currently `openrouter/free`)

### FreeBuff — Ad-Supported CLI
- **Status:** ⏳ INSTALLED, downloading 49MB binary on first run
- **Cost:** $0, no API key, no credit card (ad-supported)
- **Install:** `npm install -g freebuff` ✅ done
- **Usage:** `freebuff` in project directory
- **Limits:** 5 free hours/day on DeepSeek V4 Flash
- **Note:** Uses Chinese models (DeepSeek) — policy consideration for sensitive work

## ⏳ WAITING FOR BROWSER AUTH

### GitHub Copilot CLI
- **Status:** ⏳ Device code waiting
- **Code:** `0055-B25A`
- **URL:** https://github.com/login/device
- **Account:** Sign in as mhvnsnt
- **Free tier:** 2,000 completions + 50 chats/month
- **Action needed:** Parent agent to complete via browser task

### Codex CLI (ChatGPT auth)
- **Status:** ⏳ Device code waiting (may expire — 15 min window)
- **Code:** `13SS-10RRH`
- **URL:** https://auth.openai.com/codex/device
- **Account:** Sign in with ChatGPT (Google OAuth: fmmg.mars@gmail.com)
- **Free tier:** ChatGPT Free includes limited Codex
- **Action needed:** Parent agent to complete via browser task
- **Note:** Kilo Code gateway already works, so this is optional/bonus

## ❌ BLOCKED

### Antigravity CLI (`agy`)
- **Status:** ❌ BLOCKED on interactive auth
- **Web:** ✅ Signed in (fmmg.mars@gmail.com, free Individual plan)
- **CLI:** Requires interactive TTY for login — cannot complete from headless VM
- **Tried:** Direct run, background, `script` PTY emulation, `expect` automation — all failed
- **Workaround:** User can sign in from a real terminal; web account is ready

### OpenCode
- **Status:** ⏳ Install in progress (npm)
- **Auth:** Requires API key (BYOK) — not free without one
- **Verdict:** Skip unless paired with a free API endpoint

### Aider
- **Status:** Not installed
- **Auth:** Requires API key (BYOK) — not free without one
- **Verdict:** Could work with Kilo Code gateway or other free OpenAI-compatible endpoint, but Codex CLI already covers this use case

## 🎯 RECOMMENDED SETUP

For immediate use:
```bash
# Free coding agent, no auth needed
codex -p kilo-code exec --skip-git-repo-check "your prompt here"

# In a git repo (trusted directory), skip the --skip-git-repo-check flag
cd ~/workspace/your-project
codex -p kilo-code exec "your prompt here"
```

## Next Steps for Parent Agent
1. Complete Copilot device auth via browser: https://github.com/login/device, code `0055-B25A`
2. Complete Codex device auth via browser (if code still valid): https://auth.openai.com/codex/device, code `13SS-10RRH`
3. The Kilo Code + Codex CLI combo is ready to use NOW for all coding agent work
