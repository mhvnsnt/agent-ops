/** Dump decoded GLB geometry + hierarchy for hair analysis (Python side). */
import { readFileSync, writeFileSync } from "node:fs";
import { MeshoptDecoder } from "/home/hatch/workspace/game-sweep/AshLanev2/node_modules/three/examples/jsm/libs/meshopt_decoder.module.js";

const [,, inPath, outPath] = process.argv;

function readGLB(path) {
  const data = readFileSync(path);
  let off = 12, json = null, bin = null;
  while (off < data.length) {
    const clen = data.readUInt32LE(off), ctype = data.readUInt32LE(off + 4);
    if (ctype === 0x4e4f534a) json = JSON.parse(data.subarray(off + 8, off + 8 + clen).toString("utf8"));
    else if (ctype === 0x004e4942) bin = data.subarray(off + 8, off + 8 + clen);
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
    return { data: target, stride: ext.byteStride, count: ext.count };
  }
  const off = bv.byteOffset || 0;
  return { data: bin.subarray(off, off + bv.byteLength), stride: 0, count: 0 };
}

const { json, bin } = readGLB(inPath);
const prim = json.meshes[0].primitives[0];
const accOf = (name) => json.accessors[prim.attributes[name]];
const idxAcc = json.accessors[prim.indices];

const pos = await decodeBV(json, bin, accOf("POSITION").bufferView);
const nrm = await decodeBV(json, bin, accOf("NORMAL").bufferView);
const uv = await decodeBV(json, bin, accOf("TEXCOORD_0").bufferView);
const idx = await decodeBV(json, bin, idxAcc.bufferView);

const positions = new Float32Array(pos.data.buffer, pos.data.byteOffset, pos.count * 3);
const normals = new Int16Array(nrm.data.buffer, nrm.data.byteOffset, nrm.count * 3);
const uvs = new Uint16Array(uv.data.buffer, uv.data.byteOffset, uv.count * 2);
const indices = new Uint16Array(idx.data.buffer, idx.data.byteOffset, idx.count);

// parent map
const parent = new Array(json.nodes.length).fill(-1);
json.nodes.forEach((n, i) => (n.children || []).forEach((c) => (parent[c] = i)));
const nodes = json.nodes.map((n, i) => ({
  i, name: n.name || null, parent: parent[i],
  t: n.translation || [0, 0, 0], r: n.rotation || [0, 0, 0, 1], s: n.scale || [1, 1, 1],
}));

const out = {
  vertCount: pos.count,
  positions: Array.from(positions),
  uvs: Array.from(uvs, (v) => v / 65535),
  indices: Array.from(indices),
  nodes,
  skinJoints: json.skins[0].joints,
  skinJointCount: json.skins[0].joints.length,
};
writeFileSync(outPath, JSON.stringify(out));
console.log(`wrote ${outPath}: ${pos.count} verts, ${idx.count} indices, ${nodes.length} nodes`);
