"""GF WordNet adapter for ECHO Homework.

This module keeps lexical data behind the HomeworkGovernor permission boundary.
It does not expand the Lobby by itself. Definitions and relations are returned
only for concepts already instantiated in the Lobby.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LexicalEntry:
    word: str
    definition: str
    synset: str | None = None
    relations: dict = field(default_factory=dict)
    image_refs: tuple = ()


class GFWordNetAdapter:
    """Read-only adapter over a supplied GF WordNet-derived index."""

    source_name = "GF WordNet"

    def __init__(self, governor, entries=None):
        self.governor = governor
        self.entries = {}
        if entries:
            for word, entry in entries.items():
                self.entries[word.lower()] = self._coerce(word, entry)

    def _coerce(self, word, entry):
        if isinstance(entry, LexicalEntry):
            return entry
        return LexicalEntry(
            word=word.lower(),
            definition=entry.get("definition", ""),
            synset=entry.get("synset"),
            relations=dict(entry.get("relations", {})),
            image_refs=tuple(entry.get("image_refs", ())),
        )

    def add_entry(self, word, definition, synset=None, relations=None, image_refs=None):
        """Populate the external lexical index; this grants no Lobby permission."""
        word = word.lower()
        self.entries[word] = LexicalEntry(
            word=word,
            definition=definition,
            synset=synset,
            relations=dict(relations or {}),
            image_refs=tuple(image_refs or ()),
        )

    def lookup(self, word):
        """Return an entry only when HomeworkGovernor permits this Lobby word."""
        word = self.governor.require_lobby(word)
        if word not in self.entries:
            raise KeyError(f"No GF WordNet entry loaded for {word}")
        return self.entries[word]

    def study_definition(self, word):
        """Read a permitted definition and expose its unknown words as candidates."""
        entry = self.lookup(word)
        candidates = self.governor.discover_from_definition(word, entry.definition)
        return {
            "word": entry.word,
            "definition": entry.definition,
            "synset": entry.synset,
            "relations": entry.relations,
            "candidates": candidates,
            "source": self.source_name,
        }

    def image_references(self, word):
        """Expose mapped image references only for an instantiated Lobby concept."""
        entry = self.lookup(word)
        return list(entry.image_refs)
