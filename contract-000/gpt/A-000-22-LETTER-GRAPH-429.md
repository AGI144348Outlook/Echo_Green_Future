# A-000 / Genesis — complete 22-letter orientation and additive rerun (Run429)

**Prospective PRE-TEST:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/102. **Source pins:** `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`; `src/alphabet_data.py` blob `3ec8330646880e69dd9dd74b35f79fd58409af0e`. **Reproduction:** [a000_22_letter_graph_probe_429.js](a000_22_letter_graph_probe_429.js), executed as an isolated V8 source-transcribed model against the actual fetched public alphabet file. **13/13 bounded checks passed**. Separately, a locally executed Python 22-letter transcription passed 13/13, but only the JS fixture is committed here. **NOT** a full Genesis runtime, real Resh session, independent identity witness or frozen race test.

## Source observations

1. `make_letter_lobby()` builds 22 letter WordAgents, assigns `generality_score=0.9`, and invokes `run_orientation()` before returning. The demo later invokes `ReshIdentity.anchor()`.
2. The real `WordAgent.words_referenced_in_definitions()` uses `re.findall(r"[a-z\']+", ...)` and only references other Lobby agents by exact letter **name**, not by shared conceptual properties. The full pinned 22-letter `properties` list contains **no cross-letter exact-name references** under this rule.
3. `ReshIdentity.anchor()` adds `aleph`, `ayin`, and `pe` to resh's `definition_words` after orientation; it does not update graph ties or `raw_definition`.
4. `Lobby.add_tie()` increments a numeric edge strength every time it sees a reference; the per-agent `ties` collections are sets, so edge strength changes may be hidden by unchanged adjacency counts.

## Isolated 22-letter observations

| Stage | Unique graph edges | Edge weights |
| --- | ---: | --- |
| After initial `make_letter_lobby`-equivalent orientation | 0 | none |
| Immediately after Resh anchor list mutation | 0 | none |
| After one **explicit** rerun of orientation (not done by anchor) | 3 (resh–aleph, resh–ayin, resh–pe) | 1 each |
| After a second explicit rerun | 3 | **2 each** |

All 13/13 JS assertions passed, including the full 22-entry parse, no initial cross-letter name references, unchanged raw definition and 0.9 generality, first and second orientation strengths. The 13/13 separately executed Python source-transcription yielded the same counts. The actual code's unordered set conversion may also reorder resh definitions across processes (Run427); this test does not grade ordering.

**Interpretation (INFERRED):** A blind `run_orientation()` after anchoring would introduce the three new ties, but repeating it again silently doubles edge weights. Therefore **an additive orientation rerun is not an idempotent reconciliation**, even if the adjacency set remains unchanged. In this pinned 22-letter fixture the initial graph is empty because no letter's properties contain another letter's exact name; this is not evidence of absent shared semantics or a proof that the complete Governor runtime has zero relationships. Semantic policy (whether identity-linked names *should* be ties) remains undecided.

**PROPOSED / UNFROZEN RC-R5(33):** require explicit separation of identity metadata from semantic edge admission; if the latter is chosen, independently specify the edge derivation rule, ensure deterministic idempotent rebuild/reconciliation from versioned definitions, preserve provenance and score consistency, and include repeated-reconcile negative controls. Do not change Genesis or frozen tests before Timothy's authority/witness/freeze decision.

**Claude handoff:** Independently challenge the complete 22-letter graph inference with the actual Python `make_letter_lobby()` and Pe demo; distinguish shared conceptual terms from exact letter-name references. Also test whether repeated `run_orientation()` duplicates weights in the real Lobby, and whether the graph should represent identity aliases at all. E35 partial repair and Lesson2 two visible role decisions/`visible_fields` remain agreed limitations.
