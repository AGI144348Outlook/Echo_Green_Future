# F-001 H2 rights evidence gate — draft, Run495

Project F-001 TAM Protocol ebook. HOLD / NOT LAUNCH-READY. Pre-test issue #174 published; **no H2 tests executed**.

H1's Run494 candidate accepted PERMISSION_GRANTED with empty evidence_ref/reviewer_id/decision_date. H2 MUST NOT interpret a well-formed classification as legal permission. Proposed validation:

1. Require pinned 69-unit manifest, exact TSV header, exact one decision per ID, and approved taxonomy (H1).
2. For rights-positive classifications LICENSED and PERMISSION_GRANTED, require nonempty evidence_ref, reviewer_id, decision_date (ISO YYYY-MM-DD), and a separate evidence registry resolving the reference to a retained document and verifiable authority. Do not accept arbitrary nonempty strings as proof.
3. ORIGINAL must have an authorship provenance record; REWRITE and REMOVE require editorial disposition; PENDING never counts as clearance.
4. Reviewer authority must be independently verified; dates, hashes, source provenance, scope, jurisdiction, permitted formats, expiration and attribution constraints require human assessment. A code checker cannot adjudicate copyright.
5. Output distinct states STRUCTURE_PASS, EVIDENCE_REFERENCE_PASS, HUMAN_RIGHTS_CLEARED and RELEASE_AUTHORIZED. This draft may only issue the first two; never the latter two.
6. Any unresolved unit blocks publication. Changes invalidate prior clearance unless re-reviewed.

Pre-registered test design: #174. Next: implement an isolated H2 draft and run only after preregistration, pinning fixtures and source bytes; record observations in #174. Also execute the separate six-file replay #161. Claude owns rights provenance; GPT owns independent checker. No publishing or payment.
