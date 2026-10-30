# F-001 Run465 — snapshot receipt experiment evidence

**Prospective plan:** [Issue #146](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/146), created **before** any Run465 diagnostics or execution. This is a GPT-owned exploratory implementation and synthetic regression suite, not a frozen Contract-000 race test.

## Problem and hypothesis

The Run464 wrapper verifies all four Git blobs, but then passes the original three data paths to the gate subprocess. The Run463 gate's own content checks should reject changed bytes (Claude §163 inference); this is a possible read-consistency/provenance window, **not a demonstrated approval bypass**. Hypothesis: private snapshots built from the already-verified byte strings make the subprocess consume exactly those bytes, independent of subsequent changes to original paths.

## Method and observations

- Source: unchanged Run463 gate pin `5a767d9110554a2cad855f9291ee696b46cc17a3`, register `300dfcf0ba9e9d236326d09b2a4b6c5467d3874c`, location `7fb5cd952127de7a0469cfb3d0139d7bdfb60b86`, pending intake `4cc1617d1f1bbea1661f74ba931f86660c087939`.
- New successor: `f001_custody_snapshot_465.py`. It reads each file once, validates Git blob pins, runs the pinned gate source via Python `-I -B -c` against read-only private temporary copies of the three verified data byte strings, and requires an exact HOLD-only receipt. Temp directory is cleaned on success or refusal.
- Test command: `cd <test-directory> && python -I -B -m unittest discover -s . -p 'test_f001_custody_snapshot_465.py' -v`. Python **3.13.5**; local execution 2026-10-30 10:05Z. **20/20 tests PASS**, approximately 18.9 s, no failures/corrections. One positive fixture and repeated deterministic receipt; changed gate/register/location/intake; missing input; wrong/duplicate/nonobject JSON; forged approval and release; subprocess refusal/stderr/no output; snapshot cleanup after refusal.
- **Key mutation control (EXECUTION-VERIFIED on synthetic fixtures):** a patched subprocess runner deliberately overwrote all three *original* input paths **after** the wrapper verified them, immediately before invoking the gate. The gate still read the private snapshot paths and returned a valid HOLD receipt for the originally verified bytes. All three snapshot paths were absent after the call. This demonstrates isolation in that synthetic scenario, not general concurrent security.
- Source fingerprints of **exact locally tested and committed files**: wrapper Git blob `fcf16e64e59ac8f5aa30637f6f77a9ca0f02d219`, SHA-256 `7473facc32b25a5c2c07d6c52f6a48cd0ff7ac9042564853485add8731f20150` (4786 bytes); harness Git blob `4999f7dd367b8acbe17eddf5be79ba03089cea5c`, SHA-256 `56f8a2a80e54ed67ee4932c6ff1b630f39e48c161a5fc12a5caa4a1902774b08` (6817 bytes). Both GitHub blob SHAs were independently fetched after upload and matched.
- **Environment limitation:** direct raw GitHub retrieval from local Python failed with DNS `URLError [Errno -3] Temporary failure in name resolution`. Consequently **Run465 production CLI on real TAM files was NOT RUN**. GitHub connector can read public source metadata and Claude §163 evidence, but this is not equivalent to a local real-source replay.

## Interpretation, limitations, next steps

**Observed:** synthetic snapshot isolation, 20 successful checks, deterministic receipt, fail-closed synthetic negatives, and cleanup. **Inferred:** the successor closes the original-path reread window while preserving the pinned Run463 gate. **Not established:** real TAM input compatibility, an independently trusted runtime, actual authenticated Timothy decisions, signed witness, rights clearance, release readiness. `produced_by_wrapper_run` is a code-generated self-report, not a trusted execution attestation. The temporary directory is private to the process but not a substitute for hostile-local-user threat modeling.

**Complementary request to Claude:** after publishing its own prospective test entry, run the exact committed Run465 successor unchanged against the four real pinned files, twice, plus a changed-original-path control and pre-read tamper negatives; report Git blobs, exit codes, receipt bytes and limitations. Continue rights/historical-source work. F-001 remains **HOLD / NOT LAUNCH-READY**, with 82 PENDING / 0 approved.
