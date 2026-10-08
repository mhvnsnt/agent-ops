/** Re-skin hair: patch the body mesh's JOINTS_0/WEIGHTS_0 in place for hair verts,
 *  add hair bone nodes, extend the skin. No new geometry -> no holes possible.
 *  Hair-line verts stay 100% Head-weighted (from the plan), so no tearing.
 */
import { readFileSync, writeFileSync } from "node:fs";
import * as THREE from "/home/hatch/workspace/game-sweep/AshLanev2/node_modules/three/build/three.module.js";
import { MeshoptDecoder } from "/home/hatch/workspace/game-sweep/AshLanev2/node_modules/three/examples/jsm/libs/meshopt_decoder.module.js";

const [,, inPath, planPath, outPath] = process.argv;

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
const vCount = A("POSITION").count;

// ---- decode original skinning ----
const jBuf = await decodeBV(json, bin, A("JOINTS_0").bufferView);
const wBuf = await decodeBV(json, bin, A("WEIGHTS_0").bufferView);
const joints = new Uint16Array(jBuf.buffer, jBuf.byteOffset, vCount * 4);
const weights = new Float32Array(wBuf.buffer, wBuf.byteOffset, vCount * 4);

// ---- patch hair verts ----
let patched = 0;
for (const [vs, w] of Object.entries(plan.vert_weights)) {
  const v = +vs;
  const jj = [0,0,0,0], ww = [0,0,0,0];
  w.forEach(([j, wt], s) => { if (s < 4) { jj[s] = j; ww[s] = wt; } });
  // renormalize (safety)
  const sum = ww[0]+ww[1]+ww[2]+ww[3];
  for (let s = 0; s < 4; s++) { joints[v*4+s] = jj[s]; weights[v*4+s] = ww[s]/sum; }
  patched++;
}
console.log(`patched ${patched} verts`);

// ---- bind-pose world matrices ----
const nodes = json.nodes;
const parent = new Array(nodes.length).fill(-1);
nodes.forEach((n, i) => (n.children || []).forEach((c) => (parent[c] = i)));
const worldMats = [];
{
  const local = (i) => {
    const n = nodes[i];
    return new THREE.Matrix4().compose(
      new THREE.Vector3(...(n.translation || [0, 0, 0])),
      new THREE.Quaternion(...(n.rotation || [0, 0, 0, 1])),
      new THREE.Vector3(...(n.scale || [1, 1, 1])));
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

// ---- create hair bone nodes (identical to shell version) ----
const newNodeIdx = [];
const boneBindWorld = [];
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
const skin = json.skins[0];
const ibmAcc = json.accessors[skin.inverseBindMatrices];
const ibmBuf = await decodeBV(json, bin, ibmAcc.bufferView);
const oldIBM = new Float32Array(ibmBuf.buffer, ibmBuf.byteOffset, ibmAcc.count * 16);
const nOld = skin.joints.length, nNew = newNodeIdx.length;
const newIBM = new Float32Array((nOld + nNew) * 16);
newIBM.set(oldIBM);
boneBindWorld.forEach((bw, k) => newIBM.set(bw.clone().invert().toArray(), (nOld + k) * 16));
skin.joints = [...skin.joints, ...newNodeIdx];

// ---- append binary: new JOINTS_0, WEIGHTS_0, IBM ----
let binOut = bin;
const addBV = (buf) => {
  const off = binOut.length;
  const pad = (4 - (off % 4)) % 4;
  binOut = Buffer.concat([binOut, Buffer.alloc(pad), buf]);
  json.bufferViews.push({ buffer: 0, byteOffset: off + pad, byteLength: buf.length });
  return json.bufferViews.length - 1;
};
const addAcc = (bv, comp, type, count) => {
  json.accessors.push({ bufferView: bv, componentType: comp, type, count });
  return json.accessors.length - 1;
};
const bJ = addBV(Buffer.from(joints.buffer, joints.byteOffset, joints.byteLength));
const bW = addBV(Buffer.from(weights.buffer, weights.byteOffset, weights.byteLength));
const bIBM = addBV(Buffer.from(newIBM.buffer));
const aJ = addAcc(bJ, 5123, "VEC4", vCount);
const aW = addAcc(bW, 5126, "VEC4", vCount);
const aIBM = addAcc(bIBM, 5126, "MAT4", nOld + nNew);
prim.attributes.JOINTS_0 = aJ;
prim.attributes.WEIGHTS_0 = aW;
skin.inverseBindMatrices = aIBM;
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
console.log(`wrote ${outPath} (${(total/1048576).toFixed(2)} MB), joints ${nOld} -> ${nOld+nNew}, prims: ${json.meshes[0].primitives.length}`);
