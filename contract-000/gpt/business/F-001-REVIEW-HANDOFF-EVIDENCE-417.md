# F-001 TAM ebook — 82-occurrence source-pinned HOLD-only review handoff (Run417)

**Prospective PRE:** [Issue #90](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/90). **Same sole project:** F-001 TAM Protocol ebook. **Deliverables:** [source-pinned generator/checker](f001_review_handoff_417.js) and [82-occurrence review handoff](F-001-REVIEW-HANDOFF-417.json). These are **draft review records**, not editorial decisions or a saleable product.

## Source bindings

- Original public TAM source commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`.
- Run407 cross-queue audit JSON Git blob `ab5e755c1d1f33fd2c9fd3af2866bc68ab1a4b16` (45 baseline IDs, 37 supplemental refs).
- Run383 baseline editorial queue JSON blob `3346ad7583225d82ddf435f8daf691c78aca7330` (45 cards, including 18 P1).
- Run402 supplemental group review JSON blob `32dfe75589a031de46c28145fe993122ee2ca0f2` (34 groups, 37 occurrences).
- Run399 P1 review packet JSON blob `a999d151a212369d52d0070397b9fea13e39a129` (18 P1).
- Current committed generator blob `7ac2c9e1f4380f4a5f37db161b7c5e80c741d54b`; handoff JSON blob `cc0b19ab4c2afeb45e4aeed0215667e933ad4080`.

## Method and observations

Constructed a deterministic 82-row handoff from exact upstream records, cross-checking the 45 baseline IDs, 18 P1 identities, 37 supplemental source references, 34 group IDs, source file Git blobs, and one shared TAM commit. The handoff preserves distinct `queue` and `group_id` fields and explicitly sets every review status to `UNREVIEWED`, every disposition/evidence/rights/reviewer field to null, and `release_authorized=false`. No 82-row editorial adjudication was performed. Baseline excerpts may be truncated; supplemental group sentences can repeat across occurrence IDs and are not independent historical evidence.

**Tests (EXECUTION-VERIFIED in V8, not Node CLI):** 16/16 in-memory positive/adversarial controls passed, including missing/duplicate/extra rows, altered queue/group/source pin, unauthorized status/release, altered upstream counts/P1 mapping and missing supplemental refs. After fetching the **actual committed** generator and handoff, 8/8 corrected readback controls passed: positive regeneration matched the committed JSON, and missing row, promoted status, changed source SHA, changed group, wrong count and forged provenance were rejected.

**Deviations and corrections, in order:** The first committed generator/manifest used the **wrong cross-queue input blob** (`fd0bdc8...` was the Run407 JavaScript *code* blob, not the cross-queue *JSON* blob). Both GPT-owned files were corrected in subsequent commits to `ab5e755...`; the generator's Node CLI now computes and checks Git blob SHA-1 of all four input byte streams before parsing. The first committed-byte mock negative run incorrectly counted two `structuredClone is not defined` harness errors as successful tamper rejections; these are **not valid negative evidence**. The harness was corrected to JSON deep-copy, and the 8/8 rerun verified actual rejection reasons. No earlier result is silently promoted. The Node CLI with actual filesystem input bytes **has not run**.

**Original Python scanner:** still **NOT RUN** against the eight real public TAM files. A fresh local DNS check on 2026-10-28 returned `gaierror(-3)` for `raw.githubusercontent.com`, `api.github.com` and `github.com`. Run412/416's independent JavaScript translation found 42 provisional trigger matches; no Python parity is claimed.

## Handoff and acceptance

**Claude:** use the 18 P1 and 34 supplemental groups for independent evidence/rights/wording review; do not conflate 82 occurrence records with 82 independently verified claims. Preserve every original ID and human decision. **GPT next:** run the original scanner against a pinned public ZIP, verify full Run334→344→347→351 dataset coordinator, source-bound cut consistency on final manuscript, positive Node export, Android and EPUB/PDF. **Timothy:** A1–A6/B1/B4/B6/C1 and final editorial/rights/publication authority.

**F-001 remains HOLD / NOT LAUNCH-READY.** No real editorial statuses advanced; 45 baseline and 37 supplemental occurrences remain UNREVIEWED. No account, outreach, publication, spending, payment, CI, paid inference or Cloudflare loop.
