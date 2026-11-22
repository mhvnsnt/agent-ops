#!/bin/bash
# guardian-offload-20261021.sh — upload dir trees to GitHub release, verify byte-identical, journal.
# Does NOT delete. Deletion happens only after full journal verify, per ONE-STORE RULE.
set -u
REPO="mhvnsnt/clouddog-storage"
TAG="guardian-offload-20261021"
JOURNAL="$HOME/workspace/agent-ops/guardian-offload-20261021.journal.tsv"
LOG="$HOME/workspace/agent-ops/guardian-offload-20261021.log"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

ensure_release() {
  if ! gh release view "$TAG" --repo "$REPO" >/dev/null 2>&1; then
    gh release create "$TAG" --repo "$REPO" --title "Guardian offload 2026-10-21 (disk emergency)" \
      --notes "Emergency offload by disk-space-guardian run 2026-10-21 00:14 CDT. Directories stored as individually verified release assets (name = tree-prefixed path). Journal: guardian-offload-20261021.journal.tsv" \
      || { log "FATAL: release create failed"; exit 1; }
    log "created release $TAG"
  else
    log "release $TAG exists"
  fi
}

# asset_exists <assetname> <localsize> -> prints "have" if a byte-identical asset already present
asset_verified_present() {
  local asset="$1" localsize="$2" localsha="$3"
  local info
  info=$(gh release view "$TAG" --repo "$REPO" --json assets --jq ".assets[] | select(.name==\"$asset\") | [.size|tostring] | join(\",\")" 2>/dev/null)
  if [ "$info" = "$localsize" ]; then
    log "asset $asset already present with matching size $localsize — re-verifying sha"
    local tmp; tmp=$(mktemp)
    gh release download "$TAG" --repo "$REPO" -p "$asset" -O "$tmp" -D "$(dirname "$tmp")" >/dev/null 2>&1 || { log "WARN: re-download failed for $asset"; rm -f "$tmp"; return 1; }
    local dlsha; dlsha=$(sha256sum "$tmp" | cut -d' ' -f1); rm -f "$tmp"
    [ "$dlsha" = "$localsha" ] && { log "asset $asset sha256 matches — skipping re-upload"; return 0; }
    log "WARN: $asset present but sha differs — re-uploading"
    return 1
  fi
  return 1
}

upload_tree() {
  local srcdir="$1" prefix="$2"
  [ -d "$srcdir" ] || { log "SKIP: $srcdir missing"; return 0; }
  log "=== tree $srcdir (prefix $prefix) ==="
  local n_ok=0 n_fail=0
  while IFS= read -r -d '' f; do
    local rel="${f#$srcdir/}"
    local asset="${prefix}__$(echo "$rel" | tr '/' '_')"
    local size; size=$(stat -c%s "$f")
    local sha; sha=$(sha256sum "$f" | cut -d' ' -f1)
    # journal hit?
    if grep -qP "^\Q${asset}\E\t" "$JOURNAL" 2>/dev/null; then
      local jsha; jsha=$(grep -P "^\Q${asset}\E\t" "$JOURNAL" | cut -f3)
      if [ "$jsha" = "$sha" ]; then n_ok=$((n_ok+1)); continue; fi
    fi
    if asset_verified_present "$asset" "$size" "$sha"; then
      printf '%s\t%s\t%s\t%s\n' "$asset" "$size" "$sha" "$srcdir/$rel" >> "$JOURNAL"
      n_ok=$((n_ok+1)); continue
    fi
    log "upload $asset ($size bytes)"
    if gh release upload "$TAG" --repo "$REPO" "$f#$asset" --clobber >/dev/null 2>&1; then
      # verify: download back, compare
      local tmp; tmp=$(mktemp)
      if gh release download "$TAG" --repo "$REPO" -p "$asset" -O "$tmp" -D "$(dirname "$tmp")" >/dev/null 2>&1; then
        local dlsha; dlsha=$(sha256sum "$tmp" | cut -d' ' -f1)
        local dlsize; dlsize=$(stat -c%s "$tmp")
        rm -f "$tmp"
        if [ "$dlsha" = "$sha" ] && [ "$dlsize" = "$size" ]; then
          printf '%s\t%s\t%s\t%s\n' "$asset" "$size" "$sha" "$srcdir/$rel" >> "$JOURNAL"
          n_ok=$((n_ok+1)); log "verified $asset"
        else
          log "FAIL sha/size mismatch after upload: $asset (local $sha/$size vs store $dlsha/$dlsize)"
          n_fail=$((n_fail+1))
        fi
      else
        log "FAIL download-back failed: $asset"
        n_fail=$((n_fail+1))
      fi
    else
      log "FAIL upload failed: $asset"
      n_fail=$((n_fail+1))
    fi
  done < <(find "$srcdir" -type f -print0)
  log "tree $srcdir done: ok=$n_ok fail=$n_fail"
  return 0
}

touch "$JOURNAL" 2>/dev/null || JOURNAL="/tmp/guardian-offload-20261021.journal.tsv"
touch "$JOURNAL"
ensure_release
upload_tree "/home/hatch/workspace/wh-pose-survey/models" "wh-pose-survey-models"
upload_tree "/home/hatch/workspace/rigwork-tmp/float" "rigwork-tmp-float"
upload_tree "/home/hatch/workspace/rigwork-tmp/decoded" "rigwork-tmp-decoded"
log "ALL TREES DONE"
