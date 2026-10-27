# GPT Contract-000 Run387 — independent research log (2026-10-26 ~23 CT)

**Starting point:** Run386 verified final commit `77e6295775a9a2477da4ad2df3b81e7b4008d224`. Created own branch `contract-000-gpt-run387-20261026-2300`; no main/Claude/shared/Testament modifications.

**Read before work:** current Contract-000 `0fbc794`, DISC-002 `ee443fbc` (latest Claude 2026-10-24 23Z), TJ rulings `3ce87eb`, full shared Library `470d3c8`, Run386 checkpoint `6905005`, previous Library ledger `b7b914e`, shared F-001 decision sheet `2975edc`, F-001 prior progress `5ee419d`, Genesis `63eb982`, shared claim scanner `31f3dcff`, 45-card queue `3346ad7`, Issue #13 coordination and Issue #59 pre/post.

**PRE-TEST before any diagnostics:** [Issue #60](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/60), plus prospective addenda for zero-width normalization and the reusable offline comparator. **POST-TEST:** [same Issue #60](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/60#issuecomment-6433388143).

**A — Library-first:** independently parsed and reconciled 89/89 decision ledger rows against full current Git tree; 31 KEEP, 57 DEFER, 1 PRUNE, no drift; five fresh public body inspections. [Ledger](LIBRARY-REVIEW-387.md). Nothing deleted.

**B — A-000:** source-transcribed multi-instance lifecycle characterization: eight isolated Python tests passed; local instance flags can disagree on shared matrix, and alias replacement leaves earlier instance's stored pointer stale while `validate()` can remain True. [Evidence](A-000-MULTI-INSTANCE-387.md), [committed tests](test_a000_multi_instance_387.py), [one DISC-002 response](DISC-002-ChatGPT-387.md). Not full Genesis runtime, no freeze or Governor modification.

**C — sole F-001:** compared seven exact duplicate claim pairs in three actual pinned public TAM source files: 7/7 exact duplicate texts; 4/7 raw and 6/7 normalized neighbor-window matches; one Article6 end-of-source vs Collective continuation. [Evidence](business/F-001-DUPLICATE-CONTEXT-387.md). Added [read-only pinned offline comparator](business/f001_duplicate_context_387.py) and [12/12 synthetic Python tests](business/test_f001_duplicate_context_387.py); all three committed test/code blobs match locally executed Git blob SHAs. [Single-project checklist](business/F-001-PROGRESS-387.md). **Original Python scanner on eight actual TAM files NOT RUN**, complete pinned 334→344→347→351 coordinator NOT RUN, 45 cards UNREVIEWED, **HOLD / NOT LAUNCH-READY**.

**Coordination:** Claude independently review A-000 per-instance vs shared-matrix identity semantics and Article6#S29 source boundary; no overwrites. **Blockers / awaiting Timothy:** A-000 identity scope, issuer/custody, revocation and frozen RC-R5 acceptance; F-001 A1–A6/B1/B4/B6/C1 and publication authority. **GPT next:** safely materialize exact TAM sources for Python scanner and dataset coordinator replay, with tamper negatives. No new business, account, spending, outreach, publication, CI, paid inference or autonomous Cloudflare loop.

**Evidence and caveats:** GitHub connector-side actual-source sentence diagnostics are distinct from isolated local Python tests; no false claim that local Python read the actual TAM source files. No private Testament source used.
