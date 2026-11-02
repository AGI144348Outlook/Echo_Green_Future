#!/usr/bin/env bash
# F-001 Run544 evidence-first orchestration candidate. UNTESTED; do not use as release evidence.
# Requires prospective amendment to Issue #220 before any test execution.
set -euo pipefail
[[ "$#" -eq 1 && "$1" = /* ]] || { echo 'Usage: script /absolute/new/evidence/directory' >&2; exit 2; }
out="$1"
[[ ! -e "$out" && ! -L "$out" ]] || { echo 'HOLD: destination exists' >&2; exit 2; }
root="$(git rev-parse --show-toplevel)" || exit 2
command -v python3 >/dev/null && command -v sha256sum >/dev/null || { echo 'HOLD: missing evidence dependencies' >&2; exit 4; }
# Not race-free against concurrent replacement of ancestor symlinks.
python3 - "$root" "$out" <<'PY'
import os,sys
root=os.path.realpath(sys.argv[1]); out=os.path.realpath(sys.argv[2])
if os.path.commonpath((root,out)) == root:
    raise SystemExit('HOLD: destination inside checkout')
PY
umask 077
mkdir -m 700 -- "$out" || exit 4
cd "$root"
preflight=contract-000/gpt/business/f001_preflight_536.sh
custody=contract-000/gpt/business/f001_custody_manifest_530.sh
printf '%s\n' 'F-001 Run544 candidate; NOT RELEASE EVIDENCE' > "$out/README.txt"
printf '%s\n' "$root" > "$out/checkout-path.txt"
git rev-parse HEAD > "$out/checkout-head.txt" 2>&1 || true
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$out/start-utc.txt"
status=HOLD
finish() {
  local rc="$1"
  printf '%s\n' "$status" > "$out/verdict.txt"
  printf '%s\n' "$rc" > "$out/orchestrator-exit-status.txt"
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "$out/end-utc.txt"
  (cd "$out" && find . -maxdepth 1 -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 -r sha256sum > SHA256SUMS) || true
}
trap 'finish "$?"' EXIT
if [[ ! -f "$preflight" || ! -f "$custody" ]]; then
  echo 'HOLD: missing prerequisite script' > "$out/error.txt"
  exit 4
fi
set +e
bash "$preflight" > "$out/preflight.stdout" 2> "$out/preflight.stderr"
preflight_rc=$?
set -e
printf '%s\n' "$preflight_rc" > "$out/preflight-exit-status.txt"
if [[ "$preflight_rc" -ne 0 ]] || ! grep -Fxq 'F001_PREFLIGHT=READY_FOR_SEPARATE_PREREGISTERED_TEST' "$out/preflight.stdout"; then
  echo 'HOLD: preflight failed; custody not invoked' > "$out/error.txt"
  exit 10
fi
# Existing custody wrapper requires a new destination; preserve this run's
# evidence directory and put custody outputs in a separate child directory.
set +e
bash "$custody" "$out/custody" > "$out/custody.stdout" 2> "$out/custody.stderr"
custody_rc=$?
set -e
printf '%s\n' "$custody_rc" > "$out/custody-exit-status.txt"
if [[ "$custody_rc" -ne 0 ]]; then
  echo 'HOLD: custody failed' > "$out/error.txt"
  exit "$custody_rc"
fi
for required in environment.txt raw.log exit-status.txt; do
  if [[ ! -f "$out/custody/$required" ]]; then
    echo "HOLD: missing custody artifact $required" > "$out/error.txt"
    exit 12
  fi
done
status=EXECUTION_EVIDENCE_CAPTURED_RELEASE_HOLD
echo 'Release remains HOLD pending editorial, rights, accessibility, Android QA, Timothy authorization.'
