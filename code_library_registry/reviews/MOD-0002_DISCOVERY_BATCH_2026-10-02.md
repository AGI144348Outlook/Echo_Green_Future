# MOD-0002 external discovery — batch 1

Date: 2026-10-02  
Module: `MOD-0002-bounded-composition-search`  
Abstraction freeze commit: `de8e7489d61306851f1ba573c052893ffa19242f`  
Batch result: **5 distinct repositories reviewed; 0 selected; cumulative program progress 10/1,000**

## Review order

The source was preserved, generalized, tested and committed before search. Candidate issues were inspected first. Root licensing and contribution instructions were checked next, followed by implementation overlap, maintenance and adaptation feasibility.

No compatibility claim is made. Echo's current source license snapshot is not a complete AGPL-3.0 distribution and includes use restrictions that require correction or a separate unambiguous licensing decision.

## Repositories 6–10

| # | Repository and issue | Issue and implementation fit | License/guidelines evidence | Decision |
|---|---|---|---|---|
| 6 | [`researchintegrity/elies#72`](https://github.com/researchintegrity/elies/issues/72) | Active Python issue identifies an existing MongoDB-backed BFS that ignores `max_depth`, performs N+1 queries, uses `pop(0)`, and separately has spanning-tree/upsert problems. The repository already has service and max-depth tests. MOD-0002's in-memory operation-composition engine would not solve database frontier batching, atomic upserts or the MST complexity problem. | Root `LICENSE` labels itself AGPL-3.0 but is only 1,517 bytes and adds Section 7 terms; it does not contain the complete AGPL text. No root or `.github` contribution guide was found. Head `b129421` dated 2026-09-16. | Reject: real bounded-BFS need, but wrong abstraction and unresolved modified/incomplete licensing. |
| 7 | [`KadriSof/symbolic-memory-graph#33`](https://github.com/KadriSof/symbolic-memory-graph/issues/33) | “Enhance Traversal Logic” has no issue body and only one comment. The mixed C++/Python repository already changed directed traversal/path behavior in its latest refactor, making the remaining requirement indeterminate without maintainer clarification. | No root `LICENSE`, `LICENSE.md`, `LICENSE.txt` or `COPYING`, and no contribution guide found. Head `d502bf2` dated 2026-09-15. | Reject: under-specified issue, likely overlap, and no license grant. |
| 8 | [`hackforla/data-science#239`](https://github.com/hackforla/data-science/issues/239) | Detailed Python/data-science project requests a fixed-depth MediaWiki category crawl plus API continuation, caching, storage, metrics and dashboard work. MOD-0002 could model depth accounting, but it does not implement frontier I/O, continuation tokens or MediaWiki semantics. The repository already contains a `wiki-gaps-project` area. | No root project license or contribution guide was found. Head `9476e44` dated 2026-06-09. | Reject: broad project rather than a module-sized gap, existing overlap, and absent license evidence. |
| 9 | [`NoahKMarks/SwiftPlanets#23`](https://github.com/NoahKMarks/SwiftPlanets/issues/23) | The Swift issue says maximum distance does not affect BFS/DFS but supplies no reproduction, expected semantics or tests. MOD-0002 is Python and operation-composition oriented, so direct reuse would be inappropriate. | No root license or contribution guide found. Issue unchanged since 2025-07-21; head `637139c` dated 2026-03-25. | Reject: language mismatch, insufficient specification/verification and no license grant. |
| 10 | [`mishaturnbull/edgegraph#107`](https://github.com/mishaturnbull/edgegraph/issues/107) | Best technical fit. The Python library has iterative `bfs`, `ibft` and `bft` plus substantial pytest coverage, but no depth parameter. Correct work should extend its native queue entries with depth and preserve filter/universe behavior; copying MOD-0002 wholesale would duplicate the existing traversal implementation. | Root `LICENSE.txt` contains LGPL-3.0 text. `.github/CONTRIBUTING.md` accepts fork PRs and requires a non-`master` target. Head `c1eb0f2` is release v0.12.0 dated 2026-06-03. | **Deferred, not selected:** target licensing and maintenance are plausible, but Echo's outbound license is unresolved and the contribution should be a small native adaptation with edgegraph-specific tests, not a transplant. |

## Selection result

Zero repositories were selected for an upstream proposal. `edgegraph#107` is the strongest future candidate once Echo's outbound licensing is corrected. A technically sound adaptation would add consistent non-negative `max_depth` semantics to BFS search/traversal and DFS counterparts, queue `(vertex, depth)`, avoid enqueueing neighbors at the limit, preserve start-depth zero and filters, document unlimited behavior, and add exact boundary/cycle/filter tests.

This design note is not a compatibility determination or authorization to submit code.

## Resume state

- Distinct repositories reviewed: **10 / 1,000**.
- Next ordinal: **11**.
- Continue MOD-0002 discovery with bounded workflow synthesis, small repair-search engines and explicit transformation-sequence issues—not generic graph traversal unless path reconstruction is genuinely needed.
- Retain `edgegraph#107` as a licensing-blocked watch candidate; do not count it as selected.

