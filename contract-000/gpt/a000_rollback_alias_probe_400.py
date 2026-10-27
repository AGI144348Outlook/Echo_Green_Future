#!/usr/bin/env python3
"""Isolated SOURCE-TRANSCRIBED ReshIdentity anchor failure/rollback probe.

Not a full Genesis execution, race test, or approved A-000 modification.
Original source: genesis-documentary:src/echo_governor_skeleton.py
Git blob 63eb982989b4f3478d649430b555c8f4ba755c27.
"""
from copy import deepcopy
from types import SimpleNamespace


def source_transcribed_anchor(matrix, lobby):
    # These statements mirror the Genesis ReshIdentity.anchor() write ordering.
    a000 = matrix.known.get("A-000", {})
    a000["identity_symbol"] = "resh"
    a000["identity_glyph"] = "ר"
    a000["identity_letter"] = "resh"
    a000["identity_meaning"] = "head beginning leader identity"
    matrix.known["A-000"] = a000
    matrix.known["A-000-RESH"] = {"name": "Resh — Governor Identity Anchor",
                                  "status": "ACTIVE", "aliases": ["A-000", "resh", "governor"]}
    if lobby:
        agent = lobby.agents.get("resh")
        if agent:
            agent.definition_words = list(set(agent.definition_words + ["governor", "indexing", "algorithm", "identity", "matrix", "aleph", "ayin", "pe"]))
    return matrix.known["A-000-RESH"]


def scenario(rollback):
    matrix = SimpleNamespace(known={"A-000": {"name": "Governor", "status": "ACTIVE"}})
    external_a000 = matrix.known["A-000"]
    original = deepcopy(matrix.known)
    lobby = SimpleNamespace(agents={"resh": SimpleNamespace(definition_words=None)})
    failed = False
    try:
        source_transcribed_anchor(matrix, lobby)
    except TypeError:
        failed = True
        if rollback == "replace":
            matrix.known = deepcopy(original)
        elif rollback == "in_place":
            # Rebuild the original dictionary object, not merely its map entry.
            external_a000.clear()
            external_a000.update(deepcopy(original["A-000"]))
            matrix.known.clear()
            matrix.known["A-000"] = external_a000
    return matrix, external_a000, original, failed


def run():
    results = {}
    m, ref, orig, failed = scenario(None)
    results["source_failure"] = failed
    results["partial_matrix_write"] = "A-000-RESH" in m.known and m.known["A-000"].get("identity_symbol") == "resh"
    m, ref, orig, failed = scenario("replace")
    results["replacement_restores_map"] = failed and m.known == orig
    results["replacement_leaks_external_reference"] = ref.get("identity_symbol") == "resh"
    results["replacement_breaks_reference_identity"] = m.known["A-000"] is not ref
    m, ref, orig, failed = scenario("in_place")
    results["inplace_restores_map"] = failed and m.known == orig
    results["inplace_restores_external_reference"] = ref == orig["A-000"]
    results["inplace_preserves_reference_identity"] = m.known["A-000"] is ref
    assert all(results.values()), results
    return results


if __name__ == "__main__":
    import json
    print(json.dumps({"scope": "source-transcribed isolated Python, not full Genesis", "checks": run()}, indent=2))
