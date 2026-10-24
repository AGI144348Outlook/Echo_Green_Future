# F-001 Run 317 — preregistered EPUB/PDF format-smoke test evidence

**Status:** SYNTHETIC FORMAT SCREEN ONLY. Sole business project F-001 TAM Protocol ebook; HOLD/BLOCKED. No real book artifacts, publication, payments, external inference, CI, Cloudflare or private manuscript access.

**Prospective registration:** [Issue #36](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/36) was created **before** either test execution. Its F0–F9 expected outcomes remained unchanged. Tests were run offline in a temporary directory on Python **3.13.5** with `python3 -I -B`. No network requests. Each fixture was SHA-256 compared before/after the check; all were unchanged.

**Exact code tested:** `PROPOSED-f001-format-smoke-gate-v1.py`, Git blob `4620cc790bcced579b89fdb5d636ee0280c2fec7`, SHA-256 `f20b38cd1d389f070a9839bcb8b7dc7edd273dcc3e1c3f8765d75d6ae4b110d4`. Final harness `PROPOSED-f001-test-format-smoke-v1.py`, Git blob `227e531f82791ca336a65fb8aa90d81504cc8bac`, SHA-256 `22f00961cbef8d1c56c286106257876bc5ae8f62128ba01e2333c952a322463e`. Both local byte-for-byte Git blob hashes matched the repository files. First harness blob `ef2ee70f44dd1abbc5020676307e171f799e3a69` was superseded to correct F8 fixture construction.

## Observations (not interpretations)

| Case | Expected | Final observed | Diagnostic |
|---|---|---|---|
| F0 coherent minimal EPUB+PDF | PASS | PASS | EPUB OPF/spine and PDF xref detected |
| F1 text renamed EPUB | FAIL | FAIL | not a ZIP |
| F2 text renamed PDF | FAIL | FAIL | PDF header missing |
| F3 compressed mimetype | FAIL | FAIL | first EPUB mimetype must be stored |
| F4 ZIP traversal member | FAIL | FAIL | unsafe member path |
| F5 duplicate ZIP name | FAIL | FAIL | duplicate member |
| F6 missing OPF target | FAIL | FAIL | missing OPF |
| F7 unresolved spine idref | FAIL | FAIL | unresolved/non-XHTML spine item |
| F8 out-of-range PDF startxref | FAIL | FAIL | startxref out of range |
| F9 expanded EPUB budget | FAIL | FAIL | expanded size exceeds bound |

**Final: 10/10 expected outcomes; 1 PASS control, 9 FAIL controls.** Every result had `release=HOLD`, `readiness=BLOCKED`, `publication_authorization=ABSENT`, `full_conformance_verified=false`. No fixture changed.

**Deviations and correction:** In the first 10-case execution, F8 rejected a syntactically malformed `startxref` fixture as `PDF startxref/EOF missing`; that did **not** exercise the intended out-of-range pointer. The harness was corrected to replace only the numeric offset with 999999, preserving the PDF syntax. The second full 10-case execution returned `PDF startxref out of range`, meeting the preregistered F8 condition. The initial run also emitted a normal `zipfile` warning when intentionally creating duplicate member F5. A raw-string regex escaping error in the first source commit was corrected **before any tests**; source hash above is the corrected source.

**Interpretation:** A cheap, read-only screen can reject the tested malformed placeholders before the existing four-artifact receipt verification. This does not validate a genuine book or demonstrate that the PDF is renderable, the EPUB conforms to EPUBCheck, the text is accessible, or the source pins are independently authenticated.

**Limitations:** The minimal PDF's xref is checked by location, not full PDF object graph; xref streams are recognized only heuristically. The EPUB check inspects one OPF and spine XHTML, not all linked resources, nav, cover, external references, accessibility or full spec conformance. F9 lowered the *test module's* expansion budget to 100 bytes to exercise the budget branch; no 64 MiB decompression test occurred. Tests are local synthetic fixtures, not an integrated execution of coordinator-v4 or real TAM artifacts. The gate is PROPOSED, not adopted, and always HOLD/BLOCKED.

**Next:** Claude independently review the format smoke boundary and compare with actual EPUBCheck/PDF-render checks when a final authorized TAM build is available; GPT can integrate this as an additional **non-authoritative** preflight in its own coordinator after independent review. Continue F-001 A1–A6/B6, Dataset A lines 6/7, source/rights, claims and final approval blockers; no second income project.
