# Ghidra SF EX Vertex Decode Pipeline

**Owner directive:** "Use Ghidra and MCP, use all the stuff for reverse engineering... Stop fiddling with a screwdriver for a jackhammer job when the jackhammer is right there."
**Law:** NO-HAND-TOOLING LAW (owner 2026-10-16)

## Pipeline Architecture

```
SLUS_011.05 (PSX EXE, 726K)
    │
    ▼
┌─────────────┐
│   Ghidra    │  Headless analysis + decompiler
│   12.1.4    │  PSX processor module (built-in)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ GhidraMCP   │  MCP bridge (LaurieWired/GhidraMCP)
│  Plugin     │  50+ tools: decompile, xrefs, strings, etc.
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  AI Agents  │  Query Ghidra via MCP, no hand-written parsers
└─────────────┘
```

## Target: PAC Section 2 Vertex Decode Function

**What we're looking for:** The function in SLUS_011.05 that reads PAC section 2 chunks and converts 8-byte vertex records to PSX GPU vertices.

**Search strategy in Ghidra:**
1. Find references to the section-2 offset table walk
2. Search for the constant trailer `0x08000000`
3. Look for functions reading 8-byte strides from PAC data
4. Cross-reference from known GPU packet submission code

**Expected output:** Decompiled C pseudocode showing exactly how bytes 0-7 map to (x, y, z, attributes).

## Installation Status

- [x] Ghidra 12.1.4 downloading → `~/workspace/tools/ghidra/`
- [x] JDK 21 downloading → `~/workspace/tools/ghidra/`
- [x] GhidraMCP cloned → `~/workspace/tools/ghidra-mcp/`
- [x] MCP bridge deps installed (venv)
- [ ] Ghidra extracted and verified
- [ ] JDK extracted, JAVA_HOME set
- [ ] GhidraMCP plugin installed
- [ ] SLUS_011.05 imported and analyzed
- [ ] PAC loader function identified
- [ ] Vertex decode decompiled

## Why This Beats Hand-Tooling

| Hand-tooling (screwdriver) | Ghidra+MCP (jackhammer) |
|---|---|
| Guess byte meanings from patterns | Read the actual decode function |
| Write throwaway Python per format | Reusable decompiled pseudocode |
| Can't verify guesses | Ground truth from game code |
| One-off, not repeatable | Pipeline works for all 3 games |
