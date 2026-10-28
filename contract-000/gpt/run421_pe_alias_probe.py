"""Run421 source-transcribed Pe log reference probe. Not full Genesis execution.
Source: genesis-documentary/src/echo_governor_skeleton.py, blob
63eb982989b4f3478d649430b555c8f4ba755c27, exchange() around 3470-3520.
Prospective pre-test: Echo_Green_Future Issue #94, addendum #6471097307.
"""
from copy import deepcopy


def source_transcribed_two_turns():
    # Minimal model of exchange()'s object lifetime: _resh_knows() returns
    # a fresh dictionary, log.append retains its raw_resh reference,
    # and knowledge = next_k precedes knowledge['word'] mutation.
    knowledge = {"word": "initial", "definition": "first", "semantic_chain": ["a", "b", "c"]}
    log = []
    for turn in (1, 2):
        log.append({"turn": turn, "raw_resh": knowledge})
        next_k = {"word": "c", "definition": "second", "semantic_chain": ["c", "d", "e"]}
        knowledge = next_k
        knowledge["word"] = "entity"
    return log


def source_transcribed_storage():
    # Literal reference relationships at end of PeCommunicator.exchange():
    # self.exchanges.append({"entity": entity_word, "log": log}); return log
    log = [{"turn": 1, "raw_resh": {"word": "entity", "definition": "fixed"}}]
    exchanges = []
    exchanges.append({"entity": "entity", "log": log})
    return log, exchanges


def run():
    count = 0
    log = source_transcribed_two_turns()
    assert log[0]["raw_resh"]["word"] == "initial"; count += 1
    assert log[1]["raw_resh"]["word"] == "entity"; count += 1
    assert log[0]["raw_resh"] is not log[1]["raw_resh"]; count += 1
    # This falsifies the original hypothesis of retroactive word change
    # from knowledge = next_k; no assertion of that change is made.
    returned, exchanges = source_transcribed_storage()
    assert returned is exchanges[0]["log"]; count += 1
    returned[0]["raw_resh"]["definition"] = "ALTERED AFTER RETURN"
    assert exchanges[0]["log"][0]["raw_resh"]["definition"] == "ALTERED AFTER RETURN"; count += 1
    returned.append({"turn": 2, "raw_resh": {"word": "forged"}})
    assert len(exchanges[0]["log"]) == 2; count += 1
    # Proposed defensive-copy counterfactual (NOT in Genesis)
    returned2 = [{"turn": 1, "raw_resh": {"word": "entity"}}]
    safe_store = [{"entity": "entity", "log": deepcopy(returned2)}]
    returned2[0]["raw_resh"]["word"] = "FORGED"
    assert safe_store[0]["log"][0]["raw_resh"]["word"] == "entity"; count += 1
    returned3 = deepcopy(safe_store[0]["log"])
    returned3.append({"turn": 2})
    assert len(safe_store[0]["log"]) == 1; count += 1
    print(f"PASS {count}/8 source-transcribed isolated Python assertions; initial knowledge-alias hypothesis falsified, caller-mutation alias observed in fixture")


if __name__ == "__main__":
    run()
