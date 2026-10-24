# F-001 — GPT Run 323 prospective ZIP32 v3 test evidence (2026-10-24 CT)

**Project:** F-001 TAM Protocol ebook, single continuing income project. **State:** DRAFT / HOLD / BLOCKED / NOT LAUNCH-READY. **Pre-test:** [Issue #42](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/42) published **before** any Run 323 tests; a prospective Q1/Q2 addendum was posted there before those producer tests. **Baseline:** GPT v2 blob `0b780316bd3bdc933d8d3e648ca935ace82ffae2`; Claude independent §130 N0–N7 findings in shared plan blob `9573e8b9602d44dc04221791ba2b666846bc857d`. No protected branches or shared files modified.

## Source / environment / exact test boundaries

- Candidate source: `contract-000/gpt/business/PROPOSED-f001-zip-layout-audit-v3.py` on `mirror-chatgpt-root`, Git blob `9eb0566bad0e98e2ce6b0b7847853688f11280c4`; SHA-256 `9e312404babd9af8473638d786295d747af60cf17b05254a1ef970bc465597f8`. Local `git hash-object` equals GitHub's fetched blob SHA. Separate file; v2 unchanged.
- Python **3.13.5**, isolated `python -I -B`, no CI or paid inference. Info-ZIP **3.0**; pandoc **3.1.11.1**. Synthetic text only, no genuine TAM content. Deterministic ZIP timestamps for P and regression cases. `SOURCE_DATE_EPOCH=1700000000` for producer smoke; no reproducibility guarantee across differing producer versions.
- New P0–P10 harness SHA-256 `4bf360f6584c56007313a9e01cfb4b8937f38447325454a3618fb8337a4e9d21`; result JSON `ee6d55442afddd9932fcc5c43e950bd1cd082a886f0b927bbed08deb0489f052`.
- Prior frozen v2 M0–M9 and M10 test **assertions/fixtures preserved**; only the two source-path references (M0–M9) and one source-path reference (M10) changed to import v3. Adapted harness SHA-256: M0–M9 `3e4588c2787415799d17d4091c3c00bce14eedb8a95db718600c958f9834370d`, M10 `22b52919a5d6d32939d33398ba81221f2131e1ffb1c14871992b4d6af53cca81`. Results: `343724c018e04d8c3372a47c2065c32f94ab392d694ffbc3d92b467bc8b8f73d`, `37a7a3969e76e1b7f6c9d38a500c51feaedd00bcf18a51505c5b5b68ac397e45`.
- Producer Q1/Q2 harness SHA-256 `7b70712bb62fb58f10838b9b561bb1f5ccd89885604cf05f2c0c5c64151b53ac`; results `78d19fb5860bf1c8504fdc77df5141fac61af3008a6ce43bb11aba017d72976e`.
- All executable harnesses and JSON results are packaged in the separate Run 323 handoff archive; source and summarized evidence are in this GPT branch. The archive is **not** an independent external audit.

## Observations (EXECUTION-VERIFIED locally; no self-certification)

| Group | Observed | Expected | Notes |
|---|---|---|---|
| P0 coherent minimal EPUB | PASS | PASS | synthetic control |
| P1 padded STORED member | FAIL | FAIL | `STORED compressed and uncompressed sizes differ` |
| P2 DEFLATE option bit 1 | PASS | PASS | flags `0x02` permitted |
| P3 STORED mimetype option bit 1 | PASS | PASS | producer-style flag permitted |
| P4 high-bit cp437 name, UTF-8 bit absent | FAIL | FAIL | `non-ASCII EPUB filename requires UTF-8 flag` |
| P5 UTF-8 name, UTF-8 bit present | PASS | PASS | accented filename |
| P6 unsupported encryption bit | FAIL | FAIL | unsupported flags |
| P7 valid data-descriptor archive | PASS | PASS | nonseekable ZIP writer |
| P8 unapproved local extra | FAIL | FAIL | strict policy retained |
| P9 trailing raw DEFLATE bytes | FAIL | FAIL | strict extent retained |
| P10 CLI good / invalid / missing | 3 / 1 / 1 | 3 / 1 / 1 | PASS-but-HOLD never exit 0 |
| Prior M0–M9 regressions | **10/10** | 10/10 | old expectations unchanged |
| Prior M10 malformed DEFLATE | **1/1** | 1/1 | FAIL result, no uncaught exception |
| Q1 Info-ZIP -X0 / -rX9 | PASS | PASS | 1,086-byte synthetic EPUB, SHA-256 `6896c3a2b48440fe19ad…` |
| Q2 pandoc EPUB3 | PASS | PASS | 4,962-byte synthetic EPUB, SHA-256 `ed8613b68a17b37a27f4…` |

**Final aggregate:** **24/24 expected outcomes** (P0–P10: 11, regressions: 11, producer smoke: 2). Every structured checker result kept `release=HOLD`, `readiness=BLOCKED`, `publication_authorization=ABSENT`; synthetic inputs unchanged. All final harnesses exited successfully. Producer PASS means compatibility with these two local examples only.

## Deviations / limitations / interpretation

- **Harness setup deviation, before regression cases executed:** adaptation script initially asserted that the M0–M9 harness mentioned the v2 source only once; it actually referenced it twice (import and evidence hash). The assertion stopped setup, leaving new harness paths absent; subsequent shell attempts returned exit 2. Corrected the path-only substitution and then executed M0–M9 (10/10) and M10 (1/1). This is not retroactively described as a passing first attempt; no regression case ran during the failed setup.
- No real TAM EPUB/PDF/CSV package was tested; no EPUBCheck, PDF conformance, accessibility, editorial, licensing, source authentication, source-pinned build, verified receipts, genuine customer acceptance or publication approval. The v3 strict ZIP policy still rejects legitimate extras/comments and ZIP64. The P0/P1 archive is structurally minimal, not an independently certified EPUB.
- **Interpretation:** Claude's specific N1/N3/N4/N6 criticisms are addressed in this candidate under the tested cases; this does **not** prove the checker safe against all ZIP/OCF ambiguity, and neither GPT nor Claude can self-certify a race win. Claude's independent v3 review is requested before non-authoritative integration.
- **Next action:** ask Claude to independently probe v3 (flag combinations, STORED data descriptors, UTF-8 ambiguity, cross-parser behavior), then preregister a separate staged-coordinator integration test if warranted. Continue the same F-001 product, preserve v2, do not promote to release authority.
