#!/usr/bin/env bash
# F-001 Run528: retain exact raw evidence for the preregistered nine-case replay.
# PREPARATION ONLY. Before execution verify same-thread Issue #197 write access.
set -uo pipefail
if [[ $# -ne 1 || "${1:-}" != /* ]]; then
  echo "usage: bash $0 /absolute/path/to/new-evidence-directory" >&2; exit 2
fi
dest="$1"
if ! mkdir "$dest" 2>/dev/null; then
  echo "REFUSE: destination must be new and writable: $dest" >&2; exit 2
fi
root="$(git rev-parse --show-toplevel)" || exit 2
cd "$root" || exit 2
set +e
bash contract-000/gpt/business/f001_nine_case_audited_527.sh >"$dest/raw.log" 2>&1
status=$?
set -e
printf 'audited_wrapper_exit=%s\n' "$status" >"$dest/exit-status.txt"
(
 cd "$dest" || exit 2
 sha256sum raw.log exit-status.txt >SHA256SUMS
)
cat "$dest/raw.log"
printf 'RUN528_CUSTODY_DIR=%s\nRUN528_EXIT=%s\n' "$dest" "$status"
echo "Post unedited observations, exit status, checksums, and limitations to existing Issue #197."
exit "$status"
