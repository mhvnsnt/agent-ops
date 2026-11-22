#!/bin/bash
# disk-space-guardian 2026-10-20 21:5x run — resume stalled creation-suite-playable parts upload
# DELETE-AS-YOU-GO: verify each part on the release (size), delete local, fsync log.
STG="$HOME/workspace/.whlane-stg-creation-suite-playable"
REPO="mhvnsnt/clouddog-storage"
TAG="whwork-creation-suite-playable-20261020"
LOG="$HOME/workspace/agent-ops/disk-cleanup-log.md"
remote_list() { gh api "repos/$REPO/releases/tags/$TAG" --jq '.assets[].name' 2>/dev/null; }
UP="$(remote_list)"
for f in $(cd "$STG" && ls whwork-creation-suite-playable-20261020.tar.part-* 2>/dev/null | sort); do
  name="$f"
  if echo "$UP" | grep -qx "$name"; then
    rsz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"$name\") | .size" 2>/dev/null)
    lsz=$(stat -c%s "$STG/$name")
    if [ "$rsz" == "$lsz" ]; then
      sha=$(sha256sum "$STG/$name" | awk '{print $1}')
      rm -f "$STG/$name"
      echo "$(date -u +%FT%TZ) [guardian] DELETE-AS-YOU-GO csp $name verified on $TAG ($lsz bytes sha256=$sha) — local deleted" >> "$LOG"; sync
      continue
    fi
  fi
  ok=0
  for attempt in 1 2 3 4; do
    if gh release upload "$TAG" "$STG/$name" --repo "$REPO" --clobber >/tmp/csp-up-$name.log 2>&1; then ok=1; break; fi
    sleep $((attempt*45))
  done
  if [ $ok -eq 0 ]; then
    echo "$(date -u +%FT%TZ) [guardian] csp $name upload FAILED after 4 attempts — kept locally, aborting rest" >> "$LOG"; exit 1
  fi
  rsz=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"$name\") | .size" 2>/dev/null)
  lsz=$(stat -c%s "$STG/$name")
  if [ "$rsz" == "$lsz" ]; then
    sha=$(sha256sum "$STG/$name" | awk '{print $1}')
    rm -f "$STG/$name"
    echo "$(date -u +%FT%TZ) [guardian] DELETE-AS-YOU-GO csp $name uploaded+verified ($lsz bytes sha256=$sha) — local deleted" >> "$LOG"; sync
  else
    echo "$(date -u +%FT%TZ) [guardian] csp $name SIZE MISMATCH local=$lsz remote=$rsz — kept" >> "$LOG"; exit 2
  fi
done
echo "$(date -u +%FT%TZ) [guardian] csp parts all verified — staging dir empty" >> "$LOG"
