#!/bin/bash
# var-tmp-audit.sh — find scripts that still point durable work at /var/tmp (2G tmpfs).
#
# Why: /tmp (512M) and /var/tmp (2G) are tmpfs on this VM and are WIPED on
# every VM restart. The 001R 6B lane lost 69 frames twice (2026-11-15) and
# the 6B gate + Pokemon pull-back both died Nov 17 when /var/tmp hit 100%
# (bl524 1.2G + pb-pokemon 844M). tmpfs-guard.sh (research-friction-20261115)
# exists, but as of 2026-11-18 NO lane script calls it — adoption is zero.
# This audit is the sweep that makes the gap visible. It changes nothing;
# it only reports.
#
# Usage:
#   var-tmp-audit.sh [--root DIR]        default root: ~/workspace/agent-ops
# Exit: 0 = no HARDCODED /var/tmp output dirs, 1 = at least one found,
#       2 = usage error.
#
# Classification per hit (a script can carry several):
#   HARDCODED   — literal /var/tmp assignment (e.g. PB="/var/tmp/...") with no
#                 env override and no tmpfs-guard call. Fails the audit.
#   OVERRIDABLE — PB="${PB:-/var/tmp/...}" — still defaults to tmpfs, but a
#                 lane can redirect it. Warns, does not fail.
#   GUARDED     — script calls tmpfs-guard.sh. Passes.
#   MENTION     — /var/tmp appears only in a comment or in the guard tools
#                 themselves. Listed, does not fail.
# Scope note: the audit greps *.sh under the root only (bounded — a full
# ~/workspace grep takes 5+ minutes across the 18G dream-girl tree). Lane
# workdirs outside agent-ops need their own run with --root.
set -u

ROOT="${HOME}/workspace/agent-ops"
while [ $# -gt 0 ]; do
    case "$1" in
        --root) ROOT="$2"; shift 2 ;;
        --root=*) ROOT="${1#--root=}"; shift ;;
        -h|--help)
            echo "usage: var-tmp-audit.sh [--root DIR]"
            exit 0 ;;
        *) echo "var-tmp-audit: unknown arg: $1" >&2; exit 2 ;;
    esac
done
[ -d "$ROOT" ] || { echo "var-tmp-audit: no such dir: $ROOT" >&2; exit 2; }

echo "var-tmp audit — root: $ROOT"
echo "tmpfs now: $(df -h --output=size,used,avail,pcent,target /var/tmp /tmp 2>/dev/null | tail -n +2 | tr '\n' ' ')"
echo

HARD=0
WARN=0
# *.sh only, skip .git and the merge-queue worktrees (mirrors, not live).
while IFS= read -r -d '' f; do
    rel="${f#$ROOT/}"
    # Does the script call the guard?
    if grep -q "tmpfs-guard" "$f" 2>/dev/null; then
        # The guard tools themselves mention /var/tmp in their own docs.
        case "$rel" in research-friction-20261115/*) echo "MENTION  $rel (guard tool itself)";; *) echo "GUARDED $rel";; esac
        continue
    fi
    # Literal /var/tmp assignment without env override?
    if grep -Eq '(^|[^"{])(PB|OUT|TMP|DIR|WORKDIR)?="?/var/tmp' "$f" 2>/dev/null \
       && ! grep -Eq '\$\{[A-Za-z_]+:-/var/tmp' "$f" 2>/dev/null; then
        echo "HARDCODED $rel"
        grep -n "/var/tmp" "$f" | head -5 | sed 's/^/    /'
        HARD=$((HARD + 1))
    elif grep -Eq '\$\{[A-Za-z_]+:-/var/tmp' "$f" 2>/dev/null; then
        echo "OVERRIDABLE $rel (default still /var/tmp)"
        grep -n "/var/tmp" "$f" | head -5 | sed 's/^/    /'
        WARN=$((WARN + 1))
    elif grep -q "/var/tmp" "$f" 2>/dev/null; then
        echo "MENTION  $rel (comment/docs only)"
    fi
done < <(find "$ROOT" -type d \( -name .git -o -name "*worktrees*" \) -prune -o -type f -name "*.sh" -print0 2>/dev/null)

echo
echo "HARDCODED: $HARD  OVERRIDABLE: $WARN"
if [ "$HARD" -gt 0 ]; then
    echo "FAIL: $HARD script(s) hardcode a /var/tmp output dir — one 2G tmpfs fill kills them (Nov 17 precedent)."
    exit 1
fi
echo "PASS: no hardcoded /var/tmp output dirs under $ROOT."
exit 0
