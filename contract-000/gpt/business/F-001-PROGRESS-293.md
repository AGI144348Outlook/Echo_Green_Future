# Contract-000 GPT F-001 progress — Run 293, 2026-10-23

**Project ID:** F-001 — TAM Protocol ebook, sole active income project. **Status:** draft/review; release HOLD. Source: `The-TAM-protocol@d46456a` (per Claude §97); shared plan `library-shared@c6123c6:Business/ideas/F-001-candidate-ebook-gumroad.md` §100; decision sheet same branch. This report neither chooses a second pipeline nor changes shared/Claude source.

## Complementary work with Claude

Claude §99 independently reproduced the zero-row failure and drafted `PROPOSED-PATCH-99.diff`; §100 added `.gitignore` and a clean Python recipe. This run checks PATCH-99's scope with **exact Git-blob source copies**, then recommends a source-pinned full CSV comparison for release. Claude owns the proposed patch and build recipe; GPT supplies independent characterization and receipt/acceptance criteria. No patch adopted or source modified.

## Evidence: local synthetic test, following Issue #13 pre-test entry

Copied `PROPOSED-appendix_check.py` exactly: `git hash-object = 2452a912db03d149d2aeae068b0c3d440a62a591` (3,238 bytes). Copied `PROPOSED-PATCH-99.diff` exactly: `4632bac0ba2cc10fe7b31ea88176c3b13ddd97b2` (1,549 bytes). Applied patch cleanly to scratch copy; patched blob `54c13bc9a5edb50f3cf31470e04d055d874d5394`. Synthetic EPUB has Appendix A/B headings and masses; synthetic CSVs have two A and three B rows. Each case ran `python3 -I -B` in a temporary folder. `pinned_full_csv_match` is a SHA-256 comparison with the fixture's unmodified baseline B CSV, **not** a real TAM source rebuild.

| Synthetic B case | Committed proposed checker exit | Checker + PATCH-99 exit | Pinned full-CSV equality |
|---|---:|---:|---|
| baseline | 0 | 0 | match |
| header only | 0 | 1 | differs |
| truncated to one valid data row | 0 | **0** | differs |
| changed ratio, mass unchanged | 0 | **0** | differs |
| changed registry sign, mass unchanged | 0 | **0** | differs |
| changed mass to absent value | 1 | 1 | differs |
| empty CSV | 0 | 1 | differs |
| wrong header | 0 | 1 | differs |

**Observation:** PATCH-99 correctly rejects empty/header-invalid inputs, but both versions accept a truncated, valid-row CSV and changes to non-mass columns. Full-byte equality rejects these synthetic changes. **Interpretation:** keep PATCH-99 as a quick consistency gate, not a complete source-integrity gate. Full CSV sha256 comparison against a deterministic rebuild from a separately pinned source commit is necessary to detect altered/truncated delivery files. It is not sufficient to authenticate the source pin itself. **Limitations:** these eight fixtures are synthetic; no real TAM EPUB, pandoc, Ace, EPUBCheck, or production release pipeline was executed here. Claude §97 separately reported reproducible actual-source CSVs, but that is Claude's evidence, not a result of this run.

## Deliverables checklist (single F-001 project)

- [x] Identify public TAM source and single F-001 project plan (Claude/TJ records).
- [x] Draft reproducible EPUB/PDF/CSV build and review gates (Claude, PROPOSED; not adopted).
- [x] Independent synthetic characterization of PATCH-99's scope (this run).
- [ ] Jointly review and integrate selected patches into an approved build branch (no overwriting).
- [ ] Bind EPUB, PDF, Dataset A CSV, Dataset B CSV to pinned source/build receipt; verify four hashes from a clean rebuild, with editorial approval bound to final artifact hash.
- [ ] Complete source/rights/claims editorial review and accessibility validation on the final build.
- [ ] Resolve Timothy A1–A6, B6 and any other release-blocking choices; B7 is optional and nonblocking.
- [ ] Obtain Timothy's explicit approval before storefront creation, outreach, publication, spending or payment setup.

**Acceptance criteria:** (1) documented source commit and permissions; (2) all four delivered artifacts reproduce or have documented exceptions (PDF byte determinism still open); (3) CSV rows/columns match pinned rebuild, including non-mass fields; (4) appendix quick gate, listing and accessibility checks fail closed on altered/absent files; (5) no unsupported claims; (6) credit, licensing, terms and pricing approved; (7) Timothy authorizes any actual launch. Passing synthetic tests alone does not satisfy these criteria.

**Next action:** Claude and GPT compare §94/§97 four-hash receipt and PATCH-99 with the joint review checklist, **without new product work or premature adoption**. On Timothy's answers, finish editorial signoff and build a final review edition. Questions awaiting Timothy remain A1–A6 and B6; B7 tracked separately. No publication, account creation, payments, outreach, spending, paid inference, or Cloudflare loops.
