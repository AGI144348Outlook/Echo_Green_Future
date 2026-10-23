# F-001 Run 302 — read-only editorial-disposition v4 test evidence (2026-10-23)

**Scope:** Sole existing F-001 TAM Protocol ebook; unintegrated parser proposal, **release HOLD**. Synthetic public-style Dataset A fixtures only, no production build or actual editorial authorization. No A-000 operational tests.

**Prospective pre-test notice:** [Issue #13 comment 6369220970](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6369220970), published before execution. The notice described Claude's §108 FIFO finding, proposed descriptor-based hardening, method, expected outcomes and falsifiers.

## Exact source and environment

- Baseline GPT v3: `contract-000/gpt/business/PROPOSED-f001-disposition-binding-v3.py`, Git blob `aa632bf3c8144a2c8fa0308ba7fc88c8fe9a1102`. Extracted from prior Run 301 handoff ZIP and **verified locally** with `git hash-object` before modification; this matches the current GitHub source blob.
- New GPT v4: `PROPOSED-f001-disposition-binding-v4.py`, Git blob `c267639e5dbbf078a6af11e172f42965837582af`, commit `cc8b7a04dc0b293e7cd7f08fad829e4e1d94cfd3`. Verified GitHub `fetch_file` blob equals local `git hash-object` and bytes after creation.
- Reproducible 7-case IO harness: `PROPOSED-f001-test-v4-io.py`, Git blob `eeb5a8ac34e4d9007d536b2cdeeca0c874476c42`, commit `57142cfd2a3dc86b4d3f74ac027d42dcf2864212`. Verified exact GitHub/local blob equality.
- Additional local 16-case synthetic characterization harness (in Run 302 handoff), Git blob `71f60a958e9de21ac1e2d541563c37dffb880c6b`; result JSON SHA-256 `eb5dcfcbc0ce3230fc3c790ef6cbff6417920ac1f0d5d46a5c0c056bc1bf6bbf`. Python 3.13.5, Linux, `python3 -I -B` subprocesses in temporary directories, four-second timeout per case.
- Compilation check: `python -m py_compile` on the v4 local file completed successfully.

## Observations — EXECUTION-VERIFIED locally

**16/16 expected outcomes:** valid flagged record `0/RECORDED_UNAUTHENTICATED`; missing flagged record `3/PENDING`; clean CSV without or with an empty record `0/NO_FLAGGED_ROWS`; exactly 1,048,576-byte padded record `0/RECORDED_UNAUTHENTICATED`. Wrong source pin, malformed JSON, deeply nested JSON, 1,048,577-byte record, FIFO without writer, symlink, directory, character device, duplicate JSON key, wrong CSV line and wrong bound row all `1/INVALID`. All reports were structured JSON, `release=HOLD`, `source_pin_authenticated=false`, `decision_reference_authenticated=false`. Input regular files unchanged; no unexpected stderr or timeout.

**Reproducible subset:** The committed seven-case IO harness separately passed **7/7**: regular, exact-bound, over-bound, FIFO, symlink, directory, character device. It uses only synthetic data and read-only subprocess invocation. These seven overlap the sixteen above; **not** 23 independent test scenarios.

**Interpretation (not an authorization claim):** Descriptor-level `fstat` with nonblocking open closed Claude's demonstrated FIFO hang in these Linux tests, while `O_NOFOLLOW` rejected a symlink. The fixed-size read rejects oversized regular records. This is stronger than a separate `is_file()` then `open()` check for the tested file-type cases, but it is not a general security sandbox.

## Limitations and next steps

- Only Linux/Python 3.13.5 tested. `O_NOFOLLOW` is optional on other platforms; symlink rejection is not guaranteed where unavailable. No concurrent rename/swap race was stress-tested.
- The **Dataset A CSV** is still read with an unbounded `read_bytes()`; a non-regular CSV or very large file may block/exhaust resources. Separate input-bounds review is a future proposal, not tested here.
- Source digest is supplied by the caller and remains unauthenticated until compared against a separately pinned source/build receipt. Exit 0 never means approval. No actual TAM release artifacts, rights, editorial decision or production integration were tested.
- **Next GPT:** propose source-pinned receipt integration and independently validate final four-artifact hashes when source/approval is ready. **Next Claude:** independently review v4 descriptor handling, portability and manuscript/claims/listing stack; do not overwrite GPT branch.
- **Awaiting Timothy:** Dataset A two editorial dispositions (CSV lines 6 and 7), A1–A6/B6 scope/licensing/credit/terms, and explicit publication authorization. F-001 remains **ON HOLD**.
