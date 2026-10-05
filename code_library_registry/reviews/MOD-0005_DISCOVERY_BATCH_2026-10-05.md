# MOD-0005 external discovery — batch 1

Date: 2026-10-05  
Module: `MOD-0005-bounded-affinity-admission`  
Abstraction freeze: `3e28fe69942088d3f65caa9aab572baf1d3a97d1`  
Result: **5 distinct repositories reviewed; 0 selected; cumulative progress 25/1,000**

The source was preserved, generalized, tested and committed before this search. Current issues were inspected first, followed by root license, current implementation/duplication, maintenance, contribution guidance and adaptation feasibility. Target licenses were identified, but no compatibility claim is made because Echo's outbound license remains unresolved.

| # | Repository and current issue | License, maintenance and contribution evidence | Fit and decision |
|---|---|---|---|
| 21 | [`langchain-ai/langchain#40502`](https://github.com/langchain-ai/langchain/issues/40502) | Root MIT; active through commit `6564f7e` on 2026-10-05; monorepo development rules present. | Narrow relevance-score normalization bug. PR [`#40555`](https://github.com/langchain-ai/langchain/pull/40555) already implements the proposed fix and tests. Reject as duplicate; no queue or tie-ledger need. |
| 22 | [`fabriziosalmi/UglyFeed#62`](https://github.com/fabriziosalmi/UglyFeed/issues/62) | Root complete AGPL-3.0; permissive contribution note; active through `7517611` on 2026-10-05. | Configuration exposes unused clustering methods and misnames a distance threshold. Correct work is configuration/API cleanup plus clustering tests, not bounded admission. Reject. |
| 23 | [`Goldziher/ai-rulez#222`](https://github.com/Goldziher/ai-rulez/issues/222) | Root MIT; detailed contribution guide; active through `ac03277` on 2026-10-05. | Open design explicitly requires BM25/vector fusion, index lifecycle, embedding gates and evaluation. It intentionally ships no absolute threshold by default. MOD-0005 lacks those systems. Reject as scope mismatch. |
| 24 | [`areguig/petit-poucet#107`](https://github.com/areguig/petit-poucet/issues/107) | Root Apache-2.0; tests-first contribution guide and one-PR-per-issue rule; active release commit `2cd52c2` on 2026-10-05. | Closest conceptual fit: bounded candidate pairs, similarity thresholds and auditable decisions could help after model benchmarking. Defer as a watch candidate because the issue is Rust and benchmark/model/license selection is the real work; MOD-0005 is no substitute. |
| 25 | [`ScottRBK/forgetful#75`](https://github.com/ScottRBK/forgetful/issues/75) | Root `LICENCE.md` is MIT; layered test guidance present; active through `f8c739f` on 2026-10-04. | Requests a generic sync/async write-policy hook using existing validation paths. Its similarity warning is context only. Reject: policy extension, identity/auth and persistence seams are outside MOD-0005. |

## Resume state

- Distinct repositories reviewed: **25 / 1,000**.
- Selected proposals for MOD-0005: **0**.
- Watch only: `areguig/petit-poucet#107`.
- Next ordinal: **26**.
- Continue with bounded candidate selection, starvation-resistant admission and auditable similarity-window issues that lack an existing implementation.
