#!/bin/bash
# stage-as-it-lands.sh — stage each finished file out of a render/output dir
# the moment it lands, so a VM restart can only lose the file currently being
# written, never the finished work behind it.
#
# Why: the 001R 6B lane lost 69 rendered frames twice on 2026-11-15 because
# frames sat in /var/tmp (tmpfs) until the whole pass finished. The standing
# owner rule is "stage finished pieces as they land" — this is the drop-in
# that does it for any lane whose render script does not stage itself.
# (The 6B gate script stages per batch itself; use this for lanes that don't.)
#
# Usage:
#   stage-as-it-lands.sh --watch DIR --stage CMD [--interval SECONDS]
#                        [--state FILE] [--once|--drain] [--stable SECONDS]
#   --once  = one sweep (stages only files already stable at that moment)
#   --drain = repeat sweeps until one stages nothing (use after a render
#             finishes, to stage everything left behind)
#   (no flag = daemon: sweep forever every --interval seconds)
#   CMD receives the finished file path as its only argument ($1).
#   Example stage command: a script that `gh release upload`s the file,
#   `cp`s it to a durable dir, or commits it to a branch — whatever the
#   lane's store is. The stager only decides WHEN a file is finished.
#
# Finished = size unchanged across two polls --stable seconds apart (default
# 2s). A file still being written keeps changing size, so it is never staged
# half-written. Staged files are recorded in the state file as
# "<size> <mtime> <path>"; a restart re-reads the state and skips them, so
# the stager itself is restart-safe (idempotent by construction).
#
# Polling is deliberate: zero dependencies, works in every exec/cron session
# (no TTY), survives cell restarts when re-launched by the watchdog. For
# event-driven staging, entr 5.9 (ISC) is installed at ~/.local/bin/entr —
# see research-friction-20261115/01-stage-as-it-lands.md for the loop pattern
# (entr needs -n in non-TTY sessions; -d exits when a new file appears, so
# wrap it in a while loop that re-lists and re-stages).
#
# Exit codes: 0 = --once pass done (or killed cleanly), 1 = usage/config error,
# 2 = watch dir missing/unreadable.
set -u

WATCH=""; STAGE=""; INTERVAL=5; STATE=""; ONCE=0; DRAIN=0; STABLE=2
while [ "$#" -gt 0 ]; do
    case "$1" in
        --watch)    WATCH="$2"; shift 2 ;;
        --stage)    STAGE="$2"; shift 2 ;;
        --interval) INTERVAL="$2"; shift 2 ;;
        --state)    STATE="$2"; shift 2 ;;
        --stable)   STABLE="$2"; shift 2 ;;
        --once)     ONCE=1; shift ;;
        --drain)    DRAIN=1; shift ;;
        *) echo "stage-as-it-lands: unknown arg $1" >&2; exit 1 ;;
    esac
done
[ -n "$WATCH" ] && [ -n "$STAGE" ] || {
    echo "usage: stage-as-it-lands.sh --watch DIR --stage CMD [--interval S] [--state FILE] [--once|--drain] [--stable S]" >&2
    exit 1
}
[ -d "$WATCH" ] || { echo "stage-as-it-lands: watch dir missing: $WATCH" >&2; exit 2; }
[ -n "$STATE" ] || STATE="$WATCH/.stage-as-it-lands.state"
touch "$STATE" 2>/dev/null || { echo "stage-as-it-lands: cannot write state file: $STATE" >&2; exit 1; }

# is_staged <path> <size> <mtime> — 0 if already recorded.
is_staged() {
    grep -F -q -x "$2 $3 $1" "$STATE" 2>/dev/null
}
mark_staged() {
    printf '%s %s %s\n' "$2" "$3" "$1" >> "$STATE"
}

pass() {
    # One sweep: for every regular file under WATCH, if not staged and its
    # size is stable across --stable seconds, run the stage command and
    # record it ONLY if the stage command exits 0 (a failed stage retries).
    # Counts go to the files given as $1 (staged) and $2 (skipped as still
    # being written) — the find|while runs in a subshell, so variables
    # cannot carry the counts out.
    local staged_c="$1" unstable_c="$2"
    : > "$staged_c"; : > "$unstable_c"
    find "$WATCH" -type f ! -name "$(basename "$STATE")" -print0 2>/dev/null |
    while IFS= read -r -d '' f; do
        size1="$(stat -c %s "$f" 2>/dev/null || echo -1)"
        mtime1="$(stat -c %Y "$f" 2>/dev/null || echo -1)"
        [ "$size1" = "-1" ] && continue
        is_staged "$f" "$size1" "$mtime1" && continue
        sleep "$STABLE"
        size2="$(stat -c %s "$f" 2>/dev/null || echo -2)"
        if [ "$size1" != "$size2" ]; then echo x >> "$unstable_c"; continue; fi   # still being written
        if "$STAGE" "$f"; then
            mark_staged "$f" "$size1" "$mtime1"
            echo "stage-as-it-lands: staged $f ($size1 B)"
            echo x >> "$staged_c"
        else
            echo "stage-as-it-lands: stage FAILED for $f (rc=$?) — will retry" >&2
        fi
    done
}

if [ "$ONCE" = "1" ]; then
    # One sweep only: stages whatever is already stable at this moment.
    pass "$(mktemp)" "$(mktemp)"
    exit 0
fi
if [ "$DRAIN" = "1" ]; then
    # Repeat sweeps until one stages nothing AND nothing is still being
    # written. A file mid-write is skipped that sweep and caught later, so
    # --drain is safe to start while the producer is still running — it
    # only stops once the watch dir is quiet. (A producer that writes
    # forever keeps --drain looping; wrap it in `timeout` if that matters.)
    while true; do
        sc="$(mktemp)"; uc="$(mktemp)"
        pass "$sc" "$uc"
        n="$(wc -l < "$sc")"; u="$(wc -l < "$uc")"
        rm -f "$sc" "$uc"
        [ "$n" = "0" ] && [ "$u" = "0" ] && break
        sleep "$INTERVAL"
    done
    echo "stage-as-it-lands: drained — no more stageable files in $WATCH"
    exit 0
fi
echo "stage-as-it-lands: watching $WATCH every ${INTERVAL}s (state: $STATE)"
while true; do
    pass "$(mktemp)" "$(mktemp)" >/dev/null
    sleep "$INTERVAL"
done
