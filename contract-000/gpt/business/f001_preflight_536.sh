#!/usr/bin/env bash
# F-001 Run536: PREPARATION ONLY. Does not run tests or CI.
set -euo pipefail
root="$(git rev-parse --show-toplevel)" || exit 2
cd "$root"
if [[ -n "$(git status --porcelain --untracked-files=all)" ]]; then
  echo 'F001_PREFLIGHT=HOLD dirty checkout (including untracked files)' >&2; exit 3
fi
for p in contract-000/gpt/business/f001_exact_source_nine_case_524.sh contract-000/gpt/business/f001_nine_case_audited_527.sh contract-000/gpt/business/f001_custody_manifest_530.sh; do
  [[ -f "$p" ]] || { echo "F001_PREFLIGHT=HOLD missing $p" >&2; exit 4; }
done
for cmd in git bash python3 node timeout sha256sum mktemp; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "F001_PREFLIGHT=HOLD missing $cmd" >&2; exit 5; }
done
# Pin checks are static availability checks, not execution of the suite.
dir=contract-000/gpt/business
for pair in '578fe60cc1820784556bb89db8933fff8d06db03:f001_h3b_close_v2_514.js:d57773dcfa5e0e980539a05cb7ecb14058c7b6e9' '578fe60cc1820784556bb89db8933fff8d06db03:test_f001_h3b_close_v2_515.js:d02a1ff4147f37db9b09b5145d69768d4e568066' 'd0c7a4dd9ea4177c092dbc594817eee0bd661ef5:test_f001_h3b_supplement_521.js:081337219f4955f44a5441b7b9dbb34ab5cfd6ee'; do
  IFS=: read -r commit file expected <<< "$pair"
  actual="$(git rev-parse "$commit:$dir/$file" 2>/dev/null)" || { echo "F001_PREFLIGHT=HOLD missing pinned history $commit:$file" >&2; exit 6; }
  [[ "$actual" == "$expected" ]] || { echo "F001_PREFLIGHT=HOLD source pin mismatch $file" >&2; exit 7; }
done
echo 'F001_PREFLIGHT=READY_FOR_SEPARATE_PREREGISTERED_TEST'
printf 'commit=%s\nnode=%s\n' "$(git rev-parse HEAD)" "$(node --version)"
# READY is not a test result or release authorization.
