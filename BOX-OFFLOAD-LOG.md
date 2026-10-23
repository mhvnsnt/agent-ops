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

## Producerbot (Grok Bot) pass, 2026-10-14 (second, independent sweep)

Nothing deleted locally except one clean, fully pushed clone (/workspace/mtp/chimera-emulator-hub, 296K, backed up first). Main was never touched and nothing was force-pushed. Refs are `backup/box-2026-10-14-<path-slug>-<branch|wip|stash-N>` (hyphenated, so they can't clash with MoneyManBusch's `backup/box-2026-10-14/<dir>/...` refs). Each one was pushed to the clone's origin and verified with `git ls-remote`. Repos without a usable origin (no remote, or a 403) were pushed to the private mhvnsnt/box-storage. A WIP snapshot is a commit-tree built from a temp index, so the working tree stays untouched. The two WIP refs on public repos (M.-Engine- gradlew mode change, brutalfistgrokversioneight submodule pointer) contain no file content.

### Per-clone audit (porcelain | unpushed | stash | wip ref | uncovered)

Unpushed>0 rows: each local branch tip was verified on the remote under a backup ref (ls-remote); the counter is non-zero only because the remote-tracking ref couldn't be written while / was at 100%. Porcelain>0 rows: saved as the `-wip` ref; working tree left as-is because agents are using them.

| Path | porcelain | unpushed | stash | wip | uncovered |
|---|---|---|---|---|---|
| `/dev/shm/ao` | 0 | 3 | 0 | n/a | none |
| `/tmp/ashbuild` | 41 | 0 | 0 | wip-ref-on-remote | none |
| `/tmp/backend-plugin-bpPnXV` | 0 | 0 | 0 | n/a | none |
| `/tmp/backend-plugin-ca8enF` | 0 | 0 | 0 | n/a | none |
| `/tmp/build-M.-OS-Mochiichao-Chrome-Version-` | 0 | 0 | 0 | n/a | none |
| `/tmp/build-Mochiichao-Diamond-Version-2d-` | 0 | 0 | 0 | n/a | none |
| `/tmp/build-Neon-App-Builder` | 0 | 0 | 0 | n/a | none |
| `/tmp/ceh` | 0 | 1 | 0 | n/a | none |
| `/tmp/neonb` | 0 | 0 | 0 | n/a | none |
| `/tmp/tgt` | 0 | 1 | 0 | n/a | none |
| `/workspace/Brutal-Fist/BannonSource` | 33 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/Brutal-Fist` | 8 | 0 | 1 | wip-ref-on-remote | none |
| `/workspace/TRIPPEDD-Production-studios-` | 0 | 0 | 0 | n/a | none |
| `/workspace/agent-ops-repo` | 0 | 0 | 0 | n/a | none |
| `/workspace/ao-tt` | 0 | 0 | 0 | n/a | none |
| `/workspace/arl` | 0 | 0 | 0 | n/a | none |
| `/workspace/ashlane/base-wt` | 1 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/ashlane/play` | 0 | 0 | 0 | n/a | none |
| `/workspace/ashlane/repo` | 3 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/bible/Bannon` | 0 | 0 | 0 | n/a | none |
| `/workspace/bible/God-Molecule-Show-Studio` | 0 | 0 | 0 | n/a | none |
| `/workspace/bible/TRIPPEDD-Production-studios-` | 0 | 0 | 0 | n/a | none |
| `/workspace/bn/b` | 0 | 1 | 0 | n/a | none |
| `/workspace/brutalfistgrokversioneight` | 1 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/code-doctor/case-neon` | 0 | 3 | 0 | n/a | none |
| `/workspace/fix/AshLanev2` | 0 | 0 | 0 | n/a | none |
| `/workspace/fix/Bannon` | 0 | 0 | 0 | n/a | none |
| `/workspace/fix/Brutal-Fist` | 0 | 0 | 0 | n/a | none |
| `/workspace/fix/CODEDUMMY` | 0 | 0 | 0 | n/a | none |
| `/workspace/fix/M.-Engine-` | 1 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/fix/T` | 0 | 0 | 0 | n/a | none |
| `/workspace/fix/brutalfistgrokversion12` | 0 | 0 | 0 | n/a | none |
| `/workspace/fix/brutalfistgrokversionten` | 0 | 0 | 0 | n/a | none |
| `/workspace/ig/w-AshLanev2` | 0 | 0 | 0 | n/a | none |
| `/workspace/ig/w-Bannon` | 0 | 1 | 0 | n/a | none |
| `/workspace/ig/w-BioMechania` | 0 | 0 | 0 | n/a | none |
| `/workspace/ig/w-ConcreteDragon` | 0 | 0 | 0 | n/a | none |
| `/workspace/ig/w-God-Molecule-Show-Studio` | 0 | 0 | 0 | n/a | none |
| `/workspace/ig/w-TRIPPEDD-Production-studios-` | 0 | 0 | 0 | n/a | none |
| `/workspace/ig/w-agent-ops` | 0 | 0 | 0 | n/a | none |
| `/workspace/ig/w-money-machine-hq` | 0 | 0 | 0 | n/a | none |
| `/workspace/ig/w-western-heart` | 0 | 0 | 0 | n/a | none |
| `/workspace/kobra-fix` | 0 | 0 | 0 | n/a | none |
| `/workspace/mfluid-audit/Mochiichao-Diamond-Version-2d-` | 2 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/mmhq-autoreply` | not-a-repo (broken worktree link) |  |  |  |  |
| `/workspace/mmhq-cdt` | 0 | 0 | 2 | n/a | none |
| `/workspace/mmhq-cd` | 0 | 0 | 0 | n/a | none |
| `/workspace/mmhq-entrance` | 3 | 0 | 2 | wip-ref-on-remote (re-verified) | none |
| `/workspace/mmhq-et-v2` | 0 | 0 | 2 | n/a | none |
| `/workspace/money-machine-hq` | 0 | 0 | 2 | n/a | none |
| `/workspace/mtp/AshLane-prototype` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/AshLanev2` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/Bannon` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/BioMechania` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/Brutal-Fist` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/CODEDUMMY` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/Forge3D` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/God-Mode-OS-D3MN-V2` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/M.-Engine-` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/Moneymachine-private` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/Moneymachine` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/M` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/TRIPPEDD-Production-studios-` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/URBAN-MAYHEM-` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/agent-ops` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfist11` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversion12` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversion9` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversioneight` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversionfive` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversionfour` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversionseven` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversionsix` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversiontenpointfive` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversionten` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversionthree` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversiontwo` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/brutalfistgrokversion` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/mmhq` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/theyard` | 0 | 0 | 0 | n/a | none |
| `/workspace/mtp/western-heart` | 0 | 0 | 0 | n/a | none |
| `/workspace/originalize/pr/AshLanev2` | 51 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/oss-anim-staging/_raw/git/bandai` | 0 | 0 | 0 | n/a | none |
| `/workspace/oss-anim-staging/_raw/git/cmu-mocap` | 0 | 0 | 0 | n/a | none |
| `/workspace/oss-anim-staging/_raw/git/mesh2motion-app` | 0 | 0 | 0 | n/a | none |
| `/workspace/oss-anim-staging/_raw/git/mesh2motion-assets` | 0 | 0 | 0 | n/a | none |
| `/workspace/pt-ops` | 0 | 1 | 0 | n/a | none |
| `/workspace/ref-repos/Bannon` | 0 | 0 | 0 | n/a | none |
| `/workspace/studio-pipeline` | 0 | 0 | 0 | n/a | none |
| `/workspace/vten-ci-fix` | 15 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/vten-intro-base` | 1 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/vten-intro` | 3 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/vten-main-wt` | 3 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/vten-stages` | 3 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/wa/Bannon` | 1 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/wa/TRIPPEDD-Production-studios-` | 0 | 0 | 0 | n/a | none |
| `/workspace/wa/money-machine-hq` | 0 | 0 | 0 | n/a | none |
| `/workspace/western-heart-inventory/western-heart` | 0 | 0 | 0 | n/a | none |
| `/workspace/wh-cs` | 1 | 0 | 0 | wip-ref-on-remote | none |
| `/workspace/wh-qa` | 1 | 1 | 0 | wip-ref-on-remote | none |

### Refs pushed

- `Brutal-Fist-BannonSource`: PUSHED uncommitted-snapshot(33 paths) -> https://github.com/mhvnsnt/Bannon.git branch backup/box-2026-10-14-Brutal-Fist-BannonSource-wip @ 2859dacbf9
- `Brutal-Fist`: PUSHED branch:grok/anim-euler-gate-wire -> https://github.com/mhvnsnt/Brutal-Fist.git branch backup/box-2026-10-14-Brutal-Fist-grok-anim-euler-gate-wire @ 4b475c6dd8
- `Brutal-Fist`: PUSHED stash@{0} -> https://github.com/mhvnsnt/Brutal-Fist.git branch backup/box-2026-10-14-Brutal-Fist-stash-0 @ 95f3e6827e
- `Brutal-Fist`: PUSHED uncommitted-snapshot(8 paths) -> https://github.com/mhvnsnt/Brutal-Fist.git branch backup/box-2026-10-14-Brutal-Fist-wip @ 61d588cad4
- `agent-ops-repo`: PUSHED branch:claims/bannon-playtest-paused -> https://github.com/mhvnsnt/agent-ops.git branch backup/box-2026-10-14-agent-ops-repo-claims-bannon-playtest-paused @ 61c3a10189
- `agent-ops-repo`: PUSHED branch:claims/kobra-paused -> https://github.com/mhvnsnt/agent-ops.git branch backup/box-2026-10-14-agent-ops-repo-claims-kobra-paused @ 440b0755dc
- `agent-ops-repo`: PUSHED branch:docs/grokbot-activity-proof-2026-10-14 -> https://github.com/mhvnsnt/agent-ops.git branch backup/box-2026-10-14-agent-ops-repo-docs-grokbot-activity-proof-2026-10-14 @ be58f503ab
- `ashlane-base-wt`: PUSHED branch:grok/ashlane-crash-spawn-rig -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-ashlane-base-wt-grok-ashlane-crash-spawn-rig @ 0d8e091100
- `ashlane-base-wt`: PUSHED branch:grok/cf-pages-base-path -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-ashlane-base-wt-grok-cf-pages-base-path @ fe6be4ced2
- `ashlane-base-wt`: PUSHED branch:grok/makerig-crash-fix -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-ashlane-base-wt-grok-makerig-crash-fix @ af2ff5b782
- `ashlane-base-wt`: PUSHED uncommitted-snapshot(1 paths) -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-ashlane-base-wt-wip @ 6148320033
- `ashlane-repo`: PUSHED uncommitted-snapshot(3 paths) -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-ashlane-repo-wip @ 12f9417e1a
- `bible-Bannon`: PUSHED branch:ci/pr-clean-merge-and-bible -> https://github.com/mhvnsnt/Bannon.git branch backup/box-2026-10-14-bible-Bannon-ci-pr-clean-merge-and-bible @ 6636ad5432
- `bible-God-Molecule-Show-Studio`: PUSHED branch:ci/pr-validate-latest-check -> https://github.com/mhvnsnt/God-Molecule-Show-Studio.git branch backup/box-2026-10-14-bible-God-Molecule-Show-Studio-ci-pr-validate-latest-check @ 758365de39
- `bible-TRIPPEDD-Production-studios-`: PUSHED branch:ci/pr-clean-merge-and-bible -> https://github.com/mhvnsnt/TRIPPEDD-Production-studios-.git branch backup/box-2026-10-14-bible-TRIPPEDD-Production-studios--ci-pr-clean-merge-and-bible @ 7efcfbdde7
- `bn-b`: PUSHED branch:fix/perf-lazy-clips-debug-flag-version-stamp -> https://github.com/mhvnsnt/Bannon.git branch backup/box-2026-10-14-bn-b-fix-perf-lazy-clips-debug-flag-version-stamp @ 63643c5e65
- `brutalfistgrokversioneight`: PUSHED uncommitted-snapshot(1 paths) -> https://github.com/mhvnsnt/brutalfistgrokversioneight.git branch backup/box-2026-10-14-brutalfistgrokversioneight-wip @ 8607d60a85
- `code-doctor-case-neon`: PUSHED branch:fix/security-hardening -> https://github.com/mhvnsnt/box-storage.git branch backup/box-2026-10-14-code-doctor-case-neon-fix-security-hardening @ 4ed531cac6
- `code-doctor-case-neon`: PUSHED branch:main -> https://github.com/mhvnsnt/box-storage.git branch backup/box-2026-10-14-code-doctor-case-neon-main @ d6a812d2b5
- `dev-shm-ao`: PUSHED branch:grok/box-offload-log-2026-10-14 -> https://github.com/mhvnsnt/agent-ops.git branch backup/box-2026-10-14-dev-shm-ao-grok-box-offload-log-2026-10-14 @ 89107185f8
- `fix-AshLanev2`: PUSHED branch:fix/duplicate-chaindivider -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-fix-AshLanev2-fix-duplicate-chaindivider @ 8cc2ed0afd
- `fix-Bannon`: PUSHED branch:fix/ci-workflow-yaml-node22 -> https://github.com/mhvnsnt/Bannon branch backup/box-2026-10-14-fix-Bannon-fix-ci-workflow-yaml-node22 @ cf2df913b8
- `fix-Brutal-Fist`: PUSHED branch:fix/ci-submodule-checkout -> https://github.com/mhvnsnt/Brutal-Fist branch backup/box-2026-10-14-fix-Brutal-Fist-fix-ci-submodule-checkout @ 3a816abac4
- `fix-M.-Engine-`: PUSHED uncommitted-snapshot(1 paths) -> https://github.com/mhvnsnt/M.-Engine- branch backup/box-2026-10-14-fix-M.-Engine--wip @ eac8095e76
- `fix-T`: PUSHED branch:fix/typecheck-dup-rubberband -> https://github.com/mhvnsnt/TRIPPEDD-Production-studios- branch backup/box-2026-10-14-fix-T-fix-typecheck-dup-rubberband @ 6a3c8e6b56
- `fix-brutalfistgrokversion12`: PUSHED branch:fix/ci-ground-particle-static-shell -> https://github.com/mhvnsnt/brutalfistgrokversion12 branch backup/box-2026-10-14-fix-brutalfistgrokversion12-fix-ci-ground-particle-static-shell @ 0af523f42d
- `ig-w-AshLanev2`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-ig-w-AshLanev2-feat-instruction-gate @ 93e820f2f5
- `ig-w-Bannon`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/Bannon branch backup/box-2026-10-14-ig-w-Bannon-feat-instruction-gate @ 7a388cf880
- `ig-w-BioMechania`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/BioMechania branch backup/box-2026-10-14-ig-w-BioMechania-feat-instruction-gate @ b65dff97db
- `ig-w-ConcreteDragon`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/ConcreteDragon branch backup/box-2026-10-14-ig-w-ConcreteDragon-feat-instruction-gate @ e8dababf8c
- `ig-w-God-Molecule-Show-Studio`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/God-Molecule-Show-Studio branch backup/box-2026-10-14-ig-w-God-Molecule-Show-Studio-feat-instruction-gate @ 7fbc3430e0
- `ig-w-TRIPPEDD-Production-studios-`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/TRIPPEDD-Production-studios- branch backup/box-2026-10-14-ig-w-TRIPPEDD-Production-studios--feat-instruction-gate @ ef9f5c7081
- `ig-w-agent-ops`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/agent-ops branch backup/box-2026-10-14-ig-w-agent-ops-feat-instruction-gate @ ca32c44b98
- `ig-w-money-machine-hq`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/money-machine-hq branch backup/box-2026-10-14-ig-w-money-machine-hq-feat-instruction-gate @ c9f580ef0e
- `ig-w-western-heart`: PUSHED branch:feat/instruction-gate -> https://github.com/mhvnsnt/western-heart branch backup/box-2026-10-14-ig-w-western-heart-feat-instruction-gate @ 86f3b51a53
- `mfluid-audit-Mochiichao-Diamond-Version-2d-`: PUSHED uncommitted-snapshot(2 paths) -> https://github.com/mhvnsnt/box-storage.git branch backup/box-2026-10-14-mfluid-audit-Mochiichao-Diamond-Version-2d--wip @ bee108eabb
- `mmhq-cdt`: PUSHED stash@{0} -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-mmhq-cdt-stash-0 @ 739bd69af8
- `mmhq-cdt`: PUSHED stash@{1} -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-mmhq-cdt-stash-1 @ 467cd24829
- `mmhq-entrance`: PUSHED stash@{0} -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-mmhq-entrance-stash-0 @ 739bd69af8
- `mmhq-entrance`: PUSHED stash@{1} -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-mmhq-entrance-stash-1 @ 467cd24829
- `mmhq-entrance`: PUSHED uncommitted-snapshot(3 paths) -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-mmhq-entrance-wip @ bcf96ce9e4
- `mmhq-et-v2`: PUSHED stash@{0} -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-mmhq-et-v2-stash-0 @ 739bd69af8
- `mmhq-et-v2`: PUSHED stash@{1} -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-mmhq-et-v2-stash-1 @ 467cd24829
- `money-machine-hq`: PUSHED stash@{0} -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-money-machine-hq-stash-0 @ 739bd69af8
- `money-machine-hq`: PUSHED stash@{1} -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-money-machine-hq-stash-1 @ 467cd24829
- `mtp-AshLane-prototype`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/AshLane-prototype branch backup/box-2026-10-14-mtp-AshLane-prototype-docs-muse-training-pack-link @ caaa5607df
- `mtp-AshLanev2`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-mtp-AshLanev2-docs-muse-training-pack-link @ 8684c81e15
- `mtp-Bannon`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/Bannon branch backup/box-2026-10-14-mtp-Bannon-docs-muse-training-pack-link @ 2f5c7b4b79
- `mtp-BioMechania`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/BioMechania branch backup/box-2026-10-14-mtp-BioMechania-docs-muse-training-pack-link @ 0b6f664606
- `mtp-Brutal-Fist`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/Brutal-Fist branch backup/box-2026-10-14-mtp-Brutal-Fist-docs-muse-training-pack-link @ 2b85cecf65
- `mtp-CODEDUMMY`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/CODEDUMMY branch backup/box-2026-10-14-mtp-CODEDUMMY-docs-muse-training-pack-link @ ee8d68f552
- `mtp-Forge3D`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/Forge3D branch backup/box-2026-10-14-mtp-Forge3D-docs-muse-training-pack-link @ 7311bc817e
- `mtp-God-Mode-OS-D3MN-V2`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/God-Mode-OS-D3MN-V2 branch backup/box-2026-10-14-mtp-God-Mode-OS-D3MN-V2-docs-muse-training-pack-link @ a308712d7f
- `mtp-M.-Engine-`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/M.-Engine- branch backup/box-2026-10-14-mtp-M.-Engine--docs-muse-training-pack-link @ 8559997194
- `mtp-M`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/M-Hero-Simulator- branch backup/box-2026-10-14-mtp-M-docs-muse-training-pack-link @ f8eadb9fa1
- `mtp-Moneymachine-private`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/Moneymachine-private branch backup/box-2026-10-14-mtp-Moneymachine-private-docs-muse-training-pack-link @ adcc14acd6
- `mtp-Moneymachine`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/Moneymachine branch backup/box-2026-10-14-mtp-Moneymachine-docs-muse-training-pack-link @ 9ad6ecf73a
- `mtp-TRIPPEDD-Production-studios-`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/TRIPPEDD-Production-studios- branch backup/box-2026-10-14-mtp-TRIPPEDD-Production-studios--docs-muse-training-pack-link @ 6476068d5c
- `mtp-URBAN-MAYHEM-`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/URBAN-MAYHEM- branch backup/box-2026-10-14-mtp-URBAN-MAYHEM--docs-muse-training-pack-link @ 307feca060
- `mtp-agent-ops`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/agent-ops branch backup/box-2026-10-14-mtp-agent-ops-docs-muse-training-pack-link @ 68243c6086
- `mtp-brutalfist11`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfist11 branch backup/box-2026-10-14-mtp-brutalfist11-docs-muse-training-pack-link @ fcbe5b5a6d
- `mtp-brutalfistgrokversion12`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversion12 branch backup/box-2026-10-14-mtp-brutalfistgrokversion12-docs-muse-training-pack-link @ 03056c95fa
- `mtp-brutalfistgrokversion9`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversion9 branch backup/box-2026-10-14-mtp-brutalfistgrokversion9-docs-muse-training-pack-link @ 0ed374f89a
- `mtp-brutalfistgrokversion`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversion branch backup/box-2026-10-14-mtp-brutalfistgrokversion-docs-muse-training-pack-link @ 49500a9a24
- `mtp-brutalfistgrokversioneight`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversioneight branch backup/box-2026-10-14-mtp-brutalfistgrokversioneight-docs-muse-training-pack-link @ 6a0cf04615
- `mtp-brutalfistgrokversionfive`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversionfive branch backup/box-2026-10-14-mtp-brutalfistgrokversionfive-docs-muse-training-pack-link @ a84f6aba43
- `mtp-brutalfistgrokversionfour`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversionfour branch backup/box-2026-10-14-mtp-brutalfistgrokversionfour-docs-muse-training-pack-link @ 4087676b3d
- `mtp-brutalfistgrokversionseven`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversionseven branch backup/box-2026-10-14-mtp-brutalfistgrokversionseven-docs-muse-training-pack-link @ 54bc2e676b
- `mtp-brutalfistgrokversionsix`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversionsix branch backup/box-2026-10-14-mtp-brutalfistgrokversionsix-docs-muse-training-pack-link @ 24baeb0947
- `mtp-brutalfistgrokversionten`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversionten branch backup/box-2026-10-14-mtp-brutalfistgrokversionten-docs-muse-training-pack-link @ ab5bc88ef3
- `mtp-brutalfistgrokversiontenpointfive`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversiontenpointfive branch backup/box-2026-10-14-mtp-brutalfistgrokversiontenpointfive-docs-muse-training-pack-link @ 50873b0ece
- `mtp-brutalfistgrokversionthree`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversionthree branch backup/box-2026-10-14-mtp-brutalfistgrokversionthree-docs-muse-training-pack-link @ 768d024824
- `mtp-brutalfistgrokversiontwo`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/brutalfistgrokversiontwo branch backup/box-2026-10-14-mtp-brutalfistgrokversiontwo-docs-muse-training-pack-link @ 542d830868
- `mtp-chimera-emulator-hub`: PUSHED docs/muse-training-pack-link -> https://github.com/mhvnsnt/chimera-emulator-hub branch backup/box-2026-10-14-mtp-chimera-emulator-hub-docs-muse-training-pack-link @ d3445b745e
- `mtp-theyard`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/theyard branch backup/box-2026-10-14-mtp-theyard-docs-muse-training-pack-link @ e2892b5663
- `mtp-western-heart`: PUSHED branch:docs/muse-training-pack-link -> https://github.com/mhvnsnt/western-heart branch backup/box-2026-10-14-mtp-western-heart-docs-muse-training-pack-link @ 0f9feee15b
- `originalize-pr-AshLanev2`: PUSHED uncommitted-snapshot(51 paths) -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-originalize-pr-AshLanev2-wip @ 4b2756c272
- `pt-ops`: PUSHED branch:claims/playtest-2026-10-14 -> https://github.com/mhvnsnt/agent-ops branch backup/box-2026-10-14-pt-ops-claims-playtest-2026-10-14 @ 24e81aabf2
- `ref-repos-Bannon`: PUSHED branch:stickup/entrance-v1 -> https://github.com/mhvnsnt/Bannon.git branch backup/box-2026-10-14-ref-repos-Bannon-stickup-entrance-v1 @ 25c8bf77ed
- `tmp-ashbuild`: PUSHED uncommitted-snapshot(41 paths) -> https://github.com/mhvnsnt/AshLanev2 branch backup/box-2026-10-14-tmp-ashbuild-wip @ d5473c496a
- `tmp-ceh`: PUSHED branch:feat/private-cloud-console -> https://github.com/mhvnsnt/chimera-emulator-hub branch backup/box-2026-10-14-tmp-ceh-feat-private-cloud-console @ 51bdf07cd5
- `tmp-tgt`: PUSHED branch:master -> https://github.com/mhvnsnt/box-storage.git branch backup/box-2026-10-14-tmp-tgt-master @ 16b2fec7cd
- `vten-ci-fix`: PUSHED uncommitted-snapshot(15 paths) -> https://github.com/mhvnsnt/brutalfistgrokversionten.git branch backup/box-2026-10-14-vten-ci-fix-wip @ 416f583443
- `vten-intro-base`: PUSHED uncommitted-snapshot(1 paths) -> https://github.com/mhvnsnt/brutalfistgrokversionten.git branch backup/box-2026-10-14-vten-intro-base-wip @ 325543f99c
- `vten-intro`: PUSHED uncommitted-snapshot(3 paths) -> https://github.com/mhvnsnt/brutalfistgrokversionten.git branch backup/box-2026-10-14-vten-intro-wip @ 3478b754fe
- `vten-main-wt`: PUSHED uncommitted-snapshot(3 paths) -> https://github.com/mhvnsnt/brutalfistgrokversionten branch backup/box-2026-10-14-vten-main-wt-wip @ 439f75eadd
- `vten-stages`: PUSHED uncommitted-snapshot(3 paths) -> https://github.com/mhvnsnt/brutalfistgrokversionten branch backup/box-2026-10-14-vten-stages-wip @ 055cf60fd9
- `wa-Bannon`: PUSHED branch:docs/agents-standard -> https://github.com/mhvnsnt/Bannon branch backup/box-2026-10-14-wa-Bannon-docs-agents-standard @ 82420a8993
- `wa-Bannon`: PUSHED uncommitted-snapshot(1 paths) -> https://github.com/mhvnsnt/Bannon branch backup/box-2026-10-14-wa-Bannon-wip @ e84b7c1fa1
- `wa-TRIPPEDD-Production-studios-`: PUSHED branch:docs/agents-standard -> https://github.com/mhvnsnt/TRIPPEDD-Production-studios- branch backup/box-2026-10-14-wa-TRIPPEDD-Production-studios--docs-agents-standard @ 9ffb635ffb
- `wa-money-machine-hq`: PUSHED branch:docs/agents-edit-in-place -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-wa-money-machine-hq-docs-agents-edit-in-place @ a3481988c3
- `wa-money-machine-hq`: PUSHED branch:docs/agents-standard -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-wa-money-machine-hq-docs-agents-standard @ 9525d1cf30
- `wa-money-machine-hq`: PUSHED branch:docs/western-heart-audit -> https://github.com/mhvnsnt/money-machine-hq.git branch backup/box-2026-10-14-wa-money-machine-hq-docs-western-heart-audit @ e8aa4354ff
- `western-heart-inventory-western-heart`: PUSHED branch:grok/lab-playable-slice -> https://github.com/mhvnsnt/western-heart branch backup/box-2026-10-14-western-heart-inventory-western-heart-grok-lab-playable-slice @ 4a58f1a6c5
- `wh-cs`: PUSHED branch:grok/creation-suite-v0 -> https://github.com/mhvnsnt/western-heart.git branch backup/box-2026-10-14-wh-cs-grok-creation-suite-v0 @ b9fbbc40d6
- `wh-cs`: PUSHED branch:pr118 -> https://github.com/mhvnsnt/western-heart.git branch backup/box-2026-10-14-wh-cs-pr118 @ 7b0cdc5d16
- `wh-cs`: PUSHED uncommitted-snapshot(1 paths) -> https://github.com/mhvnsnt/western-heart.git branch backup/box-2026-10-14-wh-cs-wip @ dc5ca40c09
- `wh-qa`: PUSHED branch:grok/wh-playtest-qa -> https://github.com/mhvnsnt/western-heart.git branch backup/box-2026-10-14-wh-qa-grok-wh-playtest-qa @ 7b0cdc5d16
- `wh-qa`: PUSHED uncommitted-snapshot(1 paths) -> https://github.com/mhvnsnt/western-heart.git branch backup/box-2026-10-14-wh-qa-wip @ b63758e7c1

### Release assets on mhvnsnt/box-storage (SHA-256 matched to API digest)

- `ashlane-base-wt`: RELEASE ashlane-base-wt-ignored.tar.part00 998M sha256=a8207d058437f20a060eec3401d0d1acaa7c217dbaade6a0cd32f1c761c49352 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-ashlane-base-wt
- `ashlane-repo`: RELEASE ashlane-repo-ignored.tar.part00 948M sha256=ab30ae97b0eee0b69f07bb449071ad15637b7bb6fea5e98cc17109331b582a6d https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-ashlane-repo
- `code-doctor-case-neon`: RELEASE code-doctor-case-neon-ignored.tar.part00 12K sha256=d3b00671d395c2619155447274cad0642a83f18f271d370a65d079ee711d791d https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-code-doctor-case-neon
- `folder-_intake`: RELEASE folder-_intake.tar.part00 45M sha256=21be12cac35332052ce54a71ee5895f6bb410ee0dabcbc11570c27f81dbf4573 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-_intake
- `folder-agent-tools`: RELEASE folder-agent-tools.tar.part00 120K sha256=b05014077b6b60aee4a1f9971d466ad7a16010b33919676dfe73e5eb3e9bf6e1 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-agent-tools
- `folder-ashlane-fix-proof`: RELEASE folder-ashlane-fix-proof.tar.part00 7.2M sha256=2ea64962619d9245e6ce68fb0349d9e9a23081024982fd292c2d8e49aa8bb348 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-ashlane-fix-proof
- `folder-ashlane`: RELEASE folder-ashlane.tar.part00 459M sha256=8e174e074e8240566b2d9497967b5febf498ac5646cfcc54b3654359157f2712 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-ashlane
- `folder-bible`: RELEASE folder-bible.tar.part00 437M sha256=49250ef25e2a4ab2fc23f7845fca04c40cb6514e63401ce84b83c07c4f9e901b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-bible
- `folder-canon-moves`: RELEASE folder-canon-moves.tar.part00 320K sha256=44322657cfba6e4887f8c22094d43374c27c964f57bef00ab7c2e7afef32a8ec https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-canon-moves
- `folder-cfdeploy`: RELEASE folder-cfdeploy.tar.part00 60K sha256=1417a3e7df633595b9068f99fe68fa2f7ba3f76e496b8bb806e62137b5c37f43 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-cfdeploy
- `folder-code-doctor`: RELEASE folder-code-doctor.tar.part00 410M sha256=fbdcc61e0c1659dcf1608f14342c00bfeba5da629d621412f9ff96e4593b6ae3 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-code-doctor
- `folder-cs-proof`: RELEASE folder-cs-proof.tar.part00 14M sha256=03fc0924499f6934e2f478966822bf01ae501f5d5bad01738f0b8342973bb13f https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-cs-proof
- `folder-fix`: RELEASE folder-fix.tar.part00 12K sha256=02b11068ab4bf981a14b4216913ca8d59cda44244a6a79c60d2a2314518078ca https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-fix
- `folder-fvr`: RELEASE folder-fvr.tar.part00 31M sha256=736ab57d81d1d688cd6231836c37e1f4ff9fe08747b9e56c642e70deaa0d1e46 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-fvr
- `folder-game-kits`: RELEASE folder-game-kits.tar.part00 1.9G sha256=56080fa4788241ac4b0aef383882cebade7fd3ffb0e164da82d511216756e705 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-game-kits
- `folder-game-kits`: RELEASE folder-game-kits.tar.part01 1.9G sha256=9afe2802bbd14f75c56458db0081d422d025d6dbd02f2c0f9c9825d40a895e74 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-game-kits
- `folder-game-kits`: RELEASE folder-game-kits.tar.part02 1.9G sha256=32d0fe568ea5ed43f52088208abd1d5e69675137375dbd326527530a23ac9f81 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-game-kits
- `folder-game-kits`: RELEASE folder-game-kits.tar.part03 98M sha256=351d6168fff797e85272063f74da7ea76dde3002318c00d68e67a8f3d13c1be5 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-game-kits
- `folder-gv`: RELEASE folder-gv.tar.part00 259M sha256=cafb412a7cedd3fdd47056657a2c0d97f4d8b398e444510e90c5f9f147ff0313 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-gv
- `folder-home-box-sand-data`: RELEASE folder-home-box-sand-data.tar.part00 128M sha256=b5dabf9e7ccfda929a42fc7af8a5cb9e8ddea23695745c6915c3d5032ee1f0ce https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-home-box-sand-data
- `folder-home-box-scratch`: RELEASE folder-home-box-scratch.tar.part00 1.2G sha256=f2ca4b9886de8ae0cf6d0e9351c0c592b1abdae9f5512cd1dc176956b04a2b36 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-home-box-scratch
- `folder-ig`: RELEASE folder-ig.tar.part00 40K sha256=bb809d6c3de08ab47950efe96f143d79ce12923bb73374dfb2ba41e20aa37bdd https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-ig
- `folder-intro-movie`: RELEASE folder-intro-movie.tar.part00 469M sha256=286bea6db7d835616919d42ac2bd2268ec27d9755588230ff4f82bbf170a0cc7 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-intro-movie
- `folder-mfluid-audit`: RELEASE folder-mfluid-audit.tar.part00 280K sha256=c57fd82522e741e485527f6a926bfa3af3b8501afc5fb3040261f1ab365e2e5b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-mfluid-audit
- `folder-mirror`: RELEASE folder-mirror.tar.part00 12M sha256=42cee7b9cd3956a610760078831cdaddb83e34391b0bf2f05de325df76d075e7 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-mirror
- `folder-mmhq-autoreply`: RELEASE folder-mmhq-autoreply.tar.part00 60M sha256=19baf4b02736d8409b1b3ca064021294acc013de73adadd9b9af1d99c660b2e8 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-mmhq-autoreply
- `folder-mocap-src`: RELEASE folder-mocap-src.tar.part00 101M sha256=ec3e97683f1fe156b82fe82ed97801deb3243fb88aba84162e8a123e07e1cc7b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-mocap-src
- `folder-mtp`: RELEASE folder-mtp.tar.part00 12K sha256=715b600e44f74bd766923d77bcf2fff3fca84f5b66e2b6a8595a4f6927327ffd https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-mtp
- `folder-offers`: RELEASE folder-offers.tar.part00 460K sha256=cdd838fe403fee8ee1b3ffead35c1d8f518a04ab95d83ca976e1d6c0a5839a9a https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-offers
- `folder-originalize`: RELEASE folder-originalize.tar.part00 1.9G sha256=e33cc838a9a2dc9dca84f9e7ab253863b879838f5a830bfc86436173bc0187dc https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-originalize
- `folder-originalize`: RELEASE folder-originalize.tar.part01 1.9G sha256=1dff47cb38a1eac2ee4a8b434c5eb7ba61093c196811c32a6557b579f1c61cf2 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-originalize
- `folder-originalize`: RELEASE folder-originalize.tar.part02 799M sha256=7809da7be6f3a1edcf47337e4442f2d2fc625b90bbef7189a9adeaa03bb4281a https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-originalize
- `folder-oss-anim-staging`: RELEASE folder-oss-anim-staging.tar.part00 1.9G sha256=31d87439abe4751b5863282dcb7ef8557850330e9b1e77338349a57dbb67107d https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-oss-anim-staging
- `folder-oss-anim-staging`: RELEASE folder-oss-anim-staging.tar.part01 333M sha256=ae56b324fd7ad072af998e11ccbd184ff14be012bd230d6dd5a669d542cf02f3 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-oss-anim-staging
- `folder-oss`: RELEASE folder-oss.tar.part00 1.6G sha256=6afbc04fa4774a4aef0c6e3e8f778225391b86c5e6ecfd89e467ada770c8b377 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-oss
- `folder-pa-mkt`: RELEASE folder-pa-mkt.tar.part00 23M sha256=5716349162f57c59837d055f5c9038127d579b4e37afef61c6dcaeca2dd5534f https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-pa-mkt
- `folder-pck`: RELEASE folder-pck.tar.part00 3.6M sha256=fe759b5fd68e3fb1948929ec16c65fb28db36889a24eb94bdc82c5d9add38ac9 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-pck
- `folder-pitch`: RELEASE folder-pitch.tar.part00 380K sha256=a1ebfb1396c5d35c6bd49ad75082a623b49e3a271cf5f423f8b79258090a83da https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-pitch
- `folder-plan`: RELEASE folder-plan.tar.part00 240K sha256=fa7a431d9f0a908ac9a29d5ff87e8e7827a44f4c17e39f1d4faffc228b1051a8 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-plan
- `folder-proof`: RELEASE folder-proof.tar.part00 1.4M sha256=2b90a45af491b0d2c7e6a0d85b67d32404ebeb606737290028f89c6f4f0518b0 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-proof
- `folder-ref-repos`: RELEASE folder-ref-repos.tar.part00 12K sha256=6e51d0c70d744f971998e7ba3da9ecc037eaaae6bb63023100e1296d91047b1b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-ref-repos
- `folder-rig-repair`: RELEASE folder-rig-repair.tar.part00 1.9G sha256=7b0d7a08cc340d59b25b81d035e626019316d13355016d3a7706b06aaae4295d https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-rig-repair
- `folder-rig-repair`: RELEASE folder-rig-repair.tar.part01 534M sha256=5513e33d2440cc561c9d2fdd8375c4da578d29fcc14cf52dcad990c09eda3311 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-rig-repair
- `folder-rv`: RELEASE folder-rv.tar.part00 776M sha256=660345908f73922196a5dbf7c37da28e34b145cbb586143bf82117e66f3a9ffb https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-rv
- `folder-security`: RELEASE folder-security.tar.part00 40K sha256=5b341841713fa962431b5d2cc5de939fa23033affac62aad3df1b6c0ff242416 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-security
- `folder-share`: RELEASE folder-share.tar.part00 1.4M sha256=8356d716acc09adefb0cc7083f348e8f7fbcd60925ad8e9e6ff49e7c7b7732e1 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-share
- `folder-tekken-ref`: RELEASE folder-tekken-ref.tar.part00 1.2G sha256=e427994be946995e7a4c5567eadc87a9cc44c5ac43eb7ad0a12fb566a3da4f5b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-tekken-ref
- `folder-tmp-godwithin`: RELEASE folder-tmp-godwithin.tar.part00 12M sha256=2875661e54f13a85e390af66551710dad22c8af5f93821fc5393db7139225add https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-tmp-godwithin
- `folder-tools`: RELEASE folder-tools.tar.part00 525M sha256=bf5e16826fd4b7ac20d590884e9659a537ba1ca36dc90581e74b9e5861bf5824 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-tools
- `folder-tracks`: RELEASE folder-tracks.tar.part00 54M sha256=32fbb59eae258770dd38bbdd69ada7a2f1f39249ddacef8ecc0889dd318e65d3 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-tracks
- `folder-vis`: RELEASE folder-vis.tar.part00 4.6M sha256=1afb931817587b2beb4ba4c1a032a057390dbb2ae5dc8ca29794c0eb80ef98c0 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-vis
- `folder-wa`: RELEASE folder-wa.tar.part00 32K sha256=c99867ab45c9bf4778f2d6eb8c155a25cac0a7615e2819fb0ad28eae9d5e4d27 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-wa
- `folder-western-heart-inventory`: RELEASE folder-western-heart-inventory.tar.part00 20K sha256=ce314b944fbcef17a5c7b8d544812344324aa7b29a37bbcb94b3c8542db7f8e9 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-western-heart-inventory
- `folder-western-heart-lab`: RELEASE folder-western-heart-lab.tar.part00 76M sha256=69c6194bc6ce958b2bf6dc2bd044cb3070ff23edfc6f766a45f40f4762d44c4b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-western-heart-lab
- `folder-workspace-loose`: RELEASE workspace-loose-files.tar sha256=836f312125e9d550293d84e837c462a16a82b20c2ec8a43b8903d45d63f4364b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-folder-workspace-loose-files
- `mfluid-audit-Mochiichao-Diamond-Version-2d-`: RELEASE mfluid-audit-Mochiichao-Diamond-Version-2d--ignored.tar.part00 652K sha256=579833e9bc35ef6f28a4023734226d8167c3cbc2526979bdc6c10c812d1d4d2d https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-mfluid-audit-Mochiichao-Diamond-Version-2d
- `mmhq-cdt`: RELEASE mmhq-cdt-ignored.tar.part00 1.9G sha256=16c2208a36dc60ec951d96ebed231a3e931ff762785d2ca02edbc2663019a79e https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-mmhq-cdt
- `mmhq-cdt`: RELEASE mmhq-cdt-ignored.tar.part01 298M sha256=bfaa44df524b522d7fbaf2c075a6d1aa2a2912dae8141e800f31ba9a3cb0615b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-mmhq-cdt
- `mmhq-entrance`: RELEASE mmhq-entrance-ignored.tar.part00 920M sha256=a48733062b7fec32d96558c0b05c82b3a31864f51b7106340c190dc48e3b5981 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-mmhq-entrance
- `money-machine-hq`: RELEASE money-machine-hq-ignored.tar.part00 135M sha256=215f8c6bb1da8c22a2f88226e71e23a49467d2fb5507d026b1037191c9438d5a https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-money-machine-hq
- `studio-pipeline`: RELEASE studio-pipeline-ignored.tar.part00 1.9G sha256=ea66d8e1a2f03eb83b21a2804aa7250c02296131c79043d06b419b280c625d3c https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-studio-pipeline
- `studio-pipeline`: RELEASE studio-pipeline-ignored.tar.part01 1.9G sha256=55e9550a24f73644786650a7b0cc4a0719cc8f90c5dd324ac7856f63b2e9f551 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-studio-pipeline
- `studio-pipeline`: RELEASE studio-pipeline-ignored.tar.part02 1.4G sha256=73ceeb21da8edf609739b8d10770de0339ea3e34842fe2aee8dc47ee006fc4fd https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-studio-pipeline
- `tmp-build-M.-OS-Mochiichao-Chrome-Version-`: RELEASE tmp-build-M.-OS-Mochiichao-Chrome-Version--ignored.tar.part00 4.0M sha256=20febbc3368c3ca5cafef59838b493ba361aea89eca82164777b4604eec1824c https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-tmp-build-M_-OS-Mochiichao-Chrome-Version
- `tmp-build-Mochiichao-Diamond-Version-2d-`: RELEASE tmp-build-Mochiichao-Diamond-Version-2d--ignored.tar.part00 652K sha256=4fd711d3dfc4aed8c8b75da360e9d9457d9d258be39db91fe49e67fa82e53a12 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-tmp-build-Mochiichao-Diamond-Version-2d
- `tmp-build-Neon-App-Builder`: RELEASE tmp-build-Neon-App-Builder-ignored.tar.part00 412K sha256=a85231ca472e1a9b12b4f87f5cb71b8e383a4e4750ea53ae340bd87b5685827d https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-tmp-build-Neon-App-Builder
- `vten-ci-fix`: RELEASE vten-ci-fix-ignored.tar.part00 419M sha256=25053dba6309aafc336e31834da23a9173f7085edc63b7285464bcaea5db0d25 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-vten-ci-fix
- `vten-intro-base`: RELEASE vten-intro-base-ignored.tar.part00 500K sha256=d631bfa1d9d3525bfab0152d9a9fb4224ee00d9393f2f14c8b350b3a370c662b https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-vten-intro-base
- `vten-intro`: RELEASE vten-intro-ignored.tar.part00 242M sha256=160b1b366a65c87a03ec23f90d037cbb14cecdd6956b4dd5f5443a3813b552a2 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-vten-intro
- `vten-main-wt`: RELEASE vten-main-wt-ignored.tar.part00 500K sha256=b88c7924af7cd3abb14313125b7473c979db83c9c8a4c0cc395c0e81ab343de6 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-vten-main-wt
- `vten-stages`: RELEASE vten-stages-ignored.tar.part00 238M sha256=4ef22b134fe2e8d29685c25193301e93a722cb34199946a6c91368f9d0f588f3 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-vten-stages
- `western-heart-inventory-western-heart`: RELEASE western-heart-inventory-western-heart-ignored.tar.part00 59M sha256=60cab7ea477dc9dd6c4e2d2eb22bcf08d6a2748da85e72c8f23f5a1e55af7cac https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-western-heart-inventory-western-heart
- `wh-cs`: RELEASE wh-cs-ignored.tar.part00 12M sha256=1bb69f81b31a43ad0f988f7119445f5603c0c6be01256953aa47e862f7d40b55 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-wh-cs
- `wh-qa`: RELEASE wh-qa-ignored.tar.part00 12M sha256=2ac84c019181b9f79e5a5093fad4e6c8793700730faba7f145fd8c47102890a4 https://github.com/mhvnsnt/box-storage/releases/tag/box-2026-10-14-wh-qa
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

## Pass 2 — 2026-10-14 ~4:50 PM CT (Grok Bot / Producerbot, owner order)

Free space before: 609 MB. After clone deletions: ~15.1 GB.

### Clones deleted (porcelain 0, unpushed 0, no stashes, every branch tip reachable from an ls-remote ref, no ignored files, lsof 0, no file changes in 20 min, not under an active claim)

| Path | Size | Backup (remote) | Local HEAD |
|---|---|---|---|
| `wa/TRIPPEDD-Production-studios-` | 1489MB | https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/tree/docs/agents-standard | `9ffb635f` |
| `ig/w-TRIPPEDD-Production-studios-` | 4002MB | https://github.com/mhvnsnt/TRIPPEDD-Production-studios-/tree/feat/instruction-gate | `ef9f5c70` |
| `ref-repos/Bannon` | 5717MB | https://github.com/mhvnsnt/Bannon/tree/stickup/entrance-v1 | `25c8bf77` |
| `ig/w-God-Molecule-Show-Studio` | 281MB | https://github.com/mhvnsnt/God-Molecule-Show-Studio/tree/feat/instruction-gate | `7fbc3430` |
| `mmhq-cd` | 600MB | https://github.com/mhvnsnt/money-machine-hq/tree/main | `f0afec51` |
| `mtp/mmhq` | 829MB | https://github.com/mhvnsnt/money-machine-hq/tree/docs/muse-training-pack | `ba6a62ab` |
| `wa/money-machine-hq` | 597MB | https://github.com/mhvnsnt/money-machine-hq/tree/docs/agents-edit-in-place | `a3481988` |
| `ig/w-money-machine-hq` | 184MB | https://github.com/mhvnsnt/money-machine-hq/tree/feat/instruction-gate | `c9f580ef` |
| `oss-anim-staging/_raw/git/cmu-mocap` | 434MB | https://github.com/una-dinosauria/cmu-mocap/tree/master | `09a07f54` |
| `ig/w-BioMechania` | 188MB | https://github.com/mhvnsnt/BioMechania/tree/feat/instruction-gate | `b65dff97` |
| `ig/w-ConcreteDragon` | 190MB | https://github.com/mhvnsnt/ConcreteDragon/tree/feat/instruction-gate | `e8dababf` |

Note: some head branches no longer exist on the remote (merged and deleted), but each tip commit was confirmed to be an ancestor of a ref on the remote before deletion.

### New backup refs (non-disruptive snapshot commits; working trees and HEAD untouched)

backup/box-2026-10-14b-<clone>-wip / -stashN on: AshLanev2 (ashlane-repo, ashlane-base-wt, originalize-pr-AshLanev2, tmp-ashbuild), Brutal-Fist (wip, stash0, BannonSource-wip), brutalfistgrokversionten (vten-stages, vten-main-wt, vten-intro, vten-intro-base, vten-ci-fix), brutalfistgrokversioneight, western-heart (wh-qa wip + grok/wh-playtest-qa, wh-cs), Bannon (wa-Bannon), M.-Engine- (fix), money-machine-hq (mmhq-entrance wip+2 stashes, mmhq-cdt/money-machine-hq/mmhq-et-v2 2 stashes each).

Not backed up: mfluid-audit/Mochiichao-Diamond-Version-2d- (2 dirty files; push to mfluidmusic denied 403). Kept on disk.

## 2026-10-23 cleanup (owner standing permission, t126u 2:57 PM CT)

Rules: idle >60 min (excluding .git), no open handles, no untracked/modified files (only tracked deletions of files still on remote, or regenerable output like .output/ test-results/), 0 stashes, every local branch + HEAD reachable from a remote ref after fetch.

| Path | Size | Remote | SHA | Cleared (CT) |
|---|---|---|---|---|
| `ashlane/play` | 1861MB | https://github.com/mhvnsnt/AshLanev2 | `7409b03a` | 15:04 CT |
| `ig/w-AshLanev2` | 253MB | https://github.com/mhvnsnt/AshLanev2 | `93e820f2` | 15:04 CT |
| `ig/w-Bannon` | 2001MB | https://github.com/mhvnsnt/Bannon | `7a388cf8` | 15:04 CT |
| `ig/w-western-heart` | 741MB | https://github.com/mhvnsnt/western-heart | `86f3b51a` | 15:04 CT |
| `ig/w-agent-ops` | 4MB | https://github.com/mhvnsnt/agent-ops | `ca32c44b` | 15:04 CT |
| `bn/b` | 1645MB | https://github.com/mhvnsnt/Bannon.git | `63643c5e` | 15:04 CT |
| `bible/God-Molecule-Show-Studio` | 727MB | https://github.com/mhvnsnt/God-Molecule-Show-Studio.git | `758365de` | 15:04 CT |
| `kobra-fix` | 283MB | https://github.com/mhvnsnt/brutalfistgrokversionten.git | `dded5029` | 15:04 CT |
| `bible/TRIPPEDD-Production-studios-` | 12273MB | https://github.com/mhvnsnt/TRIPPEDD-Production-studios-.git | `7efcfbdd` | 15:04 CT |
| `bible/Bannon` | 7211MB | https://github.com/mhvnsnt/Bannon.git | `6636ad54` | 15:04 CT |
| `ashlane/base-wt` | 2641MB | https://github.com/mhvnsnt/AshLanev2 | `1ce79707` | 15:04 CT |
| `ashlane/repo` | 4266MB | https://github.com/mhvnsnt/AshLanev2 | `af2ff5b7` | 15:04 CT |
| `TRIPPEDD-Production-studios-` | 4271MB | https://github.com/mhvnsnt/TRIPPEDD-Production-studios-.git | `43623000` | 15:04 CT |
| `wh-qa` | 3874MB | https://github.com/mhvnsnt/western-heart.git | `7b0cdc5d` | 15:04 CT |
| `western-heart-inventory/western-heart` | 2683MB | https://github.com/mhvnsnt/western-heart | `4a58f1a6` | 15:04 CT |

Total freed: ~44.7 GB.
## 2026-10-23 ~15:55 CDT — Repo Co Dev own-clone cleanup (rule (a))

Checked with `/tmp/rcd-chk.sh` (clean+no untracked, empty stash, every local branch contained in a remote ref, submodules). **Removed: none** — no clone passed all checks. Kept on disk:

| Path | Size | Reason kept |
|---|---|---|
| /workspace/western-heart-lab | 76M | not a git repo (proof/src scratch) — cannot verify |
| /workspace/wh-proof | 5.5M | not a git repo — cannot verify |
| /workspace/originalize | 6.1G | not a git repo (top dir) — cannot verify |
| /workspace/Brutal-Fist | 4.5G | dirty (modified submodule BannonSource, deleted Research/*) + 1 stash |
| /workspace/vten-stages | 743M | 3 dirty paths |
| /workspace/vten-ci-fix | 493M | 15 dirty paths |
| /workspace/vten-main-wt | 275M | 3 dirty paths |
| /workspace/vten-intro | 755M | 3 dirty paths |
| /workspace/vten-intro-base | 277M | 1 dirty path |
| /workspace/brutalfistgrokversioneight | 429M | 1 dirty path |

wh-qa: not present. Other /workspace dirs (wh-*, ashlane, etc.) left untouched — ownership not confirmed.
