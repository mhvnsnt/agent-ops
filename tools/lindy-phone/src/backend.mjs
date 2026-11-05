// Agent backends: where a routed text actually goes to be answered.
// A backend receives { agent, conversationId, text, from } and returns
// { reply } (reply may be null/empty = stay silent).
//
// - "stub": deterministic local backend for dev/tests. Proves routing
//   end-to-end with no live agent attached.
// - "http": POSTs the message as JSON to the agent's bridge URL and reads
//   { reply } back. This is the seam where each Muse / lane bridge
//   plugs in (the bridge drops the text into that agent's chat and returns
//   its answer). {agentId} in the URL is expanded per agent.

export function createBackend(agent, fetchImpl = fetch) {
  const cfg = agent.backend || { type: "stub" };

  if (cfg.type === "http") {
    const url = (cfg.url || "").replace("{agentId}", encodeURIComponent(agent.id));
    if (!url) throw new Error(`Agent "${agent.id}" has backend.type http but no url.`);
    return {
      type: "http",
      async handle({ conversationId, text, from }) {
        const res = await fetchImpl(url, {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            agentId: agent.id,
            conversationId,
            from,
            text,
          }),
        });
        if (!res.ok) throw new Error(`Backend for "${agent.id}" returned HTTP ${res.status}`);
        const data = await res.json();
        return { reply: typeof data.reply === "string" ? data.reply : null };
      },
    };
  }

  // stub
  return {
    type: "stub",
    async handle({ text }) {
      return { reply: `[${agent.contactName} · mock] Got it: "${text}"` };
    },
  };
}
