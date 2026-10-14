# BOX OFFLOAD LOG — 2026-10-14

Pre-reset backup of every git repo and work folder on the shared box. Nothing deleted; no main/default branch touched; no force-push.

Method: WIP snapshot = commit-tree from a temp index (working tree untouched, untracked included, .gitignore respected). Branch refs: `backup/box-2026-10-14/<path-slug>/<branch>`. gitleaks flagged findings (mostly vendored-code false positives like rcheevos aes.c) in every scanned range, so per the rule ALL ref backups went to private **mhvnsnt/box-storage**, not the origin repos. Pushes that box-storage rejected (index-pack fail on full history) were stored as incremental git bundles (restore: clone origin, then `git fetch <bundle> 'refs/*:refs/*'`) on release [box-backup-2026-10-14](https://github.com/mhvnsnt/box-storage/releases/tag/box-backup-2026-10-14), size-verified.

## Git repos with work (backed up by Grok Bot)

| Repo path | Origin | Backed up | Where |
|---|---|---|---|
| `/workspace/mmhq-entrance` | mhvnsnt/money-machine-hq | wip stash-0 stash-1 | box-storage branches `backup/box-2026-10-14/mmhq-entrance/*` |
| `/workspace/Brutal-Fist` | mhvnsnt/Brutal-Fist | wip stash-0 | box-storage branches `backup/box-2026-10-14/Brutal-Fist/*` |
| `/workspace/vten-stages` | mhvnsnt/brutalfistgrokversionten | wip | box-storage branches `backup/box-2026-10-14/vten-stages/*` |
| `/workspace/originalize/pr/AshLanev2` | mhvnsnt/AshLanev2 | wip | box-storage branches `backup/box-2026-10-14/originalize_pr_AshLanev2/*` |
| `/workspace/vten-main-wt` | mhvnsnt/brutalfistgrokversionten | wip | box-storage branches `backup/box-2026-10-14/vten-main-wt/*` |
| `/workspace/brutalfistgrokversioneight` | mhvnsnt/brutalfistgrokversioneight | wip | box-storage branches `backup/box-2026-10-14/brutalfistgrokversioneight/*` |
| `/workspace/mfluid-audit/Mochiichao-Diamond-Version-2d-` | mfluidmusic/Mochiichao-Diamond-Version-2d- | wip | box-storage branches `backup/box-2026-10-14/mfluid-audit_Mochiichao-Diamond-Version-2d-/*` |
| `/workspace/mmhq-cdt` | mhvnsnt/money-machine-hq | stash-0 stash-1 | box-storage branches `backup/box-2026-10-14/mmhq-cdt/*` |
| `/workspace/money-machine-hq` | mhvnsnt/money-machine-hq | stash-0 stash-1 | box-storage branches `backup/box-2026-10-14/money-machine-hq/*` |
| `/workspace/vten-intro-base` | mhvnsnt/brutalfistgrokversionten | wip | box-storage branches `backup/box-2026-10-14/vten-intro-base/*` |
| `/workspace/vten-intro` | mhvnsnt/brutalfistgrokversionten | wip | box-storage branches `backup/box-2026-10-14/vten-intro/*` |
| `/workspace/code-doctor/case-neon` | none | fix/security-hardening main | box-storage branches `backup/box-2026-10-14/code-doctor_case-neon/*` |
| `/workspace/ashlane/base-wt` | mhvnsnt/AshLanev2 | wip | box-storage branches `backup/box-2026-10-14/ashlane_base-wt/*` |
| `/workspace/ashlane/repo` | mhvnsnt/AshLanev2 | wip | box-storage branches `backup/box-2026-10-14/ashlane_repo/*` |
| `/workspace/mmhq-et-v2` | mhvnsnt/money-machine-hq | stash-0 stash-1 | box-storage branches `backup/box-2026-10-14/mmhq-et-v2/*` |
| `/workspace/vten-ci-fix` | mhvnsnt/brutalfistgrokversionten | wip | box-storage branches `backup/box-2026-10-14/vten-ci-fix/*` |
| `/tmp/ashbuild` | mhvnsnt/AshLanev2 | wip | [tmp_ashbuild.bundle](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/tmp_ashbuild.bundle) (bundle) |
| `/workspace/wa/Bannon` | mhvnsnt/Bannon | wip | [wa_Bannon.bundle](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/wa_Bannon.bundle) (bundle) |
| `/workspace/fix/M.-Engine-` | mhvnsnt/M.-Engine- | wip | [fix_M.-Engine-.bundle](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/fix_M.-Engine-.bundle) (bundle) |
| `/workspace/Brutal-Fist/BannonSource` | mhvnsnt/Bannon | wip | [Brutal-Fist_BannonSource.bundle](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/Brutal-Fist_BannonSource.bundle) (bundle) |
| `/workspace/ig/w-Bannon` | mhvnsnt/Bannon | feat/instruction-gate | [ig_w-Bannon.bundle](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/ig_w-Bannon.bundle) (bundle) |
| `/workspace/agent-ops-repo` (re-run) | mhvnsnt/agent-ops | claims/bannon-playtest-paused, claims/kobra-paused | box-storage `backup/box-2026-10-14/agent-ops-repo/*` |

Three repos (western-heart-inventory/western-heart, wh-cs, ig/w-TRIPPEDD) failed initially, then their owners pushed the branches to origin; verified 0 unpushed on re-check.
~40 other repos (mtp/*, ig/*, bible/*) were pushed by Producerbot/Repo Co Dev (origin `backup/box-2026-10-14-*` refs) and verified clean.

## Non-git folders (release assets on box-backup-2026-10-14, local size == remote size)

| Asset | Bytes | SHA-256 |
|---|---|---|
| [folder-bn.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-bn.tar.part00) | 1048576000 | `84e40ed91b2240850888dcc1653940b420380217c4ef4c0358c873fa2b860fe2` |
| [folder-bn.tar.part01](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-bn.tar.part01) | 314798080 | `611d4bf4afd17ed279da117ac454e8b22d657bff19a95feb8489e65ec8647f2c` |
| [folder-kobra-diag.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-kobra-diag.tar.part00) | 141762560 | `cfae9f7e6ba0a883f0dc54cf3915e6bcd47720586853ca4db8fe86b31cb4dbf4` |
| [folder-wh-proof.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-wh-proof.tar.part00) | 129208320 | `b224721d7ca1453013e223abe1fd4872df529361e404b957008252ce499e3361` |
| [folder-pt.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-pt.tar.part00) | 2160640 | `d74ae22784965954750251371fd050ba35f5652209a7350d6b55817e0601bab9` |
| [folder-dlwork.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-dlwork.tar.part00) | 10240 | `c48cb8061d424cdb4128d3025b85679b67beb1147309468d5bf361c4be790143` |
| [folder-gdrive.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-gdrive.tar.part00) | 10240 | `e1c70abfeec527a5093dc3d7460e578811fa582f01f092546d131736e2e88777` |
| [folder-mfluid.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-mfluid.tar.part00) | 10240 | `ea7c855df8da4e60f208ae0b1b497629d16d691c5577825fc9bfc2f7cad9e555` |
| [folder-offload-tmp.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-offload-tmp.tar.part00) | 10240 | `b03b299a5d84432a6a3b22b0cd0d79fdbf5c8f0e8569a03098571f50b34429df` |
| [folder-playtest.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-playtest.tar.part00) | 225280 | `a2135c2a8318aeca29cfb12ed350bcb7cf9764b60ca1f9abe6acb6fd5a3c179b` |
| [folder-studio-consumers.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-studio-consumers.tar.part00) | 10240 | `0919513c26c488f92551b82c6045e3b1c4c03cf4b06124f9e97973f06e3105e5` |
| [folder-cc0-assets.tar.part00](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/folder-cc0-assets.tar.part00) | 10240 | `7690dbed4d53a135628939753237ffbd5e623a9cf43a452fcea8e9ff8233076d` |
| [mmhq-venv-requirements.txt](https://github.com/mhvnsnt/box-storage/releases/download/box-backup-2026-10-14/mmhq-venv-requirements.txt) | 537 | `1282af8b6e53aa94e6506dc96250401ee39b06a0a8dfb9c835c8c64fdf0b5f01` |
| mocap-venv-requirements.txt | 1508 | (venv: package list only; rebuildable) |

The other /workspace folders were tarred by Producerbot to box-storage releases `box-2026-10-14-folder-<name>` (game-kits, oss, rig-repair, tekken-ref, mmhq-autoreply, etc.).

## Verification

Every local branch tip that isn't on a remote matches a box-storage backup ref SHA or a bundled ref; every stash SHA is on box-storage; every dirty tree has a WIP snapshot. Result: **0 missing**.

## Follow-up pass (bk2.sh / ng.sh run, verified ~5:00 PM CT)

Second scheme, run from `/home/box/offload`: branches `backup/box-2026-10-14-<slug>[-<branch>|-wip|-stash-N]` pushed to each clone's **own origin**, ignored/large files and non-git folders as streamed tar parts on **mhvnsnt/box-storage** releases `box-2026-10-14-*`. Full per-line log: `/home/box/offload/log.tsv` on the box (summarized here).

- Clones processed: 94 roots in `roots.txt`, every one has a final STATUS line. Re-check now: all report `git log --branches --not --remotes` = 0, except the URL-pushed ones below (remote SHA verified with `git ls-remote`).
- Re-ran after new agent commits: `/workspace/agent-ops-repo` (claims/kobra-paused, claims/bannon-playtest-paused), `/workspace/wh-cs` (pr118 + wip).
- `/workspace/ig/w-Bannon` feat/instruction-gate: remote backup branch = 7a388cf880 (local tracking ref couldn't be written because the disk was full).
- Non-git folders: all 44 in `folders.txt` have release parts on box-storage (`box-2026-10-14-folder-*`).
- Release integrity: all 71 RELEASE lines match the GitHub asset sha256 digest. Re-downloaded and re-hashed: folder-mfluid-audit, folder-code-doctor, and the two retried tmp-build-*Mochiichao* tars — all OK.

### New private repo mhvnsnt/box-orphans
| Source | Where | Verified |
|---|---|---|
| `/workspace/code-doctor/case-neon` (no remote) | branches `case-neon/main` d6a812d2b5, `case-neon/fix/security-hardening` 4ed531cac6; ignored files on release `box-2026-10-14-code-doctor-case-neon-ignored` | ls-remote SHA match; sha256 17bae1de4446… |
| `/tmp/tgt` (no remote) | branch `tmp-tgt/master` 16b2fec7cd | ls-remote SHA match |
| `mfluid-audit/Mochiichao-Diamond-Version-2d-` proof/ + tools/ (upstream push 403) | branch `mfluid-mochiichao-proof-tools` 5ac400e84d (9 files) | file list match |
| `/workspace/mmhq-autoreply` (orphaned worktree, parent /workspace/mmhq gone) | release `box-2026-10-14-folder-mmhq-autoreply` | sha256 97c534ecadd4… |

### gitleaks on backup branches (origin/main..branch)
124 branches scanned. Findings (values masked to 6 chars, history NOT rewritten):
- mhvnsnt/Bannon (private) `start-autonomous-agent.ts:15`, `src/services/repoSyncService.ts:213`: github-fine-grained-pat `github…` — **already on Bannon main**, hardcoded fallback token. Recommend revoking/rotating it.
- mhvnsnt/Brutal-Fist (private) `firebase-applet-config.json:4` and Bannon `godmode/firebase-applet-config.json`: Firebase web key `AIzaSy…` (client key, low risk).
- 127 generic-api-key hits in bundled HTML/JS (`public/index.html`, `merged_BANNON_v150.html`) and 1 in `/tmp/ashbuild/.vercel` output: false positives (identifiers like brick…/combat…).
- box-orphans, wh-cs and agent-ops-repo new branches: clean.

## Pass 2 (after interruption, ~4:30 PM CT)

Re-scanned 99 `.git` entries across the box (/workspace, /tmp, /home/box). Refs already on remotes were skipped; WIP trees identical to the pass-1 snapshot were skipped.

| Repo path | New backup | Where |
|---|---|---|
| `/workspace/pt-ops` | claims/playtest-2026-10-14 | box-storage `backup/box-2026-10-14/pt-ops/*` |
| `/tmp/ceh` | feat/private-cloud-console | mhvnsnt/chimera-emulator-hub (private) `backup/box-2026-10-14/tmp_ceh/*` |
| `/workspace/wh-qa` (new clone) | grok/wh-playtest-qa + WIP (untracked build/) | mhvnsnt/western-heart (private) `backup/box-2026-10-14/wh-qa/*` |
| `/workspace/wh-cs` | WIP (lab/game/scripts/main.gd) | mhvnsnt/western-heart `backup/box-2026-10-14/wh-cs/wip2` |
| `/workspace/bn/b` | fix/perf-lazy-clips-debug-flag-version-stamp | mhvnsnt/Bannon (private) `backup/box-2026-10-14/bn_b/*` |

These four box-storage pushes failed (index-pack on full history), so they went to the private origin repos; gitleaks on the new commits reported no leaks.

Final verification: 94 of 99 entries OK. Every unpushed branch tip, stash and dirty tree matched a SHA on a remote. The other 5: 3 were confirmed by `ls-remote origin` SHA match. `/tmp/backend-plugin-bpPnXV` is an empty repo with no commits or files, so there was nothing to back up. `/workspace/mmhq-autoreply` is a broken worktree (its parent `/workspace/mmhq` is gone); its files are in Producerbot's release `box-2026-10-14-folder-mmhq-autoreply`.
