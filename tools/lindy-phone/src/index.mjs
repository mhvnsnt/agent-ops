// Boot: load config, wire transport + store + router, listen.
// Run locally with zero accounts:  SMS_PROVIDER=mock OWNER_NUMBER=+1... npm start

import { loadConfig, maskNumber } from "./config.mjs";
import { createTransport } from "./transport.mjs";
import { ConversationStore } from "./store.mjs";
import { createRouter } from "./router.mjs";
import { createGatewayServer } from "./server.mjs";

export function createGateway(env = process.env) {
  const config = loadConfig(env);
  const transport = createTransport(config);
  const store = new ConversationStore(env.CONVERSATIONS_FILE || "data/conversations.jsonl");
  const router = createRouter({ config, transport, store });
  const server = createGatewayServer({ config, transport, router });
  return { config, transport, store, router, server };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { config, server } = createGateway();
  server.listen(config.port, () => {
    console.log(
      `[gateway] lindy-phone up on :${config.port} provider=${config.provider} ` +
        `owner=${maskNumber(config.ownerNumber)} agents=${[...config.agents.keys()].join(",")}`,
    );
  });
}
