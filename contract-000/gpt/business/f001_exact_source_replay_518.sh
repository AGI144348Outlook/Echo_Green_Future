#!/usr/bin/env bash
# F-001 exact-source six-case replay runner. PREPARATION ONLY; NOT EXECUTED.
# Preregistered test discussion: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/197
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
commit="578fe60cc1820784556bb89db8933fff8d06db03"
dir="contract-000/gpt/business"
validator="f001_h3b_close_v2_514.js"
harness="test_f001_h3b_close_v2_515.js"
expected_validator="d57773dcfa5e0e980539a05cb7ecb14058c7b6e9"
expected_harness="d02a1ff4147f37db9b09b5145d69768d4e568066"
for entry in "$validator:$expected_validator" "$harness:$expected_harness"; do
  file="${entry%%:*}"; expected="${entry#*:}"
  actual="$(git rev-parse "$commit:$dir/$file")"
  if [[ "$actual" != "$expected" ]]; then
    printf 'FAIL pinned Git blob: %s expected=%s actual=%s\n' "$file" "$expected" "$actual" >&2
    exit 3
  fi
done
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
git show "$commit:$dir/$validator" > "$tmp/$validator"
git show "$commit:$dir/$harness" > "$tmp/$harness"
for entry in "$validator:$expected_validator" "$harness:$expected_harness"; do
  file="${entry%%:*}"; expected="${entry#*:}"
  actual="$(git hash-object "$tmp/$file")"
  [[ "$actual" == "$expected" ]] || { echo "FAIL extracted bytes $file" >&2; exit 4; }
done
printf 'Source commit: %s\n' "$commit"
sha256sum "$tmp/$validator" "$tmp/$harness"
node --version
# Only the preregistered six synthetic cases. Do not add tests without a new pretest entry.
# An external timeout is mandatory. Run in an offline, disposable environment.
timeout 20s node "$tmp/$harness"
