# F-001 — single-project deliverables and acceptance, Run386

**Project ID:** F-001 TAM Protocol ebook, unchanged since Run385. **Status:** HOLD / NOT LAUNCH-READY. **Authority:** shared decision sheet `2975edcc`, TJ R1, prior Run385 progress. No other income pipeline was opened. All 45 occurrence cards remain **UNREVIEWED** and none has rights clearance.

| Deliverable | Current evidence / state | Owner / next action |
| --- | --- | --- |
| Product source | Public TAM `d46456a`, eight source Git blobs connector-verified | GPT: original Python scanner against safely materialized actual files |
| Editorial queue | 45 occurrence cards; **20 truncated previews**, 25 full-sentence previews, **7 duplicate pairs / 38 unique normalized sentence texts** (not 38 reviewed claims) | Claude: evidence review of each context, four P1 duplicate groups; Timothy final dispositions |
| NEW offline preview audit | [Run386 read-only Python audit](f001_editorial_source_audit_386.py) and [10/10 synthetic regressions](test_f001_editorial_source_audit_386.py), committed blobs match locally tested | GPT/Claude independent real-source replay and cross-review |
| Original Python scanner | Exact shared scanner blob `31f3dcff` inspected; 42 baseline inherited, not rerun on all eight actual sources this run (container DNS blocked) | GPT: real-source 42-row replay, preserve 3 supplemental |
| Dataset staging | Earlier 6 A / 8 B rows; full pinned 334→344→347→351 coordinator not independently replayed; Run358 CSVs untouched | GPT: HOLD-only pinned staging with tamper negatives |
| Editorial/historical accuracy | Strong correlation/accuracy/archaeology claims and Article 4 unresolved; 45 statuses unchanged | Claude editorial, Timothy B1/B4 |
| Rights/licensing | R1 ownership assertion, but A1/A6 source scope and licensing unresolved | Timothy A1/A6 |
| EPUB/PDF/accessibility | Prior draft build/checker evidence exists; no final approved package independently verified this run | GPT packaging after editorial and rights, Claude cross-review |
| Listing, pricing, credit/refunds | A2–A5 draft placeholders only | Timothy |
| Payment, publication | C1 and explicit authorization absent; no accounts, outreach, uploads or sales | Timothy only |

**Acceptance criteria unchanged:** all 45 source-occurrence cards have independently evidence-backed dispositions and rights review (duplicate claims may share evidence, not automatic approval); original Python scanner and pinned dataset chain replay on actual sources with tamper negatives; A1–A6/B1/B4/B6/C1 resolved; final EPUB/PDF/accessibility/checksums/listing independently verified; explicit Timothy publication approval. Synthetic tests and prefix matches are not historical fact-checks or release gates.

**Next GPT action:** run original scanner and Run386 preview audit on eight exact pinned TAM source bytes in a safe local Python workspace; trace full 334→344→347→351 coordinator without touching Run358 CSVs. **Next Claude action:** source-context-specific editorial review for seven duplicate groups and 20 truncated previews, especially four P1 groups; Article 4, Gerah/precision, rights. **Blocker:** container GitHub DNS prevented materialization; GitHub connector could read text and blob metadata but cannot execute original Python. **F-001 HOLD.**
