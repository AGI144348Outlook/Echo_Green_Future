# F-001 TAM Protocol ebook — authoritative source and build-path recovery (Run594, DRAFT)

Project **F-001**, unchanged. **HOLD / NOT LAUNCH-READY**. This document resolves the earlier “original plan path unknown” blocker; it is not a test result or publication authorization.

## Recovered authoritative planning records (read from `library-shared`)
- `Business/ideas/F-001-candidate-ebook-gumroad.md`: original detailed project plan, including section 9.1's seven-stage workflow; read its initial product and workflow sections in this run. Existing plan stays authoritative, not superseded by the GPT release manifest.
- `Business/ideas/F-001-decision-sheet.md` (blob `2975edcc4cae8a17499e873b68ba75f5c39ea527`): A1–A6 remain pending. Defaults are **draft placeholders**, not Timothy's approvals.
- `Business/ideas/F-001-gpt-checklist.md` (blob `69449fceac9d4b7b5ac516318c685ec610fdd6df`): GPT packaging and checksums; Claude editorial/listing.
- `Workshop/README.md` (blob `d39dcb35cb4ef7bdf226ded0e907a0f2d7426ab0`) and `Business/README.md` (blob `99feb4684bbf03ac3d900b592538cba6754ff3c6`): shared wings inert; public metadata only, no private financial/customer information.

## Actual existing build entrypoints located (path inventory, NOT executed)
`library-shared:Business/ideas/F-001-tam-build/` includes `build.py`, `build_pdf.py`, `epub_check.py`, `claim_scan.py`, `listing_check.py`, `ledger_map.py`, and `ledger_merge.py`. These are historical tools, **not** evidence that current packaging or sales readiness passes.

## Acceptance-to-deliverable map
| Deliverable | Acceptance condition | Evidence/state |
| --- | --- | --- |
| Source selection | A1/A6 approved; source commit pinned; rights and license verified | OPEN |
| Editorial | Claude independently resolves claim ledger, article gaps, quotations and listing text | OPEN |
| Technical regression | #262, #258, #256, #229 preregistered checks run on pinned bytes, same-thread actual observations | UNEXECUTED in this run |
| PDF | Accessible file, stable edition identifier, hash, TOC and page/claim parity | NOT VERIFIED |
| EPUB | Accessible EPUB, validator result, navigation/metadata and hash | NOT VERIFIED |
| Android | Open, navigate, search/reflow and screen-reader evidence | NOT VERIFIED |
| Sales release | Timothy explicitly resolves A1–A6 and authorizes publication | NOT AUTHORIZED |

## Next concrete GPT action
Fetch and fingerprint exact runner and fixtures for #262, confirm issue preregistration precedes execution, then run only the preregistered checks and report observed results in **that same issue**. If tools cannot obtain a byte-verifiable executable, do not claim a run. Claude owns editorial/rights; GPT owns packaging and checksums. No new pipeline or spending.
