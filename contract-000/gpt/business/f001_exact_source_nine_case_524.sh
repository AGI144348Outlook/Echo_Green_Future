#!/usr/bin/env bash
# F-001 exact-source nine-case offline replay. PREPARATION ONLY; NOT EXECUTED.
# Preregistered: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/197
# Operator MUST confirm Issue #197 remains accessible and same-thread results can be posted BEFORE running.
set -euo pipefail
command -v git >/dev/null && command -v node >/dev/null && command -v timeout >/dev/null && command -v sha256sum >/dev/null
root="$(git rev-parse --show-toplevel)"
cd "$root"
dir=contract-000/gpt/business
base=578fe60cc1820784556bb89db8933fff8d06db03
supp=d0c7a4dd9ea4177c092dbc594817eee0bd661ef5
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
extract() {
  local commit="$1" name="$2" expected="$3" actual
  actual="$(git rev-parse "$commit:$dir/$name")"
  [[ "$actual" == "$expected" ]] || { echo "FAIL source pin $name: $actual != $expected" >&2; exit 3; }
  git show "$commit:$dir/$name" > "$tmp/$name"
  actual="$(git hash-object "$tmp/$name")"
  [[ "$actual" == "$expected" ]] || { echo "FAIL extracted byte identity $name" >&2; exit 4; }
  printf 'SOURCE %s commit=%s git_blob=%s sha256=%s\n' "$name" "$commit" "$actual" "$(sha256sum "$tmp/$name" | cut -d' ' -f1)"
}
extract "$base" f001_h3b_close_v2_514.js d57773dcfa5e0e980539a05cb7ecb14058c7b6e9
extract "$base" test_f001_h3b_close_v2_515.js d02a1ff4147f37db9b09b5145d69768d4e568066
extract "$supp" test_f001_h3b_supplement_521.js 081337219f4955f44a5441b7b9dbb34ab5cfd6ee
printf 'NODE %s\n' "$(node --version)"
printf 'TESTSET 6 original + 3 supplemental; isolated child processes; synthetic fixtures only\n'
set +e
timeout 20s node "$tmp/test_f001_h3b_close_v2_515.js"
six=$?
timeout 20s node "$tmp/test_f001_h3b_supplement_521.js"
three=$?
set -e
printf 'EXIT original=%s supplemental=%s\n' "$six" "$three"
[[ "$six" -eq 0 && "$three" -eq 0 ]] || exit 1
# Operator: paste complete stdout/stderr, source pins, exit codes and limitations
# into Issue #197. Zero exit does not imply rights or publication clearance.
