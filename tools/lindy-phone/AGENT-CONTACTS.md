# Agent contact registry (draft v1, 2026-11-04)

One agent = one number = one contact on the owner's phone, saved under
the contact name below. Texting that contact talks to that agent; that
agent's texts (including agent-initiated ones) come from that number.

| # | Save contact as | Agent / lane | Number home | Why it gets its own contact |
|---|---|---|---|---|
| 1 | **Ashes** | Main agent (Muse) | dedicated | The default contact — cross-project talk, decisions, anything that isn't one lane's business. |
| 2 | **Western Heart** | Western Heart game lane | dedicated | Roster, banks, builds, republish — his highest-volume project. |
| 3 | **Cape Jones** | Cape Jones series lane | dedicated | Scenes, dance, renders, episode work. |
| 4 | **Mochiichao** | Mochiichao / Crystal lane | dedicated | Crystal + M1 game work. |
| 5 | **Money** | Money lane | dedicated | Itch, offers, earnings — the next-dollar lane. |
| 6 | **Physique Lab** | Physique Lab / SmutBase lane | dedicated | Model fixes and visual proofs (texts carry the proof links). |
| 7 | **Wizard Gang** | Wizard Gang series lane | dedicated | Episode/pipeline work. |
| 8 | **Ops** | Disk guardian + overnight pipeline + watchdogs | dedicated | Mostly agent-initiated: alerts and landed-work summaries. Replies go to the ops lane. |

**Count: 8 dedicated numbers** — this is the set the live cost estimate
in SETUP-LIVE.md is built on (~$24/mo all-in on the recommended route).
All 8 sit in one 10DLC campaign's sender pool (see SETUP-LIVE.md for why
that's the legal shape, and why 8 toll-free numbers is not).

Rules baked into the registry (`config/agents.example.json`):

- Production numbers are never written in the registry file. Each entry
  names an env var (`numberEnv`, e.g. `NUMBER_ASHES`); the real number
  is injected at deploy time from secrets.
- A number belongs to exactly one agent (the gateway refuses duplicate
  numbers at boot) — a contact can never silently become another agent.
- Adding an agent later = buy a number, attach it to the same campaign,
  add a registry row, restart. No code change.
- Merging two lanes later = retire a number; the contact just stops
  answering (the thread history stays in the conversation log).

Expansion candidates (from the 2026-11-04 checkpoint/side-chat census —
real lane families not in the v1 eight): TRIPPEDD, Teardowns, Merge Ops,
Concrete Dragon (overlaps Money — one contact or two is the owner's
call), TorBox. Each addition is one more number on the same campaign:
+$1/mo, no new registration.

Phase note: at go-live, Ashes' bridge wires first (texts reach the main
agent). Each other contact answers through its stub until that lane's
chat bridge is connected (ARCHITECTURE.md, "chat-backend bridge") — the
contact exists and is saveable from day one, and the registry records
which are fully wired.
