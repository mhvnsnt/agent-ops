#!/bin/bash
# tmpfs-guard.sh — fail closed when a render/checkpoint output path sits on tmpfs.
#
# Why: /tmp and /var/tmp are tmpfs on this VM (512 MB and ~2 GB) and are WIPED
# on every VM restart. The Dream Girl 001R 6B lane lost 69 rendered character
# frames TWICE on 2026-11-15 because its output dir was /var/tmp/cut001r —
# and the re-render rebuilt in /var/tmp AGAIN the same night (see
# agent-ops/CUT001R-6B-VM-RESTART-LOSS-20261115.md). A render that takes
# hours must never point at a filesystem that dies with the cell.
#
# Usage:
#   tmpfs-guard.sh <path> [<path>...]     exit 0 = all durable, 2 = a path is tmpfs
#   source tmpfs-guard.sh; tmpfs_guard <path>   (same check as a function)
#
# Render/gate scripts should call this on their OUT dir BEFORE the first
# frame:  tmpfs-guard.sh "$OUT" || exit 2
# Exit 2 is deliberate: distinct from generic failure (1) so callers and
# watchdogs can tell "bad output path" apart from "render failed".
#
# Detection: `stat -f -c %T` (coreutils) with a `df -T` fallback. tmpfs is
# the only failing type today; add types to TMPFS_TYPES only with evidence.
set -u

TMPFS_TYPES="tmpfs"

# tmpfs_guard <path> — exit 0 durable, 2 tmpfs/unreadable, prints one line.
tmpfs_guard() {
    local path="$1" fstype=""
    if [ ! -e "$path" ]; then
        # Path does not exist yet: check its nearest existing parent.
        local parent="$path"
        while [ ! -e "$parent" ] && [ "$parent" != "/" ] && [ "$parent" != "." ]; do
            parent="$(dirname "$parent")"
        done
        path="$parent"
    fi
    fstype="$(stat -f -c %T "$path" 2>/dev/null || true)"
    if [ -z "$fstype" ]; then
        fstype="$(df -T --output=fstype "$path" 2>/dev/null | tail -n +2 | tr -d ' ' || true)"
    fi
    if [ -z "$fstype" ]; then
        echo "tmpfs-guard: cannot determine filesystem for $1 (treating as UNSAFE)" >&2
        return 2
    fi
    case " $TMPFS_TYPES " in
        *" $fstype "*)
            echo "tmpfs-guard: UNSAFE $1 is on $fstype — output will not survive a VM restart" >&2
            return 2
            ;;
        *)
            echo "tmpfs-guard: ok $1 is on $fstype"
            return 0
            ;;
    esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    if [ "$#" -eq 0 ]; then
        echo "usage: tmpfs-guard.sh <path> [<path>...]" >&2
        exit 1
    fi
    rc=0
    for p in "$@"; do
        tmpfs_guard "$p" || rc=2
    done
    exit "$rc"
fi
