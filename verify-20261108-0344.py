#!/usr/bin/env python3
"""Verify lane-merged PR payloads: blob SHA of each PR file on branch head vs main tip."""
import json, subprocess, sys

PRS = [
    ("game-reverse-engineering", "6e7e072", "b741660", "87", [
        "teardown/dragon-ball-gt-transformation/INVENTORY.md",
        "teardown/dragon-ball-gt-transformation/SYSTEMS.md",
        "teardown/dragon-ball-gt-transformation/data/rom-header.json",
        "teardown/dragon-ball-gt-transformation/data/rom-layout.md",
        "teardown/dragon-ball-gt-transformation/data/runtime-strings.txt"]),
    ("game-reverse-engineering", "6e7e072", "73112da", "88", [
        "teardown/castle-crashers/INVENTORY.md",
        "teardown/castle-crashers/SYSTEMS.md",
        "teardown/castle-crashers/data/file-listing.txt"]),
    ("game-reverse-engineering", "6e7e072", "7907160", "89", [
        "teardown/tmnt-shredders-revenge/INVENTORY.md",
        "teardown/tmnt-shredders-revenge/SYSTEMS.md",
        "teardown/tmnt-shredders-revenge/data/arc-structure.txt"]),
    ("Mochiichao-Diamond-Version-2d-fresh-start", "415d15a", "0fad166", "384", [
        "src/lib/s14slice284.test.ts", "src/lib/s14slice284.ts"]),
    ("ConcreteDragon2", "8ae215f", "361b6fc", "8", [
        "data/customization/style_modifiers.json",
        "docs/CUSTOM-CHARACTER.md",
        "docs/VERTICAL-SLICE.md",
        "presentation/scripts/main.gd",
        "presentation/start_flow/fighter_tint.gd",
        "presentation/start_flow/fighter_tint.gd.uid",
        "presentation/start_flow/start_flow.gd",
        "presentation/start_flow/start_flow.gd.uid",
        "presentation/start_flow/start_flow.tscn",
        "project.godot",
        "sim/start_flow/custom_fighter.gd",
        "sim/start_flow/custom_fighter.gd.uid",
        "sim/start_flow/session.gd",
        "sim/start_flow/session.gd.uid",
        "tests/move_regression.gd.uid",
        "tests/screenshot_tour.gd.uid",
        "tests/step0_flow_test.gd",
        "tests/step0_flow_test.gd.uid",
        "tests/step0_screenshot_tour.gd",
        "tests/step0_screenshot_tour.gd.uid",
        "tools/validate_cd2_data.py"]),
]

def tree_map(repo, sha):
    out = subprocess.run(
        ["gh", "api", f"repos/mhvnsnt/{repo}/git/trees/{sha}?recursive=1",
         "--jq", ".tree[] | select(.type==\"blob\") | .path + \" \" + .sha"],
        capture_output=True, text=True)
    if out.returncode != 0:
        print(f"TREE-FAIL {repo} {sha}: {out.stderr.strip()[:200]}")
        sys.exit(1)
    m = {}
    for line in out.stdout.splitlines():
        p, s = line.rsplit(" ", 1)
        m[p] = s
    return m

total_ok = total_bad = 0
for repo, main_sha, head_sha, pr, files in PRS:
    main = tree_map(repo, main_sha)
    head = tree_map(repo, head_sha)
    ok = bad = 0
    for f in files:
        hb, mb = head.get(f), main.get(f)
        if hb and hb == mb:
            ok += 1
        else:
            bad += 1
            print(f"MISMATCH {repo}#{pr} {f}: head={hb} main={mb}")
    print(f"{repo}#{pr}: {ok}/{len(files)} blobs MATCH on main {main_sha}")
    total_ok += ok; total_bad += bad
print(f"TOTAL: {total_ok} match, {total_bad} mismatch")
