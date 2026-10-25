# F-001 — GPT Run 353 package-evidence shape gate: prospective test and actual results

**Single continuing project:** F-001 TAM Protocol ebook. **Status:** HOLD / NOT LAUNCH-READY. **Prospective PRE:** [Echo_Green_Future Issue #53 comment 6401236705](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6401236705) was published before tests. **POST:** [Issue #53 comment 6401266250](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6401266250) documents actual results in the same thread. No CI, paid API, publication, account, outreach or payment.

## Problem and scope

Run 352's isolated staging receipt validator passed 16/16 synthetic decisions, but a stage receipt is not a package verification or authorization. The new standalone [shape gate](F-001-PACKAGE-EVIDENCE-GATE-353.py) checks only a proposed *candidate manifest* for exact schema, fixed F-001 identity, `HOLD` and `NOT_GRANTED` status, canonical book UUID, pinned TAM source `d46456a` and dataset CSV hashes, EPUB/PDF hash and positive-size fields, and eight evidence digest fields (editorial, rights, attribution, independent rebuild, EPUBCheck, Ace, PDF review, listing parity). The gate **never outputs READY**. A structurally complete manifest returns `STRUCTURE_VALID_ONLY`, **not** `VERIFIED` or `APPROVED`. Synthetic placeholders are not real evidence.

## Reproduction and observations

- Platform: Linux, Python 3.13.5; `python3 -I -B F-001-PACKAGE-EVIDENCE-TEST-353.py` with the gate alongside it. The [committed harness](F-001-PACKAGE-EVIDENCE-TEST-353.py) uses only synthetic dictionaries and temporary JSON files.
- **21/21 synthetic checks PASS**: valid review-only candidate accepted as structure-only; attempted release READY and GRANTED authorization rejected; wrong project, extra/missing keys, absent PDF, invalid/uppercase hashes, boolean/zero/oversized byte sizes, wrong TAM source and CSV pins, stage READY, missing/placeholder rights, noncanonical UUID, duplicate JSON keys, NaN, and input exceeding 64 KiB rejected.
- **2/2 CLI smoke checks PASS**: complete synthetic candidate returns exit 0, `STRUCTURE_VALID_ONLY`, `release=HOLD`, `publication_authorized=false`; attempted READY returns exit 1, `REJECTED`, `release=HOLD`, `publication_authorized=false`.
- Source provenance checked after upload: exact local Git blob SHA-1 matches GitHub [gate](F-001-PACKAGE-EVIDENCE-GATE-353.py) `a5d3535860a488af090f3b25cc72fcd347ef0aef` (4,164 bytes) and [harness](F-001-PACKAGE-EVIDENCE-TEST-353.py) `1b7302faa8a5e7b99f01b3fe313007ee1f35d378` (3,937 bytes). No deviations or observed test failures.

## Interpretation, limitations and next action

**EXECUTION-VERIFIED only for the synthetic structure/CLI behaviors above.** The gate does **not** open or hash actual EPUB/PDF files, attest report authenticity, authenticate an independent reviewer, verify the actual source rebuild, certify a licence, resolve disputed TAM claims or grant human publication approval. A malicious or mistaken submitter can fill every digest field with plausible-looking hashes; `STRUCTURE_VALID_ONLY` is intentionally not a trust decision. It also does not replace the pinned stage coordinator, and the full Run 351 coordinator and real TAM pipeline remain **NOT RUN** in this environment (GitHub raw hostname DNS unavailable).

**Next single GPT action:** independently materialize the actual TAM package and source-pinned dataset stage; build an evidence-to-bytes verifier that hashes the real EPUB/PDF and reports, checks editorial/rights decisions and links to a separately pinned rebuild. Do not promote to release. Claude should review the manifest evidence categories and continue editorial/listing/rights, without overwriting GPT-owned work. Timothy's A1–A6/B6/C1, Dataset A rows 6/7, Gerah, claims, exact licence/credit/book ID and explicit publication authorization remain pending.
