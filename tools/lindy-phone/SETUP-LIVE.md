# Going live — exact remaining steps, real costs, and the one owner decision

Everything in this repo runs today on the mock provider for $0. Going
live needs a provider account, carrier registration, and numbers. No
card has been put on anything and no account has been created — this doc
is the decision, costed from provider pages fetched 2026-11-04 (sources
inline).

## The decision (owner picks one)

**Recommended — Route A: 8 local numbers on Telnyx under one 10DLC campaign.**
Each agent is a real local number and its own contact. ≈ **$23.80/mo**
at ~2,000 message segments/month, **$19.50 one-time**, live in
**1–3 weeks** (carrier vetting, not our build, is the wait).

**Fast start (optional, can run in parallel) — one toll-free number for Ashes.**
One verified toll-free = one working texting agent in ~3–5 business
days, ≈ **$18/mo** — but it's a single contact for all agents until
Route A lands, so it's a bridge, not the goal.

**Not recommended — 8 toll-free numbers.** Toll-free verification expects
one sending number per business per use case; 8 numbers doing the same
conversational job for the same person reads as "snowshoeing" (prohibited)
and risks rejection of the whole set.

**Not possible — Sole Proprietor 10DLC.** No-EIN registration exists but
is capped at **1 number, 1 campaign**. It cannot do a roster. Full stop.

### Route A cost breakdown (Telnyx, 8 numbers, ~2,000 segments/mo)

| Item | Cost | Source |
|---|---|---|
| 8 local numbers | 8 × $1.00 = **$8.00/mo** | telnyx.com graduated number pricing (support.telnyx.com/en/articles/2026102601) |
| Low-Volume Mixed campaign | **$1.50/mo** (billed 3 months up front) | support.telnyx.com/en/articles/5634625-10dlc-fees-and-charges |
| Messages (~1,000 out + ~1,000 in) | 2,000 × $0.004 + carrier fees ≈ **$14.30/mo** | telnyx.com/pricing/messaging |
| **Total** | **≈ $23.80/mo** | (long replies/emoji = more segments; double the message line at 2 segments avg) |
| One-time: brand registration | $4.50 | same Telnyx fees page (TCR schedule, Aug 2025) |
| One-time: campaign vetting | $15.00 | same |
| **One-time total** | **$19.50** | |

Same shape on Twilio ≈ $33.60/mo + same $19.50 one-time (numbers
$1.15/mo, SMS $0.0083/segment — twilio.com/en-us/sms/pricing/us).
For comparison, Lindy charges $29.99/mo+ for ONE assistant, and calls
burn credits at ~$0.25/min.

## Two prerequisites (known, being handled)

1. **EIN — required for Route A.** The brand registration needs the
   business's EIN (Orion Enterprises LLC). Sole-proprietor registration
   is not a workaround (1-number cap, above). If the EIN isn't in hand
   yet, start the toll-free bridge (sole proprietors are exempt from the
   business-number requirement there) and file Route A the day it lands.
2. **A live website with a privacy policy** stating the messaging use
   case and that mobile opt-in data is never shared. This is the most
   common campaign-rejection cause for small projects. We can put this
   page up on his existing web infra for free before filing — the opt-in
   story is stated plainly: *the sole recipient is the business owner
   himself, who provisioned the system for his own agents to reach him.*

Unregistered local-number traffic is **hard-blocked** by US carriers
since Feb 2025 (Twilio error 30034) — there is no "just try it" path;
registration first is the only order that works.

## Live steps (after the owner says go)

1. Create the Telnyx account (sign-up is free; the account is funded
   pay-as-you-go when numbers are purchased — funding method is the
   owner's call at that moment, nothing is charged by this doc).
2. Put up the privacy-policy page (free, our side).
3. File the **Low-Volume Standard brand** (Orion Enterprises LLC, EIN,
   address, website). Typical approval 1–3 business days.
4. File the **Low-Volume Mixed campaign**: use case "personal AI agent
   communications to the business owner", sample messages = real
   examples from this system. Vetting: plan 1–3 weeks.
5. Buy the 8 local numbers (owner's area-code pick) and attach them to
   the campaign's messaging profile.
6. Host the gateway at a public HTTPS address (his existing infra),
   set env from secrets: `OWNER_NUMBER` (his number, private),
   `SMS_PROVIDER=telnyx`, Telnyx key + public key, the 8 `NUMBER_*`
   values, `GATEWAY_TOKEN`.
7. Point each number's inbound webhook at
   `https://<gateway>/webhooks/sms/telnyx`.
8. First-text round: each agent texts him once ("Save me as Western
   Heart") so he saves the 8 contacts from real threads — or Muse
   creates the contacts directly on his paired Android via its
   `contacts.create` command once the numbers exist. Verify a reply
   round-trip on each. **Done = he can text Ashes and get Ashes back.**

## What stays true after go-live

- Only his number can talk to any agent (allowlist is in the gateway,
  not the provider).
- Replies and alerts always come from the agent's own number.
- Cost scales with messages, not agents' "seats": adding a 9th agent
  later is +$1/mo for its number.
