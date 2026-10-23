# F-001 — GPT progress Run 301, 2026-10-23

**Sole legitimate income project identifier:** `F-001` — TAM Protocol research ebook. **Status: ON HOLD**, no sale/listing/account/publication/outreach/spending/payments. Read the current shared plan `Business/ideas/F-001-candidate-ebook-gumroad.md` blob `2bfe9cd511b245669d10e9db2dfeb95fe1f5b950` (§107), shared decision sheet blob `2975edcc4cae8a17499e873b68ba75f5c39ea527`, `APPLY-ORDER.md` blob `8e76d2a628b9c7d594ec3a4ace1d6ce334e317f4`, and previous GPT `RUN-300-CHECKPOINT.md` blob `25223393ef90ec0a73a96a0c0b76b5b302a3eb25` before work. No new income pipeline started.

## Coordination with Claude

Claude §107 independently characterized v2 on public-source-derived Dataset A (19/20 expected); its nested-JSON V19 failed to emit structured JSON because `RecursionError` escaped. Claude proposed catching that error and noted exit-0 dual status and caller-supplied source pin. GPT independently prepared **v3**, a separate unintegrated proposal, keeping v2 intact. V3 catches `RecursionError` and proposes a 1 MiB editorial record limit (stat check plus post-read check). Git blob `aa632bf3c8144a2c8fa0308ba7fc88c8fe9a1102`, commit `f6f09f4120c4781b454f364ef3ee2022d7f6d48b`. Pre-test Issue #13 [6367846503](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6367846503) preceded **8/8** local synthetic characterization outcomes; post-test [6367896126](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6367896126). No production script adopted or public release made.

## Deliverables checklist

- [x] Preserve single F-001 project plan, comparison and decision sheet; no second business.
- [x] Public-source Dataset A/B reproducible rebuild evidence: six/eight data rows; two Dataset A numerical discrepancies remain.
- [x] Read-only integrity gate v4 (Claude independently reproduced 16/16) and receipt v1.1 draft, both unintegrated.
- [x] Editorial-disposition v1/v2 parser proposals and independent Claude §106–107 review.
- [x] **New v3 hardening proposal and 8/8 synthetic tests**, exact Git blob verified; no release-ready status introduced.
- [ ] Claude independently review v3 JSON bounds/RecursionError handling, including whether 1 MiB is appropriate; source-pinned receipt integration remains unadopted.
- [ ] Authenticate Timothy's editorial decisions on Dataset A CSV lines 6 and 7; update explanatory product text without silently changing source claims.
- [ ] Independently rebuild and verify four deliverables: **EPUB, PDF, Dataset A CSV, Dataset B CSV**, with exact byte counts, SHA-256 values, build inputs, scripts, patch order, accessibility/claim checks and release receipt.
- [ ] Resolve A1–A6/B6 (product scope, storefront, exact credit, framing, terms, licence/source and identifier), rights and editorial signoff; require separate explicit Timothy authorization for publication, account creation or payments.

## Acceptance criteria, next action, blockers

**Release acceptance:** All four artifact hashes and source/script pins independently reproduced; CSV byte integrity and editorial decisions tied to authenticated source records; claim and accessibility checks reviewed; correct licence/credit/price/refund terms; independent second-participant verification; Timothy explicitly authorizes any publication or transaction. A parser's exit 0 or syntactic completeness is never approval. **Next GPT action:** request Claude's v3 review, then design a read-only integration that obtains expected Dataset A digest from an independently pinned rebuild receipt rather than from the caller's generated CSV. **Next Claude action:** review v3 size-bound policy and continue manuscript/claim/listing review in Claude-owned records. **Timothy blockers:** A1–A6/B6, two Dataset A editorial dispositions, rights/credit and publication approval. No paid inference or autonomous Cloudflare loops.
