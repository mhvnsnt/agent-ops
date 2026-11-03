# agentsfile 0.1.0 — TEST RUN RESULT

- **Tool:** `@reneturcios/agentsfile` 0.1.0 (CloudCorpRecords/agentsfile, main @ 1c596b5, MIT)
- **Date:** 2026-11-02 (America/Chicago)
- **Run by:** test-run lane, cloudcorp-pullin-2026-11-02

## Method used (the only route that persists on this VM)

1. Repo tree checked via the GitHub MCP connector (`/opt/hatch/bin/github call-read-tool --name get_file_contents`): repo root has **no `dist/`** — the published package's `dist/` + `server.json` (`package.json` `files`) are build artifacts. In-repo there is only `src/*.ts`: `cli.ts`, `core.ts`, `index.ts`, `mcp.ts`, `types.ts`, plus `package.json` and `README.md`.
2. All source files fetched via `get_file_contents` and persisted with file-write tools into this directory (`src/`, `package.json`). **Byte-size verification against the repo tree listing: cli.ts 1937, core.ts 13631, index.ts 137, mcp.ts 1056, types.ts 378 — all exact matches.** (package.json persisted as compact JSON, 869 B vs the 1047 B pretty-printed original; semantically identical.) Note: the sibling lane's rumored `src/agentsfile/package.json` did not exist on disk — `~/workspace/cloudcorp-pullin-2026-11-02/src/` contains no `agentsfile/` folder.
3. Import check: the CLI path is dependency-light — `cli.ts` imports only `./core.js`; `core.ts` imports only `node:fs`/`node:path` and `./types.js`. The `@modelcontextprotocol/sdk` + `zod` imports live only in `mcp.ts`, which the CLI loads dynamically **only** for the `mcp` subcommand — so `check` needs no node_modules.
4. First run attempt (verbatim TS): `node --experimental-strip-types src/cli.ts …` **failed** — Node v24.22.1 type stripping does not remap `./core.js` → `./core.ts`:
   `Error [ERR_MODULE_NOT_FOUND]: Cannot find module '…/agentsfile-run/src/core.js' imported from …/src/cli.ts` (exit 1 from node itself).
5. Fix, mirroring how the package actually ships: hand-stripped JS equivalents of the verified TS written to `dist/cli.js`, `dist/core.js`, `dist/types.js` (types/interfaces/casts removed, logic unchanged). Those are what was executed below. The `check` path executed is the tool's own code; the MCP subcommand was not run (it would need the SDK, which cannot be installed persistently on this VM).

## Runs

Working directory for all commands: `~/workspace/cloudcorp-pullin-2026-11-02/test-runs/agentsfile-run/`
Targets were only read — nothing was written into `~/workspace/agent-ops` or `~/AGENTS.md` (the tool is read-only by design; audit verdict CLEAN).

### 1. Version

```
$ node dist/cli.js --version
0.1.0
exit code: 0
```

### 2. Instructed target: the agent-ops checkout

```
$ node dist/cli.js check /home/hatch/workspace/agent-ops
agentsfile check /home/hatch/workspace/agent-ops: MISSING
  files: 0, findings: 1 (high: 1, medium: 0, low: 0, info: 0)
  summary: 0 agent file(s) checked; 1 finding(s): 1 high, 0 medium, 0 low, 0 info. Verdict: MISSING.

(repo):
  [HIGH] NO-FILE Neither AGENTS.md nor CLAUDE.md exists at the repo root, so agents working in this repo have no instruction file to follow.

MISSING: neither AGENTS.md nor CLAUDE.md exists at the repo root.
exit code: 1
```

This is factually correct: `~/workspace/agent-ops/` has neither `AGENTS.md` nor `CLAUDE.md` at its root (verified by directory listing before the run), so the per-spec MISSING verdict + exit 1 is the tool working as documented — there were no instruction files in that checkout for it to validate.

### 3. Substantive target: our real AGENTS.md (single-file mode, root = ~)

```
$ node dist/cli.js check /home/hatch/AGENTS.md
agentsfile check /home/hatch/AGENTS.md: DRIFT
  files: 1, findings: 9 (high: 0, medium: 8, low: 0, info: 1)
  summary: 1 agent file(s) checked; 9 finding(s): 0 high, 8 medium, 0 low, 1 info. Verdict: DRIFT.

(repo):
  [INFO] NO-PACKAGE-JSON No package.json found at the repo root, so npm script references were not checked.

AGENTS.md:
  [MEDIUM] line 90 PATH-MISSING `workspace/exports/` Referenced path does not exist in the repo: workspace/exports/
  [MEDIUM] line 182 PATH-MISSING `server.py` Referenced path does not exist in the repo: server.py
  [MEDIUM] line 317 PATH-MISSING `voice-clone-work/cb_weights/` Referenced path does not exist in the repo: voice-clone-work/cb_weights/
  [MEDIUM] line 510 PATH-MISSING `setup_creds.py` Referenced path does not exist in the repo: setup_creds.py
  [MEDIUM] line 511 PATH-MISSING `setup_creds.py` Referenced path does not exist in the repo: setup_creds.py
  [MEDIUM] line 548 PATH-MISSING `cloud_dog.py` Referenced path does not exist in the repo: cloud_dog.py
  [MEDIUM] line 571 PATH-MISSING `tools/tripo-pull/tripo-pull.py` Referenced path does not exist in the repo: tools/tripo-pull/tripo-pull.py
  [MEDIUM] line 573 PATH-MISSING `tools/tripo-pull/` Referenced path does not exist in the repo: tools/tripo-pull/

DRIFT: at least one medium or high finding; the agent files disagree with the repo.
exit code: 1
```

Notes on the findings (human judgment, not tool output): they are real relative to the home directory as root — e.g. `tools/tripo-pull/` refers to the old `~/workspace/tools/` tree that was archived and deleted on 2026-10-31, and `setup_creds.py` / `server.py` / `cloud_dog.py` are bare filenames AGENTS.md mentions in the context of specific project subdirectories, not the home root. So most are context mismatches (AGENTS.md is a global home file, not a repo-root guide) rather than rot — but the `tools/` ones are genuine staleness the tool surfaced correctly. No CLAUDE.md exists at ~, so only AGENTS.md was checked; script references were not checked anywhere (no package.json at either target root, hence the single INFO).

## Verdict: useful, narrowly — YES for repo-root guides, not for our global AGENTS.md

- **It works, end to end, offline, with zero install** once the TS is built to JS: deterministic output, correct exit codes (0 VALID / 1 DRIFT / 1 MISSING), file+line+evidence on every finding, and its two verdicts on our material were both factually right.
- **Real signal:** it correctly caught that the agent-ops checkout has no root instruction file at all, and that `~/AGENTS.md` still references the archived-away `tools/` tree.
- **Limits for our setup:** it only understands repo-root `AGENTS.md`/`CLAUDE.md` with repo-relative backticked paths. Our main AGENTS.md is a global file whose paths are relative to many different project dirs, so most of its PATH-MISSING hits there are false-context noise. It would earn its keep run per-repo (e.g. inside western-heart / cape-jones checkouts that have root guides), not against the home file.
- **Caveat on this run:** execution used hand-stripped `dist/*.js` built from the byte-size-verified TS sources because Node's strip-types cannot resolve the source's `.js` import specifiers and npm/tsx/tsc cannot be installed persistently on this VM. The logic executed is the tool's own, unmodified; only type syntax was removed.

## Files in this run directory

- `src/cli.ts`, `src/core.ts`, `src/index.ts`, `src/mcp.ts`, `src/types.ts` — verbatim repo sources (byte-size verified)
- `package.json` — the package's manifest (compact JSON)
- `dist/cli.js`, `dist/core.js`, `dist/types.js` — JS build used for the runs above
- `RESULT.md` — this file
