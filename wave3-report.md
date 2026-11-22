# LANDING WAVE 3 — MOVESETS — FINAL REPORT (2026-10-23 CDT)

**Status: ALL WORK COMPLETE. PR #944 fully green. MERGE HELD — main was clobbered by PR #498's merge while #944 was in CI. Do not merge #944 until main is restored (evidence + recovery pointer below).**

## Per-fighter outcomes

### 1. GASHADOKURO (base Kuma) — COMPLETE
- New file `game/assets/movesets/gashadokuro.json` — **530 moves / 108 strings / 24 specials, 526,649 bytes**, schema v2.
- Built from the shipped `t3-kuma.json` (decoded T3 Kuma bank + T7/T8 Kuma merges) per the repo's successor pattern (charger/mariposa/buffalo-bill): every move programmatically verified **identical to source except the name prefix** — 316 generated "KUMA ..." names re-prefixed "GASHADOKURO ..."; strings/specials/slots/hit_words/stance_after identical. proxy=false (the bank IS his recorded base). canon_note/replaces/source_moveset fields record the succession (Kuma obsolete per owner law 2026-10-23, roster/kuma/CANON.md).
- Wiring: MOVESET_IDS + index.json entry (moves 530, inputs 270) + FULL_ROSTER entry `{ id: 'gashadokuro', moveset: 'gashadokuro', model: 'gashadokuro' }` (model key was wired wave 1). **No kuma roster entry, no kuma key.**
- Portrait: captured with `tools/portraits/capture.mjs` (attire-1 static, bank 'kuma' bound via fighter.js FIGHTER_BANK). He is a 0-bone unrigged static (wave-2 rig failed its own-eyes gate — long unboned appendage class, record in PR #837), so he is honestly listed in `tools/portraits/POSE-BLOCKERS.json`, same visible-debt class as cainelias/kingtyrant/star. Portrait PNG viewed by me: the tool's unrigged-bounds framing of his spiked shoulder/back ornament (declared in the blocker entry + PR body).

### 2. AOTSUKI (base Panda) — COMPLETE
- New file `game/assets/movesets/aotsuki.json` — **530 moves / 108 strings / 24 specials, 525,503 bytes**, schema v2.
- Same T3 bear bank: in Tekken 3 Panda shares Kuma's motion bank and the teardown holds no separate panda bank, so the file is honestly flagged **proxy=true** with that note in-file (anim refs stay t3:kuma). Move data verified identical to source except 316 names re-prefixed "AOTSUKI ...".
- Wiring: MOVESET_IDS + index.json entry + FULL_ROSTER entry (model key 'aotsuki' rides the wave-2 rigged build). **No panda roster entry.**
- Portrait: captured, 73 bones, kuma bank stance applied (cmu-14_01 aim fallback — same stanceSource as chatur/menajerii), framed head-and-shoulders, viewed by me: blue aquatic humanoid, textured, clean.

### 3. SILVERTONGUE (base Lili, re-owned) — COMPLETE
- New file `game/assets/movesets/silvertongue.json` — **508 moves / 42 strings / 13 specials, 426,505 bytes**, schema v2.
- Built from the shipped `lili.json` (T3-bank-generated base + T7/T8 Lili merges, including her WH signature moves "Curtsy" and "Kiss Like a Slap"); every move verified identical except 271 generated "LILI ..." names re-prefixed "SILVERTONGUE ...". Authored as her own file per the brief (Lili bank is the animation source; the file is hers).
- Wiring: MOVESET_IDS + index.json entry + FULL_ROSTER entry. **Brief-premise correction:** the brief said her FULL_ROSTER entry already existed — verification against main showed it did NOT (she had model keys, attires, canon, but no select entry). The entry was added in this PR under the catch-up audit's standing landing order (entries land as pieces complete); declared in the PR body Deviations (#765).
- Portrait: captured, 73 bones, xiaoyu bank stance applied (cmu-14_01), viewed by me: textured head-and-shoulders in guard stance (the thin lines at frame-left are her source mesh's blade island riding the Head bone — a wave-2 declared quirk of the model itself).

### Scope check — remaining audit-12
The audit's 12 moveset-missing fighters resolve as: gashadokuro/aotsuki/silvertongue (this PR); jin excluded by design (folded into Demonio); zafina excluded (Mariposa's id carries hers); bonus excluded (no model — entry waits); the SmutBase six (chatur, pond, megami, menajerii, ryusan, tobi) are the other lane's and were NOT touched — they have since landed their own files/ids. **No fighter in scope was left incomplete.**

## PR and verification
- **PR #944** — https://github.com/mhvnsnt/western-heart/pull/944 — branch `wave3/movesets-gashadokuro-aotsuki-silvertongue-20261023`, head **e842bb2b** (commits 0e8b5583 + e842bb2b, built via Git Data API on the last-good main base 237857ce; no sparse-checkout commits).
- Diff: 12 files, all additive except two 1-line-class edits (movesets.js/roster-full.js/index.json/fighter.js appends; POSE-BLOCKERS +1 entry). Files: 3 moveset JSONs, index.json (125 → 128 fighters), game/js/movesets.js, game/js/roster-full.js (55 → 58 entries), game/js/fighter.js (FIGHTER_BANK bindings, the chatur/dorowani/menajerii pattern — needed because the portrait-capture path resolves banks without the moveset index loaded), 3 portrait PNGs, portraits-manifest.json (+3 entries, purely additive), POSE-BLOCKERS.json (+gashadokuro).
- **All 10 CI checks PASS** at head e842bb2b: canon-names, clobber-guard, deletion-guard, game-unit-tests, guard, instruction-gate, material-gate, menu-touch-e2e, rig-guard, ui-sources. (First submission failed game-unit-tests on the portraits gate; the second commit is the portrait-gate fix described above. The full test/*.test.mjs suite also passes locally against the PR tree: anim-gate 374/0, portraits PASS at 5 blockers, no-wrong-body 58 OK, fighter-completeness 4/4.)
- Payload byte sizes verified on the branch blobs (== the sizes that will land): gashadokuro.json 526,649 B (blob 5f8eebcc), aotsuki.json 525,503 B (99236617), silvertongue.json 426,505 B (fd5a4644), portraits 111,170 / 92,263 / 97,850 B.

## MERGE HOLD — main clobbered by PR #498 (needs parent/owner attention)
While #944 was in CI, main regressed:
- Last good main: **4757df4d** (merge of #701) — roster-full.js 31,500 B, all 2026-10-23 wiring present.
- **32495cfc** ("Merge main into fix/pantera-weights-20261021 — keep both sides") replaced roster-full.js with the #498 branch's old 25,602 B version.
- **a4683846** (merge of PR #498) carried it into main. Compare 4757df4d...a4683846: 300 files listed (API cap) — **269 removed, 31 modified** — including `.github/workflows/*`, `.github/scripts/clobber_guard.py`, `tools/` (80 → 41 top-level entries; tools/portraits gone), `game/assets/portraits/` (69 → 54 entries; portraits-manifest.json deleted), `game/js/movesets.js` 35,578 → 25,276 B (SmutBase + wave-1 ids gone), `game/assets/movesets/index.json` 21,495 → 16,459 B.
- Recovery pointer: everything exists at 4757df4d; a revert of a4683846 (or equivalent restore) recovers main. This lane did NOT attempt the restore (other lanes are actively merging; a fleet-level recovery is the coordinator's call).
- A HOLD comment with this evidence is posted on PR #944. Once main is restored: forward-merge main into the branch (my files were built on the last-good base; the only expected overlaps are the 4 shared files, all anchor-append edits), re-run checks, merge, then verify the 12 payloads' byte sizes on main and update this report.
- Note: merging #944 after restoration also restores `game/assets/portraits/portraits-manifest.json` and `tools/portraits/POSE-BLOCKERS.json` + `tools/portraits/capture.mjs` is NOT in #944's diff (it was only deleted on main, never touched by the branch — a main-side restore must bring it back; if the restore is a revert of a4683846 it comes back with everything else).

## No playability claims
Movesets + wiring + portraits landing is not a playtest verdict. The owner's playtest gate still requires the main agent's own harness playtest after the landing waves complete.

## Workdir
`~/workspace/wave3-work/` — generators (gen_wave3.py, gen_edits.py), PR body, reference pulls, local sparse capture checkout (`wh/`, ~1.4 GB, safe to delete — everything of value is on PR #944's branch), playwright node_modules (`pwnode/`).

## LANDING (2026-10-24, by landing lane after main restore)

- **Forward-merge:** main (then at 5c499626, incl. the 37976b5c revert of PR #498 plus PR #954) merged into branch `wave3/movesets-gashadokuro-aotsuki-silvertongue-20261023` via the update-branch API — new head **73eb88c0**, zero conflicts (both sides intact).
- **Checks:** all 10 PASS on 73eb88c0 (canon-names, clobber-guard, deletion-guard, game-unit-tests, guard, instruction-gate, material-gate, menu-touch-e2e, rig-guard, ui-sources). Long runner-queue waits (~45 min queued), no content failures, no fixes needed.
- **Merge:** PR #944 MERGED 2026-10-24T01:34:41Z, merge commit **ec3d50e9cf851564a629ade96132fed3b9f6c638** (merge commit, no rebase/squash). Verified: ec3d50e9 == current main head (compare: identical).
- **Payloads verified on main at ec3d50e9 (contents API, byte sizes):**
  - `game/assets/movesets/gashadokuro.json` — 526,649 B ✓ (exact expected)
  - `game/assets/movesets/aotsuki.json` — 525,503 B ✓ (exact expected)
  - `game/assets/movesets/silvertongue.json` — 426,505 B ✓ (exact expected)
  - `game/assets/movesets/index.json` — 21,970 B; contains gashadokuro ×1, aotsuki ×1, silvertongue ×1
  - `game/assets/portraits/gashadokuro.png` — 111,170 B
  - `game/assets/portraits/aotsuki.png` — 92,263 B
  - `game/assets/portraits/silvertongue.png` — 97,850 B
  - `game/assets/portraits/portraits-manifest.json` — 12,753 B
  - `game/js/fighter.js` — 86,742 B
  - `game/js/movesets.js` — 36,067 B; contains gashadokuro ×2, aotsuki ×2, silvertongue ×2
  - `game/js/roster-full.js` — 33,450 B; contains gashadokuro ×2, aotsuki ×2, silvertongue ×3; roster-id scan for kuma/panda/zafina/jin entries: **none found** (obsolete-originals law held)
  - `tools/portraits/POSE-BLOCKERS.json` — 1,198 B
- **Not touched:** PR #498 / its branch (payload re-land is a separate queue item). No other PRs merged. No playability claims.
