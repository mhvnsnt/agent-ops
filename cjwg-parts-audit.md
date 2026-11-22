# Wizard Gang FLA Puppets — REAL Parts Audit

**Date:** 2026-11-02 · **Auditor:** parts-audit subagent (disk inspection only — `ls`/`find`/`du`, INDEX/parts.json reads, PIL alpha/mode sampling)
**Sources audited:**
- `~/workspace/your_files/wizard-gang-part-libraries/` — 2.0 GB, 23,011 files total (most of that is `_industry/` 8,711 files + `_candidates/` + comparison sheets — **not** Wizard Gang parts)
- `~/workspace/your_files/wizard-gang-mouth-sets/` — 2.4 MB, 130 files (118 mouth PNGs + contact sheets/meta)
- `~/workspace/your_files/wizard-gang-part-libraries/_cut-apart/ashes/` — Ashes only

## Counting rules (read first — this is where past counts inflated)

1. **Contact sheets / verify sheets are NOT parts.** Every category folder contains a `_CONTACT_SHEET.png` (and eyes an `_VERIFY_base-white.png`). Eye/mouth counts below exclude them.
2. **Three different kinds of file are mixed in these folders, and only the first is a buildable part:**
   - **(A) REAL extracted cutouts** — RGBA, real alpha, tight part-bbox canvas, from the character's own pixels: `eyes/`, `arms/`, `head-hood/`, `hair-accessories/`, `hands/`, `mouths/set-one/`, plus the full-common-canvas layers in `rig-proof/parts/` + `rig-proof/rig-layers/` (RGBA, alpha present — sampled verified).
   - **(B) PACK-GENERATED art — NOT extracted, NOT the characters' own art:** `hands-gloves/` (20/char), `robe/` (ROBE_FRONT/BACK + SLEEVE_L/R, 4/char), `feet/` (SHOE_L/R/PAIR, 3/char) in every *standard* folder. Per the library's own INDEX, these are parametric PIL constructions built in-house 2026-10-29 (`glove_gen.py`/`robe_gen.py`). The owner verdict recorded in that INDEX: the gloves "look homemade." They exist and are usable as placeholders, but **do not count them as real parts.** Battle folders do **not** contain them at all.
   - **(C) FULL-FRAME, NO ALPHA — NOT parts at all:** `v1-concept/` (200 PNGs across 8 chars, **all verified mode=RGB, no alpha**, 1600×1600 full frames with the whole character behind the "part") and `ashes/ashes-approved-pack/` (26 PNGs, **all RGB, no alpha**, also an *earlier design iteration* — Celtic-knot hood, no braids/grill). These cannot be dropped into a rig as separated parts. They are reference frames only.
3. **`rig-proof/parts/00_base_full_figure.png` in every folder is a whole-character image** (RGBA silhouette on transparent background, e.g. Ashes 400×864, 54% opaque) — not a body part.
4. **No character is "only full-frame whole-character images."** Every one of the 9 has real separated cutouts (kind A). But **no character is fully buildable to the requested bend spec either** — see Universal Gaps. The honest verdict for all 9 is **PARTIAL**, at different depths.

## Universal gaps — apply to ALL 9 characters, both variants

For a rig with **neck / shoulder / elbow / hip / knee** bends:

| Joint | Status on disk | Evidence |
|---|---|---|
| **Legs (hip + knee)** | **MISSING for all 9.** No leg, thigh, shin, upper-arm/forearm, elbow, knee, or neck file exists anywhere in any character folder (filename search across all 18 folders: zero hits, except two battle `rig-layers/00_torso.png` raw layers). Every source design is robe-to-the-floor; there is no unrobed/leg reference in the source art. | Library INDEX gap #1, confirmed by search |
| **Feet** | Only kind-B pack shoes (3, standard folders only). No character's own feet exist. | `feet/` = pack art |
| **Elbow** | **MISSING for all 9.** Every extracted arm is **one single drawn piece** (REST pose only). No upper-arm/forearm split exists in any pose. Shoulder rotation only. | parts.json (Ashes) + INDEX gap #6 |
| **Neck overlap** | **0 px for the only measured case (Ashes).** Head and robe were *partitioned* by the upstream segmentation — they share an edge, not an overlap. Small head tilts stay closed; wide turns gap at the neck. No neck segment, no extended head-bottom art for any character. | `_cut-apart/ashes/parts.json` |
| **Shoulder overlap** | Same partitioning: **0 px shared pixels** arm↔torso (Ashes, measured). Arms sit in front in z-order, so small swings read fine; big swings open a wedge. | parts.json |
| **Torso as a separate part** | **No standalone torso cutout in any library folder.** The body exists only as `rig-proof/parts/01_robe.png` (full common canvas, torso+skirt as ONE unsplit robe piece; Kiko: `01_body.png`). The kind-B `robe/ROBE_FRONT` is a generated garment, not a torso. **Only Ashes (cut-apart) has a real torso/robe_skirt split.** | folder census |
| **Arm pose swaps** | Only **REST** arms were ever extracted. No raised/bent/pointing own-art arms for anyone. (Real bent arm+hand pieces exist only for *other shows'* characters in `_candidates/` — Gumball 47, Nicole 23, Pim 12, Charlie 5 — not for this cast.) | INDEX gap #6 |
| **Brows** | None for any character (void-face design; expression is carried by eyes). | INDEX gap #3 |
| **Hood-down head** | None for any character — one hooded source per character. | INDEX gap #2 |
| **TQ / back views** | Not built; no TQ/back source art. All parts are FRONT only. | INDEX gap #11 |
| **Mouths (void cast)** | See per-character notes: only Ashes has a mouth in his source art. The other 8 sets are **built** flat Blair shapes in each character's void-face language, not extracted — and by owner rule those characters are mouthless ~90% of the time anyway. | mouth-sets INDEX |

---

## Summary table

File counts = all files in folder (PNG + INDEX.md/.json/.inp). Eye count = real eye files in standard folder, excluding contact/verify sheets; `+bw` = additional base-white copies in `eyes/base-white/`. Mouth count = Set One (identical in standalone `wizard-gang-mouth-sets/<char>/` and in-library `mouths/set-one/`).

| Character | Standard folder (files / PNG) | Battle folder (files / PNG) | Eyes (std) | Mouths | Own-art arms | Own-art hands | Verdict |
|---|---|---|---|---|---|---|---|
| **Ashes** | `ashes/` 139 / 136 | `ashes-battle/` 67 / 64 | 15 +15 bw | **14, real (from his grill)** | L+R REST | R only (on-arm) | **PARTIAL — closest to buildable; only character with a pivoted cut-apart** |
| **Static** | `static/` 125 / 122 | `static-battle/` 57 / 54 | 14 +14 bw (no EYE_L_SHUT std) | 13, built | L+R REST | none | **PARTIAL** |
| **Cipher** | `cipher/` 126 / 123 | `cipher-battle/` 54 / 51 | 15 +15 bw | 13, built | R only in tidy folder (L+R raw in rig-proof) | R only | **PARTIAL** |
| **Sombra Negra** | `sombra/` 122 / 119 | `sombra-battle/` 49 / 46 | 15 +15 bw | 13, built | **none** | **none** | **PARTIAL — GAP-heavy (no arms/hands of his own)** |
| **Kiko** | `kiko/` 114 / 111 | `kiko-battle/` 54 / 51 | **4 sparkle only** +4 bw (battle: 15) | 13, built | L+R REST | none | **PARTIAL — eye system is the gap (std)** |
| **Theory** | `theory/` 128 / 125 | `theory-battle/` 54 / 51 | 15 +15 bw | 13, built | L+R REST | none (battle: R) | **PARTIAL** |
| **Onyx** | `onyx/` 137 / 134 | `onyx-battle/` 31 / 28 | 15 +15 bw (battle: **3 only**) | 13, built | L+R REST | L+R on-arm | **PARTIAL (std); battle is GAP-thin** |
| **Echo** | `echo/` 128 / 125 | `echo-battle/` 64 / 61 | 15 +15 bw | 13, built | L+R REST | none | **PARTIAL** |
| **Hollow** | `hollow/` 122 / 119 | `hollow-battle/` 48 / 45 | 14 +14 bw (no EYE_L_SHUT std) | 13, built | **none** | **none** | **PARTIAL — GAP-heavy (no arms/hands of his own)** |

---

## Per-character detail

### 1. Ashes — PARTIAL, closest to buildable
- **Path:** `wizard-gang-part-libraries/ashes/` (32 MB) + `ashes-battle/` (13 MB) + `_cut-apart/ashes/` (20 MB, 73 files incl. proofs/video)
- **Head:** YES — `head-hood/WG_ASHES_FRONT_HEAD_HOOD_UP.png` (tight cutout, RGBA sampled: 294×269, real alpha) + `rig-proof/parts/02_head.png` (full 400×864 canvas layer). Battle also has HEAD_HOOD_UP + FACE_PLATE (duplicate pixels, per INDEX).
- **Torso:** In the library, only as unsplit `rig-proof/parts/01_robe.png`. **In `_cut-apart/ashes/parts/` he alone gets a real split:** `torso.png` (robe rows 270–519, pivot 172,505), `robe_skirt.png` (rows 490–863, pivot 172,498) with a **measured 30 px real overlap band** at the waist, plus `robe_full.png` unsplit alternative.
- **Arms:** `arms/` L+R REST (single-piece, crossed pose); cut-apart `arm_L.png` pivot (62,335) / `arm_R.png` pivot (298,335), shoulder joint, **0 px overlap, no elbow segment**.
- **Hands:** own-art **R only** (`hands/WG_ASHES_FRONT_HAND_R_REST_ON_ARM.png`; cut-apart `hand_R.png` segmented out of arm_R, wrist pivot 232,338, 1,920 px true overlap — the only true-overlap joint in the set). **Hand_L does not exist in the source pose** (arm_L ends tucked under arm_R, no glove drawn — explicitly not invented, parts.json). Plus kind-B glove pack (20, generated) and kind-C approved-pack hands (10, full-frame RGB, earlier design — do not mix).
- **Other real parts:** braids L/R, chain, feet = pack shoes only.
- **Eyes:** 15 colourway + 15 base-white (L/R open/shut/half, pupils L/R, pair OPEN/LOOK L/R/UP/DOWN/SMILE/ANGRY). Cut-apart `swaps/eyes/` carries the same 15 + 15 base-white-prefixed copies.
- **Mouths:** **14 — the only REAL set in the cast**, built from his own gold-grill pixels: A–H, X_REST, O_ROUND, WIDE, HOLD_POSE, SMUG, BARE_TEETH. Cut-apart `swaps/mouths/` = same 14; default face part is `grill.png` (pivot 189,170).
- **Cut-apart (`_cut-apart/ashes/parts.json`) — 12 parts with pivots/bboxes/measured overlaps:** head (pivot 188,250, neck butt joint 0 px), torso, robe_skirt, robe_full, arm_L, arm_R, hand_R, braid_L (130,178), braid_R (260,178), chain (200,232), eyes (192,118), grill (189,170). Canvas 400×864. This is the **only character with a parts.json / pivot document anywhere in the library.**
- **GAPS for Ashes:** legs/feet (own), hip, knee, elbow (both arms), hand_L, neck overlap for wide turns, shoulder overlap for big swings, hood-down head, brows, TQ/back, arm poses beyond REST, low native resolution (400×864 source — parts are small).

### 2. Static — PARTIAL
- **Path:** `static/` (30 MB) + `static-battle/` — battle has no mouths/gloves/robe/feet folders; it shares the standard pack systems per its INDEX.
- **Head:** YES, HEAD_HOOD_UP std + battle. **Torso:** none separate; `rig-proof/parts/01_robe.png` unsplit (battle rig-layers also hold a raw `00_torso.png` layer on full canvas — not a tight cutout). **Arms:** L+R REST std; battle R only (raw `04_arm.png`). **Hands:** **no own-art hands in std** (hands live inside the sleeves in his art); battle has HAND_R_REST_ON_ARM. Gloves = pack only.
- **Accessories:** chain (1). **Eyes:** std **14** — EYE_L_SHUT is missing from the standard set (present in battle's 15); +14 base-white. **Mouths:** 13 built (special: GLITCH). His mouth does not exist in source art.
- **GAPS:** universal gaps + no own hands (std), EYE_L_SHUT (std), legs/elbow/neck/hip/knee.

### 3. Cipher — PARTIAL
- **Path:** `cipher/` (26 MB) + `cipher-battle/` (no head-hood folder in battle — use standard head, INDEX gap #7).
- **Head:** YES std HEAD_HOOD_UP. **Torso:** none separate; `01_robe.png` unsplit. **Arms:** tidy `arms/` folder holds **R REST only**, but `rig-proof/parts/` holds raw `03_arm_L.png` + `04_arm_R.png` — the left arm exists as a raw full-canvas layer, just never shipped as a tight cutout. Battle: L only. **Hands:** R on-arm only (+ pack gloves). **Accessories:** chain.
- **Eyes:** 15 +15 bw. **Mouths:** 13 built (special: FERAL). Note from mouth INDEX: his chains pile directly under his chin — mouth anchor sits above the chain line.
- **GAPS:** universal + tidy L-arm cutout missing (raw exists), hand_L, legs/elbow/neck/hip/knee.

### 4. Sombra Negra — PARTIAL, GAP-heavy
- **Path:** `sombra/` (25 MB) + `sombra-battle/` (thinnest battle folder alongside Hollow's: no arms, hands, head-hood, hair, robe, feet, or mouths folders at all — eyes + rig-proof only).
- **Head:** YES std HEAD_HOOD_UP (his eyes are genuinely two small white slits — verified by the library builder against his face art). **Torso:** none separate; `01_robe.png`.
- **Arms: NONE. Hands: NONE.** His source folder contains no arm layers at all — arms were never separated and live inside the robe/body drawing; the library explicitly refused to slice them out along invented lines. The only arm available is the kind-B pack sleeve (SLEEVE_L/R) + pack glove. **Any Sombra rig is therefore a pack-sleeve rig, not an own-art arm rig.**
- **Accessories:** chain. **Eyes:** 15 +15 bw. **Mouths:** 13 built (special: WHISPER, extra-small slit). His gold skull *pendant's* teeth are jewellery and were correctly NOT used as a mouth. Mouth INDEX also flags his standard source crop as the weakest/darkest art of the nine.
- **GAPS:** universal + **entire arm/hand system (own-art)**, battle head, legs/elbow/neck/hip/knee.

### 5. Kiko — PARTIAL, eye system is the gap (standard)
- **Path:** `kiko/` (81 MB — largest, high-res 1060×1945 source) + `kiko-battle/`.
- **Head:** YES HEAD_HOOD_UP std + battle. **Torso/body:** `rig-proof/parts/01_body.png` (not `01_robe` — her open-coat design); still unsplit, full canvas. No separate torso cutout. **Arms:** L+R REST std; battle L only (raw also has only `04_arm_l.png`). **Hands:** none own-art; pack gloves only.
- **Accessories (richest set):** chains, drape L/R, hair side A/B (5 real + sheet).
- **Eyes: STANDARD = only 4** — `EYE_L_SPARKLE`, `EYE_R_SPARKLE`, `EYE_PAIR_SPARKLE`, `EYE_PAIR_DIM` (+4 base-white). **No open/shut/half/look/smile/angry system exists for standard Kiko** — her source has no eye layers; the sparkles were luminance-keyed off her face plate. **Battle Kiko has the full conventional 15** +15 bw. A standard-Kiko blink/look rig cannot be built from her standard eyes alone.
- **Mouths:** 13 built (special: SING). No mouth in source art.
- **GAPS:** universal + standard eye system, own hands, legs/elbow/neck/hip/knee.

### 6. Theory — PARTIAL
- **Path:** `theory/` (24 MB) + `theory-battle/` (no head-hood in battle — use standard).
- **Head:** YES std. **Torso:** none separate; `01_robe.png`. **Arms:** L+R REST std; battle R only. **Hands:** none own-art in std; battle HAND_R_REST_ON_ARM. Pack gloves fill std.
- **Accessories:** chain. **Eyes:** 15 +15 bw — with a documented history: her L eye was recovered from her base figure (her left-eye layer holds ~25 usable pixels) and EYE_L_SHUT ships as a mirror of her own EYE_R_SHUT (47×26 sliver). Functional, but the L-side eye art is thin/reconstructed, not a clean extraction. **Mouths:** 13 built (special: ORACLE).
- **GAPS:** universal + own hands (std), L-eye provenance thinness, legs/elbow/neck/hip/knee.

### 7. Onyx — PARTIAL (standard); battle GAP-thin
- **Path:** `onyx/` (18 MB) + `onyx-battle/` (31 files total — the thinnest character folder in the library).
- **Head:** YES std HEAD_HOOD_UP (+ a v1-concept base-face frame, kind-C RGB, not a part). Battle: **no head-hood**. **Torso:** none separate; `01_robe.png` (rig-proof parts contain duplicated arm/bell layers under two numbers — source duplication, not extra parts). **Arms:** L+R REST std — best arm coverage in the cast after Ashes; battle R only, one arm in source. **Hands:** **L+R on-arm — the only character besides Ashes with any own-art hands, and the only one with both.**
- **Accessories:** BELL_R complete; BELL_L ships as a mirror of BELL_R (the real L extraction survives only as `WG_ONYX_FRONT_BELL_L_FRAGMENTS.png`); STAFF_ORB real; STAFF_SHAFT is kind-B generic pack wood (no shaft pixels exist in source).
- **Eyes:** std 15 +15 bw. **Battle eyes: only 3** (EYE_L_OPEN, EYE_R_OPEN, EYE_PAIR_OPEN) +3 bw — no blink/look system in battle. **Mouths:** 13 built (special: SOFT_SMILE, a thin arc — 12% fill outlier in verification).
- **GAPS:** universal + battle folder is a skeleton (3 eyes, 1 arm, 1 hand, no head/accessories), staff shaft not real, legs/elbow/neck/hip/knee.

### 8. Echo — PARTIAL
- **Path:** `echo/` (27 MB) + `echo-battle/` (richest battle folder: 64 files, incl. spray-can prop parts in rig-proof).
- **Head:** YES std + battle (battle also FACE_PLATE = duplicate of HEAD_HOOD_UP pixels). **Torso:** none separate std; battle rig-layers hold a raw `00_torso.png`. **Arms:** L+R REST std; battle has `ARM_REST` + `ARM_R_REST` (two files, naming suggests one is not side-specific — builder should verify before use). **Hands:** none own-art std; pack gloves only. Battle rig-proof has a raw `05_hand.png` layer.
- **Accessories:** chain; battle rig-proof adds spray-can parts (×2). **Eyes:** 15 +15 bw — rebuilt by the library from her pale-pink eye class (251,129,250) after the first pass caught magenta hood splatter; clean set is what's on disk. **Mouths:** 13 built (special: MIMIC).
- **GAPS:** universal + own hands (std), legs/elbow/neck/hip/knee.

### 9. Hollow — PARTIAL, GAP-heavy
- **Path:** `hollow/` (36 MB) + `hollow-battle/` (48 files: eyes + rig-proof only — no arms/hands/head-hood/robe/feet/mouths folders).
- **Head:** YES std HEAD_HOOD_UP; battle **no head-hood** (use standard). **Torso:** none separate; `01_robe.png`.
- **Arms: NONE. Hands: NONE** — same situation as Sombra: no arm layers in his source (his whole illustration holds ~300 white pixels, eyes/glints only). Only the kind-B pack sleeve + pack glove can form an arm.
- **Accessories:** chain. **Eyes:** std **14** — EYE_L_SHUT missing from standard (present in battle's 15); +14 bw. Orange flame eyes. **Mouths:** 13 built (special: JAGGED).
- **GAPS:** universal + **entire arm/hand system (own-art)**, EYE_L_SHUT (std), battle head, legs/elbow/neck/hip/knee.

---

## Bottom line for the FLA build lane

- **Buildable today (limited rig):** all 9 as a *front, hood-up, robe* puppet with head tilt (small), shoulder swing (small/moderate), eye swaps (full, except std Kiko = sparkle/dim only and battle Onyx = open only), mouth swaps (Ashes real; other 8 built/rare-use), and waist motion **only for Ashes** (cut-apart torso/skirt split). Ashes is the only one with documented pivots — every other character's pivots still have to be set by the builder from the part bboxes.
- **Not buildable from anything on disk, for anyone:** elbow bends, hip bends, knee bends, legs, own-art feet, wide neck turns without a gap, arm poses beyond REST, hood-down heads, back/TQ views. Those need a drawn-new art pass — they were not fabricated into these folders, and the pack gloves/robes/shoes that paper over some of them are generator-built placeholders the owner has already called homemade (gloves).
- **Do not count as parts:** all `v1-concept/` (200 RGB full-frames), all `ashes-approved-pack/` (26 RGB full-frames, earlier design), all `00_base_full_figure.png` whole-character images, all `_CONTACT_SHEET.png` / `_VERIFY_*.png`, and anything under `_industry/`, `_candidates/`, `character-parts-full-diagrams/`, or `correct-comparison-to-industry-standard/` (other shows' parts / comparison sheets).
