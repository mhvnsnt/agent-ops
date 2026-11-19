#!/usr/bin/env bash
# repo_preflight.sh — pre-flight gate for a repo working tree BEFORE a lane
# cuts a branch or commits. Catches the dirty/stale-clone hazard (the
# realism coordinator found the local PP clone STALE + DIRTY with v71
# leftovers on 2026-11-16; a branch cut from it would have carried junk).
#
# Usage: repo_preflight.sh [REPO_DIR] [BASE_BRANCH]
#   Exit 0 = tree clean, branch known, fetch fresh (<= 24h) or just fetched.
#   Exit 1 = FAIL: prints exactly what is wrong + the fix command.
set -u
REPO="${1:-.}"
BASE="${2:-main}"
cd "$REPO" || { echo "FAIL: cannot cd to $REPO"; exit 1; }
[ -d .git ] || { echo "FAIL: $REPO is not a git checkout"; exit 1; }
fail=0
BRANCH=$(git branch --show-current)
echo "repo: $REPO  branch: ${BRANCH:-<detached>}  base: $BASE"
if [ -n "$(git status --porcelain)" ]; then
  echo "FAIL: working tree DIRTY — commit, stash, or move the changes first:"
  git status --porcelain | head -20
  fail=1
else echo "ok: working tree clean"; fi
if ! git rev-parse --verify "$BASE" >/dev/null 2>&1; then
  echo "FAIL: base branch $BASE not present locally — fetch first"
  fail=1
else echo "ok: base branch $BASE present ($(git rev-parse --short $BASE))"; fi
LAST_FETCH=$(stat -c %Y .git/FETCH_HEAD 2>/dev/null || echo 0)
NOW=$(date +%s)
AGE=$(( (NOW - LAST_FETCH) / 3600 ))
if [ "$AGE" -gt 24 ]; then
  echo "note: last fetch ${AGE}h ago — fetching now"
  git fetch origin "$BASE" 2>&1 | tail -2 || { echo "FAIL: fetch failed"; fail=1; }
else echo "ok: last fetch ${AGE}h ago"; fi
BEHIND=$(git rev-list --count "HEAD..origin/$BASE" 2>/dev/null || echo "?")
echo "behind origin/$BASE: $BEHIND commits"
[ "$BEHIND" != "0" ] && [ "$BEHIND" != "?" ] && \
  echo "note: pull/rebase onto origin/$BASE before cutting the PR branch"
exit $fail
