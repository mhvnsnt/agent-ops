#!/usr/bin/env bash
# test-resilient-upload.sh — functional tests for resilient-gh-upload.sh
# Stubs do_curl/do_gh (no network). Run: bash lanes/tests/test-resilient-upload.sh
#
# NOTE: main is always invoked in a subshell because die() exits the process.
# Stub state that must survive is therefore file-based under $TDIR.
set -u
cd "$(dirname "$0")/.." || exit 2

PASS=0; FAIL=0
ok()   { PASS=$((PASS+1)); printf 'PASS: %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL: %s\n' "$1"; }

export RU_PART_SIZE=1048576 RU_MAX_ATTEMPTS=8
export GH_TOKEN="test-token"
sleep() { :; }   # no-op backoff in tests

# shellcheck disable=SC1091
source ./resilient-gh-upload.sh   # defines functions only (BASH_SOURCE guard)

TDIR="$(mktemp -d)"; trap 'rm -rf "$TDIR"' EXIT
export TDIR
head -c 2621440 /dev/urandom >"$TDIR/big.bin"   # 2.5MB -> 3 parts at 1MB
: >"$TDIR/calls.log"; : >"$TDIR/gh-delete.log"; : >"$TDIR/assets.state"
curl_calls() { wc -l <"$TDIR/calls.log"; }
gh_deletes() { wc -l <"$TDIR/gh-delete.log"; }
reset_run()  { : >"$TDIR/calls.log"; : >"$TDIR/gh-delete.log"; : >"$TDIR/assets.state"; GH_ASSETS_SEED=""; }

# ---------- stub infrastructure ----------
CURL_MODE="success"     # success | stall2 | perm401
export CURL_MODE
# shellcheck disable=SC2317
do_curl() {
    printf 'C\n' >>"$TDIR/calls.log"
    local bodyfile="" tfile="" aname="" prev=""
    for a in "$@"; do
        [[ "$prev" == "-o" ]] && bodyfile="$a"
        [[ "$prev" == "-T" ]] && tfile="$a"
        prev="$a"
    done
    aname="$(printf '%s' "$@" | grep -o 'name=[^ ]*' | tail -1 | cut -d= -f2-)"
    if [[ "$CURL_MODE" == "stall2" ]]; then
        local left=0
        [[ -f "$TDIR/fails.left" ]] && left="$(cat "$TDIR/fails.left")"
        if (( left > 0 )); then
            printf '%s' $((left-1)) >"$TDIR/fails.left"
            return 28
        fi
    fi
    if [[ "$CURL_MODE" == "perm401" ]]; then
        printf '{"message":"Bad credentials"}' >"$bodyfile"; printf '401'; return 0
    fi
    local sz sh
    sz="$(stat -c%s "$tfile")"; sh="$(sha256sum "$tfile" | awk '{print $1}')"
    printf '{"id":999,"name":"%s","size":%s,"state":"uploaded","digest":"sha256:%s"}' \
        "$aname" "$sz" "$sh" >"$bodyfile"
    # stateful stub: the "release" now has this asset, so final-verify passes
    printf '9%03d\t%s\t%s\tuploaded\n' "$(curl_calls)" "$aname" "$sz" >>"$TDIR/assets.state"
    printf '201'; return 0
}
# shellcheck disable=SC2317
do_gh() {
    case "$*" in
        *"releases/tags/"*) printf '12345'; return 0;;
        *"assets?per_page=100"*)
            { [[ -n "${GH_ASSETS_SEED:-}" ]] && printf '%s\n' "$GH_ASSETS_SEED"; cat "$TDIR/assets.state" 2>/dev/null; } | grep -v '^$' || true
            return 0;;
        *"-X DELETE"*) printf 'D\n' >>"$TDIR/gh-delete.log"; return 0;;
        *"auth token"*) printf 'test-token'; return 0;;
    esac
    printf 'do_gh stub: unhandled: %s\n' "$*" >&2; return 1
}
GH_ASSETS_SEED=""

# ---------- T1: split + manifest (dry-run) ----------
reset_run
export RU_DRY_RUN=1
if ( main "o/r" "v1" "$TDIR/big.bin" ) >/dev/null 2>"$TDIR/t1.log"; then
    ok "T1 dry-run main exits 0"
else bad "T1 dry-run main exits 0"; fi
grep -q "manifest: 3 parts" "$TDIR/t1.log" && ok "T1 three parts logged" || bad "T1 three parts logged"
unset RU_DRY_RUN

# ---------- T2: stall then success (exit 28 x2 -> 201) ----------
reset_run
CURL_MODE="stall2"; export CURL_MODE; printf '2' >"$TDIR/fails.left"
head -c 100 /dev/urandom >"$TDIR/p.bin"
if ( upload_one_part "o/r" "12345" "tok" "$TDIR/p.bin" "p.bin.0000" ) >/dev/null 2>&1; then
    ok "T2 stall-retry eventually succeeds"
else bad "T2 stall-retry eventually succeeds"; fi
[[ "$(curl_calls)" == "3" ]] && ok "T2 exactly 3 curl calls (2 stalls + 1 success)" \
    || bad "T2 exactly 3 curl calls (got $(curl_calls))"

# ---------- T3: idempotent skip (2 parts present, sizes match) ----------
reset_run
CURL_MODE="success"; export CURL_MODE
GH_ASSETS_SEED="$(printf '111\tbig.bin.0000\t1048576\tuploaded\n112\tbig.bin.0001\t1048576\tuploaded')"
export GH_ASSETS_SEED
if ( main "o/r" "v1" "$TDIR/big.bin" ) >/dev/null 2>"$TDIR/t3.log"; then
    ok "T3 main exits 0 with 2 parts pre-existing"
else bad "T3 main exits 0 with 2 parts pre-existing"; fi
[[ "$(curl_calls)" == "2" ]] && ok "T3 only missing part + manifest uploaded (2 curl calls)" \
    || bad "T3 only missing part + manifest uploaded (got $(curl_calls))"
grep -q "SKIP part big.bin.0000" "$TDIR/t3.log" && ok "T3 skip logged for .0000" || bad "T3 skip logged for .0000"
[[ "$(gh_deletes)" == "0" ]] && ok "T3 no deletes" || bad "T3 no deletes (got $(gh_deletes))"

# ---------- T4: permanent failure (401) — exactly 1 attempt ----------
reset_run
CURL_MODE="perm401"; export CURL_MODE
if ( upload_one_part "o/r" "12345" "tok" "$TDIR/p.bin" "p.bin.0000" ) >/dev/null 2>&1; then
    bad "T4 401 aborts (returned 0)"
else ok "T4 401 aborts (non-zero)"; fi
[[ "$(curl_calls)" == "1" ]] && ok "T4 exactly 1 attempt on 401" \
    || bad "T4 exactly 1 attempt on 401 (got $(curl_calls))"

# ---------- T5: size mismatch -> DELETE + re-upload ----------
reset_run
CURL_MODE="success"; export CURL_MODE
GH_ASSETS_SEED="$(printf '111\tbig.bin.0000\t123\tuploaded')"
export GH_ASSETS_SEED
if ( main "o/r" "v1" "$TDIR/big.bin" ) >/dev/null 2>"$TDIR/t5.log"; then
    ok "T5 main exits 0 with mismatched part"
else bad "T5 main exits 0 with mismatched part"; fi
[[ "$(gh_deletes)" == "1" ]] && ok "T5 one DELETE for mismatched part" \
    || bad "T5 one DELETE for mismatched part (got $(gh_deletes))"
grep -q "REPLACE part big.bin.0000" "$TDIR/t5.log" && ok "T5 replace logged" || bad "T5 replace logged"

# ---------- T6: manifest schema ----------
reset_run
CURL_MODE="success"; export CURL_MODE
export RU_KEEP_TMPD=1 RU_TMPD_FILE="$TDIR/tmpd.path"
if ( main "o/r" "v1" "$TDIR/big.bin" ) >/dev/null 2>&1; then
    ok "T6 full stubbed run exits 0"
else bad "T6 full stubbed run exits 0"; fi
TMPD_KEPT="$(cat "$TDIR/tmpd.path")"
MF="$TMPD_KEPT/big.bin.manifest.json"
if [[ -f "$MF" ]] && python3 - "$MF" "$TDIR/big.bin" <<'EOF'
import json,sys,hashlib
m=json.load(open(sys.argv[1])); data=open(sys.argv[2],'rb').read()
assert m["name"]=="big.bin", m
assert m["size"]==len(data), m
assert m["sha256"]==hashlib.sha256(data).hexdigest(), m
assert m["part_size"]==1048576, m
assert len(m["parts"])==3, m
assert [p["name"] for p in m["parts"]]==["big.bin.0000","big.bin.0001","big.bin.0002"], m
assert m["standard"]=="100MB-single-standard", m
print("schema ok")
EOF
then ok "T6 manifest schema valid (name/size/sha256/part_size/3 parts)"; else bad "T6 manifest schema valid"; fi
rm -rf "$TMPD_KEPT"; unset RU_KEEP_TMPD RU_TMPD_FILE

printf '\n%s passed, %s failed\n' "$PASS" "$FAIL"
[[ "$FAIL" == "0" ]]
