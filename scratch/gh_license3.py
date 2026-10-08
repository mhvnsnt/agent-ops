import json, subprocess, time
repos = {
 "MaterialGAN": "tflsguoyu/materialgan",
 "TileGen": "jackzhousz/tilegen",
 "PyMeshFix": "pyvista/pymeshfix",
 "OptCuts": "liminchen/OptCuts",
 "BFF": "GeometryCollective/boundary-first-flattening",
 "MeshFix-core": "MarcoAttene/MeshFix-V2.1",
}
out = {}
for name, rr in repos.items():
    url = f"https://api.github.com/repos/{rr}/license"
    try:
        r = subprocess.run(["curl","-s","--max-time","20","-H","Accept: application/vnd.github+json",
                            "-H","User-Agent","forge3d-catalog-research",url],
                           capture_output=True, text=True, timeout=30)
        d = json.loads(r.stdout)
        lic = d.get("license") or {}
        out[name] = {"repo": rr, "spdx": lic.get("spdx_id"), "name_field": lic.get("name"),
                     "url": d.get("html_url"), "err": d.get("message")}
    except Exception as e:
        out[name] = {"repo": rr, "error": str(e)}
    time.sleep(0.4)
# PyPI fast-simplification
try:
    r = subprocess.run(["curl","-s","--max-time","20","https://pypi.org/pypi/fast-simplification/json"],
                       capture_output=True, text=True, timeout=30)
    d = json.loads(r.stdout)
    info = d.get("info", {})
    out["fast-simplification-pypi"] = {"license": info.get("license"), "version": info.get("version"),
        "home": info.get("home_page"), "classifiers": [c for c in info.get("classifiers",[]) if "License" in c]}
except Exception as e:
    out["fast-simplification-pypi"] = {"error": str(e)}
# bilibili/ailab Real-CUGAN subdir listing for LICENSE
try:
    r = subprocess.run(["curl","-s","--max-time","20","-H","User-Agent","forge3d-catalog-research",
                        "https://api.github.com/repos/bilibili/ailab/contents/Real-CUGAN"],
                       capture_output=True, text=True, timeout=30)
    d = json.loads(r.stdout)
    names = [x["name"] for x in d] if isinstance(d, list) else d
    out["bilibili-ailab-RealCUGAN-dir"] = {"files": names}
except Exception as e:
    out["bilibili-ailab-RealCUGAN-dir"] = {"error": str(e)}
print(json.dumps(out, indent=1))
