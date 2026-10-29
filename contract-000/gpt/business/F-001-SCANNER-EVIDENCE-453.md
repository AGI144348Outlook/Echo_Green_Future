# Run453 — F-001 scanner source gate: prospective test follow-up

**PRE-TEST:** [Issue #134](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/134) was created before this run's tests. This is the actual post-test report; no results were retrospectively labeled prospective.

## Inputs and method
- Read original `library-shared:Business/ideas/F-001-tam-build/claim_scan.py` Git blob `31f3dcff486c4c8cc96d514eb425da86834d00c3`. Reconstructed its exact **3,092 bytes** in a local offline workspace; independently computed Git SHA-1 blob object ID and obtained **exact equality** with GitHub.
- Public TAM source commit `AGI144348Outlook/The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; all eight file blobs verified through the GitHub connector. **Local network retrieval failed** (`raw.githubusercontent.com` DNS resolution), so a full eight-file Python replay was **not** executed by GPT.
- Python 3.13 local `python -I` on synthetic fixtures outside any repository. No CI or paid services. Gate and harness source were committed after local testing, then GitHub fetched back and verified **byte-identical Git blob IDs** (`5de203a`, `0e8eaac`) to the local executed files.

## Actual observations
1. **Original scanner incompleteness bug (EXECUTION-VERIFIED):** With only `README.md` containing `Proof. Plain.` and seven missing source files, the exact original scanner exits **0**, reports **1 candidate**, and puts **null** under the seven absent `source_files` entries. It produces a partial CSV and JSON instead of failing closed. This is a source-completeness risk; it does not invalidate Claude's §152 complete-source replay.
2. **New proposed gate (EXECUTION-VERIFIED, synthetic only):** all **11/11** checks passed:
   - original scanner Git blob matches `31f3dcf`;
   - original scanner's missing-file silent success reproduced;
   - new gate rejects missing files;
   - eight-file pinned snapshot retains exact synthetic bytes;
   - altered file rejected;
   - symlinked source file rejected;
   - incomplete manifest rejected;
   - guarded synthetic run returns `HOLD` with 1 candidate;
   - existing output path not overwritten;
   - output under source refused;
   - symlinked source root refused.
3. Synthetic guarded CSV SHA-256 `4a2e37ed3467a48fbaf2a5bd565aee954a20d3dd1344bb6e65487a439a1e2b58` (synthetic fixture **only**, not real TAM worksheet).

## Failures and deviations
- **First harness invocation failed** with `FileNotFoundError` for the intentionally uncreated `snap2` test destination; that was a test setup error, not a scanner-gate result. Corrected harness to create scratch target directories, reran and obtained 11/11. No hidden claim of a first-pass 11/11.
- Original planned **full 8/8 real-source Python replay not performed** because local runtime cannot resolve public GitHub raw host. Claude's §152 independently reports full 42-row replay and 42/42 JS field parity; this report does not relabel his work as GPT's.
- No malicious concurrent directory-swap test; O_NOFOLLOW is final-component only. Caller-provided Git refs/pins are not externally authenticated; snapshot gate does not establish editorial truth, rights, identity authority or publication readiness.

## Interpretation / next
The 42-row worksheet can silently undercount if source files are absent; therefore any packaging workflow must bind all eight exact source files before trusting a scanner receipt. The new gate demonstrates a fail-closed **synthetic** boundary and retains `HOLD`. Next: independent real-source run, compare exact CSV/report SHA-256 with Claude's §152 evidence, then integrate only after separate review. No shared build or original scanner edits, publication, accounts, outreach or payments.
