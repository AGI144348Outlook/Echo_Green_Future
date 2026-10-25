# F-001 TAM Protocol ebook — continuing single-product checklist, GPT Run 347 (2026-10-25 ~06:55 CT)

**ONE project identifier: F-001. HOLD / NOT LAUNCH-READY.** Read existing [shared F-001 candidate](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-candidate-ebook-gumroad.md) blob `73d64d7`, [decision sheet](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-shared/Business/ideas/F-001-decision-sheet.md) blob `2975edc`, shared Workshop records and prior [Run 346 progress](F-001-PROGRESS-346.md) before this run. Shared source remains `library-shared@470d3c8`; public working TAM repository `AGI144348Outlook/The-TAM-protocol@d46456a`. Do not start another business pipeline.

**Run 347 actual advance:** GPT-only [bounded descriptor stage-consumer](F-001-STAGE-CONSUMER-347.py) prevents its JSON and CSV file paths from using unbounded `read_bytes()` after pathname checks. It uses `O_NOFOLLOW|O_NONBLOCK`, descriptor `fstat`, a byte cap during reading and before/after metadata comparison. [Pre-test](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6397331644) preceded [14/14 committed-source static + 5/5 helper-only synthetic PASS](F-001-TEST-EVIDENCE-347.md), with [post-test](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6397341979). No full consumer, caller, TAM integration, CI, publication, or shared promotion.

| Deliverable and acceptance criteria | Status / next action |
| --- | --- |
| Exact book identity, source scope, credit, copyright/licence | **BLOCKED** A1/A3/A4/A6. Timothy decides; Claude checks editorial/third-party attribution. |
| Storefront, price/refund, stable identifier/date, payout | **BLOCKED** A2/A5/B6/C1. Timothy authorizes; no accounts/listing/payment. |
| Historical and arithmetic claims, Dataset A/B contradictions | **DRAFT/BLOCKED** A rows 6/7, B 1/16=0.85625, *Gerah* 1/8 vs 1/16, ~35 claims; Claude editorial, Timothy adjudication. |
| Pinned source and three CSV/report stage outputs | **DRAFT** Run 344 gate pins and independent CSV reference hashes; real source verification still needed. |
| Stage gate/caller/consumer chain | **PARTIAL** Run 346 caller pins Run 340 consumer; Run 347 consumer is **not integrated**. Next: Claude review, full consumer tests prospectively posted, then caller repin and pinned TAM P46–P48. Acceptance: independently verified source commit, builder, exact outputs, hashes, failure cleanup and resource bounds. |
| EPUB/PDF accessible review edition | **DRAFT** reproducible book ID/date, EPUBCheck/Ace and PDF structural/visual review, final artifact SHA-256; Claude build, GPT independent verification. |
| Independent final release receipt | **BLOCKED** editorial claims, non-null artifact hashes, source provenance, separate reviewer and explicit Timothy signoff. Stage `HOLD` never equals release. |
| Listing, outreach, publication, payments | **NOT AUTHORIZED**. Timothy-only actions after approval. |

**Complementary work requested of Claude:** challenge descriptor helper and its limitations using Claude's independent `PROPOSED-PATCH-110-v4-csv-bound-lexists.diff` experience; keep editorial, rights, and listing records in Claude-owned/shared review venue. GPT will own follow-on consumer/caller integration only after preregistration; do not overwrite Claude.

**Timothy outstanding (carried forward):** A1–A6, B6/C1, Dataset A rows 6/7, *Gerah* and historical precision, identity/credit/licence, pricing/refund and explicit publication authority. No second income project, paid inference, Cloudflare loops, spending or external contact.
