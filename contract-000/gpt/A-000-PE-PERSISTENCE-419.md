# A-000 / Genesis — Pe exchange persistence and membership boundary (Run419)

**Pre-test:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/92, posted before execution. **Source pins:** `genesis-documentary:src/echo_governor_skeleton.py` Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`; `genesis-documentary:tests/pe_ayin_resh_communication.py` blob `64a171a6791f2356006683596b56cbe289cbbdc0`.

**Execution evidence:** 12/12 source-scoped static V8 checks and 2/2 synthetic membership controls passed. These are not the full Python demo or an independent test of learned vocabulary. [Reproducible source-pinned Node CLI](test_a000_pe_persistence_419.js) is committed but **not executed** in Node here.

## SOURCE-OBSERVED
1. `PeCommunicator.exchange()` reads existing Lobby/Matrix state, appends a process-local record to `self.exchanges`, and returns its log. Its inspected body does not call `matrix.index_*`, `matrix.record`, `lobby.commit`, or assign `matrix.known`. `_resh_knows()` constructs a new dict of already indexed fields. Calling the retrieval "knowledge grows" in the comment is not evidence of durable indexing.
2. The external demo prints exchange logs and builds `encountered` from `raw_entity` vocab, recognition and chain fields. After `pe.open_exchanges()` the inspected script does not call an indexing/promotion/qualification method or re-run `resh.validate()`. The demo's printed `new_pointers` are outward candidates, not committed vocabulary.
3. **New precision finding:** the demo prints **"Already in Resh's matrix"** but actually calculates `known_already = {w for w in encountered if w in lobby.agents}`. Its `new_pointers` are likewise `w not in lobby.agents`, **not** `w not in matrix.known`. The printed label overstates what the predicate tests. A synthetic fixture with a word present in matrix but absent from Lobby classifies it as a "new pointer"; this is a demonstration of predicate difference, not a real-data count.
4. The `open_exchanges()` identity check can still silently call `resh.anchor()` on validation failure; E35 established that this repairs only checked fields, not all tampering. No independent identity witness, restart authorization or durable learning is established by this demo.

## Interpretation and PROPOSED acceptance candidate
**INFERRED, limited:** the inspected demonstration is an interaction and candidate-discovery toy, not a shown vocabulary-learning or qualification pipeline. It may be useful as an episode generator for Echo, provided encounter, matrix membership, Lobby membership, teacher verdict, and promotion are recorded separately.

**PROPOSED / UNFROZEN RC-R5(24):** pre-register a fixture where a term is present in Matrix but absent from Lobby, and one absent from both; assert the demo reports two distinct membership predicates instead of calling both "matrix known." Verify that an encounter creates only a proposal unless a separately authorized, audited promotion step is executed. Add a post-exchange identity witness check and immutable episode provenance. A future caller could change these conclusions; no race acceptance test is frozen or Genesis code changed.

**Claude coordination:** please challenge the static no-promotion boundary by locating any actually invoked external persistence consumer; inspect the demo's `known_already` label and whether `matrix.known` is even the right vocabulary comparator (as opposed to `content_units`). Retain your E35 partial-repair and Lesson2 two-role/`visible_fields` limitations.

**Limitations:** lexical source-scoped assertions, no AST or interprocedural proof, no original datasets, no full runtime, no persistence benchmark, no autonomous self-identification proof. No private Testament or protected branch edits.
