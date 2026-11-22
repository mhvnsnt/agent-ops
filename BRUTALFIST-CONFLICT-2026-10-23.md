# BRUTAL-FIST conflict-resolution lane — 2026-10-23
Conflict work keeping BOTH sides of every conflict (anti-clobber law). Repo-wide CI quota-dead until 2026-11-01 — manual gate-intent verification pattern per MERGE-QUEUE.md.

- PR #10 (rocket-update, 08e8fbe): IN-PROGRESS — stopped by cron timeout mid-resolution. 28/29 conflicted files resolved (0 markers, staged, uncommitted); src/engine/pipeline/CharacterPipeline.ts still has all 25 conflict markers, resolution plan fully mapped but not applied. No push/merge done. Local state: ~/workspace/_conflict-work/brutal-fist/pr-10 on local branch pr-10 (from origin/rocket-update); plumbing merge-commit plan (merge-tree --write-tree, no sparse-checkout commit) documented in prior context. Resume: apply the 25-hunk resolution, fix hunk-22 call site + CharacterPortrait3D.tsx:7,179 to determineForwardCorrectionByCentroid, node --check the esbuild output, then plumbing-commit, push to rocket-update, gate-verify, merge.

## RESUME — 2026-10-23 ~19:50 CDT — PR #10 CONFLICT RESOLUTION COMPLETE, MERGED, VERIFIED ON MAIN

**Outcome: PR #10 (rocket-update → main) RESOLVED, MERGED, and VERIFIED ON MAIN.** ✅

### What was done this run
1. **Verified local state**: worktree `~/workspace/_conflict-work/brutal-fist/pr-10` (sparse), branch `pr-10` @ 08e8fbe (= origin/rocket-update). 25/25 conflict markers in `src/engine/pipeline/CharacterPipeline.ts`, 0 elsewhere; 26 unmerged index paths total.
2. **Resolved all 25 hunks keep-both-sides** (anti-clobber law — neither side dropped):
   - H1 FACING comment: merged (centroid law + shoulder-line note).
   - H2 imports: merged; the two `bindClipTracksToTargetBones` (Euler adapter takes `(clip, targetScene)`, AnimationRetargeter takes `(clip, boneNames)`) kept via alias `bindEulerClipTracksToTargetBones`.
   - H3 imports: merged (SEMANTIC_STATE_ALIASES + COMBAT_STATE_TO_SEMANTIC + PREFERRED_REQUIRED_SEMANTIC_STATES + FighterMotionBank fns).
   - H4/H8/H12/H13/H15–H21/H25: main-side additions kept verbatim (HEAD side empty or subsumed).
   - H5: kept BOTH `determineForwardCorrectionByCentroid` (HEAD) and `estimateRigForwardXZ`/`determineForwardCorrection` (main) as exports.
   - H6: HEAD's detailed per-mismatch console.error + bone snapshot, with main's 8-entry cap.
   - H7: HEAD's console.error FAILED gate + main's finger/toe note appended.
   - H9–H11: integrated pipeline — canonical `AnimationRetargeter` map first, then main's bind-relative ingest over the retargeted clips (fallback keeps the retargeted clip on bind miss); HEAD's preferred-state gap fill (Euler bank via aliased binder, procedural TEST_ONLY placeholder) + main's bind-relative bank ingest + `fillBindRelativeGaps`.
   - H14 (`void applyPSXShader`): dropped — param is used again by the restored PSX block.
   - H22 (floor snap): HEAD's AGENT-LAW comment + main's `plantFeetOnFloor` + finite guard.
   - H23 (STEP 11/12): `cloned.rotation.y = 0` + `forwardCorrectionY = determineForwardCorrectionByCentroid(cloned)` (geometry-centroid law) + `preserveAuthoredMaterials` + PSX vertex-snap block gated by `applyPSXShader` (main's "project_vertex hid meshes" kept as a documented caution).
   - H24: main's try/catch with `characterId = rosterIdFromModel(modelName) || <HEAD regex fallback>`.
   - CharacterPortrait3D.tsx:7,179 → `determineForwardCorrectionByCentroid` (matches the file's own "GEOMETRY CENTROID ONLY" comment).
3. **Fixed a real defect**: `src/engine/GameEngine.ts` had a duplicate `export { getMoveById as getMove }` (lines 11 & 19) from the earlier resolution — removed the duplicate + a stray `// ... Remove this block or line ...` comment.
4. **Syntax gate**: esbuild parse-clean on all touched TS/TSX (repo CI quota-dead until 2026-11-01, so manual gate-intent per MERGE-QUEUE.md).
5. **Sparse-worktree safety**: the 28 earlier-resolved files were edited but never `git add`ed — staged all 26 unmerged paths after a marker scan (0 markers tree-wide). Built the merge via plumbing (`write-tree` → verified 1006-file complete tree → `commit-tree -p 08e8fbe -p origin/main`); NO plain `git commit` in the sparse tree, no rebase/squash/force.
6. **Deletion guard**: ZERO deletions vs either parent. 728 adds vs HEAD (main-side files).
7. **Pushed** `pr-10` → `origin/rocket-update` (08e8fbe..798e674). PR #10 went CONFLICTING → MERGEABLE.
8. **Merged** via `gh pr merge --merge` (merge commit only). PR #10 state=MERGED at 2026-10-24T01:17:09Z.

### Verified on main (own-eyes, contents API)
- `origin/main` = `f6715c148b3248d406f146c0c405bf67730de246` (the PR #10 merge commit).
- `src/engine/pipeline/CharacterPipeline.ts` on main: 67,945 bytes, **0 conflict markers**, both forward detectors present.
- `src/components/CharacterPortrait3D.tsx` on main: imports + calls `determineForwardCorrectionByCentroid` (lines 7, 56, 179).
- `src/engine/GameEngine.ts` on main: exactly 1 `getMove` re-export.

### Notes / caveats
- The 25-hunk "resolution plan" from the prior lane's context was not visible to this run; resolutions were re-derived from the marker hunks per the anti-clobber law. The hunk-22/portrait note matched the geometry-centroid call-site decision.
- Draft PRs #22, #19, #17, #16, #13 untouched (owner-held). Only PR #10 merged.
- Local worktree `~/workspace/_conflict-work/brutal-fist/pr-10` left at the merge commit; backup of the pre-resolution file at `/tmp/CharacterPipeline.ts.bak` (ephemeral).
