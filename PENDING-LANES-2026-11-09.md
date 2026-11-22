# PENDING LANES — written 2026-11-09 ~16:05 CST by the Build-A-Bitch chat parent

Spawn infrastructure fault at write time: `subagent.spawn` returns
"subagent reservation owner is terminal or structurally invalid" and
`browser.browse` returns sqlx pool timeouts. Two owner orders are fully
briefed below and MUST be launched the moment spawning recovers. Do not
shrink them. (Lanes already running and unaffected: waddle v4 657e5701,
glam 6a277f67.)

## LANE A — REEL BROWSER CAPTURE (owner order: "Here's another video to mocap", 2026-11-09 ~15:35 CST)

Browser task (browser.browse, task_id new, url https://www.facebook.com/reel/1695079522145293/):

GOAL: download the actual video file of Facebook reel 1695079522145293 so it
can be motion-capture tracked. All logged-out routes are documented dead in
~/workspace/_reel-1695079522145293/BLOCKED-download.md (yt-dlp latest included:
Facebook serves logged-out clients a shell with no media URLs; anonymous
GraphQL rejected; FDown bot-blocked). Only route left = signed-in Muse
browser; facebook.com saved login exists; owner standing law: sign in
directly, never ask him. DO: sign in if prompted, open the reel, let it play,
download the video file; completion report MUST include the download
artifact's exact path from the receipt + size (+duration/resolution if
visible). Then hand the file to the (already-prepared) tracking pipeline in
~/workspace/_reel-1695079522145293/ (MediaPipe verified ready per
BLOCKED-download.md tail) → study + tracked-overlay proof video
~/workspace/your_files/reel-1695079522145293-tracked-20261109.mp4 + mocap
library landing PR with readback.

## LANE B — LICENCE-HOLD SWEEP + FREE EQUIVALENTS (combined relaunch)

Owner law (restated 2026-11-09 ~15:45–15:53 CST): licence NEVER gates
pulling/wiring/using anything that helps; "documented-not-pulled" category
ABOLISHED (AGENTS.md + MEMORY.md rewritten). Paywall/vendor-account items do
NOT come back as a purchase list — find a FREE top-level industry-standard
EQUIVALENT for each and wire that up. No purchases; no login/paywall
circumvention (route around via equivalents); licences logged honestly;
weights fetch-at-pin; stage payloads early; PR → merge → read back every
payload file from main. Repo: PP mhvnsnt/physics-playground-pwa,
docs/build-a-bitch/.

PART 1 — wire everything held back (directly obtainable):
(a) tools/ai-animation/: HunyuanVideo wiring (fetch-at-pin + runner + smoke note).
(b) tools/reaction/: Py-Feat weights + L2CS-Net/Gaze360 weights (were code-only).
(c) Reaction not-pulled list: OpenFace, InsightFace models, WebGazer.js, Pupil, openSMILE, Wav2Lip — pull + wire.
(d) TOP-20 eight + watch-only: FLAME family (FLAME/DECA/EMOCA/MICA/SMIRK/SPECTRE), BFM, SMPL/SMPL-X/STAR + MPI regressors, Pixel3DMM, NPHM, HRN — pull/wire what's obtainable; registration-gated free academic downloads: try, name absolute walls and route those to Part 2; update TOP-20.md/SURVEY.md — not-pulled category GONE.
(e) WAVE2-STACKS.md never-pulled: Cascadeur + VRoid Studio + ArmorPaint free builds — pull + wire; rest → Part 2.
(f) MPFB2: the 25 CC-BY packs excluded in PR #77 — catalogue + pull like CC0.
(g) Visual annex: remaining WITHHELD figures (4 NC ones landed PR #144 — don't redo) — find + file.
(h) Grep docs/build-a-bitch/ for "documented-not-pulled" / "not pulled" / "WITHHELD" / "licence gap" — clear every hit.

PART 2 — free equivalents for gated items (real research per item; leads are
leads, verify/upgrade): KeenTools FaceBuilder → GNM fitter + ICT-FaceKit +
HRN-class; Faceform Wrap → Instant Meshes/Quadriflow/MeshLab + barycentric
transfer; Faceware → OpenSeeFace + MediaPipe solve glue as a mocap station;
Affectiva/iMotions → Py-Feat + OpenFace AUs + NeuroKit2 as an affect station;
JALI → Rhubarb + viseme tooling; NVIDIA Audio2Face → SadTalker/MuseTalk/
Wav2Lip-class; MetaHuman → capability mapping onto GNM + MPFB2 + Anny/MHR
(honest deltas); DAZ G9 / Reallusion CC5 → MPFB2 + Anny/MHR + VRoid;
Marvelous Designer → Blender cloth + strongest free garment pipeline;
Substance Painter → ArmorPaint/Materialize/Quixel Mixer; BDO creator → the
creation suite itself (document); MiniMax H3 → Wan/HunyuanVideo class; paid
asset-hunt packs (Kibbitz/SEAMPROOF/Vefects/Daz Wet Body) → vendored MIT
fluid solvers + Mantaflow bakes + SPlisHSPlasH.
SMOKE-PROVE each wired equivalent on one of OUR assets (still/clip/test —
"installed" is not proof). DELIVER: EQUIVALENTS.md + updated survey docs;
final report = ONE master table: item → wired (where + proof) /
equivalent-wired (which + proof) / blocked (exact wall + what was tried).
