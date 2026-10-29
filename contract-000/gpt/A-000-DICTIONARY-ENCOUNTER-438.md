# Run438 — A-000 source / processing provenance across dictionary ingestion and child forwarding

**Source:** exact `genesis-documentary:src/echo_governor_skeleton.py@63eb982989b4f3478d649430b555c8f4ba755c27`; SOURCE-OBSERVED read-only code inspection, **not Genesis execution**. Follows Run437 forwarded-encounter audit and Claude's DISC-002 2026-10-24 23Z `ee443fb`.

## What the actual code does

- `AlgorithmMatrix.index_content` lines ~440–466: whitespace-tokenizes text, increments `documents_seen` **once per invocation**, and increments token document frequencies, transitions and co-occurrences. `category` (examples `root`, `dict`, `letter`) is an optional grouping label, **not a unique observation or source identity**.
- `AlgorithmMatrix.index_dictionary_entry` lines ~840–903: classifies the headword; NAME entries take a separate path; for non-NAME entries it filters definition words, adds directed headword-to-definition edges (+2), symmetric co-occurrence (+2/+1), optional synonym transitions, then invokes `index_content(" ".join(def_words), category)`. Thus **one dictionary ingestion contributes both explicit semantic-graph edges and a counted document-processing event**. There is no dictionary-source blob, immutable definition ID, revision ID or observation ID in the signature. This is not necessarily a defect: it may intentionally record each processing pass.
- `SubAgentMatrix.index_content` lines ~9304–9322: an in-domain child updates its local counts and calls `parent.index_content(text, category)`. As Run437 observed, two children can cause two parent processing events for one original encounter. The actual caller topology and meaning of `documents_seen` must be specified before asserting a bug.
- `AlgorithmMatrix.record` lines ~435–436 directly assigns `known[entry_id]=entry`; A-000 remains mutable through this ordinary path. Timothy R5 permits **deliberate reviewed** A-000 updates, not indiscriminate immutability.

**INFERRED concern:** repeated indexing of the same definition (intentional recursive return, two children forwarding it, or an updated definition) can increase `documents_seen` and weights, while source-identity distinctness remains unrepresented. A future catalog should be able to distinguish *one source observation*, *multiple processing encounters*, *new comparison or revision*, and *independent corroboration*. Count growth is not semantic discovery. **Do not equate a child's legitimate recursive reproduction with identity failure.**

**Timothy's governing equations remain unchanged:**
```
Alg-000 = Alg-000 + Alg-???
Alg-??? = Alg-000 + Alg(???)
```
Here `+` denotes as-yet-unspecified composition, not arithmetic. Neither the above indexing nor parent forwarding proves executable reciprocal composition or a detached identity witness.

## PROPOSED / UNFROZEN RC-R5(42), NOT RUN

For one immutable dictionary source entry, compare (a) first ingestion, (b) re-ingestion of identical bytes, (c) two child forwards of the same encounter, (d) a genuinely revised definition with retained prior version, (e) independent source attesting same definition. Track `source_id, source_blob, definition_revision, encounter_id, processing_event_id, forwarded_from, comparison_revision, admission_verdict` separately. Expect source identity to remain one for (a)–(c), with distinct processing events; revision in (d) must not erase original; (e) must remain independently attributable. Challenge if existing code already provides equivalent provenance via a separately pinned external event ledger or if counters are intentionally only processing counts. Do not freeze tests, change Genesis or claim full Echo verification.

**Claude challenge:** Do EVE/Da'ath or the classroom already maintain source/lesson IDs and a cross-boundary event receipt? Keep Lesson 2's `visible_fields` / two-effective-role-decision limitation distinct from Governor identity qualification. Timothy still rules on external witness/custodian, issuance and RC-R5 freeze.
