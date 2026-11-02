#!/usr/bin/env bash
# F-001 Run540: fail-closed orchestration. NOT EXECUTED OR TESTED.
# Requires prospective Issue #197 entry and ability to post results in that thread.
# Usage: bash contract-000/gpt/business/f001_preflight_custody_540.sh /absolute/new/evidence/directory
set -euo pipefail
[[ "$#" -eq 1 && "$1" = /* ]] || { echo 'Usage: script /absolute/new/evidence/directory' >&2; exit 2; }
out="$1"
[[ ! -e "$out" ]] || { echo 'Evidence path already exists' >&2; exit 2; }
root="$(git rev-parse --show-toplevel)" || exit 2
cd "$root"
preflight=contract-000/gpt/business/f001_preflight_536.sh
custody=contract-000/gpt/business/f001_custody_manifest_530.sh
[[ -f "$preflight" && -f "$custody" ]] || { echo 'Missing required scripts' >&2; exit 4; }
# Capture preflight output in memory so failure cannot accidentally execute the regression.
# Run BEFORE creating evidence files, to avoid contaminating the clean-checkout check.
set +e
preflight_output="$(bash "$preflight" 2>&1)"
preflight_rc=$?
set -e
if [[ "$preflight_rc" -ne 0 ]] || ! grep -Fxq 'F001_PREFLIGHT=READY_FOR_SEPARATE_PREREGISTERED_TEST' <<< "$preflight_output"; then
  printf '%s\n' "$preflight_output" >&2
  printf 'F001_ORCHESTRATOR=HOLD preflight_rc=%s; regression NOT RUN\n' "$preflight_rc" >&2
  exit 10
fi
# Custody creates a new mode-700 evidence directory and records regression output.
# The evidence directory MUST be outside the checkout, otherwise an untracked-file
# race can contaminate the checkout after preflight. Reject in-tree paths.
case "$out/" in "$root/"*) echo 'Evidence directory must be outside Git checkout' >&2; exit 11;; esac
# Store preflight output only after custody has created its directory; if custody
# fails before creation, the preflight text remains in the console.
set +e
bash "$custody" "$out"
custody_rc=$?
set -e
if [[ -d "$out" ]]; then
  printf '%s\n' "$preflight_output" > "$out/preflight.log"
  printf '%s\n' "$preflight_rc" > "$out/preflight-exit-status.txt"
  printf '%s\n' "$custody_rc" > "$out/custody-exit-status.txt"
  (cd "$out" && sha256sum environment.txt raw.log exit-status.txt preflight.log preflight-exit-status.txt custody-exit-status.txt > SHA256SUMS && sha256sum SHA256SUMS > MANIFEST-DIGEST.txt) || {
    echo 'F001_ORCHESTRATOR=HOLD incomplete evidence manifest' >&2; exit 12;
  }
fi
echo "F001_ORCHESTRATOR_CUSTODY_EXIT=$custody_rc"
echo 'All observations and failures must be posted in the pre-test Issue #197 thread.'
exit "$custody_rc"
