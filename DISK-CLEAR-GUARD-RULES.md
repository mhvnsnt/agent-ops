# Disk Clear Guard — Rules (mandatory, no override)

## The incident that made this file

2026-11-17T02:45Z, disk-cleanup ROUND 6 QUIET1 cleared the ENTIRE
`~/workspace/_squishyfx-native-20261116/` (833,678,167 B) WHILE the P3
SquishyFX re-render batch was running in it. Renders failed "No such file"
at 02:48. The clear verified the STORED payload (PR #205 merged 56/56,
8 blends on release `squishyfx-native-20261116`, delta release
`squishyfx-native-20261116-delta`, pull-back verified 02:44:18Z) — but the
dir also held UNSTORED dev files: web harness + capture + calibration
scripts carrying live v2 edits, B1 v1 proof seq frames + metrics. The v1
frames + metrics are unrecoverable from disk (numbers survive in
BUILD-REPORT.md in the repo; peak stills + mp4s survive in `your_files/`).
Recovery was verified (8 blends re-downloaded sha256 8/8 OK; delta tar
restored the harness with v2 edits intact; v25 GLB recovered from the
afro-v25 workdir). Full record: `agent-ops/disk-cleanup-log.md:42353` and
`_proof-quality-upgrade-20261116/p3-squishyfx/CHECKPOINT.md` §WORKDIR WIPED.

## The cause (measured, not assumed)

1. **The reaper contract was never called.** `guard-paths.sh check-tree`
   (the LANE_GUARD.md reaper contract, written 2026-10-20 after a cleanup
   lane deleted a 93%-complete Tekken 5 ISO) appears **0 times** in 42,564
   lines of `disk-cleanup-log.md`. The disk-space-guardian never invoked it.
2. **The registry was empty of lanes.** `protected-paths.json` holds only 6
   static Oct-20 entries. `_squishyfx-native-20261116` was never registered.
   Nothing in the lane flow registers `~/workspace/_*-2026*` workdirs.
3. **No charter existed.** "disk-space-guardian" appears in agent-ops only
   in old CloudDog-era checkpoint JSONs. Its instructions live in the
   runtime cron, not in any repo file. No machine-enforced gate existed
   anywhere in its path.
4. **Judgment flipped.** All day Nov 16 the guardian held the dir as SACRED
   ("in-flight", "active lane"). Once PR #205 merged + the delta release
   completed, it reclassified the dir as a completed-lane store-then-clear
   candidate. It protected the P3 workdir (live Blender renders) but cleared
   the SOURCE workdir the P3 batch was reading/editing from. The guard
   protected a lane's current workdir, not the dirs the lane depends on.
5. **Payload proof ≠ dir proof.** "PR merged + release verified" was accepted
   as whole-dir proof. No unstored-content inventory was ever taken, no
   recency check, no open-file check, no dependency check. No
   `.DO_NOT_DELETE` marker existed at clear time (written 03:10Z, during
   recovery — it could not have saved the dir).

## The rule

**No cleanup — guardian, reaper, or ad-hoc — deletes, moves, or "tidies"
ANY directory without a CLEARABLE verdict from `disk-clear-guard.sh`
first.** There is NO override flag, by design. Exit 1 (BLOCKED) or exit 2
(ERROR / UNCERTAIN) means hands off: log the verdict, skip the dir, move on.
A blocked dir is never re-evaluated in the same run to get a different
answer.

```bash
# every candidate, every time, before any delete:
./disk-clear-guard.sh --stored-manifest <manifest> --log <dir>
# exit 0 = CLEARABLE, 1 = BLOCKED (reasons printed), 2 = ERROR (treat as BLOCKED)
```

## What the gate checks

| Check | Blocks when |
|---|---|
| `[registry]` | `guard-paths.sh check-tree` refuses the path (LANE_GUARD contract, now actually called). |
| `[marker]` | A `.DO_NOT_DELETE*` marker exists at/under the dir, or on an ancestor up to `~/workspace`. |
| `[recency]` | Any file under the dir was modified in the last 24 hours. |
| `[live-procs]` | Any process has its cwd inside the dir, or (when `lsof` exists) an open handle under it. |
| `[dependency]` | A recent (< 7 days) `CHECKPOINT*.md` / `PROGRESS.md` under `~/workspace` lane workdirs references the dir by path or basename. |
| `[git-dirty]` | The dir is a git repo with uncommitted changes. |
| `[manifest]` | No `--stored-manifest` supplied, or files in the dir are not listed in it. |

## The manifest rule (the ROUND 6 fix)

A whole-directory clear requires a **per-file stored manifest**: a text file
listing, one relative path per line, every file in the directory, each
verified byte-identical on a store (GitHub release, TeraBox, or repo) by the
pull-back step that produced it. "PR merged" / "release verified" without a
file list is **not** proof — it proves the payload, not the directory. Any
file not in the manifest blocks the clear and is named in the verdict. The
guard does not verify the store itself; the manifest is the operator's
attestation, and the pull-back verification behind it is what makes it true.

## Lane duty (closes the registry gap)

Every lane registers its workdir the moment it spawns, and unregisters it
when it completes:

```bash
guard-paths.sh add ~/workspace/_my-lane-20261117 --kind active-scratch --owner <lane-id> --note "<what runs here>"
# ... lane completes, branch pushed ...
guard-paths.sh remove ~/workspace/_my-lane-20261117
```

Anything that must never be cleared gets a `.DO_NOT_DELETE` marker file in
the dir itself. Both mechanisms are cheap; the guard enforces both.

## What this gate does NOT do

- It does not verify store contents itself (see the manifest rule).
- It does not replace the ONE-STORE RULE, the NEVER-KILL-IN-PROGRESS law,
  or the SAFE-STORAGE-FIRST law — it enforces them mechanically.
- It does not delete, move, or modify anything. It only reads and returns
  a verdict. The `--log` flag appends one verdict line to
  `disk-cleanup-log.md`; dry runs omit it.

## Cron update required (parent action)

The disk-space-guardian cron's instructions must be updated to call this
gate before ANY delete, with the command above and the no-override rule.
Until that update lands, the gate is enforced by convention only — the
incident proves convention is not enough. The gate script, this charter,
and `disk-clear-guard-test.sh` (10/10 self-test, 2026-11-17) are the
deliverable; the cron instruction change is the remaining step.
