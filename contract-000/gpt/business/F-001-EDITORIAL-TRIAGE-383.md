# F-001 TAM Protocol ebook — editorial queue handoff, Run383

**Project ID:** F-001, unchanged. **Status:** HOLD / NOT LAUNCH-READY. **Prospective test:** [Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6430242103); [post-test](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6430273317). **Authority:** shared `Business/ideas/F-001-decision-sheet.md`, previous Run382 progress; **input:** actual-source-bound Run378 45-candidate inventory at blob `d9e36400b90cf534f9914c1c42b39d17f6d8a7fc`. 

## Delivered and observed

- New deterministic, read-only [queue builder](f001_editorial_triage_383.js), [repeatable Node regression runner](test_f001_editorial_triage_383.js) and [45-card review queue](F-001-EDITORIAL-QUEUE-383.json). Source locator, exact excerpt, Git source blob SHA, original detection group and UNREVIEWED state are preserved. The source-pinned inventory itself was previously verified against eight actual TAM source texts in Run382; **no new real-source Python scanner replay in Run383**.
- **18/18 V8 checks passed**: 10 positive structural/preservation checks and eight negative controls (duplicate ID, wrong SHA, changed review status, blank excerpt, invalid sentence number, release authorization, missing source and missing claim). The committed source was re-fetched and regenerated the committed JSON queue exactly. The committed Node regression runner was **not executed in Node**.
- 45 distinct cards: **42 baseline + 3 supplemental**, **18 P1 / 27 P2** by transparent heuristic flags. Source distribution: README 2; Article 1 2; Article 2 3; Color/Dental 4; Article 5 3; Article 6 3; Article 10 4; Collective 24. Flags: quantitative 10, certainty/inference 9, comparative/superlative 13, historical 6, causal 3, general support 13. Flags can overlap. The P1/P2 ranking is a *triage aid*, not a risk verdict.
- Every `editorial_disposition`, `evidence_reference`, `reviewer`, and `rights_clearance` is null; every card is `UNREVIEWED`. No claim was verified true or false. The output remains `HOLD`.

## Complementary work and acceptance

**Claude:** independently review P1 claims, attach external evidence where appropriate, distinguish historical inference from demonstration, resolve Article 4 and Gerah/precision questions, check rights and listing text. Do not auto-approve cards; preserve reviewer identity, evidence links and source version.

**ChatGPT next:** execute exact shared Python claim scanner and fail-closed source preflight on all eight pinned TAM texts, compare with 42 baseline and 3 supplemental candidates, then stage 6/8 datasets and verify EPUB/PDF when editorial and rights gates permit. This queue is a supplement, not a replacement for the source-ledger.

**Acceptance remains blocked** until all 45 dispositions have accountable evidence and independent editorial review, the original Python source scan is replayed, A1–A6/B1/B4/B6/C1 are decided by Timothy, rights/source are authorized, dataset/EPUB/PDF/a11y/checksums pass and Timothy explicitly approves publication. No account creation, outreach, publication, payment, CI, paid inference or Cloudflare loop occurred.
