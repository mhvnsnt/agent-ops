# TAG-TEAM board (live)

Last updated: 2026-10-14 3:23 PM CT by Repo Co Dev (claims refresh).
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
| 8 | AshLanev2 #38 + #42 (crash fix / visual tests) | Repo Co Dev | In progress | [AshLanev2 #38](https://github.com/mhvnsnt/AshLanev2/pull/38), [AshLanev2 #42](https://github.com/mhvnsnt/AshLanev2/pull/42) | Merge when green with proof; then Urban Reign chimera / mobile fidelity |
| 9 | western-heart Godot Lab 1v1 + T6/TTT2 importers | Repo Co Dev | In progress | [western-heart](https://github.com/mhvnsnt/western-heart) | Playable 1v1 on one stage; then T6/TTT2 + chimera importers. Private, never published |
| 10 | Shared creation suite with jiggle physics (Tripo first) | Repo Co Dev | In progress | western-heart `docs/creation-suite/` | Spec + first working import; body-size jiggle (glute/thigh/chest/belly); deepen from WWE/Tekken teardown suites |
| 11 | Templates PR | Producerbot | Open | [money-machine-hq #16](https://github.com/mhvnsnt/money-machine-hq/pull/16) | Get CI green, then merge |
| 12 | El Toro hometown placeholder | Producerbot | Open | money-machine-hq `tracks/promo-cinematic-kit/` | Replace the placeholder with the hometown from canon. Never guess it |
| 13 | Owner to-dos | Owner | Waiting | (none) | Revoke the 2 Bannon GitHub tokens and the Telegram token. Rotate the Gemini, HF and Firebase keys. Create the Neon PR. Review the Mochiichao PR. Have Muse push its why-shortcut-research file |

| 14 | Brutal-Fist all-character model audit + Tripo intake | Repo Co Dev | In progress | [brutalfistgrokversionten](https://github.com/mhvnsnt/brutalfistgrokversionten) (Bannon bone fix merged in #34) | Every character arena-pass like Bannon; Tripo export intake; secondary-bone / jiggle later |
| 15 | Cloudflare Pages PWAs (private-repo deploys) | Repo Co Dev | Live (manual redeploy) | [bannon.pages.dev](https://bannon.pages.dev), [brutalfist.pages.dev](https://brutalfist.pages.dev), [ashlane-1aa.pages.dev](https://ashlane-1aa.pages.dev) | Redeploy as merges land; AshLane from crash-fix branch until main builds |
| 16 | western-heart per-character height/scale (owner rule c) | Grok Bot | PR open | [western-heart #120](https://github.com/mhvnsnt/western-heart/pull/120) | **Heads-up, Repo Co Dev:** this adds a scale hook inside your Lab claim, additive only. `fighter.gd` gets `char_id`, `height_cm` and `apply_height(id)`. `main.gd` gets an `apply_height` call for both fighters, a cm readout on the HUD names, and `--p1-char`/`--p2-char`. New files: `scripts/height_scale.gd` and `data/characters/heights.json`. Keep `apply_height` after `setup()` when you refactor. Swap in T6/TTT2 skeleton heights when your importer lands |

## Tasks Muse can claim now
Add a line to CLAIMS.md first.
- **Canon character art for the Fiverr samples** (#4): replace the stand-in mascot with the owner's real characters. Edit the existing sample files in PR #25's branch. Don't regenerate them from scratch.
- **Goodville segment edits with mask cutouts** (#6): use Smart/Magic Cut that follows each piece's edges. **No rectangular crops.** Show proof on a checkerboard, matched to the Preston Blair frames (beer-can hold, punch, face).
- **Gig 3 video cut from the Bannon render**: cut a sample from the existing render. Log the method and commit with a hash of the output.
- **Push the why-shortcut-research file** (#13) to agent-ops via a branch plus PR.
