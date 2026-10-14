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

## TeraBox (secondary target)
Status 2026-10-14: the box browser is signed in to TeraBox as **Mars FMMG** (Premium+, ~5 TB free but only ~30 GB permanent; premium expires ~2026-10-20 — after that only the permanent quota is safe). No connector/API credentials, no `rclone`/`terabox` CLI on the box (rclone has no official TeraBox backend).
- GitHub (branches + SHA-verified box-storage Release assets) stays the PRIMARY, verified backup. TeraBox is SECONDARY only; never delete anything because it is "on TeraBox".
- Upload is done through the browser by a **desktop agent** (one with a box desktop/browser), never by a headless/executor agent and never by signing in again — use the existing session only.
- Procedure: (1) after steps 1-4, stage files in `/workspace/terabox-out/<date>/` with the sha256 manifest from bk.sh; (2) desktop agent opens terabox.com in the box browser, uploads that folder to `/box-backups/<date>/`; (3) checks uploaded file count and sizes match the manifest; (4) logs folder path + counts in `agent-ops/BOX-OFFLOAD-LOG.md`.
- Keep critical sets under the 30 GB permanent quota; anything above it may vanish when Premium+ lapses (~Oct 20, 2026).
