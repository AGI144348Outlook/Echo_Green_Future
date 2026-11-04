# F-001 — Verification evidence contract v0.1 (draft, NOT TESTED)

Project: F-001 TAM Protocol ebook. Status: HOLD. This document is a *schema proposal*, not test evidence or release approval.

## Distinct outcomes
- `runner_exit`: exit status of the wrapper process, nullable on launch failure.
- `harness_exit`: exit status of the invoked test harness, nullable on timeout/launch failure.
- `assertions_total` / `assertions_passed`: integer counts only if the harness emits a documented, parseable summary; otherwise null. Never infer from exit status.
- `gate_blob`, `harness_blob`, `runner_blob`: Git blob IDs, checked against the actual bytes before execution.
- `fixture_manifest_sha256`: hash of a canonical manifest listing fixture names and SHA-256 byte hashes; null until the fixture set is defined.
- `stdout_sha256`, `stderr_sha256`: SHA-256 of the captured *raw bytes*; store whether output was truncated.
- `git_repository_identity`: declared origin/worktree identity, separate from verified blob identity; do not assume a remote origin proves trust.
- `pretest_issue`, `observations_issue`: same GitHub thread, verified before and after execution.
- `utc_started`, `utc_finished`, `python_version`, `argv`, `timeout_seconds`, `timed_out`: reproducibility metadata.
- `interpretation`: separately authored post-test narrative, never auto-populated as PASS.

## Acceptance
1. Every executed case has a pre-existing, source-pinned Issue/Discussion entry; prospective changes receive a new entry before execution.
2. Raw observations and human interpretation appear in that same thread.
3. No absent assertion count is reported as zero or inferred as a pass.
4. Nonzero, timeout, missing-object, and malformed-evidence paths are documented, with no silent success.
5. A verifier pass is *not* an ebook release approval: editorial provenance, quotation rights, accessible EPUB/PDF, Android QA, and Timothy A1–A6 remain separate gates.

## Next action
Implement this schema as a **new** runner revision without altering pinned v583 or its frozen pre-test #262. Preregister exact runner blob and synthetic fixture cases before any execution. Then run v583's already-registered checks if byte-verified local Git objects become available; post observations to #262. No tests were executed in preparing this document.

## Claude complement
Claude: review the ebook's sentence-level claims, historical accuracy, quotation permissions and rights provenance; report uncertainties as unresolved rather than asserting release readiness.
