# F-001 Run 299 — Exact v1 disposition parser against archived public TAM Dataset A

**Status: EXECUTION-VERIFIED offline characterization, NOT an editorial approval or release.** Pre-test Issue #13 entry [6365415232](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6365415232) was posted **before** executing any Run 299 tests. This report records results from Python 3.13.5 with `-I -B`, no CI, network inference, Cloudflare loops, paid services, production A-000 execution or private Testament data.

**Exact provenance:** Reused local archived Run 297 handoff `Contract000_Run297_Handoff.zip` containing the public TAM source files and outputs built at The-TAM-protocol commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. Checked archived source Git blobs `b62c970a660e0a6685b58db1ef121690daa4fce7` (Dataset A), `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4` (Dataset B), and shared builder blob `fa3a62f76549ecaea6e226ba5cca41597000d790`. Archived Dataset A SHA-256 `d3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2` matched the previously pinned output; Dataset B SHA-256 `fecd151b5b7393fc69975a0b323e02c5f306eb1fd49bedc2901f849001e8afc5`, report `036a85e5fe3b372c6ada0e0851f3463fd6da3e5d6ab825972cb454085f85dde4`. The **exact parser file executed** had Git blob `a6d25f989b4b7cae7e66b6fa02848481cb6c87a4`, matching the GPT-owned [v1 parser commit 17cec22](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/17cec22bbdb9de2a46eb1a3899855dcd79ac11dd). No actual source values were corrected.

**Method:** Extracted the archived public fixtures into an isolated work folder; ran `python3 -I -B test_actual_disposition_v1.py`. The harness invokes the exact v1 parser as a separate Python process in temporary directories, verifies exit/status/release/authentication fields and checks that inputs are not mutated. Constructed all editorial JSON records as **synthetic test data** with `decision_reference=null`, never as Timothy decisions. For the clean-A characterization, altered only the match flags in a synthetic CSV copy, not the pinned Dataset A.

| Case | Observed exit | Observed status | Expected? |
|---|---:|---|---|
| Real six-row Dataset A, record absent | 3 | PENDING / HOLD | yes |
| Real Dataset A, synthetic exact row-bound record | 0 | RECORDED_UNAUTHENTICATED / HOLD | yes |
| Real Dataset A, stale record digest | 1 | INVALID / HOLD | yes |
| Real Dataset A, altered bound row field | 1 | INVALID / HOLD | yes |
| Changed delivered CSV, old record | 1 | INVALID / HOLD | yes |
| Synthetic clean-A CSV, record absent | 3 | PENDING / HOLD | yes |
| Synthetic clean-A CSV, empty rows record | 0 | RECORDED_UNAUTHENTICATED / HOLD | yes |

**Observed:** **7/7 expected outcomes**. Real Dataset A had **6 data rows**, exactly two flagged at CSV line indices **6 (Silver Droplet)** and **7 (Small Scrap)**. No case reported authenticated decision, authenticated source pin or release READY. All input bytes remained unchanged. Exact harness SHA-256: `7c4fc6a8b67c8ae708febc2da4cd848c893aaaa6e08b7cdc8b2936ddfa38ae1d`; result JSON SHA-256: `9d53bf60b073d955927ddde06cfa4fdd7c11ddfa25c151a523c0f106d08b1ace`. The harness and JSON are included in the local Run 299 handoff package, not claimed to be committed to GitHub.

**Interpretation and new issue:** The v1 parser correctly enforces the row/file binding against the *actual archived* six-row Dataset A. The no-flag synthetic case also revealed a **status-semantic ambiguity**: an empty record for a CSV with zero flagged rows returns `RECORDED_UNAUTHENTICATED`, even though no editorial disposition was needed or recorded. It still returns `release=HOLD` and cannot authorize publication, so this is **not** a fail-open release result. Proposed v2 should explicitly distinguish `NO_FLAGGED_ROWS / NOT_APPLICABLE` from `RECORDED_UNAUTHENTICATED` and should not use a parser exit 0 as approval. No v2 code was changed or tested in this run.

**Limits:** Archived public fixture, not a fresh network clone or final production build. SHA and Git blob comparisons verify archived bytes against recorded pins but do **not** authenticate who chose the pins or who authorized editorial decisions. No EPUB/PDF or complete release receipt was built. F-001 remains HOLD pending Timothy A1–A6/B6, two dispositions, rights/claims/accessibility, final four-artifact hashes and explicit independent publication authorization.

**Next:** Claude independently review v1 on real A and the no-flag status proposal; draft v2 only after agreement, post a new pre-test Issue entry before any v2 test.