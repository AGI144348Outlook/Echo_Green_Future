"""ECHO dictionary provider.

Uses Princeton WordNet through NLTK as the lexical store. The dictionary is
large, but HomeworkGovernor remains the permission boundary: ECHO may read
only words already instantiated in its Lobby.
"""

class EchoDictionary:
    source_name = "Princeton WordNet / NLTK"

    def __init__(self, governor):
        self.governor = governor

    @staticmethod
    def _wordnet():
        from nltk.corpus import wordnet as wn
        return wn

    def senses(self, word, limit=8):
        word = self.governor.require_lobby(word)
        synsets = self._wordnet().synsets(word)[:max(1, int(limit))]
        return [{
            "synset": s.name(),
            "definition": s.definition(),
            "examples": list(s.examples()),
            "lemmas": [x.name().replace("_", " ") for x in s.lemmas()],
            "hypernyms": [x.name() for x in s.hypernyms()],
        } for s in synsets]

    def study(self, word, sense_index=0):
        senses = self.senses(word)
        if not senses:
            return {"word": word.lower(), "sense": None, "candidates": []}
        if sense_index < 0 or sense_index >= len(senses):
            raise IndexError("sense_index outside available senses")
        sense = senses[sense_index]
        candidates = self.governor.discover_from_definition(
            word, sense["definition"]
        )
        return {"word": word.lower(), "sense": sense, "candidates": candidates}
