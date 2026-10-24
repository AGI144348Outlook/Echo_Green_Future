# F-001 Run 320 — dual-format composition test evidence (2026-10-24 CT)

**PRE-TEST PUBLICATION:** [Issue #39](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/39) was created 2026-10-24 10:02:20 UTC **before** local execution. This file is the post-execution evidence record; it does not retroactively alter the predictions. All tests used synthetic local files and no CI, paid inference, Cloudflare, network calls, publication or real manuscript artifacts.

**Exact source identity:** tested and committed wrapper Git blob `0980844b3c0d0419485ee0ea81f428641ba93a2f`; tested and committed C0–C6 harness Git blob `cc41920de4b8bcbf8d2e4b73a670c07f8f2b64e4`; smoke gate blob `4620cc790bcced579b89fdb5d636ee0280c2fec7`; supplement v2 blob `96223a9ad1f43910c18b670e43b51ed266d1b854`. The local source blobs were checked against these values, and the two new GitHub uploads were independently fetched to confirm their blob SHAs matched. Fixture-generation helper is the unchanged Run 317 `PROPOSED-f001-test-format-smoke-v1.py` from its archived handoff; it was imported for `epub_bytes` and `pdf_bytes`, **not** used to rerun Run 317's F0–F9 suite.

**Method:** Python 3.13.5, command `python -I -B PROPOSED-f001-test-dual-format-preflight-v1.py` from a local scratch directory. Harness copies the wrapper and both exact-pinned gate sources to per-case private temporary folders; creates a synthetic EPUB/PDF pair; for C4 substitutes a symlink, for C5 appends a marker to the supplement source. It invokes the wrapper as a subprocess and checks JSON output, exit code, HOLD/BLOCKED, absent publication authorization, and SHA-256 equality of all tracked regular files before and after. Each wrapper checks both EPUB/PDF inputs **once**, then passes identical bytes to both pinned gate checkers.

| Case | Prospective expected | Observed | Specific evidence |
|---|---|---|---|
| C0 coherent EPUB/PDF | PASS/HOLD | **PASS/HOLD/BLOCKED** | Both gates PASS, input SHA-256 unchanged. |
| C1 container references missing OPF | FAIL/HOLD | **FAIL/HOLD/BLOCKED** | Smoke: missing/unsafe EPUB OPF; supplement: PASS. |
| C2 Unicode NFC/NFD filename collision | FAIL/HOLD | **FAIL/HOLD/BLOCKED** | Smoke PASS; supplement: NFC/casefold-colliding EPUB members. |
| C3 invalid PDF startxref | FAIL/HOLD | **FAIL/HOLD/BLOCKED** | Both gates FAIL: out-of-range/invalid pointer shape. |
| C4 final-component EPUB symlink | FAIL/HOLD | **FAIL/HOLD/BLOCKED** | Preflight rejects with OSError ELOOP; no symlink followed. |
| C5 tampered supplement script | FAIL/HOLD | **FAIL/HOLD/BLOCKED** | Source pin mismatch; appended `TAMPER_EXECUTED` marker never ran. |
| C6 forged PDF markers, no real object graph | possible PASS, known limitation | **PASS/HOLD/BLOCKED** | **Observed false positive**: both heuristics PASS; release still HOLD. |

**Total:** 7/7 preregistered expectations matched; zero failed assertions, zero timeouts, no input modifications and no test-plan deviations observed. **Interpretation:** the composition adds coverage across the two gates and verifies source-byte pins, but does **not** establish PDF validity. C6 is a confirmed *false positive* against the intended broader notion of a valid PDF; it is deliberately retained as a negative control, not counted as PDF validation success.

**Selected per-run SHA-256 evidence:** C0 EPUB `5ccb1a8b5235a8af48ae53ae4dd19434000537d0b8631c8ab301caa19149a8ca`, PDF `c053eb237d043f105babfd4f0446864050c091dc05bf61fb6508347a9499e5ac`; C2 collision EPUB `f45adeaa8975f105583f6b67dddb20413b7141e66cd698da28c7037314946f74`; C6 fake PDF `99001c57140363a3c2f78c8a6bd129621e1b8435c7553ed4156b3c64b2d3798a`. Fixture generator uses ZipFile's default current timestamps; cross-run EPUB byte SHA-256 may vary, so these hashes identify this execution's bytes, not a frozen fixture corpus.

**Limitations:** synthetic only; no genuine book EPUB/PDF, EPUBCheck, PDF object graph parser/render, accessibility, rights/claims/editorial dispositions, source authentication or publication approval. In-process execution of reviewed pinned gate code is **not** an isolation sandbox. Ancestor directory substitution and hostile same-UID actors remain outside the boundary. Source Git hashes attest equality to selected repository blobs, **not** independent source authenticity. The wrapper is a proposal, not integrated with the existing staged receipt/coordinator or Claude's shared F-001 build.

**Next:** ask Claude to review this integration and challenge C6, ZIP64/data-descriptor edge cases, symlinked ancestors and fixture determinism. Maintain the same F-001 deliverables checklist and HOLD. No operational Genesis/A-000 code changed.
