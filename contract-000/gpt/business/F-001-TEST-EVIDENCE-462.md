# F-001 Run462 — prospective Issue #143 and observed source-location audit

**Scope:** same sole F-001 TAM Protocol speculative research-notebook ebook. HOLD / NOT LAUNCH-READY. [Prospective test entry](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/143) was published before any Run462 executable diagnostic. The code and all 82 results are GPT-owned, non-main; no editorial text was rewritten.

## Inputs and method

- Exact 82-row register `F-001-EDITORIAL-DECISIONS-458.tsv` Git blob `300dfcf0ba9e9d236326d09b2a4b6c5467d3874c`, all rows `PROPOSED_NOT_APPROVED`.
- Eight actual **primary** TAM source files at `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; connector-returned blob IDs matched the pinned Git tree **8/8**. The current TAM `main` tree also resolves to that same commit (11/11 source files unchanged). This is GitHub source metadata, not a local `git hash-object` replay.
- Read `library-shared:Business/ideas/F-001-candidate-ebook-gumroad.md@cb125a1`, but it is the 159-section **project progress document**, not the primary TAM text. **Deviation from initial plan:** use the eight primary TAM source files for occurrence-to-sentence mapping; do not misidentify a match in the progress document as manuscript evidence.
- Reimplemented the exact `claim_scan.py` sentence splitting expression `(?<=[.!?])\\s+|\\n{2,}` in JavaScript. For each `<filename>#S<number>`, retrieve the indexed primary-source sentence. Verify all ten `same_text_as` exact-copy links by equality of full sentences. The excerpt diagnostic compares normalized short quote to full source: `LITERAL` if contained, `PREFIX` if its first 28 normalized characters are contained, otherwise `MANUAL`. **These labels are search aids, not correctness or historical-verification ratings.**

## Observed (V8, actual connector source content)

**82/82 occurrence IDs resolve to an existing primary-source sentence; 8/8 source blobs match; 10/10 duplicate-copy links equal exactly.** Quote search-aid classes: **16 LITERAL, 23 PREFIX, 43 MANUAL**. The 43 MANUAL are *not* missing source sentences; many quotes are editorial paraphrases, punctuation variants, markdown prefixes or truncated summaries, and require human contextual review before an overlay. All 82 remain proposed and unapproved. No textual edits or publication occurred.

Per source: README 5 (2/2/1 literal/prefix/manual); Article 1 4 (1/3/0); Article 2 7 (5/0/2); Color/Dental 6 (1/4/1); Article 5 6 (0/6/0); Article 6 6 (1/1/4); Article 10 4 (0/2/2); Collective 44 (6/5/33).

**Six V8 checks passed:** (1) real 82-row positive map, (2) out-of-range `README.md#S9999` rejected, (3) changed duplicate target rejected, (4) missing Article 10 rejected, (5) wrong Article 10 source blob rejected, (6) forged `APPROVED` label rejected. No failed final checks. The negative cases mutate in-memory fixtures, not repository files.

## Interpretation, limitations and next action

The register is **structurally traceable** to the pinned public TAM corpus. This does not establish that 82 proposed editorial conclusions are correct, that an excerpt is verbatim, or that historical claims are sourced. The exact full-source sentence is available for all 82 IDs and can be displayed to Timothy before approval; the `MANUAL` class requires review, not automated rejection. This audit uses connector-provided UTF-8 strings and Git blob IDs; the committed JavaScript audit core was executed by V8 with real data, but no standalone Node CLI or original Python scanner was run here. No EPUB/PDF, EPUBCheck or Android QA was executed.

**Next:** Claude independently inspect the 43 MANUAL excerpt mappings and identify any genuinely incorrect context; ChatGPT can prepare a **separate approval-controlled overlay** only after explicit Timothy decisions, current-source contextual recheck and independent validation. Preserve all 82 original proposals and HOLD.
