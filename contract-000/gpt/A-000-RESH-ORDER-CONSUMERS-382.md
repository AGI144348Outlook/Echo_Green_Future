# A-000 / Resh Lobby definition-order consumer trace — Run 382

**Pre-test:** [Issue #13, PRE 6429357855](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6429357855). **Authority:** Contract-000 `0fbc794`, DISC-002 `ee443fbc`, TJ R5; **source:** `genesis-documentary:src/echo_governor_skeleton.py` exact blob `63eb982989b4f3478d649430b555c8f4ba755c27`. Read the entire source, not just the anchor excerpt.

## Observations (source-level, not full Genesis execution)

Seven bounded source assertions matched **7/7**: `ReshIdentity.anchor()` uses `list(set(...))` on `resh_agent.definition_words`; `Lobby._compute_genus_depths()` selects the **first** qualifying definition word then `break` (around lines 1281–1291); `WordAgent.report()` exposes only `definition_words[:8]` (around 1118); `PeCommunicator._resh_knows()` joins only the first ten (around 3359); curriculum builders join definition words in their current order (around 1543/1716); overlap/Jaccard converts them to sets (around 1486); `WordAgent` tie extraction uses set-based token accumulation (around 1108).

An isolated, **synthetic two-order first-match model** with available words `governor` and `identity` selected `governor` from `[governor, algorithm, identity]` and `identity` from `[identity, governor, algorithm]` (**2/2 expected selections**). This is a bounded demonstration of a possible dependency, **not** a full execution of `_compute_genus_depths()` or proof that a real resh Lobby has both qualifying dictionary agents.

## Interpretation and counter-evidence

Run381 established nondeterministic output order from the anchor's set conversion. Run382 finds a **real order-sensitive consumer**: genus inference chooses the first qualifying word. That gives a plausible path from resh anchor order to a different genus head and depth/generalization score, **if** resh is present in the dictionary and multiple qualifying words exist at that time. The first-eight/first-ten report slices can also expose different visible words. Conversely, Jaccard overlap and set-based tie extraction are order-insensitive. Some curricula are constructed before the anchor, so no retroactive change is established.

## Proposed (not implemented)

First determine whether `definition_words` is an ordered sequence or an unordered membership set, whether duplicates carry evidence, and when genus/study-group recomputation occurs relative to anchoring. If a set, use a documented canonical sort; if an ordered sequence, stable deduplication may preserve original lexical order. Do not silently replace an author-defined semantic ordering. Freeze a controlled actual-Lobby test with two qualifying genus heads and a failure receipt only after Timothy's boundary decision. No A-000 write, identity witness, race acceptance or main change was made.

**Claude coordination:** independently trace whether `resh` participates in the actual `_compute_genus_depths()` call after anchoring, and whether consumers cache pre-anchor values. Keep the Swadesh Lesson 2 two-role/40-item caveat separate from A-000 identity. **Timothy pending:** external identity witness/custodian, retention and freeze; ordered-versus-set semantics for resh definition words.
