"""Isolated source-transcribed probe: NOT the complete Genesis runtime.
Pinned Genesis src/echo_governor_skeleton.py blob 63eb982989b4f3478d649430b555c8f4ba755c27.
Reproduces ReshIdentity.anchor list(set(...)) and Lobby._compute_genus_depths first-known-word heuristic.
"""
import json, os, subprocess, sys

ADDITIONS = ["governor", "indexing", "algorithm", "identity", "matrix", "aleph", "ayin", "pe"]


def genus_first(definition_words, known, stop=frozenset()):
    """Source-equivalent selection loop from Lobby._compute_genus_depths."""
    for word in definition_words:
        if word != "resh" and word in known and word not in stop:
            return word
    return None


def resh_anchor_words(old):
    """Exact expression from ReshIdentity.anchor; no production mutation."""
    return list(set(old + ADDITIONS))


def one(seed):
    script = """import json
ADDITIONS = ['governor','indexing','algorithm','identity','matrix','aleph','ayin','pe']
old=['governor','matrix','governor']
words=list(set(old+ADDITIONS))
known={'resh','governor','matrix'}
genus=next((w for w in words if w != 'resh' and w in known),None)
print(json.dumps({'words':words,'genus':genus}))"""
    env = dict(os.environ, PYTHONHASHSEED=str(seed))
    p = subprocess.run([sys.executable, "-B", "-c", script], env=env,
                       text=True, capture_output=True, check=True)
    return json.loads(p.stdout)


def main():
    known = {"resh", "governor", "matrix"}
    baseline = ["governor", "matrix", "governor"]
    assert genus_first(baseline, known) == "governor"
    assert len(baseline) == 3
    normalized = resh_anchor_words(baseline)
    assert len(normalized) == len(set(normalized))
    assert len(normalized) == 8
    assert set(normalized) == set(ADDITIONS)
    assert resh_anchor_words(normalized) != []
    assert genus_first(["matrix", "governor"], known) == "matrix"
    assert genus_first(["governor", "matrix"], known) == "governor"
    samples = {i: one(i) for i in range(8)}
    genera = sorted({v["genus"] for v in samples.values()})
    assert genera == ["governor", "matrix"], genera
    assert all(len(v["words"]) == 8 for v in samples.values())
    # Stored generality scores are not recomputed by anchor in source;
    # this assertion only checks our synthetic representation.
    stale_score = {"resh": 0.25}
    resh_anchor_words(baseline)
    assert stale_score == {"resh": 0.25}
    print(json.dumps({"assertions": 11, "seeds": 8, "genera": genera,
                      "genus_counts": {g: sum(v["genus"] == g for v in samples.values()) for g in genera},
                      "baseline_genus": "governor", "note": "isolated synthetic only"}, sort_keys=True))

if __name__ == '__main__':
    main()
