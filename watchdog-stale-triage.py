import json, os
names = ["accessory-pull.json","ai-teardown.json","bout-render-fix.json",
"cn-gigaleak-archiveorg-pull.json","concrete-dragon-rename.json",
"creation-suite-v3.json","dialogue.json","disk-cleanup-sweep-20261021.json",
"disk-cleanup-sweep-pass2-20261021.json","docfrank-ladder-reorder-20261021.json",
"godmodeos-build.json","mini-house49-wireup-20261021.json",
"mini-retemplate-20261021.json","mocap-lab-wiring.json","money-takeover.json",
"pro-study-files-locations-20261029.json","step2-defects.json",
"storeoff-relaunch8-20261021.json","storeoff-relaunch9-20261021.json",
"street-brawl-cicd.json","street-brawl.json","t6ps3-upload-state.json",
"teardown-coord-relaunch4-20261021.json","ur-feel.json","zen-render-batch2-note.json"]
d = "/home/hatch/workspace/agent-ops/checkpoints"
for n in names:
    try:
        j = json.load(open(os.path.join(d, n)))
    except Exception as e:
        print(n, "UNREADABLE", e); continue
    notes = j.get("notes")
    if isinstance(notes, list):
        notes = notes[-1] if notes else ""
    print("=" * 70)
    print(n, "| status:", j.get("status"), "| watchdog:", j.get("watchdog"),
          "| updated_at:", j.get("updated_at"), "| last_heartbeat:", j.get("last_heartbeat"))
    print("  task:", str(j.get("task") or j.get("goal") or j.get("resume_prompt") or "")[:200])
    print("  repo:", j.get("repo"), "| branch:", j.get("branch"),
          "| attempts:", j.get("attempts"), "| progress_seq:", j.get("progress_seq"))
    print("  notes tail:", str(notes)[:300])
