// Transport: ALL provider I/O goes through @opencoredev/sms-sdk (MIT) —
// one typed send API + verified, normalized webhooks for Twilio / Telnyx /
// Plivo / Vonage / Bandwidth / Sinch. No hand-rolled provider HTTP here.
//
// - mock   -> sms-sdk's documented memory() adapter: records every send,
//             calls nothing, needs no account. Same code path as live.
// - telnyx -> sms-sdk telnyx() adapter (recommended live route, SETUP-LIVE.md)
// - twilio -> sms-sdk twilio() adapter

import { createSmsClient } from "@opencoredev/sms-sdk";
import { memory } from "@opencoredev/sms-sdk/testing";
import { telnyx } from "@opencoredev/sms-sdk/telnyx";
import { twilio } from "@opencoredev/sms-sdk/twilio";
import { parseSmsWebhook } from "@opencoredev/sms-sdk/webhooks";

export function createTransport(config) {
  let adapter;
  if (config.provider === "mock") {
    adapter = memory({ name: "memory" });
  } else if (config.provider === "telnyx") {
    adapter = telnyx({
      apiKey: config.credentials.telnyxApiKey,
      ...(config.credentials.telnyxMessagingProfileId
        ? { messagingProfileId: config.credentials.telnyxMessagingProfileId }
        : {}),
    });
  } else if (config.provider === "twilio") {
    adapter = twilio({
      accountSid: config.credentials.twilioAccountSid,
      authToken: config.credentials.twilioAuthToken,
    });
  }
  const client = createSmsClient({ adapters: [adapter] });
  return {
    client,
    adapter, // exposed so tests/smoke can inspect memory().sent
    async send({ from, to, body, idempotencyKey }) {
      return client.send({ from, to, body, ...(idempotencyKey ? { idempotencyKey } : {}) });
    },
  };
}

/**
 * Verify + normalize an inbound provider webhook into an SmsEvent
 * ({ type: "message.received", from, to, body, dedupeKey, ... }).
 * Throws WebhookSignatureError on a forged/badly-signed request.
 * Only used for live providers; the mock path builds the same event shape
 * locally (see server.mjs).
 */
export async function parseInbound(config, provider, request, url) {
  const common = { provider, request, ...(url ? { url } : {}) };
  if (provider === "twilio") {
    return parseSmsWebhook({ ...common, credentials: { authToken: config.credentials.twilioAuthToken } });
  }
  if (provider === "telnyx") {
    return parseSmsWebhook({ ...common, credentials: { publicKey: config.credentials.telnyxPublicKey } });
  }
  throw new Error(`No webhook parser wired for provider "${provider}"`);
}
