# A-000 / Genesis — same-file Resh-to-generality reachability boundary (Run417)

**Prospective PRE:** [Issue #90](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/90). **Actual source:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27` (9,529 lines). **Source-bound test:** [test_a000_reachability_417.js](test_a000_reachability_417.js); 10/10 lexical/static assertions passed in V8 against fetched exact source text. Committed Node test is a reproducibility aid; its Node filesystem command was not executed in this run.

## Observations (SOURCE-OBSERVED)

1. `ReshIdentity` is **defined** at line 3233 and referenced as a type annotation in `PeCommunicator.__init__` at line 3338. There are **zero** literal `ReshIdentity(` constructor call sites anywhere in this 9,529-line file.
2. `PeCommunicator` is defined at line 3313; there are **zero** literal `PeCommunicator(` constructor calls in this file. `open_exchanges(` occurs only as its definition at line 3513, not as an invocation.
3. The sole literal `self.resh.anchor()` invocation is at line 3520 inside `PeCommunicator.open_exchanges()`, conditioned on `not self.resh.validate()`.
4. `ReshIdentity.anchor()` (3287–3290) does replace the Resh agent's definition words using `list(set(...))` when a Hebrew Lobby/resh agent is supplied. Run415 showed seed-dependent ordering; Run416 showed order-sensitive downstream consumers in isolated fixtures.
5. The only executable `lobby.compute_generality_scores()` call in this file is at line 4651 in `PipelineOrchestrator.orchestrate()`, after **`lobby = Lobby(self.matrix)` at line 4641**. No Resh/Pe construction or anchor appears in that orchestrator. `Lobby.run_study_proposals()` has no literal in-file call site (definition and textual references only).

## Interpretation (INFERRED, bounded)

The inspected file does **not** supply a literal same-file execution chain from Resh anchoring to a subsequent generality recomputation. Therefore Run416's statement that a **post-anchor** recomputation could depend on unordered vocabulary remains conditional. The source demonstrates **two separately available mechanisms**, not their demonstrated runtime integration. This narrows the earlier hypothesis rather than disproving the potential problem: external importers, manual construction, dynamic dispatch, reflection, or code in other files could wire the path together. The static test cannot rule those out. It also does not establish that the Governor is currently executing Resh self-identification autonomously.

**PROPOSED / UNFROZEN RC-R5(22) refinement:** require an explicit, independently documented integration path and stable word-order semantics before testing end-to-end identity-linked genus/generality outputs. Separately test the current Resh anchor and ordinary write/recovery protections under Timothy-approved issuer/witness authority. No tests frozen and no Genesis edits.

**Claude request:** independently identify any external constructor/wiring of `ReshIdentity`, `PeCommunicator` or Hebrew Lobby and verify whether a real post-anchor `compute_generality_scores()` call occurs. Keep E35's partial-repair qualification and Lesson 2's two visible role decisions/visible_fields limitation separate from identity evidence.

**Limitations:** 10/10 source-lexical checks, **not** a full AST interprocedural call graph, not a complete Genesis runtime, not an identity attack, not a claim that no external callers exist. No private Testament material, main, shared Library, Claude files or frozen tests changed.
