# T6 Recon Handoff — 2026-10-16

**Status:** Local `~/workspace/game-reverse-engineering/tekken6/` cleared from disk 2026-10-16 per owner order (PUSH-AND-CLEAR, disc cleaner chad chat). The work continues from GitHub.

## What the work is

Tekken 6 (PSP) full teardown for Western Heart. The recon pipeline: extract everything
from the game files → Blender pose renders → AI generation on top for proprietary-universe
character renders → all model extractions feed Western Heart (chimera build).

- 40-fighter roster documented (6 T6 newcomers: Alisa, Bob, Lars, Leo, Miguel, Zafina)
- 46 ending/opening PMF videos extracted (337MB) + 42 reference frames
- ISO file-structure map; customization system research doc (template for Western Heart's system)
- Decrypt lane: EBOOT decrypt call graph FULLY reversed (runtime VAs documented),
  K1K2 key extraction validated against machine code, bulk-decrypt tooling in tools/
- Bob Richards owner-flagged as Western Heart candidate

## Where it lives (GitHub)

**Release (full tree backup):**
- Repo: `mhvnsnt/western-heart`
- Tag: `tekken6-recon-20261016`
- Asset: `t6-recon-backup.tar` split into 3 parts (proxy flaky on 1.1G single upload):
  `t6-recon-backup.tar.part-aa` 524,288,000B +
  `t6-recon-backup.tar.part-ab` 524,288,000B +
  `t6-recon-backup.tar.part-ac` 82,708,480B = 1,131,284,480B total
- sha256: `2c738b24f46395960e463fd03c637b038a0942590c0055b9ef3fe1bc9d77afcc`
- Reassemble: `cat t6-recon-backup.tar.part-aa t6-recon-backup.tar.part-ab t6-recon-backup.tar.part-ac > t6-recon-backup.tar`
- Verified: all 3 asset sizes byte-match local parts exactly (own-eyes `gh release view`, 2026-10-16); release published (not draft)
- Contents: `decrypted/` `extracted/` `docs/` `tools/` `work/` (incl. `work/landing/wh-clone`
  with feature branch), `TEARDOWN.md`, `PPSSPP-LIVE-RUN-GUIDE.md`
- URL: https://github.com/mhvnsnt/western-heart/releases/tag/tekken6-recon-20261016
- Verified: asset size byte-matches local tar (own-eyes `gh release view`, 2026-10-16)

**Live feature branch:**
- Repo: `mhvnsnt/western-heart`, branch `feature/tekken6-100-teardown`
- Tip at clear time: `9ae91ce` ("T6 recon WIP 2026-10-16 — disk-clear checkpoint")
- Prior: `e5476ee` (NDPP format doc + bounding-volume GLB, 1103 boxes / 357 sections)

**Also on GitHub already:** ISO on release `tekken6-psp-v1` (855,638,016B, byte-identical);
per-game copy on `mhvnsnt/game-reverse-engineering` release `tekken6-psp-v1`.

## Done vs next (from TEARDOWN.md + checkpoints)

Done: ISO verified · structure mapped · 46 videos + 42 ref frames extracted · 40-fighter
roster · customization system doc · decrypt call graph reversed · bulk-decrypt tooling.
Checkpoints: `tekken6-teardown.json`, `tekken6-teardown-complete.json`, `t6-bulk-decrypt.json`,
`t6-live-dump.json`, `tekken6-data401-decrypt.json` (in `~/workspace/agent-ops/checkpoints/`).

Next (blocked on PSP/Namco encryption): character models (GMO), textures (TIM2/GIM),
stages, animation data, customization meshes, EBOOT full decryption. Future path is
documented in TEARDOWN.md ("Future Path" section). Idle-queue entry #4 holds the thread.

## Exact pickup commands

```bash
# Full tree backup:
gh release download tekken6-recon-20261016 --repo mhvnsnt/western-heart
tar -xf t6-recon-backup.tar

# Live branch work:
git clone --branch feature/tekken6-100-teardown https://github.com/mhvnsnt/western-heart.git
cd western-heart && git log --oneline -5
```

## Notes for the next agent

- The tar contains `work/landing/wh-clone/.git` (sparse checkout, blob:none) — the branch
  push above is the canonical live state; prefer the branch over the tar's embedded clone.
- Do NOT re-extract the ISO from scratch: the release tar + branch hold everything.
- Recon pattern going forward (owner 2026-10-16 ~19:00 EDT): push 100% to GitHub
  (release assets + live feature branch), write a handoff doc like this one, then clear local.
