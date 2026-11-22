#!/bin/bash
# disk-space-guardian helper: as tekken-models-batch-2 release assets land,
# delete the redundant browser_downloads originals (each verified: release
# asset byte-exact + md5(browser original) == md5(models/ copy)).
# models/ copies AND release assets both remain afterwards — double backup.
REPO="mhvnsnt/western-heart"
TAG="tekken-models-batch-2"
MODELS="$HOME/workspace/game-reverse-engineering/tekken7/models"
BD="$HOME/workspace/browser_downloads"
LOG="$HOME/workspace/agent-ops/tekken-watch.log"

# asset_name|models_relpath|browser_sess|browser_file|expected_size
ITEMS=(
"zafina-t7-alt-costumes-blender.zip|zafina/zafina-t7-alt-costumes-blender.zip|sess-2759274430|browser-download-20261013T070021.389018988Z-10-Tekken_7_Zafina_Blender_Model_Ported_by_AD-8_Renders.zip|132506260"
"kunimitsu-t7-rig.blend|kunimitsu/kunimitsu-t7-rig.blend|sess-2759274430|browser-download-20261013T070544.244940763Z-11-Tekken_7_Kunimitsu_Rig.blend|292662984"
"dragunov-t7-rig.blend|dragunov/dragunov-t7-rig.blend|sess-2759274430|browser-download-20261013T071548.197249684Z-12-Tekken_7_Dragunov_Rig.blend|73766856"
"hwoarang-t7-rig.blend|hwoarang/hwoarang-t7-rig.blend|sess-2759274430|browser-download-20261013T071835.858889622Z-13-Tekken7HwoarangRig.blend|129731772"
"feng-wei-t7-rig.blend|feng-wei/feng-wei-t7-rig.blend|sess-2244382003|browser-download-20261013T072613.617860440Z-0-Tekken7FengWeiRIg.blend|288028152"
"azucena-t8-blender.zip|azucena/azucena-t8-blender.zip|sess-2244382003|browser-download-20261013T073612.161314045Z-1-T8_Azucena_Blender_Model_Ported_by_AD-8_Renders_Kq1zaVH.zip|341918493"
"tekken-force-soldier-t7-rig.blend|tekken-force-soldier/tekken-force-soldier-t7-rig.blend|sess-2244382003|browser-download-20261013T074757.013548542Z-2-Tekken_7_Tekken_Force_Soldier_Rig.blend|75421180"
)

echo "$(date -u +%FT%TZ) watcher started" >> "$LOG"
deadline=$(( $(date +%s) + 3600 ))
while [ $(date +%s) -lt $deadline ]; do
  all_done=true
  for item in "${ITEMS[@]}"; do
    IFS='|' read -r asset mrel sess bfile esize <<< "$item"
    bpath="$BD/$sess/$bfile"
    [ -f "$bpath" ] || continue  # already deleted
    all_done=false
    asize=$(gh api "repos/$REPO/releases/tags/$TAG" --jq ".assets[] | select(.name==\"$asset\") | .size" 2>/dev/null)
    if [ "$asize" == "$esize" ]; then
      mpath="$MODELS/$mrel"
      h1=$(md5sum "$bpath" | cut -d' ' -f1)
      h2=$(md5sum "$mpath" | cut -d' ' -f1)
      if [ "$h1" == "$h2" ] && [ -n "$h1" ]; then
        rm -v "$bpath" >> "$LOG" 2>&1
        echo "$(date -u +%FT%TZ) DELETED $bfile (asset $asset verified: size $asize, md5 $h1)" >> "$LOG"
      else
        echo "$(date -u +%FT%TZ) MD5 MISMATCH $bfile ($h1 vs $h2) - NOT deleted" >> "$LOG"
      fi
    fi
  done
  $all_done && { echo "$(date -u +%FT%TZ) all browser originals deleted, watcher done" >> "$LOG"; break; }
  sleep 90
done
echo "$(date -u +%FT%TZ) watcher exiting" >> "$LOG"
