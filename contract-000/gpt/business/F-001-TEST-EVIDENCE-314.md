# F-001 GPT Run 314 — staged coordinator adapter evidence (2026-10-23 CT)

**Pre-test registration:** [Issue #33](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/33) created **before** any local test execution. Scope: only F-001 TAM ebook, no A-000 tests. Source code committed unchanged from passing local run: [adapter blob `6d8ec2275e780105013b69317495c3c3122c12b1`](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/mirror-chatgpt-root/contract-000/gpt/business/PROPOSED-f001-staged-coordinator-adapter-v1.py); [harness blob `772c14aa7f4111de8c318d61e64e2e4bb69671e1`](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/mirror-chatgpt-root/contract-000/gpt/business/PROPOSED-f001-test-staged-adapter-v1.py). The reviewed dependencies were verified by Git blob against `4fac471` (Run 313 pinned FD helper) and `9eee201` (Run 312 coordinator-v4). Reviewed v3 receipt, v5 parser/report gate and v4 binding scripts from the Run 312 handoff ZIP were invoked in the positive chain.

**Method (EXECUTION-VERIFIED, local):** Linux CPython 3.13.5; `python -I -B test_staged_adapter_v1.py`. Each case uses a fresh private temp copy of archived public-derived Dataset A and **synthetic placeholder EPUB/PDF** plus Dataset B, pins, receipt, binding and disposition report. Adapter opens inputs with directory-relative no-follow descriptors, hashes four artifact files and metadata into a private staging tree, rewrites only derived receipt paths/build-output root, records both original and derived receipt SHA-256, and runs the exact reviewed coordinator-v4 against the staged tree. Caller-provided pins are **not** independently authenticated; release is always HOLD.

| Case | Expected | Observed | Assessment |
|---|---|---|---|
| T0 actual reviewed-script synthetic chain | PASS / HOLD / BLOCKED | PASS, 3 stages | expected |
| T1 modified EPUB bytes | FAIL / HOLD / BLOCKED | FAIL: source digest mismatch | expected |
| T2 symlinked PDF | FAIL / HOLD / BLOCKED | FAIL: ELOOP | expected |
| T3 replace EPUB pathname after held FD opened | original bytes preserved or reject | PASS, 3 stages using held original | expected |
| T4 `../` in receipt artifact path | reject | FAIL: unsafe relative component | expected |
| T5 missing PDF | reject | FAIL: ENOENT | expected |
| T6 change pins JSON after first read, before snapshot | reject or consistently pin first-read bytes | FAIL: source digest mismatch | expected |
| T7 derived receipt disclosed and HOLD | distinct original/derived SHA, no authority | PASS with distinct digests and absent authority | expected |
| T8 **exploratory add-on**, forged original build-output-root | reject | FAIL: original root mismatch | expected; not preregistered |

**Final local rerun:** **9/9 expected outcomes**, exit 0. Cases T0–T7 were prospectively listed in Issue #33. T8 was added as an exploratory negative after implementation and is not retrospectively represented as preregistered. An initial single T0 CLI control was run after the Issue but before the final harness; it returned PASS/HOLD/BLOCKED. During refinement an explicit check for original receipt build root was added; no failing formal harness run was concealed. The passing harness was rerun after the code was committed and the exact committed Git blob SHAs were fetched and matched to local. Raw local JSON evidence SHA-256 `a05b07d6599aef2c0bbf27643edf30e72e5ea6c4bdedc78eb1e68f5ac3201f28` (included in handoff ZIP).

**Observation vs interpretation:** All four staged artifacts were byte-checked against caller pins; the synthetic pathname swap did not redirect the held FD. This narrows a coordinator-v4 check/use gap in the tested scenario, **not** a proof of source authenticity, finished book integrity or adversarial process isolation. The derived receipt is an internal testing transformation, not the original signed/approved receipt. **Limitations:** same-UID staging mutation, parent-directory races, >1 MiB metadata replacement resource cost, process-grandchild escape, untrusted subprocesses, non-POSIX systems, real EPUB/PDF accessibility and commercial rights were not resolved. There is no production release authorization.

**Next:** Claude independently review the adapter's derived-receipt semantics and staging trust model, test process-grandchild containment separately after prospective registration; GPT refine artifact limits and tool execution isolation without modifying shared/Claude work. F-001 remains HOLD pending Timothy A1–A6/B6, Dataset A rows 6/7, authentic deliverables, rights/claims/a11y and explicit release approval.
