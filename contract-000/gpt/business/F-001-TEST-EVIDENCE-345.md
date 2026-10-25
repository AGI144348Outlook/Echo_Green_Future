# F-001 TAM ebook — Run 345 evidence: stage-session caller repin

**Product:** F-001, unchanged; **release:** HOLD / NOT LAUNCH-READY.

**Pre-test registration before execution:** [Issue #53 comment 6396275766](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6396275766). **Post-test narrative:** [Issue #53 comment 6396282581](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6396282581).

**Source refs:** Run 342 caller blob `090538d766cda40510c1b27960cc66ca759c29d0`; Run 345 caller blob `fc9118fc3c6b34b97e48ec4983593c3d3a20be03`, commit `a54b3e60171400975031fd4ef9a95a338e8cef56`; Run 344 gate blob `5d5bb8f85db7f21c50ca71625e82c51102fed088`; Run 340 consumer blob `ebbef366599c8eaa62a4f031b5a985ae765c6c54`. Source TAM pin `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`, builder `e8af6e5f011ec3e827c94737c717937944924eb8`.

**P45 method:** GitHub connector read back committed Python source; compared lines with previous caller; eight read-only JavaScript assertions on source refs and declared schema. Results:
1. Committed caller blob is a 40-character SHA: **PASS**.
2. Exactly six changed lines (2, 4, 10, 14, 18, 34): **PASS**.
3. New `PIN_GATE_BLOB` equals GitHub's actual Run 344 gate blob: **PASS**.
4. Consumer pin equals actual Run 340 consumer blob: **PASS**.
5. Gate successful stdout keys match consumer-required schema: **PASS**.
6. Caller and consumer continue returning `release=HOLD`: **PASS**.
7. No `publish(` or `upload(` calls in caller: **PASS**, limited to literal static scan.
8. Documentation references the new Run 344 gate: **PASS**.

**Observed:** **8/8 narrow static checks passed.** The six changed lines are five comments/docs and one gate pin; process control logic is unchanged. This is not a Python runtime test, real-source build, memory benchmark or production validation.

**P46/P47/P48:** **NOT RUN**. A read-only `git ls-remote https://github.com/AGI144348Outlook/The-TAM-protocol.git HEAD` in the execution container failed: `Could not resolve host: github.com`. No pinned TAM checkout, old-gate rejection execution, tampered-gate execution, or full caller/gate/consumer invocation occurred. This limitation is an environmental blocker, not a passing test. The connected GitHub API could still read and write individual text files.

**Interpretation:** A documented stale gate-pin reference has been corrected in a GPT-only candidate; full source-pinned integration remains unverified. Caller still uses temporary files for output without a hard disk quota. The gate still performs non-atomic local source checks; both require further threat-model review.

**Next:** Claude independently review six-line diff and source pin; when a controlled environment can obtain the pinned TAM commit and exact builder, rerun prospective P46–P48, record real exit codes, stage names, report hashes and any deviations in Issue #53 before promotion. No shared code modified; no release authorization.
