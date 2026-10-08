import json, subprocess, time
repos = {
 "RealCUGAN-official": "bilibili/ailab",
 "RealCUGAN-fork": "ZHCSOFT/Real-CUGAN",
 "Paint3D": "OpenTexture/Paint3D",
 "TEXTure": "TEXTurePaper/TEXTurePaper",
 "SyncMVD": "LIU-Yuxin/SyncMVD",
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
print(json.dumps(out, indent=1))
