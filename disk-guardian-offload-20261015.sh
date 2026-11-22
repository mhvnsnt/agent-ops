#!/bin/bash
# disk-guardian bulk offload lane v2 (2026-10-15 21:01 EDT cron).
# Drive quota EXCEEDED -> GitHub release pipe on mhvnsnt/drive-storage.
# SAFE DESIGN: tar|split streams (no intermediate tar file); each part is
# uploaded -> download-back sha256-verified -> part deleted immediately.
# Peak extra disk = current item's parts only. Source dir is deleted ONLY
# after EVERY part is individually verified. Idempotent: re-runnable.
set -u
REPO=mhvnsnt/drive-storage
TAG=bulk-archive-2026-10-15
WORK=~/workspace/.guardian-offload-20261015
LOG=~/workspace/agent-ops/disk-cleanup-log.md
CKPT=~/workspace/agent-ops/checkpoints/disk-guardian-offload-20261015.json
WS=~/workspace
mkdir -p "$WORK"
cd "$WS" || exit 1

beat() {
  python3 - "$CKPT" "$1" <<'EOF'
import json,sys,datetime
p=sys.argv[1]; note=sys.argv[2]
try:
  d=json.load(open(p))
  d["updated_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
  d["last_heartbeat"]=d["updated_at"]
  d["notes"]=(((d.get("notes") or "")+"\n"+datetime.datetime.now().strftime("%H:%M")+" "+note)[-4000:])
  json.dump(d,open(p,"w"),indent=1)
except Exception as e: print("beat failed:",e)
EOF
}

disk_ok() { # abort if we'd risk the 88% ceiling
  local u; u=$(df /home/hatch | tail -1 | awk '{print $5}' | tr -d '%')
  [ "$u" -lt 87 ]
}

ensure_release() {
  if ! gh release view "$TAG" --repo "$REPO" >/dev/null 2>&1; then
    gh release create "$TAG" --repo "$REPO" --draft \
      --title "bulk-archive 2026-10-15 (disk-guardian)" \
      --notes "Disk-guardian bulk offload 2026-10-15. Each asset group = 1G-split tar parts of a local dir, each part individually sha256-verified by download-back before local deletion. Reassemble: cat <name>.part-* > <name>.tar ; tar -xf <name>.tar" \
      || { echo "FATAL: cannot create release"; exit 1; }
  fi
}

remote_has() {
  gh release view "$TAG" --repo "$REPO" --json assets -q '.assets[].name' 2>/dev/null | grep -qx "$1"
}

verify_part() { # $1=itemdir $2=partpath ; downloads back, sha256-checks, deletes part on success
  local idir="$1" part="$2" asset vdir ok try
  asset=$(basename "$part"); vdir="$idir/v"; mkdir -p "$vdir"
  ok=0
  for try in 1 2 3 4 5; do
    if gh release download "$TAG" --repo "$REPO" -p "$asset" -D "$vdir" --clobber >/dev/null 2>&1; then ok=1; break; fi
    echo "retry dl-verify $asset try $try"; sleep 10
  done
  [ "$ok" = 1 ] || { echo "FATAL dl-verify $asset"; beat "VERIFY-DL FAILED $asset"; return 1; }
  if ( cd "$idir" && grep -F " $asset" parts.sha256 | ( cd "$vdir" && sha256sum -c --status ) ); then
    rm -f "$part" "$vdir/$asset"
    echo "$asset" >> "$idir/verified.list"
    return 0
  fi
  echo "FATAL sha256 mismatch $asset"; beat "SHA256 MISMATCH $asset"; return 1
}

# item format: "archivename|tar-args..." (tar args relative to $WS)
process_item() {
  local name="$1"; shift
  local idir="$WORK/$name"
  local pdir="$idir/parts"
  mkdir -p "$pdir"
  # already fully done?
  [ -f "$idir/deleted.done" ] && { echo "DONE $name"; return 0; }

  # 1. stream tar|split (skip if already split)
  if [ ! -f "$idir/split.done" ]; then
    disk_ok || { echo "ABORT: disk >=87%, refusing to stage more"; beat "ABORT disk>=87%"; exit 2; }
    echo "STAGING $name"
    rm -f "$pdir"/*
    # shellcheck disable=SC2086
    tar -cf - -C "$WS" $* | split -b 1G - "$pdir/$name.part-"
    ( cd "$pdir" && sha256sum "$name".part-* > "$idir/parts.sha256" )
    touch "$idir/split.done"
  fi
  touch "$idir/verified.list"

  # 2. upload + verify each remaining part
  for part in "$pdir"/$name.part-*; do
    [ -f "$part" ] || continue
    local asset; asset=$(basename "$part")
    grep -qx "$asset" "$idir/verified.list" 2>/dev/null && continue
    if ! remote_has "$asset"; then
      local ok=0 try
      for try in 1 2 3 4 5; do
        if gh release upload "$TAG" "$part" --repo "$REPO" --clobber >/dev/null 2>&1; then ok=1; break; fi
        echo "retry up $asset try $try"; sleep 10
      done
      [ "$ok" = 1 ] || { echo "FATAL upload $asset"; beat "UPLOAD FAILED $asset"; exit 1; }
    fi
    verify_part "$idir" "$part" || exit 1
    beat "verified $asset"
  done

  # 3. all parts verified? (parts dir empty + every sha256 entry in verified.list)
  local total verified
  total=$(wc -l < "$idir/parts.sha256"); verified=$(wc -l < "$idir/verified.list")
  if [ "$total" = "$verified" ] && [ "$total" -gt 0 ]; then
    echo "ALL $total PARTS VERIFIED for $name"
    return 0
  fi
  echo "FATAL: part count mismatch $name ($verified/$total)"; exit 1
}

delete_source() { # $1=archivename $2=human label for log ; only call after process_item verified
  local name="$1" label="$2" idir="$WORK/$name"
  local total verified
  total=$(wc -l < "$idir/parts.sha256"); verified=$(wc -l < "$idir/verified.list")
  [ "$total" = "$verified" ] && [ "$total" -gt 0 ] || { echo "REFUSE delete $name: not fully verified"; exit 1; }
  echo "DELETING local $label"
  # shellcheck disable=SC2086
  rm -rf $3 || { echo "FATAL rm $label"; exit 1; }
  rm -rf "$idir/v"
  touch "$idir/deleted.done"
  echo "$(date -u +%FT%TZ) guardian-offload: $label archived to GitHub release $TAG ($REPO), all $total parts download-back sha256 verified, local deleted" >> "$LOG"
  beat "DELETED $label"
}

ensure_release
beat "lane v2 started"

# ---- small untouched-7d dirs first (each <400M) ----
process_item concrete-dragon-itch-builds concrete-dragon-itch/builds && delete_source concrete-dragon-itch-builds "concrete-dragon-itch/builds" "$WS/concrete-dragon-itch/builds"
process_item case-studies case-studies && delete_source case-studies "case-studies" "$WS/case-studies"
process_item brutalfist-fix-public brutalfist-fix/public && delete_source brutalfist-fix-public "brutalfist-fix/public" "$WS/brutalfist-fix/public"
process_item ashlane-art ashlane-art && delete_source ashlane-art "ashlane-art" "$WS/ashlane-art"
process_item concrete-dragon-ads concrete-dragon-ads && delete_source concrete-dragon-ads "concrete-dragon-ads" "$WS/concrete-dragon-ads"
process_item wt-soul .wt-soul && delete_source wt-soul ".wt-soul" "$WS/.wt-soul"
process_item wave5dl wave5dl && delete_source wave5dl "wave5dl" "$WS/wave5dl"
process_item menu-research-dl menu-research-dl && delete_source menu-research-dl "menu-research-dl" "$WS/menu-research-dl"

# ---- hero-parts-pull in pieces (keeps peak staging low) ----
process_item hero-parts-extracted hero-parts-pull/extracted && delete_source hero-parts-extracted "hero-parts-pull/extracted" "$WS/hero-parts-pull/extracted"
process_item hero-parts-okko-out hero-parts-pull/okko-out && delete_source hero-parts-okko-out "hero-parts-pull/okko-out" "$WS/hero-parts-pull/okko-out"
process_item hero-parts-top --exclude=hero-parts-pull/extracted --exclude=hero-parts-pull/okko-out hero-parts-pull && delete_source hero-parts-top "hero-parts-pull (top-level files)" "$WS/hero-parts-pull"

# publish only when every source dir is gone
for d in "$WS/concrete-dragon-itch/builds" "$WS/case-studies" "$WS/brutalfist-fix/public" "$WS/ashlane-art" "$WS/concrete-dragon-ads" "$WS/.wt-soul" "$WS/wave5dl" "$WS/menu-research-dl" "$WS/hero-parts-pull"; do
  [ -e "$d" ] && { echo "NOT ALL DONE, $d remains"; exit 1; }
done
rm -rf "$WORK"
gh release edit "$TAG" --repo "$REPO" --draft=false
python3 - "$CKPT" <<'EOF'
import json,sys,datetime
p=sys.argv[1]
d=json.load(open(p))
d["status"]="done"
d["updated_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
d["last_heartbeat"]=d["updated_at"]
json.dump(d,open(p,"w"),indent=1)
EOF
beat "ALL DONE, release published"
echo "ALL DONE - release $TAG published"
