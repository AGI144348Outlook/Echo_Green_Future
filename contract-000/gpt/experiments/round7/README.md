# Echo GPT Round 7 — integrated relational DSL

Prospective preregistration: issue #276, published before tests. Isolated research branch, no Genesis changes.

## Experiment

A Python stdlib research prototype defines 27 uniquely addressed glyphs, 22 canonical roles and five final variants. A bounded interpreter executes the subset `ע` (perceive), `ד` (filter), `מ` (flow), `פ` (express), `ת` (seal); other glyphs are registered but deliberately raise `NotImplementedError` rather than masquerade as executable. Each execution emits event ID, operator glyph, before/after values, packet ID and evidence provenance. Typed edges distinguish `application`, `precedes` and manually asserted `causal_claim`. Role queries are edge-relative. A toy structural model supports `do(B=...)` by overriding its declared equation.

## Actual results

15 Python unittest cases ran locally, 15 PASS, 0 failures (reported 0.000s). Checks: 27 unique coordinates; registry role alignment; DSL `עדמפ` produces expressed tuple `(1,2)` from `[0,1,2]` under externally supplied predicate `x>0`; application operator/operand; dual roles for ד; temporal precedence not inferred as causation; B effect of A and cause of C on declared causal edges; event provenance; hop budget; unknown glyph; index recipe SHA-256 tamper rejection; toy intervention changes C while A stays fixed; missing causal evidence rejected; ordered trace; unsupported glyph explicitly rejected. No tests failed or were revised. Executed Python source, test file and raw output supplied as conversation ZIP `echo_round7_relational_dsl.zip` but not committed here.

## Interpretation and limitations

The model separates execution observation from causal claims and makes operator/operand and cause/effect relational roles, preserving identity. This does NOT infer causal truth, provide 27 executable algorithms, implement a neuroplastic graph, or discover new DSL programs. Causal claims and structural equations are programmer-specified. Future work: implement causal evidence and interventions for actual glyph state transitions; typed event DAG with branching and concurrent flows; 27 mature algorithm families; independently assessed algorithm discovery.
