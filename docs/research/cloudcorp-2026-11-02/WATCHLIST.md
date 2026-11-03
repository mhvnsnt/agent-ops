# CloudCorpRecords — RESEARCH / WATCH list (everything not in the top 25)

Logged 2026-11-02 per owner order: every CloudCorpRecords repo that
was NOT pulled in is recorded here as RESEARCH/WATCH, with what it
could help us with. The full per-repo table (name, license, language,
last updated, description) is `INVENTORY.md` in this folder — each
repo's description there is its one-line "what it is"; the notes below
add "what it could help us with" by group. 355 repos total in the
inventory (265 originals + 90 forks), minus xod/internet-of-things,
minus the 25 pulled in (see README.md in this folder).

## Rules for this list

- **No-license / NONE / NOASSERTION repos = WATCH / IDEAS ONLY.**
  Never pull code from them. (45 NONE + 15 NOASSERTION in the sweep.)
- **Forks are not CloudCorpRecords code.** If a fork looks useful,
  evaluate and pull from UPSTREAM, never from this account.
- **AGPL/GPL repos** (6 AGPL-3.0, 2 GPL-3.0): document-only unless a
  lane confirms the license fits the destination repo.
- Anything promoted off this list goes through the same gate as the
  top 25: source security audit → pinned pull-in → test-run on our
  own material. No exceptions.

## Groups and what they could help with

### The *-port SaaS wrapper fleet (~120 repos, mostly MIT/TypeScript)
Clean-room MCP rebuilds of known services — CRM (crmport HubSpot,
crmcloud Salesforce), payments (payport Stripe), comms (channelchat
Slack, chatport WhatsApp, mailport Gmail), cloud (deployport Vercel,
cloudpanel Azure, clusterport kubectl, containerport Docker), data
(databridge-kit SQL, cacheport Redis, pgport Postgres), search
(searchport Brave, deepsearch Exa, crawlport Firecrawl).
**Help potential:** LOW for now — we already have official connectors
or better routes for nearly all of these (GitHub MCP/`gh`, Google
connectors, Vercel connector, Stripe connector). WATCH for: any
service we adopt later that has no official MCP — a *-port wrapper
plus a fresh audit is a fast starting point. Subsets are partial
(e.g. animeport is 20 of 42 upstream tools), and several depend on
hosted/keyed backends rather than being fully local.

### Original fleet beyond the top 25 (MIT unless noted)
- **greenlight-adjacent:** claimcheck, gatefile, gapproof,
  reprocheck, tracewatch, claimcheck — release/claim hygiene;
  claimcheck is in the index of candidate promotions (it was #26 in
  spirit; audit before use like everything else).
- **Repo hygiene cluster:** contextbudget (token-budget auditor —
  could help lane context discipline), envdoctor, envdoc, linkrot,
  lockdrift, installaudit, npmpreflight, tododebt, typosquat,
  wallcheck, readmeaudit-adjacent tools — cheap deterministic CI
  checks; promote individually if a lane hits the matching pain.
- **Agent tooling:** burnmeter (Claude Code token analytics — could
  feed Proving Ground cost scoring), thinkstep, termmux,
  sandboxrun, deskcommand, inboxwatch — WATCH.
- **Media/voice beyond the pulled four:** cliqwise (video→vertical
  clips; finished-episode sources only per CLIP SOURCE LAW),
  voicegen-port (ElevenLabs MCP — complements our connector),
  musicport (Spotify MCP), videohub-port (YouTube Data API) —
  promote when the Wizard Gang / Concrete Dragon clip lanes need
  them, with audit.
- **Browser/QA:** browserdebug (Chrome perf/network/console),
  browserstage/headlessstage (audited in the sweep as effectively
  stubs standalone — no browser bundled; executor must be injected)
  — WATCH, do not rely on them as-is.
- **Hosted-key products (deprioritized by design):** taskpilot
  (api.coderide.ai), cueport (api.cueapi.ai), policyrecall (hosted
  signed-memory), visualdiff (SnapDiff API) — they need third-party
  hosted services; specforge (pulled in) covers the local-first
  equivalent ground.
- **Games in the account:** open-city-remake (MIT, GTA-style web
  slice), strikemobile (MIT, UE5 tactical FPS), test-ai (Godot
  experiments) — design/reference reading only; neither maps onto
  western-heart (web fighting) or Bannon (wrestling) without an
  engine switch.
- **Exotic public-data wrappers:** brdata, ashareport, procureport,
  myopendata, chainlens, lancontrol, nasport, topiclint — no current
  fit; WATCH only.

### No-license watch-only (IDEAS ONLY — never pull code)
- **ai-handoff** — two AIs hand off via one shared
  `docs/AI_HANDOFF.md` per repo with MCP tools
  handoff_read/append/ask/answer. The IDEA fits our TAG-TEAM /
  no-relay handoff system; implement our own version if wanted.
- **musicboi** — MusicGen + local DAW in Electron (3 stars, no
  license). Idea watch for the music lanes.
- **agent-eval-harness, context-budget-analyzer, browserboi,
  nightshift-gb10** — prototypes/patterns only (agent-evals, the
  MIT one, is the pulled-in eval harness).

### Forks worth knowing (pull from UPSTREAM if ever used)
- **squidbrake** (Apache-2.0) — "agents propose, people approve"
  gate with tamper-evident record; matches the Xod approval model —
  candidate for the agent-ops safety layer.
- **cuga-agent** (Apache-2.0, IBM) — enterprise agent harness;
  Proving Ground benchmark/reference.
- **manim** (MIT) — mathematical animation engine; cartoon-factory
  explainer segments.
- **soundcraft** (Apache-2.0) — scriptable DAW in Rust; music/voice
  production research.
- **SceneDreamer** (no license in API) — 3D scene generation;
  Forge3D research only.
- **activepieces / composio / n8n** — automation aggregators; we
  already have a Composio skill, no new pull needed.
- **ClipForge** (MIT) — Chrome video clipping studio; alternative
  to cliqwise for the pages.
- Remaining ~80 forks (openclaw, firecrawl, E2B, chroma, nocodb,
  ToolJet, open-webui, awesome-mcp-servers, etc.) are a curation
  signal only — the author found them worth forking; no action.

## Xod and internet-of-things (the two the owner asked about first)

- **xod** — parts pulled in (`tools/xod-parts/`); the app itself is
  NOT adopted (duplicates Muse; Mac-first). WATCH for its fix-round
  releases — its changelog grading culture is the pattern our Proving
  Ground harness borrows.
- **internet-of-things** — no code, no license, 3 markdown files.
  Nothing to pull, ever; its scoreboard claims are not publicly
  verifiable. WATCH only as a catalog pointer to the per-tool repos.
