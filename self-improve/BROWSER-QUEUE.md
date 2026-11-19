# BROWSER-QUEUE — live-browser checks the kit cannot do
Checks that need the live browser (login, JS, download button). A lane
never claims the site is down from a fetch error alone, and never leaves
an item UNVERIFIED forever — it goes here, and the parent runs it in the
live browser. (BROWSER-QUEUE LAW, ~/AGENTS.md.)

## Open
- [ ] **MetaHuman digital-human reference (Behance gallery "My Own MetaHuman")**
  What to confirm: turntable images, close-ups, facial-rig test video,
  blue/green lighting, NYC night HDRI — the top digital-human render
  reference named in research. Fetch the gallery images into
  `reference/` (FETCH-VERIFIED, sha256 in manifest.json) or record why not.
  Why browser-gated: curl returned a 453-byte bot-check page; page text was
  verified by search, images not fetchable by curl.
  Source: Behance gallery (search "My Own MetaHuman" on behance.net).
  Added 2026-11-16 by self-improve round 2 (reference library gap).
- [ ] **Best facial-expression rig test (MetaHuman facial-rig test video)**
  Same item as above — the rig-test video from the same gallery.
  Added 2026-11-16 by self-improve round 2 (reference library gap).
- [ ] **Mixamo downloads** (carried from round 1 — direct fetch failed with
  an upstream error, not proof the site is down).
  What to confirm: that Mixamo's mocap animation library is downloadable
  (pick a run/dance animation, confirm the download works) and what the
  auto-rig flow returns. Mixamo's role: mocap LIBRARY + auto-rig/retarget
  — it does NOT AI-generate new mocap (see ~/MEMORY.md, AI MOCAP
  GENERATION 2026-11-16).
  Source: https://www.mixamo.com/
  Added 2026-11-16 by self-improve round 1.

## Done
- (none yet)
