# F-001 TAM Protocol ebook — release evidence reconciliation 2026-11-13 05Z

**Single continuing income project:** F-001, TAM Protocol research ebook. Status **HOLD / NOT LAUNCH-READY**. No second pipeline, publication, outreach, account creation or payment.

## Source-pinned observations
- `library-shared/Business/ideas/F-001-decision-sheet.md` blob `35ece85d203b8f1a5bac5a2bf3b5d6b8780ac2eb`: A1–A5 and **A6** blocking; A6 is MIT-versus-copyright branch/license choice, unanswered. B1–B6 editorial/build; C1–C4 operations. Draft defaults are not approvals.
- `listing_check.py` blob `adc3123c...`: unconditional claims.csv status check exists now; do not repeat historical bypass as current defect.
- `build_pdf.py` blob `c029cd67...`: regex-based page estimate insufficient for final parity.
- `rights_rows.py` blob `976a726c...`: path containment missing. Claude owns source patch proposal, GPT does not overwrite.

## Release manifest draft (schema, NOT approval)
```json
{
 "project":"F-001","state":"HOLD",
 "source":{"repo":"The-TAM-protocol","commit":null,"license_decision_A6":null},
 "deliverables":{"pdf":{"sha256":null,"pages_parser_verified":false},"epub":{"sha256":null,"epubcheck_verified":false},"sample":{"sha256":null},"listing":{"sha256":null}},
 "editorial":{"claims_complete":false,"rights_complete":false,"accessibility_reviewed":false},
 "approval":{"issuer_verified":false,"artifact_digest_bound":false,"scope":null,"revocation_checked":false}
}
```
Nulls represent missing evidence, not defaults. A release gate MUST refuse when any required evidence is absent or self-asserted, even when local format scripts pass. Do not use a caller-controlled `timothy_authorized` flag as authority.

## Deliverables checklist and acceptance criteria
- [ ] Source revision and A1/A6 rights/license decisions from Timothy, with evidence.
- [ ] Claude editorial and rights disposition receipts; claims.csv all marked and reconciled to source revision.
- [ ] GPT deterministic PDF/EPUB/sample/listing artifacts, immutable SHA256 digests and independent PDF parser page count; EPUBCheck plus accessibility review.
- [ ] Android reader QA for PDF/EPUB and matching listing/sample content.
- [ ] Verified approval signed or otherwise independently authenticated, scoped to exact artifact hashes, with revocation status.
- [ ] Timothy explicitly authorizes account/publication steps separately; only then launch.

**Next GPT action:** write an inert manifest validator on GPT branch that returns a fail-closed diagnostic list; preregister before any repository test. **Complementary Claude task:** continue rights/editorial receipts and path-containment remediation on Claude-owned work; do not alter GPT files. **Outstanding Timothy:** A1–A6 decisions, trust root, actual publication authorization. No tests of F-001 code this run.
