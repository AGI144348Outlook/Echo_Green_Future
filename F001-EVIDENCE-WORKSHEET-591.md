# F-001 evidence reconciliation worksheet — Run591
Status: PREPARATION ONLY; no tests executed, no observed results entered.

Project: F-001 TAM Protocol ebook. This worksheet does not replace frozen preregistrations in Issues #258, #262, #256, #229.

## Per-case ledger schema
`case_id | preregistration_url | fixture_git_blob | harness_git_blob | runner_git_blob | expected | observed | assertions_passed | assertions_total | outcome(PASS/FAIL/ERROR/NOT_RUN) | evidence_artifact_sha256 | limitations`

## Empty reconciliation rows
| Experiment | Required case count | Recorded | Passed | Failed | Error | Not run | Evidence |
|---|---:|---:|---:|---:|---:|---:|---|
| #258 six-case | 6 | 0 | 0 | 0 | 0 | 6 | NOT_RUN |
| #262 runner checks | 6 | 0 | 0 | 0 | 0 | 6 | NOT_RUN |
| #256 v577 | derive from frozen issue | 0 | 0 | 0 | 0 | unknown | NOT_RUN |
| #229 fifteen-case | 15 | 0 | 0 | 0 | 0 | 15 | NOT_RUN |

These are administrative placeholders, not claims about actual CI status. Before populating, read the exact issue body and source object hashes; do not assume six runner checks equal six executable test cases.

## Acceptance gates
- Every frozen declared case has exactly one terminal case record; reruns use separate attempt IDs and never overwrite evidence.
- Count consistency: declared = PASS + FAIL + ERROR + NOT_RUN, and each PASS requires all its assertions to pass.
- A successful wrapper exit alone does not count as product verification.
- Record observed values, stderr, source fingerprints and immutable output hash in the original issue thread.
- Claude editorial lane: provenance, quotation permissions, accuracy. GPT technical lane: reproducible test evidence and packaging readiness.
- PDF/EPUB and Android reader checks remain incomplete. Publication requires Timothy's explicit authorization and A1–A6 decisions.

## Next action
Obtain byte-verified source objects, read the original preregistrations, then execute without changing frozen fixtures; report observed results in the SAME issue. No tests should run before a published pre-test record.
