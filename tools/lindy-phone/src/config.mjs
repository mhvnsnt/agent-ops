// Config loading for the lindy-phone gateway.
// All secrets and the owner's number come from the environment only.
// The owner's number is never logged in full (see maskNumber).

import { readFileSync } from "node:fs";

const E164_RE = /^\+[1-9]\d{6,14}$/;

export function maskNumber(n) {
  if (!n || typeof n !== "string") return "(unset)";
  return n.length <= 6 ? "***" : `${n.slice(0, 3)}***${n.slice(-2)}`;
}

function requireE164(value, name) {
  if (!value || !E164_RE.test(value)) {
    throw new Error(
      `${name} must be set to an E.164 number (e.g. +12225550123). ` +
        `It is read from the environment only and is never committed.`,
    );
  }
  return value;
}

/**
 * Load config from env + the agent registry JSON.
 * env vars:
 *   OWNER_NUMBER   (required, E.164) — the only allowlisted sender.
 *   SMS_PROVIDER   mock | telnyx | twilio   (default mock)
 *   AGENTS_CONFIG  path to agents.json (registry; per-agent numberEnv wins
 *                  over the registry's placeholder `number` when the env
 *                  var is set — production numbers never live in the file).
 *   GATEWAY_TOKEN  shared secret for POST /send (required outside mock).
 *   PUBLIC_BASE_URL  public URL of this server (webhook signature checks).
 */
export function loadConfig(env = process.env, readFile = readFileSync) {
  const ownerNumber = requireE164(env.OWNER_NUMBER, "OWNER_NUMBER");
  const provider = (env.SMS_PROVIDER || "mock").toLowerCase();
  if (!["mock", "telnyx", "twilio"].includes(provider)) {
    throw new Error(`SMS_PROVIDER must be mock | telnyx | twilio, got "${provider}"`);
  }

  const registryPath = env.AGENTS_CONFIG || "config/agents.example.json";
  const registry = JSON.parse(readFile(registryPath, "utf8"));
  const agents = new Map();
  const byNumber = new Map();
  for (const a of registry.agents || []) {
    const fromEnv = a.numberEnv ? env[a.numberEnv] : undefined;
    const number = fromEnv || a.number;
    if (!number || !E164_RE.test(number)) {
      throw new Error(`Agent "${a.id}" has no valid number (env ${a.numberEnv || "-"} / registry).`);
    }
    if (byNumber.has(number)) {
      throw new Error(`Duplicate agent number ${maskNumber(number)} for agents "${byNumber.get(number)}" and "${a.id}".`);
    }
    const agent = {
      id: a.id,
      contactName: a.contactName || a.id,
      role: a.role || "",
      number,
      backend: a.backend || { type: "stub" },
    };
    agents.set(agent.id, agent);
    byNumber.set(number, agent);
  }
  if (agents.size === 0) throw new Error("Agent registry is empty.");

  return {
    ownerNumber,
    provider,
    port: Number(env.PORT || 8787),
    gatewayToken: env.GATEWAY_TOKEN || "",
    publicBaseUrl: (env.PUBLIC_BASE_URL || "").replace(/\/$/, ""),
    credentials: {
      telnyxApiKey: env.TELNYX_API_KEY || "",
      telnyxPublicKey: env.TELNYX_PUBLIC_KEY || "",
      telnyxMessagingProfileId: env.TELNYX_MESSAGING_PROFILE_ID || "",
      twilioAccountSid: env.TWILIO_ACCOUNT_SID || "",
      twilioAuthToken: env.TWILIO_AUTH_TOKEN || "",
    },
    agents,
    byNumber,
  };
}
