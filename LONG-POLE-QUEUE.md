# LONG-POLE FOLLOW-UP QUEUE
## Planted 2026-10-12 per owner directive: when a task completes, the next one kicks off autonomously. No idle gaps.

### Queue 1: Tekken 3 Model Mapping → Character Renders
**Trigger:** model-mapping worker completes (King renderable)
**Next:**
1. Render all 7 Western Heart fighters (King, Jin, Yoshimitsu, Heihachi, Bryan, Gun Jack, Xiaoyu) front-facing, default pose, P1 attire
2. Render remaining Tekken 3 roster the same way
3. Extract animation data for each fighter
4. Build the "inspectable model viewer" — owner wants to rotate/inspect models

### Queue 2: Tekken 7 Pull → Extraction → Reskin Pipeline
**Trigger:** disk freed + 47GB download completes
**Next:**
1. Extract all 51 fighters' models via UModel
2. Map to Western Heart names (7 named, 44 to be named by owner)
3. Extract customization system (CCI/CI/CS items)
4. Build reskinning pipeline: Tekken 7 base → Western Heart character
5. THEN do the same for Tekken 3 models (legacy reskins)

### Queue 3: CN Gigaleak Pull → Sort → Distribute
**Trigger:** 200GB download lands
**Next:**
1. Sort by show into per-show directories
2. Distribute: matching repos get their show's materials, others get new cn-gigaleak-[show] repos
3. Wire study materials into Pocket Studio
4. Extract templates for future shows

### Queue 4: Wrestling Teardown → Animation Retargeting
**Trigger:** No Mercy deep teardown + WMXIX download complete
**Next:**
1. Extract wrestling skeletons and animations
2. Test retargeting onto Tekken 3/7 models
3. Document arena/stage systems for separate fighting modes
4. Build the creation-suite-inspired customization system

### Queue 5: Game Dev Production Study → Western Heart Pipeline
**Trigger:** production study worker completes
**Next:**
1. Apply pro fighting game character pipeline to Western Heart
2. Build character production docs for each of the 7 named fighters
3. Set up the per-fighter production folders in mhvnsnt/western-heart

### Queue 6: Western Heart Repo → Playable Build
**Trigger:** Tekken 7 models extracted + reskin pipeline working
**Next:**
1. First playable prototype (1-2 fighters, 1 stage)
2. Expand roster as reskins complete
3. Add Eastern Mind stages
4. Add wrestling mode

---
**Watchdog:** check this queue when a checkpoint marks done. Kick off the next item autonomously.

### Queue 7: EP01-TRIP-EDIT — Resume EP01 "The Walk" with Trip-Effects Direction
**Trigger:** disk <75% AND CN gigaleak pulls complete/throttled down AND cards/bumps/segments/fake commercials/gags exist
**Direction:** `production/WIZARD_GANG_EP01/TRIP-EFFECTS-DIRECTION.md` in mhvnsnt/TRIPPEDD-Production-studios- (PR #267)
**Handoff:** `~/workspace/agent-ops/EP01-TRIP-EDIT-HANDOFF-2026-10-15.md`
**Next:**
1. Read TRIP-EFFECTS-DIRECTION.md for full owner directive (psychedelic trip effects on live footage, building heavier then releasing, across all transitions)
2. Gather new cards/bumps/segments/commercials/gags + owner's Cape Jones transition material
3. Cut the trip edit from EP01-THE-WALK-v2.mp4 master (GitHub release ep01-v2-2026-10-15)
4. NO chroma key on main animation (owner law) — trip effects are overlays/grading only
