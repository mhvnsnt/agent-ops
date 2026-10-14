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
