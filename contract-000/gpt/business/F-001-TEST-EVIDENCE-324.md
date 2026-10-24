# F-001 ZIP32 v4 — Contract-000 GPT Run 324 test evidence (2026-10-24 CT)

**Status:** Candidate-only / `release=HOLD` / `readiness=BLOCKED`; **not launch-ready**. All tests used synthetic text/ZIPs and local Python 3.13.5 with `-I -B`; no network, CI, paid API, real TAM book, private Testament or publication. Source read-only; no shared or protected branch edits.

## Prospective registrations and exact source pins

- [Pre-test Issue #43](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/43), published **before implementation and all Run 324 executions**: T0–T9 expectations and <3 timing ratio.
- [Exploratory timing addendum](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/43#issuecomment-6385204010) published **before** 2k/4k/8k repeats; [16k extension](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/43#issuecomment-6385207875) published **before** that execution. Exploratory work is not counted as a preregistered pass.
- Baseline `contract-000/gpt/business/PROPOSED-f001-zip-layout-audit-v3.py`: Git blob `9eb0566bad0e98e2ce6b0b7847853688f11280c4`, SHA-256 `9e312404babd9af8473638d786295d747af60cf17b05254a1ef970bc465597f8`. Retrieved from Run 323 handoff; exact Git blob confirmed by `git hash-object`.
- Candidate `PROPOSED-f001-zip-layout-audit-v4.py`: Git blob `4e295a8e0ad66cdb45148a937a2ce43fce5b0857`, SHA-256 `3bffac5a9877cc110634dcc8d5eef9b5708a2819ae722b59d1e0f8857b2a9660`. Local reconstruction matched the **final GitHub blob exactly** by `git hash-object`.
- Harness `TEST-f001-zip-layout-run324.py`: Git blob `17d14ded3a06ccb5f51a68c83b66111efe0b5950`, SHA-256 `c89bb5e27ff2b4793bb5e9eaae27c0b89d9fcbe1e074b9d6ac4f611b173b50ce`; local executed bytes matched the final GitHub blob exactly.
- **Pre-execution static correction:** initial v4 CLI error-path still labeled schema `v3`; corrected to `v4` in commit `9e7cd6a`. Initial committed harness had double-escaped ZIP signature/Unicode literals; corrected before GitHub-pinned re-execution in `b26711c`. These corrections were source/harness edits, **not** hidden post-hoc changes to T0–T9 expectations.

## Observed frozen-case results (two separate executions, not one selectively reported result)

| Case | Expected | First execution | GitHub-pinned re-execution | Interpretation |
|---|---|---|---|---|
| T0 coherent synthetic control | PASS | PASS | PASS | Baseline accepted. |
| T1 file-as-ancestor | FAIL | FAIL | FAIL | Denied as intended. |
| T2 directory-as-ancestor | PASS | PASS | PASS | Legitimate directory preserved. |
| T3 casefolded file-as-ancestor | FAIL | FAIL | FAIL | Denied as intended. |
| T4 NFC/NFD ancestor | FAIL | FAIL | FAIL | Denied as intended. |
| T5 sibling paths | PASS | PASS | PASS | No false rejection in this fixture. |
| T6 mimetype data descriptor | PASS | PASS | PASS | Known unresolved OCF conformance question, not an EPUB-validity assertion. |
| T7 2k/4k member scaling, each <5s, ratio <3 | PASS | PASS, 0.06837/0.18490 s, ratio 2.7044 | **FAIL**, 0.07472/0.22863 s, ratio **3.0598** | **Frozen timing threshold failed on re-execution; do not count as pass.** |
| T8 bad CRC | FAIL | FAIL | FAIL | Denied as intended. |
| T9 all outputs HOLD/BLOCKED, absent publication authority, unchanged bytes | PASS | PASS | PASS | No release claim. |

**Totals:** First local execution 10/10; corrected GitHub-pinned re-execution **9/10** (T7 failed). Both outcomes retained; no claim of unconditional 10/10. JSON SHA-256: first `5c974a651e1f83fc702604a8fc7f1f2f337277e77a2bf104df753c8a22ac7cda`; second `6780572ebfe0c3268509b38d3a746e7b73f9e628dfdae40266a4d64faa4f06aa`. No unexpected exceptions. Both source inputs remained byte-identical. T7 is timing-sensitive and cannot be certified from one fast run.

## Separate prospectively announced exploratory timing (not frozen-case substitutions)

Three repeats, deterministic STORED archives; medians: v4 2k **0.06387 s**, 4k **0.17850 s**, 8k **0.25693 s**; median ratios 2k→4k **2.7947**, 4k→8k **1.4394**. Isolated `zipfile.testzip()` medians 0.03401 / 0.06583 / 0.17843 s, ratios 1.9356 / 2.7105. There was an 8k v4 outlier **1.32392 s**; wall time is noisy. Diagnostic JSON SHA-256 `3139e9a5e02c6c9af7039d08150869e4488ce89fb65acf62dbb073a958cf85a4`.

Separately preregistered **16,000 STORED members + mimetype**: 1,744,134 bytes, SHA-256 `ab3f9c498ca82d39f298b86895bf1f2060b3bf2da5e41c8bb2b3c17a103a3c73`, v4 wall time **0.88596 s**, `layout=PASS`, `release=HOLD`, `readiness=BLOCKED`, input unchanged, under announced 10 s exploratory bound. JSON SHA-256 `209d95eea26c324ea53bb7c22466080345bb6646fc99ee36c32b592e689bc82c`. Claude's earlier v3 16k run reported 28.74 s **on a different runtime**, so do not present 28.74/0.886 as a controlled speedup factor.

## Research narrative, limitations, next steps

**Observation:** The only algorithmic code change replaces an all-pairs file/descendant search with one normalized-file set and slash-delimited prefix lookups. Eight semantic controls and the HOLD/immutability assertion agree across v3 and v4 in both runs. The original single-run timing acceptance was **not reproducibly satisfied**. Exploratory 16k v4 result is substantially faster in absolute time than Claude's reported v3 result, but machines and fixtures differ. 

**Interpretation (not certification):** The quadratic ancestor loop is plausibly removed; remaining parsing/CRC and host scheduling introduce timing variation. No claim of formal linear complexity for the complete verifier, no race win, and no automatic production promotion. **Limitations:** synthetic archives; no genuine TAM artifacts, EPUBCheck, full PDF validation, OCF conformance ruling for mimetype descriptor, cross-parser/security review, subprocess isolation or independently authenticated source. Strict extras/comments may reject legitimate EPUBs.

**Next:** Ask Claude to independently review v4 correctness, especially normalized-prefix equivalence, OCF mimetype bit-3 semantics and 16k behavior on its environment. Retain v3 baseline; do not integrate into the staged coordinator until a separate prospective integration plan and independent review. F-001 editorial/rights/claims/Dataset A 6/7, four real deliverables, A1–A6/B6 and explicit publication approval remain blocking.
