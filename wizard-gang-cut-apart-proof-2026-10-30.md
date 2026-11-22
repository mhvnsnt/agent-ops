# Cut-apart proof lane — log (2026-10-30)

## Scope as it ended (owner corrections during the run)
- STARTED as: Blossom (PPG EPS) + Space Ghost (SG EPS) cleanup/cut-apart proof.
- Owner 14:31 CDT: Space Ghost DROPPED ("we already have art and stuff if cape jones") — SG cut-apart outputs were deleted from _cut-apart/ the same run; no SG deliverable stands.
- Owner 14:32 CDT: Cape Jones named primary (his own drawn art) — then 14:35 CDT PARKED (his show's later turn).
- Owner 14:35 CDT: PRIMARY = WIZARD GANG, Ashes first. Blossom DROPPED at that point.
- Owner T-pose correction: T-pose source art is fine as a rig base if genuinely animated out of the pose; acceptance = motion + joins, not the source sheet. (No T-pose source was used in the Ashes set regardless.)
- Owner bend rule: parts must carry joint overlap so rotation on pivots doesn't tear. Measured per part in parts.json (see Ashes notes — the honest headline is that the upstream segmentation partitioned the figure, so most joints measure 0px overlap; the two overlaps that exist were built from real pixels by this lane.)

## ASHES (Wizard Gang) — DELIVERED
Folder: ~/workspace/your_files/wizard-gang-part-libraries/_cut-apart/ashes/
- parts/ (400x864 common canvas, transparent, binary alpha): head, torso, robe_skirt, robe_full, arm_L, arm_R, hand_R, braid_L, braid_R, chain, eyes, grill
- swaps/eyes/ (30 files: library eye states + base-white colorway), swaps/mouths/ (14: Mouth Set One)
- parts.json — source, bbox, pivot, measured joint overlap + note per part; swap anchors (eyes bbox 115,95-269,141; grill bbox 115,155-263,184); occluded gaps
- whole_ashes.png (the source figure, 00_base_full_figure)
- ashes_cut-apart_sheet.png — "ASHES (WIZARD GANG) — CUT APART": whole left, exploded labeled pieces with red pivot dots right, mouth swap strip bottom. Verified by eye by this lane.

Method: consumed the cast's own GMSS wizard-rig-proof layers (rig-proof/parts, HSV segmentation upstream, alpha counts verified == parts_manifest.json exactly). This lane: split robe into torso/robe_skirt with a deliberate 30px shared overlap band at the waist; segmented hand_R out of arm_R's own white-glove pixels (+3px outline ring, 1920px shared = the set's one true overlap); measured every other joint's overlap (0px — butt joints, stated plainly in parts.json).
NOT used: the library hands-gloves/robe/feet folders (generator-built parametric — owner called the gloves homemade); approved-pack 1600px frames (earlier design iteration: Celtic-knot hood, no braids/grill — left unmixed for owner's pick).
GAPS (logged, nothing invented): hand_L not drawn in this pose (arm_L tucks under arm_R; 13 stray white px); legs/feet not drawn (robe to the floor); no elbow segments (arms are single crossed pieces — shoulder rotation only); neck = butt joint; robe layer has no upper-center chest pixels (covered by head/braids/chain in assembly) and stairstep edges from the 400x864 source; upstream robe separation used Telea inpainting per its manifest.

## BLOSSOM (industry EPS technique proof — done for pose 01, then dropped by owner)
Folder: ~/workspace/your_files/wizard-gang-part-libraries/_industry-rendered/_cut-apart/blossom/
- blossom_cut.svg (layered master, one named group per part), parts/ (11 PNGs: bow, hair_front, hair_back, head, arm_L, arm_R, torso, leg_L, foot_L, leg_R, foot_R), parts.json (pivots + occluded gaps), blossom_cut-apart_sheet.png
Method: EPS -> Ghostscript pdfwrite -> pdftocairo -svg (real vector paths, 29). Source construction discovered: one black silhouette base path + color flats stacked on top (each flat is exactly its visible region). Color paths assigned to parts verbatim; the silhouette was split per part by zone polygons (sampled-curve shapely clip, simplify 0.25). Caption/page junk: none present in this file. Draw-order bug (fragments over flats) found on first sheet and fixed (fragments are the base layer).
Poses 02-05 were converted to SVG but NOT cut — owner dropped Blossom before that work.
Occluded gaps (in blossom/parts.json): head top under bangs has no skin art; torso under head not drawn; leg tops under dress hem not drawn; hands don't exist as separate paths (PPG arms are nubs — arm+hand are single paths); hair_back/arm_L boundary is an approximate cut through a genuinely overlapped projection region.

## CAPE JONES — PARKED, not worked this run (owner's later turn)
Notes preserved from the brief: sources are his drawn sheets 04/07/08 (+05/06 swap matrices), deliverable would go to ~/workspace/your_files/cape-jones-cut-apart/, design-sheet colors are NOT canon (A-ROYAL, cowl #3E1473), sheet 01 T-pose usable as rig base per the 14:37 correction provided he's animated out of the pose.
