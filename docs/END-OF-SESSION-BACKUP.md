# END-OF-SESSION BACKUP (watchdog procedure)

Run this when work is wrapping up, or when session/usage is ~90-95% spent (reserve enough budget: roughly 1 tool-minute per dirty clone plus upload time for large files). Follows `docs/NO-DATA-LOSS-RULES.md`.

## 1. Inventory every clone on the box
```bash
for g in $(find /workspace /home/box -name .git -maxdepth 6 -prune 2>/dev/null); do d=${g%/.git}
  dirty=$(git -C "$d" status --porcelain -uall | wc -l)
  unpushed=$(git -C "$d" log --oneline @{u}.. 2>/dev/null | wc -l || echo NOUPSTREAM)
  echo -e "$d\t$dirty\t$unpushed\t$(git -C "$d" branch --show-current)"; done
```
Target: every clone `0 dirty / 0 unpushed`.

## 2. Push work to -wip branches (never main, never force)
```bash
git switch -c "$(git branch --show-current)-wip-$(date +%Y%m%d)"   # or keep the feature branch
git add -A && git commit -m "wip: end-of-session snapshot" && git push -u origin HEAD
```
Large binaries (> ~50 MB, or anything git refuses) go to Release assets instead — step 3.

## 3. Large files -> SHA-verified Release assets in mhvnsnt/box-storage
`scripts/bk.sh <clone-dir> <name>` creates release `box-2026-10-14-final-<name>` (edit the tag prefix to today's date), uploads every dirty/untracked file, uploads a manifest (path, git status, sha256, asset name), then compares each release asset `digest` to the local sha256 and prints `verified=N bad=M`. `bad` must be 0.

## 4. Verify
- Branches: `git ls-remote origin <branch>` equals local `git rev-parse HEAD`; `git ls-tree -r origin/<branch>` contains the files.
- Release assets: digest `sha256:<x>` equals local `sha256sum`.
- Re-run the inventory: all `0/0`.

## 5. Only then clean disk
- Delete only items that passed step 4. Log each removed path + where it is backed up + sha256 in WORKLOG / `agent-ops/BOX-OFFLOAD-LOG.md`.
- Anything questionable: back it up again; do not delete.

## 6. Report
Post per clone: dirty/unpushed counts, -wip branch names, release tags, verified/bad counts.

## TeraBox
Status 2026-10-14: no TeraBox connector or credentials; no `rclone` or `terabox` CLI on the box. GitHub (branches + box-storage Release assets) is the only verified backup target. To add TeraBox later the owner must: (1) choose a tool — rclone has no official TeraBox backend; options are a community CLI (e.g. `terabox-cli`/`BaiduPCS-Go`-style tools) or the TeraBox web/desktop app; (2) sign in himself and provide credentials via env/secret store (never pasted in chat); (3) then add a step here that uploads the same manifest + files and verifies sizes/sha256. Agents must not sign in to TeraBox on their own.
