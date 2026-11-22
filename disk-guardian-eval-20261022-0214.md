# Disk Guardian Evaluation — 2026-10-22 ~02:45 CDT
**Run context:** disk at 89% (hard ceiling 88%), must free ~19GB to get below 70%.
**IN-FLIGHT (sacred, untouched):** `.r8-stage/pp-storeoff` (streaming `personality-pass-20261022.tar`, 14+ parts OK) and `.r8-stage/rigwork-storeoff` (streaming `rigwork-tmp-20261022.tar`, 16+ parts OK) are ACTIVE lanes. Sources = `~/workspace/_wh-work/personality-pass` (4.4G) and `~/workspace/rigwork-tmp` (12G) — DO NOT TOUCH until lanes verify+clear themselves.

## SAFE-TO-CLEAR (ranked)

1. **`~/workspace/_t6r4-work/iso/tekken6-psp.iso`** — 855,638,016 bytes. **SHA256 VERIFIED byte-identical** to GitHub release asset `tekken6-psp.iso` on `mhvnsnt/western-heart` tag `tekken6-psp-v1` (hash `b5e52660a52caeca351e93c54bb4db0011325af0c1e3c67230bddde8f7cecf44` both sides; also mirrored on `mhvnsnt/game-reverse-engineering` `tekken6-psp-v1`). ONE-STORE RULE satisfied (2 stores). Not active teardown (recon work idle since 10-21). Pull-back: `gh release download tekken6-psp-v1 --repo mhvnsnt/western-heart`.
   - `rm -f ~/workspace/_t6r4-work/iso/tekken6-psp.iso` → **0.80 GB**
2. **`~/workspace/_w7b-wh/`** — 2.2G. Git repo: clean (0 dirty), branch `gap/w7d-t5-ctype5-decode-20261021`, HEAD `8afbef63fa4a` == origin. Gap W7d verdict landed (WH #521 OPEN on origin branch). Safe per rule 5.
   - `rm -rf ~/workspace/_w7b-wh` → **2.2 GB**
3. **`~/workspace/wh-godot-slice/`** — 1.4G. Git repo: clean, branch `feat/godot-slice-20261021`, HEAD `c6afc5b3214f` == origin. Safe per rule 5.
   - `rm -rf ~/workspace/wh-godot-slice` → **1.4 GB**
4. **`~/workspace/ur-phase3-work/wh/`** — 2.0G. Git worktree: clean, branch `ur-phase5-names-polish`, HEAD `c76eaaa8c535` == origin. Safe per rule 5.
   - `rm -rf ~/workspace/ur-phase3-work/wh` → **2.0 GB**
5. **`~/workspace/_docfrank-feet/wh/`** — 1.6G. Git worktree: clean, branch `fix/docfrank-feet-rootcause-20261021`, HEAD `2a567d9c4b05` == origin. Fix PR #508 MERGED. Safe per rule 5.
   - `rm -rf ~/workspace/_docfrank-feet/wh` → **1.6 GB**
6. **`~/workspace/scii-work/p13/wh/`** — 539M. Git: clean, branch `scii-phase14-stages-costumes-av`, HEAD `e0f6a9d6f627` == origin. Safe per rule 5.
   - `rm -rf ~/workspace/scii-work/p13/wh` → **0.5 GB**
7. **`~/workspace/_docfrank-rig/wh/`** — 855M. Git: HEAD `c54f328338a8` == origin; only untracked items are 3 regenerable `__pycache__/` dirs. Safe per rule 5.
   - `rm -rf ~/workspace/_docfrank-rig/wh` → **0.86 GB**
8. **`~/workspace/_t6r4-work/venv/`** — 82M. Python venv. Per rule 7: `~/workspace/_t6r4-work/venv/bin/pip freeze > ~/workspace/agent-ops/venv-manifests/_t6r4-work-requirements.txt` first, then rm.
   - → **0.08 GB**

**Total reclaimable from SAFE list: ~9.4 GB.** Below the ~19GB target — remainder must come from mirroring the BLOCKED items (recommend storeoff lanes for `_doa4p2-scratch`, `scii-work` game chunks, `wh-pose-survey`, `_w3b-work/wh`, `_cs-round2-work` untracked proofs).

## BLOCKED / UNCERTAIN
- `~/workspace/rigwork-tmp/` (12G) — **IN-FLIGHT**: source of active `rigwork-storeoff` lane streaming to release `rigwork-tmp-20261022`. Sacred. Clears itself on verify.
- `~/workspace/_wh-work/` (5.3G) — `personality-pass/` (4.4G) **IN-FLIGHT** (active `pp-storeoff` lane). `pp-repo/` (624M) has uncommitted work (modified `game/js/assets.js` + untracked `model-rigged.glb` files) — not clean, not backed up → blocked until committed/pushed.
- `~/workspace/cape-jones/` (6.9G) — **NOT clean**: 10,403 dirty lines incl. deletions in `animation-study/donor/` + untracked blend files. Blocked.
- `~/workspace/_cs-round2-work/` (3.3G) — HEAD `82fa3e3c0060` == origin, but ~120MB of untracked proof GLBs/PNGs (`customization/tools/proof/…`) not backed up → whole-dir clear blocked. Recommend: storeoff the proof dir, then clear entire checkout (tracked portion safe).
- `~/workspace/wh-pose-survey/` (4.1G) — no git; rigwork/models/work GLBs, no archive release found. Blocked (needs mirror lane).
- `~/workspace/_w3b-work/wh/` (1.6G) — **broken linked worktree** (`.git` points at deleted `~/workspace/_cornerstone-work/wh/.git/worktrees/wh1`). Cannot verify HEAD. Blocked; needs storeoff of content or re-clone-compare.
- `~/workspace/_t6r4-work/` remainder — `iso/` cleared above; `recon/` (1.5G), `bulk_decrypted_r6.bin` (367M), `ppsspp/` (259M): game teardown files, no verified store copy → BLOCKED (ONE-STORE RULE, no archive release found).
- `~/workspace/_doa4p2-scratch/` (1.7G) — DOA game extraction (`afsdl/`, `p8–p11`); game files, no archive release → BLOCKED.
- `~/workspace/scii-work/` remainder — `p10` (607M), `p2` (132M): SCII game chunks, no archive → BLOCKED.
- `~/workspace/tools/` (15G) — `blender/` (1.5G) persistent keep per TOOLS.md. `blender42/` (1.3G), `blender-4.5/` (1.2G), `godot/` (1.6G), `ghidra/` (1.3G), `android-sdk/` (721M), `natron/` (720M): installed tool binaries, not scratch; re-downloadable but are the owner's tools — **no delete without his say** (uncertain, needs his call).
- `~/workspace/_docfrank-rig/scratch/` (1.8G), `/tmp/` (127M), `_doa4p2-scratch` logs — no git, no store → blocked pending mirror.

## Notes
- The local file hash check above was the only byte-verify performed; all git "pushed" claims verified via `git ls-remote origin <branch>` matching local HEAD this run.
- Log destinations per guardian: deletions → `~/workspace/agent-ops/disk-cleanup-log.md`; venv manifests → `~/workspace/agent-ops/venv-manifests/`.
