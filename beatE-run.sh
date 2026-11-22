#!/bin/bash
# Beat E store-and-clear run. Incremental, restart-resilient:
# registry + log appended per dir AFTER verification, before deletion.
set -euo pipefail
REPO="mhvnsnt/western-heart"
ARCH=~/workspace/.beatE-tmp   # /tmp is only 512MB tmpfs; parts live here, removed per-dir after verify
LOG=~/workspace/agent-ops/disk-cleanup-log.md
REG=~/workspace/agent-ops/cloud-dog-registry.json
mkdir -p "$ARCH"

log(){ echo "$@" | tee -a "$LOG"; }
utc(){ date -u +%Y-%m-%dT%H:%M:%SZ; }
abort(){ log "- ABORT: $1 — local files intact, no deletions"; exit 1; }

verify_and_record(){
  local name="$1" tag="$2" partdir="$3"
  log "- [$(utc)] BEAT E: verifying release $tag ..."
  # Drafts are invisible to /releases/tags/{tag} (404) — resolve by ID
  local rid=$(gh api "repos/$REPO/releases" --jq ".[] | select(.tag_name==\"$tag\") | .id" 2>/dev/null | head -1)
  if [ -z "$rid" ]; then log "  VERIFY FAIL: no release found for tag $tag"; return 1; fi
  # API own-eyes: asset name+size must match local part sizes byte-exact
  local ok=1
  while read -r fname; do
    local sz=$(stat -c %s "$partdir/$fname")
    local rsz=$(gh api "repos/$REPO/releases/$rid" --jq ".assets[] | select(.name==\"$fname\") | .size" 2>/dev/null)
    if [ "$sz" != "$rsz" ]; then log "  VERIFY FAIL $fname local=$sz remote=$rsz"; ok=0; fi
  done < <(cd "$partdir" && ls *.part-* SHA256SUMS-arch.txt)
  local nremote=$(gh api "repos/$REPO/releases/$rid" --jq '.assets | length' 2>/dev/null)
  local nlocal=$(ls "$partdir"/*.part-* "$partdir"/SHA256SUMS-arch.txt | wc -l)
  if [ "$nremote" != "$nlocal" ]; then log "  VERIFY FAIL asset count remote=$nremote local=$nlocal"; ok=0; fi
  if [ "$ok" != "1" ]; then log "  VERIFICATION FAILED for $tag — nothing deleted, manual review needed"; return 1; fi
  # Own-eyes hash verification for EVERY asset via GitHub sha256 digests
  # (digest API returns the hash of the stored bytes — no download needed)
  local hok=1
  while read -r fname; do
    local wh=$(sha256sum "$partdir/$fname" | cut -d' ' -f1)
    local rd=$(gh api "repos/$REPO/releases/$rid" --jq ".assets[] | select(.name==\"$fname\") | (.digest // \"\") | sub(\"sha256:\";\"\")" 2>/dev/null)
    if [ "$wh" != "$rd" ]; then log "  VERIFY FAIL digest $fname local=$wh remote=$rd"; hok=0; fi
  done < <(cd "$partdir" && ls *.part-* SHA256SUMS-arch.txt)
  if [ "$hok" != "1" ]; then log "  VERIFICATION FAILED for $tag (digest mismatch) — nothing deleted"; return 1; fi
  log "  VERIFIED: $nlocal assets, byte-exact sizes, ALL sha256 digests MATCH"
  return 0
}

# Resume-aware upload: gh uploads assets in PARALLEL, so any subset may land.
# Create the (draft) release empty, then upload only assets not already on it.
resume_upload(){
  local tag="$1" partdir="$2" title="$3" notes="$4"
  local t=1
  while [ $t -le 4 ]; do
    if gh release view "$tag" -R "$REPO" >/dev/null 2>&1; then
      log "- release $tag established"; break
    fi
    gh release create "$tag" -R "$REPO" --title "$title" --notes "$notes" --draft >/dev/null 2>&1
    sleep 5; t=$((t+1))
  done
  if ! gh release view "$tag" -R "$REPO" >/dev/null 2>&1; then
    log "- WARNING: release $tag could not be established (proxy) — uploads will fail; verify gate will block deletion"
  fi
  local existing
  for f in "$partdir"/$tag.tar.part-* "$partdir/SHA256SUMS-arch.txt"; do
    local b=$(basename "$f") want=$(stat -c %s "$f") whash=$(sha256sum "$f" | cut -d' ' -f1) a=1 done=0
    while [ $a -le 5 ]; do
      local rid2=$(gh api "repos/$REPO/releases" --jq ".[] | select(.tag_name==\"$tag\") | .id" 2>/dev/null | head -1)
      local existing="" edigest=""
      [ -n "$rid2" ] && existing=$(gh api "repos/$REPO/releases/$rid2" --jq '.assets[] | select(.name=="'"$b"'") | .size' 2>/dev/null)
      [ -n "$rid2" ] && edigest=$(gh api "repos/$REPO/releases/$rid2" --jq '.assets[] | select(.name=="'"$b"'") | (.digest // "") | sub("sha256:";"")' 2>/dev/null)
      if [ "$existing" = "$want" ] && [ "$edigest" = "$whash" ]; then log "  - $b present ($want B, digest MATCH), skipping"; done=1; break; fi
      if [ -n "$existing" ]; then
        log "  - $b present with mismatched size/digest (stale) — deleting and re-uploading"
        gh release delete-asset "$tag" "$b" -R "$REPO" --yes 2>/dev/null
      fi
      log "  - uploading $b (try $a)"
      gh release upload "$tag" -R "$REPO" "$f" 2>/dev/null && done=1 && break
      log "  - $b try $a failed (proxy), retrying"; sleep $((a*20)); a=$((a+1))
    done
    if [ $done -ne 1 ]; then log "  - $b still missing after 5 tries — verification will catch this; NOTHING will be deleted unless complete"; fi
  done
  return 0
  # NOTE: no early abort here. verify_and_record is the gate: only when every
  # asset is byte-exact (count + sizes + spot hash) do we touch local files.
}

store_clear(){
  local name="$1" dir="$2" tag="$3" title="$4" notes="$5"
  if [ ! -d ~/workspace/"$dir" ] || [ -z "$(ls -A ~/workspace/"$dir" 2>/dev/null)" ]; then
    log "## Beat E $(date -u +%Y-%m-%dT%H:%M:%SZ) — $name ($dir): dir empty or gone (already cleared in a prior run) — skipping"
    return 0
  fi
  log "## Beat E $(date -u +%Y-%m-%dT%H:%M:%SZ) — $name ($dir)"
  local partdir="$ARCH/$name"; mkdir -p "$partdir"
  # Guarded manifest BEFORE tar (for safe delete later)
  (cd ~/workspace && find "$dir" -type f | sort | while read -r f; do sha256sum "$f"; done > "$partdir/manifest.txt")
  log "- tar/split $dir (pre-tar manifest: $(wc -l < "$partdir/manifest.txt") files)"
  local tarfile="$partdir/$tag.tar"
  tar -C ~/workspace -cf "$tarfile" "$dir"
  local tarbytes=$(stat -c %s "$tarfile")
  split -b 100M "$tarfile" "$partdir/$tag.tar.part-"
  local partbytes=$(cat "$partdir"/$tag.tar.part-* | wc -c)
  if [ "$partbytes" != "$tarbytes" ]; then abort "split integrity: parts=$partbytes != tar=$tarbytes for $dir"; fi
  rm -f "$tarfile"   # splits now hold the data
  (cd "$partdir" && sha256sum *.part-* > SHA256SUMS-arch.txt)
  local nparts=$(ls "$partdir"/*.part-* | wc -l)
  local bytes=$(cat "$partdir"/*.part-* | wc -c)
  log "- $nparts parts, $bytes bytes total"
  if ! resume_upload "$tag" "$partdir" "$title" "$notes"; then
    log "- UPLOAD FAILED after retries — leaving local intact"
    return 1
  fi
  if ! verify_and_record "$name" "$tag" "$partdir"; then return 1; fi
  # Registry entry (append per-dir so restarts keep the record)
  python3 - "$name" "$dir" "$tag" "$REPO" "$partdir" <<'EOF' >> "$REG.tmp"
import json,sys,os,time
name,dirn,tag,repo,partdir=sys.argv[1:6]
reg=json.load(open(os.path.expanduser("~/workspace/agent-ops/cloud-dog-registry.json")))
entry={"path":"/home/hatch/workspace/"+dirn,"tag":tag,"repo":repo,"assets":[a for a in os.listdir(partdir) if a.startswith(tag+".tar.part-") or a=="SHA256SUMS-arch.txt"],"release":"draft:"+tag,"verified":"byte-exact sizes via GitHub API + spot sha256","cleared":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"beat":"E","pullback":"gh release download "+tag+" -R "+repo+" -D ~/workspace/pullback-"+name+" && cd ~/workspace/pullback-"+name+" && cat "+tag+".tar.part-* > "+name+".tar && tar -xf "+name+".tar -C ~/workspace"}
reg.append(entry)
json.dump(reg,open(os.path.expanduser("~/workspace/agent-ops/cloud-dog-registry.json"),"w"),indent=2)
EOF
  if [ -s "$REG.tmp" ]; then :; fi; rm -f "$REG.tmp"
  log "- registry updated"
  # Guarded delete: only files whose current hash == tar-time hash; keep dir shell + anything new/changed
  local freed=0 kept=0
  while read -r want f; do
    local rel=${f#/home/hatch/workspace/}
    if [ -f "$f" ] && [ "$(sha256sum "$f" | cut -d' ' -f1)" = "$want" ]; then
      local s=$(stat -c %s "$f"); rm -f "$f"; freed=$((freed+s))
    else kept=$((kept+1)); fi
  done < "$partdir/manifest.txt"
  find ~/workspace/$dir -type d -empty -delete 2>/dev/null
  log "- deleted $freed bytes from $dir; kept $kept files (new/changed since tar, or already gone)"
  log "- Pull-back: gh release download $tag -R $REPO -D ~/workspace/pullback-$name && cd ~/workspace/pullback-$name && cat $tag.tar.part-* > $name.tar && tar -xf $name.tar -C ~/workspace"
  rm -rf "$partdir"   # free staging space incrementally
  return 0
}

# DISABLED-done: tripo-downloads cleared manually

store_clear "tripo-wire" "tripo-wire-20261019" "tripo-wire-20261019" \
  "Tripo wiring workdir 2026-10-19 (1019M)" \
  "Disk-cleanup Beat E archive: ~/workspace/tripo-wire-20261019 as of 2026-10-19 (Tripo pulls2/pulls3, decoded dec/dec2/dec3 GLBs, render scripts, tpose-ref X.png renders; several renders already committed to western-heart). Own-eyes verified byte-exact."

# DISABLED-for-manual: skin-research cleared manually

log "- [$(utc)] BEAT E script finished"
