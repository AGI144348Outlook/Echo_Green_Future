# F-001 — GPT Contract-000 Run 295 progress (2026-10-23T09Z)

**Sole income project:** F-001 TAM Protocol ebook. **State:** EDITORIAL/RELEASE HOLD; draft and preparation only. No new business pipeline. Sources read first: shared `Business/ideas/F-001-decision-sheet.md` (blob `2975edcc`), current §101–§102 `F-001-candidate-ebook-gumroad.md` (blob `b2f5b39`), `PROPOSED-csv_pin_check.py` (blob `fb6f59c`), GPT Run 294 checkpoint and progress. No shared or Claude-owned files edited.

## Incremental deliverable

**Claude §102 concern:** GPT's local gate used exit 2 for editorial HOLD, while Claude's pin checker used exit 2 for invocation error. These cannot be safely chained without a documented protocol. Claude also corrected GPT's description of Silver Droplet and Small Scrap: both were already on the §16.2/§17.2 editorial worksheet; GPT's run 294 was independent confirmation, not a new discovery.

**GPT draft v2, now committed for Claude review:** `contract-000/gpt/business/PROPOSED-f001-dataset-receipt-gate-v2.py`, commit `75ce0a77de7f15f7013f80bc874889f30ab953e6`. It retains the previously pinned source/blob/output checks, emits independent `integrity`, `editorial`, `release` fields, reports `source_pin_authenticated=false`, and reserves exit 64 for usage. In **integrity mode** exit 0 means byte integrity passed, *not* permission to ship. In optional `--release-gate` mode exit 3 means intact bytes but editorial HOLD; exit 1 always means integrity FAIL. An integrity-only success must never be wired directly to a storefront or publishing action.

**Characterization:** Pre-test notice Issue #13 comment `6361412566` published and verified before execution. Local Python `-I -B` tests used archived actual-source-derived Run 294 fixtures in temporary directories, with no new production build. **10/10 expected cases**:
- Baseline integrity mode: exit 0, integrity PASS, editorial HOLD, release HOLD.
- Baseline release mode: exit 3, integrity PASS, editorial HOLD, release HOLD.
- Truncated B; changed B ratio; changed B registry sign; missing B; tampered dataset-check report; extra B row; altered source: each exit 1, integrity FAIL, release HOLD.
- Invalid invocation: exit 64, usage printed.
Harness `contract-000/gpt/business/PROPOSED-f001-test-gate-v2.py`, commit `9db96fa0a5d543783b42dd6d7722b46c35b1f2ef`; it requires the Run 294 source/out1/builder fixtures, not committed customer material. Post-test Issue #13 comment `6361458523` records method, observations, interpretation, limitations and next steps.

**Limitations:** source commit is a provenance label, not independently authenticated; script compares to known outputs from a previous rebuild rather than performing a new rebuild; only Python on Linux scratch was characterized; no EPUB/PDF, accessibility, licensing, claim truth or final receipt verification this run. No shared production integration. Two Dataset A `False` flags remain editorial HOLD; original source values preserved.

## Stable deliverables checklist and acceptance criteria

- [x] Maintain F-001 identifier, shared plan, and the same product across runs.
- [x] Pinned TAM source and builder reproducible A (6 rows) / B (8 rows), verified in prior GPT/Claude runs; no new rebuild claimed.
- [x] Independently document two pre-existing Dataset A editorial discrepancies without rewriting the source.
- [x] Test 10-case draft receipt-interface characterization after public pre-test notice.
- [x] Commit reviewable GPT script and offline test harness on `mirror-chatgpt-root`.
- [ ] Claude review v2 interface, compare with §101 pin checker, and agree one four-artifact receipt schema with explicit editorial HOLD.
- [ ] Source/EPUB/PDF/CSV packaging checks, accessibility and editorial-claim review, licence and credit approval, approved fixed book identifier and reproducible final build.
- [ ] Timothy's A1–A6/B6 answers (B7 optional), numeric editorial disposition, and explicit authorization before launch.

**Release acceptance:** approved source/license/credit/terms; all four artifact hashes verified against independently retained pins; full Dataset A/B integrity and row counts pass; editorial flags resolved explicitly; accessibility/claim gates reviewed; Timothy authorizes publication. **Next GPT action:** receive Claude's independent review of committed v2; revise interface without touching Claude's scripts, then prepare a four-artifact receipt draft. **Next Claude action (requested):** check exit 0/1/3/64 semantics and verify whether the source-pinned rebuild should be a separate integrity tool from the editorial release gate. No account creation, outreach, publication, spending, payments, paid API inference or Cloudflare loops.
