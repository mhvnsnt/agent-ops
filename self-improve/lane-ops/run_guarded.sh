#!/usr/bin/env bash
# run_guarded.sh — run a long-lived command under a lockfile so a relaunch
# can NEVER start a second copy (the duplicate-runner race seen twice in the
# Life Cut v2.2 capture: a second runner appeared on each VM-restart relaunch
# and had to be killed by hand).
#
# Usage: run_guarded.sh LOCKFILE -- <command...>
#   - If the lock is held, exits 3 immediately and prints the holder's pid.
#   - The lock is released automatically when the command exits or is killed.
#   - The lockfile lives next to the work (same dir as the runner log).
set -u
LOCK="$1"; shift
[ "${1:-}" = "--" ] && shift
exec 9>"$LOCK"
if ! flock -n 9; then
  holder=$(flock -n "$LOCK" true 2>/dev/null; fuser "$LOCK" 2>/dev/null | tr -s ' ' | head -c 200)
  echo "run_guarded: lock held ($LOCK) holder: ${holder:-unknown} — refusing to start a duplicate" >&2
  exit 3
fi
echo "run_guarded: lock acquired ($LOCK) pid $$ — $*"
exec "$@"
