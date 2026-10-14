# How Grok Bot works (copy this process)

Rules: [money-machine-hq docs/AGENTS.md](https://github.com/mhvnsnt/money-machine-hq/blob/main/docs/AGENTS.md) (laws 14 and 15 plus the adopted patterns), [docs/muse-training-pack/](https://github.com/mhvnsnt/money-machine-hq/tree/main/docs/muse-training-pack) (PRE-FLIGHT.md, EXAMPLES.md), and the media-proof standard in AGENTS.md (also mirrored in [Bannon AGENTS.md](https://github.com/mhvnsnt/Bannon/blob/main/AGENTS.md)).

1. **Lock the method.** Quote the owner's words verbatim. Name the method he said (e.g. "Smart Cut"). Say it back. If you can't do it that way, stop and say why. Never swap in a different method.
2. **Claim it.** Add a line to [CLAIMS.md](CLAIMS.md) (agent, task, branch, time).
3. **Branch plus PR, always.** Never push to main. Fill every section of the PR template (instruction gate).
4. **Small pushes.** Push each piece as soon as it's done. Don't sit on WIP.
5. **Edit in place.** Open the existing file or project and change it. Never start a new copy.
6. **Never delete or overwrite** his work without his explicit OK. Check the diff stat before every commit. Deletion guard: more than 20 files or anything in `canon/` means stop and ask.
7. **Proof.** Every "done" comes with evidence: renders/frames, checkerboard edge checks for cutouts (no rectangles), sha256 hashes of outputs, test or CI output, links.
8. **Honest status line first.** Put "Failed", "Partial" or "Done" in the first line. Mock-tested is not live. Unreadable CI counts as a fail.
9. **Merge rule.** Merge only if it merges cleanly, every check is verified green, and nothing is deleted. Otherwise leave it open and say why.
10. **Log the workflow.** Record what you did, how, which tools and files, and where the output is, in the repo.
11. **Check before claiming done.** Re-read his literal words and compare them to the result, method included.
12. **Hygiene.** Run gitleaks before pushing. No secrets. Use unique temp file names.
