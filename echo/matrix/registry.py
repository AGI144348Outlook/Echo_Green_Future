"""The canonical Registry, headquarters for semantic resident identity.

R_t = (E, I, M, H, P, C): this module holds E (canonical residents) and H
(typed is-a structure). Manifestations and Presentiation routes live in the
Canvas store; they point here by canonical id and never copy a resident.

Rules kept from the Unified Spec:
- Canonical identity is stable. teach() cannot rewrite a canonical resident.
- Local additions go to a private overlay (Rendition 2), marked as such and
  unvalidated. The overlay is exported so the host can persist it.
- The seed set is small and offline. The full lobby (D1) arrives later through
  MCW; hypernyms here are a curated slice, not WordNet.
"""
from ..operators.lhea import profile

# word: (definition, [direct hypernyms])
SEED = {
    "entity": ("that which is perceived or known or inferred to have its own distinct existence", []),
    "abstraction": ("a general concept formed by extracting common features from specific examples", ["entity"]),
    "physical entity": ("an entity that has physical existence", ["entity"]),
    "object": ("a tangible and visible entity", ["physical entity"]),
    "living thing": ("a living entity", ["object"]),
    "organism": ("a living thing that can act or function independently", ["living thing"]),
    "animal": ("a living organism characterized by voluntary movement", ["organism"]),
    "mammal": ("a warm-blooded vertebrate that nourishes its young with milk", ["animal"]),
    "canine": ("any of various fissiped mammals with nonretractile claws", ["mammal"]),
    "feline": ("any of various lithe-bodied carnivores", ["mammal"]),
    "equine": ("hoofed mammals having slender legs and a flat coat", ["mammal"]),
    "dog": ("a member of the genus Canis, domesticated since prehistoric times", ["canine"]),
    "cat": ("a small domesticated feline", ["feline"]),
    "horse": ("a solid-hoofed herbivorous equine", ["equine"]),
    "bird": ("a warm-blooded egg-laying vertebrate with feathers and wings", ["animal"]),
    "sparrow": ("a small brownish-grey bird", ["bird"]),
    "attribute": ("an abstraction belonging to or characteristic of an entity", ["abstraction"]),
    "property": ("a basic or essential attribute shared by all members of a class", ["attribute"]),
    "identity": ("the distinct character of an entity; what it is and remains", ["property"]),
    "invariant": ("a quantity or feature that remains unchanged under a transformation", ["property"]),
    "process": ("a sustained phenomenon or one marked by gradual changes", ["physical entity"]),
    "phenomenon": ("any state or process known through the senses", ["process"]),
    "reflection": ("the phenomenon of a wave being thrown back from a surface", ["phenomenon"]),
    "echo": ("a reflected sound; in this project, A-000 Resh, the index made algorithm", ["reflection"]),
    "shape": ("the spatial arrangement of something as distinct from its substance", ["attribute"]),
    "line": ("a length without breadth or thickness", ["shape"]),
    "edge": ("the line along which a surface terminates", ["line"]),
    "boundary": ("the line or plane indicating the limit or extent of something", ["edge"]),
    "cognition": ("the psychological result of perception, learning and reasoning", ["abstraction"]),
    "knowledge": ("the result of perception, learning and reasoning", ["cognition"]),
    "perception": ("becoming aware of something through the senses", ["cognition"]),
    "discipline": ("a branch of knowledge", ["knowledge"]),
    "hermeneutics": ("the theory of interpretation", ["discipline"]),
    "activity": ("any specific behaviour", ["abstraction"]),
    "procedure": ("a particular course of action intended to achieve a result", ["activity"]),
    "algorithm": ("a precise procedure for solving a problem in a finite number of steps", ["procedure"]),
    "operation": ("a process or series of acts involved in a particular form of work", ["activity"]),
    "presentiation": ("making the same canonical identity present at another locus without duplication", ["operation"]),
    "system": ("a group of interacting elements forming a complex whole", ["abstraction"]),
    "framework": ("a structure supporting or containing something", ["system"]),
    "mashet": ("the framework: FLOW, TRANSFORM, SEAL", ["framework"]),
    "architecture": ("the structure and organization of a system", ["system"]),
    "lhea": ("Latin-Hebrew Execution Architecture, 22 letter operators", ["architecture"]),
    "controller": ("a device or agent that regulates a system", ["system"]),
    "governor": ("A-000: identifies, validates, opens", ["controller"]),
    "communication": ("something that is communicated by or to or between people or groups", ["abstraction"]),
    "symbol": ("something visible that represents something invisible", ["communication"]),
    "glyph": ("a written or carved symbol", ["symbol"]),
    "word": ("a unit of language that carries meaning; davar, word and thing", ["communication"]),
    "truth": ("conformity to fact or actuality", ["property"]),
    "form": ("the structure of something as distinct from its matter", ["attribute"]),
    "pattern": ("a regular and intelligible form", ["form"]),
    "state": ("the way something is with respect to its main attributes", ["attribute"]),
    "vacuum": ("an unresolved gap: a concept encountered but not yet indexed", ["state"]),
    "arrangement": ("an orderly grouping of things", ["abstraction"]),
    "matrix": ("a rectangular arrangement of elements into rows and columns", ["arrangement"]),
    "index": ("a list that routes a lookup to where something is stored", ["arrangement"]),
    "surface": ("the outermost boundary of an object", ["object"]),
    "canvas": ("a surface on which presentiations are placed and related", ["surface"]),
}


class Registry:
    def __init__(self, kernel_matrix=None):
        self.canonical = {w: {"def": d, "parents": list(p)} for w, (d, p) in SEED.items()}
        self.overlay = {}
        self.kernel_matrix = kernel_matrix
        self.kernel_indexed = 0
        if kernel_matrix is not None:
            for w, (d, _) in SEED.items():
                try:
                    kernel_matrix.index_dictionary_entry(w, d, pos="noun", category="registry")
                    self.kernel_indexed += 1
                except Exception:
                    pass

    # -- identity ---------------------------------------------------------
    @staticmethod
    def key(word):
        return " ".join((word or "").lower().split())

    def _entry(self, w):
        if w in self.canonical:
            return self.canonical[w], "canonical"
        if w in self.overlay:
            return self.overlay[w], "local-overlay"
        return None, "gap"

    def has(self, word):
        return self._entry(self.key(word))[0] is not None

    def resolve(self, word):
        """rho(word) -> resident. Unknown words resolve to an explicit gap, never an invention."""
        w = self.key(word)
        entry, source = self._entry(w)
        res = {"id": "word:" + w, "word": w, "sense": "n.01", "source": source, **profile(w)}
        if entry is None:
            res.update({"def": "Not yet indexed: a vocabulary gap.", "hypernyms": [], "hyponyms": [], "chain": []})
            return res
        res.update({"def": entry["def"], "hypernyms": list(entry["parents"]),
                    "hyponyms": self.hyponyms(w), "chain": self.chain(w)})
        return res

    # -- is-a structure (H) ------------------------------------------------
    def parents(self, w):
        entry, _ = self._entry(self.key(w))
        return list(entry["parents"]) if entry else []

    def chain(self, word, limit=24):
        """Generalization path: follow the first hypernym until the root."""
        out, cur, seen = [], self.key(word), set()
        while len(out) < limit:
            ps = self.parents(cur)
            if not ps or ps[0] in seen:
                break
            cur = ps[0]; seen.add(cur); out.append(cur)
        return out

    def ancestors(self, word):
        """All hypernyms with their depth above the word."""
        depth, frontier = {}, [(self.key(word), 0)]
        while frontier:
            w, d = frontier.pop(0)
            for p in self.parents(w):
                if p not in depth or d + 1 < depth[p]:
                    depth[p] = d + 1
                    frontier.append((p, d + 1))
        return depth

    def hyponyms(self, word):
        w = self.key(word)
        pool = list(self.canonical.items()) + list(self.overlay.items())
        return sorted(k for k, e in pool if w in e["parents"])

    def common_hypernyms(self, words):
        """Shared hypernyms, nearest first (lowest summed depth)."""
        maps = [self.ancestors(w) for w in words]
        if not maps:
            return []
        shared = set(maps[0])
        for m in maps[1:]:
            shared &= set(m)
        return sorted(shared, key=lambda h: (sum(m[h] for m in maps), h))

    # -- local overlay (Rendition 2 private state) -------------------------
    def teach(self, word, parent, definition=""):
        w, p = self.key(word), self.key(parent)
        if not w or not p:
            return False, "Both a word and a hypernym are needed."
        if w in self.canonical:
            return False, (f"'{w}' is a canonical resident. Its identity stays stable; "
                           "the local overlay can only add new words.")
        if w == p:
            return False, "A word cannot be its own hypernym."
        if w in self.ancestors(p) or w == p:
            return False, f"That would make '{w}' its own ancestor."
        entry = self.overlay.setdefault(w, {"def": definition or f"a {p} (taught locally, unvalidated)", "parents": []})
        if definition:
            entry["def"] = definition
        if p not in entry["parents"]:
            entry["parents"].append(p)
        note = "" if self.has(p) else f" '{p}' is itself a gap."
        return True, f"Added '{w}' is-a '{p}' to the local overlay (unvalidated).{note}"

    def export_overlay(self):
        return {w: dict(e) for w, e in self.overlay.items()}

    def load_overlay(self, data):
        self.overlay = {}
        for w, e in (data or {}).items():
            w = self.key(w)
            if w and w not in self.canonical and isinstance(e, dict):
                self.overlay[w] = {"def": str(e.get("def", "")), "parents": [self.key(p) for p in e.get("parents", []) if p]}

    def all_words(self):
        return sorted(set(self.canonical) | set(self.overlay))
