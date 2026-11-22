# Render Seen-List (dedupe: never render twice)

**Owner law 2026-10-16 ~02:31 EDT:** STOP rendering models he's already seen. Render ALL unseen models. Maintain this list.

## SEEN (front renders delivered + eyes-verified 2026-10-16)

Tripo recoveries (renders at `~/workspace/forge3d-pipeline/track1-tripo-recovery/work/renders/`):
- [x] waterfall_attire_1 (Waterfall MAIN attire)
- [x] saku_ra (Saku Ra MAIN attire)
- [x] purple_rain (Purple rain MAIN attire)
- [x] kiko_tanaka (Kiko Tanaka MAIN, hooded/robed)
- [x] kiko_tanaka_unrobed (Kiko Tanaka SECOND, unrobed)
- [x] cape_jones (Cyborg X fighter, "Cape Jones" attire)
- [x] fantasy_warrior_3d_model (Thor)

Western-heart tpose-refs (committed, own-eyes verified — front+side, white bg):
- [x] awa-pop, doc-frank, dxmmii, king-tyrant, kinpo, n3g4tiv0, nightwolf, phantom, purple-rain, rave, saku-ra, sam-ur-a1, skull, thor, waterfall, zui

Render-lane 2026-10-16 (front 2048px, white void, eyes-QC'd limb-by-limb; at `~/workspace/render-lane/outputs_teardown/`):
- [x] T7 King (rigmodels FBX, t-posed)
- [x] T7 Asuka Kazama (asuka-alt FBX, t-posed)
- [x] T7 Eddy Gordo (capoeira FBX, t-posed)
- [x] T7 Steve Fox (steve-fox-alt FBX, t-posed)
- [x] T7 Ling Xiaoyu (pink-dress FBX, t-posed)
- [x] T7 Armor King (whitemagesunny FBX, t-posed; heterochromatic eyes are source design)
- [x] No Mercy Kevin Nash, Kurt Angle, Rhino, Rob Van Dam, Scott Hall, Shawn Michaels (x2 attires), Stephanie McMahon, Steve Austin, The Rock (x3 attires), Triple H (13 GLBs, authoring pose)

Render-lane 2026-10-16 (front 2048px, white void, eyes-QC'd; at `~/workspace/render-lane/outputs_game/`):
- [x] baek, lili, zafina, zen-body (textured, t-posed)
- [x] demonio (= rin-body = steve-fox.glb, byte-identical trio — rendered once)
- [x] jin (was authored lying down; stood upright via rigid -90° X rotation)
- [x] kai-body (hair texture is 0x0 in source → honest gray, not pink)
- [x] pantera, pantera_fixed (textured, t-posed)
- [x] king-tyrant_alt1, kinpo_alt1, pantera-body (= pantera_alt1 dup), saku-ra_alt1, zui_alt2 (untextured in source → gray clay fallback renders)

Byte-identical DUPES skipped (never render twice):
- jin-body.glb = phantom.glb (seen) | retsu-body.glb = skull.glb (seen) | sha-body.glb = saku-ra.glb (seen) | sam-ur-a1-body.glb = sam-ur-a1.glb (seen)
- pantera_alt1.glb = pantera-body.glb (rendered once as pantera-body)
- demonio.glb = rin-body.glb = steve-fox.glb (rendered once as demonio)

## TO DEDUPE (remaining) — ALL DONE 2026-10-16

- [x] game/assets/models/ 36 files — 16 had tpose-refs renders (seen), 15 unique unseen rendered, 5 skipped as byte-dupes of seen. NOTHING left unseen.
- [x] T7 teardown: King, Asuka, Eddy Gordo, Steve Fox, Xiaoyu, Armor King — rendered.
- [x] No Mercy: 10 wrestlers (13 GLBs) — rendered (even though moving to XIX repo).

Open questions for coordinator/owner:
- T7 King S2 variant (`t8-king-s2-whitemagesunny/Raw Files/King S2.fbx`, 29.5k verts) — genuinely different model, NOT rendered (not in the 16). Render it?
- king_joined.glb (GLB of rigmodels King) — same as rendered King FBX, skipped as dup.

## Rules
- Add every model here the moment its render is delivered to the owner.
- "Seen" = a front-facing render reached the owner. A render that exists but was never shown does NOT count.
- When in doubt, check with the coordinator — don't guess, don't double-render.

## Lane-overlap note (2026-10-16 ~04:06 EDT, coordinator ruling)
- The pull-rest lane renders verification shots into `~/workspace/pull-rest/verified/` + `docs/pull-rest/` PRs as part of ITS pipeline. Those are NOT owner deliverables — they do NOT count as "seen" for this list.
- 4 models have renders in BOTH lanes: baek, lili, zafina, Ling Xiaoyu (T7). The render-lane versions (2048px, T-pose, full-arm-reach, white-void, eyes-QC'd for his customize→Tripo workflow) are the workflow deliverables and stand. Do NOT render a third copy of these — if a re-render is ever needed, reuse the render-lane outputs.
- Going forward: lanes render independently (different purpose, different specs), but check this note + the other lane's `verified/` folder before rendering to avoid a third copy.

## Delivered 2026-10-20 ~21:2x CDT (main chat, own-eyes verified by coordinator)
- [x] dio (Akuma community rip, game/assets/models/dio.glb) — clean textured front T-pose delivered. Colorway is as-found on the rip: mint-green pants + dark hair (alt colorway vs classic red topknot/indigo). Owner direction noted: Dio → classic Japanese demon / JoJo oni-yokai look via his Gemini pass.
- [x] diablo CURRENT model (game/assets/models/diablo.glb) — front T-pose delivered AS STATE EVIDENCE: it is the gtainside GTA Heihachi conversion, texture smeared brown across the whole body (same class as the pull-rest FAIL verdict). NOT a usable Gemini ref. Replacement (clean T7 Heihachi pull + render) dispatched 2026-10-20.
- NOT delivered (withheld under no-untextured rule): michiko + torch + yukihyo repo renders are gray clay; bruno repo render has a blank featureless face. Texture/face investigation + re-renders folded into the newer-models lane 2026-10-20.

## Newer-models lane 2026-10-20 (front renders, own-eyes verified, in ~/workspace/your_files/)
- [x] armor-king-guest_front_20261020 (GUEST Armor King, roster/armor-king/attires/attire1 Sketchfab rip — textured, rest-pose T, no skeleton) — DONE
- [x] bruno_front_20261020 (Bruno/Miguel T7 — FIXED: head textures recovered from miguel-t7-sfmlab.zip source VTFs; face/hair/eyes now render; replaces the blank-face repo render) + bruno_face-closeup_20261020 — DONE
- [x] negan-n3g4tiv0_face-closeup_20261020 + face-zoom (EVIDENCE, not a T-pose: pink patch = saturated pink baked into the Eyes texture edges + Face texture eyelid bands; beard white in Workbench = hair-card alpha artifact, not a defect)
- [x] yukihyo_front_20261020 (Yukihyō — FIXED: repo GLB was texture-stripped; its own diffuse set recovered from the T8 Armor King "Battle Cloth" (whitemagesunny) pack in tekken7-full-v1 and re-injected by material name; jaguar head + heterochromia render correct. PROVENANCE: this model is the T8 Battle Cloth Armor King, NOT a T7 rip — same model as the render-lane's "T7 Armor King" entry above. Pose note: arm skin rides ADR twist bones off the deltoid branch; fixed skeleton-only by rotating that branch by the arm's rest→posed delta, single application) — DONE 2026-10-21

## Diablo Attire 1 Tripo lane 2026-10-20 (front render, own-eyes verified)
- [x] diablo A1 "Fantasy Demon" (Tripo aee46f6a, owner's own build) — front T-pose render `docs/tpose-refs/diablo/a1_front.png` in western-heart PR #412 (Workbench textured, white void). Oni Heihachi: long silver wing-hair, two short horns, irezumi-tattooed chest/arms, purple dragon hakama. Textures CLEAN — this is the render the main chat shows the owner; the model replaces the smeared gtainside Heihachi conversion as Diablo's main attire (conversion ladders back, not deleted). Back render also made (orientation proof, scratch only).

## Diablo Attire 2 "Devil God" Tripo lane 2026-10-20 (front render, own-eyes verified)
- [x] diablo A2 "Devil God" (Tripo 9b096022, owner's own build) — front render `docs/tpose-refs/diablo/a2_front.png` in western-heart (PR #419, merged 2026-10-21). Oni figure: snarling horned face, wild white hair, irezumi-tattooed bare torso, dark hakama with rope belt; the long white/grey Hagoromo drapery swirls around him forming the Raijin Taiko Drum Ring circle behind his back. Textures CLEAN, no smear, no clay. Delivered at 512px (hi-res renders died under VM RAM pressure from parallel lanes; drum/Mitsudomoe details read at silhouette level, not emblem level) — hi-res re-render is an open follow-up. Model wired as Attire 2: `roster/diablo/attires/attire2/model.glb`, MODEL_URLS `diablo-attire2`.

## Vain Abel Attire 3 lane 2026-10-20 (front render, own-eyes verified)
- [x] vainabel A3 "Masked Demon of the Purple Haze" (Tripo 0bb4c6da, owner's link) — front T-pose render `docs/tpose-refs/vainabel/a3_front.png` in western-heart (this lane's PR; Cycles 2048, white void, margins 110/110/147/147). Black mask with purple stripes over bald head, perforated muzzle, diagonal stitched torso scar, dog tags, purple-flame pants/boots. Textures CLEAN. Facing quirk: this Tripo imports facing +X (repo tool front pass needs a 180° prep rotation of the render copy). Ear note: mask straps cross the ear area; small ear forms faintly visible under/behind straps in profile — NOT cleanly removed like his A1 edit; flagged to owner.

## Kinpo Attire 2 "Goth Sport" Tripo lane 2026-10-20 (front render, own-eyes verified)
- [x] kinpo A2 "Goth Sport" (Tripo 4f3eb502, owner's own build) — front T-pose render `docs/tpose-refs/kinpo/a2_front.png` in western-heart (PR #422). Goth makeup reads clearly (pale face, black lips, dark eye makeup), black twin-tails with green ties, black sleeveless top, SAME pleated mini skirt as Attire 1 with green trim, no jacket, very thick muscular thighs, fingerless gloves, knee socks. Textures CLEAN, no smear, no clay. Delivered at 512px Cycles (two 1024px attempts OOM-killed under VM RAM pressure from parallel rig lanes) — 1024px re-render is an open follow-up. Facing quirk: this Tripo imports Y-up in Blender (front = +X view; render copy rotated upright in post). Model wired as Attire 2: `roster/kinpo/attires/attire2/model.glb`, MODEL_URLS `kinpo-attire2`. Rig specs (enhanced jiggle butt/thighs/hips + M-rated anatomy rig requirement) recorded in `roster/kinpo/RIG-NOTES.md`.

## Kinpo Attire 1 Tripo lane 2026-10-20 (front render, own-eyes verified)
- [x] kinpo A1 (Tripo 2cb681d2, owner's own build) — front T-pose render `docs/tpose-refs/kinpo/a1_front.png` in western-heart (PR #436, MERGED). Black twin pigtails with yellow buttercup clips, green cropped jacket with floral embroidery, black crop top with green heart + yellow buttercup emblem, black pleated MINI SKIRT with green garter straps, very thick muscular thighs, green patterned knee boots. Textures CLEAN, no smear, no clay. Delivered at 768px Workbench (Blender via the vendored EGL stack + XDG_RUNTIME_DIR=/tmp; RAM-gated for hours behind parallel rig lanes — two attempts died on missing-EGL/Wayland env, one OOM at gate-open 2.0GB). Facing: front = +X view, same as A2. Model wired as Attire 1 (MAIN): `roster/kinpo/attires/attire1/model.glb` (20,304,060 B, sha256 ec67f8f0ddd57e97a915cc85408df08956dcc8bfddfe982698261f03fb6a155f), MODEL_URLS `kinpo` + `kinpo-attire1`; previous A1 laddered back as `kinpo-legacy` (NOT deleted). Jiggle spec (butt + thighs + hips, owner verbatim) recorded in `roster/kinpo/RIG-NOTES.md`. Original backed up in release `kinpo-tripo-pulls-20261020`.

## Vain Abel Attire 2 lane 2026-10-20 (front render, own-eyes verified)
- [x] vainabel A2 (Tripo 68a17c55 "wrestler character 3d model" by knotenvyapparel, owner's link) — front T-pose render `docs/tpose-refs/vainabel/a2_front.png` in western-heart (PR #428, MERGED). Bald muscular wrestler: purple flame vest over black tank, dog tags, black pants with bold purple cross-stitching, boots, fingerless glove + forearm wrap. Textures CLEAN, no smear, no clay. Unusual details: eyes are MISMATCHED (his right eye pale/milky, left eye dark); ears are PRESENT and small — unlike Attire 1's sculpt where the ears are gone (ear holes). Wired: `roster/vainabel/attires/attire2/model.glb` (19.8MB meshopt, byte-identical to the pull), MODEL_URLS `vainabel-attire2`, attires.js `vainabel` variants. Original backed up in release `vain-abel-tripo-pulls-20261020`. Render note: Workbench 1000px via the vendored EGL stack (plain xvfb-run aborts on libEGL tonight), film-transparent pass composited on white.

## Zui Tripo A1 lane 2026-10-21 (front render, own-eyes verified)
- [x] zui A1 "Drunken Monk" (owner Tripo, Drive file, `roster/zui/attires/attire1/model.glb`) — front T-pose render `docs/tpose-refs/zui/a1_front.png` in western-heart PR #431 (repo tpose tool, Cycles 2-sample, white bg). Bald monk, prayer-bead necklace, full irezumi + kanji torso tattoos, saffron sash wrap, wine gourds at the hip, sake cup in hand. Textures CLEAN, no smear, no clay. Axis note: this Tripo faces +X on import, so the tool's side camera produced the face-on view — repo files are labeled by content (a1_front.png = face-on front, a1_side.png = profile). Wired in PR #431 as Zui's DEFAULT on both resolution paths (the GLBs previously had NO MODEL_URLS keys — unreachable); A2 Rework v2 wired as alternate in the same PR (no new render; A2's clay-fallback render from 2026-10-16 stands as its only prior render).

## Vain Abel Attire 4 lane 2026-10-21 (front render, own-eyes verified)
- [x] vainabel A4 "Half mask Horror of the Haze" (Tripo 4d00d686 "wrestler character 3d model" by fmmf.mars, owner's link) — front render `docs/tpose-refs/vainabel/a4_front.png` in western-heart (PR #503). Bald muscular wrestler: purple-and-black HALF MASK over the upper face (mouth/jaw exposed), bare torso with the long diagonal stitched scar, dog tags, black pants with purple stitched flame patterns, purple-flame boots, fingerless glove + forearm wrap. Textures CLEAN, no smear, no clay. Ears present at the sides under the mask straps (same owner-noted pattern as A2/A3; A1's sculpt has them gone). Wired: `roster/vainabel/attires/attire4/model.glb` (20.3MB meshopt, byte-identical to the pull, sha256 5b4f8519…), MODEL_URLS `vainabel-attire4`, attires.js ATTIRE 4 variant. Original backed up in release `vain-abel-a4-tripo-20261021`. Render note: Workbench 1000px textured via the EGL stack; model faces +X — the +X view is the true front, confirmed against the −X back view (mask strap, belt pouch).
