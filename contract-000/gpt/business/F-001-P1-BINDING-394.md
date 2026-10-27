# F-001 TAM Protocol ebook — Run394 P1 occurrence-binding receipt

**Project:** F-001, unchanged; **status: HOLD / NOT LAUNCH-READY**. [PRE/POST Issue #67](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/67). **No editorial decision approved.**

**Pinned inputs (read-only):**
- Full-sentence queue `contract-000/gpt/business/F-001-FULL-SENTENCE-QUEUE-388.json`, Git blob `06530d6729c3af39feebce9a6999650270008bf5`: 45 occurrences, 42 baseline + 3 supplemental, all UNREVIEWED.
- Proposed 18 P1 editorial treatments `contract-000/gpt/business/F-001-P1-EDITORIAL-PROPOSALS-393.json`, blob `5a4af09820c5842616cb26a3eefe3612195633d8`, all UNREVIEWED; source commit `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`.

**Executed (connector-side V8, source retrieved from GitHub, no CI):** all 89 shared Library rows matched prior ledger (separate [review](../LIBRARY-REVIEW-394.md)); 18/18 distinct P1 proposal IDs bound to an actual queue occurrence with exact source file, blob SHA, sentence number, full sentence, status, and duplicate-occurrence references. No missing proposal fields, forged approvals, or rights clearance. New reusable read-only [binding gate](f001_p1_binding_gate_394.js) and [13-case test suite](test_f001_p1_binding_gate_394.js) were run against the actual pinned queue and 12 synthetic tamper cases; **13/13 passed**. Positive case 1/1; negative controls 12/12 detected. Nine proposed-action categories were retained. Tested function was the exact source string committed to the branch; the separate test source was executed in V8 before commit. No Node CLI or actual EPUB/PDF execution is claimed.

**What passed does not prove:** correctness of empirical assertions, authenticity of the independently supplied source pins, rights, editorial authorization, final artifact contents, or that both queue and proposals were not collusively replaced. This is a *binding* gate only. External source pins and a separately authorized editorial decision record are needed before promotion.

**Next same-project action:** Claude independently evaluates the 18 P1 source-bound editorial proposals and their primary evidence. Timothy resolves A1–A6 and relevant B/C choices, manuscript rights, editorial decisions and release authorization. GPT then binds approved per-occurrence dispositions to EPUB/PDF bytes and verifies the original eight-source Python scanner and complete 334→344→347→351 staging chain. No new income pipeline or release action.
