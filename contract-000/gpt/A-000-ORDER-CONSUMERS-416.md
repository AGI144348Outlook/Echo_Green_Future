# A-000 / Genesis — actual order-sensitive consumers of Resh vocabulary (Run416)

**Pre-test:** [Issue #89](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/89). **Actual source:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. **Reproducible isolated probe:** [test_a000_order_consumers_416.py](test_a000_order_consumers_416.py), committed Git blob `e11a832c431d23fa0543dcdd04d4349b0120fce1`. Python 3.13.5.

## Source-observed (not inferred from a name)

Run415 demonstrated that `ReshIdentity.anchor()` lines 3287–3290 deduplicates `resh_agent.definition_words` with `list(set(...))`, producing noncanonical ordering across Python hash seeds. Run416 inspected **actual downstream code**:

1. `Lobby._compute_genus_depths()` (lines 1274–1305) selects the **first** eligible `definition_words` member also in `self.agents` as a genus. `Lobby.compute_generality_scores()` calls it around line 1250. For a Hebrew-letter Lobby with `resh`, `aleph`, `ayin`, `pe`, these are actual letter-agent names and can be competing candidates. A call after a Resh re-anchor could therefore depend on order; **actual timing/call-path remains unverified**.
2. `LogicReasoningMatrix._is_genuine_subtype()` (lines 6279–6291) checks the **first five** indirect definition words; the same set in another order can change a subtype result. The normal `_find_specializations()` filter excludes `department='letter'`, so this is a genuine general consumer but **not evidence that normal Resh specialization invokes it**.
3. `WordAgent.report()` (around line 1119) projects the **first eight** definition words; `Lobby.run_typed_study_groups()` (around line 1543) joins all definition words into curriculum text. These are order-sensitive representations, though their identity-signature significance is unproven.
4. `RussianDollGenerality._genus_of()` (around lines 7729–7745) also chooses the **first** eligible noun-parent word. This is another source-level candidate; it was not exercised in the isolated Run416 fixture.

## Execution-verified: isolated source-transcribed fixture only

The 10/10 Python controls passed. Identical Resh word sets ordered `aleph,ayin,pe,governor` vs `ayin,aleph,pe,governor` produced **genus depths 2 vs 1** when `aleph` led to `pe` and `ayin` had no parent. An independent six-word subtype fixture placed a bridge to an abstract term first vs sixth: `_is_genuine_subtype()` returned **True vs False** despite identical word sets. Direct-subtype positive, absent-subtype negative, stable-repeat and report/curriculum order-projection checks passed.

The fixture copies behavior-bearing method statements with simplified STOPWORDS and boilerplate constants that do not affect the discriminating words. It is **not a full Genesis import, not the real Hebrew Lobby data, not a production identity exploit, and not proof that a live Governor recomputes generality after anchor**. No Genesis, shared Library, Claude branch, main or frozen tests changed.

## Interpretation and candidate specification

**Observed:** order-sensitive consumers exist in actual Genesis source; synthetic identical-set permutations change two computations. **Inferred:** if a real Resh re-anchor occurs before a dependent recomputation, order changes may propagate into genus/generality, reported definitions or curriculum. **Not demonstrated:** runtime reachability, persisted identity divergence or a downstream security impact.

**PROPOSED / UNFROZEN refinement to RC-R5(22):** use canonical ordering for identity-linked word sets *or* explicitly preserve original lexical order with a stable deduplication rule; compare downstream genus, report and curriculum outputs under two clean hash seeds. If the intended semantics are set-based, canonicalize before any order-sensitive use; if ordered, preserve provenance rather than sort away meaning. Include a changed-word negative and a legitimate bootstrap/restart positive. Do not freeze without Timothy's issuer/witness/recovery decisions.

**Claude coordination:** please independently check whether the actual Hebrew-letter Lobby ever recomputes `compute_generality_scores()` after `ReshIdentity.anchor()`, and whether the LRM excludes all letter-domain paths. E35's precise partial repair and Lesson2's two visible role-label decisions remain accepted; neither is a proof of independent A-000 continuity.
