# F-001 — single-project deliverables, acceptance and next action, Run384

**Project ID:** F-001 TAM Protocol ebook (unchanged from Run383). **Status:** HOLD / NOT LAUNCH-READY. **Authority:** [shared F-001 decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md), [Run383 progress](F-001-PROGRESS-383.md). No second business pipeline, no storefront action.

| Deliverable | Verified state | Owner / next action |
| --- | --- | --- |
| Product/source | Sole F-001 ebook; eight source blob pins from TAM commit `d46456a` | GPT: actual eight-file Python replay |
| Editorial inventory | 45 source-bound candidate cards, 42 baseline + 3 supplemental, **45 UNREVIEWED**; 18 P1/27 P2 heuristics | Claude: independent evidence/dispositions; GPT: Python parity |
| Original Python scanner | Run384 exact `claim_scan.py` Git blob reproduced locally and executed against synthetic eight-file fixtures; **11/11** fail-closed replay-gate tests; **real TAM replay NOT RUN** (DNS) | GPT: actual pinned source replay, compare 42 rows, keep 3 supplemental |
| Dataset A/B | Prior 6/8 rows and 334→344→347→351 staging evidence; not replayed Run384 | GPT: complete stage chain, do not change Run358 CSVs; Claude: Gerah/precision |
| Article 4, historical framing | Article 4 unresolved; no historical truth certification | Claude editorial; Timothy B1/B4 |
| Rights/source and authorship | Timothy R1 ownership, but source/licensing A1/A6 choices still open | Timothy A1/A6; Claude review |
| EPUB/PDF/a11y/cover/identifier | Draft tools; final package not independently verified this run | GPT: after rights/editorial gates; Timothy B5/B6 |
| Listing, price, credit/refunds | Draft scenarios only; A2–A5 not approved | Timothy decisions; Claude listing draft only |
| Payments/payout/publication | No account/spend/sale/publication; C1 and explicit release authorization absent | Timothy only |

**New deliverables:** [HOLD-only Python replay gate](f001_python_replay_gate_384.py), [11-case synthetic regression](test_f001_python_replay_gate_384.py), [evidence report](F-001-PYTHON-REPLAY-384.md), [PRE/POST Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6431166146). Source pin and synthetic tests are not historical or editorial proof.

**Acceptance criteria (unchanged):** (1) all 45 editorial cards receive evidence-backed independent dispositions; (2) original Python scanner and pinned dataset chain replay against actual source bytes; (3) rights/source and manuscript questions resolved; (4) final EPUB/PDF/a11y/checksum and listing checks; (5) Timothy's explicit release authorization. No automatic promotion on test pass.

**Next GPT:** obtain pinned source files in a runtime with GitHub access and execute replay gate; stage the original dataset pipeline; leave F-001 HOLD. **Next Claude:** review P1 claims, Article 4/rights/Gerah and precision. **Timothy pending:** A1–A6, B1/B4/B6, C1, publication.
