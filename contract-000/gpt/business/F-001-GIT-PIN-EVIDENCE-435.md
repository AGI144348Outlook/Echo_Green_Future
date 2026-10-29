# F-001 HOLD-only trusted Git-blob pin gate — Run435 evidence

**Same project:** F-001 TAM Protocol speculative research-notebook ebook. **HOLD / NOT LAUNCH-READY**. No new business pipeline. Pre-test entry was published in Issue #115 **before** the 19 synthetic tests. Earlier read-only Library metadata comparison before that issue was disclosed in the prospective entry, not relabeled as preregistered.

## Why

Shared `Business/ideas/F-001-tam-build/claim_scan.py` blob `31f3dcff486c4c8cc96d514eb425da86834d00c3` skips missing files and can exit 0. Run434's separate presence preflight `f001_source_preflight_434.py` blob `59720d729e0a63ec2ee2d656a4f2f4e7468fe305` validates eight local source files and computes SHA-256, but does not establish that those bytes match a trusted GitHub source commit.

## New deliverables

- `f001_git_pin_gate_435.py` **Git blob `c9707f03816505467c1343449b4b28ba0184c76b`**: exact eight names; externally supplied full commit SHA and Git blob SHA-1 pins; reject missing/duplicate/extra/malformed names and pins, missing/symlink/nonregular/empty/oversize/non-UTF-8 local files, modified bytes, output inside source or pre-existing output. Computes `SHA1("blob "+len+"\\0"+raw)` exactly as Git object identity, plus independent SHA-256 for each source in a HOLD-only receipt. No scanner, account, sale, release or network call.
- `test_f001_git_pin_gate_435.py` **Git blob `b9f603a6a585db2d97e3f8c3839412bb52780bd2`**: 19 synthetic positive/negative controls.
- `F-001-TAM-PINS-435.json`: source-bound eight-file pin manifest, `repository=AGI144348Outlook/The-TAM-protocol`, **commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`**, commit's tree **`5dfabe3a978e05e26528f0cb90101dd7de943f3a`**. Independently fetched exact GitHub commit tree and each of eight files through the GitHub connector at that commit; **8/8 file blob SHA values matched tree**. This is connector-side source-identity verification, not execution of Python against eight local real files.

## Actual local synthetic execution

Command (from scratch working directory with exact source/test bytes): `PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_f001_git_pin_gate_435.py`.

**EXECUTION-VERIFIED:** 19 tests run, **19 PASS**, exit 0, elapsed 0.043 seconds. Positive fixture verified eight synthetic source bytes and deterministic HOLD receipt; negatives rejected changed bytes, missing/empty/non-UTF-8/symlinked source, missing/duplicate/unexpected/wrong pins, invalid commit, duplicate JSON keys, pin manifest inside source, receipt inside source or overwrite, and missing manifest. Source-byte immutability checked. Known Git blob SHA-1 test vector `test\\n` matched `9daeafb9864cf43055ae93beb0afd6c7d144bfa4`.

**Exact executed-byte check:** locally calculated Git blob SHAs for the two tested Python files were `c9707f03816505467c1343449b4b28ba0184c76b` and `b9f603a6a585db2d97e3f8c3839412bb52780bd2`, identical to the connector's committed blob SHAs. No changes to tests after the run. No test failures or deviations in the 19-control invocation.

## Limitations and falsifiers

The trusted pin manifest must be obtained and reviewed independently from the specified GitHub commit; **a forged pin manifest plus forged sources can still pass this byte comparison**. A 40-hex commit string is syntactic, not an authentication or stewardship guarantee. Git SHA-1 is Git object identity, not a modern collision-resistant security seal; receipt SHA-256 does not itself establish authority. Read/stat operations are not race-free against adversarial concurrent source replacement (TOCTOU); a trusted immutable snapshot is still needed. No local materialization of all eight original TAM files, no original `claim_scan.py` replay, no 334→344→347→351 coordinator integration, no EPUB/PDF/Android QA, no editorial approval, no licence/rights decision. All **82 editorial occurrences remain UNREVIEWED**.

**Next:** obtain immutable local snapshot of the eight source files with exact commit/tree pins; run Run434 presence gate then Run435 external pin gate; run original Python scanner on those exact bytes, compare occurrence IDs and statuses with 82-item HOLD queue; independently test coordinator positive and tamper negatives under a new prospective issue; Claude independently reviews historical claims and rights. No public release without Timothy.
