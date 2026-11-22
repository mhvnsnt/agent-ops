#!/usr/bin/env python3
"""VF5 model-library ingest driver (idempotent, resumable).

Downloads fighter/stage .farc archives from GitHub Release vf5-ps3-v1
(mhvnsnt/western-heart), verifies size + FArC integrity, organizes into
teardown/virtua-fighter-5/models/<code>/ and stages/<code>/ with a README
per entry, and commits incrementally on the current branch.

Safe to re-run: entries whose target dir already holds the .farc files are skipped.
"""
import os, re, shutil, struct, subprocess, sys, urllib.request

REPO = os.path.expanduser("~/workspace/western-heart-vf5")  # isolated sparse worktree on feat/vf5-model-library
BASE = "https://github.com/mhvnsnt/western-heart/releases/download/vf5-ps3-v1/"
VF5 = os.path.join(REPO, "teardown", "virtua-fighter-5")
DL = "/tmp/vf5dl"
LOG = "/tmp/vf5-ingest.log"

FIGHTERS = [
    # code, name, style, note, has_item
    ("aki", "Akira Yuki", "Bajiquan", "", True),
    ("akixx", "Akira Yuki (alt)", "—", "variant body (4.3MB uncompressed)", False),
    ("pai", "Pai Chan", "Ensei-Ken", "", True),
    ("lau", "Lau Chan", "Koen-Ken", "biggest item pack (114MB uncompressed)", True),
    ("wol", "Wolf Hawkfield", "Pro Wrestling", "HIGH priority", True),
    ("jef", "Jeffry McWild", "Pancratium", "", True),
    ("kag", "Kage-Maru", "Hagakure-ryu Jujutsu", "HIGH priority, most files", True),
    ("sar", "Sarah Bryant", "Martial Arts", "", True),
    ("jak", "Jacky Bryant", "Jeet Kune Do", "", True),
    ("shu", "Shun Di", "Drunken Kung Fu", "HIGH priority", True),
    ("lio", "Lion Rafale", "Praying Mantis Kung Fu", "HIGH priority", True),
    ("aoi", "Aoi Umenokouji", "Aiki-Jujutsu", "HIGH priority", True),
    ("lei", "Lei-Fei", "Shaolin Kung Fu", "", True),
    ("van", "Vanessa Lewis", "Vale Tudo", "HIGH priority", True),
    ("bra", "Brad Burns", "Kickboxing", "", True),
    ("goh", "Goh Hinogami", "Judo", "HIGH priority", True),
    ("mon", "Eileen", "Monkey Kung Fu (code `mon` = monkey)", "", True),
    ("msk", "El Blaze", "Lucha Libre (code `msk` = mask)", "HIGH priority", True),
    ("dur", "Dural (boss)", "—", "final boss, minimal item set", True),
]

# code -> (arena name or None, bgm or None, note)
STAGES = {
    "are": ("Arena (Akira)", "vf5b_are.adx", ""),
    "aur": (None, "vf5b_aur.adx", "on-screen name baked into stage-select UI textures (AET/PIC)"),
    "ban": (None, "vf5b_ban.adx", "on-screen name baked into stage-select UI textures (AET/PIC)"),
    "bar": ("Bar (Brad)", "vf5b_bar.adx", "confirmed by stage-select UI symbol `stage_icon_bar`"),
    "cas": (None, "vf5b_cas.adx", "on-screen name baked into stage-select UI textures (AET/PIC)"),
    "djo": ("Dojo", "vf5b_djo.adx", ""),
    "dur": ("Dural's stage", "vf5b_dur.adx", ""),
    "hai": (None, "vf5b_hai.adx", "on-screen name baked into stage-select UI textures (AET/PIC)"),
    "jin": ("Shinto Shrine (Kage)", "vf5b_jin.adx", "`jin` = jinja"),
    "nyc": ("New York City (Jacky)", "vf5b_nyc.adx", "confirmed by stage-select UI symbol `stage_icon_nyc`"),
    "riv": ("River (Shun)", "vf5b_riv.adx", ""),
    "sin": (None, "vf5b_sin.adx", "on-screen name baked into stage-select UI textures (AET/PIC)"),
    "slk": (None, "vf5b_slk.adx", "on-screen name baked into stage-select UI textures (AET/PIC)"),
    "tak": (None, "vf5b_tak.adx", "on-screen name baked into stage-select UI textures (AET/PIC)"),
    "tan": (None, "vf5b_tan.adx", "on-screen name baked into stage-select UI textures (AET/PIC)"),
    "ter": ("Terrace", "vf5b_ter.adx", ""),
    "umi": ("Sea (Jeffry)", "vf5b_umi.adx", "`umi` = sea in Japanese"),
    "yuk": ("Snow (Vanessa)", "vf5b_yuk.adx", "`yuki` = snow"),
    "tr2": ("Training stage variant", None, ""), "tr3": ("Training stage variant", None, ""),
    "tr4": ("Training stage variant", None, ""), "tr5": ("Training stage variant", None, ""),
    "tr6": ("Training stage variant", None, ""), "tr7": ("Training stage variant", None, ""),
    "tr8": ("Training stage variant", None, ""), "tr9": ("Training stage variant", None, ""),
    "trm": ("Training (menu?)", None, ""), "trn": ("Training", None, ""),
    "trs": ("Training stub", None, "tiny 4.5KB stub"),
    "ts2": ("Test stage", None, ""), "ts3": ("Test stage", None, ""),
    "tst": ("Test stage", None, ""),
    "du1": ("Dural-related stage", None, ""), "du2": ("Dural-related stage", None, ""),
    "du3": ("Dural-related stage", None, ""), "du4": ("Dural-related stage", None, ""),
    "cid": ("Stub", None, "16KB stub"), "wht": ("Stub", None, "4.5KB stub"),
}

def log(msg):
    print(msg, flush=True)
    with open(LOG, "a") as f:
        f.write(msg + "\n")

def sh(*args):
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        log(f"CMD FAILED: {' '.join(args)}\n{r.stderr[-2000:]}")
        raise SystemExit(1)
    return r.stdout.strip()

def count_farc(path):
    """Count entries the same way tools/farc_extract.py parses them."""
    with open(path, "rb") as f:
        data = f.read()
    assert data[:4] == b"FArC", f"Not a FArC file: {path}"
    pos, filesize, n = 12, len(data), 0
    while pos < filesize:
        if data[pos:pos+4] == b"\x00" * 4:
            break
        try:
            end = data.index(b"\x00", pos)
        except ValueError:
            break
        if end - pos > 256 or end - pos == 0:
            break
        try:
            name = data[pos:end].decode("ascii")
        except Exception:
            break
        if not all(32 <= ord(c) < 127 or c in "/_." for c in name):
            break
        pos = end + 1
        if pos + 12 > filesize:
            break
        offset, comp_size, uncomp_size = struct.unpack(">III", data[pos:pos+12])
        pos += 12
        if offset + comp_size > filesize:
            break
        n += 1
    return n

def fetch(fname):
    os.makedirs(DL, exist_ok=True)
    dst = os.path.join(DL, fname)
    if os.path.exists(dst):
        os.remove(dst)
    urllib.request.urlretrieve(BASE + fname, dst)
    return dst

def fmt_size(n):
    return f"{n/1048576:.1f}MB" if n >= 1048576 else f"{n/1024:.1f}KB" if n >= 1024 else f"{n}B"

def ingest_fighter(code, name, style, note, has_item):
    d = os.path.join(VF5, "models", code)
    files = [f"{code}.farc"] + ([f"{code}itm.farc"] if has_item else [])
    if all(os.path.exists(os.path.join(d, f)) for f in files) and os.path.exists(os.path.join(d, "README.md")):
        log(f"SKIP fighter {code} (already ingested)")
        return
    os.makedirs(d, exist_ok=True)
    rows = []
    for fname in files:
        p = fetch(fname)
        size = os.path.getsize(p)
        n = count_farc(p)
        assert n > 0, f"{fname}: no FArC entries parsed"
        kind = "base body" if not fname.endswith("itm.farc") else "customization items"
        rows.append((fname, size, n, kind))
        shutil.move(p, os.path.join(d, fname))
    lines = [
        f"# {name} — VF5 model archives", "",
        f"- **Code:** `{code}` · **Style:** {style}",
        "- **Source:** Virtua Fighter 5 PS3 (BLES00029), Ver.C",
        f"- **Release:** `vf5-ps3-v1` — {BASE}", "",
        "## Archives", "",
        "| File | Size | Inner files | Contents |",
        "|------|------|-------------|----------|",
    ]
    for fname, size, n, kind in rows:
        inner = ", ".join(f"`{fname[:-5]}_obj.bin` (model) + `{fname[:-5]}_tex.bin` (textures)"
                          if not fname.endswith("itm.farc") else "`*_obj.bin` (model data) + `*_tex.bin` (texture data)")
        lines.append(f"| `{fname}` | {fmt_size(size)} | {n} | {kind}: {inner} |")
    lines += ["", "## Extraction", "",
              "`../tools/farc_extract.py` — FArC magic + BE u32 entries + gzip payloads.",
              "Decompressed `*_obj.bin` → chrrox 3ds Max script; `*_tex.bin` → TXP.bms (QuickBMS).", ""]
    if note:
        lines += ["## Notes", "", note, ""]
    with open(os.path.join(d, "README.md"), "w") as f:
        f.write("\n".join(lines))
    sh("git", "add", os.path.join("teardown/virtua-fighter-5/models", code))
    sh("git", "commit", "-q", "-m", f"feat(vf5): add {name} ({code}) model archives")
    log(f"OK fighter {code}: {', '.join(f'{r[0]} {fmt_size(r[1])}/{r[2]} files' for r in rows)}")

def ingest_stage(code):
    d = os.path.join(VF5, "stages", code)
    fname = f"stg{code}.farc"
    if os.path.exists(os.path.join(d, fname)) and os.path.exists(os.path.join(d, "README.md")):
        log(f"SKIP stage {code} (already ingested)")
        return
    os.makedirs(d, exist_ok=True)
    aname, bgm, note = STAGES[code]
    p = fetch(fname)
    size = os.path.getsize(p)
    n = count_farc(p)
    assert n > 0, f"{fname}: no FArC entries parsed"
    shutil.move(p, os.path.join(d, fname))
    title = aname if aname else f"Stage `{code}`"
    lines = [f"# {title} — VF5 stage archive", "",
             f"- **Code:** `{code}`",
             f"- **BGM:** `{bgm}`" if bgm else "- **BGM:** — (stage↔BGM mapping confirmed from USRDIR/fcache.txt only for arenas)",
             "- **Source:** Virtua Fighter 5 PS3 (BLES00029)",
             f"- **Release:** `vf5-ps3-v1` — {BASE}", ""]
    if note:
        lines += [f"- **Note:** {note}", ""]
    lines += ["## Archive", "",
              "| File | Size | Inner files | Contents |",
              "|------|------|-------------|----------|",
              f"| `{fname}` | {fmt_size(size)} | {n} | `stg{code}_obj.bin` (geometry) + `stg{code}_tex.bin` (textures) |",
              "", "## Extraction", "",
              "`../tools/farc_extract.py` — same pipeline as characters.",
              "`*_obj.bin` → chrrox 3ds Max script; `*_tex.bin` → TXP.bms (QuickBMS).", ""]
    with open(os.path.join(d, "README.md"), "w") as f:
        f.write("\n".join(lines))
    sh("git", "add", os.path.join("teardown/virtua-fighter-5/stages", code))
    sh("git", "commit", "-q", "-m", f"feat(vf5): add stage {code} ({aname or 'unidentified'}) archive")
    log(f"OK stage {code}: {fname} {fmt_size(size)}/{n} files")

def main():
    only = sys.argv[1:]  # optional: "fighters" / "stages"
    if not only or "fighters" in only:
        for code, name, style, note, has_item in FIGHTERS:
            ingest_fighter(code, name, style, note, has_item)
    if not only or "stages" in only:
        for code in STAGES:
            ingest_stage(code)
    log("ALL DONE")

if __name__ == "__main__":
    main()
