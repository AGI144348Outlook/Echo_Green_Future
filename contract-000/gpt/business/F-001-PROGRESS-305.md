# F-001 — TAM Protocol ebook, GPT Run 305 progress (2026-10-23)

**Single continuing income project:** `F-001` — TAM Protocol ebook (PDF + EPUB + Datasets A/B CSV). **Status: ON HOLD, draft only.** This continues the shared `library-shared:Business/ideas/F-001-candidate-ebook-gumroad.md` plan (blob `d134d68`, Claude §111), decision sheet `2975edc`, and GPT Run 304 progress. No second income pipeline. Claude owns editorial/manuscript/listing, GPT owns independent packaging/receipt validation; neither edits the other's work. Shared Workshop/Business references were read, not modified.

**Run 305 contribution:** The GPT-owned receipt verifier v1 `696e66f` has a status contradiction: it permits `NO_FLAGGED_ROWS` or `RECORDED_UNAUTHENTICATED` while requiring Dataset A's unresolved flagged CSV lines [6,7], without independently validating a disposition record. The [prospective pre-test Issue #25](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/25) preceded all tests. A separate [v2 proposed checker](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/050509cfb63379fa46ccf2efac584d6401b6e241) now accepts only `PENDING/HOLD` for editorial status until a v5 disposition report is source-pinned and independently verified. v1 is retained unchanged. [Ten-case regression](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/827c85d12cf7075a5faea672f6ea988f4d1e685d) **10/10**; [seven editorial cases](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/ef804742f2e34eee4f45122ae4e64551d4d8743b) **7/7**; two v1 baseline reproductions **2/2**; all expected, 19 executions total with deliberate scenario overlap. [Evidence](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/370288c7d87c75a1309fcd95af3b2df3f84ae66d). No real book artifacts or approval verified.

## Deliverables checklist — same F-001

- [x] One F-001 product and Claude/GPT complementary roles retained.
- [x] Archived Dataset A/B reconstruction and two Dataset A line 6/7 editorial flags preserved; no dispositions inferred.
- [x] Unintegrated GPT v5 editorial-disposition validator and Claude independent review recorded.
- [x] Source-pinned four-artifact receipt v1.2 specification and unintegrated v1 byte-consistency verifier.
- [x] **New:** unintegrated v2 checker rejects unsupported editorial completion, 17/17 expected v2 synthetic outcomes, two v1 baseline reproductions; exact Git blobs verified.
- [ ] Claude independently reviews v2 and integration boundary to a source-pinned v5 disposition report.
- [ ] Trusted independent source-pin/witness, full actual source/script/patch/environment evidence; not a same-credential self-attestation.
- [ ] Jointly reviewed patch stack in authorized non-main candidate branch; reproducible **real EPUB, PDF, Dataset A CSV and Dataset B CSV**.
- [ ] Independently check four real output hashes, EPUBCheck/accessibility, PDF layout, claims, TOC, licensing, listing and refund/fee statements.
- [ ] Timothy authenticates exact editorial decisions for Dataset A CSV line 6 Silver Droplet and line 7 Small Scrap.
- [ ] Timothy resolves A1–A6/B6 (scope, store, exact credit, framing, price/refund, license/source and identifier), then separately authorizes publication.

**Acceptance criteria:** All four actual deliverables byte-pinned and reproducible, claims/rights/a11y/editorial decisions checked, independent source and approval witness, Claude's independent review and Timothy's explicit authorization. Parser PASS or an unauthenticated record does not make F-001 READY.

**Next GPT:** Ask Claude to review v2 fail-closed editorial policy; design an actual v5 disposition-report binding with immutable source pin and test it prospectively before any integration. **Next Claude:** continue editorial/listing review and inspect v2 without changing GPT's files. **Blockers awaiting Timothy:** A1–A6/B6, two disputed dataset rows, independent approval witness and permission to publish. No outreach, account creation, publication, spending, payment, paid inference or autonomous Cloudflare loops.
