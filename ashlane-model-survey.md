# AshLane / AshLanev2 Character Model Quality Survey
Date: 2026-10-09 | Surveyor: subagent (model-unification job) | Tool: `diagnose_rig.py` (Blender 4.0.2 headless) + independent skin/island verification
Method: every GLB meshopt-decompressed (`gltf-transform copy`) before import; rest pose (arm° from straight-down), bone count, L/R label mirror check, weight-bleed % (verts with >15% weight on bones >0.35m away), mesh islands (edge-connected, verified independently via bmesh), groups-per-vert skin check on shortlist.
Scoring: rest (T≥75°=3, 55-75°=2, A 20-55°=1, <20°=0) + skeleton (40-80 bones + mirrored + no mislabel=3; minor=2; mislabeled/<15=0) + bleed (<2%=3, 2-5%=2, 5-15%=1, >15%=0) + mesh (whole=3, accessories=2, severed=0). Max 12.
NOTE: /tmp was wiped mid-survey by the disk-cleanup daemon; all diagnostic numbers below were captured from tool output before the wipe; skin checks were re-run after.

## Ranked table (all 19 screened)

| # | Model | Repo | Size | Rest° | Bones | Bleed% | Islands>100v | Score | Critical flags |
|---|-------|------|------|-------|-------|--------|---------------|-------|----------------|
| 1 | PABLO_attire2.glb | V2 | 14.4MB | 82 T-pose | 52 | 0.0 (skinned, clean) | 142 | 8 | mesh exploded fragments; 0/23 mirrored |
| 2 | SOMBRA_NEGRA.glb | V2 | 19.9MB | 90 bone-T | 53 | 0.0 **VACUOUS** | 20 | 8 | **UNSKINNED (0 vertex groups)** — 0% bleed means no weights exist |
| 3 | EDWIN_KENNEDY_attire3.glb | V2 | 14.0MB | 65.6 between | 52 | 0.0 (skinned, clean) | 215 | 7 | mesh exploded fragments |
| 4 | CAIN_ELIAS_attire3.glb | V2 | 9.3MB | 90 bone-T | 52 | 14.9 | 74 | 6 | skinned; needs paint pass |
| 5 | BILL_DOZER.glb | V2 | 12.2MB | 90 bone-T | 53 | 0.0 **VACUOUS** | 27 | 6 | **UNSKINNED**; mirrored labels (21 pairs) |
| 6 | ASTRID.glb | V2 | 18.5MB | 90 bone-T | 53 | 0.0 **VACUOUS** | 22 | 6 | **UNSKINNED**; mirrored labels (21 pairs) |
| 7 | JAGER_nobeard.glb | V2 | 8.6MB | 90 bone-T | 52 | 25.2 | 126 | 5 | heaviest bleed of Tripo family |
| 8 | MARKS.glb | V2 | 7.7MB | 69.4 between | 53 | 6.1 | 10 (largest 41%) | 3 | mirrored labels; least-severed mesh |
| 9 | JAGER.glb | both (identical md5) | 3.0MB | 156.5 verts / 32.6 bones | 58 | 100 | 66 | 3 | **mesh/bone pose mismatch** — verts T-posed, bones A-posed; bleed is artifact |
| 10 | CASSIAN_THORNE_suit.glb | V2 | 2.5MB | 90 bone-T | 86 | 100 | 9 | 3 | scrambled skin; mirrored labels (12); mesh is "0007_M0003_02_Brian_Cage" |
| 11 | STICKUP.glb | AshLane | 497KB | 27.6 A-pose | 58 | 12.6 | 34 | 2 | known-bad confirmed |
| 12 | STICKUP.glb | V2 | 858KB | 22.1 A-pose | 58 | 14.2 | 34 | 2 | known-bad confirmed (same mesh, BANNON_XFER_MESH) |
| 13 | CIPHER_rigged.glb | AshLane | 512KB | 22.1 A-pose | 52 | 6.9 | 45 | 2 | mirrored labels |
| 14 | MASTER_SENSEI.glb | AshLane | 593KB | 38.4 A-pose | 58 | 13.6 | 31 | 2 | mirrored labels |
| 15 | KOBRA.glb | AshLane | 589KB | 32.5 A-pose | 58 | 14.4 | 40 | 2 | mirrored labels |
| 16 | VIPER.glb | AshLane | 565KB | 31.5 A-pose | 58 | 12.4 | 43 | 2 | mirrored labels |
| 17 | TITAN.glb | AshLane | 603KB | 45.5 A-pose | 58 | 18.5 | 42 | 1 | mirrored labels |
| 18 | BANNON_muscular_skinned.glb | V2 | 3.2MB | 33.2 A-pose | 58 | 44.6 | 20 | 1 | mirrored labels; worst bleed of transfer family |
| — | SOMBRA_NEGRA_rigged.glb | AshLane | 25MB | n/a | n/a | n/a | n/a | n/a | **CORRUPT — Blender cannot import**: skin joint index 46530 out of bounds (58 joints) |

## Two rig families found
- **Transfer family** (mesh name `BANNON_XFER_MESH`, `mixamorig:` bones): all of anim-fix cast + BANNON_muscular V2 + STICKUP V2. 58 bones, 20/23 L/R pairs positionally mirrored BUT labels mirrored (bones named Left sit on anatomical right — fatal for retarget), A-pose ~22-46°, bleed 6.9-44.6%, meshes severed into 20-66 pieces.
- **Tripo auto-rig family** (mesh names `tripo_node_*` / `Object_*`, `MixamoRig` bones): V2 attire variants. 52-53 bones, labels CORRECT, bone rest 90° (T), bleed either genuinely clean (PABLO_A2, EDWIN_A3 — smooth 1-4 bones/vert) or vacuous (SOMBRA_V2, ASTRID, BILL_DOZER — zero vertex groups, unskinned), meshes exploded into 10-215 large islands (Tripo image-to-3D fragmentation artifact, verified via bmesh on PABLO_A2: 14,153 islands, largest 3.16%).

## Deep report: top 8
1. **PABLO_attire2.glb** (8/12): T-pose 82° vertex-measured; 52 bones, correct labels; genuinely skinned with 0.0% bleed (1-4 groups/vert); 142 islands — mesh unusable as-is, but weights+skeleton are the cleanest measured.
2. **SOMBRA_NEGRA.glb** (8/12, ⚠️): scores 8 mechanically but mesh has ZERO vertex groups — the 0.0% bleed is vacuous. Skeleton (53 bones, correct labels, 90° rest) is fine; weights must be painted from scratch.
3. **EDWIN_KENNEDY_attire3.glb** (7/12): 65.6° between-pose; 52 bones, correct labels; genuinely skinned, 0.0% bleed; 215 islands — most fragmented mesh of the set.
4. **CAIN_ELIAS_attire3.glb** (7→6/12): 90° bone rest; 52 bones, correct labels; skinned but 14.9% bleed (Hips worst) — needs a paint pass; 74 islands.
5. **BILL_DOZER.glb** (6/12, ⚠️): unskinned + mirrored labels (21 pairs) — despite 0.0% bleed, not a donor.
6. **ASTRID.glb** (6/12, ⚠️): unskinned + mirrored labels (21 pairs) — not a donor.
7. **JAGER_nobeard.glb** (5/12): correct labels, 52 bones, but 25.2% bleed (Hips/Spine) and 126 islands — weakest of the Tripo rigs.
8. **MARKS.glb** (3/12): best of the transfer family by mesh (10 islands, 41% largest) and bleed 6.1% with real weights (shoulder bleed), but mirrored labels kill it as a skeleton donor.

## Donor recommendations (for model-unification job)
1. **PABLO_attire2.glb** (V2, `public/models/cast/`) — best WEIGHTS donor: only model with smooth multi-bone skinning AND 0.0% measured bleed; 52-bone rig with correct L/R labels; vertex-measured T-pose 82°. Caveat: mesh is exploded fragments — donate weights+skeleton, not the mesh.
2. **EDWIN_KENNEDY_attire3.glb** (V2) — second weights/skeleton donor: same Tripo rig family, 0.0% bleed smooth skinning, correct labels, 52 bones. Caveat: 215 islands, 65.6° between-pose.
3. **CAIN_ELIAS_attire3.glb** (V2) — third: correct labels, 52 bones, genuinely skinned (14.9% bleed needs a paint pass), 90° bone rest.
No screened model has verified L/R positional mirror symmetry WITH correct labels — the Tripo rigs have correct labels but 0-4/23 mirrored (auto-rig asymmetry); the transfer family is symmetric but mislabeled.

## Headline findings for the owner
- **The belief "AshLane has the best working models" is not supported by measurement.** The entire anim-fix cast is the same broken transfer pipeline as Bannon's Stick-Up: mirrored bone labels, 12-44% bleed, severed meshes.
- **STICKUP confirmed broken in BOTH repos** (AshLane 27.6°/12.6%/34 islands; V2 22.1°/14.2%/34 islands) — same `BANNON_XFER_MESH`.
- **anim-fix `SOMBRA_NEGRA_rigged.glb` (25MB) is corrupt** — skin references joint 46530 of 58; Blender cannot import it at all.
- **Three big V2 models are unskinned statues**: SOMBRA_NEGRA.glb, ASTRID.glb, BILL_DOZER.glb (zero vertex groups; their "0% bleed" is vacuous).
- **JAGER.glb is byte-identical in both repos** and has a mesh-vs-bone pose mismatch (verts 156°, bones 32.6°) — its 100% bleed is an artifact.
