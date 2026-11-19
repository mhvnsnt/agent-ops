# PR body template — passes instruction gates (e.g. western-heart law 15)

Some repos gate merges on the PR body proving the owner's method was used
(western-heart `.github/scripts/instruction_gate.py`). A plain-paragraph body
FAILS the gate. Copy this template into every PR body, fill it in truthfully,
and keep the six headings exactly as written (the gate matches headings by
normalised text).

## Owner instruction (verbatim quote)

> Paste the owner's exact words. Do not paraphrase.

## Method the owner specified

The method the owner named, in his words as close as possible.

## Method actually used

The method actually used. Write it IDENTICAL to the section above when you
used exactly what he specified — if the two differ and Deviations says
"None", the gate fails. If you deviated, list each deviation below with his
approval link.

## Deviations (none / list, each with owner approval link)

None.

## Proof (paths to files, frames, test output)

- `path/in/this/prs/diff` (each file/frame/test-output path in backticks)
- https://github.com/mhvnsnt/<repo>/... (URLs resolve; commits must exist in
  THIS repo; digests alone do not count — attach them to a file/commit/tag)

Every proof path must be in the PR diff, exist in the repo, or be a URL /
commit / tag / release of this repo — otherwise the gate fails that line.

## Self-check: I verified the result against the literal instruction

- [x] I verified the result against the literal instruction: <one line, what
  you actually checked — counts, hashes, files read back from main>.
