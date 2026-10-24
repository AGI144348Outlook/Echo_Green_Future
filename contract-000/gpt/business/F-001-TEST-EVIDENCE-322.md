# F-001 TAM ebook — GPT Run 322 test evidence (2026-10-24 CT)

**Status:** EXECUTION-VERIFIED in local Python 3.13.5 sandbox, synthetic ZIP32 fixtures only. **Not a product release.** Prospective [Issue #41](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/41) published before tests; additional M10 was separately announced in that Issue **before** M10 execution. No GitHub Actions or deployed tests triggered.

**Source:** `contract-000/gpt/business/PROPOSED-f001-zip-layout-audit-v2.py`, final Git blob `0b780316bd3bdc933d8d3e648ca935ace82ffae2`, local SHA-256 `42042c3222f076290afb2c2d0b51dae93defb00bd78d2c06562a8f839df2533d`. Source derived conservatively from Run 321 v1 Git blob `a2360718d000bcbd09772b45a672ad63088974a8`. Final Git blob independently matched the tested local file by `git hash-object`. Harnesses likewise match tested local Git blobs: M0–M9 `6627fa1b6ea85786ca9ce8382c68ef3775aa1219`, M10 `2d459b44718e1505f62c4609ad339aecc326a92d`.

**Method:** deterministic synthetic EPUB ZIP32 archives with fixed timestamps; local read-only `check_package_bytes()` invoked in process, `python3 -I -B`, no network, private data or CI. Every test records fixture SHA-256, before/after immutability, expected/actual layout and fail-closed publication status. To reproduce from GPT branch, in the directory containing the three scripts run:

```sh
python3 -I -B TEST-f001-zip-layout-v2-run322.py
python3 -I -B TEST-f001-zip-layout-v2-m10-run322.py
```

| ID | Prospective expectation | Final observation | Fixture SHA-256 prefix | Outcome |
|---|---|---|---|---|
| M0 minimal EPUB | PASS | PASS | ca866db18469 | as expected |
| M1 local extra | FAIL | FAIL, local extra forbidden | b505d0d1dac6 | as expected |
| M2 central extra | FAIL | FAIL, central extra forbidden | 1462bbef0ad2 | as expected |
| M3 member comment | FAIL | FAIL, member comment forbidden | 8540b400b088 | as expected |
| M4 EOCD comment | FAIL | FAIL, archive comment forbidden | 2bebcf86a191 | as expected |
| M5 DEFLATE trailing payload | FAIL | FAIL, raw stream boundary | b563aaa1c1b7 | as expected |
| M6 trailing-dot member | FAIL | FAIL, unsafe portable name | 59136ee2d0c2 | as expected |
| M7 colon member | FAIL | FAIL, unsafe portable name | 2f3003dd91a1 | as expected |
| M8 data descriptor | PASS | PASS | ee92ec5ebf2f | as expected |
| M9 extended timestamp extra | FAIL | FAIL, conservative policy | ac8c4bb42778 | as expected, compatibility cost |
| M10 malformed raw DEFLATE (prospective addendum) | FAIL, no exception | **Initial uncaught zlib.error**, then FAIL after correction | 1b1c19989988 | initial failure; final pass |

**Observations:** M0–M9: **10/10** final expectations. M10: **0/1 initial** (uncaught `zlib.error: invalid block type`), then **1/1** after adding `zlib.error` to the verifier's caught exception types and rerunning both harnesses (**11/11 final**). All final cases retained `release=HOLD`, `readiness=BLOCKED`, `publication_authorization=ABSENT`; all input hashes unchanged. The initial v2 code is preserved by commit `b2db24b`, correction by `ab2312d`. A pre-execution script-generation assertion also initially assumed one schema occurrence, found two, and was corrected before writing v2; no tests were run in that preparation step.

**Interpretation (not a conformance claim):** Under the tested conditions, strict v2 closes Claude's §129 L3–L7 synthetic counterexamples and treats malformed raw DEFLATE as a FAIL instead of an exception. It also deliberately rejects a ZIP extended-timestamp extra field (M9), which may be legitimate metadata. This is a conservative compatibility trade-off, not proof that an EPUB is invalid. ZIP64, broad OCF naming, archive comments allowed by standards, real EPUBCheck, PDF parsing, accessibility, editorial truth, licensing, authenticity, source custody, subprocess containment and production integration remain untested. A synthetically passing layout is **not** an authenticated, valid or launch-ready ebook.

**Next:** Claude independently reviews the strict policy, possible legitimate EPUB false rejections, raw-DEFLATE bounds and CLI exit 3 on HOLD. If accepted, GPT proposes integration as a **non-authoritative** staged check only after another prospective Issue. F-001 stays HOLD pending Timothy A1–A6/B6, Dataset A 6/7, source rights and provenance, genuine EPUB/PDF/CSV package, independent validation and explicit release approval.
