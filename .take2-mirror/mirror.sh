#!/bin/bash
# sitting-take2-scene-mirror: back up ~/workspace/sitcanon-work/ scene files
# to GitHub release sitting-wt-sitcanon-20261019 (mhvnsnt/cape-jones).
# Idempotent, resume-safe: processes ONE group per invocation, updates the
# checkpoint JSON after every verified part. Run via overnight-idle-pipeline.
#
# Safety: NEVER touches the source files (read-only). Local staging parts are
# transient transfer copies; each is deleted only after its upload is verified
# by name+size against the release asset API. Source blends stay on disk.

set -u
SRC="$HOME/workspace/sitcanon-work"
STAGE="$HOME/workspace/agent-ops/.take2-mirror"
CKPT="$HOME/workspace/agent-ops/checkpoints/sitting-take2-scene-mirror.json"
REPO="mhvnsnt/cape-jones"
REL="sitting-wt-sitcanon-20261019"
PART_BYTES=104857600   # 100M, the owner's single standard

mkdir -p "$STAGE"

# file groups (each tar ~<=650MB to keep disk peak under the 88% ceiling)
declare -A FILEGROUPS=(
 [A]="scene_baked.blend scene_work.blend scene_sit_phys.blend@ proofs render.log check_cape.py check_rest.py check_rots.py check_vis.py del_cape.py diag_tear.py find_spikes.py fix_twist.py fix_twist_fast.py list_mesh.py render_clay.py render_closeup.py render_final.py"
 [B]="scene_legrest_retracted2.blend scene_legrest_retracted.blend scene_baked2.blend"
 [C]="scene_wave2.blend rig_wave2.blend scene_sit_hisexact.blend scene_sit_hisexact2.blend"
 [D]="scene_sit_hisexact3.blend scene_sit_placed.blend scene_sit_placed.blend1 scene_sit.blend"
 [E]="scene_sit_trs.blend scene_sit_dropped.blend scene_sit_render.blend"
 [F]="scene_sit_phys.blend scene_sit_phys_fixed.blend scene_sit_phys.blend1"
)

log() { echo "[$(date -u +%H:%M:%SZ)] $*"; }

ckpt_set() {
  # usage: ckpt_set <field> <value>   (updates JSON + heartbeat)
  python3 - "$CKPT" "$1" "$2" <<'EOF'
import json,sys,datetime
p,f,v=sys.argv[1],sys.argv[2],sys.argv[3]
d=json.load(open(p))
d[f]=v
d['updated_at']=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
d['heartbeat']=d['updated_at']
json.dump(d,open(p,'w'),indent=1)
EOF
}

# --- which groups are done? -----------------------------------------------
done_groups=$(python3 -c "import json; d=json.load(open('$CKPT')); print(' '.join(d.get('groups_done',[])))" 2>/dev/null)
next=""
for g in A B C D E F; do
  case " $done_groups " in *" $g "*) ;; *) next="$g"; break;; esac
done
if [ -z "$next" ]; then
  log "ALL GROUPS UPLOADED. Final verify pending (re-download pass)."
  ckpt_set status "awaiting_final_verify"
  exit 0
fi
g="$next"
files="${FILEGROUPS[$g]}"
log "GROUP $g: files=$files"

# verify all source files exist before tarring
missing=0
for f in $files; do
  [ -e "$SRC/$f" ] || { log "MISSING SOURCE: $f"; missing=1; }
done
[ "$missing" = "1" ] && { ckpt_set status "needs_owner"; log "MISSING SOURCES - set needs_owner"; exit 1; }

# --- build deterministic tar, split into 100M parts -------------------------
tarfile="$STAGE/take2-$g.tar"
log "tarring group $g ..."
(cd "$SRC" && tar --sort=name --mtime='2026-10-20' --owner=0 --group=0 --numeric-owner -cf "$tarfile" $files) || { log "TAR FAILED"; exit 1; }
tarsha=$(sha256sum "$tarfile" | cut -d' ' -f1)
tarsize=$(stat -c %s "$tarfile")
log "tar sha256=$tarsha size=$tarsize"
split -b $PART_BYTES "$tarfile" "$STAGE/take2-$g.tar.part-"
rm -f "$tarfile"   # tar reassemblable from parts; parts are the store units

# --- upload each part, verify by name+size, delete staging part --------------
asset_list() {
  gh api "repos/$REPO/releases" --jq ".[] | select(.tag_name==\"$REL\") | .assets[] | \"\(.name) \(.size)\"" 2>/dev/null
}
fail=0
for part in "$STAGE"/take2-$g.tar.part-*; do
  name=$(basename "$part")
  size=$(stat -c %s "$part")
  # skip if already on the release with matching size (idempotent resume)
  if asset_list | grep -q "^$name $size$"; then
    log "SKIP (already on release): $name"
  else
    log "upload $name (${size}B) ..."
    if ! gh release upload "$REL" "$part" --repo "$REPO" --clobber 2>&1 | tail -1; then
      log "UPLOAD FAILED: $name"; fail=1; break
    fi
    # verify: name+size present on release
    if asset_list | grep -q "^$name $size$"; then
      log "VERIFIED: $name ($size B on release)"
    else
      log "VERIFY FAILED (not found on release): $name"; fail=1; break
    fi
  fi
  sha=$(sha256sum "$part" | cut -d' ' -f1)
  python3 - "$CKPT" "$g" "$name" "$sha" "$size" <<'EOF'
import json,sys,datetime
p,g,name,sha,size=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5])
d=json.load(open(p))
d.setdefault('parts',{}).setdefault(g,{})[name]={'sha256':sha,'size':size,'uploaded':True}
d['updated_at']=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
d['heartbeat']=d['updated_at']
json.dump(d,open(p,'w'),indent=1)
EOF
  rm -f "$part"   # transient transfer copy; source blends untouched on disk
  log "staging part removed: $name"
done

if [ "$fail" = "1" ]; then
  log "GROUP $g INCOMPLETE - will resume next run"
  exit 1
fi

# group complete: record tar hash for final re-download verify
python3 - "$CKPT" "$g" "$tarsha" "$tarsize" <<'EOF'
import json,sys,datetime
p,g,ts,tsz=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4])
d=json.load(open(p))
d.setdefault('group_tars',{})[g]={'sha256':ts,'size':tsz}
d.setdefault('groups_done',[]).append(g)
d['progress_seq']=len(d['groups_done'])  # supervisor.sh tracks this; groups_done alone made the lane look STUCK (false positive 2026-10-20 watchdog)
d['updated_at']=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
d['heartbeat']=d['updated_at']
json.dump(d,open(p,'w'),indent=1)
EOF
log "GROUP $g COMPLETE. tar_sha256=$tarsha"
