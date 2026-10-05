import re, json, collections
from nltk.corpus import wordnet as wn
PRIMES = """I you someone something thing people body kind part this same other else one two some all much many little few
good bad big small think know want feel see hear say words true do happen move be there mine live die when time now before after
long short moment where place here above below far near side inside touch not maybe can because if very more like way""".split()
GRAMMAR = "noun verb adjective adverb pronoun preposition conjunction article determiner sentence word phrase clause subject object predicate".split()
FUNCTION = set("""a an the this that these those some any every each all no none both either neither of to in for with by from on at into onto as about through
between among under over after before during without within upon via than and or but nor so yet if because while although though when where whether which who
whom whose what it its it's he she they them their his her him we us our you your i me my is are was were be been being am do does did done has have had having
can could may might must shall should will would not also usually especially etc one ones such other another something someone somebody anything thing""".split())
POSN = {"n": "noun", "v": "verb", "a": "adjective", "s": "adjective", "r": "adverb"}
def lemma(w):
    for p in ("n", "v", "a", "r"):
        m = wn.morphy(w, p)
        if m: return m
    return None
def proper(w):
    ss = wn.synsets(w)
    return bool(ss) and all(s.instance_hypernyms() or s.lemmas()[0].name()[0].isupper() for s in ss)
def content_words(defn):
    out = []
    for t in re.findall(r"[a-z]+", defn.lower()):
        if t in FUNCTION or len(t) < 2: continue
        l = lemma(t)
        if l and "_" not in l and not proper(l): out.append(l)
    return out
level, order, frontier = {}, [], [w for w in dict.fromkeys(PRIMES + GRAMMAR) if wn.synsets(w)]
L = 0
while frontier and len(order) < 5000:
    nxt = []
    for w in frontier:
        if w in level: continue
        level[w] = L; order.append(w)
        for s in wn.synsets(w)[:3]:
            nxt += content_words(s.definition())
    # within a level, most common (more senses) first
    nxt = sorted(set(x for x in nxt if x not in level), key=lambda x: -len(wn.synsets(x)))
    frontier = nxt; L += 1
order = order[:5000]
entries = {}
for w in order:
    senses = collections.defaultdict(list)
    for s in wn.synsets(w):
        p = POSN[s.pos()]
        if len(senses[p]) < 4: senses[p].append(s.definition())
    counts = collections.Counter(POSN[s.pos()] for s in wn.synsets(w))
    entries[w] = {"level": level[w], "senses": dict(sorted(senses.items(), key=lambda kv: -counts[kv[0]])), "counts": dict(counts)}
json.dump({"order": order, "entries": entries, "primes": [w for w in dict.fromkeys(PRIMES) if w in entries]}, open("/tmp/dict.json", "w"))
print(len(order), "words; levels:", collections.Counter(level[w] for w in order))
print(order[:40]); print(order[2000:2015]); print(order[-15:])
import os; print(os.path.getsize("/tmp/dict.json")//1024, "KB")
