# F-001 — GPT progress 300, 2026-10-23T13:56Z

**Sole income project:** F-001 TAM Protocol ebook; status **ON HOLD**. Existing shared plan `Business/ideas/F-001-candidate-ebook-gumroad.md` (current blob `083ce391023d26843207f4bc29ccde86eac44887`, Claude §106) and decision sheet (blob `2975edcc4cae8a17499e873b68ba75f5c39ea527`) read before work. The prior GPT checkpoint is `RUN-299-CHECKPOINT.md` (blob `4f85ca82e1aea3945c4ae04b0d81fd0c4226f682`). No other income pipeline started.

## Complementary work with Claude

Claude's §106 reproduced v1 16/16, independently characterized pinned public Dataset A, and proposed (i) explicit CSV line numbers, (ii) a clean-dataset `NO_FLAGGED_ROWS` state, and (iii) binding the disposition record's CSV digest to the source-pinned receipt. GPT implemented a **separate, unintegrated v2 parser** (commit `bdce8d206f86b8cb16ea2f849241c953fd0ed29a`) without editing Claude's build files. A prospective [Issue pre-test](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6366603232) preceded **26/26 offline synthetic characterization outcomes**; [evidence](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/e86f0940ca374d2ec865f725df7d7fd0d768c382). `csv_line` is 1-based with header line 1; records use `record_version=2`. Expected SHA-256 is required as a CLI argument, but is **not authenticated** by the parser; all outputs remain `release=HOLD`.

## Deliverables checklist

- [x] Single F-001 plan, candidate comparison and decision sheet retained; no second business.
- [x] Dataset A/B public-source rebuild evidence: 6/8 rows, original discrepancies retained.
- [x] Read-only integrity gate v4; Claude independently reproduced 16/16 (§105); no READY path.
- [x] Four-artifact receipt v1.1 specification (proposal); source hashes and actual script blobs required.
- [x] v1 editorial-disposition parser and independent Claude reproduction (§106).
- [x] **New v2 proposal and 26/26 synthetic tests**: explicit `csv_line`, `NO_FLAGGED_ROWS`, required expected digest; preserve v1.
- [ ] Claude independently review v2 schema, clean-A exit 0 (binding-only) and expected-pin trust limitation; agree on integration and independent pin source.
- [ ] Resolve two Dataset A discrepancies with authenticated Timothy editorial decisions, reflecting chosen dispositions in product text.
- [ ] Final reviewed **EPUB, PDF, Dataset A CSV, Dataset B CSV**, with byte counts, four SHA-256 values and independently source-pinned release receipt.
- [ ] Complete claim, rights, accessibility, listing, terms, refund and reproducibility checks, then Timothy A1–A6/B6 and separate explicit publication authorization.

## Acceptance criteria and next action

No release without exact four-artifact hashes, input/script/patch provenance, full CSV byte integrity, editorial dispositions tied to authenticated decisions, independently reviewed build/claims/accessibility, agreed licensing/terms, and Timothy's explicit publication authorization. Parser success never grants publication permission. **Next GPT:** obtain Claude's independent v2 review, then draft the source-pinned receipt integration (no production modifications). **Next Claude:** independently test v2 and continue manuscript/claim/listing review in Claude-owned records; do not overwrite GPT branch. **Awaiting Timothy:** existing A1–A6/B6, two Dataset A dispositions, rights/credit and launch authorization. No accounts, outreach, spending, payments, publishing, paid API inference or autonomous loops.
