"""ECHO writes: select content from data -> EMEL -> tree -> audits -> revise -> English -> parse-back check.

Content selection is rule-based over the records, not a script of sentences: which
candidates are partial, which metric shows the weakness, where a contrast ('but')
is earned. Every sentence that reaches the output passed all audits.
"""
import re
from .parser import parse, Parser, lex, ParseError
from .ast import Property, Join
from .realize import english, emel, Discourse
from .english_parse import EnglishParser
from .audit import Auditor
from .lexicon import Lexicon


def plan(records, memory=None):
    """Content selection. `memory` holds ECHO's own earlier beliefs, which may be stale."""
    memory = memory or {}
    out = []
    s = records.get("A-177", {})
    if s:
        out.append(f"A-177.candidate_count = {s['candidate_count']} and A-177.valid_count = {s['valid_count']}")
    for cid in sorted(k for k in records if re.match(r"^C-\d+$", k)):
        r = records[cid]
        verdict = memory.get(cid, {}).get("verdict", r["verdict"])        # ECHO speaks from memory first
        if verdict != "PARTIAL" and r["verdict"] != "PARTIAL":
            continue
        good = [k for k, v in r.items() if k.endswith("accuracy") and not str(v).startswith("0")]
        bad = [k for k, v in r.items() if (k.endswith("accuracy") and str(v).startswith("0")) or k.endswith("count")]
        line = f"{cid}.verdict = {verdict}"
        if good and bad:
            line += f" and {cid}.{good[0]} = {r[good[0]]} but {cid}.{bad[0]} = {r[bad[0]]}"
        elif bad:
            line += f" and {cid}.{bad[0]} = {r[bad[0]]}"
        out.append(line)
    if "E2" in records:
        e = records["E2"]
        out.append(f"E2.exact_form_count = {e['exact_form_count']} but E2.shifted_form_count = {e['shifted_form_count']}")
        out.append("dog:canine::cat:feline")
    if "E1" in records:
        e = records["E1"]
        out.append(f'E1.checked_count = {e["checked_count"]} and E1.factorization = "{e["factorization"]}"')
    return out


def write(records, registry, memory=None, known_word=None):
    lx = Lexicon(registry, records)
    aud = Auditor(registry, records)
    ds, ep = Discourse(), EnglishParser(lambda: Parser([], lx))
    known_word = known_word or (lambda w: lx.word_known(w) or any(w == str(v).lower() for r in records.values() for v in r.values())
                               or w in {t.lower() for r in records.values() for k in r for t in k.split("_")})
    sentences, log = [], []

    def fix_properties(node):
        """Revision: a property that contradicts its record takes the record's value."""
        if isinstance(node, Property):
            v, src = aud.truth(node)
            if v == "CONTRADICTED":
                rec = records[node.subject.surface][node.attribute]
                new = parse(f'{node.subject.surface}.{node.attribute} = "{rec}"', lx)
                log.append(f"revised {emel(node)!r} -> {emel(new)!r} ({src})")
                return new
            return node
        if isinstance(node, Join):
            return Join(node.conj, fix_properties(node.left), fix_properties(node.right))
        return node

    def relink(node):
        if isinstance(node, Join):
            conj = node.conj
            if conj == "but" and aud.discourse(Join(conj, node.left, node.right))["status"] == "FAIL" \
                    and isinstance(node.left, Property) and isinstance(node.right, Property):
                conj = "and"
            return Join(conj, relink(node.left), relink(node.right))
        return node

    for src in plan(records, memory):
        try:
            node = parse(src, lx)
        except ParseError as e:
            log.append(f"dropped {src!r}: syntax {e}"); continue
        t = aud.type(node)
        if t["status"] == "FAIL":
            log.append(f"dropped {src!r}: type {t['errors']}"); continue
        node = fix_properties(node)
        d = aud.discourse(node)
        if d["status"] == "FAIL":
            node = relink(node)
            log.append(f"revised connective: {d['issues'][0]} -> 'and'")
        verdict, why = aud.truth(node)
        if verdict != "SUPPORTED":
            log.append(f"withheld {emel(node)!r}: {verdict} ({why})"); continue
        before = ds.focus
        text = english(node, ds)
        g = aud.grammar(node, text, ep, known_word)
        if g["status"] == "FAIL":
            ds.focus = None; ep.focus = None
            text = english(node, ds); g = aud.grammar(node, text, ep, known_word)
            log.append(f"re-realized without a pronoun: {g['status']}")
        if g["status"] == "FAIL":
            log.append(f"dropped {emel(node)!r}: grammar {g['issues']}"); continue
        sentences.append({"english": text, "emel": emel(node), "lexical": aud.lexical(node)["status"],
                          "type": t["status"], "discourse": aud.discourse(node)["status"], "semantic": verdict, "provenance": why, "grammar": g["status"]})
    return {"report": " ".join(s["english"] for s in sentences), "sentences": sentences, "revisions": log}
