# MERGE QUEUE — everything built but not landed, all repos

Rule: an item leaves this queue ONLY as LANDED-VERIFIED (payload confirmed on the repo's main by the checker) or OWNER-CLOSED. "Done" claims without main-verification do not count. Seeded 2026-10-23 from the cross-repo stranded audit (~/workspace/agent-ops/CROSS-REPO-STRANDED-AUDIT-2026-10-23.md, agent-ops PR #40) + main-agent verified counts. Western Heart fighter-content items land here when docs/CATCHUP-AUDIT-2026-10-23.md merges.
Canon-sync last run: 2026-10-23 ~17:00Z (overnight pipeline) — no new game canon in MEMORY.md/daily notes/handoffs since the 16:35Z sync; nothing to commit.
Overnight run 2026-10-23 ~16:42-17:15Z: landed-verified 1 (western-heart #462). New PRs: GRE #47 (tekken6 decrypt docs), CD #63/#64/#65 (branch-only → PR). Bannon #89 CLOSED as superseded (full 5-law anti-clobber already on main). Verify-sweep: 5 claims, all VERIFIED.
Overnight run 2026-10-23 ~15:10-16:35Z: landed-verified 27 (brutal-fist 8, western-heart 14 incl. #783 fix, wrestling-game 1, GRE 1, agent-ops 4). Previous stale run (13:37-14:49Z, never logged) merged wrestling-game #9-#19, GRE #20-#46, Bannon #77/#80/#83/#84/#88 — all confirmed merged via API + payload spot-checks this run.

## western-heart (112 open PRs / 759 branches / 89 releases at audit time)
- [DONE 2026-10-23, this run] Docs/research batch landed-verified: #778 (industry sweep), #777 (body morphing), #776 (customization research), #775 (morphing freedom), #773 (WWE 2K pull docs), #770 (parts & clothing spec), #769 (session docs), #760 (directives + canon gaps), #748 (Gyou Godflame). All MERGEABLE+CLEAN, zero deletions, payloads on main.
- [DONE 2026-10-23, this run] #733 chordz blade-transformation archive (3 GLBs + manifests + spec + owner-directives section) — conflict-resolved via Git Data API keeping both sides, merged, then #783 fixed a bad-blob (gh `-f content=@file` does NOT expand @file for blobs API; base64 explicitly). Directives verified 29320B with all sections on main.
- [DONE 2026-10-23, stale 13:37Z run] #766, #768, #771, #772, #774, #779, #780, #781 — merged 12:04-13:07Z, confirmed via API; #781 payloads spot-verified (obsolete ids absent from roster-full.js, CornerStone model.glb 18.8MB on main).
- [DONE 2026-10-23, this run] #462 Rig & Pose Studio — LANDED-VERIFIED (merge ec7d6645, 2026-10-23T16:58:04Z). Gate-format body applied (instruction-gate script verified locally, passes); diff +11138/-22, deletions are the PR's own doc-draft finalizations only. Payloads on main: DIAGNOSIS-2026-10-21.md, rigpose_bake.py, rigpose.js, star-after.json. FLAG: 3 committed .pyc files (customization/tools/__pycache__/ + tools/rig-pose-studio/__pycache__/) — follow-up: lane should gitignore *.pyc.
- [OPEN-PR] Urban Reign phase stack: #506/#518/#548 merged branch-to-branch 16:09Z (stack collapsed, nothing to main). Tip PR #784 (ur-phase6-bank-completion → main, 33 commits, 300 files) is CONFLICTING — tip based on 13f50c72, dozens of overlapping files (.github/, CANON.md, WORKLOG.md, customization/). Needs dedicated conflict lane. Phase payloads safe on branch.
- [OPEN] #464 Urban Reign phase 3 — EMPTY PR (0 files changed). Close candidate.
- [OPEN] Megami/Menajerii/Ryusan/Tobi (renamed parvati/vixen/mina-ashido/miruko per identity rules): model keys + movesets + canon on main, NO roster-full.js entries (verified 2026-10-23). SmutBase lane active today (#772/#779) — CHECK OWNERSHIP before wiring; lane not stalled.
- [BLOCKED] PR #497 — CONFLICTING; merging as-is regresses the #508 feet fix. Owning lane must rebase preserving #508.
- [BLOCKED] PR #498 — instruction-gate semantic fail (method used ≠ specified, deviations says none). Lane must correct.
- [OPEN-PR] PR #499 W3c AKI corrective — all 11 clips FAIL gate on true data, 0 rows; awaits AKI FK→T3 IK follow-on.
- [BLOCKED-owner-held] PR #377 — stays OPEN as evidence. Do not merge.
- [OPEN-PR] PR #462 Rig & Pose Studio — merge when CLEAN.
- [BLOCKED] No Mercy true-window re-extraction program — NOT RUN. All NM-derived assets on main are wrong-window (PR #505 audit). Correct re-extraction exists nowhere.
- [UNBLOCKED 2026-10-23] Def Jam converter + CATALOG.json wiring — was NEVER RUN, gated on the wrestling-game W5 set. The W5 set (#14→#18) ALL LANDED-VERIFIED on wrestling-game main 2026-10-23. The wiring lane can now run: convert the landed models + wire CATALOG.json.
- [OPEN] Vain Abel Attire 1 Tripo (f7e90de8) is NOT in the repo (TRIPO-REGISTRY 2026-10-22: missing). Hunt releases + local worktrees; if found, land as roster/vainabel/attires/attire1 + repoint base key 'vainabel' to it (currently Attire 2 per PR #781). If nowhere, it needs a fresh pull via tools/tripo-pull from the owner's Tripo link — owner ask.
- [OPEN] Scimitar source GLB (roster/scimitar/attires/attire1/source/scimitar-a1.glb) still unwired (audit attires-unwired set; wave 1 left it out of scope). Rides wave 2.
- [OPEN] Stale shipped roster entry id 'ryuji' fails completeness (no ryuji.json) — documented KNOWN_GAPS item owned by the CornerStone lane; wave 1 fixed the model side only (key 'ryuji-rock' resolves). Do not duplicate; flag if that lane stalls.
- [BLOCKED] Tekken 6 motion extraction — DOES-NOT-EXIST. Blocked on decrypt6 encode-context crack (teardown-sweep lane owns the crack; decrypt6 sub-lane parked needs_owner since 2026-10-16 with no concrete decision ever recorded — restate the decision concretely or fold into sweep lane).
- [ACTIVE] TTT2 Phase 2 extraction — running, not stranded (reassembly parked by design behind disk gate).

## wrestling-game (was 11 open / 7 merged at audit — backlog cleared 2026-10-23)
- [DONE 2026-10-23, stale 13:37Z run] #9 (No Mercy 13 GLBs — payload spot-verified models/wwf-no-mercy/ on main), #10 (render-orientation), #11/#12 (anti-clobber pair), #13 (teardown mirror), #14→#18 (W5 Def Jam set), #19 (local-only FBX landing). All merged 13:07-14:49Z, confirmed via API.
- [DONE 2026-10-23, this run] #6 MERGE-IT-YOURSELF LAW — merged 15:43Z, AGENTS.md verified on main.
- [OPEN] None. Queue clear for wrestling-game.

## game-reverse-engineering (33 open / 11 merged at audit — backlog cleared 2026-10-23)
- [DONE 2026-10-23, stale 13:37Z run] SF EX stack #42/#43/#45, SCII stack (#26/#28/#40 + phases), Tekken 5 lanes #20-#27, YYH lanes #35/#39/#41/#46, research #29, census #38 — all merged 13:55-14:12Z, confirmed via API.
- [DONE 2026-10-23, this run] #10 RE tooling pull-in (905 files) — merged 15:43Z after deletion-guard check (2 deletions were 0-byte dead gitlinks wwf-no-mercy/re-docs + recomp, superseded by real docs/ + tools/ dirs). wwf-no-mercy/tools/ verified on main (7 entries).
- [OPEN-PR] #47 tekken6 decrypt callgraph + corrections docs (opened 2026-10-23 this run, branch watchdog/tekken6-decrypt-callgraph-20261015) — 3 added docs + NO-SWEEP-INFLIGHT law + TEARDOWN-STATUS sync, add-only. CONFLICTING on open (branch behind main); conflict resolve in progress this run, keeping both sides.
- [BLOCKED] feat/re-toolchain-research-20261016 (ahead 8, diverged) — CANNOT PR as-is: unexplained deletions of other lanes' files (soulcalibur/TEARDOWN.md, soulcalibur/XBOX-EXTRACTION-REPORT.md, soulcalibur/xbox-extract/* (6 files), tekken-tag-tournament-2/HEADER-LISTING.txt, tekken-tag-tournament-2/tools/{god_surgical,stfs_blobs,xdvdfs_reader}.py + pycache). Prior PR #8 was CLOSED unmerged. Owning lane must split: add-only PR (docs/toolchains/* + AGENTS.md/TEARDOWN-STATUS.md edits) vs confirmed-by-owner deletions. Do NOT merge with deletions intact.
- [STALE] docs/sale-status-owner-rule-2026-10-14 — content already on main (docs/RULES.md 7 lines, byte-identical to the branch commit; PR #2 MERGED). Nothing to PR; branch is hygiene debt.
- [OPEN] None other. Queue clear for game-reverse-engineering. (Note: 7 orphan-history branches still cannot PR normally — archive + owner deletion decision; NEVER delete without his per-item sign-off.)
- [BRANCH-ONLY] feat/re-toolchain-research-20261016 (ahead 8); watchdog/tekken6-decrypt-callgraph-20261015 (ahead 4); docs/sale-status-owner-rule-2026-10-14.

## Bannon (18 open / 70 merged at audit)
- [DONE 2026-10-23, stale 13:37Z run] #77 (rig-repair pipeline — tools/rig-repair/ 16 entries verified on main), #80, #83, #84, #88 — merged 14:14Z, confirmed via API. #48/#49/#41 already MERGED (earlier).
- [CLOSED-superseded 2026-10-23, this run] #89 anti-clobber — payload verified on main and SUPERSEDED: main AGENTS.md already carries the FULL 5-law version (DELETION CHECK, OWN THE TREE, CIRCUIT BREAKER, SAY THE DELETIONS, MERGE GATE), which is newer and a superset of #89's 7-line stub. Closed with comment; no merge needed. (verify-then-land item resolved.)
- [BLOCKED-owner-held] #78 Stick Up HQ — DRAFT, owner-excluded, do not merge. #43/#44/#45 dormant drafts.
- [BLOCKED] #39 reality audit + #38 grapple solver — CONFLICTING/DIRTY (#38 is the oldest substantive PR in the fleet, from Aug 4). Conflict work keeping both sides.
- [OPEN] #22 "Aye" — 0 files, MERGEABLE. Close candidate (owner call).

## brutal-fist
- [DONE 2026-10-23, this run — all verified on main] #36 anti-clobber law, #35 render-orientation + tpose tools, #32 merge-it-yourself law (conflict-resolved keeping both laws), #31 Producerbot runbook, #30 no-data-loss rules + deletion guard (conflict-resolved keeping all three laws), #28 CI submodule fix (2 explained deletions), #33 universal rig standard (full doc), #34 rig standard-2 + runner (doc merged with #33's, run.sh landed). Combined UNIVERSAL-RIG-STANDARD.md (8939B) + tools/rig/run.sh on main.
- [BLOCKED-draft] #22, #19, #17, #13 — all DRAFTS, mergeable but unmergeable without owner word. Do not merge.
- [BLOCKED] 6 CONFLICTING PRs: #21, #20, #18, #16, #12, #11, #10. Conflict work keeping both sides.
- Watch: CI is quota-dead repo-wide until 2026-11-01; merge mergeable after hand-verifying gate intent + zero unexplained deletions.

## ConcreteDragon (4 open / 56 merged — ALL blocked by branch protection)
- [OPEN-PR 2026-10-23, this run] #63 customization-suite (feature/customization-suite → main) — CUSTOMIZER_SUITE_CD.md + game-3d/main.js + template.html wiring, add/modify only.
- [OPEN-PR 2026-10-23, this run] #64 weight-paint-pwa (→ main) — tools/watermark-removal/{remove_watermark.py, wm_template_left.png, wm_template_right.png}, add-only.
- [OPEN-PR 2026-10-23, this run] #65 content waves 2-4 (content/waves-2-4 → main) — wiring/anatomy/audit docs + Kenney CC0 asset staging, add/modify only.
- [BLOCKED] #62 Quantum Jam prep (jam ended Sep 28, nothing submitted) — owner decision: land as repo work or close.
- [BLOCKED] #59 render-orientation; #60/#61 anti-clobber pair.
- [BRANCH-ONLY] + 5 more no-PR branches (beyond the three PR'd above) — check and PR them.
- [LOCAL-ONLY] itch staging ~/workspace/concrete-dragon-itch/ untouched since Oct 9 (money path — owner-manual payout setup is the real blocker).

## cape-jones (3 open / 207 merged — healthy)
- [DONE 2026-10-23] #167 mesh-repair — MERGED 11:59Z (queue entry was stale listing it owner-held; verified merged on main by verify-sweep).
- [DONE 2026-10-23] #219 recliner spec — merged 13:34Z from sparse checkout, WIPED 21 root entries from main; recovered via #220 (merged 15:24Z), payload + full tree verified on main this run. NO-SPARSE-COMMIT LAW written (~/AGENTS.md + agent-ops #43 merged).
- [FLAG] #168 merged with production/tools/auto-seat/proof_sitting.blend (97.1MB) on main — violates the >50MB repo-binary rule. Needs a follow-up (move to release asset); do NOT delete from history without owner word.
- 176 remote branches sample-verified contained in main (ahead_by=0) — hygiene debt only, not stranded work.
- [BLOCKED-owner-held] #156/#157 sitting takes — CLOSED as superseded (rejected takes → PR #159 + placed scenes).

## agent-ops
- [DONE 2026-10-23, this run — all verified on main] #27 MERGE-IT-YOURSELF LAW (docs-only), #31 ANTI-CLOBBER LAW, #32 ANTI-CLOBBER LAWS, #43 NO-SPARSE-COMMIT LAW. Merged during CI outage after manual gate-intent verification (docs-only label → instruction-gate passes; 0 file deletions → no-deletion-guard passes).
- [DONE 2026-10-23] #42, #40, #29, #25 — merged by earlier runs, confirmed via API.
- [OPEN] NO-SPARSE-COMMIT LAW propagation: law is in ~/AGENTS.md (injected context) + agent-ops AGENTS.md (#43). NOT yet in western-heart, cape-jones, Bannon, brutal-fist, wrestling-game, GRE, ConcreteDragon AGENTS.md copies. Queue the propagation (same pattern as the anti-clobber 135-repo push).
- [BLOCKED] Repo-wide CI outage: instruction-gate + no-deletion-guard fail on EVERY branch (81 failures vs 19 successes all-time; last success 2026-10-15). mergeable_state stays "unstable" for all PRs. Needs log access or a token with checks:read to diagnose; until then every merge needs the manual gate-intent verification done for #40/#29/#27/#31/#32/#43 above.

## FALSE CLAIMS REOPENED (verify-done sweep seeds)
- "Anti-clobber law propagated to 135/135 repos" — FALSE for wrestling-game, GRE, ConcreteDragon mains (0 mentions, contents-API verified 2026-10-23); partial in Bannon. Landed only in cape-jones + western-heart. Fix = item in the law/doc dedup landing order.
- "Def Jam 912/912 extracted + stored" — stored only as open-PR branches; on no main. (See wrestling-game W5 set.)
- "No Mercy extraction complete (2026-10-13)" — wrong-window set; see western-heart re-extraction item.
- [SWEEP 2026-10-23 ~17:05Z] 5 claims sampled (checkpoints + daily notes + handoff): 5 VERIFIED, 0 FALSE. cape-jones #219/#220 (RECLINER-MECHANISM-2026-10-23.md 1673B + 22 root entries on main); western-heart #781 (roster/ryuji-rock/attires/attire1/model.glb 18,872,720 B on main); agent-ops #27 (docs/MERGE-IT-YOURSELF-LAW.md 1222B on main — queue note's "AGENTS.md" path was wrong, corrected), #31/#32/#43 (ANTI-CLOBBER LAWS + NO-SPARSE-COMMIT LAW headers in AGENTS.md on main); GRE #10 (wwf-no-mercy/tools/ 7 entries on main); Bannon #77 (tools/rig-repair/ 16 entries on main).
- [SWEEP 2026-10-23 ~15:30Z] 9 claims sampled (checkpoints + daily notes + handoff): 9 VERIFIED, 0 FALSE. Flags: (1) cape-jones #167 queue entry was stale (merged 11:59Z) — fixed above; (2) #168's ".blend blocker resolved" claim wrong — 97.1MB proof_sitting.blend IS on main (flagged above); (3) GitHub contents API transient 404s — retry before declaring FALSE; (4) #572 file is rows.pack.json not rows.paca.json (naming wrinkle only).
