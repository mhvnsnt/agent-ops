# Architecture — lindy-phone gateway

Owner order (2026-11-04): "set up a way where we can talk like Lindy…
you can text my phone and we can interact through my phone number… set up
all my agents where they can text me… as different contacts." Better than
Lindy, built from what's already in his repos.

## What Lindy actually does (researched 2026-11-04, sourced in the lane report)

- Current Lindy (relaunched Feb 2026) is **one** personal AI executive
  assistant. Texting = iMessage/SMS to that single assistant after you
  verify *your* number; voice = **one** Lindy number you can buy.
  Per-agent numbers were the old Gaia product; no current Lindy doc
  offers a roster of agent contacts.
- Pricing shape: Plus $29.99 / Pro $99.99 / Max $199.99 per user/month in
  credits ($0.01/credit), calls from 25 credits/min (~$0.25/min), number
  fee unpublished.
- **"Better than Lindy" here means:** (1) every agent is its own contact
  (Lindy = 1), (2) the agents behind the numbers are *his* agents — with
  his memory, repos, checkpoints and live project state, not a fresh
  SaaS assistant, (3) no subscription and no credit pool — the only cost
  is raw SMS carriage (~$24/mo at his scale, see SETUP-LIVE.md),
  (4) the whole stack is his code in his repo.

## Components

| Piece | What | Source |
|---|---|---|
| Transport (send + verified webhooks) | `@opencoredev/sms-sdk` v0.1.1, MIT, zero runtime deps | wired in, pinned in package.json |
| Webhook server + router | `src/server.mjs`, `src/router.mjs` (node:http, no framework) | this repo |
| Allowlist | `src/allowlist.mjs` — owner number only | this repo |
| Agent registry | `config/agents.json` (from `agents.example.json`) — number → agent → backend | this repo |
| Conversation store | `src/store.mjs` — JSONL per-agent threads + webhook dedupe | this repo |
| Agent backends | `src/backend.mjs` — `stub` (local) or `http` bridge per agent | this repo |

### Why sms-sdk (evaluation summary, 2026-11-04 lane)

Candidates evaluated from fetched sources: AgentLine (MIT, full Python
server, per-agent numbers/webhooks/MCP, but outbound SMS is not
documented in its API — inbound-only on paper), Twilio Agent Connect
(MIT, official, native multi-sender, but Twilio-only and needs Twilio
Conversations/Memory, no documented mock), Hail (AGPL-3.0, heavy voice
stack, its own repo contradicts itself on whether SMS is implemented),
Chatwoot (MIT core, a human support desk — AI agent is paid/Enterprise),
LangBot (Apache-2.0 router, no SMS channel), Jasmin/playSMS/Gammu/
Kannel/RapidSMS (SMPP, modem, bulk-portal or dormant — wrong model for
cloud numbers), and the 2023 TextGPT demos (stale, license-unverified).

sms-sdk won because it is the only candidate with a **documented
first-class mock** (`memory()` adapter + signed webhook builders for
tests that never touch the network), verified normalized webhooks for
both finalist providers (Twilio HMAC-SHA1, Telnyx Ed25519), MIT, and a
provider-agnostic send API — so the provider decision can change without
touching routing. Disclosed risk: the project is young (created Sep
2026, small community). Mitigation: version pinned, and the gateway only
touches it through `src/transport.mjs`, so swapping to a provider's own
SDK later is a one-file change.

**No candidate ships a sender allowlist.** That check is ours, by
design: first thing in the router, before any storage or backend call.

## Request lifecycle (inbound)

1. Provider POSTs the signed webhook to `/webhooks/sms/<provider>`.
2. sms-sdk verifies the signature and normalizes the payload to
   `{ type: "message.received", from, to, body, dedupeKey }`.
   Bad signature → 403, nothing is read.
3. Router claims the `dedupeKey` (provider retries answer once).
4. **Allowlist:** `from !== OWNER_NUMBER` → log masked, drop, 200 ack
   (so the provider doesn't retry; the sender learns nothing).
5. Agent = registry lookup by `to` number. Unknown number → log, drop.
6. Message appended to that agent's thread (`data/conversations.jsonl`).
7. Agent backend answers (stub locally; the agent's HTTP bridge live).
8. Reply sent **from that agent's number** via sms-sdk; appended to the
   thread.

## Agent-initiated texts (outbound-first)

Deliveries, blockers, and proof links are half the point (it's how lanes
already report — this just puts them in his pocket):

```
POST /send   header: x-gateway-token: $GATEWAY_TOKEN
{ "agentId": "ops", "body": "Disk at 71%. Guardian pass clean." }
```

…goes out from Ops' number to the owner, and is recorded in Ops' thread,
so his reply lands back in the same conversation.

## What already existed in his stack (inventory, 2026-11-04)

- **No SMS code anywhere.** GitHub code search across agent-ops,
  western-heart, and cape-jones found zero twilio/sms/webhook/telnyx
  code (cape-jones conclusive; the two big repos' search indexing is
  incomplete, but nothing in their layouts suggests a messaging service
  exists). This layer is greenfield; the reusable assets are the ones
  below, not code.
- **Composio** (his local skill, `local-composio-tools`): its *current*
  hosted catalog includes full **Twilio** and **Telnyx** toolkits —
  including send-message, number purchase, and (Twilio) webhook triggers
  — usable as an auxiliary send path for individual agents once his own
  provider account exists. Two honest caveats: his locally pinned
  install is stale and its venv is currently missing on disk, and
  routing everything through Composio would put a third party in the
  middle of the allowlist. So: the gateway talks to the provider
  directly via sms-sdk; Composio stays available for agent-side tooling.
- **His paired Android phone** already streams his incoming SMS into
  Muse and supports `contacts.create` — at go-live, the 8 agent
  contacts can be created on his phone by Muse directly once the
  numbers exist (SETUP-LIVE.md step 8). Muse's own chat transports
  today are WhatsApp-only; a native Muse "SMS provider" is
  platform-side and not buildable from his repos, which is why this
  gateway is an external bridge that mirrors that model (one durable
  thread per agent, replies bound to their thread).

## The chat-backend bridge (the remaining integration seam)

Each agent entry can point at an `http` backend:
`POST { agentId, conversationId, from, text }` → `{ reply }`.
The bridge on the other side is per-agent glue that drops the text into
that agent's existing chat (the same side-chat / lane infrastructure the
agents already run on) and returns its answer. Until a given agent's
bridge exists, its backend stays `stub`, and the registry marks it —
the number, routing, and allowlist already work; only the brain hookup
is per-agent follow-up. This is deliberate: transport and identity are
solved once, centrally, instead of per lane.

## Security model

- One allowlisted sender (the owner). No commands, keywords, or opt-in
  flows exist for anyone else; there is no public surface to attack
  beyond "text a number and be ignored."
- The owner's number and provider keys exist only in env/secrets.
  Committed config uses env-var indirection (`numberEnv`) and fictional
  test numbers. Logs mask numbers (`+12***02`).
- Webhook signatures verified by sms-sdk before parsing (Twilio path
  proven in this lane with a signed test request + a forged-signature
  rejection).
- `/send` requires the gateway token; it exists so only his own agent
  infrastructure can originate texts.
- Inbound media (MMS) is parsed by sms-sdk but not yet forwarded to
  backends — phase 2.

## Phases

1. **This scaffold** — gateway, registry, allowlist, mock end-to-end,
   tests + smoke green, docs. No accounts, no numbers, no cost.
2. **Go live (owner decision, SETUP-LIVE.md)** — provider account, brand
   + campaign (10DLC) or toll-free verification, buy numbers, point
   webhooks, set env. ~$24/mo at 8 numbers / ~2,000 msgs on the
   recommended route.
3. **Bridges** — wire each agent's chat backend one by one (Ashes
   first), so texts reach the real agents.
4. **Voice (later)** — the same numbers can take calls (Lindy's other
   trick); provider voice webhooks + a speech stack get evaluated then.
   Not in v1.
5. **In all his repos** — the gateway lives in agent-ops (the ops home);
   other repos consume it through the `/send` API + their bridge, which
   is the "set up in all my repos" shape: one gateway, every repo's
   agents reachable, no per-repo telephony code.
