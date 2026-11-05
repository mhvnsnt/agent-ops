// End-to-end tests against the MOCK provider (sms-sdk memory() adapter).
// No live number, no network: a simulated inbound text must be routed to
// the right agent and answered from that agent's number; a stranger's text
// must be dropped; an agent-initiated text must go out from its own number.
// Test numbers are reserved fictional numbers (+15550001xxx agent lines,
// +15550009999 = the "owner" for tests). The real owner number is never
// used in tests and never committed.

import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createGateway } from "../src/index.mjs";

const OWNER = "+15550009999";
const STRANGER = "+15550007777";
const ASHES = "+15550001001";
const WESTERN_HEART = "+15550001002";

let gw;
let base;

before(async () => {
  const dir = mkdtempSync(join(tmpdir(), "lindy-phone-test-"));
  gw = createGateway({
    OWNER_NUMBER: OWNER,
    SMS_PROVIDER: "mock",
    AGENTS_CONFIG: "config/agents.example.json",
    GATEWAY_TOKEN: "test-token",
    CONVERSATIONS_FILE: join(dir, "conversations.jsonl"),
  });
  await new Promise((resolve) => gw.server.listen(0, resolve));
  base = `http://127.0.0.1:${gw.server.address().port}`;
});

after(() => gw.server.close());

function inbound(from, to, body, id) {
  return fetch(`${base}/webhooks/sms/mock`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ from, to, body, id }),
  });
}

function sentMessages() {
  // sms-sdk records `from` as an SmsFrom object ({kind, value}); unwrap it.
  const num = (v) => (typeof v === "string" ? v : v && v.value);
  return gw.transport.adapter.sent.map((s) => ({
    from: num(s.message.from),
    to: num(s.message.to),
    body: s.message.body,
  }));
}

test("owner text to Ashes' number is answered by Ashes", async () => {
  gw.transport.adapter.reset();
  const res = await inbound(OWNER, ASHES, "what is the disk at?", "evt-1");
  assert.equal(res.status, 200);
  const sent = sentMessages();
  assert.equal(sent.length, 1);
  assert.equal(sent[0].from, ASHES);
  assert.equal(sent[0].to, OWNER);
  assert.match(sent[0].body, /Ashes/);
  assert.match(sent[0].body, /disk/);
});

test("owner text to Western Heart's number is answered by Western Heart, not Ashes", async () => {
  gw.transport.adapter.reset();
  const res = await inbound(OWNER, WESTERN_HEART, "roster status?", "evt-2");
  assert.equal(res.status, 200);
  const sent = sentMessages();
  assert.equal(sent.length, 1);
  assert.equal(sent[0].from, WESTERN_HEART);
  assert.match(sent[0].body, /Western Heart/);
});

test("a stranger's text is dropped and never answered", async () => {
  gw.transport.adapter.reset();
  const res = await inbound(STRANGER, ASHES, "hello?", "evt-3");
  assert.equal(res.status, 200); // acked so the provider doesn't retry
  assert.equal(sentMessages().length, 0);
});

test("a duplicate webhook delivery is answered only once", async () => {
  gw.transport.adapter.reset();
  await inbound(OWNER, ASHES, "ping", "evt-dup");
  await inbound(OWNER, ASHES, "ping", "evt-dup");
  assert.equal(sentMessages().length, 1);
});

test("agent-initiated text goes out from that agent's own number", async () => {
  gw.transport.adapter.reset();
  const res = await fetch(`${base}/send`, {
    method: "POST",
    headers: { "content-type": "application/json", "x-gateway-token": "test-token" },
    body: JSON.stringify({ agentId: "ops", body: "Disk at 71%. All lanes healthy." }),
  });
  assert.equal(res.status, 200);
  const sent = sentMessages();
  assert.equal(sent.length, 1);
  assert.equal(sent[0].from, "+15550001008");
  assert.equal(sent[0].to, OWNER);
  assert.match(sent[0].body, /Disk at 71%/);
});

test("/send rejects a bad gateway token", async () => {
  const res = await fetch(`${base}/send`, {
    method: "POST",
    headers: { "content-type": "application/json", "x-gateway-token": "wrong" },
    body: JSON.stringify({ agentId: "ops", body: "should not send" }),
  });
  assert.equal(res.status, 401);
});

test("health endpoint reports the mock provider and agent roster", async () => {
  const res = await fetch(`${base}/health`);
  const data = await res.json();
  assert.equal(data.ok, true);
  assert.equal(data.provider, "mock");
  assert.ok(data.agents.includes("ashes"));
  assert.ok(data.agents.includes("ops"));
});
