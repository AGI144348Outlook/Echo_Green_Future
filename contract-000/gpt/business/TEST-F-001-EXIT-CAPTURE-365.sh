#!/bin/sh
set -eu
wrapper=$1
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
export TMPDIR="$work"
pass_output=$("$wrapper" sh -c 'printf success; printf note >&2; exit 0')
pass_dir=$(printf '%s\n' "$pass_output" | sed -n 's/^evidence_dir=//p')
[ "$(cat "$pass_dir/session.exit")" = 0 ]
[ "$(cat "$pass_dir/session.stdout")" = success ]
[ "$(cat "$pass_dir/session.stderr")" = note ]
printf 'P1: PASS success retains streams and exit=0\n'
set +e
fail_output=$("$wrapper" sh -c 'printf partial; printf failure >&2; exit 23')
fail_status=$?
set -e
fail_dir=$(printf '%s\n' "$fail_output" | sed -n 's/^evidence_dir=//p')
[ "$fail_status" = 23 ]
[ "$(cat "$fail_dir/session.exit")" = 23 ]
[ "$(cat "$fail_dir/session.stdout")" = partial ]
[ "$(cat "$fail_dir/session.stderr")" = failure ]
printf 'P2: PASS failure retains streams and exit=23\n'
set +e
"$wrapper" >/dev/null 2>"$work/usage.stderr"
usage_status=$?
set -e
[ "$usage_status" = 64 ]
printf 'P3: PASS no-argument invocation rejects exit=64\n'
[ "$(stat -c %a "$pass_dir")" = 700 ]
[ "$(stat -c %a "$pass_dir/session.stdout")" = 600 ]
printf 'P4: PASS private directory and output mode\n'
