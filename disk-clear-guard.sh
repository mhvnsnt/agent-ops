#!/usr/bin/env bash
# disk-clear-guard.sh — MANDATORY pre-clear gate for every disk cleanup.
#
# Incident: 2026-11-17T02:45Z, ROUND 6 QUIET1 cleared the ENTIRE
# ~/workspace/_squishyfx-native-20261116/ (833 MB) WHILE the P3 SquishyFX
# re-render batch was running in it. The clear verified the STORED payload
# (PR #205, 8 blends, delta release) but never inventoried the dir for
# UNSTORED contents — web harness + capture + calibration scripts with live
# v2 edits, B1 v1 proof seq frames + metrics were deleted. The
# disk-space-guardian had NEVER called the LANE_GUARD reaper contract
# (guard-paths.sh check-tree: 0 mentions in 42,564 lines of
# disk-cleanup-log.md), the dir was never registered in
# protected-paths.json, and no .DO_NOT_DELETE marker existed at clear time.
#
# This script is the machine-enforced gate. NO cleanup — guardian, reaper,
# or ad-hoc — deletes, moves, or "tidies" ANY directory without a CLEARABLE
# verdict from this script first. There is NO override flag, by design.
#
# Usage:
#   disk-clear-guard.sh [--stored-manifest FILE] [--log] DIR
#
#   --stored-manifest FILE  list of relative paths (one per line) verified
#                           byte-identical on a store (GitHub release /
#                           TeraBox / repo). A whole-dir clear requires it:
#                           EVERY file in DIR must be listed. Any file not
#                           in the manifest blocks the clear and is named.
#   --log                   append the verdict line to
#                           ~/workspace/agent-ops/disk-cleanup-log.md.
#                           (Dry runs omit --log.)
#
# The script NEVER deletes, moves, or modifies anything. It only reads and
# prints a verdict. Exit codes:
#   0  CLEARABLE — every check passed.
#   1  BLOCKED   — at least one check failed; reasons printed.
#   2  ERROR / UNCERTAIN — treat as BLOCKED. Never clear on exit 2.
#
# Checks (all run; every blocking reason is reported, not just the first):
#   [registry]    guard-paths.sh check-tree refuses the path.
#   [marker]      a .DO_NOT_DELETE* marker at/under the dir, or on an
#                 ancestor up to ~/workspace.
#   [recency]     any file under the dir modified in the last 24 hours.
#   [live-procs]  any process with its cwd inside the dir, or (when lsof
#                 is available) any open file handle under the dir.
#   [dependency]  a recent (< 7 days) CHECKPOINT*.md / PROGRESS.md under
#                 ~/workspace lane workdirs references this dir by path or
#                 basename — some live lane believes it needs this dir.
#   [git-dirty]   the dir is a git repo with uncommitted changes.
#   [manifest]    no --stored-manifest supplied, or files in the dir are
#                 not listed in it (unstored contents).
#
# Refusals (exit 2): the script will not evaluate /, $HOME, ~/workspace
# itself, or ~/workspace/agent-ops itself as a clear candidate.

set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -x "$SCRIPT_DIR/guard-paths.sh" ]; then
  GUARD_PATHS="$SCRIPT_DIR/guard-paths.sh"
else
  GUARD_PATHS="${HOME}/workspace/agent-ops/guard-paths.sh"
fi
LOG_FILE="${HOME}/workspace/agent-ops/disk-cleanup-log.md"
RECENCY_HOURS=24
DEPENDENCY_DAYS=7

usage() {
  sed -n '2,40p' "$0"
  exit 2
}

MANIFEST=""
DO_LOG=0
TARGET=""
while [ $# -gt 0 ]; do
  case "$1" in
    --stored-manifest) [ $# -ge 2 ] || usage; MANIFEST="$2"; shift 2;;
    --log) DO_LOG=1; shift;;
    --help|-h) usage;;
    --*) echo "unknown flag: $1" >&2; usage;;
    *) [ -z "$TARGET" ] || usage; TARGET="$1"; shift;;
  esac
done
[ -n "$TARGET" ] || usage

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
# Canonicalize (realpath -m works for missing paths too).
TARGET="$(realpath -m "$TARGET" 2>/dev/null || echo "$TARGET")"
WS="${HOME}/workspace"

REASONS=()
block() { REASONS+=("[$1] $2"); }

# --- refusal: top-level targets are never clear candidates ---
case "$TARGET" in
  "/"|"$HOME"|"$WS"|"$WS/agent-ops")
    echo "GUARD $TS $TARGET"
    echo "VERDICT: ERROR — refusing to evaluate a top-level directory as a clear candidate."
    exit 2;;
esac

# --- existence ---
if [ ! -e "$TARGET" ]; then
  echo "GUARD $TS $TARGET"
  echo "VERDICT: ERROR — path does not exist."
  exit 2
fi
if [ ! -d "$TARGET" ]; then
  echo "GUARD $TS $TARGET"
  echo "VERDICT: ERROR — path is not a directory (this gate covers whole-directory clears only)."
  exit 2
fi

# --- [registry] LANE_GUARD reaper contract ---
if [ -x "$GUARD_PATHS" ]; then
  if ! "$GUARD_PATHS" check-tree "$TARGET" >/dev/null 2>&1; then
    REG_REASON="$("$GUARD_PATHS" check-tree "$TARGET" 2>&1 | head -1)"
    block "registry" "$REG_REASON"
  fi
else
  block "registry" "guard-paths.sh not found/executable at $GUARD_PATHS — registry check unavailable (uncertain)."
fi

# --- [marker] .DO_NOT_DELETE at/under the dir, or on an ancestor ---
MARKER_HIT="$(find "$TARGET" -name '.DO_NOT_DELETE*' -print -quit 2>/dev/null)"
if [ -n "$MARKER_HIT" ]; then
  block "marker" "marker present: $MARKER_HIT"
else
  _p="$TARGET"
  while [ "$_p" != "$WS" ] && [ "$_p" != "/" ]; do
    _p="$(dirname "$_p")"
    if [ -e "$_p/.DO_NOT_DELETE" ] || [ -e "$_p/.DO_NOT_DELETE"* ]; then
      # shellcheck disable=SC2012
      _m="$(ls -d "$_p"/.DO_NOT_DELETE* 2>/dev/null | head -1)"
      block "marker" "ancestor marker present: ${_m:-$_p/.DO_NOT_DELETE}"
      break
    fi
    [ "$_p" = "$WS" ] && break
  done
fi

# --- [recency] any file modified in the last 24 hours ---
NEWEST="$(find "$TARGET" -type f -newermt "-${RECENCY_HOURS} hours" -print 2>/dev/null | head -5)"
if [ -n "$NEWEST" ]; then
  _n="$(find "$TARGET" -type f -newermt "-${RECENCY_HOURS} hours" -print 2>/dev/null | wc -l)"
  block "recency" "$_n file(s) modified in the last ${RECENCY_HOURS}h, e.g.: $(echo "$NEWEST" | head -1)"
fi

# --- [live-procs] cwd inside the dir, or open handles under it ---
_LIVE=""
for _pid_dir in /proc/[0-9]*; do
  _pid="${_pid_dir#/proc/}"
  # Skip this script's own process tree: any pid whose cmdline names this guard.
  if [ -r "$_pid_dir/cmdline" ] && tr '\0' ' ' < "$_pid_dir/cmdline" 2>/dev/null | grep -q "disk-clear-guard.sh"; then
    continue
  fi
  _cwd="$(readlink "$_pid_dir/cwd" 2>/dev/null || true)"
  case "$_cwd" in
    "$TARGET"|"$TARGET"/*)
      _comm="$(tr '\0' ' ' < "$_pid_dir/cmdline" 2>/dev/null | cut -c1-120)"
      [ -z "$_comm" ] && _comm="$(cat "$_pid_dir/comm" 2>/dev/null || echo '?')"
      _LIVE="${_LIVE}pid ${_pid} (${_comm}) cwd=${_cwd}; "
      ;;
  esac
done
if command -v lsof >/dev/null 2>&1; then
  _LSOF="$(timeout 30 lsof +D "$TARGET" 2>/dev/null | tail -n +2 | head -5)"
  if [ -n "$_LSOF" ]; then
    _LIVE="${_LIVE}lsof open handles: $(echo "$_LSOF" | head -1 | awk '{print $1" pid "$2" "$NF}'); "
  fi
fi
if [ -n "$_LIVE" ]; then
  block "live-procs" "$_LIVE"
fi

# --- [dependency] a recent lane CHECKPOINT references this dir ---
_BASE="$(basename "$TARGET")"
_DEP_FILES="$(timeout 60 find "$WS"/_* -maxdepth 3 \( -name 'CHECKPOINT*.md' -o -name 'PROGRESS.md' \) -newermt "-${DEPENDENCY_DAYS} days" -type f 2>/dev/null)"
_DEP_HITS=""
if [ -n "$_DEP_FILES" ]; then
  _DEP_HITS="$(echo "$_DEP_FILES" | grep -v "^$TARGET/" | grep -v "disk-cleanup-guard-fix" | xargs grep -l -F -e "$TARGET" -e "$_BASE" 2>/dev/null | head -5)"
fi
if [ -n "$_DEP_HITS" ]; then
  block "dependency" "referenced by recent lane checkpoint(s): $(echo "$_DEP_HITS" | tr '\n' ' ')"
fi

# --- [git-dirty] uncommitted changes in the dir itself ---
if [ -d "$TARGET/.git" ]; then
  if ! _GS="$(cd "$TARGET" && git status --porcelain 2>/dev/null)" || [ -n "$_GS" ]; then
    block "git-dirty" "git repo with uncommitted changes (or status unreadable)."
  fi
fi

# --- [manifest] whole-dir clear requires a per-file stored manifest ---
if [ -z "$MANIFEST" ]; then
  block "manifest" "no --stored-manifest supplied — a whole-directory clear requires a per-file list verified on a store."
elif [ ! -f "$MANIFEST" ]; then
  block "manifest" "stored-manifest file not found: $MANIFEST"
else
  # .git internals are excluded from the manifest list: they are covered by
  # the [git-dirty] check plus the repo's own remote, not by a file manifest.
  _ALL="$(find "$TARGET" -type f -not -path '*/.git/*' -printf '%P\n' 2>/dev/null | sort)"
  _COUNT_ALL="$(echo "$_ALL" | grep -c . || true)"
  _MAN="$(sort -u "$MANIFEST" | grep -v '^$' || true)"
  _UNSTORED="$(comm -23 <(echo "$_ALL") <(echo "$_MAN") || true)"
  _N_UNSTORED="$(echo "$_UNSTORED" | grep -c . || true)"
  if [ "$_N_UNSTORED" -gt 0 ]; then
    block "manifest" "$_N_UNSTORED of $_COUNT_ALL file(s) NOT in the stored manifest (unstored contents), e.g.: $(echo "$_UNSTORED" | head -3 | tr '\n' ' ')"
  fi
fi

# --- verdict ---
echo "GUARD $TS $TARGET"
if [ "${#REASONS[@]}" -eq 0 ]; then
  echo "VERDICT: CLEARABLE"
  _VERDICT="CLEARABLE"
  _CODE=0
else
  echo "VERDICT: BLOCKED"
  echo "REASONS:"
  for _r in "${REASONS[@]}"; do echo "  - $_r"; done
  _VERDICT="BLOCKED — $(printf '%s; ' "${REASONS[@]}")"
  _CODE=1
fi
if [ "$DO_LOG" -eq 1 ]; then
  printf -- '- GUARD %s %s %s\n' "$TS" "$TARGET" "$_VERDICT" >> "$LOG_FILE" 2>/dev/null || echo "warning: could not append to $LOG_FILE" >&2
fi
exit "$_CODE"
