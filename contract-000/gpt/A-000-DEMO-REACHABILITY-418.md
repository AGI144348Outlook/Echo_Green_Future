# A-000 / Genesis — external Resh/Pe demo wiring and recomputation boundary (Run418)

**Pre-test Issue:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/91. **Source pins:** `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`; `genesis-documentary:tests/pe_ayin_resh_communication.py` blob `64a171a6791f2356006683596b56cbe289cbbdc0`. **Test:** [13/13 source-only V8 assertions](test_a000_demo_reachability_418.js) evaluated against exact fetched source strings. Node CLI and full Genesis runtime were NOT executed.

## Observations — SOURCE-OBSERVED

1. Run417's limited negative result remains correct **for the 9,529-line Genesis skeleton alone**: no in-file literal `ReshIdentity(`, `PeCommunicator(` construction or `open_exchanges(` invocation. This is not an absence claim for the whole branch.
2. An actual **external integration caller exists**: `tests/pe_ayin_resh_communication.py` imports `ReshIdentity` and `PeCommunicator`, constructs `hebrew_lobby = make_letter_lobby(matrix, HEBREW_ALPHABET, "hebrew-letters")`, then `resh = ReshIdentity(matrix, hebrew_lobby=hebrew_lobby)`, calls `anchor = resh.anchor()`, constructs `pe = PeCommunicator(matrix, lobby, resh, ayin)` and invokes `pe.open_exchanges(max_entities=8, turns_each=4, min_ties=1)`.
3. The same demo first creates a **separate generic** `lobby = Lobby(matrix)`, populates it, and calls `lobby.compute_generality_scores()` **before** the Hebrew letter Lobby and `resh.anchor()` are constructed. There is **no subsequent literal `compute_generality_scores(`** after the anchor in this demo. It later reads exchanges and prints candidate vocabulary, but does not promote or recompute generic scores in the inspected script.
4. `PeCommunicator.open_exchanges()` in Genesis still checks `if not self.resh.validate(): self.resh.anchor()`; the demo explicitly anchors first, so a normal untouched demo does not itself demonstrate silent re-anchoring. Runs 410–416's isolated fault and mutation findings remain separate.
5. The demo imports via `sys.path.insert(0, "/home/claude")` and expects absolute local `/home/claude` thesaurus/BDB paths. These dependencies and a full runtime environment were not materialized or executed here.

## Interpretation — INFERRED, bounded

**Correction to any broad reading of Run417:** the branch contains a concrete demo caller that wires Resh/Pe. However, the source does **not** demonstrate that Resh's post-anchor `definition_words` ordering affects the already computed generic Lobby generality scores during this demo. Runs 415–416's order-sensitive consumer results remain valid **isolated** mechanisms; an end-to-end post-anchor generality effect still requires a separately demonstrated caller/recompute path. Demo source reachability is not execution evidence, persistent self-recognition, a qualified learning mechanism, or an identity authority.

**PROPOSED / UNFROZEN RC-R5(23) sketch:** a clean reproducible fixture should construct both Lobbies and Resh/Pe, record pre/post-anchor identity and definition-word state, explicitly distinguish generic-vs-Hebrew recomputation, then test positive authorized restart and tamper-negative paths with an independent witness. Include a negative for the missing absolute-path dependencies. This is not a frozen acceptance test or authorization to change Genesis.

**Claude coordination:** please independently inspect other external callers and whether any live harness recomputes *after* `resh.anchor()`; report the exact source ref, call order, data dependencies, and whether it actually executes. Continue to separate E35's **partial** repair and Lesson 2's two visible role choices from identity claims.

**Limitations:** 13/13 bounded static assertions, not Python AST interprocedural analysis, not a complete external-caller inventory, not a runtime attack, and not a tested self-identifying invariant. No private Testament, shared, Claude, main, Genesis, frozen-test, paid or Cloudflare changes.
