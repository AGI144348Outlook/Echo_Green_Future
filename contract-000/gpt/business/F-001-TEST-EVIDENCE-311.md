# Contract-000 GPT Run 311 — F-001 actual-script integration evidence (2026-10-23)

**Prospective notice:** [Issue #30](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/30) was created **before any local tests**. A separate prospective addendum was posted in the same thread **before v3 tests**. This record distinguishes observations from interpretations and discloses deviations.

## Sources and environment

- Linux scratch workspace; Python **3.13.5**; `python3 -I -B`; no GitHub Actions, API inference, Cloudflare or publication.
- **Actual** Git-blob-matched GPT scripts: receipt-v3 `4aafb14298e901079428864bb57be28810bb226c`, v5 parser `f8c2b4b29f9fffb1bc3d65f4f1fdf56954b7a4f0`, v5 gate `7556a83ff3923528b0be5d6c419a231285cee1d3`, cross-report v4 `848040fcfd7f73b1f65d0772c25bfcd6e9e1be56`, coordinator-v2 `20cc610ae5c127dd34efa876812dd0a6279a402b`. All matched their exact Git blob IDs in the local workspace before execution; coordinator-v2 was reconstructed from its GitHub source and its exact blob ID verified before use.
- Proposed coordinator-v3: Git blob `ade012e6b248dc1e05b8338aab7c53268fff73f0`; local tested bytes match the committed GPT-owned file. Only GPT-owned code was written.
- Fixture: archived public-derived Dataset A CSV (584 bytes, SHA-256 `d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2`, flagged CSV lines **6, 7**); synthetic Dataset B; **intentionally invalid placeholder** EPUB and PDF; caller-supplied `0`*40 source/other script pins are deliberately **not authenticated**. Synthetic editorial record, where present, has `SYNTHETIC_TEST_ONLY_NOT_TIMOTHY_DECISION` explanations and no decision reference.
- Local harness SHA-256: `test_actual_chain.py` `b9b31c35b0d10f879df54c993deb1d331aff7fa74ea263c777a440e6572daba1`; `test_v3_assertions.py` `305b25654c3302920e8d2cf206711facd5cc813ea6663b921d5a476c74f01f4a`. Evidence JSON SHA-256: `actual-chain-results.json` `e466049e802c13360d481683b41ae5c55c0e83174a2834dd4c1e68403af8199e`; `v3-assertions.json` `28b5a7873401650c4d4830988965d55b528823cf230e8b5bc644f5cedfa3ed16`. Full harnesses and JSON are included in the accompanying run handoff archive.

## Observations — actual scripts, not stubbed subprocesses

| Case | v5 parser | receipt-v3 | v5 gate | v4 binding | coordinator-v2 | proposed coordinator-v3 |
|---|---|---|---|---|---|---|
| **Pending editorial record absent** | exit 3, PENDING/HOLD | exit 0, PASS/HOLD | exit 0, PASS/HOLD | exit 0, PASS/HOLD | exit 0, PASS/HOLD | exit 0, **PASS/HOLD/BLOCKED**, `editorial_dispositions_pending` |
| **Synthetic editorial record present** | exit 0, RECORDED_UNAUTHENTICATED/HOLD | exit 0, PASS/HOLD | exit 0, PASS/HOLD | exit 0, PASS/HOLD | exit 0, PASS/HOLD | exit 0, **PASS/HOLD/BLOCKED**, `editorial_decision_authority_unverified` |
| **Alter EPUB bytes after pinning** | — | rejected by coordinator | — | — | not rerun | exit 1, **FAIL/HOLD/BLOCKED**, receipt-v3 stage exit 1 |

**Follow-on assertions:** 3/3 outcomes confirmed for v3; the two controls retained `readiness=BLOCKED`, `source_pin_authenticated=false`, `approval_authenticated=false`, `publication_authorization=ABSENT`, and `format_accessibility_rights_verified=false`; the tamper negative rejected. All stages reported HOLD, and the tampered EPUB was restored after the test.

## Interpretation and deviations

1. **Original hypothesis challenged:** the pre-test entry expected pending editorial evidence to yield FAIL/HOLD. Actual tools yield **integrity PASS / release HOLD** for pending, because `v5_gate` deliberately accepts a pinned PENDING report and v4 accepts either PENDING or RECORDED_UNAUTHENTICATED. That is a consistency pass, **not** editorial completion. v3 preserves integrity semantics but adds explicit `readiness=BLOCKED`, `editorial_status`, and blocker reasons. It does not invent an approval.
2. **No-flagged-row control replaced:** the actual F-001 receipt and gate require flags exactly `[6,7]`; a no-flagged-row control cannot pass by design. The second control used a clearly synthetic, unauthenticated record instead. This is a disclosed change to the proposed method, not a retrospective claim.
3. **Format blind spot observed:** matching hashes for placeholder EPUB/PDF were accepted. This is expected for a byte-consistency checker, but shows that a PASS must never be called launch-ready or valid-book evidence. Separate EPUB/PDF validation and real deliverables remain required.
4. The local fixture contains caller-controlled source pins and synthetic editorial dispositions. No trusted external source witness, genuine finished book, independent Claude review, live account, release approval, or production sandbox was tested. The child process time/memory/IO boundary and concurrency are not comprehensively secured.

## Next work and acceptance

**Same income project: F-001 TAM Protocol ebook.** Ask Claude to independently review v3's readiness semantics and its nested subprocess resource bounds; continue manuscript/claims/a11y/listing on Claude-owned paths. GPT next: test real four-artifact build and source authentication once public source pins and editorial authority are settled, under a fresh prospective Issue notice. **Acceptance remains unmet:** four genuine reproducible deliverables, editorial decisions for lines 6/7, authenticated source/decision witness, validated formats/rights/terms, independent review and Timothy's explicit publication approval. **Release remains HOLD.**
