# TAG-TEAM board (live)

Last updated: 2026-10-14 3:20 PM CT by Grok Bot (MoneyManBusch).
Agents: **Grok Bot** (MoneyManBusch), **Muse/Ashes** (Meta), **Repo Co Dev**, **Producerbot**, **Dom Assist**, **Owner** (Marquis, mhvnsnt).

Before touching anything: read [HOW-GROKBOT-WORKS.md](HOW-GROKBOT-WORKS.md), then add a line to [CLAIMS.md](CLAIMS.md).
Update your row's status and link in the same PR as your work.

| # | Workstream | Owner | Status | Links | Next step |
|---|---|---|---|---|---|
| 1 | Muse training pack | Grok Bot | Merged | [money-machine-hq #20](https://github.com/mhvnsnt/money-machine-hq/pull/20) | Muse: load it into memory. Add new mistakes to EXAMPLES.md |
| 2 | Activity proof for Muse | Grok Bot | Merged | [agent-ops #4](https://github.com/mhvnsnt/agent-ops/pull/4) | Muse: read it. Search commits by author `mhvnsnt`, not "Grok Bot" |
| 3 | Code Doctor launch kit | Grok Bot | Kit merged, page live. Fiverr gig 1 being filled in the browser | [money-machine-hq #23](https://github.com/mhvnsnt/money-machine-hq/pull/23), [landing page](https://mhvnsnt.github.io/code-doctor/) | Owner approves gig 1 before Publish, then gig 2. Wire the gig URLs into the landing page |
| 4 | Fiverr creative gig lineup (7 gigs) | Grok Bot | PR open. Samples use a stand-in mascot until owner canon art is in | [money-machine-hq #25](https://github.com/mhvnsnt/money-machine-hq/pull/25) | Swap in canon character art, owner picks which gigs go live |
| 5 | animation-research-library | Grok Bot | 30 films in the repo. 64-file download queue blocked by low disk. Box disk cleanup in progress (only clearing things confirmed saved on GitHub) | [repo](https://github.com/mhvnsnt/animation-research-library) | Resume the one-file-at-a-time queue once there's room |
| 6 | Goodville postmortem, mask cutouts, mobile layered timeline | Grok Bot | In progress | (PR link goes here when pushed) | Edge-following cutouts with checkerboard proof, Preston Blair frame mapping, Lahey/Dangley line sync |
| 7 | CI fixes: 7 repos merged while red, plus open PRs | Grok Bot | In progress | [western-heart #115](https://github.com/mhvnsnt/western-heart/pull/115), [AshLanev2 #40](https://github.com/mhvnsnt/AshLanev2/pull/40), [brutalfistgrokversionten #37](https://github.com/mhvnsnt/brutalfistgrokversionten/pull/37), [Brutal-Fist #27](https://github.com/mhvnsnt/Brutal-Fist/pull/27), [brutalfistgrokversion12 #1](https://github.com/mhvnsnt/brutalfistgrokversion12/pull/1), [Bannon #71](https://github.com/mhvnsnt/Bannon/pull/71), [chimera-emulator-hub #3](https://github.com/mhvnsnt/chimera-emulator-hub/pull/3). Open: [TRIPPEDD #257](https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/pull/257), [M.-Engine- #17](https://github.com/mhvnsnt/M.-Engine-/pull/17), [CODEDUMMY #3](https://github.com/mhvnsnt/CODEDUMMY/pull/3), [BioMechania #22](https://github.com/mhvnsnt/BioMechania/pull/22) | Fix the real builds. No disabling checks, no deleting work. BioMechania #22 needs the owner's review |
| 8 | AshLanev2 #38 crash fix | Repo Co Dev | In progress | [AshLanev2 #38](https://github.com/mhvnsnt/AshLanev2/pull/38) | Fix, with proof that it runs |
| 9 | western-heart Godot Lab 1v1 slice | Repo Co Dev | Queued after #8 | [western-heart](https://github.com/mhvnsnt/western-heart) | Godot 4, T3 to glTF importer, shared skeleton. Private, never published |
| 10 | Shared creation suite with jiggle physics (Tripo first) | Repo Co Dev | Queued | (TBD) | Spec plus first working import |
| 11 | Templates PR | Producerbot | Open | [money-machine-hq #16](https://github.com/mhvnsnt/money-machine-hq/pull/16) | Get CI green, then merge |
| 12 | El Toro hometown placeholder | Producerbot | Open | money-machine-hq `tracks/promo-cinematic-kit/` | Replace the placeholder with the hometown from canon. Never guess it |
| 13 | Owner to-dos | Owner | Waiting | (none) | Revoke the 2 Bannon GitHub tokens and the Telegram token. Rotate the Gemini, HF and Firebase keys. Create the Neon PR. Review the Mochiichao PR. Have Muse push its why-shortcut-research file |

## Tasks Muse can claim now
Add a line to CLAIMS.md first.
- **Canon character art for the Fiverr samples** (#4): replace the stand-in mascot with the owner's real characters. Edit the existing sample files in PR #25's branch. Don't regenerate them from scratch.
- **Goodville segment edits with mask cutouts** (#6): use Smart/Magic Cut that follows each piece's edges. **No rectangular crops.** Show proof on a checkerboard, matched to the Preston Blair frames (beer-can hold, punch, face).
- **Gig 3 video cut from the Bannon render**: cut a sample from the existing render. Log the method and commit with a hash of the output.
- **Push the why-shortcut-research file** (#13) to agent-ops via a branch plus PR.
