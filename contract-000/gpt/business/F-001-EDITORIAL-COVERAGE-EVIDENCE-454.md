# F-001 editorial coverage receipt — Run454 test evidence

**Project:** F-001 TAM speculative research-notebook ebook, **HOLD / NOT LAUNCH-READY**. Source queue: `contract-000/gpt/business/F-001-CROSS-QUEUE-407.json`, Git blob `ab5e755c1d1f33fd2c9fd3af2866bc68ab1a4b16`; underlying TAM `main@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. Claude shared §153 manuscript blob `3abeb9efb268dbf74d1491e262305987407327fd`, mapping script `d58266a`, arithmetic script `bc4b02e`. This does not change or approve Claude's editorial work.

**Pretest published before execution:** [Issue #135](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/135). **Exact tested source:** `F-001-EDITORIAL-COVERAGE-GATE-454.js` Git blob `8937b785089958f3cbd4355af5e08ce25cb2c25e`, initial commit `51090d98cfcb86d9f27b1a3004d02b01be29019d`. Fetched back from GitHub. Evaluated in V8 with a fake non-CLI require; no Node CLI or CI.

**Observations (independently executed by ChatGPT):** 10/10 checks passed: actual 82-row queue yielded 20 pending Collective IDs, 62 Claude-reported proposed, zero final, HOLD. Nine negative cases failed closed: wrong source commit; release authorization; forged final approval count; altered total; duplicate ID; malformed ID; missing pending ID; missing supplemental row; altered status. The helper returns all 20 pending IDs explicitly.

**Execution deviation:** The first dynamic-function evaluation attempted to parse the Node shebang and raised `SyntaxError: Invalid or unexpected token` **before any tests**. The second attempt stripped only the shebang from the in-memory evaluation string; all other source bytes were fetched and evaluated as committed. 10/10 then passed. Node CLI not run.

**Interpretation:** This is a consistency guard for the *reported editorial coverage* and source queue shape, not evidence that 62 individual proposed decisions were independently checked, and not proof of archaeology, licensing or release readiness. It does not cryptographically verify the queue file's Git blob at runtime; provenance is recorded in this evidence document. It does not rederive the 82 IDs from raw TAM files. No publication, account, outreach or payment.

**Next:** Claude reviews 20 remaining Collective IDs; GPT independently replays original Python scanner on eight exact public TAM source bytes and verifies output digests/packaging receipts once executable bytes are available. F-001 remains HOLD even after editorial coverage reaches 82/82 until Timothy's decisions and rights checks.
