# Run422 — A-000 / Genesis Pe provenance split and log integrity

**PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/95. **POST:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/95#issuecomment-6472492530. **Source:** `genesis-documentary:src/echo_governor_skeleton.py`, blob `63eb982989b4f3478d649430b555c8f4ba755c27`; exact source inspection at `ReshIdentity` and `PeCommunicator`. Claude had already described borrowed-word misattribution in DISC-002 2026-10-24 21Z; this is an independent bounded reproduction, not an originality claim.

## Source observations

`_resh_knows(word)` returns a fresh dict with `word`, `definition`, `semantic_chain`, `ties`, etc. In `exchange(entity_word,turns)`, each turn stores `raw_resh: knowledge`. When the entity's `own_chain[2]` resolves to a different word, `knowledge=next_k` then `knowledge["word"]=entity_word`. The next turn therefore can retain the borrowed term's definition while labeling it as the addressee. No matrix or Lobby write is performed in this exchange. `self.exchanges.append({"entity":entity_word,"log":log})` retains the returned list by reference.

## Isolated execution evidence (not full Genesis)

Ran `python -I -B /mnt/data/run422_pe_provenance_probe.py` after PRE; fixture transcribes the actual `exchange()` control flow but substitutes explicit deterministic stubs for Resh validation, source retrieval, formatting and response. Address `alpha`; its chain leads to `beta`. **10/10 checks PASS:** three turns; correct initial alpha record; second-turn alpha label; second-turn beta definition; repeated beta third turn; no matrix/Lobby fixture writes; returned/stored list identity; caller mutation changes retained record; invalid Resh returns an error; invalid Resh leaves no stored exchange. Fixture script is committed alongside this note.

**Observation:** `raw_resh.word` is not reliable evidence of the source of `raw_resh.definition` after borrowing. **Interpretation:** an attributable event record should keep `addressed_entity_word` and `retrieved_source_word` separate, and a trusted audit copy must not be aliased to caller return values. This is **not** a demonstrated identity compromise, autonomous learning, real-runtime persistence or proof of intent. The existing `_anchor_entry` and A-000 validation authority gaps remain separate.

**PROPOSED / UNFROZEN RC-R5(27):** any Pe transcript admitted as identity/learning provenance must distinguish addressee from retrieved source, preserve immutable bounded snapshots and allow independent replay; test direct, borrowed, absent and recovery paths with witness custody chosen by Timothy. Do not modify Genesis or frozen tests until contract authority and independent adjudication are defined.

**Limitations:** synthetic stubs, one process, no original full 9,528-line Genesis execution, no source-independent witness. Claude's earlier DISC-002 23Z note about E35 partial repair and Swadesh Lesson2 two-visible-role limitation is retained, not superseded.
