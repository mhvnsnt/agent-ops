// Conversation store: one thread per agent (the owner only ever talks to
// one agent per number, so thread = agentId). Messages are appended to a
// JSONL file so a text always lands in that agent's durable context, and
// provider webhook retries are deduplicated by event key.

import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname } from "node:path";

export class ConversationStore {
  constructor(file) {
    this.file = file;
    this.seen = new Set();
    if (file) {
      mkdirSync(dirname(file), { recursive: true });
      if (existsSync(file)) {
        for (const line of readFileSync(file, "utf8").split("\n")) {
          if (!line.trim()) continue;
          try {
            const rec = JSON.parse(line);
            if (rec.dedupeKey) this.seen.add(rec.dedupeKey);
          } catch {
            /* tolerate a torn last line */
          }
        }
      }
    }
  }

  /** Returns false when this event was already processed (provider retry). */
  claimEvent(dedupeKey) {
    if (!dedupeKey) return true;
    if (this.seen.has(dedupeKey)) return false;
    this.seen.add(dedupeKey);
    return true;
  }

  append(record) {
    const rec = { ts: new Date().toISOString(), ...record };
    if (this.file) appendFileSync(this.file, JSON.stringify(rec) + "\n");
    return rec;
  }
}
