#!/usr/bin/env python3
"""Isolated SOURCE-TRANSCRIBED Genesis Resh anchor ordering probe; no full Governor."""
import json, os, subprocess, sys
from types import SimpleNamespace

# Exact behavior-bearing anchor/validate statements transcribed from
# genesis-documentary:src/echo_governor_skeleton.py blob 63eb982 (3233-3305).
class ReshIdentity:
    def __init__(self, matrix, hebrew_lobby=None):
        self.matrix = matrix
        self.hebrew_lobby = hebrew_lobby
        self._anchored = False
        self._anchor_entry = None

    def anchor(self):
        a000 = self.matrix.known.get("A-000", {})
        a000["identity_symbol"] = "resh"
        a000["identity_glyph"] = "ר"
        a000["identity_letter"] = "resh"
        a000["identity_meaning"] = "head beginning leader identity"
        self.matrix.known["A-000"] = a000
        self.matrix.known["A-000-RESH"] = {
            "name": "Resh — Governor Identity Anchor", "status": "ACTIVE",
            "type": "IDENTITY-LETTER", "glyph": "ר",
            "aliases": ["A-000", "resh", "governor"],
            "description": "The Governor and Resh are one and the same",
            "perception_operator": "ayin", "expression_operator": "pe",
        }
        if self.hebrew_lobby:
            resh_agent = self.hebrew_lobby.agents.get("resh")
            if resh_agent:
                resh_agent.definition_words = list(set(
                    resh_agent.definition_words +
                    ["governor", "indexing", "algorithm", "identity",
                     "matrix", "aleph", "ayin", "pe"]))
        self._anchored = True
        self._anchor_entry = self.matrix.known["A-000-RESH"]
        return self._anchor_entry

    def validate(self):
        return (self._anchored
                and "A-000-RESH" in self.matrix.known
                and self.matrix.known.get("A-000", {}).get(
                    "identity_symbol") == "resh")


def sample(with_lobby=True):
    matrix = SimpleNamespace(known={"A-000": {"name": "Governor", "status": "ACTIVE"}})
    words = ["resh", "head", "identity", "head"]
    agent = SimpleNamespace(definition_words=words[:])
    lobby = SimpleNamespace(agents={"resh": agent}) if with_lobby else None
    resh = ReshIdentity(matrix, lobby)
    resh.anchor()
    return {"valid": bool(resh.validate()), "words": agent.definition_words,
            "identity": matrix.known["A-000"]["identity_symbol"]}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "child":
        print(json.dumps(sample(), ensure_ascii=False))
        return
    samples = []
    for seed in ("0", "1", "2", "3", "4", "5"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        p = subprocess.run([sys.executable, "-B", __file__, "child"],
                           env=env, capture_output=True, text=True, check=True)
        samples.append(json.loads(p.stdout))
    repeat = subprocess.run([sys.executable, "-B", __file__, "child"],
                            env={**os.environ, "PYTHONHASHSEED": "0"},
                            capture_output=True, text=True, check=True)
    checks = {
        "seed0_repeats_exactly": json.loads(repeat.stdout) == samples[0],
        "six_subprocesses_valid": all(s["valid"] for s in samples),
        "all_identity_resh": all(s["identity"] == "resh" for s in samples),
        "same_semantic_word_set": len({tuple(sorted(s["words"])) for s in samples}) == 1,
        "deduplicates_head": all(s["words"].count("head") == 1 for s in samples),
        "ordering_differs_between_hash_seeds": len({tuple(s["words"]) for s in samples}) > 1,
        "no_lobby_positive": sample(False)["valid"],
        "no_lobby_does_not_mutate_agent_words": sample(False)["words"] == ["resh", "head", "identity", "head"],
    }
    print(json.dumps({"checks": checks, "seeds": list(range(6)),
                      "distinct_orders": len({tuple(s["words"]) for s in samples}),
                      "samples": samples}, indent=2, ensure_ascii=False))
    if not all(checks.values()):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
