// Router: the whole request lifecycle in one place.
//   inbound event -> dedupe -> ALLOWLIST (owner only) -> agent by the
//   number that was texted -> store -> agent backend -> reply from that
//   same agent number.
// Agent-initiated texts (deliveries, blockers, proof links) go out through
// sendFromAgent(): an agent texts the owner from its own number/contact.

import { isOwner } from "./allowlist.mjs";
import { createBackend } from "./backend.mjs";
import { maskNumber } from "./config.mjs";

export function createRouter({ config, transport, store, log = console }) {
  const backends = new Map();
  for (const agent of config.agents.values()) backends.set(agent.id, createBackend(agent));

  async function handleInbound(event) {
    if (!event || event.type !== "message.received") {
      return { status: "ignored", reason: "not-a-message" };
    }
    if (!store.claimEvent(event.dedupeKey)) {
      return { status: "ignored", reason: "duplicate" };
    }
    if (!isOwner(event.from, config.ownerNumber)) {
      // Logged (masked) and dropped. Never answered, never stored as a
      // conversation, no hint to the sender that the number is live.
      log.warn(`[gateway] dropped inbound from non-owner ${maskNumber(event.from)} to ${maskNumber(event.to)}`);
      store.append({ kind: "dropped-non-owner", from: maskNumber(event.from), to: maskNumber(event.to) });
      return { status: "dropped", reason: "not-owner" };
    }
    const agent = config.byNumber.get(event.to);
    if (!agent) {
      log.warn(`[gateway] owner texted unknown number ${maskNumber(event.to)}`);
      store.append({ kind: "unknown-number", to: maskNumber(event.to) });
      return { status: "ignored", reason: "unknown-number" };
    }
    const conversationId = `sms:${agent.id}`;
    store.append({
      kind: "inbound",
      agentId: agent.id,
      conversationId,
      from: event.from,
      to: event.to,
      body: event.body,
      dedupeKey: event.dedupeKey,
    });
    const { reply } = await backends.get(agent.id).handle({
      conversationId,
      text: event.body,
      from: event.from,
    });
    if (reply) {
      await transport.send({
        from: agent.number,
        to: config.ownerNumber,
        body: reply,
        idempotencyKey: `reply:${event.dedupeKey || conversationId + ":" + Date.now()}`,
      });
      store.append({ kind: "outbound-reply", agentId: agent.id, conversationId, body: reply });
    }
    return { status: "replied", agentId: agent.id, replied: Boolean(reply) };
  }

  async function sendFromAgent(agentId, body) {
    const agent = config.agents.get(agentId);
    if (!agent) throw new Error(`Unknown agent "${agentId}"`);
    const result = await transport.send({
      from: agent.number,
      to: config.ownerNumber,
      body,
      idempotencyKey: `agent:${agentId}:${Date.now()}`,
    });
    store.append({ kind: "outbound-agent", agentId, body });
    return result;
  }

  return { handleInbound, sendFromAgent };
}
