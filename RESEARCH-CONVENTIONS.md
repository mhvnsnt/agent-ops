# Research Conventions (all repos, all agents)

**Laws:** RESEARCH-TO-REPO LAW + CONTINUOUS RESEARCH + PULL-IN LAW (owner 2026-10-16). Owner hates bureaucracy — this is the whole system, keep it this small.

## Where research docs live
1. **Repo-specific findings → that repo's `docs/research/`**. Example: render research → `western-heart/docs/research/`, teardown tooling → `game-reverse-engineering/docs/research/`, animation → `cape-jones/docs/research/`.
2. **Cross-cutting / multi-repo findings → `mhvnsnt/agent-ops`** (this repo is the docs hub). Handoffs, indexes, conventions, manifests.
3. **Never local-only.** A research doc that only exists on the VM disk doesn't exist.

## The master index
`~/workspace/agent-ops/RESEARCH-PULLIN-INDEX.md` — one line per topic:
`| Topic | Date | Doc (repo + path) | Pulled in | Status |`
Status: `researching` → `wired` (installed+tested+green) → `excluded` (license reason documented).
**Check the index BEFORE starting new research** (`./research-check.sh "topic"`). A finding without a pull-in is incomplete — track until wired or excluded.

## Decision records (ADR-lite)
For decisions with real consequences (tool choice, format choice, pipeline design), drop a short file in the repo's `docs/adr/`:
`docs/adr/0001-short-title.md` — template at `~/workspace/agent-ops/adr-template.md`.
Rules: one decision per file, dated, status line (proposed/accepted/superseded). **Never edit a decided ADR** — write a new one that supersedes it and link both ways.

## Research → action pipeline
Every research pass ends in one of three states, recorded in the index:
1. **Wired** — tool pulled in, installed, tested, pushed green (branch → PR → merge).
2. **Excluded** — documented with the honest license/technical reason (e.g. non-commercial, region-excluded).
3. **Queued** — finding recorded, pull-in tracked as a work item with an owner.

## Dedupe
- Before researching: `research-check.sh` + index search. If it exists, extend it — don't start over.
- Before pulling: check the index's "Previously pulled" tables. If it's there, wire the existing copy.
- Source trail survives: every index entry links the doc; every doc links its sources.

## Cross-referencing (wikilinks)
Use `[[DOC-NAME]]` wikilinks when one doc references another (Zettelkasten pattern:
atomic notes, links over folders). They render as plain text on GitHub but are
grep-able, so agents and `research-check.sh` can follow the graph:
`grep -r "\[\[RESEARCH-PULLIN-INDEX\]\]" --include="*.md"`.
- The master index is `[[RESEARCH-PULLIN-INDEX]]` — link it from every research doc's header.
- Related docs link each other both ways (A links B, B links A).
- Searchable docs site: `mkdocs.yml` builds this hub with mkdocs-material
  (full-text search, phone-friendly). Deploys to GitHub Pages via
  `.github/workflows/docs.yml` on push to main. Local preview: `mkdocs serve`.
  When adding a new root `.md`, also add its symlink: `cd docs && ln -s ../NEW.md .`
  (the CI workflow re-links automatically, but local serve needs it).
