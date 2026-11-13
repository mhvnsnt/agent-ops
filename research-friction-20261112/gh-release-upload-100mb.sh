#!/usr/bin/env bash
# gh-release-upload-100mb.sh — release upload that enforces the owner
# 100 MB single standard (CloudDog PR #44, 2026-10-20) and the state+hash
# verify rule (never size-only).
#
# Why: lanes keep uploading 1.9 GB parts (store2.sh/chunker.py hardcode
# PART=1900000000). GitHub release upload is a single POST with no resume;
# a 1.9 GB POST dies with HTTP 408 "Upload body timed out due to
# inactivity" (2026-11-06) or stalls silently behind the egress proxy
# (wgpl part00, 2026-11-12). 100 MB parts bound the loss per stall to ~4 min.
#
# Usage:
#   ./gh-release-upload-100mb.sh --repo owner/repo --tag TAG --file FILE [--part-mb 100] [--no-verify]
#
# Behavior per part (part names: <basename>.part00, .part01, ...):
#   1. Preflight: gh auth, file exists, release exists (created by caller),
#      per-part asset state via gh api (state + size, never size-only).
#   2. Skip parts already `uploaded` at the expected size (idempotent re-run).
#   3. `starter` assets (empty 502 placeholders) are deleted first, then
#      re-uploaded. --clobber is NEVER used over a verified `uploaded` asset.
#   4. Upload with 3 attempts, 15/30/45 s backoff. gh has no retry; the loop
#      is the retry.
#   5. Verify (default on): re-query state=uploaded + size, then full
#      re-download of the part and sha256 compare. A part is not "done"
#      until the hash matches after pull-back.
#   6. Parts are kept in <file>.parts/ until verification passes, then
#      removed. Manifest <file>.parts/MANIFEST.sha256 is kept.
# Stdlib + gh CLI only. Never touches in-flight lanes; operates on its own
# release/tag only.
set -u
REPO=""; TAG=""; FILE=""; PART_MB=100; VERIFY=1
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="$2"; shift 2;;
    --tag) TAG="$2"; shift 2;;
    --file) FILE="$2"; shift 2;;
    --part-mb) PART_MB="$2"; shift 2;;
    --no-verify) VERIFY=0; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$REPO" ] && [ -n "$TAG" ] && [ -n "$FILE" ] || { echo "usage: $0 --repo owner/repo --tag TAG --file FILE [--part-mb 100] [--no-verify]" >&2; exit 2; }
[ -f "$FILE" ] || { echo "file not found: $FILE" >&2; exit 1; }
command -v gh >/dev/null || { echo "gh CLI required" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh not authenticated" >&2; exit 1; }

BASENAME=$(basename "$FILE")
PARTDIR="${FILE}.parts"
mkdir -p "$PARTDIR"
# Release must exist (caller creates it; never auto-create a release here).
gh api "repos/${REPO}/releases/tags/${TAG}" --jq '.id' >/dev/null 2>&1 \
  || { echo "release tag $TAG not found in $REPO — create it first" >&2; exit 1; }

# Split at the standard (skip if parts already exist from a prior run).
if ! ls "$PARTDIR/${BASENAME}.part"* >/dev/null 2>&1; then
  split -b "${PART_MB}M" -d "$FILE" "$PARTDIR/${BASENAME}.part"
  (cd "$PARTDIR" && sha256sum "${BASENAME}.part"* > MANIFEST.sha256)
  echo "split $(stat -c%s "$FILE") bytes into $(ls "$PARTDIR/${BASENAME}.part"* | wc -l) part(s) of ${PART_MB}M"
fi

asset_state() { # name -> "state size" or empty when absent
  gh api "repos/${REPO}/releases/tags/${TAG}" --jq \
    ".assets[] | select(.name==\"$1\") | \"\(.state) \(.size)\"" 2>/dev/null | head -1
}

fail=0
for part in "$PARTDIR/${BASENAME}.part"*; do
  pname=$(basename "$part")
  psize=$(stat -c%s "$part")
  psha=$(sha256sum "$part" | cut -d' ' -f1)
  st=$(asset_state "$pname")
  if [ -n "$st" ]; then
    state=$(echo "$st" | cut -d' ' -f1); size=$(echo "$st" | cut -d' ' -f2)
    if [ "$state" = "uploaded" ] && [ "$size" = "$psize" ]; then
      echo "SKIP $pname already uploaded ($size bytes, state=uploaded)"
      continue
    fi
    if [ "$state" = "starter" ]; then
      echo "DELETE starter asset $pname (502 placeholder) before retry"
      gh release delete-asset "$TAG" "$pname" --repo "$REPO" -y || { echo "delete-asset failed for $pname" >&2; fail=1; continue; }
    else
      echo "WARN $pname exists state=$state size=$size (expected $psize) — not clobbering, investigate" >&2
      fail=1; continue
    fi
  fi
  ok=0
  for attempt in 1 2 3; do
    if gh release upload "$TAG" "$part" --repo "$REPO" --clobber 2>"$PARTDIR/upload.err"; then ok=1; break; fi
    echo "upload $pname attempt $attempt failed: $(tail -2 "$PARTDIR/upload.err" | tr '\n' ' ')" >&2
    sleep $((attempt * 15))
  done
  [ "$ok" = 1 ] || { echo "FAILED $pname after 3 attempts" >&2; fail=1; continue; }
  st2=$(asset_state "$pname")
  state2=$(echo "$st2" | cut -d' ' -f1); size2=$(echo "$st2" | cut -d' ' -f2)
  if [ "$state2" != "uploaded" ] || [ "$size2" != "$psize" ]; then
    echo "VERIFY-STATE FAILED $pname: state=$state2 size=$size2 (expected uploaded $psize)" >&2; fail=1; continue
  fi
  if [ "$VERIFY" = 1 ]; then
    gh release download "$TAG" --repo "$REPO" --pattern "$pname" --dir "$PARTDIR/.verify" --clobber >/dev/null 2>&1
    vsha=$(sha256sum "$PARTDIR/.verify/$pname" 2>/dev/null | cut -d' ' -f1)
    if [ "$vsha" = "$psha" ]; then
      echo "VERIFIED $pname state=uploaded size=$psize sha256 match"
      rm -f "$PARTDIR/.verify/$pname"
    else
      echo "VERIFY-HASH FAILED $pname: got $vsha expected $psha" >&2; fail=1; continue
    fi
  else
    echo "UPLOADED $pname state=uploaded size=$psize (hash verify skipped --no-verify)"
  fi
done
rmdir "$PARTDIR/.verify" 2>/dev/null
if [ "$fail" = 0 ]; then
  echo "ALL PARTS DONE: $BASENAME ($TAG) — manifest at $PARTDIR/MANIFEST.sha256"
  rm -f "$PARTDIR/${BASENAME}.part"*
  exit 0
else
  echo "COMPLETED WITH FAILURES — parts kept in $PARTDIR for resume" >&2
  exit 1
fi
