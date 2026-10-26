# F-001 TAM Protocol ebook — pinned, read-only claim-gap crosswalk (Run 379)

**Project continuity:** F-001 only, **HOLD / NOT LAUNCH-READY**. Based on [shared F-001 decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md), [shared Python claim scanner](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-tam-build/claim_scan.py) blob `31f3dcff`, [Run377 source-binding checker](f001_claims_binding_377.py), [Run378 45-candidate inventory](F-001-REAL-CLAIMS-378.md), and [Issue #56 prospective PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6425998064).

## Deliverable

[Read-only opt-in executable crosswalk](f001_claim_gap_audit_379.js) checks the eight public TAM source files pinned to `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. It fails closed on missing or changed Git blob identities, preserves the four original scanner triggers, adds `demonstrating` to the certainty pattern and optional literal backslash before percentage signs. It prints a JSON candidate report; it **does not edit the source, shared Python scanner, or any editorial status**. Usage in a Node environment: `node f001_claim_gap_audit_379.js --self-test` or `node f001_claim_gap_audit_379.js <pinned-source-dir>` (not run under Node during this run).

## Prospective test and actual observations

- **8/8 public source Git blob identities** matched the pinned tree; tree not truncated. Source blobs: README `213bcfaf`, Article 1 `237bd333`, Article 2 `ec657c3f`, Color/Dental `b525ad60`, Article 5 `c8c1bf61`, Article 6 `662d745f`, Article 10 `e82be564`, Collective `710ad3cd`.
- Evaluated the *exact committed JavaScript source* as a module in an isolated V8 function with `require.main=null` (no filesystem, Node CLI or network inside that module), and invoked its pure `selfTest()`: **14/14 synthetic cases passed**.
- Applied the same committed `scanText()` to the eight retrieved source strings: **42 baseline candidate sentences, 45 extended, 0 baseline losses**, three supplemental candidates at `README.md:8` (`demonstrating`), `The Color Dyed and Dental Records:14` (escaped percent) and `Collective information:90` (escaped percent). Re-fetched the committed JS Git blob `7a005dcfe9231073317af4e8d961d7dfcb04b473` and reproduced 14/14 and 42→45 on pinned source.
- Earlier first draft of the in-memory script failed at JavaScript evaluation with a SyntaxError (hashbang/escaping construction); it was **not executed or committed**. The corrected source evaluated, passed controls and was committed. This is a recorded harness-development failure, not a hidden PASS.

## Interpretation, limitations and handoff

This corroborates Run378's JS-translated claim inventory and packages a reproducible *opt-in* audit. It does not prove the historical claims, completeness of the editorial review queue, Python regex parity, false-positive/false-negative rates, the final manuscript, or release readiness. The original Python `claim_scan.py`, Run377 Python binder, full Run334→344→347→351 stage, EPUBCheck/Ace, final PDF/EPUB, and Node CLI were **not executed** here. Git blob SHA is source provenance, not editorial truth or a release signature.

**Next GPT:** run the original Python claim scanner and binder against exact pinned source, reconcile Unicode boundary behavior, then verify manuscript claims and package hashes. **Next Claude:** independently adjudicate the three supplemental candidates, Article 4, rights/licensing and precision/Gerah questions; preserve own files. **Timothy:** A1–A6, B1/B4/B6, C1, measurement precision, and explicit publication authority remain open. No account, outreach, spending, payment, publication, CI, paid inference or autonomous Cloudflare loop.
