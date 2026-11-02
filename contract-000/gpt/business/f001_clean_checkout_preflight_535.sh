#!/usr/bin/env bash
# F-001 Run535: read-only PRE-EXECUTION gate. No tests invoked by this script.
# Use after the existing Issue #197 preregistration is confirmed and before any replay.
set -euo pipefail
root="$(git rev-parse --show-toplevel)" || exit 2
cd "$root"
if [ -n "$(git status --porcelain --untracked-files=all)" ]; then
  echo 'F001_PREFLIGHT=HOLD dirty or untracked checkout; do not execute exact-source replay' >&2
  exit 3
fi
for p in \
  contract-000/gpt/business/f001_exact_source_nine_case_524.sh \
  contract-000/gpt/business/f001_nine_case_audited_527.sh \
  contract-000/gpt/business/f001_custody_manifest_530.sh; do
  if [ ! -f "$p" ]; then echo "F001_PREFLIGHT=HOLD missing $p" >&2; exit 4; fi
done
for cmd in git bash python3 sha256sum; do
  if ! command -v "$cmd" >/dev/null 2>&1; then echo "F001_PREFLIGHT=HOLD missing $cmd" >&2; exit 5; fi
done
printf 'F001_PREFLIGHT=READY_FOR_SEPARATE_AUTHORIZED_TEST\ncommit=%s\n' "$(git rev-parse HEAD)"
printf 'source_blobs:\n'
git ls-files -s -- \
  contract-000/gpt/business/f001_exact_source_nine_case_524.sh \
  contract-000/gpt/business/f001_nine_case_audited_527.sh \
  contract-000/gpt/business/f001_custody_manifest_530.sh
# This gate is not evidence that the 9 cases ran or passed.
