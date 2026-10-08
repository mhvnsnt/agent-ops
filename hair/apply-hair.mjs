/** Apply hair plan to a GLB: adds hair bone nodes, extends the skin, and appends
 *  a hair-shell primitive (original hair triangles offset +2mm along normals,
 *  skinned to the new hair bones with Head-anchored roots).
 *  Binary-append-only surgery: original bufferViews/accessors untouched.
 */
import { readFileSync, writeFileSync } from "node:fs";
import * as THREE from "/home/hatch/workspace/game-sweep/AshLanev2/node_modules/three/build/three.module.js";
import { MeshoptDecoder } from "/home/hatch/workspace/game-sweep/AshLanev2/node_modules/three/examples/jsm/libs/meshopt_decoder.module.js";

const [,, inPath, planPath, outPath] = process.argv;
const EPS = 0.002; // hair shell offset (2mm) above body surface

function readGLB(path) {
  const data = readFileSync(path);
  let off = 12, json = null, bin = null;
  while (off < data.length) {
    const clen = data.readUInt32LE(off), ctype = data.readUInt32LE(off + 4);
    if (ctype === 0x4e4f534a) json = JSON.parse(data.subarray(off + 8, off + 8 + clen).toString("utf8"));
    else if (ctype === 0x004e4942) bin = Buffer.from(data.subarray(off + 8, off + 8 + clen));
    off += 8 + clen;
  }
  return { json, bin };
}

async function decodeBV(json, bin, bvIndex) {
  const bv = json.bufferViews[bvIndex];
  const ext = bv.extensions?.["EXT_meshopt_compression"];
  if (ext) {
    await MeshoptDecoder.ready;
    const src = bin.subarray(ext.byteOffset, ext.byteOffset + ext.byteLength);
    const target = Buffer.alloc(ext.count * ext.byteStride);
    MeshoptDecoder.decodeGltfBuffer(target, ext.count, ext.byteStride, src, ext.mode, ext.filter);
    return target;
  }
  const off = bv.byteOffset || 0;
  return bin.subarray(off, off + bv.byteLength);
}

const { json, bin } = readGLB(inPath);
const plan = JSON.parse(readFileSync(planPath, "utf8"));
const prim = json.meshes[0].primitives[0];
const A = (n) => json.accessors[prim.attributes[n]];

const posBuf = await decodeBV(json, bin, A("POSITION").bufferView);
const nrmBuf = await decodeBV(json, bin, A("NORMAL").bufferView);
const uvBuf = await decodeBV(json, bin, A("TEXCOORD_0").bufferView);
const idxBuf = await decodeBV(json, bin, json.accessors[prim.indices].bufferView);
const vCount = A("POSITION").count;
const positions = new Float32Array(posBuf.buffer, posBuf.byteOffset, vCount * 3);
const normals = new Int16Array(nrmBuf.buffer, nrmBuf.byteOffset, vCount * 3);
const uvs = new Uint16Array(uvBuf.buffer, uvBuf.byteOffset, vCount * 2);
const indices = new Uint16Array(idxBuf.buffer, idxBuf.byteOffset, json.accessors[prim.indices].count);
// old inverse bind matrices
const skin = json.skins[0];
const ibmAcc = json.accessors[skin.inverseBindMatrices];
const ibmBuf = await decodeBV(json, bin, ibmAcc.bufferView);
const oldIBM = new Float32Array(ibmBuf.buffer, ibmBuf.byteOffset, ibmAcc.count * 16);

// ---- bind-pose world matrices ----
const nodes = json.nodes;
const parent = new Array(nodes.length).fill(-1);
nodes.forEach((n, i) => (n.children || []).forEach((c) => (parent[c] = i)));
const worldMats = [];
{
  const local = (i) => {
    const n = nodes[i];
    const m = new THREE.Matrix4().compose(
      new THREE.Vector3(...(n.translation || [0, 0, 0])),
      new THREE.Quaternion(...(n.rotation || [0, 0, 0, 1])),
      new THREE.Vector3(...(n.scale || [1, 1, 1])));
    return m;
  };
  const wm = (i) => {
    if (worldMats[i]) return worldMats[i];
    const l = local(i);
    worldMats[i] = parent[i] === -1 ? l : wm(parent[i]).clone().multiply(l);
    return worldMats[i];
  };
  nodes.forEach((_, i) => wm(i));
}
const headWorld = worldMats[plan.head_node];
const headWorldInv = headWorld.clone().invert();

// ---- create hair bone nodes ----
const newNodeIdx = [];
const boneBindWorld = []; // ACTUAL bind world matrices (inherit parent rotation)
plan.locks.forEach((lock, li) => {
  let parentIdx = plan.head_node;
  let parentWorld = headWorld;
  lock.joints.forEach((jw, k) => {
    const w = new THREE.Vector3(jw[0], jw[1], jw[2]);
    const assumedWorld = new THREE.Matrix4().makeTranslation(w.x, w.y, w.z);
    const local = parentWorld.clone().invert().multiply(assumedWorld);
    const lt = new THREE.Vector3().setFromMatrixPosition(local);
    const node = { name: `hair_${lock.name}_${k + 1}`, translation: [lt.x, lt.y, lt.z] };
    const ni = nodes.length;
    nodes.push(node);
    if (!nodes[parentIdx].children) nodes[parentIdx].children = [];
    nodes[parentIdx].children.push(ni);
    newNodeIdx.push(ni);
    const bindW = parentWorld.clone().multiply(new THREE.Matrix4().makeTranslation(lt.x, lt.y, lt.z));
    boneBindWorld.push(bindW);
    parentIdx = ni; parentWorld = bindW;
  });
});
console.log(`added ${newNodeIdx.length} hair bones`);

// ---- extend skin ----
const extJoints = [...skin.joints, ...newNodeIdx];
const nOld = skin.joints.length;
const nNew = newNodeIdx.length;
const newIBM = new Float32Array((nOld + nNew) * 16);
newIBM.set(oldIBM);
boneBindWorld.forEach((bw, k) => {
  newIBM.set(bw.clone().invert().toArray(), (nOld + k) * 16);
});

// ---- hair shell geometry ----
const hverts = [];
const vmap = new Map();
for (const t of plan.hair_tris) {
  for (let k = 0; k < 3; k++) {
    const v = indices[t * 3 + k];
    if (!vmap.has(v)) { vmap.set(v, hverts.length); hverts.push(v); }
  }
}
const H = hverts.length;
const hPos = new Float32Array(H * 3), hNrm = new Float32Array(H * 3),
      hUv = new Float32Array(H * 2), hJ = new Uint16Array(H * 4), hW = new Float32Array(H * 4);
hverts.forEach((v, i) => {
  const nx = Math.max(normals[v*3]/32767, -1), ny = Math.max(normals[v*3+1]/32767, -1), nz = Math.max(normals[v*3+2]/32767, -1);
  hPos[i*3]   = positions[v*3]   + nx * EPS;
  hPos[i*3+1] = positions[v*3+1] + ny * EPS;
  hPos[i*3+2] = positions[v*3+2] + nz * EPS;
  hNrm[i*3] = nx; hNrm[i*3+1] = ny; hNrm[i*3+2] = nz;
  hUv[i*2] = uvs[v*2]/65535; hUv[i*2+1] = uvs[v*2+1]/65535;
  const w = plan.vert_weights[String(v)] || [[plan.head_joint, 1]];
  w.forEach(([j, wt], s) => { hJ[i*4+s] = j; hW[i*4+s] = wt; });
});
const hIdx = new Uint16Array(plan.hair_tris.length * 3);
plan.hair_tris.forEach((t, ti) => {
  for (let k = 0; k < 3; k++) hIdx[ti*3+k] = vmap.get(indices[t*3+k]);
});
console.log(`hair shell: ${H} verts, ${plan.hair_tris.length} tris`);

// ---- append binary ----
let binOut = bin;
const blobs = [Buffer.from(hPos.buffer), Buffer.from(hNrm.buffer), Buffer.from(hUv.buffer),
               Buffer.from(hJ.buffer), Buffer.from(hW.buffer), Buffer.from(hIdx.buffer),
               Buffer.from(newIBM.buffer)];
const addBV = (buf) => {
  const off = binOut.length;
  const pad = (4 - (off % 4)) % 4;
  binOut = Buffer.concat([binOut, Buffer.alloc(pad), buf]);
  const bv = { buffer: 0, byteOffset: off + pad, byteLength: buf.length };
  json.bufferViews.push(bv);
  return json.bufferViews.length - 1;
};
const addAcc = (bv, comp, type, count, min, max) => {
  const acc = { bufferView: bv, componentType: comp, type, count };
  if (min) { acc.min = min; acc.max = max; }
  json.accessors.push(acc);
  return json.accessors.length - 1;
};
const minmax = (arr, n) => {
  const mn = [1e9,1e9,1e9], mx = [-1e9,-1e9,-1e9];
  for (let i = 0; i < arr.length; i += n) for (let k = 0; k < n; k++) {
    mn[k] = Math.min(mn[k], arr[i+k]); mx[k] = Math.max(mx[k], arr[i+k]);
  }
  return [mn.slice(0,n), mx.slice(0,n)];
};
const [pmin, pmax] = minmax(hPos, 3);
const bPos = addBV(blobs[0]), bNrm = addBV(blobs[1]), bUv = addBV(blobs[2]),
      bJ = addBV(blobs[3]), bW = addBV(blobs[4]), bI = addBV(blobs[5]), bIBM = addBV(blobs[6]);
const aPos = addAcc(bPos, 5126, "VEC3", H, pmin, pmax);
const aNrm = addAcc(bNrm, 5126, "VEC3", H);
const aUv = addAcc(bUv, 5126, "VEC2", H);
const aJ = addAcc(bJ, 5123, "VEC4", H);
const aW = addAcc(bW, 5126, "VEC4", H);
const aI = addAcc(bI, 5123, "SCALAR", hIdx.length);
const aIBM = addAcc(bIBM, 5126, "MAT4", nOld + nNew);

// ---- wire up ----
skin.joints = extJoints;
skin.inverseBindMatrices = aIBM;
json.meshes[0].primitives.push({
  attributes: { POSITION: aPos, NORMAL: aNrm, TEXCOORD_0: aUv, JOINTS_0: aJ, WEIGHTS_0: aW },
  indices: aI, material: 0, mode: 4,
});
json.buffers[0].byteLength = binOut.length;

// ---- write GLB ----
const jsonStr = Buffer.from(JSON.stringify(json), "utf8");
const jsonPad = (4 - (jsonStr.length % 4)) % 4;
const binPad = (4 - (binOut.length % 4)) % 4;
const total = 12 + 8 + jsonStr.length + jsonPad + 8 + binOut.length + binPad;
const out = Buffer.alloc(total);
out.writeUInt32LE(0x46546c67, 0); out.writeUInt32LE(2, 4); out.writeUInt32LE(total, 8);
let o = 12;
out.writeUInt32LE(jsonStr.length + jsonPad, o); out.writeUInt32LE(0x4e4f534a, o+4); o += 8;
jsonStr.copy(out, o); out.fill(0x20, o + jsonStr.length, o + jsonStr.length + jsonPad); o += jsonStr.length + jsonPad;
out.writeUInt32LE(binOut.length + binPad, o); out.writeUInt32LE(0x004e4942, o+4); o += 8;
binOut.copy(out, o);
writeFileSync(outPath, out);
console.log(`wrote ${outPath} (${(total/1048576).toFixed(2)} MB), joints ${nOld} -> ${nOld+nNew}`);
