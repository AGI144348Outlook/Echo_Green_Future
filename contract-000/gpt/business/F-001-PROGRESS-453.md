# F-001 — sole business project, Run453

**Identifier:** F-001 TAM Protocol speculative research-notebook ebook. **Status: HOLD / NOT LAUNCH-READY.** No second business pipeline.

## Incremental deliverable (GPT-owned, not adopted into shared build)
- `F-001-SCANNER-SNAPSHOT-GATE-453.py` blob `5de203a496013ed652a13a1eec828cb12d785010`: pinned Git blob check for **all eight** TAM public source files and exact original Python scanner `31f3dcf`; creates a temporary private snapshot, runs the scanner offline and returns output hashes with **status HOLD**. Refuses missing/modified/symlinked files, partial manifests, in-source output and overwriting existing output. This is a proposed gate, not a production security boundary.
- `test_snapshot_gate_453.py` blob `0e8eaacf2e4b834575e9c667d2cb0ac8d8c3b28c`: local synthetic regression harness, source SHA-verified. **11/11 PASS** after one test-harness setup error was corrected (missing synthetic target directory). Actual results in `F-001-SCANNER-EVIDENCE-453.md` and Issue #134.
- **New substantive defect:** original exact `claim_scan.py@31f3dcf` exits 0 with seven of eight inputs absent; report lists `null` for missing files and still writes a partial worksheet. GPT executed this synthetic case. A claim worksheet alone is not evidence that all sources were scanned.
- Claude's §152 reports original 8/8 Python replay and 42/42 row-level parity to GPT Run452 JS; that is **Claude-executed**, not independently replayed on the full TAM source by GPT. GPT's attempt to fetch the pinned TAM sources into the local runtime failed due DNS/no outbound network. Connector source reads succeeded; no full-source Python output hashes were produced by GPT this run.

## Deliverables checklist and acceptance
- [x] Eight source Git blob pins; JS aggregate 42 candidates (GPT Run452); Claude §152 original Python 42 rows and 42/42 field parity (not GPT-rerun).
- [x] Proposed missing-source fail-closed snapshot gate and synthetic **11/11** checks; code and harness committed to GPT-owned branch.
- [x] Source-pinned 82-occurrence editorial queue and HOLD-only draft disposition validator from earlier runs; no approvals implied.
- [x] Six-mass arithmetic and rescaling caveats from Runs 448–451; archaeological authenticity not established.
- [ ] **Independent full 8/8 original Python replay by GPT** from the pinned public source bytes, exact output hash comparison to Claude §152, and test of wrapper on real sources (blocked by local network access in Run453).
- [ ] Claude maps 34 remaining Collective queue IDs; latest §152: **48/82 proposed, 0 final**.
- [ ] Source authentication of object-level Eshtemoa masses and other asserted archaeology; rights/editorial review and Timothy's A1–A6/B1/B4/B6/C1 decisions.
- [ ] Reproducible EPUB/PDF package, receipts/checksums, Android QA, independent release gates, and explicit Timothy publication authorization.

**Single next action:** Independently replay the exact scanner with all eight pinned source bytes and the snapshot gate in a runtime that can materialize the public repository, then compare full CSV/report hashes to Claude's §152 receipts. Claude owns remaining editorial mapping and source research; GPT owns reproducibility/packaging. No accounts, outreach, publication, spending, payments, paid inference or Cloudflare loops.
