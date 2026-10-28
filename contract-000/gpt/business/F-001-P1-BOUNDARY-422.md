# F-001 Run422 — structural validator versus raw-blob authority

**PRE/POST:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/95. **Exact sources:** `f001_p1_family_binding_421.js` blob `66f63b88fc95ddabc84f02e3270298903e7d4136`; `F-001-P1-TRIAGE-420.json` blob `eb139defefba0e86ac23879e753e892ee654aca5`. No product source modified.

Ran the actual exported `validateP1` function in a bounded JavaScript V8 isolate with parsed original packet; **8/8 observed results matched expectations**:

| Control | Expected / observed |
| --- | --- |
| Unaltered packet | PASS / PASS |
| Coherently change a family's sentence **and** its occurrence | PASS / PASS (structural function alone cannot authenticate content) |
| Change only family sentence | FAIL / FAIL |
| Change reviewer question | PASS / PASS (not semantically checked) |
| Change human disposition to APPROVED | FAIL / FAIL |
| Change release flag to true | FAIL / FAIL |
| Change source pin SHA | FAIL / FAIL |
| Change occurrence file/location | FAIL / FAIL |

**Interpretation:** structural consistency is not source authenticity. The original **Node CLI** in the same file computes `sha1("blob "+len+"\\0"+raw)` and checks the exact packet blob before parsing; this should reject coherent byte edits but was **NOT executed**. Do not call this a bypass of the complete CLI. Local `urllib` fetch of raw GitHub returned DNS failure `[Errno -3] Temporary failure in name resolution`; Node v22.16.0 is installed but exact input files were unavailable in that environment. The original Python claim scanner against eight TAM files also remains unexecuted. The previous 42-candidate JS translation remains provisional.

**Next:** materialize exact packet and JS bytes to a local Node environment, run positive + one-byte negative, record stdout/exit codes; then run original Python scanner on eight exact source blobs and compare rows/pins. Neither structural check nor raw pin supplies editorial truth or rights. F-001 HOLD.
