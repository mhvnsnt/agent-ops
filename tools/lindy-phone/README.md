# lindy-phone — text your agents like people

A Lindy-style phone texting layer for Real's agents, owned outright instead
of rented from a SaaS: every agent gets **its own phone number**, so on the
owner's phone each agent is its own contact with its own thread — text
Ashes, text the Western Heart lane, get texted back by Ops when something
needs him.

Lindy's current product (researched 2026-11-04) is one personal assistant
with one optional voice number. This is the thing Lindy doesn't sell:
a roster of agent contacts that already know his repos, his memory, and
his projects — no per-seat subscription, no credit pool.

## How it works (60 seconds)

```
Owner's phone ──SMS──► provider (Telnyx) ──webhook──► THIS GATEWAY
                                                          │ allowlist: owner only
                                                          │ route by number texted
                                                          ▼
                                              that agent's chat backend
                                                          │ reply
Owner's phone ◄──SMS── agent's own number ◄───────────────┘
```

- **Transport is wired, not hand-built:** all provider I/O goes through
  [`@opencoredev/sms-sdk`](https://github.com/opencoredev/sms-sdk) (MIT) —
  one typed send API + signature-verified, normalized webhooks for
  Twilio/Telnyx/Plivo/Vonage/Bandwidth/Sinch. The gateway's own code is
  only the three pieces no library can know: the agent registry, the
  owner allowlist, and the chat-backend call. (Full evaluation of the
  alternatives — AgentLine, Twilio Agent Connect, Hail, Chatwoot, the
  SMPP-era gateways — is in ARCHITECTURE.md.)
- **Allowlist security:** exactly one inbound number is ever answered —
  the owner's (from the `OWNER_NUMBER` env var, never committed). Every
  other sender is logged (masked) and silently dropped.
- **Agent-initiated texts:** any agent can text the owner first
  (deliveries, blockers, proof links) via `POST /send` from its own
  number, gated by a shared token.
- **Threading:** one conversation per agent, appended to a JSONL log, so
  a text always lands in that agent's context. Provider webhook retries
  are deduplicated.

## Run it locally (no account, no number, no cost)

```bash
cd tools/lindy-phone
npm install
OWNER_NUMBER=+15550009999 SMS_PROVIDER=mock npm start   # terminal 1
npm run smoke                                           # terminal 2
npm test
```

Mock mode uses sms-sdk's `memory()` adapter: sends are recorded, nothing
touches a network. The smoke test boots the server, simulates an inbound
owner text to Ashes' number, and verifies the reply.

## Docs

- [ARCHITECTURE.md](ARCHITECTURE.md) — design, routing, security, phases
- [AGENT-CONTACTS.md](AGENT-CONTACTS.md) — the contact registry (who gets
  a number, what to save each contact as)
- [SETUP-LIVE.md](SETUP-LIVE.md) — the exact remaining steps to go live,
  with the real costs and the one decision the owner still has to make

## Config

Everything sensitive comes from the environment — see `.env.example`.
The owner's real number and all provider keys live in env/secrets only;
committed files contain placeholders and reserved fictional test numbers
(+15550001xxx) only.
