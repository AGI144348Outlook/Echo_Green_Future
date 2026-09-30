"""ECHO as a Canvas actor.

ECHO uses the same operation API as the person: it returns operations and the
host applies them through one reducer, tagged actor 'echo'. Operations the
person asked for in the I/O dock are tagged actor 'user'. Before anything is
returned, ECHO runs IDENTIFY -> VALIDATE -> OPEN on it.

Snapshot the host passes in:
  {"manifestations": [{"id", "word", "canonicalId", "x", "y", "actor"}],
   "relations": [{"from", "to", "type"}], "selection": [id, ...]}
"""
import re
import time

from ..operators.lhea import equilibrium, profile
from ..operators.invariant import probe

STOP = {"the", "and", "for", "with", "that", "this", "from", "have", "what", "which", "about",
        "into", "your", "you", "are", "was", "were", "can", "does", "how", "why", "when", "who",
        "there", "their", "they", "them", "then", "than", "just", "also", "some", "like", "will"}

DASH = "\u2014"

HELP = (
    "resolve <word> \u00b7 presentiate <word>[, word] \u00b7 chain <word> \u00b7 hypernyms of <word> \u00b7 "
    "hyponyms of <word> \u00b7 relate <a> <b> [type] \u00b7 select <word> \u00b7 remove <word> \u00b7 "
    "selection \u00b7 equilibrium <a> <b> \u00b7 invariant <word> \u00b7 teach <word> is-a <word>[: definition] \u00b7 "
    "cycle [text] \u00b7 identify \u00b7 words \u00b7 mcw <message>"
)


def article(word, cap=False):
    a = "an" if word[:1].lower() in "aeiou" else "a"
    return a.capitalize() if cap else a


class EchoActor:
    def __init__(self, registry, runtime):
        self.registry = registry
        self.runtime = runtime
        self.n = 0

    # -- IDENTIFY -> VALIDATE -> OPEN -------------------------------------
    def identify(self):
        return {"id": "echo", "role": "governor", "algorithm": "A-000", "glyph": "\u05e8"}

    def validate(self, op, snap):
        if op["actor"] != "echo":
            return True
        target = op.get("target")
        if op["op"] in ("MOVE", "REMOVE") and target:
            man = self._by_id(snap, target)
            if man and man.get("actor") != "echo":
                return False
        return True

    def open(self, ops, snap):
        return [op for op in ops if self.validate(op, snap)]

    # -- helpers ----------------------------------------------------------
    def new_id(self):
        self.n += 1
        return f"man:e{int(time.time() * 1000):x}{self.n}"

    @staticmethod
    def _by_id(snap, mid):
        for m in snap.get("manifestations", []):
            if m["id"] == mid:
                return m
        return None

    @staticmethod
    def _by_word(snap, word):
        return [m for m in snap.get("manifestations", []) if m.get("word") == word]

    @staticmethod
    def _related(snap, a, b):
        return any(r["from"] == a and r["to"] == b for r in snap.get("relations", []))

    @staticmethod
    def op(actor, name, target=None, provenance="echo-autonomous", **args):
        if "from_" in args:
            args["from"] = args.pop("from_")
        return {"actor": actor, "op": name, "target": target, "args": args, "provenance": provenance}

    @staticmethod
    def out(kind, text, refs=None, **extra):
        return {"actor": "echo", "kind": kind, "text": text, "refs": refs or [], **extra}

    def _present_or_find(self, snap, word, x, y, ops, actor="echo", provenance="echo-autonomous"):
        """Return a manifestation id for word, creating a Presentiation only if none exists."""
        existing = self._by_word(snap, word)
        if existing:
            return existing[0]["id"]
        for o in ops:  # already queued in this batch
            if o["op"] == "PRESENTIATE" and o["args"].get("word") == word:
                return o["args"]["manifestationId"]
        mid = self.new_id()
        res = self.registry.resolve(word)
        ops.append(self.op(actor, "PRESENTIATE", provenance=provenance, manifestationId=mid,
                           canonicalId=res["id"], word=word, renderer="circle", x=x, y=y))
        return mid

    # -- autonomous reaction ---------------------------------------------
    def on_presentiate(self, snap, man_id):
        man = self._by_id(snap, man_id)
        if not man:
            return {"outputs": [], "ops": []}
        word = man["word"]
        res = self.registry.resolve(word)
        outputs, ops = [], []
        if res["source"] == "gap":
            outputs.append(self.out("text",
                f"'{word}' is not yet indexed. LHEA: {res['lhea'] or DASH} ({res['glyphs']} {res['gematria']}). "
                f"Teach me with: teach {word} is-a <hypernym>", refs=[word]))
            return {"outputs": outputs, "ops": ops}
        parents = res["hypernyms"]
        if parents:
            h = parents[0]
            outputs.append(self.out("text",
                f"{article(word, True)} {word} is {article(h)} {h}.\nLHEA: {res['lhea']}\n"
                f"Gematria: {res['gematria']}  {res['glyphs']}", refs=[word, h]))
            hid = self._present_or_find(snap, h, man["x"], man["y"] - 110, ops)
            if not self._related(snap, man_id, hid):
                ops.append(self.op("echo", "RELATE", from_=man_id, to=hid, type="is-a", label="is-a"))
        else:
            outputs.append(self.out("text", f"{article(word, True)} {word} is the root: {res['def']}", refs=[word]))
        for other in snap.get("manifestations", []):
            if other["id"] == man_id or other["word"] == word:
                continue
            eq = equilibrium(word, other["word"])
            if eq and eq["value"] >= 200:
                outputs.append(self.out("status",
                    f"Equilibrium: '{word}' \u2194 '{other['word']}' at {eq['glyph']} {eq['letter']} "
                    f"({eq['operation']}, {eq['value']})", refs=[word, other["word"]]))
                break
        return {"outputs": outputs, "ops": self.open(ops, snap)}

    # -- commands from the I/O dock ------------------------------------------
    def handle(self, text, mode, snap):
        t = (text or "").strip()
        low = t.lower()
        result = {"outputs": [], "ops": []}
        o, ops = result["outputs"], result["ops"]
        sel = [self._by_id(snap, i) for i in snap.get("selection", [])]
        sel = [m for m in sel if m]

        def arg(prefixes):
            for p in prefixes:
                if low.startswith(p):
                    return t[len(p):].strip()
            return None

        if low in ("help", "?"):
            o.append(self.out("status", HELP)); return result

        if low == "identify":
            info = self.runtime.identify()
            o.append(self.out("matrix", "IDENTIFY", columns=["field", "value"],
                              rows=[[k, str(v)] for k, v in info.items()])); return result

        if low in ("words", "registry"):
            words = self.registry.all_words()
            o.append(self.out("text", f"{len(words)} residents: " + ", ".join(words), refs=words)); return result

        w = arg(["resolve ", "what is ", "what's "])
        if w is not None:
            w = re.sub(r"^(a|an|the)\s+", "", w.rstrip("?. "), flags=re.I)
            r = self.registry.resolve(w)
            rows = [["canonicalId", r["id"]], ["source", r["source"]], ["definition", r["def"]],
                    ["LHEA", r["lhea"] or "\u2014"], ["gematria", f"{r['gematria']}  {r['glyphs']}"],
                    ["hypernyms", ", ".join(r["hypernyms"]) or "\u2014"],
                    ["hyponyms", ", ".join(r["hyponyms"]) or "\u2014"]]
            o.append(self.out("matrix", f"\u03c1({r['word']})", columns=["field", "value"], rows=rows,
                              refs=[r["word"]] + r["hypernyms"] + r["hyponyms"])); return result

        w = arg(["presentiate ", "show ", "place "])
        if w is not None:
            words = [x.strip() for x in w.split(",") if x.strip()]
            for word in words:
                word = self.registry.key(word)
                # no x/y: the host places it in view and avoids overlaps
                ops.append(self.op("user", "PRESENTIATE", provenance="io-command", manifestationId=self.new_id(),
                                   canonicalId="word:" + word, word=word, renderer="circle"))
            if not words:
                o.append(self.out("error", "Name a word: presentiate dog"))
            return result

        w = arg(["chain "])
        if w is not None:
            word = self.registry.key(w)
            if not self.registry.has(word):
                o.append(self.out("error", f"'{word}' is a gap; no chain to draw.", refs=[word])); return result
            path = [word] + self.registry.chain(word)
            base = self._by_word(snap, word)
            x0, y0 = (base[0]["x"], base[0]["y"]) if base else (200, 560)
            prev = None
            for i, node in enumerate(path):
                mid = self._present_or_find(snap, node, x0 + (i % 2) * 40, y0 - i * 95, ops,
                                            provenance="user-request")
                if prev and not self._related(snap, prev, mid):
                    ops.append(self.op("echo", "RELATE", provenance="user-request",
                                       from_=prev, to=mid, type="is-a", label="is-a"))
                prev = mid
            o.append(self.out("text", " \u2192 ".join(path), refs=path))
            result["ops"] = self.open(ops, snap); return result

        w = arg(["hypernyms of ", "hypernym of ", "generalize "])
        if w is not None:
            word = self.registry.key(w)
            path = self.registry.chain(word)
            o.append(self.out("text", f"{word} \u2192 " + (" \u2192 ".join(path) if path else "(no hypernyms: gap or root)"),
                              refs=[word] + path)); return result

        w = arg(["hyponyms of ", "hyponym of ", "specify "])
        if w is not None:
            word = self.registry.key(w)
            hs = self.registry.hyponyms(word)
            o.append(self.out("text", f"{word} \u2192 " + (", ".join(hs) if hs else "(no hyponyms indexed)"),
                              refs=[word] + hs)); return result

        w = arg(["relate "])
        if w is not None:
            parts = w.split()
            if len(parts) < 2:
                o.append(self.out("error", "Usage: relate <a> <b> [type]")); return result
            a, b = self.registry.key(parts[0]), self.registry.key(parts[1])
            rtype = parts[2] if len(parts) > 2 else "is-a"
            ma, mb = self._by_word(snap, a), self._by_word(snap, b)
            if not ma or not mb:
                missing = [x for x, m in ((a, ma), (b, mb)) if not m]
                o.append(self.out("error", "Not on the Canvas: " + ", ".join(missing), refs=missing)); return result
            ops.append(self.op("user", "RELATE", provenance="io-command", from_=ma[0]["id"], to=mb[0]["id"],
                               type=rtype, label=rtype)); return result

        w = arg(["remove "])
        if w is not None:
            word = self.registry.key(w)
            found = self._by_word(snap, word)
            if not found:
                o.append(self.out("error", f"'{word}' is not on the Canvas.")); return result
            for m in found:
                ops.append(self.op("user", "REMOVE", target=m["id"], provenance="io-command"))
            o.append(self.out("status", f"Removed {len(found)} Presentiation(s) of '{word}'. The canonical resident is unchanged."))
            return result

        w = arg(["select "])
        if w is not None:
            word = self.registry.key(w)
            found = self._by_word(snap, word)
            if not found:
                o.append(self.out("error", f"'{word}' is not on the Canvas.")); return result
            ops.append(self.op("user", "SELECT", provenance="io-command", manifestationId=found[0]["id"], exclusive=True))
            return result

        if low in ("selection", "common", "what is selected", "common hypernym"):
            if not sel:
                o.append(self.out("status", "Nothing is selected. Tap circles on the Canvas first.")); return result
            words = [m["word"] for m in sel]
            if len(sel) == 1:
                o.append(self.out("text", f"Selected: {words[0]}", refs=words)); return result
            common = self.registry.common_hypernyms(words)
            rows = [[h, str(sum(self.registry.ancestors(wd).get(h, 0) for wd in words))] for h in common[:8]]
            o.append(self.out("matrix", f"Common hypernyms of {', '.join(words)}",
                              columns=["hypernym", "summed depth"], rows=rows or [["\u2014", "none shared"]],
                              refs=words + common[:8]))
            if common:
                h = common[0]
                cx = sum(m["x"] for m in sel) / len(sel)
                cy = min(m["y"] for m in sel) - 120
                hid = self._present_or_find(snap, h, cx, cy, ops, provenance="selection-query")
                for m in sel:
                    if not self._related(snap, m["id"], hid):
                        ops.append(self.op("echo", "RELATE", provenance="selection-query",
                                           from_=m["id"], to=hid, type="is-a", label="is-a"))
                result["ops"] = self.open(ops, snap)
            return result

        w = arg(["equilibrium "])
        if w is not None:
            parts = [p for p in re.split(r"[\s,]+", w) if p]
            if len(parts) < 2:
                o.append(self.out("error", "Usage: equilibrium <a> <b>")); return result
            eq = equilibrium(parts[0], parts[1])
            if not eq:
                o.append(self.out("text", f"'{parts[0]}' and '{parts[1]}' share no letter operator.", refs=parts[:2]))
            else:
                o.append(self.out("text", f"'{parts[0]}' \u2194 '{parts[1]}' balance at {eq['glyph']} {eq['letter']} "
                                          f"({eq['operation']}, {eq['value']}). Shared: {', '.join(eq['shared'])}",
                                  refs=parts[:2]))
            return result

        w = arg(["invariant ", "rie "])
        if w is not None:
            tr = probe(w.split()[0] if w.split() else w)
            rows = [["sequence", f"{tr['sequence']} \u2192 {tr['inverted']}"],
                    ["gematria preserved", str(tr["gematria_preserved"])],
                    ["strict involution fixed", str(tr["strict_involution_fixed"])],
                    ["letter set fixed", str(tr["letter_set_fixed"])],
                    ["I\u00b2 = x", str(tr["involution_check"])],
                    ["forward", " \u2192 ".join(tr["forward_ops"])],
                    ["reversed", " \u2192 ".join(tr["reversed_ops"])],
                    ["phase (hypothesis)", f"index sum {tr['phase']['index_sum']}, real axis {tr['phase']['on_real_axis']}"]]
            o.append(self.out("matrix", f"A-174 trace: {tr['thing']}", columns=["field", "value"], rows=rows,
                              note=tr["note"], refs=[tr["thing"]]))
            return result

        m = re.match(r"^teach\s+(.+?)\s+(?:is-a|is a|isa)\s+([^:]+?)(?:\s*:\s*(.+))?$", t, re.I)
        if m:
            ok, msg = self.registry.teach(m.group(1), m.group(2), (m.group(3) or "").strip())
            o.append(self.out("status" if ok else "error", msg, refs=[self.registry.key(m.group(1)), self.registry.key(m.group(2))]))
            if ok:
                result["overlay"] = self.registry.export_overlay()
            return result
        if low.startswith("teach"):
            o.append(self.out("error", "Usage: teach <word> is-a <hypernym>[: definition]")); return result

        w = arg(["cycle"])
        if w is not None:
            rows = self.runtime.cycle(w or "the governor indexes its own algorithms")
            o.append(self.out("matrix", "A-000 Governor cycle (kernel run_cycle)", columns=["field", "value"],
                              rows=[[k, str(v)] for k, v in rows.items()]))
            return result

        w = arg(["mcw "])
        if w is not None:
            env = self.runtime.outbox.envelope("note", {"text": w, "selection": [m["word"] for m in sel]}, actor="user")
            result["mcw"] = env
            o.append(self.out("status", f"Queued MCW message {env['id']} in the local outbox."))
            return result

        # free text / query: read what ECHO knows in the message
        tokens = [x.lower() for x in re.findall(r"[A-Za-z][A-Za-z'-]+", t)]
        known = [x for x in dict.fromkeys(tokens) if self.registry.has(x)]
        if mode == "CANVAS" and not known:
            o.append(self.out("error", "Not a Canvas command. " + HELP)); return result
        for word in known[:6]:
            r = self.registry.resolve(word)
            up = f" \u2192 {r['chain'][0]}" if r["chain"] else ""
            o.append(self.out("text", f"'{word}'{up}: {r['def']}  ({r['glyphs']} {r['gematria']})", refs=[word] + r["chain"][:1]))
        gaps = [x for x in dict.fromkeys(tokens) if len(x) > 3 and x not in STOP and not self.registry.has(x)]
        if gaps:
            o.append(self.out("status", "Gaps (not yet indexed): " + ", ".join(gaps[:6])))
        if not known and not gaps:
            o.append(self.out("status", "Try: help"))
        return result
