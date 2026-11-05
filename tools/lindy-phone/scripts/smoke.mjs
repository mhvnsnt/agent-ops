// Local smoke test: boot the gateway on the mock provider, simulate an
// inbound owner text, verify the reply is recorded by the memory adapter.
// Run: npm run smoke   (no account, no network, no live number)

import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createGateway } from "../src/index.mjs";

const OWNER = "+15550009999"; // fictional test number
const ASHES = "+15550001001";

const dir = mkdtempSync(join(tmpdir(), "lindy-phone-smoke-"));
const gw = createGateway({
  OWNER_NUMBER: OWNER,
  SMS_PROVIDER: "mock",
  AGENTS_CONFIG: "config/agents.example.json",
  GATEWAY_TOKEN: "smoke-token",
  CONVERSATIONS_FILE: join(dir, "conversations.jsonl"),
});
await new Promise((resolve) => gw.server.listen(0, resolve));
const base = `http://127.0.0.1:${gw.server.address().port}`;

const res = await fetch(`${base}/webhooks/sms/mock`, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ from: OWNER, to: ASHES, body: "smoke: are you there?", id: "smoke-1" }),
});
if (res.status !== 200) throw new Error(`webhook returned ${res.status}`);
const sent = gw.transport.adapter.sent;
if (sent.length !== 1) throw new Error(`expected 1 recorded send, got ${sent.length}`);
const msg = sent[0].message;
const num = (v) => (typeof v === "string" ? v : v && v.value); // sms-sdk SmsFrom object
if (num(msg.from) !== ASHES || num(msg.to) !== OWNER || !/Ashes/.test(msg.body)) {
  throw new Error(`unexpected reply: ${JSON.stringify(msg)}`);
}
console.log(`SMOKE PASS — inbound text routed to Ashes; reply recorded from ${num(msg.from)}: "${msg.body}"`);
gw.server.close();
