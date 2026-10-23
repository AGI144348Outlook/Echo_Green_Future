# F-001 — GPT progress Run 303, 2026-10-23

**Sole income project:** `F-001` — TAM Protocol research ebook. **ON HOLD**; no new business pipeline, account, publication, outreach, spending or payment. Continued from GPT Run 302 and Claude's shared F-001 §§109–110.

**Read before work:** Current Contract-000, R1–R7, DISC-002, shared Library tree `5d3f5cdb7f90f022448f0659aab6e10df7aed536`, shared plan blob `364ccdf89bea6df419bc993fbbbb92e26259e414`, decision sheet `2975edcc4cae8a17499e873b68ba75f5c39ea527`, `APPLY-ORDER.md` blob `43e9d5b40fcc78507dbcde9e70f00b6454a6342e`, GPT Run 302 checkpoint blob `24d8a4668a9b4883b7f7fb2c643f1671b27b8bf9`, v4 exact blob `c267639`, Claude PATCH-110 `a505ced` and §110 test evidence.

## Development and evidence

- **Library-first:** 63 candidates reviewed, **31 KEEP / 31 DEFER / 1 PRUNE**, no deletion; ledger commit `2d7d0ed`.
- **A-000/Genesis:** separate E11/E12 response to Claude on GPT branch `754fb53`; source reasoning only, no operational tests.
- **F-001 v5:** proposed GPT-owned descriptor-checked 1 MiB Dataset A CSV reader, dangling editorial-record symlink detection and v5 usage string; preserved v1–v4 and all Claude/shared code. Source commit `309c7f6` (blob `f8c2b4b`), nine-case harness `55b1b68` (blob `de2aa01`).
- **Tests:** prospective Issue #13 notices `6370393355` and `6370433489` preceded testing; local Linux Python 3.13.5 **16/16 regression + 7/7 overlapping IO + 9/9 new IO + 3/3 archived public Dataset A** expected outcomes (35 executions, overlapping scenarios). Archived A digest `d3c176b9…26f2`, flagged CSV lines [6,7]. All reports HOLD/unauthenticated. Detailed evidence commit `46e15fe`; post-test Issue #13 `6370467054`.
- **Receipt:** Proposed source-pinned four-artifact receipt v1.2 interface, commit `f15591b`; **not implemented/tested**. Explicitly separates source pin provenance, editorial binding, independent four-artifact verification and Timothy's authorization.

## Same-project deliverables checklist

- [x] F-001 selected; shared plan and decision sheet retained.
- [x] Reproducible archived Dataset A/B rebuild evidence retained; Dataset A numeric discrepancies remain editorial HOLD.
- [x] Unintegrated integrity gate, editorial parser v1–v5 and proposed receipt schemas documented; v5 local characterization completed.
- [x] GPT v1.2 source-pin receipt **design** and trust-boundary checklist drafted, not implemented.
- [ ] Claude independently review v5 (Linux portability, CSV symlink policy, 1 MiB bound, symlinked parents) and receipt v1.2, without overwriting GPT files.
- [ ] GPT implement and pre-test a separate **read-only receipt verifier** using independently sourced pins; require all four artifact hashes, fail closed without external source/approval authentication. No READY on parser exit 0.
- [ ] Jointly review/apply Claude's proposed patch stack in a separate authorized candidate branch and independently rebuild/validate EPUB, PDF, Dataset A and Dataset B.
- [ ] Timothy decides exact Dataset A CSV line 6 Silver Droplet and line 7 Small Scrap dispositions; verify the decision reference separately.
- [ ] Timothy resolves A1–A6/B6 (scope, rights/licensing, credit, pricing, identifier, terms) and explicitly authorizes any account creation, publication, outreach, spending or payments.

**Acceptance criteria:** four reproducibly pinned deliverables, independent hashes and build records, validated claims/accessibility/rights, no unresolved editorial discrepancies, Claude's independent review, and explicit authenticated Timothy launch approval. Until all gates pass: **HOLD**. No final production build or launch claimed.

**Next GPT:** implement source-pinned read-only receipt verifier only after prospective Issue pre-test entry. **Next Claude:** review v5 and receipt v1.2, continue manuscript/claims/listing patch stack on Claude-owned/shared records. **Blockers:** Timothy's F-001 editorial/rights/launch decisions and A-000 authority decisions (separate discourse).
