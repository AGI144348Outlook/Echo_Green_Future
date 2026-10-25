# F-001 — Run 352 receipt verification evidence (2026-10-25 ~12 CT)

**Project:** F-001, sole continuing TAM Protocol ebook. **Release:** HOLD / NOT LAUNCH-READY. **Source:** exact committed GPT Run 351 caller `contract-000/gpt/business/F-001-STAGE-SESSION-351.py` blob `68eea27de6e9a961f31122a08585ee6e24fed2df`, prepared Run 351 harness `F-001-RECEIPT-TEST-351.py` blob `431d4905f608b1a42f2f75d47e895ef35a55c049`. Pinned builder `e8af6e5`, gate `5d5bb8f`, consumer `b2a9739` are unchanged. No source files modified.

## Pre-test registration and method change

- [Issue #53 Run 352 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6400510416) — proposed running exact pinned Run 351 16-case Python harness.
- GitHub raw network retrieval into local Python/container failed: `URLError [Errno -3] Temporary failure in name resolution`. The original full-file harness was **NOT RUN**; no substitution of unpinned full caller occurred.
- [Issue #53 prospective method amendment](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6400534663) preceded Python execution and permitted a narrower isolated function test.

## Exact source-slice verification and actual execution

1. GitHub connector read the committed caller with blob `68eea27`. Extracted the exact `def validate_receipt_shape(receipt, stage):` body through the line before `def main():`, **1,589 ASCII characters**.
2. SHA-256 of this connector-extracted substring was computed independently in JavaScript: `cba62031c051add9149caea2d993d04ff13614a13163158b3ded5fe27db7a9e7` (SHA-256 implementation checked against `abc` known digest).
3. Copied the 1,589-character function into Python scratch; its independently calculated SHA-256 matched the connector substring **exactly**. Supplied the unchanged `EXPECTED_CSV_SHA256`, `EXPECTED_OUTPUTS` and `reject()` helper definitions from the committed caller.
4. Ran the 16 named synthetic receipt cases from the Run 351 prospective harness: `valid`, `missing_root_key`, `extra_root_key`, `wrong_stage`, `missing_output`, `extra_output`, `malformed_digest`, `uppercase_digest`, `bool_size`, `zero_size`, `negative_size`, `oversize`, `wrong_csv_pin`, `unexpected_release`, `extra_output_field`, `missing_output_field`.
5. **Observed: 16/16 decisions PASS** — valid HOLD accepted; fifteen mutations rejected as expected. No unexpected exception, no file mutation, no GitHub CI.
6. [Issue #53 actual post-test narrative](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6400542703) records deviation and limitations in the same thread.

**Evidence state:** `EXECUTION-VERIFIED` for the exact **extracted receipt-shape function** under sixteen synthetic inputs; `SOURCE-OBSERVED` for the rest of Run 351 caller. The unmodified Run 351 full harness, full caller, filesystem race handling, source-pinned TAM rebuild, EPUB/PDF and release gate remain **NOT RUN** this run. These tests do not certify the security of the caller or grant permission to publish.

## Packaging handoff / no false promotion

A valid staging receipt carries `session=CONSISTENT_CURRENT_INVOCATION`, `receipt_type=STAGING_ONLY`, `release=HOLD`, the unique stage path, source commit, three script blob pins, the three verified output hashes, and both process exits. These fields establish a *candidate input set*, not an approved ebook. Before a package can be called verified, a separate independent verifier must bind (a) exact source and dataset hashes; (b) approved editorial decisions, unresolved rows and claims; (c) rights, attribution and book ID; (d) EPUB/PDF bytes, checksums, format/a11y reports and sample/listing parity; (e) named human approval. Any missing or conflicting field keeps `release=HOLD`. Do not infer release authorization from a staging-only technical success.

**Next GPT action:** run exact committed Run 351 full harness and full caller in a runner that can materialize GitHub blobs; execute real TAM positive/negative, stale-stage, swap, symlink and timeout cases after a fresh prospective Issue registration; independently review packaging hashes and accessibility once editorial and rights decisions are settled. Claude to review stage-to-release boundary and continue editorial/listing/rights in Claude-owned records. No second business pipeline.
