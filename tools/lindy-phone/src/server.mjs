// HTTP server (node:http, no framework dependency):
//   GET  /health                  -> { ok, provider, agents }
//   POST /webhooks/sms/mock       -> local/dev inbound: JSON {from,to,body}
//                                    (only enabled when SMS_PROVIDER=mock)
//   POST /webhooks/sms/twilio     -> live Twilio webhook (signature-verified
//   POST /webhooks/sms/telnyx        by sms-sdk before anything is read)
//   POST /send                    -> agent-initiated text:
//                                    { agentId, body } + header
//                                    x-gateway-token: $GATEWAY_TOKEN
//                                    (in mock mode the token may be omitted
//                                    only when GATEWAY_TOKEN is unset)

import { createServer } from "node:http";
import { randomUUID } from "node:crypto";
import { parseInbound } from "./transport.mjs";

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks)));
    req.on("error", reject);
  });
}

function json(res, status, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(status, { "content-type": "application/json" });
  res.end(body);
}

export function createGatewayServer({ config, transport, router }) {
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, "http://localhost");

      if (req.method === "GET" && url.pathname === "/health") {
        return json(res, 200, {
          ok: true,
          provider: config.provider,
          agents: [...config.agents.keys()],
        });
      }

      if (req.method === "POST" && url.pathname === "/send") {
        const token = req.headers["x-gateway-token"];
        if (config.gatewayToken && token !== config.gatewayToken) {
          return json(res, 401, { error: "bad gateway token" });
        }
        const payload = JSON.parse((await readBody(req)).toString("utf8") || "{}");
        if (!payload.agentId || !payload.body) {
          return json(res, 400, { error: "agentId and body are required" });
        }
        await router.sendFromAgent(payload.agentId, payload.body);
        return json(res, 200, { ok: true });
      }

      const wh = url.pathname.match(/^\/webhooks\/sms\/(mock|twilio|telnyx)$/);
      if (req.method === "POST" && wh) {
        const provider = wh[1];
        let event;
        if (provider === "mock") {
          if (config.provider !== "mock") return json(res, 404, { error: "mock webhook disabled" });
          const payload = JSON.parse((await readBody(req)).toString("utf8") || "{}");
          if (!payload.from || !payload.to || typeof payload.body !== "string") {
            return json(res, 400, { error: "from, to, body are required" });
          }
          event = {
            type: "message.received",
            provider: "mock",
            providerId: payload.id || randomUUID(),
            dedupeKey: payload.id || randomUUID(),
            from: payload.from,
            to: payload.to,
            body: payload.body,
            mediaUrls: [],
          };
        } else {
          if (config.provider !== provider) {
            return json(res, 404, { error: `${provider} webhook disabled (SMS_PROVIDER=${config.provider})` });
          }
          const raw = await readBody(req);
          const fetchReq = new Request(
            `${config.publicBaseUrl || `http://localhost:${config.port}`}${url.pathname}`,
            {
              method: "POST",
              headers: req.headers,
              body: raw,
            },
          );
          const publicUrl = config.publicBaseUrl ? `${config.publicBaseUrl}${url.pathname}` : undefined;
          event = await parseInbound(config, provider, fetchReq, publicUrl);
        }
        const result = await router.handleInbound(event);
        // Providers only need a 2xx ack; routing detail stays server-side.
        return json(res, 200, { ok: true, routed: result.status });
      }

      return json(res, 404, { error: "not found" });
    } catch (err) {
      const name = err && err.name ? err.name : "Error";
      if (name === "WebhookSignatureError") return json(res, 403, { error: "bad signature" });
      console.error("[gateway] request failed:", err);
      return json(res, 500, { error: "internal" });
    }
  });
  return server;
}
