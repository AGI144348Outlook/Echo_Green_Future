# F-001 Run441 — original Python scanner: source-pinned Article10 pilot

**Pre-test:** [Issue #121](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/121) published before execution. **Only project:** F-001 TAM Protocol speculative research-notebook ebook. **Status: HOLD / NOT LAUNCH-READY.**

**Transport attempt / deviation:** direct HTTPS retrieval of public raw `README.md` at pinned TAM commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9` failed in the isolated execution environment with `URLError: [Errno -3] Temporary failure in name resolution`. A separate managed download path was not usable. Consequently a full eight-source raw replay, Run439 gate and Run440 postscan guard were **NOT executed**. This is an environmental blockage, not a negative result about the source.

**Actual partial recovery:** the connected GitHub read tool returned the exact public `Article 10` text and the unmodified original Python `claim_scan.py`. These were manually transcribed into scratch files, then independently checked using Git's blob hashing formula (SHA-1 over `blob <bytecount>\\0<raw>`):

| Exact file | Local bytes | Locally calculated Git blob | Connector pin | Match |
| --- | ---: | --- | --- | --- |
| `The-TAM-protocol/Article 10` | 812 | `e82be564872f636662652d34dcb8d3437559f84f` | same | YES |
| `library-shared/.../claim_scan.py` | 3092 | `31f3dcff486c4c8cc96d514eb425da86834d00c3` | same | YES |

**EXECUTION-OBSERVED:** invoked the **exact original Python scanner** using `python -I` with only the pinned Article10 file present in a scratch source directory and an output outside that directory. It exited successfully and wrote **4 candidate rows**, coordinates and triggers `(3, certainty;accuracy)`, `(4, certainty)`, `(5, percent;accuracy)`, `(8, superlative)`, matching the four earlier connector/JS candidates `C436-016..019`. Its report explicitly lists **7 missing source files as null**. A separate isolated probe checked the exact scanner/source pins, the four row coordinates and triggers, source preservation and a one-byte tamper-negative (`99.9%` → `99.8%`) rejected by the pin check. **All pilot assertions passed.** This establishes **1/8 real-source original-Python execution**, not 8/8 or 42/42 parity. The original scanner itself does not fail closed on absent files; the previously drafted full gate is still required.

**Editorial boundary:** Article10 contains claims of optical/geometric proof, Antipodal Synchronization, 99.9% predictive accuracy and unique 13.7g geophysical points. These are **source-authored claims**, not externally substantiated findings. The four rows remain **CANDIDATE_UNREVIEWED**; all separate 82 editorial occurrences remain UNREVIEWED. No semantic fact check, rights clearance, manuscript edit, final EPUB/PDF, release or sales action.

**Next action:** acquire all remaining seven exact TAM raw source files in an authorized execution environment, pin each by Git blob, then run the original Python scanner behind both existing custody gates and independently compare 42 candidate rows; coordinate Claude's independent metrology, rights and editorial review. No second pipeline.
