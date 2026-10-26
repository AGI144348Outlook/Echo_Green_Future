# F-001 — HOLD-only evidence capture addendum (GPT Run 365, 2026-10-26 ~01 CT)

**Single continuing product:** F-001 TAM Protocol ebook. **HOLD / NOT LAUNCH-READY.** This addendum supplements [Run 364's pinned source and stage handoff](F-001-REAL-STAGE-HANDOFF-364.md), and **does not claim** a real TAM staging execution.

## Observed operator-evidence defect

Run 364's example begins `set -eu` and invokes the coordinator as a plain command with stdout/stderr redirection. When that command exits nonzero (a meaningful fail-closed result), `set -e` can terminate the recipe before its operator can capture and report the exit status and preserved diagnostics. The output files may exist, but the example does not guarantee a structured exit record. The underlying coordinator's nonzero status must **not** be converted into success.

## Bounded correction

Use the GPT-owned [evidence capture wrapper](F-001-EXIT-CAPTURE-365.sh) with the **same pinned** Run 334 builder, 344 gate, 347 consumer and 351 coordinator. It creates a private `mktemp -d` directory, captures both streams and the **actual exit status** in `session.stdout`, `session.stderr`, `session.exit`, prints the evidence directory, then exits with the exact command status. It never interprets `HOLD` as approval, modifies the TAM source, or publishes anything.

**Operator fragment — UNEXECUTED on real TAM source:**

```sh
# Follow Run 364 source checkout and exact blob checks first.
# BASE, SRC, ROOT, BUILDER, GATE, CONSUMER, SESSION as in Run 364.
CAPTURE="$BASE/F-001-EXIT-CAPTURE-365.sh"
# Use a trusted, private local TMPDIR. All referenced paths should be absolute.
if capture_report=$(sh "$CAPTURE" python3 -I -B "$SESSION" \
    --source "$SRC" --builder "$BUILDER" --root "$ROOT" \
    --gate "$GATE" --consumer "$CONSUMER"); then
    session_rc=0
else
    session_rc=$?
fi
printf '%s\n' "$capture_report"
printf 'observed_session_rc=%s\n' "$session_rc"
# Inspect the printed evidence_dir, session.exit, session.stdout and session.stderr.
# Scrub paths and sensitive local information before any public issue comment.
# A nonzero status remains a failed stage; never re-pin or overwrite to force success.
```

**Limitations:** the wrapper does not authenticate the command it is given, protect against hostile `TMPDIR`/filesystem mutation, impose output-file quotas, validate the final receipt, or authorize publication. Those properties depend on the pinned scripts, isolated trusted operator environment, independent review and Timothy's approval. No credentials/private figures belong in public GitHub logs.

## Prospective record and actual bounded tests

[Run 365 PRE in Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6409402026) was posted **before** local execution. Local test command: `sh TEST-F-001-EXIT-CAPTURE-365.sh /tmp/F-001-EXIT-CAPTURE-365.sh` with the exact wrapper bytes copied into a disposable local file. **Observed: 4/4 shell assertions PASS:** successful command retains stdout/stderr/exit 0; deliberately failing command exits 23 and retains both streams and exit 23; missing command rejects with exit 64; evidence directory mode 700 and captured file mode 600. Remote Git blobs verified byte-identical to locally tested files: wrapper `91626cef39188358ba72772d75b4bd33e2d59fd9`, harness `ca6f3463043a0b8f013d5deaa46781cd58d86023`. These are **synthetic shell tests only**, not real stage/receipt or EPUB/PDF checks.

**Network blocker:** read-only `git ls-remote https://github.com/AGI144348Outlook/The-TAM-protocol.git HEAD` returned `Could not resolve host: github.com`, exit **128** in the execution container. The GitHub connector can read the public source, but this does not provide a verified local Git checkout at the pinned TAM commit. **Real Run 334→344→347→351, tamper negative, EPUB/PDF, CI NOT RUN.**

**Next action:** after local GitHub DNS is restored, post a new prospective Issue entry, perform the exact Run 364 source-pin checkout, use this wrapper around the pinned HOLD session, inspect exit/receipt/hash evidence and separately test a disposable altered-input negative. If failed, retain failure evidence; do not quietly replace it with a fresh success. Claude: independent rights/editorial/claims/accessibility/listing review, without modifying GPT artifacts. Timothy: A1–A6, B6, C1 and publication authorization remain unresolved.
