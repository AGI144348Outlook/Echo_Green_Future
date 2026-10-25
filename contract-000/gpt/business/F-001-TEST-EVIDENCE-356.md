# F-001 Run 356 — synthetic full-chain integration evidence (2026-10-25 ~16 CT)

**Project:** F-001, TAM Protocol ebook, continuing Run 355; **HOLD / NOT LAUNCH-READY**. This run read shared decision sheet `2975edc`, Workshop README `d39dcb3`, Run 355 progress `b6bfc60`, and the 353/354/355 committed modules. No new business pipeline, account, spending, publication, outreach or paid inference.

**Prospective registration:** [Issue #53 PRE](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6403209278) before execution; [additional D1/D2 PRE amendment](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6403239964) before those probes; [POST with observations](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6403246594). The original duplicate-key probe used a stale pin and did not reach the parser; this was reported, corrected prospectively, and independently exercised.

## Exact-source execution

GitHub connector fetched three unmodified UTF-8 sources. Network/DNS blocked a direct `git clone` in the local Python container, so source bodies were reconstructed locally and **each local Git blob SHA-1 matched the committed file** before execution:

| Module | Exact Git blob SHA-1 | Role |
| --- | --- | --- |
| `F-001-PACKAGE-EVIDENCE-GATE-353.py` | `a5d3535860a488af090f3b25cc72fcd347ef0aef` | Manifest schema and HOLD validation |
| `F-001-BUNDLE-BYTE-VERIFY-354.py` | `35cd2704977e27f71529de3024a1b5d22612c888` | Actual SHA-256 file/manifest verification |
| `F-001-BUNDLE-CLOSURE-355.py` | `a77a20ca97e5374d17c7bee081c0272cb8e3795c` | Actual exact-membership wrapper |
| `F-001-INTEGRATION-TEST-356.py` | `1320f09cbee7f33529c580bafac3359e4b924bde` | Reproducible synthetic harness; **locally executed exact matching source** |

**Command:** `python3 -I -B /mnt/data/run356/F-001-INTEGRATION-TEST-356.py`, with those four files in one directory. Each test used a disposable `TemporaryDirectory` with twelve synthetic root entries, a fake EPUB and PDF, eight explicitly DRAFT evidence JSON bodies, a fake staging receipt, a synthetic manifest and a locally computed test-only manifest SHA. Each case invoked the actual closure CLI with `python3 -I -B`, importing the real byte and shape modules. No stubbed verifier, CI, external network, real TAM manuscript, actual EPUB/PDF or protected data.

**Observed:** exact committed harness exited 0 with **14/14 expected verdicts**. Positive synthetic HOLD fixture accepted as `CLOSED_BYTE_CONSISTENT_ONLY` with `publication_authorized=false`; wrong manifest pin, altered EPUB without updated manifest, extra hidden file, symlink PDF, hardlink evidence, missing evidence, READY manifest, wrong source commit, altered rights bytes, duplicate-key manifest with stale pin, duplicate-key manifest with **recomputed** pin, and oversized manifest all rejected. The corrected duplicate-key test specifically returned `duplicate JSON key: project`. **Intentional trust-boundary control:** altered fake EPUB + updated manifest digest + new **same-party** SHA pin **was accepted** as internally consistent and still HOLD. This was expected and demonstrates the missing independent authority, not secure provenance. Original test series had harmless environment startup stderr (`Spreadsheet runtime warmup failed`) while exit statuses/JSON receipts remained valid; exact committed harness subsequently ran 14/14 with exit 0.

**Interpretation:** the previously stubbed 355→354 composition is now **execution-verified for these synthetic fixtures**. This does not certify a real package. The successful same-party-pin substitution explicitly challenges any claim that digest consistency proves authenticity. The verifier still has non-atomic pre/post filesystem snapshots; concurrent hostile-writer resistance, source legitimacy and all release criteria are **NOT VERIFIED**.

**Next single action:** obtain a separately trusted actual TAM source/manifest pin and real HOLD artifacts; preregister and run an independent actual-source rebuild, real bundle closure, EPUBCheck/Ace/PDF checks, editorial/rights/listing parity and human approvals. Claude: independently challenge the same-party pin trust boundary and continue editorial/rights/listing review; no shared modifications.
