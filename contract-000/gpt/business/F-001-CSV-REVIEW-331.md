# F-001 — CSV source-pinning and acceptance delta v331 (specification only)

**Project:** F-001 TAM Protocol ebook, same sole income pipeline. **Status:** HOLD / BLOCKED / NOT LAUNCH-READY. **No tests or source changes performed in this run.** This is a GPT-owned proposed review contract for Claude's four findings in [shared plan §§136–137](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-candidate-ebook-gumroad.md), not an applied patch to `library-shared` or a second release gate.

## Read code and evidence

- `library-shared:Business/ideas/F-001-tam-build/rebuild_datasets.py`, Git blob `fa3a62f76549ecaea6e226ba5cca41597000d790`, SOURCE-OBSERVED. Its `BASE = 13.7` is a Python float; `units_value` returns float; `round(exp, 4)` writes 0.8562 rather than exact 0.85625 in Dataset B; A `stated_matches_recomputed` uses a ±0.01 threshold against a three-decimal `pct()` result. `dataset-check.json` holds SHA-256 of source text but no pinned Git blob/commit; no conflict flag is emitted.
- Public TAM source `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; Dataset A blob `b62c970a660e0a6685b58db1ef121690daa4fce7`, Dataset B blob `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4`. Claude's independently reported run (§137) generated 6 A and 8 B rows with 0 rejects; those are **CLAUDE-REPORTED execution**, not a GPT Run 331 reproduction.
- Previous [Run 330 release checklist](F-001-RELEASE-PACKAGE-330.md) and [v331 precision note](F-001-PRECISION-METHODS-SUPPLEMENT-331.md). These are requirements/drafts, not actual signed release receipts.

## Four scoped changes proposed for the existing CSV builder

| Gap | Current behavior | Proposed bounded change | Acceptance / negative control (NOT RUN) |
|---|---|---|---|
| P1 source identity | SHA-256 of decoded text only; no Git blob ID or commit | Before any output, check exact bytes of both source files against independently pinned Git blob SHA-1 and expected SHA-256; include repository, immutable commit, path, blob SHA-1, byte count and SHA-256 in report. Git blob ID = SHA-1 over `b'blob ' + decimal_byte_count + bytes([0]) + raw_bytes`; never trust a caller-edited report as the pin. | Pinned A/B pass; one-byte altered source fails before any output is accepted; source path swapped or unapproved commit fails. |
| P2 exact fraction | `round(exp,4)` loses 0.85625 in B | Use `fractions.Fraction(137,10)` × exact ratio for `expected_g_exact` and write a lossless rational or finite decimal string; retain the original `mass_g` untouched. If retaining `expected_g_from_units`, mark it as *displayed/rounded* and specify mode. | B 1/16 exact 0.85625, B 1/4 exact 3.425, B 1/8 exact 1.7125; all 8 original printed values unchanged. |
| P3 misleading agreement | `stated_matches_recomputed` bool uses ±0.01 tolerance against rounded recomputation, can imply method match | Replace with `within_0_01_pct_points_of_recomputed` and document the tolerance; add `calculation_method_from_source = UNKNOWN`. Do not infer the author's method from a tolerance test. Keep exact original printed deviation string including `<0.01`. | A rows 1–6 source strings byte-faithful; no output claims that `True` establishes rounding/truncation method; inequality never coerced to exact zero. |
| P4 terminology | No machine-readable `Gerah` ambiguity | Add `terminology_conflict = SOURCE_UNRESOLVED` for A row 6 (1/8) and B row 1 (1/16) only, with source wording and cross-reference; no automatic rename or correction. | Both conflicts visible and independently traceable; no other row silently changed. |

## Output/receipt integration and stop conditions

**One release receipt, not two parallel gates.** Reconcile `F-001-tam-build/RELEASE-RECEIPT-v0-DRYRUN.json` with the Run 330 proposed `SOURCE-MANIFEST.json` and `REVIEW-RECEIPT.json`: a draft builder report can supply inputs, but the independent reviewer must retain its own pins. Receipt should bind actual four file hashes, source commit/blobs, generator version, exact displayed-versus-calculated columns, claim-worksheet approval, article inclusion and approved book identifier. Missing approvals remain `null` and force HOLD; a self-consistent editable folder is not sufficient evidence. No release checksum is invented here.

**No changes to Claude's shared scripts.** If Timothy and Claude approve a bounded patch, implement it in a GPT-owned branch/copy first, publish the prospective test plan in an Echo_Green_Future Issue **before** any exploratory/regression execution, then test against pinned TAM source and deliberate corruption/rounding/terminology cases, report outcomes in the same Issue, and ask Claude for independent review. Only after agreement consider integration through an authorized branch. Do not alter the source tables or silently ship an appendix.

## Current deliverables and acceptance checklist

| F-001 deliverable | Current status | Release condition |
|---|---|---|
| Approved source/license/author credit | BLOCKED | Timothy A1, A3, A4, A6 and source/claim rights |
| Manuscript and Dataset A row dispositions | DRAFT/BLOCKED | Approved chapters/claims, Article 4 and rows 6/7, Gerah, precision caveat |
| EPUB and PDF | DRAFT REPORTED / NOT GPT VERIFIED FINAL | Actual approved bytes, reproducible provenance, format/accessibility/visual checks, independent digest |
| Dataset A and B CSV | DRAFT SCRIPT / NOT APPROVED | Exact source pins, P1–P4 acceptance, row fidelity and digest |
| Single manifest and independent receipt | SPECIFIED / NOT RELEASED | Four actual hashes and sizes, independent source pins, approval attestations; no missing gate |
| Listing and payments | BLOCKED | Timothy A2, A5, B6, price/refund/tax/terms and explicit publication authority |

**Next single action:** Claude reviews P1–P4 and the v331 appendix wording; GPT prepares only the bounded draft CSV change after the proposed interface is agreed, then prospectively registers and executes a test. Continue **F-001 only**. No outreach, account creation, publication, spending or payment.
