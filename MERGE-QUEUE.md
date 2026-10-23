# MERGE QUEUE — everything built but not landed, all repos

Rule: an item leaves this queue ONLY as LANDED-VERIFIED (payload confirmed on the repo's main by the checker) or OWNER-CLOSED. "Done" claims without main-verification do not count. Seeded 2026-10-23 from the cross-repo stranded audit (~/workspace/agent-ops/CROSS-REPO-STRANDED-AUDIT-2026-10-23.md, agent-ops PR #40) + main-agent verified counts. Western Heart fighter-content items land here when docs/CATCHUP-AUDIT-2026-10-23.md merges.
Canon-sync last run: never (starts with overnight pipeline v2).

## western-heart (112 open PRs / 759 branches / 89 releases at audit time)
- [OPEN-PR] Backlog triage in progress via catch-up audit + landing waves (wiring fixes → models → movesets → rigs → canon). CornerStone (ryuji-rock) wiring fix is wave 1 item 1: source/cornerstone-a1.glb archived on main, never copied to wired attire1/model.glb, never rigged, no roster-full entry.
- [BLOCKED] PR #497 — CONFLICTING; merging as-is regresses the #508 feet fix. Owning lane must rebase preserving #508.
- [BLOCKED] PR #498 — instruction-gate semantic fail (method used ≠ specified, deviations says none). Lane must correct.
- [OPEN-PR] PR #499 W3c AKI corrective — all 11 clips FAIL gate on true data, 0 rows; awaits AKI FK→T3 IK follow-on.
- [BLOCKED-owner-held] PR #377 — stays OPEN as evidence. Do not merge.
- [OPEN-PR] PR #462 Rig & Pose Studio — merge when CLEAN.
- [BLOCKED] No Mercy true-window re-extraction program — NOT RUN. All NM-derived assets on main are wrong-window (PR #505 audit). Correct re-extraction exists nowhere.
- [BLOCKED] Def Jam converter + CATALOG.json wiring — NEVER RUN. Gated on wrestling-game W5 set landing (below).
- [DONE 2026-10-23, PR #781 merged 12:57Z, verified on main by parent] OBSOLETE-ORIGINALS WIRING: FULL_ROSTER entries for zangief/vega/iori/armor-king REMOVED; their models verified reachable as late successor-ladder attires (zangief→Kronos 4–5, vega→Koreshi 3, iori→Deathfang 3, armor-king→Yukihyō 5–6, blanka→Charger 3; lili→silvertongue-noir-gala slot 4 and zafina→Mariposa already correct). Wave 1 also: MODEL_URLS 155→174 keys, broken targets 1→0, CornerStone copied byte-identical to wired path, buffalo-bill/vainabel/cainelias/chordz entries added, buffalo-bill listed in both moveset loaders.
- [OPEN] Megami + Menajerii have model keys + movesets on main (SmutBase PR #779) but NO FULL_ROSTER entries (verified 2026-10-23). Believed to be the active SmutBase lane's pipeline (their #774/#779 landed today; fighters 1–2 Ryusan/Tobi not yet landed) — CHECK OWNERSHIP before working; if that lane stalls, add the two entries in a wiring follow-up.
- [OPEN] Vain Abel Attire 1 Tripo (f7e90de8) is NOT in the repo (TRIPO-REGISTRY 2026-10-22: missing). Hunt releases + local worktrees; if found, land as roster/vainabel/attires/attire1 + repoint base key 'vainabel' to it (currently Attire 2 per PR #781). If nowhere, it needs a fresh pull via tools/tripo-pull from the owner's Tripo link — owner ask.
- [OPEN] Scimitar source GLB (roster/scimitar/attires/attire1/source/scimitar-a1.glb) still unwired (audit attires-unwired set; wave 1 left it out of scope). Rides wave 2.
- [OPEN] Stale shipped roster entry id 'ryuji' fails completeness (no ryuji.json) — documented KNOWN_GAPS item owned by the CornerStone lane; wave 1 fixed the model side only (key 'ryuji-rock' resolves). Do not duplicate; flag if that lane stalls.
- [DONE 2026-10-23, PR #766 merged 12:04Z, verified on main] OBSOLETE-IN-CANON rule in CANON-MASTER.md: rule doc docs/OBSOLETE-ORIGINALS-RULE.md on main (5,973B, incl. CHARACTER SELECT + ATTIRE LADDER section), banner on CANON-MASTER line 3, exactly 1 section notice needed (JIN, line 902 — every other original already appears only as a base mention inside its successor's section). Remaining: obsolete pointer files ride bios batch 2; JIN marking is the owner's open call (his 2026-10-19 naming law keeps the name 'Jin' in Eastern Mind canon + jin_soul in soul records).
- [BLOCKED] Tekken 6 motion extraction — DOES-NOT-EXIST. Blocked on decrypt6 encode-context crack (teardown-sweep lane owns the crack; decrypt6 sub-lane parked needs_owner since 2026-10-16 with no concrete decision ever recorded — restate the decision concretely or fold into sweep lane).
- [ACTIVE] TTT2 Phase 2 extraction — running, not stranded (reassembly parked by design behind disk gate).

## wrestling-game (11 open / 7 merged — ALL stranded, ALL mergeable, CI-blocked)
- [OPEN-PR] W5 Def Jam set in order: #14 → #15 → #16 → #17 (912 parts) → #18 (microcode negative result). Landing this unblocks the western-heart CATALOG wiring.
- [OPEN-PR] #9 No Mercy wrestlers (13 GLBs) — main models/ holds only WMXIX. Bannon #87 is its duplicate twin (close after this lands).
- [OPEN-PR] #13 teardown mirror (139 files) — Bannon #92 is its duplicate twin (close after this lands).
- [OPEN-PR] #10 render-orientation, #6 merge-it-yourself law, #11/#12 anti-clobber duplicate pair (land one).
- [BRANCH-ONLY] docs/sale-status-owner-rule-2026-10-14 (also in GRE + ConcreteDragon).
- [LOCAL-ONLY] ~/workspace/wrestling-work/ — 6 wrestling-move FBX + 6 JSON, never committed anywhere. Commit into wrestling-game.

## game-reverse-engineering (33 open / 11 merged — ALL stranded, ALL mergeable, CI-blocked)
- [OPEN-PR] SF EX phases in order: #42 → #43 → #44 → #45.
- [OPEN-PR] SCII stack: 10 PRs, stacked branches, phase-10 tip 144 commits ahead — land in phase order or verify the tip carries the stack.
- [OPEN-PR] 7 Tekken 5 lane PRs; 3 YYH PRs; W1 All Stars census #38; teardown research #29; #9; #7.
- [OPEN-PR] #10 RE tooling pull-in (905 files) — has −2 deletions; deletion-guard check BEFORE any merge.
- [OPEN-PR] #12/#13 anti-clobber duplicate pair (land one).
- [BRANCH-ONLY] feat/re-toolchain-research-20261016 (ahead 8); watchdog/tekken6-decrypt-callgraph-20261015 (ahead 4); docs/sale-status-owner-rule-2026-10-14.
- [BLOCKED] 7 orphan-history branches with no common ancestor to main (master, offload-push, push-clean, tekken-pull-verify-20261013, watchdog/doa4-download-fix, watchdog/wrestling-teardown-20261013, feat/ymg-skinning-decoder) — cannot PR normally; archive + owner deletion decision. NEVER delete without his per-item sign-off.

## Bannon (18 open / 70 merged)
- [OPEN-PR] Rig line: #77 rig-repair pipeline, #48 rig hardening.
- [OPEN-PR] Playable line: #49 Stick-Up v2 cinematic, #41 PWA-sync CI.
- [OPEN-PR] #84, #80, #88, #83.
- [BLOCKED] #39 reality audit + #38 grapple solver — CONFLICTING/DIRTY (#38 is the oldest substantive PR in the fleet, from Aug 4). Conflict work keeping both sides.
- [OPEN-PR] #89 anti-clobber — partially landed (main AGENTS.md has 1 mention); verify before landing.
- [BLOCKED-owner-held] #78 Stick Up HQ — DRAFT, owner-excluded, do not merge. #43/#44/#45 dormant drafts.
- [OPEN-PR] #22 "Aye" — 0 files, close candidate (owner call).

## ConcreteDragon (4 open / 56 merged — ALL blocked by branch protection)
- [BLOCKED] #62 Quantum Jam prep (jam ended Sep 28, nothing submitted) — owner decision: land as repo work or close.
- [BLOCKED] #59 render-orientation; #60/#61 anti-clobber pair.
- [BRANCH-ONLY] feature/customization-suite (11 ahead); content/waves-2-4 (4 ahead); weight-paint-pwa (3 ahead) + 5 more no-PR branches — PR them.
- [LOCAL-ONLY] itch staging ~/workspace/concrete-dragon-itch/ untouched since Oct 9 (money path — owner-manual payout setup is the real blocker).

## cape-jones (3 open / 207 merged — healthy)
- [BLOCKED-owner-held] #167 mesh-repair, #156/#157 sitting takes — the sitting choice is the owner's. Do not merge.
- 176 remote branches sample-verified contained in main (ahead_by=0) — hygiene debt only, not stranded work.

## agent-ops
- [OPEN] OBSOLETE-ORIGINALS handoff sections — edits staged this run (see merge-queue-sync PR below); flip to DONE when merged+verified.
- [DONE 2026-10-23, PR #40 merged 495fe68f, verified on main] Cross-repo stranded audit (this queue's seed source) — `CROSS-REPO-STRANDED-AUDIT-2026-10-23.md` (22,508 B) confirmed on main via contents API. Note: repo-wide CI outage (instruction-gate + no-deletion-guard failing on ALL branches since 2026-10-15; logs/check-runs unreadable with current token) — merged after direct verification of both gates' intents (gate-format body verified against the gate script locally; 0 deletions in diff).
- [DONE 2026-10-23, PR #29 merged 5030c9ba, verified on main] Owner-authored docs PR — was CONFLICTING since 2026-10-21; rebased keeping both sides (CLAIMS.md add/add resolved, main added no rows in the hunk). Payload verified on main: `RESEARCH-CONVENTIONS.md`, `adr-template.md`, `research-check.sh`, `tools/watermark-removal/remove_watermark.py` all present via contents API.
- [BLOCKED] Repo-wide CI outage: instruction-gate + no-deletion-guard fail on EVERY branch (81 failures vs 19 successes all-time; last success 2026-10-15). mergeable_state stays "unstable" for all PRs. Needs log access or a token with checks:read to diagnose; until then every merge needs the manual gate-intent verification done for #40/#29 above.

## FALSE CLAIMS REOPENED (verify-done sweep seeds)
- "Anti-clobber law propagated to 135/135 repos" — FALSE for wrestling-game, GRE, ConcreteDragon mains (0 mentions, contents-API verified 2026-10-23); partial in Bannon. Landed only in cape-jones + western-heart. Fix = item in the law/doc dedup landing order.
- "Def Jam 912/912 extracted + stored" — stored only as open-PR branches; on no main. (See wrestling-game W5 set.)
- "No Mercy extraction complete (2026-10-13)" — wrong-window set; see western-heart re-extraction item.
