#!/usr/bin/env python3
"""Run401 isolated Resh alias-reference probe. NO full Genesis runtime.
Source-transcribed from genesis-documentary src/echo_governor_skeleton.py,
Git blob 63eb982989b4f3478d649430b555c8f4ba755c27.
Pre-registered BEFORE execution on Echo_Green_Future Issue #74.
Only stdlib; no network, CI, paid inference, file writes or release.
"""
from types import SimpleNamespace

class Matrix:
    def __init__(self):
        self.known = {"A-000": {"name": "Governor", "status": "ACTIVE"}}

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
            "name": "Resh — Governor Identity Anchor",
            "status": "ACTIVE",
            "type": "IDENTITY-LETTER",
            "glyph": "ר",
            "aliases": ["A-000", "resh", "governor"],
            "description": (
                "The Governor and Resh are one and the same — "
                "Resh is head, beginning, identity; the Governor "
                "reads Resh when it reads itself in the matrix. "
                "Identity validation (IDENTIFY→VALIDATE→OPEN) "
                "runs through this entry."
            ),
            "perception_operator": "ayin",
            "expression_operator": "pe",
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

def run():
    checks = {}
    def record(name, result):
        checks[name] = bool(result)
        if not result:
            raise AssertionError(name)
    m = Matrix()
    r = ReshIdentity(m)
    a = r.anchor()
    record("first_anchor_valid", r.validate() is True)
    b = r.anchor()
    record("reanchor_new_alias_object", a is not b)
    record("current_anchor_ref_matches_new", r._anchor_entry is b)
    a["aliases"] = []
    record("stale_alias_tamper_unseen", r.validate() is True and
           b["aliases"] == ["A-000", "resh", "governor"])
    b["aliases"] = []
    record("live_alias_tamper_unseen", r.validate() is True)
    r.hebrew_lobby = SimpleNamespace(agents={
        "resh": SimpleNamespace(definition_words=None)})
    prior = r._anchor_entry
    try:
        r.anchor()
        failure = None
    except Exception as exc:
        failure = type(exc).__name__
    record("reanchor_lobby_raises_typeerror", failure == "TypeError")
    record("failed_reanchor_retains_anchored_true",
           r._anchored is True and r.validate() is True)
    record("failed_reanchor_leaves_stale_anchor_entry",
           r._anchor_entry is prior and
           m.known["A-000-RESH"] is not prior)
    m2 = Matrix()
    r2 = ReshIdentity(m2, SimpleNamespace(agents={
        "resh": SimpleNamespace(definition_words=None)}))
    try:
        r2.anchor()
    except TypeError:
        pass
    record("first_failed_anchor_not_valid", r2.validate() is False)
    return checks

if __name__ == "__main__":
    import json
    results = run()
    print(json.dumps({"passed": sum(results.values()),
                      "total": len(results), "checks": results,
                      "scope": "isolated source-transcribed; not full Genesis"},
                     indent=2))
