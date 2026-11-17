#!/usr/bin/env bash
# disk-clear-guard-test.sh — self-test for disk-clear-guard.sh.
# Builds fixtures under /tmp, asserts each block reason fires and the clean
# case passes. Exits non-zero if any test fails. Creates one temporary lane
# dir under ~/workspace for the dependency test and removes it in teardown.
# Never touches the real protected-paths registry (uses a temp
# LANE_GUARD_STATE_DIR) and never deletes anything outside its fixtures.
set -u
GUARD="${0%/*}/disk-clear-guard.sh"
[ -x "$GUARD" ] || { echo "guard not executable: $GUARD"; exit 2; }
FIX=/tmp/disk-clear-guard-test
LANE_FIX=~/workspace/_guard-test-lane-20261117
PASS=0; FAIL=0

teardown() {
  pkill -f "^sleep 60$" 2>/dev/null || true
  rm -rf "$FIX" "$LANE_FIX"
}
trap teardown EXIT
rm -rf "$FIX" "$LANE_FIX"
mkdir -p "$FIX"

# expect <name> <want_exit> <want_reason_substring> <guard args...>
expect() {
  local name="$1" want="$2" want_reason="$3"; shift 3
  local out code
  out="$("$GUARD" --no-log "$@" 2>&1)"; code=$?
  if [ "$code" -eq "$want" ] && { [ -z "$want_reason" ] || echo "$out" | grep -q -F "$want_reason"; }; then
    echo "PASS $name (exit $code)"
    PASS=$((PASS+1))
  else
    echo "FAIL $name: want exit $want + reason '$want_reason', got exit $code"
    echo "$out" | head -12
    FAIL=$((FAIL+1))
  fi
}

mkold() { # mkold <dir> <file...> : create files, backdate 2 days (beats 24h recency)
  local d="$1"; shift
  mkdir -p "$d"
  for f in "$@"; do mkdir -p "$(dirname "$d/$f")"; echo "x" > "$d/$f"; done
  find "$d" -exec touch -d '2 days ago' {} + 2>/dev/null
}

# t1: clean dir, manifest covers every file -> CLEARABLE (0)
mkold "$FIX/t1-clean" a.txt sub/b.txt
(cd "$FIX/t1-clean" && find . -type f -printf '%P\n' | sort > "$FIX/t1-manifest.txt")
expect "t1-clean-clearable" 0 "" --stored-manifest "$FIX/t1-manifest.txt" "$FIX/t1-clean"

# t2: a file modified in the last 24h -> BLOCKED [recency]
mkold "$FIX/t2-recent" a.txt
echo "fresh" > "$FIX/t2-recent/fresh.txt"
(cd "$FIX/t2-recent" && find . -type f -printf '%P\n' | sort > "$FIX/t2-manifest.txt")
expect "t2-recent-blocked" 1 "[recency]" --stored-manifest "$FIX/t2-manifest.txt" "$FIX/t2-recent"

# t3: .DO_NOT_DELETE marker present -> BLOCKED [marker]
mkold "$FIX/t3-marker" a.txt
touch "$FIX/t3-marker/.DO_NOT_DELETE"
(cd "$FIX/t3-marker" && find . -type f -printf '%P\n' | sort > "$FIX/t3-manifest.txt")
expect "t3-marker-blocked" 1 "[marker]" --stored-manifest "$FIX/t3-manifest.txt" "$FIX/t3-marker"

# t4: no manifest supplied -> BLOCKED [manifest]
mkold "$FIX/t4-nomanifest" a.txt
expect "t4-no-manifest-blocked" 1 "[manifest]" "$FIX/t4-nomanifest"

# t5: manifest missing one file -> BLOCKED [manifest], names the file
mkold "$FIX/t5-partial" a.txt secret.txt
printf 'a.txt\n' > "$FIX/t5-manifest.txt"
expect "t5-partial-manifest-blocked" 1 "secret.txt" --stored-manifest "$FIX/t5-manifest.txt" "$FIX/t5-partial"

# t6: a recent lane CHECKPOINT references the candidate -> BLOCKED [dependency]
mkold "$FIX/t6-guardtest-candidate" a.txt
(cd "$FIX/t6-guardtest-candidate" && find . -type f -printf '%P\n' | sort > "$FIX/t6-manifest.txt")
mkdir -p "$LANE_FIX"
printf '# CHECKPOINT\nUses %s for renders.\n' "$FIX/t6-guardtest-candidate" > "$LANE_FIX/CHECKPOINT.md"
expect "t6-dependency-blocked" 1 "[dependency]" --stored-manifest "$FIX/t6-manifest.txt" "$FIX/t6-guardtest-candidate"

# t7: registry entry via guard-paths.sh (temp registry only) -> BLOCKED [registry]
mkold "$FIX/t7-registry" a.txt
(cd "$FIX/t7-registry" && find . -type f -printf '%P\n' | sort > "$FIX/t7-manifest.txt")
export LANE_GUARD_STATE_DIR="$FIX/reg"
mkdir -p "$FIX/reg"
~/workspace/agent-ops/guard-paths.sh add "$FIX/t7-registry" --kind active-scratch --owner guard-test >/dev/null
expect "t7-registry-blocked" 1 "[registry]" --stored-manifest "$FIX/t7-manifest.txt" "$FIX/t7-registry"
unset LANE_GUARD_STATE_DIR

# t8: live process with cwd inside the dir -> BLOCKED [live-procs]
mkold "$FIX/t8-liveproc" a.txt
(cd "$FIX/t8-liveproc" && find . -type f -printf '%P\n' | sort > "$FIX/t8-manifest.txt")
(cd "$FIX/t8-liveproc" && sleep 60 &)
sleep 1
expect "t8-liveproc-blocked" 1 "[live-procs]" --stored-manifest "$FIX/t8-manifest.txt" "$FIX/t8-liveproc"

# t9: git repo with uncommitted changes -> BLOCKED [git-dirty]
mkold "$FIX/t9-gitdirty" a.txt
(cd "$FIX/t9-gitdirty" && git init -q . && git add -A && git -c user.email=t@t -c user.name=t commit -qm init && echo mod >> a.txt)
(cd "$FIX/t9-gitdirty" && find . -type f -not -path './.git/*' -printf '%P\n' | sort > "$FIX/t9-manifest.txt")
expect "t9-gitdirty-blocked" 1 "[git-dirty]" --stored-manifest "$FIX/t9-manifest.txt" "$FIX/t9-gitdirty"

# t10: top-level target refused -> exit 2
expect "t10-toplevel-refused" 2 "refusing" ~/workspace

echo "---"
echo "PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ]
