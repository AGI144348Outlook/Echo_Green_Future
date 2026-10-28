# A-000 / Genesis — four distinct membership stores (Run420)

**Prospective PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/93; prospective refinement comment #6469626492 preceded tests. **Source pins:** `genesis-documentary:src/echo_governor_skeleton.py` blob `63eb982989b4f3478d649430b555c8f4ba755c27`; `genesis-documentary:tests/pe_ayin_resh_communication.py` blob `64a171a6791f2356006683596b56cbe289cbbdc0`. **Method:** 12 bounded lexical assertions against connector-returned source text, 5 isolated JS membership fixtures; not a full Genesis import or executed Pe demo. One initial printed-label assertion failed because the *test harness* used an incorrectly escaped JS string; corrected exact-string check passed on rerun. No source change or concealed failure.

## SOURCE-OBSERVED distinctions

1. `AlgorithmMatrix.known` begins with `A-000` and contains algorithm/identity/other recorded entries; `record()` directly writes to it. It is **not** the general word-agent membership registry. A-000's Resh anchor resides here.
2. `AlgorithmMatrix.content_units` records token document frequencies through `index_content()`; `index_dictionary_entry()` can also insert proper-name headwords. Presence means indexed token/headword occurrence, **not** a qualified semantic agent.
3. `AlgorithmMatrix.entry_classes` maps classified dictionary headwords to `TYPE`, `SPECIFIC`, `NAME`, `ABSTRACT`; a headword can be classified while absent from the Lobby.
4. `Lobby.populate()` iterates `entry_classes`, excludes `NAME`, and instantiates `WordAgent` in `lobby.agents`. This is a derived semantic-agent roster, not an independent identity witness.
5. `PeCommunicator._resh_knows()` requires an existing `lobby.agents` record; the external Pe demo reports `known_already` using `w in lobby.agents` but prints **"Already in Resh's matrix"**. Run419 identified the label mismatch; Run420 clarifies that substituting `w in matrix.known` would also be semantically wrong for ordinary vocabulary. The correct output must name **which** store/predicate is being queried.

## Isolated four-store fixture (not Genesis execution)

| Word | Algorithm/identity record | Token indexed | Classified headword | Lobby agent | Demo calls 'new pointer' |
| --- | --- | --- | --- | --- | --- |
| A-000 | true | false | false | false | true |
| token | false | true | false | false | true |
| proper | false | true | true | false | true |
| admitted | false | true | true | true | false |
| pending | false | true | true | false | true |

**OBSERVATION:** four membership predicates can disagree, and the demo's 'new' means only 'not in Lobby' for its encountered strings. **INFERENCE:** a term absent from Lobby may already have token evidence or a classified dictionary entry; do not conflate candidate discovery with novel lexical ingestion, teaching, or promotion. **LIMIT:** fixture membership sets are deliberately synthetic, and the `A-000` example is not asserted to occur in a real Pe encounter. The actual demo depends on unavailable historical datasets and was not executed.

**PROPOSED / UNFROZEN RC-R5(25):** for a Pe episode, log separately `algorithm_record_present`, `token_indexed`, `headword_classified`, `lobby_agent_present`, and `promotion_decision` with exact source and identity-witness references. A token-only or NAME-only item must not be advertised as entirely new knowledge; a word missing from the Lobby must not be called missing from the matrix. Promotion requires an authorized audited path. Do not freeze or implement before Timothy's authority and test rulings. Claude should challenge any other actual code path that unifies these stores, including post-exchange ingestion.

**Testing:** 17/17 corrected source/fixture checks PASS; previous initial printed-label harness error retained in Issue #93 POST. No Python, full Genesis, frozen tests, identity witness, or autonomous-learning validation.
