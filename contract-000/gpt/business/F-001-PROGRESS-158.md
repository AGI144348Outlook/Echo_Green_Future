# F-001 TAM Protocol ebook — GPT Run 158 (2026-10-17)

**Project:** F-001 only. **Release: HOLD.** Existing plan: `library-shared:Business/ideas/F-001-candidate-ebook-gumroad.md` §41 and `F-001-decision-sheet.md`. No new income project, account, listing, outreach, paid inference, publication or spending.

## Actual-source census (SOURCE-OBSERVED)

Read all **11/11** public text files via GitHub connector at `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; each returned blob SHA matched the pinned Git tree. The five separate article files are Articles 1, 2, 5, 6, and 10. Article 4 is not present. The infographic reference file lists three Google Drive links; their content and commercial rights were **not** opened or verified. No source content was modified.

**Claim review queue (independent JS port of Claude's published `claim_scan.py` sentence splitting and four trigger patterns):** 42 candidate occurrences across eight scanned text files: README 1; Article 1 2; Article 2 3; Color/Dental 3; Article 5 3; Article 6 3; Article 10 4; Collective 23. Exact whitespace-normalized deduplication yields **35 distinct sentences** and **7 duplicate pairs** (14 occurrences), all seven pairing Article 6 or Article 10 with Collective. This explains why `~35` is a plausible distinct-claim estimate even though the occurrence worksheet is longer. This is **not** an execution of Claude's original Python scanner; Claude should independently cross-check 42/35/7 on pinned source.

**New tool:** `f001_claim_grouping.py` (local handoff): review-only JSON claim grouping from the unchanged Claude scanner outputs. Preserves all occurrence positions, source fingerprints, original wording and triggers; hashes whitespace-normalized exact sentences to stable IDs; rejects incomplete counts, unexpected sources, duplicate positions, filled editorial decisions and malformed triggers; writes a NEW output directory only; never authorizes release. Nine synthetic unit tests passed. It must run **after** the existing independent claim-source fidelity gate, because grouping alone does not authenticate source text.

**A-000 side work:** two characterization tests passed against Dev Suite blob `f7cf465`; see DISC-002 response.

## F-001 deliverables / acceptance

- [x] Source paths and blob IDs verified (11/11, public main pin).
- [x] Independent candidate occurrence/duplicate census (42 occurrences, 35 distinct, 7 duplicate pairs; Python cross-check pending).
- [x] Review-only grouping utility and 9 synthetic tests.
- [ ] Verify actual Claude claim scanner output and group mapping against all 11 pinned files in a compatible local stage.
- [ ] Build complete manuscript with every source accounted for; independently audit actual EPUB and PDF.
- [ ] Claude editorial dispositions for all 35 unique claims, with all 42 occurrences traceable; resolve dataset precision notes, three infographics, accessibility and third-party rights.
- [ ] Timothy A1–A6 decisions, final cross-check, explicit publication authorization.

**Next action:** Claude cross-checks 42/35/7 and provides editorial classifications once Timothy's framing/source decision is resolved; GPT stages all eleven files and performs real build and artifact audits when GitHub source bytes are available in the execution environment. No false claim of EPUB/PDF completion. **Acceptance:** verified provenance, complete and accessible EPUB/PDF, editorial and rights clearance, accurate listing, approvals, then Timothy-only publication. Until then HOLD.
