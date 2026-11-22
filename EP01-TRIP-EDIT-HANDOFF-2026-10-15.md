# EP01 "THE WALK" — TRIP-EDIT HANDOFF
**Created:** 2026-10-15 ~18:30 EDT
**Owner order:** 2026-10-15 ~18:26 EDT — log the trip-effects direction everywhere for when work resumes

---

## The Direction (owner's words, condensed)

Pick back up on EP01 "The Walk" (TRIPPEDD) after disk clears and downloads finish — likely later today or tomorrow (2026-10-15/16).

When it resumes, the edit gets **PSYCHEDELIC TRIP EFFECTS** on the live footage:
- Feels like the camera person is tripping hard
- Phasing in and out like an actual psychedelic trip
- Effects get **HEAVIER and HEAVIER** as the episode plays
- Then fade in/out — heavier, then lighter, until they go away
- Throughout the episode AND into the transitions between live footage and animated parts/segments/gags/cards/commercials
- Cape Jones material (he's making now) inserts into transitioning scenes
- He watched the current cut, said it was pretty good
- Wants video edits on certain parts + extensions with this trip treatment

**Full direction doc:** `production/WIZARD_GANG_EP01/TRIP-EFFECTS-DIRECTION.md` in mhvnsnt/TRIPPEDD-Production-studios- (PR #267)

---

## Current EP01 State

**Master:** `EP01-THE-WALK-v2.mp4`
- Size: 2,441,259,465 bytes (2.44GB)
- Duration: 1272.53s (~21:12)
- 11 segments in locked order
- On GitHub: release `ep01-v2-2026-10-15` (mhvnsnt/TRIPPEDD-Production-studios-)
- TeraBox: upload in progress (2026-10-15)

**Known issue:** A/V drift — video 1272.17s vs audio 1272.52s = 0.35s diff inherited from p2 source. Exceeds 0.1s QC threshold. Owner was told to listen on his end.

**What v2 includes:**
- Cold open, motel, Shumafied (owner-located), disappointment+cigar
- LOTI card + raw + commercial (YouTube 60s version spliced in)
- The walk, bag sequence, WBRB card + Goodville promo
- Joe prayer scene (16 watercolor panels, 160.4s)
- TV segment, Clothed and Confused (66.5s), smoking, STAY TRIPPEDD card
- 3 Wizard Gang interstitials at act breaks

---

## Assets Still Needed

Before the trip edit can happen, more of these need to exist:
- [ ] Cards (network cards, title cards, transition cards)
- [ ] Bumps (transitional bumpers)
- [ ] Segments (new produced segments)
- [ ] Fake commercials
- [ ] Gags
- [ ] Owner's Cape Jones transition material (he's making this now)

---

## Resume Trigger

Pick this back up when ALL of these are true:
1. **Disk <75%** (currently 90% — CN pulls and TeraBox uploads in progress)
2. **CN gigaleak downloads done** or throttled to background
3. **Assets above exist** (cards/bumps/segments/commercials/gags)

**Queue entry:** `~/workspace/agent-ops/LONG-POLE-QUEUE.md` → Queue 7: EP01-TRIP-EDIT

---

## Technical Constraints (owner laws)

- **NO chroma key on main animation** (owner law 2026-10-15) — chroma key is for overlays/color grading ONLY, and only when he specifically says so. Trip effects = overlays/grading, NOT keying.
- **NO hand-tooling** — use proven tools (FFmpeg filters, etc.), not hand-built approximations
- **NO mockups** — everything real and wired
- Effect toolkit: FFmpeg (hue rotation, saturation pulse, RGB shift, trails/echo, breathing zoom, wave distortion)
- The intensity curve (build → peak → release) is the key creative decision

---

## Related Docs

- Direction: `production/WIZARD_GANG_EP01/TRIP-EFFECTS-DIRECTION.md` (TRIPPEDD repo, PR #267)
- Memory: `~/MEMORY.md` → "EP01 THE WALK TRIP-EFFECTS DIRECTION (owner 2026-10-15 ~18:23 EDT)"
- EP01 v2 release: https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/releases/tag/ep01-v2-2026-10-15
- PR: https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/pull/267
