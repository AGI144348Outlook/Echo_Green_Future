# F-001 — 09Z rights-gate interface refinement (DRAFT, NOT TESTED)

Single project: **F-001 TAM Protocol ebook**. HOLD, not launch-ready. Read shared F-001 §209 on `library-shared` (Git blob 55e01798) after prior 08Z acceptance fixtures. Claude identified the real inconsistency: earlier fixture 10 used band S despite §181's numeric bands; corrected synthetic fixture uses B0. Preserve original evidence as erratum rather than silently rewriting it.

## GPT-owned validator contract v3 (proposal)
1. Require pinned source Git blob SHA, explicit immutable `as_of` UTC, canonical worksheet bytes (NFC UTF-8 LF, sorted passage IDs, final LF), and separately verified Timothy-controlled attestation binding the worksheet SHA-256; never equate Git blob SHA with worksheet SHA-256.
2. Parse source ranges strictly as `L1:C1-L2:C2` (positive decimal integers, no leading zeros, inclusive Unicode codepoint columns); reject reversed or malformed ranges as `noncanonical_source_range`. Reject out-of-bounds against the **pinned source bytes**, not a mutable checkout, as `source_range_out_of_bounds`.
3. Derive length band from the inclusive span (crossed LF counts 1): B0 <40; B1 40–99; B2 100–199; B3 200–299; B4 >=300. Reject mismatches with `length_band_mismatch`. These categories are for source triage only, not proof of copyright permission.
4. Preserve the §209 six synthetic variants as expected-case fixtures, including the deliberately invalid §208 band S; do not count them as GPT-executed. No private source text or personal financial data in public records.
5. Eligibility from synthetic positive fixtures means **editorial review only**, never publication. Any unknown rights, conflicting evidence, absent attestation, inaccessible packaging, or absent explicit Timothy approval => HOLD.

## Deliverables and acceptance
- [x] Single F-001 project and release HOLD preserved.
- [x] Rights-gate v2 fixture specification preserved.
- [x] Proposed source-range and B0–B4 acceptance contract documented (this artifact).
- [ ] Implement strict source-bound validator on GPT-only branch; preregister before execution.
- [ ] Run prospective fixture suite with byte-for-byte source replay and report same-thread evidence.
- [ ] Claude: reconcile 69 rights units and 82 editorial decisions against pinned manuscript (human rights decision required).
- [ ] Build accessible PDF/EPUB and listing parity; no public listing yet.
- [ ] Timothy: choose authenticated attestation mechanism, decide scope A1, approve release explicitly.

**Next action:** implement a fail-closed, pure-stdlib parser and negative-case fixture harness, then preregister it before testing. Claude owns worksheet/editorial; GPT owns validator and tests; Timothy owns rights and launch. No account creation, outreach, publication, payments or spending.
