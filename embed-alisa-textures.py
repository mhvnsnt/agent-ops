#!/usr/bin/env python3
"""Embed external PNG textures into alisa.glb (cyborg-x) as baseColorTexture.
Material names map to ~/workspace/pull-rest/textures/*_Diff.png files."""
import os, re, struct, json, sys

SRC = "/home/hatch/workspace/pull-rest/glb/alisa.glb"
TEXDIR = "/home/hatch/workspace/pull-rest/textures"
OUT = "/tmp/cyborg-x-textured.glb"

from pygltflib import GLTF2, BufferView, Image, Texture

gltf = GLTF2().load(SRC)

# index texture files by normalized key
texfiles = {}
for fn in os.listdir(TEXDIR):
    if not fn.lower().endswith(".png"):
        continue
    key = re.sub(r"(_diff|_d|_c)$", "", fn[:-4], flags=re.I).lower()
    texfiles.setdefault(key, fn)

def mat_candidates(name):
    k = name.lower()
    k = re.sub(r"\.001$", "", k)          # Blender duplicate suffix
    cands = [k]
    s = re.sub(r"^[ta]", "", k)           # transparent/alpha variant prefix
    if s != k:
        cands.append(s)
    return cands

# explicit overrides: material key -> texture key (lowercased stem)
OVERRIDES = {
    "alisa": "face",       # head
    "boots": "pantsboots",
    "eyeball_l": "eyeball",
    "eyeball_r": "eyeball",
}

# work on the binary blob
with open(SRC, "rb") as f:
    raw = f.read()
json_len = struct.unpack("<I", raw[12:16])[0]
bin_off = 20 + json_len
bin_len = struct.unpack("<I", raw[bin_off:bin_off+4])[0]
blob = bytearray(raw[bin_off+8:bin_off+8+bin_len])

embedded = {}
mapped, unmapped = [], []
for m in gltf.materials:
    keys = mat_candidates(m.name or "")
    tkey = OVERRIDES.get(keys[0], keys[0])
    fn = None
    # try override/full key first, then t/a-stripped variant
    for base in ([tkey] + keys[1:]):
        for cand in (base, base + "s", base.rstrip("s")):
            if cand in texfiles:
                fn = texfiles[cand]
                break
        if fn:
            break
    if fn is None:
        # substring fallback: texture key contained in material key or vice versa
        for base in ([tkey] + keys[1:]):
            for tk, tfn in texfiles.items():
                if tk in base or base in tk:
                    fn = tfn
                    break
            if fn:
                break
    if fn is None:
        unmapped.append(m.name)
        continue
    if fn not in embedded:
        with open(os.path.join(TEXDIR, fn), "rb") as f:
            png = f.read()
        bv_index = len(gltf.bufferViews)
        gltf.bufferViews.append(BufferView(buffer=0, byteOffset=len(blob),
                                           byteLength=len(png), name=fn))
        blob.extend(png)
        # pad to 4-byte alignment
        while len(blob) % 4:
            blob.append(0)
        img_index = len(gltf.images)
        gltf.images.append(Image(bufferView=bv_index, mimeType="image/png", name=fn))
        tex_index = len(gltf.textures)
        gltf.textures.append(Texture(source=img_index, name=fn))
        embedded[fn] = tex_index
    else:
        tex_index = embedded[fn]
    pbr = m.pbrMetallicRoughness
    if pbr.baseColorTexture is None:
        from pygltflib import TextureInfo
        pbr.baseColorTexture = TextureInfo(index=tex_index)
    else:
        pbr.baseColorTexture.index = tex_index
    pbr.baseColorFactor = [1.0, 1.0, 1.0, 1.0]
    pbr.metallicFactor = 0.0
    pbr.roughnessFactor = 0.9
    mapped.append((m.name, fn))

gltf.buffers[0].byteLength = len(blob)
gltf.set_binary_blob(bytes(blob))
gltf.save(OUT)

print(f"mapped {len(mapped)} materials, unmapped {len(unmapped)}")
for name, fn in mapped:
    print(f"  {name} -> {fn}")
print("UNMAPPED:", unmapped)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
