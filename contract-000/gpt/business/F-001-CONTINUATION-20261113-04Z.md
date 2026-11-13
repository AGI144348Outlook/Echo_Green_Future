# F-001 / TAM Protocol ebook — GPT 04Z continuation

Status: HOLD / NOT LAUNCH-READY. **Same sole income project**; no new pipeline, account, publication or spend.

Evidence: previous F-001 continuation blob eed172347ca4e27ffea0136a15f920c0aadde4ae and checkpoint 690125bc. A6 is present but unresolved; a draft MIT branch is not release authority. Claude retains editorial/rights; GPT packaging/verification.

## Incremental deliverable: artifact-to-authorization evidence join (design only)

Use an immutable manifest per proposed release candidate: `project_id=F-001`, `source_revision`, `decision_sheet_blob`, `pdf_sha256`, `epub_sha256`, `rights_ledger_revision`, `editorial_ledger_revision`, `license_revision`, `issuer_receipt_id`, `issuer_verified_externally`, `revocation_checked_at`. Reject missing/placeholder fields. A source row existing is not a decision. A checksum matching a file is integrity, not authorization. Neither self-asserted approval nor caller-supplied verification may grant release. Unknown or conflicting blocking rows fail closed. Never publish private receipts in GitHub.

## Acceptance checklist
- [x] Sole project identity preserved.
- [x] Source-pinned decision adapter and negative vectors specified in previous pass.
- [x] Release candidate manifest schema drafted here.
- [ ] Timothy decides A1–A6 and relevant B rows; independently authenticated evidence.
- [ ] Claude editorial and rights dispositions completed and verified.
- [ ] Actual source/license revisions pinned; A6 resolved.
- [ ] PDF and EPUB independently parsed, accessibility and Android QA passed.
- [ ] Reproducible SHA-256s, listing/sample parity and externally authenticated release authorization.

Next action: implement offline manifest parser and negative tests **after prospective GitHub preregistration**. No tests were executed for this draft. Blockers: rights/editorial, licensing, release trust root, QA. No outreach or publication.
