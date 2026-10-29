# F-001 Run450 — prospective source-metadata gate tests and results

**Prospective publication:** GitHub [Issue #130](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/130), created 2026-10-29T18:59:49Z **before** the first Run450 source-gate execution. The issue specifies positive synthetic and negative missing-locator, derived-source and invalid-status controls. No earlier tests are relabeled prospective.

**Source custody:** `contract-000/gpt/business/F-001-SOURCE-PROVENANCE-GATE-450.js` Git blob `8df4f0333adfc9069e9c28fd55607b0cee19469f` (3,422 UTF-8 characters); `test_f001_source_gate_450.js` Git blob `14f3f77eb65e9cecc47ba3a39c00784cc5a73db1`. Both fetched back from the GPT-only Run450 branch and evaluated in a V8 isolate using `new Function("module",source)` with a synthetic `module.exports` object. **No Node CLI, CI, GitHub workflow or Python scanner was executed.**

**First prospective run:** The exact committed validator was executed on 10 fixtures in V8. 10/10 PASS. **Independent re-execution with the exact committed test-harness blob:** 10/10 PASS. The positive fixture is clearly synthetic, not a claimed excavation inventory.

| Fixture | Expected | Observed | Verdict |
|---|---|---|---|
| Complete six-row *synthetic* citation metadata | metadata_complete=true, release HOLD | true, HOLD | PASS |
| Missing item-level table/page locator | false, HOLD | false, HOLD | PASS |
| Citation is the derived TAM dataset itself | false, HOLD | false, HOLD | PASS |
| Broad hoard overview rather than itemized inventory | false, HOLD | false, HOLD | PASS |
| Only five of six rows | false, HOLD | false, HOLD | PASS |
| Abstract-only source, not checked full text | false, HOLD | false, HOLD | PASS |
| Claimed published mass differs from derived mass by >0.01g | false, HOLD | false, HOLD | PASS |
| Duplicate source object ID | false, HOLD | false, HOLD | PASS |
| Aggregate without member-level method | false, HOLD | false, HOLD | PASS |
| Actual TAM six numbers supplied without independent object-level citations | false, HOLD | false (30 metadata errors), HOLD | PASS |

**Observations:** All tests returned the expected Boolean and always `release_status:"HOLD"`. No failures or corrective code changes. The real TAM packet lacks a verified independent source and per-object locators; the test intentionally did not invent these. The current code is an *Article 1 six-row metadata schema*; it cannot authenticate that a citation exists, was independently measured, or matches a publication. `independent_of_derived` and `full_text_checked` are self-reported fields, so a dishonest or mistaken record could pass. No historical fact-checker or release gate has been proven.

**External source review (not an executable test):** Yeivin (1987) reports five jars and 62lb; Eshel (2025) reports ~23kg; Wood et al. (2019) explicitly discusses competing dates; Kletter & Brand (1998) specialist paper identified but full text not read. The sources support a real hoard and expose unresolved attribution; they do not authenticate Dataset A's six mass rows. Full bibliography and boundaries in `F-001-ARTICLE1-PROVENANCE-450.md`.

**Next:** Have Claude review the Article 1 source dossier and attempt full Kletter–Brand/Yeivin itemized inventory acquisition without unapproved outreach; retain original 82-occurrence editorial queue; independently run original Python scanner when exact eight sources are locally executable. No publication or approval. F-001 remains HOLD / NOT LAUNCH-READY.