# F-001 rights-gate v2 design — 2026-11-06 05Z (DRAFT, NOT EXECUTED)

**Single income project:** F-001, TAM Protocol ebook candidate. Status **HOLD**. Source: library-shared `Business/ideas/F-001-candidate-ebook-gumroad.md` §198–204; Claude §204 and previous GPT 04Z checkpoint. No manuscript, source rights or release approval inferred. 69 source units remain UNREVIEWED. No account, outreach, pricing action, publication or payment.

## Delta from v1 (draft specification, not an implemented or tested gate)
- All 9 v1 fields remain; add `source_range` as required pinned character/line range. `source_id` is exact source path; `immutable_digest` must match 40 lowercase hex characters (Git blob format) and be independently checked against the actual source bytes; syntax alone is insufficient.
- Normalize `passage_id` with Unicode NFC and strip whitespace for duplicate comparison, but **reject** non-canonical IDs rather than silently rewriting signed manifests. Enforce pinned `file:line:col` shape after confirmation of §198 worksheet format.
- Require parseable timezone-aware UTC `reviewed_at`; refuse natural-language dates, missing time zone, and timestamps in the future.
- Reject unknown fields, unexpected decision vocabulary, unsupported scope, conflicts and ambiguous evidence references. `rights_basis` = own / third-party-permission / third-party-public-domain / unsure / disputed. `unsure` or `disputed` always HOLD.
- `ChatGPT` and `Claude` may propose `REJECT` or `HOLD`, never `ALLOW`. Human reviewer string is NOT proof of identity. Only Timothy's separately authenticated approval, tied to the **exact canonical manifest SHA-256** and source ranges, can permit a release review; neither assistant creates that attestation.
- Preserve all failure reasons, sorted deterministically: `missing_field`, `conflict`, `unverified_digest`, `disputed`, `unsure`, `scope_gap`. Output `HOLD` if any reason, regardless of a row's `ALLOW` field. Release gate additionally requires manuscript availability, source-rights verification, editorial signoff, packaging hashes/accessibility, listing parity and Timothy's explicit publication authorization.

## Adversarial acceptance vectors to preregister before running
- fabricated ALLOW; `immutable_digest='x'`; `reviewed_at='yesterday'`; `reviewer='ChatGPT'`; `note='DENIED by Timothy'`; `P1` vs `P1 `; missing `source_range`; two conflicting sources for one passage; a valid-looking but nonexistent source blob; an attestation for an earlier manifest hash; unauthorized sample/listing scope; disputed basis. All must fail closed.
- A syntactically valid document with fake reviewer/attestation is **not** cleared. No automated gate can establish legal rights from self-asserted strings.

## Division of work and checklist
Claude: editorial worksheet, provenance and rights evidence candidates (never attests for Timothy). ChatGPT: v2 validator implementation, preregistered adversarial tests, PDF/EPUB packaging and checksums after approved manuscript. Timothy: authentic rights and publication approval.
- [ ] Source manuscript and 69 units verified
- [ ] Passage-by-passage rights evidence verified by human
- [ ] Independent attestation of immutable manifest
- [ ] Editorial review and accessible PDF/EPUB package
- [ ] Cross-checked listing parity, price/refund decisions
- [ ] Explicit publication authorization
**Next:** implement v2 as a separate GPT draft; preregister test cases in a GitHub Issue before any execution. HOLD remains mandatory.
