#!/bin/sh
# F-001 HOLD-only evidence capture wrapper. Does not interpret or authorize release.
set -eu
if [ "$#" -lt 1 ]; then
  printf '%s\n' 'usage: F-001-EXIT-CAPTURE-365.sh <pinned-session-command> [arguments...]' >&2
  exit 64
fi
umask 077
# Only run in a trusted local execution environment with a trusted TMPDIR.
evidence_dir=$(mktemp -d "${TMPDIR:-/tmp}/f001-hold-evidence.XXXXXXXX")
if "$@" >"$evidence_dir/session.stdout" 2>"$evidence_dir/session.stderr"; then
  session_status=0
else
  session_status=$?
fi
printf '%s\n' "$session_status" >"$evidence_dir/session.exit"
printf 'evidence_dir=%s\nsession_exit=%s\n' "$evidence_dir" "$session_status"
# Preserve the true session exit status. A HOLD receipt never permits release.
exit "$session_status"
