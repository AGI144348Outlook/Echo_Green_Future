# ECHO-016 — Algorithm Matrix + discoverable MCP dictionary + Neon card/evidence networks

**Status:** completed bounded comparative **in-process** trial, November 12, 2026. **Not** a deployed autonomous Echo runtime, a production MCP endpoint, or a demonstration of independent semantic learning.

**Pre-test plan:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/437  
**First failed CI run:** https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/43185098765  
**Passing CI run:** https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/43185167189  
**Tested commit:** `6d588c0609e541a5091968e6aafad627269a2655`  
**Environment:** Node.js 24, GitHub Actions Ubuntu runner; local SQL-result projection of **real existing Echo dev Neon structure**, with schema counts separately queried through the connected Neon account. No LLM calls or live CI-to-Neon credentials.

## Research question

Can Echo algorithmically interpret the *discovered descriptions* of MCP tools—including a dictionary whose positive self-description says **"Use it for gaining additional meaning..."**—to select operations appropriate to a contextual objective? Does bounded feedback from A-101 UCB, A-105 EMA, and A-120-style quality scoring improve held-out performance?

### Architectural components exercised

The experiment loaded the 65-entry Echo Algorithm Matrix and checked registry entries `A-000`, `A-101`, `A-105`, `A-120`, `A-121`, `A-134`, `A-166`. It then used the actual [Echo MCP application-level JSON-RPC handler](../neon/card_evidence_rpc.mjs) and [parameterized Neon SQL adapter](../neon/neon_pg_adapter.mjs) through an **in-memory data adapter** reproducing the exact public 22-word WordNet fixture and the Neon development-branch projections. Neither the original 9k-line Governor nor the separate 3³ Neon neuroplasticity runtime was launched.

The model discovered read-only tools through `tools/list`; descriptions, input schemas and a limited synthetic mission context were available. A generic argument binder supplied parameters from the shared task context based on each selected tool's declared required input schema. Tool results were graded for task relevance and source-linked provenance, **not just non-error RPC responses**. Only training outcomes updated the UCB/EMA policy.

## Preregistered experimental design

- **Five task families:** dictionary meaning, dictionary lexical relationship comparison, pinned catalog-card retrieval, evidence-edge traversal, and evidence-node inspection.
- **Twenty training episodes:** four per family.
- **Fifteen held-out paraphrase episodes:** three per family.
- **Four strategies:** fixed dictionary lookup, descriptions removed, metadata-only similarity ranker, and metadata ranker with bounded UCB/EMA learning.
- **Equal budget:** one tool invocation per ordinary episode, identical public WordNet data. The contextual model could only select from discovered, authorized **read-only** tools.
- **No claims of out-of-domain generalization:** heldout items were task paraphrases, with significant vocabulary overlap. Reward rubric and descriptions were authored for this fixed benchmark.

## Actual observations

| Policy | Training correct / 20 | Heldout correct / 15 | Heldout completion / 15 | Heldout source witnesses | Mean heldout reward |
|---|---:|---:|---:|---:|---:|
| Fixed dictionary | 4 | 3 | 3 | 3 | 0.200 |
| Descriptions hidden | 4 | 3 | 3 | 3 | 0.200 |
| Metadata similarity (nonadaptive) | **13** | **11** | **11** | **10** | **0.710** |
| Metadata + UCB/EMA feedback | **14** | **10** | **10** | **9** | **0.643** |

The initial GitHub Actions run executed the new test suite and **9 of 10 tests passed**. The remaining assertion failed solely because floating-point arithmetic returned `0.6499999999999999` while the assertion expected exactly `0.65`. No comparative trial ran on that initial failed job because CI stopped at unit tests. The assertion was corrected to use a `1e-12` tolerance. The next CI run passed **10 new experiment tests** and **8 pre-existing Echo MCP tests**, and executed the comparative benchmark successfully. GitHub-hosted action tooling also emitted Node-version deprecation maintenance warnings, not a Python or JavaScript test failure.

**Six additional negative-control observations:** unadmitted dictionary words were refused; an attempt to propose an authority-stamp card through an unauthorized tool was denied; a nonexistent exact revision returned no card; a comparison remained provisional; withholding a lexical evidence edge produced abstention; and dictionary discovery exposed its positive, nonconditional "Use it for…" description.

### Actual isolated Neon branch witnesses

Neon project: `lexicon-catalog` (no change to default). Child branch: `echo-card-evidence-dictionary-dev-20261112`.

Before the experiment: **22 WordNet dictionary rows, 22 pinned lexical cards, 73 graph nodes, 124 proposed lexical-path edges.** These counts and the exact source/card/edge lineage for `being` and `existence` were verified through real Neon SQL reads (but **not** read by the GitHub-hosted algorithmic trial).

After running CI, the research ledger was updated **only on the Neon child branch**:
- one new proposed card `echo016:trial-report@1` with the actual measurements and CI evidence link;
- a source experiment node plus two observation nodes;
- two provisional empirical evidence relationships linking the CI run to the observations;
- four explicitly non-executing, synthetic evaluation receipts, one for each policy.

The Neon child branch currently has **23 cards, 76 evidence nodes, 126 evidence edges and 4 receipts**, with the original **124 WordNet edges intact**. The new research card is `review_state='proposed'` and explicitly `outcome_status='research_observation_unverified'`.

## Interpretation and negative findings

**Supported within this benchmark:** contextual, discoverable tool descriptions improved task-matched tool selection from **3/15** to **11/15** on held-out paraphrases, while preserving lexical-source attribution and guard checks. This is a measurable effect of metadata-guided tool employment in a narrow algorithmic setting.

**Not supported:** adding UCB/EMA feedback did **not** improve held-out performance above the metadata-only selector. It improved training from **13/20** to **14/20**, but heldout deteriorated from **11/15** to **10/15**. The trial does not establish durable neuroplastic development, genuine linguistic comprehension, or causal benefit of a 3³ substrate.

**Important caveat:** the descriptor-informed tool chooser still uses fixed tokenization, scoring functions, a known family of tasks and an explicit reward rubric. Its behavior is **functional context-sensitive selection**, not proof that Echo can understand tools generally; the results could be sensitive to authored description wording.

## Limitations and next experiments

1. **Live MCP and Neon:** The trial exercised *actual Echo RPC/adaptor source code* in process with a fixture-shaped SQL query adapter. The GitHub runner **did not call live Neon**, and no MCP Streamable HTTP server or delegated OAuth identity was used.
2. **Algorithm Matrix:** The harness references existing named A-101/A-105/A-120 concepts but implements a **bounded experiment-specific approximation**, not direct use of every Governor class or the full 3³ wave/neuroplastic design.
3. **Generalization:** Heldout set used novel phrasing but overlapping vocabulary and five predefined goals; measure on unseen tool descriptions, tasks, and independently adjudicated semantic relations next.
4. **Tool claims:** Discovery metadata is self-reported capability information. Validate effectiveness from observed outcomes and secure capability grants separately.
5. **Knowledge:** Evidence graph paths are proposed WordNet-derived lexical relations, not independently verified facts. No new Lobby words were admitted.
6. **Security:** Protected writes and role escalation remained denied under mock trusted context; this is not a production authorization penetration test, nor a live RLS verification.
7. **Adaptive design:** Compare feature-specific UCB, explicit reward calibration, A-105 threshold gating and multi-step delayed outcomes with the same call budget before making any neuroplastic claim.

**Decision:** Keep metadata-guided discovery as a validated **research candidate**. Keep neuroplastic adaptation **experimental** until it beats metadata-only baselines on genuinely novel, independently graded contexts. Do not change NexusBoard, the original `autonomous-agency` branch, Echo's live warehouse, or Neon default branch on the basis of this preliminary study.
