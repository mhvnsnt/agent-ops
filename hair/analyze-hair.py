"""Hair analysis for AshLane fighters: detect hair triangles from texture color,
cluster into locks, define hair bone chains, compute skinning weights.

Writes /tmp/<NAME>_hairplan.json
"""
import json, sys
import numpy as np
from PIL import Image
from collections import defaultdict

NAME = sys.argv[1]  # ECHO or BRUTUS
PROFILE = sys.argv[2]  # green or black

ana = json.load(open(f'/tmp/{NAME}_analysis.json'))
pos = np.array(ana['positions'], dtype=np.float64).reshape(-1, 3)
uv = np.array(ana['uvs'], dtype=np.float64).reshape(-1, 2)
idx = np.array(ana['indices'], dtype=np.int64).reshape(-1, 3)
nodes = ana['nodes']
skin_joints = ana['skinJoints']
NJ = ana['skinJointCount']

# ---- bind-pose world matrices (quat math) ----
def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
                    w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
def qrot(q, v):
    w, x, y, z = q
    t = 2*np.cross([x, y, z], v)
    return v + w*t + np.cross([x, y, z], t)
def node_world(i):
    # returns (pos, quat) in model space
    T, R = np.zeros(3), np.array([1., 0., 0., 0.])
    chain = []
    while i != -1:
        chain.append(i); i = nodes[i]['parent']
    for i in reversed(chain):
        n = nodes[i]
        q = np.array(n['r'], dtype=np.float64)  # stored [x,y,z,w]? dump used three fmt
        # three.js quaternion order is [x,y,z,w]; dump wrote r as-is from glTF (glTF is [x,y,z,w])
        q = np.array([q[3], q[0], q[1], q[2]])  # -> [w,x,y,z]
        t = np.array(n['t'], dtype=np.float64)
        s = np.array(n['s'], dtype=np.float64)
        T = T + qrot(R, t * s)
        R = qmul(R, q)
    return T, R

head_idx = next(i for i, n in enumerate(nodes) if n['name'] == 'mixamorig:Head')
neck_idx = next(i for i, n in enumerate(nodes) if n['name'] == 'mixamorig:Neck')
head_pos, head_rot = node_world(head_idx)
neck_pos, _ = node_world(neck_idx)
head_joint = skin_joints.index(head_idx)  # joint index in skin
print(f'head world pos {head_pos.round(3)}, head joint {head_joint}, verts {len(pos)}')

# ---- per-vertex color ----
# three.js GLTFLoader sets flipY=false, so uv=(u,v) samples the image directly
# with v=0 at the top row (matching PIL's layout).
img = Image.open(f'/tmp/{NAME}_basecolor.webp').convert('RGB')
ia = np.asarray(img).astype(np.float64) / 255.0
H, W, _ = ia.shape
px = np.clip((uv[:, 0]*W).astype(int), 0, W-1)
py = np.clip((uv[:, 1]*H).astype(int), 0, H-1)
col = ia[py, px]
r, g, b = col[:, 0], col[:, 1], col[:, 2]

if PROFILE == 'green':
    vmask = (g > 0.32) & (g > r*1.7) & (g > b*1.15)
else:
    vmask = (r < 0.16) & (g < 0.16) & (b < 0.17)
print(f'vertex hair-color mask: {vmask.sum()} / {len(pos)} ({vmask.mean()*100:.1f}%)')

# ---- triangle mask + hair region detection ----
def tri_centroid_color(ti):
    return col[idx[ti]].mean(axis=0)

def sample_uv(uvs):
    px = np.clip((uvs[:, 0]*W).astype(int), 0, W-1)
    py = np.clip((uvs[:, 1]*H).astype(int), 0, H-1)
    return ia[py, px]

def is_loose_green(c):
    r, g, b = c[:, 0], c[:, 1], c[:, 2]
    return (g > 0.20) & (g > r*1.4) & (g > b*1.05)

# Blur the image to mimic GPU mipmapping: per-texel sampling misses green that
# the renderer sees via filtered/mipped fetches. Blur spreads strand color.
from PIL import ImageFilter
img_blur = img.filter(ImageFilter.GaussianBlur(radius=4))
ia_blur = np.asarray(img_blur).astype(np.float64) / 255.0
def sample_uv_blur(uvs):
    px = np.clip((uvs[:, 0]*W).astype(int), 0, W-1)
    py = np.clip((uvs[:, 1]*H).astype(int), 0, H-1)
    return ia_blur[py, px]

def is_green_blur(c):
    r, g, b = c[:, 0], c[:, 1], c[:, 2]
    return (g > 0.13) & (g > r*1.18) & (g > b*0.85)

if PROFILE == 'green':
    # green is hair-only in this texture. Moderate threshold + head-proximity filter.
    # (Re-skinning is safe against misses: missed verts just stay Head-rigid.)
    tri_mask = vmask[idx].sum(axis=1) >= 2
    htris = np.where(tri_mask)[0]
    vert_tris = defaultdict(list)
    for ti in htris:
        for v in idx[ti]: vert_tris[v].append(ti)
    seen = np.zeros(len(idx), dtype=bool)
    comps = []
    for ti in htris:
        if seen[ti]: continue
        stack = [ti]; seen[ti] = True; comp = []
        while stack:
            t = stack.pop(); comp.append(t)
            for v in idx[t]:
                for nt in vert_tris[v]:
                    if not seen[nt]:
                        seen[nt] = True; stack.append(nt)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    print(f'components: {len(comps)}, sizes: {[len(c) for c in comps[:10]]}')
    # loose threshold needs spatial filtering: keep components touching the head
    kept = []
    for c in comps:
        if len(c) < 15: continue
        vs = np.unique(idx[c])
        d = np.linalg.norm(pos[vs] - head_pos, axis=1)
        cdist = np.linalg.norm(pos[vs].mean(axis=0) - head_pos)
        if (d < 0.22).mean() > 0.03 or cdist < 0.42:
            kept.append(c)
    print(f'kept {len(kept)} components (head-proximity filtered)')
    hair_set = set(t for c in kept for t in c)
    # hole filling: absorb non-hair tris fully surrounded by hair (edge-adjacency)
    edge_map = defaultdict(list)
    for ti in range(len(idx)):
        a, b, c = idx[ti]
        for e in [tuple(sorted((a,b))), tuple(sorted((b,c))), tuple(sorted((c,a)))]:
            edge_map[e].append(ti)
    tri_nbrs = defaultdict(set)
    for e, ts in edge_map.items():
        for t1 in ts:
            for t2 in ts:
                if t1 != t2: tri_nbrs[t1].add(t2)
    for _ in range(4):
        grown = set()
        for ti in range(len(idx)):
            if ti in hair_set: continue
            nbrs = tri_nbrs.get(ti)
            if nbrs and all(n in hair_set for n in nbrs):
                grown.add(ti)
        if not grown: break
        hair_set |= grown
    hair_tris = sorted(hair_set)
    print(f'after hole-fill: {len(hair_tris)} tris')
else:
    # black profile: flood fill from scalp-touching dark tris (captures nape + beard)
    strict = vmask[idx].all(axis=1)
    region = ((pos[idx].mean(axis=1)[:, 0] > -0.25) & (pos[idx].mean(axis=1)[:, 0] < 0.18) &
              (pos[idx].mean(axis=1)[:, 1] > 0.42) & (pos[idx].mean(axis=1)[:, 1] < 1.0) &
              (np.abs(pos[idx].mean(axis=1)[:, 2]) < 0.22))
    seed = strict & region & (np.linalg.norm(pos[idx].mean(axis=1) - head_pos, axis=1) < 0.24)
    # beard seeds: dark tris near jaw
    cen = pos[idx].mean(axis=1)
    beard_seed = (strict & (cen[:, 0] > -0.02) & (cen[:, 0] < 0.20) &
                  (cen[:, 1] > 0.42) & (cen[:, 1] < 0.70) & (np.abs(cen[:, 2]) < 0.14))
    growable = region & (col[idx].max(axis=2).max(axis=1) < 0.34)
    # adjacency
    tri_adj = defaultdict(set)
    vert_tris = defaultdict(list)
    cand = np.where(growable)[0]
    candset = set(cand.tolist())
    for ti in cand:
        for v in idx[ti]: vert_tris[v].append(ti)
    for ti in cand:
        for v in idx[ti]:
            for nt in vert_tris[v]:
                if nt != ti and nt in candset: tri_adj[ti].add(nt)
    seen = set(); stack = [t for t in np.where(seed | beard_seed)[0] if t in candset]
    print(f'seed tris: {len(stack)}')
    while stack:
        t = stack.pop()
        if t in seen: continue
        seen.add(t)
        for nt in tri_adj[t]:
            if nt not in seen: stack.append(nt)
    hair_tris = sorted(seen)
print(f'KEPT hair tris: {len(hair_tris)}')
if not hair_tris:
    print('NO HAIR FOUND — abort'); sys.exit(1)

# ---- lock clustering: angular sectors around head Y axis ----
# model faces +X (cast convention); angle measured from +X axis
hverts = np.unique(idx[hair_tris])
hv = pos[hverts]
if PROFILE == 'green':
    ang = np.arctan2(hv[:, 0]-head_pos[0], hv[:, 2]-head_pos[2])  # legacy, hair all around
else:
    ang = np.arctan2(hv[:, 2]-head_pos[2], hv[:, 0]-head_pos[0])  # 0=fwd(+X), pi=back
NB = 8
bins = np.floor((ang + np.pi) / (2*np.pi) * NB).astype(int) % NB
lock_of_vert = {}
locks = []
GAP = 0.07  # height gap that splits one sector into separate locks (e.g. beard vs scalp)
for s in range(NB):
    m = bins == s
    if m.sum() < 0.015 * len(hverts): continue
    sv = hverts[m]
    sy = pos[sv][:, 1]
    order = np.argsort(-sy)  # tallest first
    pieces, cur = [], [order[0]]
    for k in order[1:]:
        if sy[cur[-1]] - sy[k] > GAP:
            pieces.append(cur); cur = [k]
        else:
            cur.append(k)
    pieces.append(cur)
    # gaps between consecutive pieces (height order)
    gaps = []
    for a, b in zip(pieces[:-1], pieces[1:]):
        gaps.append(sy[a[-1]] - sy[b[0]])
    # merge a small piece into its taller neighbor only if the gap is small;
    # a large gap means genuinely separate (e.g. beard vs scalp) -> keep
    MINV, MAXGAP = 25, 0.10
    final = []
    i = 0
    while i < len(pieces):
        p = pieces[i]
        if len(p) < MINV and i + 1 < len(pieces) and gaps[i] < MAXGAP:
            pieces[i+1] = p + pieces[i+1]  # merge down into next (taller? no, lower) piece
            i += 1
            continue
        if len(p) < MINV and final and (sy[final[-1][-1]] - sy[p[0]]) < MAXGAP:
            final[-1].extend(p)
            i += 1
            continue
        final.append(p); i += 1
    pieces = [p for p in final if len(p) >= 12]
    for piece in pieces:
        pv = sv[np.array(piece)]
        lv = pos[pv]; ys = lv[:, 1]
        root = lv[ys >= np.quantile(ys, 0.80)].mean(axis=0)
        tip = lv[ys <= np.quantile(ys, 0.20)].mean(axis=0)
        d = tip - root; L = np.linalg.norm(d)
        if L < 0.05: d = np.array([0., -1., 0.]); L = 0.08
        d = d / np.linalg.norm(d)
        jw = [root + d*(L/3)*k for k in range(3)]
        locks.append({'sector': s, 'verts': pv, 'root': root, 'tip': tip,
                      'dir': d, 'len': L, 'joints': jw})
        for v in pv: lock_of_vert[v] = len(locks)-1
print(f'locks: {len(locks)}')
for i, L in enumerate(locks):
    print(f'  lock {i}: sector {L["sector"]} verts {len(L["verts"])} len {L["len"]:.3f} root {L["root"].round(3)}')

# ---- per-vertex weights ----
def sstep(x):
    x = min(max(x, 0.0), 1.0); return x*x*(3-2*x)
# orphans (verts in hair tris but dropped from locks): nearest lock by root
roots = np.array([Lk['root'] for Lk in locks])
for v in hverts:
    if v not in lock_of_vert:
        d = np.linalg.norm(roots - pos[v], axis=1)
        lock_of_vert[v] = int(np.argmin(d))
vert_w = {}
for v in hverts:
    li = lock_of_vert[v]
    Lk = locks[li]
    t = float(np.dot(pos[v]-Lk['root'], Lk['dir']) / Lk['len'])
    t = min(max(t, 0.0), 1.0)
    if t < 0.30:
        vert_w[v] = [[head_joint, 1.0]]
    else:
        u = (t-0.30)/0.70*3.0
        i = min(int(u), 2); f = sstep(u-i)
        # chain: B0=head_joint, B1..B3 = lock bones
        chain = [head_joint] + [NJ + li*3 + k for k in range(3)]
        w0, w1 = 1-f, f
        pair = [[chain[i], w0], [chain[i+1], w1]]
        # renormalize (drop zeros)
        pair = [[jj, ww] for jj, ww in pair if ww > 1e-4]
        s = sum(w for _, w in pair); pair = [[jj, w/s] for jj, w in pair]
        vert_w[v] = pair

plan = {
    'name': NAME,
    'head_node': int(head_idx),
    'head_joint': int(head_joint),
    'joint_count': int(NJ),
    'locks': [{'name': f'L{k+1}', 'joints': [[float(x) for x in j] for j in Lk['joints']]} for k, Lk in enumerate(locks)],
    'hair_tris': [int(t) for t in hair_tris],
    'vert_weights': {str(int(v)): [[int(jj), float(ww)] for jj, ww in w] for v, w in vert_w.items()},
}
json.dump(plan, open(f'/tmp/{NAME}_hairplan.json', 'w'))
print(f'wrote /tmp/{NAME}_hairplan.json: {len(locks)} locks, {len(vert_w)} weighted verts')
