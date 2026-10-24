# CROSS-REPO STRANDED-WORK AUDIT — 2026-10-23

Owner question (verbatim): "what else hasn't been pushed or merged or completed"

Scope: every game repo EXCEPT western-heart (112 open / 607 merged PRs — owned by a separate audit lane).
Repos audited: wrestling-game, game-reverse-engineering, ConcreteDragon, cape-jones, and Bannon
(found during the audit — the Bannon goals live there). Method: live `gh` API on 2026-10-23 —
open-PR mergeable/state, changed-file counts, branch-vs-main containment (`compare main...branch`),
and contents-API spot verification of whether payloads already exist on main. Nothing in this
report was merged or closed by the audit; classification only.

## Headline

- **69 open PRs audited** across the 5 repos. **Zero are conflicting** except 2 in Bannon.
  The dominant failure class is not conflict — it is **MERGEABLE work sitting unmerged**:
  - wrestling-game: 11/11 open PRs MERGEABLE, all state UNSTABLE (CI not green — Actions quota outage).
  - game-reverse-engineering: 33/33 MERGEABLE, all UNSTABLE.
  - ConcreteDragon: 4/4 MERGEABLE, all BLOCKED (branch protection on main).
  - cape-jones: 3/3 MERGEABLE and CLEAN — but all 3 are owner-held decisions, not neglect.
  - Bannon: 16/18 MERGEABLE/UNSTABLE, 2 CONFLICTING/DIRTY, 1 empty (0 files).
- **No-PR stranded branches** (unique commits not on main, no open PR): wrestling-game 1,
  game-reverse-engineering 3 (+7 orphan-history branches), ConcreteDragon 8, cape-jones 0 in sample.
- **Local-only work**: wrestling move FBX/JSON set in `~/workspace/wrestling-work/` (not a git repo);
  uncommitted edits in the local agent-ops clone; dirty local cape-jones clone (lane-owned).

Status classes used below:
- **STRANDED-READY** — payload exists nowhere on main; PR/branch is the only copy; land it.
- **STRANDED-CI** — MERGEABLE but checks not green (quota outage); stranded on CI, not on content.
- **BLOCKED-PROTECTION** — MERGEABLE but branch protection blocks merge (ConcreteDragon).
- **OWNER-HELD** — deliberately unmerged per standing owner decision/exclusion.
- **DUPLICATE** — same payload as a twin PR/branch; land one, close the other.
- **ALREADY-ON-MAIN** — branch contained in main (ahead_by=0); hygiene only.
- **ORPHAN-HISTORY** — no common ancestor with main; cannot PR/merge normally.
- **NEVER-STARTED / DOES-NOT-EXIST** — claimed or owed work that exists nowhere.

---

## 1. mhvnsnt/wrestling-game — 11 open / 7 merged PRs; 19 branches

All 11 open PRs: MERGEABLE, state UNSTABLE (STRANDED-CI). Verified: `models/` on main contains
only `wwe-wrestlemania-xix` — the No Mercy wrestler GLBs are NOT on main. Main `AGENTS.md`
contains **0** mentions of "anti-clobber" — the law never landed here.

| Item | Payload | Class | Recommendation |
|---|---|---|---|
| PR #14 (2026-10-21) W5a Def Jam reconciliation | 9 files, +1196 | STRANDED-READY | Land first in the W5 set (foundation doc) |
| PR #15 W5b G1 Def Jam archives (42 entries) | 42 files | STRANDED-READY | Land with W5 set |
| PR #16 W5b G2 Def Jam archives (217 entries) | 217 files | STRANDED-READY | Land with W5 set |
| PR #17 W5b G3 Def Jam archives (653 entries) | 653 files | STRANDED-READY | Land with W5 set |
| PR #18 W5b microcode hunt (exhaustive negative) | 2 files, +101 | STRANDED-READY | Land with W5 set (valid negative result) |
| PR #9 (2026-10-17) 10 No Mercy wrestlers, 13 GLBs | 14 files | STRANDED-READY | Land here (canonical home per owner rule); Bannon #87 is its twin |
| PR #13 (2026-10-19) Teardown mirror (NM/WMXIX/2K docs+tools) | 139 files, +63,917 | STRANDED-READY | Land; Bannon #92 is its twin |
| PR #10 (2026-10-17) Render-orientation method + tpose tools | 3 files, +614 | STRANDED-READY | Land (same doc family as GRE #11, CD #59) |
| PR #11 Anti-clobber law (`law/anti-clobber-20261017`) | 1 file, +7 | DUPLICATE pair with #12 | Land ONE of #11/#12, close the other |
| PR #12 Anti-clobber laws (`anti-clobber-laws`) | 1 file, +16 | DUPLICATE pair with #11 | See #11 |
| PR #6 (2026-10-15) MERGE-IT-YOURSELF law doc | 1 file, +8 | STRANDED-READY | Land (twin PRs exist in GRE #6, CD #60) |
| Branch `docs/sale-status-owner-rule-2026-10-14` | 1 commit ahead, NO PR | STRANDED-READY | Open PR or fold into a docs landing; same branch stranded in GRE + ConcreteDragon |
| Local `~/workspace/wrestling-work/` | 6 wrestling-move FBX (BrainBuster, Chokeslam, DDT, GermanSuplex, Suplex, Tombstone) + 6 matching JSON | LOCAL-ONLY, never committed anywhere | Commit into wrestling-game (moves/animation intake) |

Already on main (ahead_by=0, no action): branches `docs/no-data-loss-rules`,
`docs/wrestling-animation-pipeline`, `feat/wwe2k-packs-docs`, `teardown/def-jam-ffny`,
`tools/partposer`, `wmxix-wrestler-000`.

**wrestling-game totals:** 11 PRs stranded (10 unique payloads, 1 duplicate pair), 1 no-PR branch,
1 local-only payload set.

---

## 2. mhvnsnt/game-reverse-engineering — 33 open / 11 merged PRs; 55 branches

All 33 open PRs: MERGEABLE, state UNSTABLE (STRANDED-CI). Main `AGENTS.md` contains **0**
mentions of "anti-clobber" — the law never landed here either, despite the 2026-10-17
propagation record. Note the stacking pattern: teardown phase branches are cumulative
(each phase branch carries the previous phases' commits — e.g. SCII phase 10 is 144 commits
ahead of main), so landing order matters.

### SF EX trilogy (fresh, 2026-10-23 — active program)
| PR | Payload | Class |
|---|---|---|
| #42 Phase 1: PAC loader contract + EX2 model decode + census | 216 files, +13,245 | STRANDED-READY |
| #43 Phase 2: EX1 geometry + EX2 textures + EX3 archive | 60 files, +45,160 | STRANDED-READY |
| #44 Phase 3: EX1 TMD assembly + EX3 .mdl contract | 150 files, +6,599 | STRANDED-READY |
| #45 Phase 4: animation decode + final state | 43 files, +7,826 | STRANDED-READY |
Land in phase order #42 → #43 → #44 → #45.

### SoulCalibur II phases (stacked, 2026-10-20/21)
| PR | Payload | Class |
|---|---|---|
| #26 Model hunt: archive map + XBE loader + blocker | 4 files, +302 | STRANDED-READY (stack base) |
| #28 Phase 2: VMX format cracked | 8 files, +613 | STRANDED-READY |
| #30 Phase 3: fighter position stream, idx47 GLB | 11 files, +411 | STRANDED-READY |
| #31 Phase 4: rigid placement + 24-slot batch | 50 files, +1,187 | STRANDED-READY |
| #32 Phase 5: skinning SOLVED, 22 GLBs, 24 movesets | 55 files, +46,632 | STRANDED-READY |
| #33 Phase 6: motion DB crack, +30 fighter DBs | 3 files, +639 | STRANDED-READY |
| #34 Phase 7: bank track layout + decoder | 4 files, +380 | STRANDED-READY |
| #36 Phase 8: composition, D-formula refuted | 3 files, +363 | STRANDED-READY |
| #37 Phase 9: template initializer corrected | 2 files, +386 | STRANDED-READY |
| #40 Phase 10: composition candidates + state packet | 13 files, +1,393 | STRANDED-READY (stack tip) |
Land in phase order, or verify the #40 tip carries the full stack and land the tip.

### Tekken 5 lanes (2026-10-20)
| PR | Payload | Class |
|---|---|---|
| #20 DATA0/DATA1 cipher hunt | 3 files, +1,949 | STRANDED-READY |
| #21 Devil Within deep-dive | 69 files, +22,348 | STRANDED-READY |
| #22 Production architecture docs (Lane F) | 2 files, +869 | STRANDED-READY |
| #23 E5/E6 data: roster ground truth, name tables | 3 files, +7,122 | STRANDED-READY |
| #24 Research pull-in: IPU/TIM2/Ghidra-EE tools (Lane G) | 40 files, +12,896 | STRANDED-READY |
| #25 E7 72-file archive catalogue + E8/E9 maps (Lane C) | 8 files, +1,798 | STRANDED-READY |
| #27 Lane E: ISO complete (MD5 verified) + extraction status | 1 file, +44 | STRANDED-READY |

### Yu Yu Hakusho / W1 / research / tooling
| PR | Payload | Class |
|---|---|---|
| #35 YYH Dark Tournament census (W2) | 3 files, +1,632 | STRANDED-READY |
| #39 YYH RESOURCE.PAK unpacker + Toguro teardown | 23 files, +27,291 | STRANDED-READY |
| #41 YYH MDL→GLB (47-bone) + 4-PAK reconciliation | 8 files, +533 | STRANDED-READY |
| #38 W1 census: WWE All Stars — Rock animation data located | 2 files, +3,209 | STRANDED-READY |
| #29 Teardown-completion research (8 unfinished games) | 9 files, +639 | STRANDED-READY |
| #10 RE/teardown tooling pull-in (9 tools) | 905 files, +297,834 / **−2** | STRANDED-READY — note 2 deletions; run the deletion guard before merge |
| #9 RE toolchain research + install scripts | 11 files, +528 | STRANDED-READY |
| #7 WMXIX YOBJ skinning decoder (blocker documented) | 12 files, +1,744 | STRANDED-READY |

### Law/docs duplicates
| PR | Payload | Class |
|---|---|---|
| #13 Anti-clobber laws (+17) / #12 Anti-clobber law (+8) | 1 file each | DUPLICATE pair — land one, close other |
| #11 Render-orientation docs | 3 files, +614 | STRANDED-READY (family: wrestling #10, CD #59) |
| #6 MERGE-IT-YOURSELF law | 1 file, +8 | STRANDED-READY (family: wrestling #6, CD #60) |

### Branches with unique work and NO PR
| Branch | Ahead | Class |
|---|---|---|
| `feat/re-toolchain-research-20261016` | 8 commits | STRANDED — sibling of PR #9/#10 material, never PR'd |
| `watchdog/tekken6-decrypt-callgraph-20261015` | 4 commits | STRANDED — T6 decrypt callgraph work, never PR'd |
| `docs/sale-status-owner-rule-2026-10-14` | 1 commit | STRANDED (same in wrestling-game + ConcreteDragon) |

### Orphan-history branches (NO common ancestor with main — cannot be PR'd/merged normally)
`master`, `offload-push`, `push-clean`, `tekken-pull-verify-20261013`,
`watchdog/doa4-download-fix`, `watchdog/wrestling-teardown-20261013`, `feat/ymg-skinning-decoder`.
Class: ORPHAN-HISTORY. Recommendation: archive each tip to a release, then owner decision on
deletion (REPO LAW: no repo/branch deletion without owner sign-off).

Already on main (ahead_by=0): `chore/offload-commit-20261015`, `chore/teardown-status-20261019`,
`feat/tekken5-100-teardown-resume`, `feat/tekken5-binary-teardown`, `feat/tekken5-deobfuscator-cracked`,
`feat/tekken5-obfuscation-analysis`, `feat/tekken5-teardown-start`, `offload/pushable-20261014`,
`wwe2k-lane-docs`, `docs/no-data-loss-rules`.

**GRE totals:** 33 PRs stranded (31 unique payloads + 1 duplicate pair), 3 no-PR stranded branches,
7 orphan-history branches.

---

## 3. mhvnsnt/ConcreteDragon — 4 open / 56 merged PRs; 59 branches

All 4 open PRs: MERGEABLE, state **BLOCKED** — branch protection on main is the blocker
(matches the standing record for CD #59/#61). Main `AGENTS.md` contains **0** mentions of
"anti-clobber" — the law never landed here.

| Item | Payload | Class | Recommendation |
|---|---|---|---|
| PR #62 (2026-10-20) Quantum Game Jam 2026 prep: district build + quantum-seeded scaffold | 8 files, +982 | BLOCKED-PROTECTION + purpose-expired: the jam itself ran Sep 25–28, 2026 and is over (verified by main agent 2026-10-22); nothing was ever submitted | Owner decision: land the district build as ordinary repo work, or close |
| PR #61 Anti-clobber laws | 1 file, +17 | BLOCKED-PROTECTION, DUPLICATE of #60's law family | Land one law PR after protection is resolved |
| PR #60 Anti-clobber law (`law/anti-clobber-20261017`) | 1 file, +7 | BLOCKED-PROTECTION, DUPLICATE pair with #61 | See #61 |
| PR #59 Render-orientation docs | 3 files, +614 | BLOCKED-PROTECTION | Land (family: wrestling #10, GRE #11) |

### Branches with unique work and NO PR
| Branch | Ahead | Notes |
|---|---|---|
| `feature/customization-suite` | **11 commits** | Biggest stranded CD branch — the customization suite build |
| `content/waves-2-4` | 4 commits | Content waves 2–4 (`content/wave-1` IS on main) |
| `weight-paint-pwa` | 3 commits | Weight-paint PWA work |
| `feat/youtube-videos-archive` | 2 commits | Video archive |
| `improveloop-c5` | 1 commit | Improvement loop c5 (c1–c4 are on main) |
| `mirror/streetbrawl-20261017` | 1 commit | Streetbrawl mirror |
| `mirror-checkpoint-20261017` | 1 commit | Mirror checkpoint |
| `backup/box-2026-10-14-ig-w-ConcreteDragon-feat-instruction-gate` | 1 commit | Backup snapshot branch — archive, don't PR |
| `docs/sale-status-owner-rule-2026-10-14` | 1 commit | Same stranded docs branch as wrestling-game + GRE |

Local state: `~/workspace/concrete-dragon-itch/` (itch staging) untouched since Oct 9 —
the itch.io upload/payout step never happened (owner-manual blocker in the money pipeline).

**ConcreteDragon totals:** 4 PRs blocked (3 unique payloads), 8 no-PR stranded branches
(+1 shared docs branch).

---

## 4. mhvnsnt/cape-jones — 3 open / 207 merged PRs; 176 branches

All 3 open PRs: MERGEABLE, state **CLEAN** — mechanically mergeable today. All 3 are
**OWNER-HELD** per standing records (the sitting-take choice is the owner's;
#156/#157 carry a do-not-merge standing note; #167 is owner-gated). This repo's backlog
is a decision backlog, not a neglect backlog.

| Item | Payload | Class |
|---|---|---|
| PR #167 (2026-10-20) Mesh hole repair pipeline | 6 files, +595 | OWNER-HELD |
| PR #157 (2026-10-19) Sitting redo take 3 | 10 files, +289 | OWNER-HELD (sitting-take decision) |
| PR #156 (2026-10-19) Sitting redo v5 (5 poses) | 18 files, +93 | OWNER-HELD (sitting-take decision) |

Main `AGENTS.md` DOES contain the anti-clobber law (3 mentions) — landed here.

Branches: **176 remote branches**, the largest pile of any repo audited. Sample-verified
8 representative no-PR branches (`anim-stack-20261019`, `cape-jones-show-v1`,
`lane/cape-rebuild-20261017`, `feature/expansion-3`, `ai-body-replace`,
`pull/animation-tools-20261017`, `agents/ai-coding-team-20261016`, `mega-pull-pipeline`):
**all ahead_by=0 — fully contained in main.** The branch pile is merged-but-never-deleted
hygiene debt, not stranded work. A dedicated branch-hygiene pass (verify contained → delete)
would clear it; deletion needs the usual care, not owner time.

Local state: `~/workspace/cape-jones` clone is dirty — ~10.4k unstaged deletions
(anim-stack donor mocap files) on branch `pull/glaxnimate-20261023`. The deleted content
is contained on main (recoverable from git history); lane-owned state, flagged not touched.

**cape-jones totals:** 0 stranded PRs (3 owner-held), 0 stranded branches in sample.

---

## 5. mhvnsnt/Bannon — 18 open / 70 merged PRs; ~90 branches (found during this audit)

The Bannon goals (character model repair, playable build) live in their own repo,
mhvnsnt/Bannon — it was not in the original four-repo list and carries its own backlog:
18 open PRs, of which 16 are MERGEABLE/UNSTABLE (STRANDED-CI), 2 are CONFLICTING/DIRTY,
4 are drafts. Bannon checkpoints (`bannon-ci-fix`, `bannon-correct-render`) are both `done` —
no active Bannon lane; the backlog is dormant, not in flight.

| Item | Payload | Class |
|---|---|---|
| PR #77 (2026-10-14) Rig repair pipeline + STICK UP entrance arena | 11 files, MERGEABLE | STRANDED-READY — the model-repair line |
| PR #48 (2026-10-08) Rig hardening: GLB rig gates + 4 defect fixes | 5 files, MERGEABLE | STRANDED-READY — model-repair line |
| PR #78 (2026-10-14) STICK UP full-quality original model | 4 files, **DRAFT** | OWNER-HELD — standing do-not-merge draft |
| PR #49 (2026-10-09) Stick-Up v2 staged entrance cinematic | 8 files, MERGEABLE | STRANDED-READY — playable-build line |
| PR #41 (2026-09-14) CI: keep PWA synced with playable revisions | 4 files, MERGEABLE | STRANDED-READY — playable-build line |
| PR #84 Universal rig standard + rig runner docs | 2 files, MERGEABLE | STRANDED-READY |
| PR #80 Producerbot handoff runbook | 1 file, MERGEABLE | STRANDED-READY |
| PR #92 Teardown mirror (NM/WMXIX/2K) | 139 files, MERGEABLE | DUPLICATE of wrestling-game #13 — land in one repo, close twin |
| PR #87 No Mercy wrestler models (13 GLBs) | 14 files, MERGEABLE | DUPLICATE of wrestling-game #9 — land in wrestling-game, close this |
| PR #89 Anti-clobber law | 1 file, MERGEABLE | PARTIALLY LANDED — main `AGENTS.md` has 1 anti-clobber mention; verify full text before closing |
| PR #88 Render-orientation docs | 3 files, MERGEABLE | STRANDED-READY (doc family) |
| PR #83 MERGE-IT-YOURSELF law | 1 file, MERGEABLE | STRANDED-READY (doc family) |
| PR #39 (2026-09-02) BannonEngine module + full-repo reality audit | 21 files, **CONFLICTING/DIRTY** | STRANDED-CONFLICTING — needs rebase/conflict work |
| PR #38 (2026-08-04) Grapple solver model fixes | 44 files, **CONFLICTING/DIRTY** | STRANDED-CONFLICTING — oldest substantive PR in the audit |
| PR #45 Emulator staging | 18 files, **DRAFT** | OWNER-HELD (temporary staging by design) |
| PR #44 Animation bridge: source registry + retarget lane | 3 files, **DRAFT** | DRAFT — revive or close by owner call |
| PR #43 UE 5.8 migration | 3 files, **DRAFT** | DRAFT — superseded in practice by UE5.5/5.6/5.8 branch pile |
| PR #22 (2026-07-07) "Aye" | **0 files** | EMPTY — close candidate (nothing to land) |

**Bannon totals:** 11 stranded-unique PRs, 2 conflicting, 2 duplicate twins, 1 partially landed,
1 empty, 4 drafts (1 owner-excluded, 3 dormant).

---

## 6. Known non-PR stranded categories (verified against repos/checkpoints)

1. **Tekken 6 motion/move extraction — BLOCKED, needs owner.**
   The T6 teardown's landed product is in the repos, but motion extraction itself is blocked
   on the decrypt6 encode-context (DEFLATE distance-table) crack, unsolved since 2026-10-16.
   Checkpoint `wh-tekken6-100` is kept heartbeat-alive by its watchdog but its core path is
   parked `needs_owner`. Class: **DOES-NOT-EXIST yet — blocked, not neglected.**
   Related stranded branch: GRE `watchdog/tekken6-decrypt-callgraph-20261015` (4 commits, no PR).

2. **TTT2 Phase 2 extraction — IN PROGRESS, not stranded.**
   Checkpoint `ttt2-resume-100` status `running` with a fresh heartbeat (2026-10-23);
   the Phase-2 pull is live. The reassembly path is parked by design behind a disk gate.
   Class: **ACTIVE**.

3. **No Mercy wrong-window re-extraction — OWED, never started.**
   The 2026-10-13 extraction (checkpoint `extract-nomercy`, status done) used the wrong
   FileTable window; per the later audit (western-heart PR #505), EVERY No Mercy-derived
   asset on western-heart main is wrong-window. The correct-window re-extraction plus
   per-character rewiring **exists nowhere**. Class: **CLAIMED-DONE-BUT-WRONG** —
   the "done" extraction is the wrong one; the real program is unstarted.

4. **Def Jam converter/catalog wiring into western-heart CATALOG.json — NEVER RUN.**
   The Def Jam payload itself (912 extracted parts, motion census exact) is real, but it sits
   in wrestling-game PRs #14–#18 (open, unmerged). The downstream wiring step — converter +
   CATALOG.json integration — was never run and exists nowhere.
   Class: **NEVER-STARTED downstream step**, gated on landing the wrestling-game W5 set first.

5. **Bannon goals** — see section 5. Model repair = PRs #77/#48 (stranded-ready) + #78
   (owner-held draft). Playable build = #49/#41 stranded-ready; UE migration line dormant
   in drafts #43/#45/#44.

---

## 7. Claimed-done in records, but could not be located on any main

1. **Anti-clobber law "propagated to 135/135 repos"** — in the repos audited here, the law text
   is verifiably ABSENT from the main `AGENTS.md` of wrestling-game, game-reverse-engineering,
   and ConcreteDragon (0 mentions each, contents-API verified 2026-10-23), and only partially
   present in Bannon (1 mention). It IS landed in cape-jones (3 mentions) and western-heart.
   The propagation record and the repos disagree; the repos win.
2. **Def Jam "912/912 extracted + stored"** — true only as open-PR branches in wrestling-game
   (#15/#16/#17). Not on any main. "Stored" meant "on a branch."
3. **No Mercy extraction "done" (2026-10-13)** — located, but it is the wrong-window set
   (see 6.3). The correct extraction exists nowhere.
4. **Quantum Game Jam entry** — the jam ran Sep 25–28, 2026 and closed with 26 entries;
   ConcreteDragon PR #62's district build never landed and nothing was submitted under it.
5. **Wrestling-game teardown mirror + No Mercy models** were described in records as living
   in "the wrestling repos" — they live only on open-PR branches (#9/#13, Bannon #87/#92),
   not on either repo's main.

---

## 8. Prioritized landing order (cross-repo)

1. **wrestling-game W5 Def Jam set** — #14 → #15 → #16 → #17 → #18. Unblocks the never-run
   CATALOG.json wiring (6.4). All MERGEABLE; needs CI green or an owner-approved path around
   the quota outage (resets 2026-11-01 per records).
2. **No Mercy wrestlers, once** — wrestling-game #9 (canonical home); then close Bannon #87
   as duplicate. Same for the teardown mirror: wrestling-game #13, close Bannon #92.
3. **GRE SF EX phases** — #42 → #43 → #44 → #45 in order (fresh, active program).
4. **GRE SCII stack** — land in phase order #26/#28/#30/#31/#32/#33/#34/#36/#37/#40,
   or verify the #40 tip carries the whole stack and land the tip.
5. **GRE Tekken 5 + YYH + W1 sets** — #20/#21/#22/#23/#24/#25/#27, then #35/#39/#41, then #38.
   Run the deletion guard on #10 (905 files, −2) before its merge.
6. **Law/doc dedup, one per repo** — anti-clobber: wrestling-game (one of #11/#12),
   GRE (one of #12/#13), ConcreteDragon (#61 after protection is resolved), Bannon (#89 after
   text verification). MERGE-IT-YOURSELF: #6 in wrestling-game/GRE/Bannon.
   Render-orientation: wrestling #10 / GRE #11 / CD #59 / Bannon #88.
   Plus PRs for the shared `docs/sale-status-owner-rule-2026-10-14` branch (3 repos).
7. **ConcreteDragon** — resolve the branch-protection block (repo settings decision), then
   #62 owner decision (land as repo work or close — jam is over), then open PRs for
   `feature/customization-suite` (11 commits) and `content/waves-2-4`.
8. **Bannon** — rig line #77 + #48; playable line #49 + #41; then conflict work on #39/#38
   (rebase, keep both sides); close empty #22. Drafts stay as-is per owner exclusion.
9. **Local-only payloads** — commit `~/workspace/wrestling-work/` FBX+JSON set into
   wrestling-game; commit or discard the uncommitted agent-ops clone edits (they sit on
   branch `docs/research-conventions-20261016` in the local clone).
10. **Orphan-history GRE branches (7)** — archive tips to releases; deletion only with
    owner sign-off (REPO LAW). **cape-jones branch hygiene** — 176 branches, sample-verified
    contained; bulk-delete contained branches in a dedicated pass.

*Audit performed 2026-10-23 by the cross-repo stranded-work lane. All counts are live-API
values from that date; CI states reflect the GitHub Actions quota outage period.*
