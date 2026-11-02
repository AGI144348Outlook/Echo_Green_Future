#!/usr/bin/env bash
# F-001 Run527: evidence-counted wrapper for frozen nine-case Run524 replay.
# PREPARATION ONLY. Test preregistration: Issue #197. Do not run without same-thread reporting access.
set -euo pipefail
command -v python3 >/dev/null || { echo "python3 required for independent output audit" >&2; exit 2; }
root="$(git rev-parse --show-toplevel)"
cd "$root"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
# Preserve complete raw output and process exit status even if the replay fails.
set +e
bash contract-000/gpt/business/f001_exact_source_nine_case_524.sh >"$tmp/raw.log" 2>&1
replay_status=$?
set -e
cat "$tmp/raw.log"
printf 'RUN527_REPLAY_EXIT=%s\n' "$replay_status"
python3 - "$tmp/raw.log" "$replay_status" <<'PY'
import json, pathlib, sys
lines=pathlib.Path(sys.argv[1]).read_text(errors='replace').splitlines()
status=int(sys.argv[2])
original=[
 'matching bytes require human review and HOLD',
 'wrong digest rejects and holds',
 'missing file rejects and holds',
 'traversal rejects and holds',
 'close fault after match rejects without throwing',
 'close fault after mismatch retains earlier reason']
supplement=[
 'final-component symlink refuses and holds',
 'intermediate-directory symlink refuses and holds',
 'oversized regular file refuses and holds']
passes=[line[5:] for line in lines if line.startswith('PASS ')]
failures=[line for line in lines if line.startswith('FAIL ')]
summaries=[]
for line in lines:
 try:
  obj=json.loads(line)
  if isinstance(obj,dict) and 'planned' in obj: summaries.append(obj)
 except json.JSONDecodeError: pass
sources=[line for line in lines if line.startswith('SOURCE ')]
exits=[line for line in lines if line.startswith('EXIT original=')]
expected=original+supplement
valid=(status==0 and passes==expected and not failures and len(summaries)==2
 and summaries[0].get('planned')==6 and summaries[0].get('failures')==0
 and summaries[1].get('planned')==3 and summaries[1].get('pass')==3
 and summaries[1].get('fail')==0 and len(sources)==3 and len(exits)==1
 and exits[0]=='EXIT original=0 supplemental=0')
print('RUN527_AUDIT='+('PASS' if valid else 'FAIL_OR_INCONCLUSIVE'))
print('RUN527_COUNTS='+json.dumps({'pass_lines':len(passes),'fail_lines':len(failures),'summaries':len(summaries),'sources':len(sources),'exit_lines':len(exits)}))
if not valid:
 print('RUN527_LIMITATION=Original stdout/stderr shown above; no inference of successful nine-case replay.')
sys.exit(0 if valid else 1)
PY
# Operator must copy complete raw output into existing Issue #197; do not claim execution without that post.
