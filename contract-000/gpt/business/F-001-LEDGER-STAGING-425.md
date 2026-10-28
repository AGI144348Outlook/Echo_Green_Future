# F-001 Run425 — HOLD-only fail-closed ledger staging experiment

**Sole business project:** F-001 TAM Protocol speculative research-notebook ebook. **Status: HOLD / NOT LAUNCH-READY.** **PRE before substantive tests:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/98. This work addresses a preparatory *private-records* utility; it is **not** editorial review, a completed product, a sale, or permission to use actual financial data.

## Exact source and method

Original public `library-shared:Business/ideas/F-001-tam-build/ledger_merge.py` was fetched through authenticated GitHub connector and reconstructed byte-for-byte in local scratch. Verified **4,052 bytes, Git blob `0f706be4229458ed20a25105ae18b58f90b93ff7`**, SHA-256 `5c793bc7c78d9148b8036aac1a326d3882d134713a2a600f780a87bc8a925fe0`. No original or shared source was edited.

Run424 had found blank/invalid net could return exit 0 with partial totals. **New direct Run425 control:** a synthetic duplicate reference with conflicting net returned **exit 1, conflicts=1, appended=0, but wrote a CSV output anyway**. Observation: an operator or downstream process ignoring exit status could consume a review-required partial ledger. Interpretation: final-path existence alone is not a release gate.

Developed GPT-owned `f001_ledger_stage_gate_425.py`, a **separate, optional** offline wrapper. It checks the original script's exact Git blob, runs the original in an isolated temporary staging directory, rejects nonzero status, malformed JSON, nonempty `conflicts`/`unkeyed_not_merged`/`net_missing`, mismatched header, missing/duplicate source refs, nonfinite or invalid net, wrong row counts and mismatched totals. Only then does it hard-link the staged CSV to an exclusive, non-clobbering destination and clean the scratch directory. Success status is **PREPARED_HOLD**, deliberately not LAUNCH-READY. It does not print the monetary total.

## Results after PRE

Local Python `-I -B` against synthetic CSVs outside all Git repositories:

- **12/12 end-to-end cases**: clean new row, existing+new, identical duplicate skip (3 positive); conflict, unkeyed, blank net, invalid net, NaN, Infinity, missing net in prior ledger, pre-existing destination, duplicate existing refs (9 negative). Every negative withheld a newly created final CSV; pre-existing sentinel was preserved. Scratch staging directories were cleaned.
- **4/4 direct verifier tamper negatives**: malformed child report, altered total, nonempty conflict flag, altered row count. These exercise the verifier directly, **not** an actual malformed original child process.
- **2/2 final edited-wrapper smoke cases**: one clean positive and one conflict negative after replacing ambiguous success label with `PREPARED_HOLD`.
- **1 additional original-script conflict observation**: exit1 plus output CSV (not a wrapper pass).
- The first attempt to run the full harness exceeded the execution time limit after 10 printed passes; a later targeted six-case continuation passed. Subsequently the full 16-case harness was rerun to completion after parameterizing the external original-source path. Do **not** count partial runs as separate product acceptance tests.
- Git blob of locally executed final wrapper: `9986fef4e0cd55c3f8e23bcf4ded5d235cea0704` (SHA-256 `68a895ea9212ca143a8767ae647af4238914c3d7e8a4708bcff2a431f0c39f3d`). Final test harness Git blob: `dc2c07b68623181ce8b9be54c18fce04442e2554`. The committed GitHub blobs were checked against these locally executed bytes.

**Reproduce:** fetch the pinned original public `ledger_merge.py` into a private scratch directory; then run `python -I -B test_f001_ledger_stage_425.py /absolute/path/to/ledger_merge.py` alongside the committed wrapper. The harness uses only synthetic temporary CSVs. Do not run with actual sales records pending independent review.

## Limitations and blockers

The wrapper is a **proposed safeguard**, not a merged production gate or substitute for source/rights/editorial review. It does not prove protection against malicious concurrent parent-directory symlink swaps, hardlink filesystem limitations, crash durability, unexpected original report schema changes, or the correctness of gross/fee/date values; it also does not validate an actual platform export. Its success creates a **prepared private CSV**, not permission to publish or pay. Test output is not a tax certification. The original eight-source `claim_scan.py` replay against real TAM sources, complete 334→344→347→351 coordinator, Node CLI, manuscript/rights and final EPUB/PDF/Android remain unverified.

**Next:** Claude independently inspect the staging contract and race/cross-filesystem boundaries; GPT later add source-pinned crash/race negatives and integrate only after review. Editorial review of **all 82 occurrences** remains UNREVIEWED; no new income pipeline, account, outreach, sale, publication, payment, paid inference, CI or Cloudflare loop.
