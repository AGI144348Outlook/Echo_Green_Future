# F-001 — GPT progress Run 302, 2026-10-23

**One continuing income project:** `F-001` — TAM Protocol research ebook, **ON HOLD**. This is the same project as Runs 293–301, not a new business pipeline. No publication, account creation, outreach, payment, spending or paid inference authorized or attempted.

## Sources read before work

Current shared plan `Business/ideas/F-001-candidate-ebook-gumroad.md` blob `776df9045046b8de19361803b7bae0283b52d046` (Claude §§108–109), `Business/ideas/F-001-decision-sheet.md` blob `2975edcc4cae8a17499e873b68ba75f5c39ea527`, `Business/ideas/F-001-tam-build/APPLY-ORDER.md` blob `43e9d5b40fcc78507dbcde9e70f00b6454a6342e`, previous GPT `F-001-PROGRESS-301.md` blob `de0ed3bba9c131ad3c96c7351ffa5ab1ea88b5aa` and `RUN-301-CHECKPOINT.md` blob `230df72216d5325e12757c9a50d1f483fef42b1c`.

## Complementary coordination with Claude

Claude §108 independently reproduced GPT v3 on the archived six-row public Dataset A (24/24) and identified the FIFO read hang; §109 checked the proposed patch sequence but applied none. Claude's `PROPOSED-PATCH-108-v3-bounded-read.diff` blob `3d0b1a76a660a89228d02da8a6deb0c8c5fcb1fc` proposes `is_file()` and bounded read. GPT independently proposed **v4** with a nonblocking, no-follow (where supported) open and `fstat` on the opened descriptor, followed by a 1 MiB+1 read. This avoids the separate path-type check/open gap for the tested Linux cases. V3 and Claude's patch remain unchanged.

**New commits:** v4 `cc8b7a04dc0b293e7cd7f08fad829e4e1d94cfd3`, reproducible seven-case IO harness `57142cfd2a3dc86b4d3f74ac027d42dcf2864212`, detailed evidence `8273422ded712cd73c6e9f042546fe11c003369b`. Prospective Issue #13 pre-test comment `6369220970` preceded all tests; post-test comment `6369302970` followed them. **16/16 synthetic cases passed**, seven overlapping IO cases independently rerun 7/7; all reports HOLD and unauthenticated. No final production artifacts tested.

## Deliverables checklist (same F-001)

- [x] Single F-001 selection and shared project plan/decision sheet maintained.
- [x] Archived public-source Dataset A/B reproducible rebuild evidence (six/eight rows); two Dataset A stated-vs-recomputed discrepancies remain editorial HOLD.
- [x] Unintegrated dataset integrity gate v4, proposed receipt v1.1 and editorial-binding parser v1–v3; Claude independent review documented.
- [x] **Run 302:** proposed v4 regular-file bounded reader, exact Git blob and 16/16 synthetic characterization; no release status introduced.
- [ ] Claude independently review v4 descriptor policy, portability, remaining CSV read bounds and whether to incorporate into jointly reviewed stack.
- [ ] GPT integrate parser status into a **read-only, source-pinned receipt verifier**: expected Dataset A SHA-256 must originate from separately authenticated TAM source commit/build manifest, not the same invocation that produced the CSV; fail closed if independent pin absent. Keep status and exit code separate, and never set READY from a parser result.
- [ ] Resolve Timothy's editorial dispositions for Dataset A CSV lines 6 (Silver Droplet) and 7 (Small Scrap), with source-bound authenticated references.
- [ ] Rebuild, package and independently validate **EPUB, PDF, Dataset A CSV and Dataset B CSV**; record each byte count, SHA-256, source and script blob, patch order, accessibility/claims verification, and release receipt.
- [ ] Resolve A1–A6/B6 product scope, licensing/rights, credit, storefront/terms, pricing and explicit Timothy approval for any publication, account creation, outreach or payment.

## Acceptance criteria, next action and blockers

**Acceptance:** all four artifacts verified with source/script pins and reproducible hashes, no unresolved editorial claims, accessibility and listing claims checked, independent Claude review, documented rights/credit/terms, explicit Timothy launch authorization. Exit 0 from v4 only indicates parser status; source and decision authentication booleans remain false. **Next GPT:** source-pinned receipt integration design and separate prospective test notice before any new tests. **Next Claude:** review v4 and continue editorial/manuscript/listing work in Claude-owned records; do not overwrite one another. **Timothy blockers:** A1–A6/B6, two Dataset A editorial dispositions, rights/credit and launch authorization. No unapproved external action.
