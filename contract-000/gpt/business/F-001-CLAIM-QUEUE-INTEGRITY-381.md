# F-001 TAM Protocol ebook — 45-claim integrity gate (Run 381)

**Single project ID: F-001; HOLD / NOT LAUNCH-READY.** Continued the existing TAM Protocol ebook; no second income pipeline. Read shared [decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md), Workshop Business README, GPT checklist, Run380 progress, and Run378 pinned [candidate inventory](F-001-REAL-CLAIMS-378.json) first.

**PRE-TEST:** [Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6428412088), posted before diagnostics. **Code:** [read-only gate](f001_claim_queue_gate_381.js), [reproducible ten-case runner](test_f001_claim_queue_gate_381.js).

## EXECUTION-VERIFIED
The exact GitHub-fetched committed gate blob `e67e3b103c2d145141a5972b7fd534aa6bbf1cdd` was loaded into the JS test environment after removing only its Node shebang for function evaluation; the pinned actual Run378 JSON blob was `d9e36400b90cf534f9914c1c42b39d17f6d8a7fc`. The first diagnostic failed to parse the shebang; corrected the test loader and reran before recording results. **10/10 subsequent checks passed**:

| Case | Expected | Observed |
| --- | --- | --- |
| Pinned real 45-candidate inventory | integrity PASS, release HOLD | PASS / HOLD; 8 source records, 42 baseline, 3 supplemental, 45 unique, 0 reviewed |
| One baseline candidate removed | FAIL | FAIL (42-count, per-file, trigger, unique count) |
| Supplemental replaced with duplicate | FAIL | FAIL (duplicate, missing supplemental trigger, unique count) |
| Claim source blob altered | FAIL | FAIL (stale source) |
| Forged reviewed status without evidence | FAIL | FAIL (review without evidence) |
| One source record removed | FAIL | FAIL (8-source and unknown source) |
| Queue total falsified | FAIL | FAIL |
| Sentence number outside source range | FAIL | FAIL |
| Unknown trigger | FAIL | FAIL |
| Release flag switched to true | FAIL | FAIL |

This gate validates **inventory internal consistency**, source pin *references*, candidate identities, and review bookkeeping; it **does not re-fetch eight source bytes or independently regenerate the candidates**. A self-consistent forged inventory or edited executable can still pass; use independently pinned Git objects and the original Python scanner replay as separate controls. It does not verify historical claims or confer publication permission. No local Node CLI execution was performed; test ran the committed gate in the V8 tool environment against the actual committed JSON and mutations.

## Next complementary work
**GPT:** execute the original pinned Python claim scanner against all eight actual TAM source files, compare candidate keys and Unicode boundaries with the 45-item inventory; then run Run334→344→347→351 pinned dataset stage, EPUB/PDF/a11y and hash checks. **Claude:** independently adjudicate all 45 claims and Article 4, Gerah, precision, rights/license; do not overwrite GPT work. **Timothy:** A1–A6, B1/B4/B6, C1, explicit release permission. All 45 candidates remain **UNREVIEWED**. No account, listing, outreach, payment, publication, spending, paid inference, CI or autonomous Cloudflare loop.

## Addendum — independently pinned source tuples and unapproved-status rejection

**Second prospective entry:** [Issue #56](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6428483871), published before revision/retest. The initial 10/10 gate had two self-consistency weaknesses: source hashes could be jointly forged in the inventory, and arbitrary reviewed statuses with evidence could pass. Independently fetched `The-TAM-protocol` Git tree `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9` and compared **8/8** inventory file SHA/byte pairs to its entries (all matched). Hard-pinned those eight pairs in the GPT-only gate; until a reviewed status vocabulary is approved, any non-`UNREVIEWED` status is rejected even if it includes evidence.

**EXECUTION-VERIFIED final:** executed the **exact committed JS gate** blob `6d3df53bf5fd2c946fb0484edec615abd9cdb43a` and **exact committed 13-case test runner** blob `49c01aceca18d70a9bf5aa8e9b2669eff0d2456c` in the V8 environment with a minimal read-only `require` shim supplying the actual pinned JSON blob `d9e3640`. **13/13 expected outcomes passed:** the real inventory passed integrity/HOLD, and twelve mutations failed, including jointly forged source+claim SHA, changed source size and nonapproved reviewed status with an evidence string. No Node CLI was executed. The positive result remains inventory integrity only, not source-text or editorial verification. Release remains HOLD. The initial 10/10 evidence above is retained as historical diagnostic evidence, not presented as the final gate.
