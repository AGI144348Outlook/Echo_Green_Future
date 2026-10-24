# F-001 Run 332 — prospective CSV P1–P4 test evidence (2026-10-24)

**Status: EXECUTION-VERIFIED DRAFT, NOT RELEASE.** Prospective test Issue [#50](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/50) published **before** execution. Same-thread [post-test narrative](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/50#issuecomment-6389560057). One-shot [Actions run 40132907456](https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/40132907456), head `87cd1635eea04a9604fe9a16eee98190693ecbcf`, job `120988251077`, 2026-10-24 21:08:35–21:08:44 UTC, **completed success**. Python test harness printed **18/18 PASS**. The first local clone attempt failed DNS resolution; no local test was claimed. CI was run instead with GitHub's free hosted runner, no model inference, no Cloudflare, no secrets and no publication.

## Actual method and observations

- GPT-only files: [draft builder](F-001-REBUILD-DATASETS-332.py) from shared blob `fa3a62f`, [extended existing §101 pin checker](F-001-CSV-PIN-CHECK-332.py) from shared blob `fb6f59c`, [test harness](F-001-TEST-RUN332.py) and [one-shot workflow](../../../.github/workflows/gpt-run332-csv-verify.yml). Source was the public `AGI144348Outlook/The-TAM-protocol` at commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`.
- Verified Git blob A `b62c970a660e0a6685b58db1ef121690daa4fce7`, B `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4`; 6/8 source rows, zero rejected. The source clone remained clean.
- B printed `0.85` g and exact recomputed `0.85625` g both retained; A's printed `<0.01` inequality preserved. A method `UNKNOWN`; A approximate comparison column now states its 0.01 percentage-point tolerance; A row 6 and B row 1 alone have `SOURCE_UNRESOLVED` terminology flags.
- Extended pin checker accepted draft delivery. Negative controls rejected wrong commit, delivered CSV alteration, mutated source, missing source and invalid args. Mutated/missing source deliberately produced tracebacks and nonzero exits; expected denial, not test failures.
- Draft output SHA-256 A `989d83c16568f23a97251d93919068f3a5e726c738644625af909b278f395fdb`; B `ff442e48acaf00900a3bc3d7900bf987995355a34226b749dbd5b81878e2f7c0`. These are **NOT final release artifacts**.

## Limits / next

Tests used the same GPT-authored implementation/harness and one public source commit on Ubuntu; Claude must independently review. No independent provenance custodian, source rights, author approval, original rounding method, historical claims, EPUB/PDF final checks or release receipt was established. Keep original printed values; do not infer *Gerah* correction. Ask Claude to review the draft without overwriting either side; Timothy retains final manuscript, credit, claim and publication decisions. **F-001 HOLD / NOT LAUNCH-READY.**
