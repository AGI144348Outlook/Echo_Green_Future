# Builds a runnable Sandbox ECHO from the skeleton + the repo's matrices.
import json, re
def load_echo(sk, mx):
    matrix = sk.AlgorithmMatrix()
    lobby = sk.Lobby(matrix)
    stop = set(getattr(sk, "STOPWORDS", ()))
    for w, d in mx["echo_lobby_agents"].items():
        definition = d.get("definition") or ""
        dw = [t for t in re.findall(r"[a-z]+", definition.lower()) if t not in stop and len(t) > 2]
        a = sk.WordAgent(w, dw, d.get("entry_class") or "ABSTRACT", d.get("department") or "noun", matrix, raw_definition=definition)
        a.ties = set(d.get("ties") or []); a.neighborhood = d.get("neighborhood"); a.generality_score = d.get("generality_score") or 0.0
        lobby.agents[w] = a
    lexicon = {w: {"desc": (d.get("definition") or "")} for w, d in mx["echo_lobby_agents"].items()}
    for w, d in mx["echo_wordnet_chains"].items():
        lexicon.setdefault(w, {"desc": d.get("definition", "")})
    comm = sk.AlgorithmicCommunicator(lobby=lobby, vgm=mx["echo_vgm"], lexicon=lexicon,
                                      number_agents=mx["echo_number_matrix"], alg_matrix=mx["echo_algorithm_matrix"])
    # Glyph-aware tokenizer (Sandbox only; the GitHub source keeps its original [a-z]+ tokenizer).
    # English words: as before (3+ letters, stop words removed). Hebrew: every glyph gets through;
    # a single glyph is read as its letter (ר -> resh); a Hebrew word is kept whole and also read letter by letter.
    import types as _types
    glyph_name = {v["glyph"]: k for k, v in getattr(sk, "HEBREW_LETTER_INDEX", {}).items() if isinstance(v, dict) and v.get("glyph")}
    def _tokenize(self, text):
        out = []
        for m in re.finditer(r"[a-z]+|[\u05d0-\u05ea]+", text.lower()):
            t = m.group(0)
            if "\u05d0" <= t[0] <= "\u05ea":
                if len(t) == 1: out.append(glyph_name.get(t, t))
                else: out.append(t); out.extend(glyph_name.get(c, c) for c in t)
            elif t not in self.STOP_WORDS and len(t) > 2:
                out.append(t)
        return out
    comm._tokenize = _types.MethodType(_tokenize, comm)
    comm.glyph_name = glyph_name
    return {"matrix": matrix, "lobby": lobby, "comm": comm, "lexicon": lexicon}


class Evolution:
    """A real evolution loop for Sandbox ECHO.
    Observe: what actually happened in the terminal (gaps, shallow words, rejected replies).
    Diagnose -> Propose -> Validate -> Govern -> Select -> Apply -> Measure, one cycle per Step."""
    PROTECTED = {"resh", "governor", "echo"}
    FORMAT_WORDS = {"lhea", "match", "glyph", "val", "class", "mother", "double", "elemental", "sofit", "connection", "connections"}
    SUFFIXES = [("ies", "y"), ("ing", ""), ("ing", "e"), ("ed", ""), ("ed", "e"), ("es", ""), ("s", ""),
                ("ly", ""), ("ness", ""), ("ers", ""), ("er", ""), ("est", ""), ("ation", "e"), ("ment", ""), ("ity", "e")]
    def __init__(self, sk, e, learned=None):
        self.sk, self.e, self.comm, self.lobby, self.lex = sk, e, e["comm"], e["lobby"], e["lexicon"]
        self.obs, self.taught, self.learned, self.t, self.queue = [], {}, [], 0, []
        self.stop = set(getattr(sk, "STOPWORDS", ())) | set(self.comm.STOP_WORDS)
        self.inward = sk.InwardSearchEngine(alg_matrix=self.comm.alg_matrix, vgm=self.comm.vgm, number_agents=self.comm.number_agents)
        for item in (learned or []): self._apply(item, record=False); self.learned.append(item)
    # --- what he perceives about a word right now
    def _status(self, w):
        cls = self.comm._ayin_classify(w)
        depth = len(self.comm.gen_stack.build(w, 6))
        return {"word": w, "gap": "GAP" in cls, "depth": depth}
    def observe(self, text, reply):
        toks = self.comm._tokenize(text)
        self.obs.append({"text": text, "tokens": toks, "feedback": None})
        return len(self.obs)
    def feedback(self, ok):
        if not self.obs: return "No reply to mark yet."
        self.obs[-1]["feedback"] = bool(ok); return "Marked the last reply " + ("=T" if ok else "=F") + "."
    def teach(self, word, definition):
        w = word.lower().strip(); self.taught[w] = definition.strip(); return w
    def measure(self):
        toks = [t for o in self.obs for t in o["tokens"]]
        if not toks: return {"tokens": 0, "indexed": 0.0, "depth": 0.0, "rejected": 0}
        st = [self._status(t) for t in toks]
        return {"tokens": len(toks), "indexed": round(sum(not s["gap"] for s in st) / len(st), 3),
                "depth": round(sum(s["depth"] for s in st) / len(st), 2),
                "rejected": sum(1 for o in self.obs if o["feedback"] is False)}
    # --- the loop
    def diagnose(self):
        d, seen = [], set()
        for o in self.obs:
            for t in o["tokens"]:
                if t in seen: continue
                seen.add(t); s = self._status(t)
                if s["gap"]: d.append({"type": "GAP", "word": t})
                elif s["depth"] <= 1: d.append({"type": "SHALLOW", "word": t})
            if o["feedback"] is False: d.append({"type": "REJECTED", "text": o["text"]})
        return d
    def _content(self, text):
        import re as _r
        return [w for w in _r.findall(r"[a-z]+", text.lower()) if w not in self.stop and len(w) > 2]
    def _stem(self, w):
        for suf, add in self.SUFFIXES:
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                cand = w[: -len(suf)] + add
                if cand in self.lobby.agents: return cand
        return None
    def propose(self, defs):
        cands, needs = [], []
        for d in defs:
            w = d.get("word")
            if d["type"] == "REJECTED":
                for t in self._content(d["text"]):
                    if t not in self.taught: needs.append(t)
                continue
            if w in self.taught:
                cands.append({"kind": "taught", "word": w, "definition": self.taught[w], "fix": d["type"]}); continue
            if d["type"] != "GAP": needs.append(w); continue
            stem = self._stem(w)
            if stem:
                base = (self.lex.get(stem) or {}).get("desc", "")
                cands.append({"kind": "stem", "word": w, "stem": stem, "definition": f"a form of {stem}: {base}", "fix": "GAP"}); continue
            r = self.inward.search(w)
            if r.found and r.sources:
                cands.append({"kind": "inward", "word": w, "definition": "; ".join(s["detail"] for s in r.sources)[:300], "fix": "GAP"}); continue
            needs.append(w)
        self.queue = sorted(set(needs))
        return cands
    def validate(self, c):
        words = self._content(c["definition"])
        grounded = [x for x in words if x in self.lex and x != c["word"] and x not in self.FORMAT_WORDS]
        if len(words) < 2: return False, 0, "definition too thin (fewer than 2 content words)"
        if not grounded: return False, 0, "not grounded: no word of the definition is known to him"
        if c["kind"] == "inward" and len(grounded) < 2: return False, 0, "inward match too weak (grounded in fewer than 2 known words)"
        if c["word"] in self.lobby.agents and c.get("fix") == "GAP": return False, 0, "already indexed"
        return True, len(grounded), f"grounded in {len(grounded)} known words: " + ", ".join(grounded[:5])
    def govern(self, c, accepted):
        if c["word"] in self.PROTECTED: return False, "protected identity word (A-000 invariant)"
        if accepted >= 5: return False, "cycle budget reached (5 changes)"
        if len(self.lobby.agents) >= 5000: return False, "lobby at capacity"
        return True, "within budget"
    def _apply(self, item, record=True):
        w, definition = item["word"], item["definition"]
        hw = getattr(self, "hw", None)
        if hw is not None and w not in hw.vocab:   # invariant: transcribe into the Vocabulary Registry before lobbying
            hw.vocab[w] = {"pos": "noun", "definition": definition, "lateral": f"{w.capitalize()} = ({item.get('source', 'taught')})",
                           "chain": [w], "analog": "|{}|", "main": [], "level": None, "into": [], "step": 0, "source": item.get("source", "taught")}
        dept = "noun"
        if item.get("stem") and item["stem"] in self.lobby.agents: dept = self.lobby.agents[item["stem"]].department or "noun"
        dw = self._content(definition)
        a = self.sk.WordAgent(w, dw, "ABSTRACT", dept, self.e["matrix"], raw_definition=definition)
        a.ties = set(x for x in dw if x in self.lobby.agents)
        if item.get("stem"): a.ties.add(item["stem"])
        self.lobby.agents[w] = a
        self.lex[w] = {"desc": (item["stem"] + " " + definition) if item.get("stem") else definition}
        sg = getattr(self.lobby, "study_groups", None)
        if isinstance(sg, dict):
            sg[w] = {"topic": w, "leader": w, "curriculum": " ".join(dw), "department": dept, "entry_class": "ABSTRACT",
                     "generality": 0.0, "invited": set(a.ties), "found": set(), "thesaurus": set()}
    def step(self):
        self.t += 1
        before = self.measure()
        defs = self.diagnose()
        cands = self.propose(defs)
        results, accepted = [], 0
        for c in cands:
            ok, margin, why = self.validate(c)
            if ok:
                g, gwhy = self.govern(c, accepted)
                if not g: ok, why = False, gwhy
            c.update({"passed": ok, "margin": margin, "why": why}); results.append(c)
        chosen = sorted([c for c in results if c["passed"]], key=lambda c: -c["margin"])[:5]
        for c in chosen:
            item = {"word": c["word"], "definition": c["definition"], "source": c["kind"], "stem": c.get("stem"), "cycle": self.t}
            self._apply(item); self.learned.append(item); self.taught.pop(c["word"], None); accepted += 1
        acc = {c["word"] for c in chosen}
        self.queue = sorted(set(self.queue) | {c["word"] for c in results if not c["passed"] and c["word"] not in self.PROTECTED})
        self.queue = [w for w in self.queue if w not in acc]
        for o in self.obs:
            if o["feedback"] is False and acc & set(o["tokens"]): o["feedback"] = "addressed"
        after = self.measure()
        return {"t": self.t, "deficiencies": defs, "candidates": results, "accepted": [c["word"] for c in chosen],
                "needs_teaching": self.queue, "before": before, "after": after, "lobby": len(self.lobby.agents)}

def boot_echo(sk, mx, learned=None, dictionary=None, vocab=None):
    e = load_echo(sk, mx); e["_vocab_in"] = vocab
    if dictionary: e["dict"] = Dictionary(dictionary)
    e["_vocab"] = None
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        e["lobby"].run_study_proposals(); e["lobby"].run_typed_study_groups()
    e["evo"] = Evolution(sk, e, None)
    if e.get("dict"):
        hw = Homework(e["dict"], vocab=e.get("_vocab_in") or {})
        e["hw"] = hw; e["evo"].hw = hw
        def lobbify(word, definition):
            if word in e["lobby"].agents: return False
            item = {"word": word, "definition": definition, "source": "homework"}
            e["evo"]._apply(item); e["evo"].learned.append(item); return True
        hw.lobbify = lobbify
    for item in (learned or []): e["evo"]._apply(item, record=False); e["evo"].learned.append(item)
    return e

class Dictionary:
    """The imported dictionary: WordNet's definitions only (no WordNet relations).
    5,000 words ordered from most general (semantic primes and grammar terms) outward.
    ECHO reads it; he does all the relating himself."""
    def __init__(self, data):
        self.order = data["order"]; self.entries = data["entries"]; self.primes = set(data.get("primes", []))
        self.rank = {w: i for i, w in enumerate(self.order)}
        self._uses = None
    def __contains__(self, w): return w in self.entries
    def lookup(self, word):
        return self.entries.get(word) or self.entries.get(word.lower())
    def definitions(self, word, pos=None):
        e = self.lookup(word) or {"senses": {}}
        return [(p, d) for p, ds in e["senses"].items() if pos in (None, p) for d in ds]
    def level(self, word):
        e = self.lookup(word); return None if e is None else e["level"]
    def uses(self, word):
        """Filter: every word whose definitions use this word (as a whole word)."""
        if self._uses is None:
            import re as _r, collections as _c
            idx = _c.defaultdict(set)
            for w, e in self.entries.items():
                for ds in e["senses"].values():
                    for d in ds:
                        for t in set(_r.findall(r"[a-z]+", d.lower())): idx[t].add(w)
            self._uses = idx
        return sorted(self._uses.get(word.lower(), ()), key=lambda w: self.rank.get(w, 10**9))
    def next_general(self, known, n=10):
        """The most general words not yet known: the acquisition order."""
        return [w for w in self.order if w not in known][:n]

class Homework:
    """Vocabulary Homework (A-ACQ). One step = one phase; seven phases per word:
    READ → SLOTS → LATERAL → VERTICAL → TRANSCRIBE → FILTER → PRESENTIATE.
    Acquisition invariant: words are taken from the dictionary most-general-first."""
    PHASES = ["READ", "SLOTS", "LATERAL", "VERTICAL", "ANALOGICAL", "TRANSCRIBE", "FILTER", "PRESENTIATE"]
    BOUND = set("that which who whom whose where when of to in for with by from on at into as about through between without".split())
    PREPS = set("of in with by from on at into as about through between without".split())
    ARTS = {"a", "an", "the"}
    SKIP = set("usually especially often typically mainly any some its their his her one such very more most less all each every "
               "also not no been is are was were be having has have can may might must".split())
    def __init__(self, D, vocab=None):
        self.D = D; self.vocab = vocab or {}; self.presences = {}
        for w, e in self.vocab.items():
            for v in e.get("into", []): self.presences.setdefault(v, []).append(w)
        self.cur = None; self.phase = -1; self.steps = 0
    # ---------- reading helpers
    def pos_of(self, w):
        e = self.D.lookup(w); return set(e["senses"]) if e else set()
    PLACEHOLDERS = {"something", "someone", "somebody", "anything", "thing", "person", "people"}
    def is_noun(self, w): return w in self.PLACEHOLDERS or "noun" in self.pos_of(w)
    PARTICIPLES = {"done", "made", "said", "given", "taken", "known", "seen", "used", "held", "found", "built", "kept", "set", "put"}
    MODALS = {"can", "may", "must", "will", "would", "could", "should", "to"}
    def is_verb(self, w): return "verb" in self.pos_of(w) or w in self.PARTICIPLES
    def lemma(self, t):
        if t in self.D: return t
        for suf, add in (("ies", "y"), ("es", ""), ("s", ""), ("ing", ""), ("ing", "e"), ("ed", ""), ("ed", "e"), ("d", "")):
            if t.endswith(suf) and t[:-len(suf)] + add in self.D: return t[:-len(suf)] + add
        return t
    def art(self, w, the=False):
        if the: return "the " + w.capitalize()
        vowel_sound = w[0] in "aeiou" and not w.startswith(("uni", "use", "usu", "uti", "eu", "one", "ewe")) or w.startswith(("hour", "honest", "honor", "heir"))
        return ("an " if vowel_sound else "a ") + w.capitalize()
    def choose_sense(self, w):
        """Lesk-style: the definition sharing most words with what he already knows (first sense breaks ties)."""
        defs = self.D.definitions(w)
        known = set(self.vocab) | set(x for e in self.vocab.values() for x in e.get("main", []))
        best, score = None, -1
        counts = (self.D.lookup(w) or {}).get("counts", {}); top = max(counts.values()) if counts else 1
        for i, (p, d) in enumerate(defs):
            s = len(set(self.words(d)) & known) * 2 - i * 0.3 + 3 * counts.get(p, 0) / top
            if s > score: best, score = (p, d, i), s
        return best
    def words(self, d):
        import re as _r
        return [self.lemma(t) for t in _r.findall(r"[a-z]+", d.lower())]
    # ---------- the slot audit (genus, relation, objects, recipient, connectors)
    def slots(self, pos, d):
        import re as _r
        raw = _r.findall(r"[a-z]+|[,;()]", _r.sub(r"\([^)]*\)", " ", d.lower()))
        toks = [self.lemma(t) if t.isalpha() else t for t in raw]
        out = {"genus": None, "alts": [], "the": False, "relation": None, "objects": [], "recipient": None, "connectors": []}
        i, n = 0, len(toks)
        if pos == "verb":
            while i < n and (toks[i] in self.SKIP or not toks[i].isalpha()): i += 1
            if i < n: out["genus"] = toks[i]; i += 1
            out["relation"] = out["genus"]
            if i + 1 < n and toks[i] == "to" and toks[i + 1].isalpha() and toks[i + 1] not in self.ARTS:
                out["relation"] = toks[i + 1]; i += 2
        else:
            head = None
            while i < n and toks[i] not in self.BOUND and toks[i] not in ",;(":
                t = toks[i]
                if t == "the": out["the"] = True
                if t in ("or", "and") and head: out["alts"].append(head); head = None
                elif t.isalpha() and t not in self.ARTS and t not in self.SKIP and self.is_noun(t): head = t
                i += 1
            if out["alts"] and head: out["genus"] = out["alts"].pop(0); out["alts"].append(head)
            else: out["genus"] = head or (out["alts"].pop(0) if out["alts"] else None)
            if i < n and toks[i] in ("that", "which", "who"):
                i += 1; win = [j for j in range(i, min(n, i + 7)) if toks[j].isalpha() and toks[j] not in self.SKIP
                               and (self.is_verb(toks[j]) or (j > 0 and toks[j - 1] in self.MODALS and not self.is_noun(toks[j])))]
                pure = [j for j in win if not self.is_noun(toks[j])]
                j = (pure or win or [None])[0]
                if j is not None: out["relation"] = toks[j]; i = j + 1
            elif i < n and toks[i].isalpha() and (toks[i] in self.PARTICIPLES or (raw[i].endswith(("ed", "en")) if i < len(raw) else False)):
                out["relation"] = toks[i]; i += 1
        while i < n:
            t = toks[i]
            if t in ("that", "which", "who") and not out["relation"] and pos != "verb":
                win = [j for j in range(i + 1, min(n, i + 8)) if toks[j].isalpha() and toks[j] not in self.SKIP
                       and (self.is_verb(toks[j]) or (toks[j - 1] in self.MODALS and not self.is_noun(toks[j])))]
                pure = [j for j in win if not self.is_noun(toks[j])]
                j = (pure or win or [None])[0]
                if j is not None: out["relation"] = toks[j]; i = j + 1; continue
            if t in ("to", "for") and i + 1 < n and toks[i + 1] in self.ARTS | {"somebody", "someone", "something"} | set(w for w in [toks[i+1]] if self.is_noun(w) and not self.is_verb(w)):
                j = i + 1
                while j < n and toks[j] in self.ARTS | self.SKIP: j += 1
                if j < n and toks[j].isalpha() and self.is_noun(toks[j]) and toks[j] not in ("or", "and"): out["recipient"] = toks[j]; i = j + 1; continue
            if t in self.PREPS and i + 1 < n:
                j = i + 1
                while j < n and (toks[j] in self.ARTS or toks[j] in self.SKIP): j += 1
                if j < n and toks[j].isalpha() and self.is_noun(toks[j]):
                    out["connectors"].append((t, toks[j])); i = j + 1; continue
            if t.isalpha() and t not in self.BOUND and t not in self.ARTS and t not in self.SKIP and t not in ("or", "and") \
                    and self.is_noun(t) and t != out["genus"] and len(out["objects"]) < 4 and t not in out["objects"]:
                if out["relation"] or pos == "verb": out["objects"].append(t)
            i += 1
        return out
    def noun(self, x, the=False):
        return x.capitalize() if x in self.PLACEHOLDERS - {"thing", "person"} else self.art(x, the)
    def lateral(self, w, s, pos="noun"):
        left = w.capitalize() + " = "
        if s["genus"]:
            g = s["genus"].capitalize() if pos == "verb" else self.noun(s["genus"], s["the"])
            left += " / ".join([g] + [a.capitalize() for a in s.get("alts", [])])
        rel = s["relation"] if s["relation"] and s["relation"] != s["genus"] else None
        strand = left + (" :- " + rel.capitalize() if rel else "")
        if s["objects"]: strand += (" :-" if not rel and pos != "verb" else "") + " - " + " / ".join(self.noun(o) for o in s["objects"])
        for p, x in s["connectors"]: strand += f" ({p} {x.capitalize()})"
        if s["recipient"]: strand += " → " + s["recipient"].capitalize()
        return strand
    def vertical(self, w, pos, depth=6, first=None):
        chain, seen, cur, ctx = [w], {w}, w, set(self.words(first or ""))
        for _ in range(depth):
            if cur in self.D.primes: break
            defs = [d for p, d in self.D.definitions(cur, pos)] or [d for p, d in self.D.definitions(cur)]
            if not defs: break
            d = max(enumerate(defs), key=lambda x: (len(set(self.words(x[1])) & ctx), -x[0]))[1] if ctx else defs[0]
            g = self.slots(pos, d)["genus"]; ctx = set(self.words(d))
            if not g or g in seen: break
            chain.append(g); seen.add(g); cur = g
            if (self.D.level(g) or 9) == 0: break
        return chain
    def term(self, w, s):
        rel = s.get("relation") if s.get("relation") and s.get("relation") != s.get("genus") else None
        obj = (s.get("objects") or [None])[0]
        right = f"({rel}-{obj})" if rel and obj else f"({rel})" if rel else f"({obj})" if obj else "(?)"
        return f"({w}<{s['genus']})" if s.get("genus") else f"({w})", right
    def analogize(self, c):
        """This:That::These:Those. Pair the word with learned siblings that share its genus (or its relation):
        |{(verb<word):(denote-action)::(noun<word):(refer-place)}|"""
        s, w = c["slots"], c["word"]
        if c.get("pos") == "prime" or not (s.get("genus") or s.get("relation")):
            return "|{(" + w + "):(prime)::(?):(?)}|" if c.get("pos") == "prime" else "|{(?):(?)::(?):(?)}|", []
        a1, a2 = self.term(w, s)
        sibs = [x for x, e in self.vocab.items() if x != w and s.get("genus") and e.get("genus") == s.get("genus")][:3]
        if not sibs and s.get("relation"):
            sibs = [x for x, e in self.vocab.items() if x != w and e.get("relation") == s.get("relation")][:3]
        if not sibs: return "|{" + a1 + ":" + a2 + "::(?):(?)}|", []
        parts, back = [], []
        for x in sibs:
            b1, b2 = self.term(x, self.vocab[x])
            parts.append("|{" + a1 + ":" + a2 + "::" + b1 + ":" + b2 + "}|"); back.append((x, "|{" + b1 + ":" + b2 + "::" + a1 + ":" + a2 + "}|"))
        return " :: ".join(parts), back
    def analog(self, chain):
        pairs = [f"({a}<{b})" for a, b in zip(chain, chain[1:])]
        if not pairs: return "|{}|"
        groups = [pairs[i:i + 4] for i in range(0, len(pairs), 4)]
        def fmt(g):
            g = g + ["(?)"] * (4 - len(g)) if len(g) < 4 else g
            return "|{" + g[0] + ":" + g[1] + "::" + g[2] + ":" + g[3] + "}|"
        return " :: ".join(fmt(g) for g in groups)
    # ---------- one step = one phase
    def next_word(self):
        for w in self.D.order:
            if w not in self.vocab: return w
        return None
    def step(self):
        self.steps += 1
        if self.cur is None or self.phase >= len(self.PHASES) - 1:
            w = self.next_word()
            if not w: return {"done": True}
            self.cur = {"word": w, "level": self.D.level(w)}; self.phase = -1
        self.phase += 1; ph = self.PHASES[self.phase]; c = self.cur
        prime = c["word"] in self.D.primes
        if ph == "READ":
            if prime:   # primes are axioms: nothing to audit, so SLOTS, LATERAL and VERTICAL are settled in this one step
                c.update(pos="prime", definition="a semantic prime: undefined, the base where strands end", sense=0, senses=0,
                         slots={"genus": None, "alts": [], "the": False, "relation": None, "objects": [], "recipient": None, "connectors": []},
                         lateral=f"{c['word'].capitalize()} = (prime)", chain=[c["word"]], analog="|{(" + c["word"] + "):(prime)::(?):(?)}|")
                self.phase = 4
            else:
                p, d, i = self.choose_sense(c["word"]) or ("noun", "", 0)
                c.update(pos=p, definition=d, sense=i + 1, senses=len(self.D.definitions(c["word"])))
        elif ph == "SLOTS":
            c["slots"] = {"genus": None, "alts": [], "the": False, "relation": None, "objects": [], "recipient": None, "connectors": []} if prime \
                else self.slots(c["pos"], c["definition"])
        elif ph == "LATERAL":
            c["lateral"] = f"{c['word'].capitalize()} = (prime)" if prime else self.lateral(c["word"], c["slots"], c["pos"])
        elif ph == "VERTICAL":
            c["chain"] = [c["word"]] if prime else self.vertical(c["word"], c["pos"], first=c["definition"])
            c["analog"] = "|{(" + c["word"] + "):(prime)::(?):(?)}|" if prime else self.analog(c["chain"])
        elif ph == "ANALOGICAL":
            c["analogy"], c["siblings"] = self.analogize(c)
        elif ph == "TRANSCRIBE":
            s = c["slots"]
            main = [x for x in [s["genus"], s["relation"]] + s["objects"] + [x for _, x in s["connectors"]] + [s["recipient"]] if x]
            c["main"] = list(dict.fromkeys(main))
            s = c["slots"]
            self.vocab[c["word"]] = {"pos": c["pos"], "definition": c["definition"], "lateral": c["lateral"], "chain": c["chain"],
                                     "classical": c["analog"], "analogy": c.get("analogy", ""), "genus": s.get("genus"), "relation": s.get("relation"),
                                     "objects": s.get("objects", []), "main": c["main"], "level": c["level"], "into": [], "occurrences": 0, "step": self.steps}
            for sib, term in c.get("siblings", []):   # the analogy runs both ways: the sibling gains it too
                e = self.vocab.get(sib)
                if e is not None and c["word"] not in e.get("analogy", "") and e.get("analogy", "").count("|{") < 6:
                    e["analogy"] = (e.get("analogy") + " :: " if e.get("analogy") and "(?)" not in e["analogy"] else "") + term
            lb = getattr(self, "lobbify", None)
            c["lobbied"] = bool(lb and lb(c["word"], c["definition"]))
        elif ph == "FILTER":
            c["uses"] = [v for v in self.D.uses(c["word"]) if v != c["word"]]
        elif ph == "PRESENTIATE":
            # § the word's classical, lateral and analogical strands under every occurrence of it inside other words' definitions
            into, occ = c["uses"][:50], 0
            for v in into:
                for p, d in self.D.definitions(v):
                    occ += sum(1 for t in self.words(d) if t == c["word"])
                self.presences.setdefault(v, []).append(c["word"])
            self.vocab[c["word"]]["into"] = into; self.vocab[c["word"]]["occurrences"] = occ; c["into"] = into; c["occurrences"] = occ
        return {"phase": ph, "index": self.phase, "phases": self.PHASES, "task": c, "learned": len(self.vocab),
                "presences": len(self.presences), "steps": self.steps}
