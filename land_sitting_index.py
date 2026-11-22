#!/usr/bin/env python3
"""Land the sitting-saga index + build scripts on cape-jones main via Git Data API.
Base tree = main's CURRENT tree. Adds new paths only, plus an append-only
edit to docs/ASSET-INVENTORY.md. No deletions possible by construction."""
import base64, glob, json, os, subprocess, sys

REPO = "mhvnsnt/cape-jones"
BRANCH = "docs/sitting-saga-index-20261023"
WS = os.path.expanduser("~/workspace")

def gh(args, inp=None, raw=False):
    cmd = ["gh", "api"] + args
    r = subprocess.run(cmd, input=inp, capture_output=True, text=False)
    if r.returncode != 0:
        sys.exit(f"FAIL {' '.join(args)}: {r.stderr.decode()[:400]}")
    out = r.stdout
    return out if raw else json.loads(out.decode())

def blob(data: bytes) -> str:
    body = json.dumps({"content": base64.b64encode(data).decode(), "encoding": "base64"}).encode()
    return gh([f"repos/{REPO}/git/blobs", "--method", "POST", "--input", "-"], inp=body)["sha"]

# 1. main head + tree
ref = gh([f"repos/{REPO}/git/ref/heads/main"])
head_sha = ref["object"]["sha"]
head_commit = gh([f"repos/{REPO}/git/commits/{head_sha}"])
base_tree = head_commit["tree"]["sha"]
print("main head:", head_sha, "tree:", base_tree)

entries = []
def add(path, data: bytes):
    entries.append({"path": path, "mode": "100644", "type": "blob", "sha": blob(data)})
    print("blob:", path, len(data))

# 2. index doc
with open(f"{WS}/agent-ops/SITTING-SAGA-2026-10-23.md", "rb") as f:
    add("docs/SITTING-SAGA-2026-10-23.md", f.read())

# 3. append-only edit to ASSET-INVENTORY.md
inv = gh([f"repos/{REPO}/contents/docs/ASSET-INVENTORY.md", "-H", "Accept: application/vnd.github.raw"], raw=True)
appendix = ("""
## 7. Sitting saga scenes (2026-10-23) - HAVE (on Releases)

The finished chair work. Scene files are too big for the git tree, so they
live on this repo's Releases. Full index: `docs/SITTING-SAGA-2026-10-23.md`.

| Scene | Release | Size |
|---|---|---|
| `scene_anim_placed3.blend` (canon placed) | `sitcanon-anim-placed-20261020` | 172,551,169 B |
| `scene_recliner_mech.blend` | `recliner-mech-20261023` | 164,790,998 B |
| `scene_capebaked.blend` | `cape-bake-20261023` | 828,433,505 B |
| `scene_final.blend` (FINAL) | `sitting-final-20261023` | 832,635,494 B |

Build scripts: `production/sitting-saga-20261023/scripts/`.
""").encode("utf-8")
add("docs/ASSET-INVENTORY.md", inv.rstrip(b"\n") + b"\n" + appendix)

# 4. scripts
SCR = "production/sitting-saga-20261023/scripts"
readme = ("# Sitting saga build scripts (2026-10-23)\n\n"
          "The exact scripts that built the recliner mechanism, the cape cloth bake,\n"
          "and the final merged sitting scene. They ran locally in\n"
          "`~/workspace/sitcanon-work/` (sitcanon/) and `~/workspace/capebake-work/`\n"
          "(capebake/) plus cape physics probes from the workspace root (root-probes/).\n"
          "Landed 2026-10-23 so the sitting work is reproducible from this repo alone.\n"
          "Deliverables indexed in `docs/SITTING-SAGA-2026-10-23.md`.\n").encode()
add(f"{SCR}/README.md", readme)

def add_glob(pattern, dest_prefix):
    for p in sorted(glob.glob(pattern)):
        with open(p, "rb") as f:
            add(f"{SCR}/{dest_prefix}/{os.path.basename(p)}", f.read())

add_glob(f"{WS}/sitcanon-work/*.py", "sitcanon")
add_glob(f"{WS}/sitcanon-work/mech-scratch/*.py", "sitcanon/mech-scratch")
add_glob(f"{WS}/capebake-work/*.py", "capebake")
for sub in ["full_kernel", "probe_kernel", "render_kernel", "krender", "kout", "kout2"]:
    add_glob(f"{WS}/capebake-work/{sub}/*.py", f"capebake/{sub}")
add_glob(f"{WS}/phys-cape*.py", "root-probes")

# 5. tree + commit + branch
tree = gh([f"repos/{REPO}/git/trees", "--method", "POST", "--input", "-"],
          inp=json.dumps({"base_tree": base_tree, "tree": entries}).encode())
print("new tree:", tree["sha"])
commit = gh([f"repos/{REPO}/git/commits", "--method", "POST", "--input", "-"],
            inp=json.dumps({
                "message": "docs: sitting saga index + build scripts (owner asked where the chair work lives)",
                "tree": tree["sha"], "parents": [head_sha]}).encode())
print("commit:", commit["sha"])
gh([f"repos/{REPO}/git/refs", "--method", "POST", "--input", "-"],
   inp=json.dumps({"ref": f"refs/heads/{BRANCH}", "sha": commit["sha"]}).encode())
print("branch created:", BRANCH, "files:", len(entries))
