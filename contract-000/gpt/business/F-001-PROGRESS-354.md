# F-001 — sole continuing TAM Protocol ebook, GPT Run 354

**Project ID F-001; status HOLD / NOT LAUNCH-READY.** Continuation of Run 353. Shared candidate plan `library-shared:Business/ideas/F-001-candidate-ebook-gumroad.md` blob `73d64d7`; decision sheet `2975edc`; GPT checklist `69449fc`; Workshop `d39dcb3`. GPT develops technical packaging, provenance and checksums; Claude independently handles editorial, listing, rights. No second project, no shared/Claude overwrite.

**This run's tangible advance:** draft-only [bundle byte verifier](F-001-BUNDLE-BYTE-VERIFY-354.py) + [11-case harness](F-001-BUNDLE-BYTE-TEST-354.py). [Evidence](F-001-TEST-EVIDENCE-354.md): **11/11 synthetic cases PASS**, exact committed-source blobs matched local tested bytes. Requires caller-supplied manifest pin, streams 11 bounded files, refuses symlinks/nonregular files, checks declared hashes/sizes, always `release=HOLD`. Proves only byte consistency, not authenticity or release.

| Deliverable | Acceptance criteria | Current state / next action |
| --- | --- | --- |
| Rights/licence/credit/source | Timothy settles A1/A3/A4/A6; exact text source branch, copyright/licence and credit recorded | **BLOCKED**; no default is approval. |
| Editorial accuracy | Dataset A rows 6/7, Gerah 1/8 vs 1/16, ~35 claims independently dispositioned | **BLOCKED**; Claude review + Timothy decisions. |
| Reproducible dataset stage | TAM commit `d46456a`, 6 A/8 B rows, independently pinned source and CSV SHA, fail-closed stage | **PARTIAL**; actual end-to-end stage NOT RUN. |
| Three-script staging coordinator | Verified private builder/gate/consumer, exact HOLD receipt, adversarial and real-source integration | **DRAFT**; prior isolated tests, full integration NOT RUN. |
| Package manifest shape | F-001/HOLD/NOT_GRANTED, EPUB/PDF and eight evidence digests | **SYNTHETIC TESTED** Run 353, shape only. |
| Bundle byte consistency | Trusted external manifest pin and real file hashes/sizes, regular bounded files | **SYNTHETIC TESTED** Run 354 11/11; real files/pin NOT VERIFIED. |
| Independent rebuild, formats and accessibility | Hash actual EPUB/PDF/report bytes, separate source-pinned rebuild, EPUBCheck/Ace/PDF and listing parity, fixed book ID | **BLOCKED / NOT RUN**. |
| Storefront, pricing, release | Timothy resolves A2/A5/C1 and authorizes release explicitly after rights/claims/terms verified | **NOT AUTHORIZED**; no publication, accounts, outreach, spending, payments. |

**Next single GPT action:** obtain real package files and separately trusted manifest pin through an authorized read path, preregister and run full F-001 staging + byte/report/format verification, document any deviations, maintain HOLD. **Complementary Claude request:** independently critique byte-verifier trust boundary and advance editorial/listing/rights without overwriting GPT files. **Timothy blockers:** A1–A6, B6/C1, Dataset A 6/7, Gerah, claims, licence/credit/book ID, explicit publication permission; A-000 witness/issuer/recovery/freeze is separate.
