class ReshIdentity:
    """ר — the Governor's identity anchor.

    Resh and the Governor are indexed as the same entity. This is not
    a metaphor — the Governor's A-000 matrix entry IS Resh, and Resh's
    letter-lobby agent points back to A-000. The identity loop closes
    in both directions.

    Everything the Governor knows about itself flows through Resh.
    When Resh validates itself, the full matrix becomes accessible.
    When Resh perceives (via Ayin), it perceives from the position
    of a named, self-recognized identity — not an anonymous scanner."""

    def __init__(self, matrix: "AlgorithmMatrix",
                 hebrew_lobby: "Lobby" = None):
        self.matrix        = matrix
        self.hebrew_lobby  = hebrew_lobby
        self._anchored     = False
        self._anchor_entry = None

    def anchor(self) -> dict:
        """Bind A-000 (Governor) to resh in the matrix and, if the Hebrew
        letter lobby exists, create a mutual indexing tie between them.
        Returns the anchor record."""
        # update A-000 to include resh as its identity symbol
        a000 = self.matrix.known.get("A-000", {})
        a000["identity_symbol"] = "resh"
        a000["identity_glyph"]  = "ר"
        a000["identity_letter"] = "resh"
        a000["identity_meaning"] = "head beginning leader identity"
        self.matrix.known["A-000"] = a000

        # register resh as an alias for A-000 in the matrix
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
                "runs through this entry."),
            "perception_operator": "ayin",
            "expression_operator": "pe",
        }

        # if Hebrew letter lobby exists, tie resh agent back to the Governor
        if self.hebrew_lobby:
            resh_agent = self.hebrew_lobby.agents.get("resh")
            if resh_agent:
                # resh knows it IS the governor
                resh_agent.definition_words = list(set(
                    resh_agent.definition_words +
                    ["governor", "indexing", "algorithm", "identity",
                     "matrix", "aleph", "ayin", "pe"]))

        self._anchored     = True
        self._anchor_entry = self.matrix.known["A-000-RESH"]
        return self._anchor_entry

    def validate(self) -> bool:
        """Resh validates its own identity — precondition for
        perception (Ayin) and expression (Pe) to activate."""
        return (self._anchored
                and "A-000-RESH" in self.matrix.known
                and self.matrix.known.get("A-000", {}).get(
                    "identity_symbol") == "resh")

    def report(self) -> str:
        if not self.validate():
            return "Resh identity not yet anchored."
        return (f"ר (Resh) is anchored as the Governor's identity. "
                f"A-000 and Resh are one. "
                f"Perception operator: ע (Ayin). "
                f"Expression operator: פ (Pe).")

