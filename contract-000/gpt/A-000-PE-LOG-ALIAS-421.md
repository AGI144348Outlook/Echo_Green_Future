# A-000 / Genesis — Pe exchange evidence-reference boundary (Run421)

**PRE-TEST:** [Issue #94](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/94); prospective narrowing addendum [#6471097307](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/94#issuecomment-6471097307) posted before tests. **Source pin:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. This is a read-only source inspection plus a **source-transcribed isolated Python fixture**, not execution of the 9,528-line Genesis runtime.

## What the code actually does (SOURCE-OBSERVED)

- `PeCommunicator._resh_knows()` builds and returns a new dictionary with word, definition, semantic chain, generality, ties, etc. It does not return a direct WordAgent object.
- `PeCommunicator.exchange()` appends `{"raw_resh": knowledge, "raw_entity": entity_response}` to each turn log. Later, after the response, it assigns `knowledge = next_k` and then `knowledge["word"] = entity_word`.
- At the end, `self.exchanges.append({"entity": entity_word, "log": log})` retains the **same list** that `exchange()` returns to its caller. `open_exchanges()` also exposes those returned lists in `all_logs`.

## Prospective hypothesis, actual results, correction

**Initial hypothesis (falsified in the fixture):** the `knowledge["word"]` assignment might retroactively rewrite a previously logged `raw_resh`. Source order and **3/3** fixture assertions show that `knowledge = next_k` rebinds the local name to a fresh dictionary first; earlier raw objects remain distinct and unchanged in that modeled path. The pre-test addendum recorded this possibility **before execution**.

**Refined hypothesis (supported in fixture and directly by source references):** caller access to the returned `log` can modify `self.exchanges` after the exchange. **3/3** fixture assertions confirm list identity, nested raw-field mutation, and append mutation of the stored record. **2/2** copy-at-storage/copy-at-return counterfactual assertions show how separate snapshots avoid this specific alias.

**Result:** `8/8` isolated Python assertions passed. Command: `python run421_pe_alias_probe.py` in a local temporary working directory. This does **not** demonstrate a malicious caller, a full Genesis failure, or A-000 identity compromise. It demonstrates an evidence-integrity boundary in the inspected Pe record API; the original word-rewrite suspicion was rejected.

**Interpretation:** a mutable exchange transcript is not an independent identity witness or an append-only provenance receipt. The source does not provide immutable, independently attested logs. A defense would copy or serialize at the storage boundary, return copies, and separately define trusted audit custody. This is a design candidate only; no Genesis code, main, or frozen tests were modified.

**PROPOSED / UNFROZEN RC-R5(26):** if Pe exchange records are ever used as identity evidence, an externally mutable returned log must not change the retained audit record; test positive caller-mutation and legitimate replay/recovery, with custodian and acceptance tests chosen by Timothy. This is separate from the four-store vocabulary qualification candidate RC-R5(25) and Claude's E35 identity validation findings.

**Limitations / next:** run the real Pe class with pinned dependencies in an authorized test environment; check all callers of `self.exchanges`; have Claude independently review evidence semantics. Identity issuer, witness custody, recovery and frozen acceptance authority remain unresolved.
