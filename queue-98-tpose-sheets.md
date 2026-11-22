# QUEUED: T-pose sheets for all 98 unnamed models (owner order 2026-10-14 ~21:46 EDT)

**Do not start until:** Zui rework shown to owner, T6/TTT2 teardown coordinator landed, WWE 2K19 TeraBox pull resolved.

**Source inventory:** `~/workspace/agent-ops/UNNAMED-MODELS-INVENTORY.md` (verified 2026-10-14, 98 models)
- Tekken 7 (5): Lili, Lei Wulong, Baek, Mokujin, Zafina — `~/workspace/game-reverse-engineering/tekken7/models/` (zips with FBX)
- Virtua Fighter 5 (19): Akira, Pai, Lau, Wolf, Jeffry, Kage, Sarah, Jacky, Shun, Lion, Aoi, Lei-Fei, Vanessa, Brad, Goh, Eileen, El Blaze, Dural — `~/workspace/western-heart-vf5/teardown/virtua-fighter-5/models/`
- Urban Reign (72): char001–char072 — `western-heart/teardown/urban-reign/models/` (OBJ + ROSTER.json, coded no names)
- Street Fighter (1): Rashid, 3 variants — `western-heart/teardown/street-fighter-5/models/rashid/`
- Mixamo Soldier (1) — `~/workspace/game-reverse-engineering/western-heart-assets/tk-fighting-game/assets/models/Soldier.glb`

**Excluded:** ~6,400 wrestling models (Def Jam, No Mercy, WWE) — earmarked for the wrestling game per the separation rule. Doc Frank / Dr. Bosconovitch is NAMED (not in pool).

**Spec to follow:** `western-heart/docs/tpose-refs/MUSE_TPOSE_SPEC.md` — 2048x2048 PNG, pure white, orthographic, T-pose via skeleton (never edit mesh), fingertips/toes/tail/hair in frame, flat lighting, no magenta/untextured = FAIL, SHA256SUMS entry per file.
**Render tool:** `western-heart/docs/tpose-refs/_tools/tpose_render.py` (Blender headless; supports Mixamo + Tekken 8 bone names; XPS/.mesh.ascii needs extra importer).
**Naming:** `docs/tpose-refs/<fighter>/p1_front.png` + `p1_side.png` (lowercase, `-` inside names). Fighter = model source name for now (no WH names yet).
**Owner review:** sheets shown INDIVIDUALLY in chat (his words). He judges every visual.

**Blockers known up front:** Rashid XPS variants need the XPS importer (same as Beast King); some models may be static/no-rig → mark BLOCKED-no-rig per spec, don't hand-fix.
**Laws:** branch → PR → merge; deliverable verification (own eyes on every sheet before it reaches owner); no unasked renames.
