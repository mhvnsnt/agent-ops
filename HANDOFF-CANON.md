# HANDOFF — CANON (where the game's knowledge lives)


## OBSOLETE-ORIGINALS RULE (owner, 2026-10-23 — binding)

Canon is **never** written for obsolete originals — source-game characters whose moveset and identity became a proprietary character of this universe. They get no canon file, no bio, no story, no roster entry, and never appear on the character select list. Their models exist only as late-ladder attires (slots 5+) of their successor, behind Tripo models and the owner's proprietary reskins. **Write all canon for the SUCCESSOR.**

Mapping: Blanka->CHARGER, Zangief->KRONOS, Vega->KORESHI, Iori->DEATHFANG, Kuma->GASHADOKURO, Panda->AOTSUKI, Baek->KEVIN, Zafina->MARIPOSA, Lili->SILVERTONGUE, Jin->DEMONIO, Armor King->YUKIHYO; base-only names (never had roster entries, scaffolding mentions only): Xiaoyu, Christie, Nina, Asuka, Bryan, Bob, Heihachi, King, Yoshimitsu, Lei, Dragunov, Ganryu, Mokujin. Existing text about originals is KEPT with the obsolete notice at the top. Authority: mhvnsnt/western-heart `docs/OBSOLETE-ORIGINALS-RULE.md` (on main since 2026-10-23, PR #766).

State verified 2026-10-23. Sources: western-heart main tree check (main agent, 2026-10-23), `MERGE-QUEUE.md`, owner directives recorded 2026-10-23. Purpose: no agent ever again reports canon as "missing" because it wasn't in the repo, or holds it only in chat memory.

## The rule (owner, 2026-10-23 — binding)

When the owner says merge and push everything to main, that means **all the canon, all the notes, all the development records** — not just code. Canon, notes, and decisions are committed to the repos **the day they are recorded**. Assistant memory files (`~/MEMORY.md`, `~/memory/*.md`) are a **working copy only, never the only home**. If canon exists only in a memory file, that is a defect: sync it (overnight pipeline v2 STEP 4 does this every run) and queue anything you can't land immediately in `MERGE-QUEUE.md`.

## Where canon lives

| Location | What | State |
|---|---|---|
| mhvnsnt/western-heart `roster/<fighter>/CANON.md` | Per-fighter canon, in the game repo | Only 4 fighters landed so far (below); harvest in flight |
| mhvnsnt/western-heart `docs/canon-archive/` (`CANON-MASTER.md`, `DEV-NOTES-ARCHIVE.md`) | The full compiled record: every fighter's recorded canon + development notes/decisions archive | Archive push IN FLIGHT (branch in progress 2026-10-23) — game material only; the owner's personal/legal/financial information never goes in any repo |
| `~/MEMORY.md` + `~/memory/2026-*.md` | Assistant's working copy where canon is first recorded | NOT a source of truth for other agents — if it's only here, it effectively doesn't exist for the fleet |

## Verified state on main today

Only **4 of 67** roster dirs have a canon file on main:
- `roster/buffalo-bill/CANON.md`
- `roster/dorowani/VOICE-CANON.md` (voice canon)
- `roster/gyou/CANON.md`
- `roster/zen/CANON.md`

The other 63 dirs have no canon file on main. That does NOT mean the canon doesn't exist — most of it is recorded in the memory working copy (e.g. full owner-locked sections for Pantera, Doc Frank, Michiko, Torch, Dio, Zen, CornerStone, Mariposa, Sun Rā, Thor, Deathfang, and the nine-souls world canon). It was simply never committed. The bios harvest (below) is closing exactly this gap. **Never tell the owner or another agent a fighter "has no canon" until you have checked: (1) the repo, (2) `docs/canon-archive/` once landed, (3) the memory working copy via the main agent.**

## In flight (2026-10-23 — verify before assuming landed)

- **Bios harvest batch 1** — writes `roster/<dir>/CANON.md` for 25 fighters (pantera, demonio, zui, skull, doc-frank, cyborg-x, michiko, torch, dio, deathfang, charger, kronos, koreshi, nightwolf, star, slice, awa-pop, burger, sam-ur-a1, yukihyo, ryuji-rock, kiko-tanaka, kinpo, diablo, phantom), compiled ONLY from owner-recorded material (memory files + repo docs). Invention is banned: every file carries `## Not yet recorded` and `## Sources` sections. Fighters with zero recorded material get NO file — they go on the truly-blank list (below). Rave's canon file goes in `roster/kiko-tanaka/` (Kiko Tanaka = Rave in this game).
- **Canon archive push** — the `docs/canon-archive/` landing described above.
- Further batches follow batch 1 until every fighter with recorded material has a file on main.

## The truly-blank process

Some fighters genuinely have no recorded canon anywhere (owner's own list includes most of the SmutBase intake — Mina Ashido, Mirko, Rahkasa, Parvati, Tsuyu, Vixen — until he dictates them). For those:
1. They appear on the harvest lane's **truly-blank list** — that list is the deliverable, not a failure.
2. **Nobody invents bios.** Not from the base character, not from vibes, not from another AI's output.
3. The owner dictates; we write it **verbatim** into `roster/<dir>/CANON.md` and merge it the same day. His word is the only source.

## Canon handling rules for every agent

- Attribute characters by **traits**, not by typed name — dictation garbles names ("Tanisha" = Tyneshia; "Goodwill" = Goodville; "Vigil/Viggle" = Viggle; "the sea" = CN). Tekken base names in mapping docs (e.g. Pantera ← King) are transitional scaffolding, not canon errors.
- Owner bios/canon go in **word-for-word** where he dictated them; mark owner-locked sections as such (see `roster/zen/CANON.md` for the format).
- Anything the owner talked about gets harvested from the record — never declare material "missing" without checking all three locations above.
- When you record new canon in a session, the session isn't done until it's committed to the repo (branch → PR → merge → verified on main, per HANDOFF-INDEX.md).
