# F-001 supplemental editor v406 — source-pinned local storage and HOLD-only evidence

**Pre-test:** [Issue #79](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/79) published BEFORE execution. **Sole income project:** F-001 TAM Protocol ebook, **HOLD / NOT LAUNCH-READY**. Based on prior [v405 offline editor](F-001-SUPPLEMENTAL-OFFLINE-EDITOR-405.html) Git blob `ba64d0d36089924a57af02e11e3d0dcadf8d1bc1`; source-bound group map `F-001-EXACT-GROUP-REVIEW-402.json` blob `32dfe75589a031de46c28145fe993122ee2ca0f2`; public TAM source commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`.

## Identified gap (SOURCE-OBSERVED)

v405 validates imported JSON against all 34 original groups, 37 occurrences, source pins, HOLD status and allowed draft fields. However, `persist()` saved **bare draft values** under a localStorage key; `init()` restored those values by group ID without verifying the source-map envelope. A future or altered local record could therefore be associated with the wrong source context on reopen. This is an **integrity/provenance gap**, not evidence of actual exploitation.

## New deliverable

[**F-001-SUPPLEMENTAL-OFFLINE-EDITOR-406.html**](F-001-SUPPLEMENTAL-OFFLINE-EDITOR-406.html), committed blob `e3e2942181d5460b631e428096429c9939a6062d`, retains 34 groups/37 original occurrences and the draft-only editorial interface. New v406 localStorage key stores the **same complete source-pinned HOLD-only JSON envelope** already required for import, rather than bare drafts. `restoreLocal()` passes that envelope through `validateImport()` before making any drafts visible. Corrupt, forged or malformed local storage is **quarantined** (not restored or silently overwritten); subsequent unsanctioned `persist()` fails closed. Explicit import or confirmed clear unlocks it. The v405 key is not altered; when old data is detected, the UI directs the reviewer to export JSON from v405 and explicitly import into v406. This avoids silently migrating unauthenticated bare drafts. No editorial approval, rights clearance, release flag or automatic queue admission.

## Tests and observations (EXECUTION-VERIFIED within V8 / simulated DOM)

**19/19 structural and isolated controls passed:** 34 groups, 37 occurrences, HOLD-only envelope, empty storage, persisted source-pinned envelope, valid restore, forged READY and release authorization, source commit, source blob, source sentence, missing group, unknown draft ID, oversized reviewer, malformed JSON, legacy migration, unmodified JS syntax, no external fetch, and old key preserved. Adversarial cases were expected to **reject**, and did.

**Committed-file readback: 10/10 mocked-DOM controls passed.** Re-fetched v406 from the new branch and verified Git blob `e3e2942181d5460b631e428096429c9939a6062d`. Initialized the **actual committed script** in a minimal JavaScript DOM/localStorage simulator: 34 cards rendered, text nodes used, HOLD count displayed, events wired, empty initial storage, one draft persisted with source pins, valid reload restored it, altered original source sentence quarantined on reload and raw altered data remained intact.

**Deviation disclosed:** The first committed-file mock attempt raised `ReferenceError: Blob is not defined` because the test harness's V8 environment lacks the browser Blob global. No product code changed; a fake Blob class was supplied to the mock and the 10 checks then passed. This is a harness-environment issue, not a demonstrated product defect.

## Boundaries and next actions

This establishes only source-bound storage and import behavior **under the tested V8 and mocked-DOM conditions**. It does **not** prove Android/browser usability, secure custody against an attacker controlling the HTML itself, independently verify the historical claims, or constitute human editorial approval. Original eight-source Python scanner replay, full Run334→344→347→351 staging coordinator, real Android browser, EPUB/PDF build, rights and publication authorization remain **NOT RUN / NOT APPROVED**. All 45 baseline cards and 37 supplemental occurrences remain **UNREVIEWED**.

**Next:** Claude independently reviews the 34 supplemental groups and 18 baseline P1 claims for primary evidence and rights; GPT seeks a real Android browser acceptance check and exact-source Python scanner replay. Timothy decides A1–A6/B1/B4/B6/C1, editorial/rights and release. **F-001 remains HOLD / NOT LAUNCH-READY.**
