"""E12: record ECHO's Canvas Recess on the KSM, for the replay page."""
import json, re, sys
from nltk.corpus import wordnet as wn
from echo.kernel import K
from echo.matrix.registry import Registry
from echo.canvas.ks_recess import KSRecess
from echo.language import senses as S
from echo.language.parser import parse, Parser
from echo.language.lexicon import Lexicon
from echo.language.audit import Auditor
from echo.language.realize import english, emel
from echo.language.english_parse import EnglishParser
from echo.language.ast import to_dict

reg = Registry(); km = K.AlgorithmMatrix(); frontier, seen = list(reg.canonical), set()
while frontier and len(seen) < 900:
    w = frontier.pop(0)
    if w in seen: continue
    ss = wn.synsets(w.replace(" ", "_"), "n")
    if not ss: continue
    seen.add(w); d = ss[0].definition(); km.index_dictionary_entry(w, d, pos="noun", category="lobby")
    for tok in d.replace(",", " ").replace(";", " ").split():
        t = tok.lower().strip("()'\"")
        if t.isalpha() and len(t) > 3 and t not in seen and wn.synsets(t, "n"): frontier.append(t)
lobby = K.Lobby(km); lobby.populate(); lobby.run_orientation(); lobby.matrix = km
gscore = {w: g for w, g in (lobby.compute_generality_scores() or {}).items() if w in lobby.agents and " " not in w}

def relate(a, b, top=2):
    """Sense-pinned is-a, using only each word's two most common senses (WordNet orders senses by use)."""
    best = None
    for sa in wn.synsets(a, "n")[:top]:
        for sb in wn.synsets(b, "n")[:top]:
            for x, y, typ in ((sa, sb, "is_a"), (sb, sa, "includes")):
                d = S.ancestors(x.name()).get(y.name())
                if d and (best is None or d < best[1]): best = (typ, d)
    return best

lx = Lexicon(reg, {}); au = Auditor(reg, {}); ep = EnglishParser(lambda: Parser([], lx))
spoken = set()
def speak(u, kind, v):
    """Only sentences that parse, pass the truth audit, and parse back to the same tree are spoken.
    Words are spoken in their base form (activities -> activity), and nothing already said is repeated."""
    if not re.fullmatch(r"[a-z]+", u) or not re.fullmatch(r"[a-z]+", v): return None
    from lemminflect import getLemma
    u, v = getLemma(u, upos="NOUN")[0], getLemma(v, upos="NOUN")[0]
    if u.endswith("ing") or v.endswith("ing"): return None    # gerunds are mass nouns: his grammar has no article-free rule yet
    if (u, kind, v) in spoken or u == v: return None
    try: n = parse(f"{u} {kind} {v}", lx)
    except Exception: return None
    if au.truth(n)[0] != "SUPPORTED": return None
    text = english(n)
    if to_dict(ep.sentence(text)) != to_dict(n): return None
    spoken.add((u, kind, v))
    return {"english": text, "emel": emel(n), "audits": "lexical, type, semantic, grammar: PASS"}

def define(w):
    ss = wn.synsets(w, "n"); return ss[0].definition() if ss else ""

canon = [w for w in reg.canonical if w in gscore]
start = max(canon, key=lambda w: (gscore[w], w))
rec = KSRecess(K, lobby, gscore, relate, speak, define)
log = rec.run(sessions=int(sys.argv[1]) if len(sys.argv) > 1 else 6, turns=20, start=start)
json.dump({"start": start, "lobby_words": len(lobby.agents), "log": log}, open("experiments/e12_recess_log.json", "w"))
arms = [e["arm"] for e in log if e["arm"] not in ("START", "CHECKPOINT")]
from collections import Counter
print("start:", start, "| turns:", len(arms), "| planes:", len(rec.planes), "| sets:", len({p['group'] for p in rec.planes.values() if p['group']}),
      "| contained:", sum(1 for p in rec.planes.values() if p['parent']), "| spoken:", sum(len(e['say']) for e in log))
for e in log:
    if e["arm"] == "CHECKPOINT": print(f"  session {e['session']}: {e['reason']} | history {e['history']}")
print("per session arms:", [Counter(e['arm'] for e in log if e['session'] == s and e['arm'] in ('INTRODUCE','ALIGN','CONTAIN','MANIFOLD')) for s in range(1, 7)])
print("sample:", [(e['turn'], e['arm'], e['ok'], e['reason'][:90]) for e in log if e['arm'] in ('ALIGN', 'CONTAIN', 'MANIFOLD')][:10])
print("spoken:", [s['english'] for e in log for s in e['say']][:12])
