#!/usr/bin/env bash
# F-001 Run541: hardened preflight/custody preparation; NOT TESTED.
# Test only after a prospective issue entry and ability to report results.
set -euo pipefail
[[ "$#" -eq 1 && "$1" = /* ]] || { echo 'Usage: script /absolute/new/evidence/directory' >&2; exit 2; }
out="$1"
[[ ! -e "$out" && ! -L "$out" ]] || { echo 'Evidence destination exists (including symlink)' >&2; exit 2; }
root="$(git rev-parse --show-toplevel)" || exit 2
cd "$root"
preflight=contract-000/gpt/business/f001_preflight_536.sh
custody=contract-000/gpt/business/f001_custody_manifest_530.sh
[[ -f "$preflight" && -f "$custody" ]] || { echo 'Missing prerequisite scripts' >&2; exit 4; }
command -v python3 >/dev/null || { echo 'Missing python3' >&2; exit 4; }
# Resolve symlinked ancestors before checking checkout containment.
# A lexical prefix check misses paths through a symlink outside the checkout.
if ! python3 - "$root" "$out" <<'PY'
import os,sys
root=os.path.realpath(sys.argv[1])
out=os.path.realpath(sys.argv[2])
if os.path.commonpath((root,out))==root:
    sys.exit(1)
PY
then echo 'Evidence destination resolves inside checkout' >&2; exit 11; fi
set +e
preflight_output="$(bash "$preflight" 2>&1)"
preflight_rc=$?
set -e
if [[ "$preflight_rc" -ne 0 ]] || ! grep -Fxq 'F001_PREFLIGHT=READY_FOR_SEPARATE_PREREGISTERED_TEST' <<< "$preflight_output"; then
  printf '%s\n' "$preflight_output" >&2
  printf 'F001_ORCHESTRATOR=HOLD preflight_rc=%s; regression NOT RUN\n' "$preflight_rc" >&2
  exit 10
fi
# This path validation is not race-free: a parent symlink could change later.
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
printf 'F001_ORCHESTRATOR_CUSTODY_EXIT=%s\n' "$custody_rc"
echo 'Report actual results and limitations in the prospectively registered test issue.'
exit "$custody_rc"
