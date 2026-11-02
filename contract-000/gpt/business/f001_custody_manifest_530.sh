#!/usr/bin/env bash
# F-001: offline evidence custody entrypoint. PREPARATION ONLY; preregistered Issue #197.
# Usage: bash contract-000/gpt/business/f001_custody_manifest_530.sh /absolute/evidence/directory
# Run only when Issue #197 is writable and same-thread actual-results follow-up is possible.
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "Usage: $0 /absolute/new/evidence/directory" >&2; exit 2; fi
case "$1" in /*) ;; *) echo "Evidence path must be absolute" >&2; exit 2;; esac
out="$1"
if [ -e "$out" ]; then echo "Refusing existing evidence path" >&2; exit 2; fi
command -v git >/dev/null
command -v sha256sum >/dev/null
command -v python3 >/dev/null
root="$(git rev-parse --show-toplevel)"
cd "$root"
mkdir -m 700 "$out"
# Do not store secrets, manuscript text, or private user data in this public evidence package.
{
  printf 'utc='; date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'commit='; git rev-parse HEAD
  printf 'branch='; git branch --show-current
  printf 'dirty='; if [ -z "$(git status --porcelain)" ]; then echo false; else echo true; fi
  printf 'os='; uname -a
  printf 'bash='; bash --version | head -n 1
  printf 'python='; python3 --version
  printf 'node='; if command -v node >/dev/null; then node --version; else echo unavailable; fi
  printf 'timeout='; if command -v timeout >/dev/null; then timeout --version | head -n 1; else echo unavailable; fi
} >"$out/environment.txt"
set +e
bash contract-000/gpt/business/f001_nine_case_audited_527.sh >"$out/raw.log" 2>&1
rc=$?
set -e
printf '%s\n' "$rc" >"$out/exit-status.txt"
# The runner's own audit is part of acceptance; missing audit is inconclusive.
if ! grep -Fxq 'RUN527_AUDIT=PASS' "$out/raw.log"; then rc=1; fi
(
  cd "$out"
  sha256sum environment.txt raw.log exit-status.txt >SHA256SUMS
  sha256sum SHA256SUMS >MANIFEST-DIGEST.txt
)
echo "Evidence directory: $out"
echo "Audit status: $rc (0=audited pass; 1=fail/inconclusive)"
cat "$out/MANIFEST-DIGEST.txt"
echo "Post the digest and complete observed results to pre-test Issue #197; a local checksum is not an independent trust anchor."
exit "$rc"
