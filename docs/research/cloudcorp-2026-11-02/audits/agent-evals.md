# Security Audit — agent-evals

- **Repo:** github.com/CloudCorpRecords/agent-evals (MIT)
- **Version:** 0.1.0 (`package.json`)
- **npm:** name is unscoped `agent-evals`; **no `bin` entry** in `package.json` — run via the `evals` script (`tsx src/index.ts`) / `npx agent-evals` per README.
- **Dependencies:** `@anthropic-ai/sdk ^0.30.0`, `@modelcontextprotocol/sdk ^1.0.0`, `commander ^12.0.0`; dev `@types/node ^20`, `tsx ^4`, `typescript ^5`. Note: all three runtime deps appear **unused** in `src/` — the judge calls the Anthropic API with raw `fetch`, the MCP agent adapter is hand-rolled JSON-RPC over `fetch`, and argv is parsed manually. Unused deps are a hygiene note, not a security issue. `web/` is a separate Next.js leaderboard viewer with its own `web/package.json`.
- **Method used:** `git clone` is broken VM-wide (“unable to write symref for HEAD: Operation not permitted”) and codeload tarballs return 0 bytes through the proxy, and tar extraction into the scratch tree hit write-EPERM — so no local `src/` copy could be persisted. Primary method per coordinator: `gh api repos/CloudCorpRecords/agent-evals/git/trees/main?recursive=1` for the file inventory and `gh api repos/CloudCorpRecords/agent-evals/contents/<path>` (base64 content) for source, cross-checked with streamed `raw.githubusercontent.com` reads: full-file reads of `package.json`, `src/agent.ts`, `src/index.ts`, `src/runner.ts`, `src/scorer.ts`, and `grep -n` scans of the remaining files listed under Coverage. Nothing was installed or run.
- **Coverage:** All executable source covered — `package.json` (+ `web/package.json`), every file in `src/` (`agent.ts`, `index.ts`, `runner.ts`, `scorer.ts`, `types.ts`, `suites/latency.ts`, `suites/rag-accuracy.ts`, `suites/tool-use.ts`), plus `test/*.ts`, `web/app/page.tsx`, `web/app/layout.tsx`, `README.md`, `data/rag-corpus.json` (scanned). Bundled `results/*.json` are data outputs (inventoried, not code). No Dockerfile in this repo.

## Findings

- **Install hooks:** Scripts are `evals`, `build`, `test` only. **No** `preinstall` / `postinstall` / `prepare`.
- **Network egress — two destinations, both are the tool's job:**
  1. **User-supplied agent endpoint.** `src/agent.ts` `httpAgent(baseUrl)` does `fetch(\`${url}/run\`, POST {input, tools})`; `mcpAgent(serverUrl)` does `fetch(serverUrl, POST JSON-RPC tools/call)`. The URL comes from the required `--agent <url>` CLI flag (`src/index.ts` `cmdRun`). No default or hardcoded third-party agent endpoint.
  2. **Hardcoded Anthropic judge endpoint.** `src/scorer.ts` `llmJudgeScorer` does `fetch("https://api.anthropic.com/v1/messages", …)` with header `x-api-key` and default model `claude-haiku-4-5-20251001`. It sends the eval case input, the expected answer, and the agent's output to Anthropic for PASS/FAIL grading. It only runs for cases whose judge is neither `exact` nor `keyword` (`src/runner.ts` `scoreCase`), and if the key is unset it returns “skipped” **without** calling out.
- **Credential / env access:** Exactly one key in the whole tool: `src/scorer.ts` reads `process.env.ANTHROPIC_API_KEY`. No other `process.env` in `src/` (test file `test/scorer.test.ts:95` deletes it for tests). No `~/.ssh`, `~/.aws`, Keychain, or browser-profile access.
- **Code execution:** No `child_process`, `eval`, or `new Function` anywhere in `src/`.
- **Filesystem:** `src/index.ts` writes only under a CWD-relative `results/` dir, and only with `--publish`: `results/<agent>-<suite>-<timestamp>.json`, plus `results/leaderboard.json` regenerated from `results/*.json` (also rewritten by the `leaderboard` command). Reads are `results/*.json` and the bundled `data/rag-corpus.json`.
- **Web viewer:** `web/app/page.tsx` reads the results/leaderboard files server-side and renders them; no egress found (grep-verified). Docs reference `http://localhost:3000` as an example agent URL.
- **Distinct hosts:** `api.anthropic.com` (hardcoded, judge only), whatever host the user passes to `--agent`, `localhost` (docs example). No telemetry/analytics endpoints.
- **Obfuscation / data collection:** None. Plain readable TypeScript; bundled `results/*.json` are the author's mock-run outputs.

## Verdict: CLEAN-WITH-NOTES

Notes are exactly the egress/env above, both intrinsic to an eval harness: (1) it POSTs eval inputs/outputs to the **user-supplied** agent URL — its job; (2) the LLM-judge scorer sends case input + expected + agent output to **`api.anthropic.com`** using **`ANTHROPIC_API_KEY`** from the environment, only when an llm-judged case runs and the key is set. No other egress, no other secrets, no install hooks, no subprocesses.
