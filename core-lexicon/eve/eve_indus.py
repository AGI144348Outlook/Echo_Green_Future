"""
Replay of the Indus decipherment prompts (12 Jan – 5 Feb 2025) inside a coded EVE.
Vigil's answers here are only what the code measures on real inscriptions.

Corpus in hand: CISI digitisation by M. Carlson (github.com/mayig/indus-valley-script-corpus, MIT),
Mohenjo-daro unicorn seals M-1…M-199 (Parpola sign numbers, Mahadevan cross-references).
Graphemes are stored left→right; the script reads right→left, so texts are reversed here.
"""
import json, math, random, re, collections, itertools, sys
import numpy as np
sys.path.insert(0, '.')
from eve_core import EVE, null_model_note

random.seed(144348); np.random.seed(144348)
D = json.load(open('cisi_mayig.json'))
SIGN = D['signs']
ILLEG = 'P000'
texts_all = [list(reversed(a['signs'])) for a in D['arts']]            # reading order
texts = [t for t in texts_all if t]                                     # keep illegible as a gap marker
clean = [[s for s in t if s != ILLEG] for t in texts]
toks = [s for t in clean for s in t]
uni = collections.Counter(toks)
V = len(uni)
desc = lambda p: (SIGN.get(p) or {}).get('desc') or p
short = lambda p: re.sub(r'\s+', ' ', desc(p))[:60]

out = dict(corpus=dict(), replay=[], eve=dict())
def vigil(when, prompt, answer, **data):
    out['replay'].append(dict(when=when, prompt=prompt, answer=answer, data=data))

# ── Corpus facts ─────────────────────────────────────────────────────────────────────────
lens = [len(t) for t in texts]
out['corpus'] = dict(source="CISI digitisation (Carlson, MIT licence), Mohenjo-daro M-1–M-199", texts=len(texts),
    tokens=len(toks), illegible=sum(t.count(ILLEG) for t in texts), sign_types=V,
    hapax=sum(1 for c in uni.values() if c == 1), mean_len=round(sum(lens) / len(lens), 2), max_len=max(lens),
    reference=dict(icit_texts=5644, icit_signs=709, icit_occurrences=19831, mahadevan_signs=419,
                   right_to_left_share="≈87% of texts with known direction", note="Fuls 2022, Corpus of Indus Inscriptions"))

# ── Prompt: can you decipher it? how many combinations? ─────────────────────────────────
combos = {n: len({tuple(t[i:i + n]) for t in clean for i in range(len(t) - n + 1)}) for n in range(1, 8)}
space = {n: f"{709 ** n:.2e}" for n in (2, 3, 5, 7)}
vigil("12 Jan 2025, 21:18", "If there's only 400–600 symbols, how many finite combinations are there? Let's try it.",
      "With 709 signs (Wells/Fuls list) the possible strings grow as 709ⁿ: about 5.0×10⁵ pairs, 3.6×10⁸ triples and "
      "9.0×10¹⁹ seven-sign strings. Brute force over that space is not a method. What can be counted is what actually "
      "occurs. In the 179 seals in hand, these are the distinct sequences of each length:",
      possible=space, observed_distinct=combos)

# ── Lexicon NVE: single signs on the core surface, combinations on the inner walls ──────
top = [(p, c, short(p)) for p, c in uni.most_common(15)]
bigr = collections.Counter((a, b) for t in clean for a, b in zip(t, t[1:]))
walls = {n: collections.Counter(tuple(t[i:i + n]) for t in clean for i in range(len(t) - n + 1)).most_common(5) for n in (2, 3, 4)}
out['lexicon'] = dict(top_signs=top, walls={n: [[list(k), v] for k, v in w] for n, w in walls.items()})

# Zipf slope (log-log fit) — the "Comparative" ray
r = np.arange(1, V + 1); f = np.array(sorted(uni.values(), reverse=True))
zipf = float(np.polyfit(np.log(r), np.log(f), 1)[0])

# ── Entropy: is there order? (real text vs shuffled within each seal) ────────────────────
def H_uni(ts):
    c = collections.Counter(s for t in ts for s in t); n = sum(c.values())
    return -sum(v / n * math.log2(v / n) for v in c.values())
def H_cond(ts):
    big = collections.Counter((a, b) for t in ts for a, b in zip(t, t[1:])); first = collections.Counter(a for (a, b) in big.elements())
    n = sum(big.values())
    return -sum(v / n * math.log2(v / first[a]) for (a, b), v in big.items())
Hc_real = H_cond(clean)
shuf = []
for _ in range(500):
    shuf.append(H_cond([random.sample(t, len(t)) for t in clean]))
Hc_shuf = float(np.mean(shuf)); Hc_shuf_sd = float(np.std(shuf))
z_order = (Hc_shuf - Hc_real) / Hc_shuf_sd
out['entropy'] = dict(H_unigram=round(H_uni(clean), 3), H_conditional=round(Hc_real, 3),
                      H_conditional_shuffled=round(Hc_shuf, 3), shuffled_sd=round(Hc_shuf_sd, 3), z=round(z_order, 1))

# ── Gyroscopic core: plug-and-play fill-in-the-blank, leave-one-text-out ──────────────
def train(ts):
    u = collections.Counter(s for t in ts for s in t)
    L = collections.Counter(); R = collections.Counter()
    for t in ts:
        for a, b in zip(t, t[1:]):
            L[(a, b)] += 1; R[(b, a)] += 1
    return u, L
def fill(u, L, left, right, k=5, alpha=0.1):
    vocab = list(u); n = sum(u.values()); Vn = len(vocab)
    lc = collections.Counter(); rc = collections.Counter()
    for (a, b), v in L.items():
        lc[a] += v
    sc = {}
    for s in vocab:
        p = (u[s] + alpha) / (n + alpha * Vn)
        if left: p *= (L[(left, s)] + alpha * p * Vn) / (lc[left] + alpha * Vn)
        if right: p *= (L[(s, right)] + alpha) / (u[s] + alpha * Vn)
        sc[s] = p
    return [s for s, _ in sorted(sc.items(), key=lambda x: -x[1])[:k]]
hit1 = hit5 = base1 = base5 = total = 0
for i, t in enumerate(clean):
    if len(t) < 2: continue
    u, L = train(clean[:i] + clean[i + 1:])
    freq = [s for s, _ in u.most_common(5)]
    for j, s in enumerate(t):
        left = t[j - 1] if j > 0 else None; right = t[j + 1] if j < len(t) - 1 else None
        g = fill(u, L, left, right)
        total += 1; hit1 += g[0] == s; hit5 += s in g; base1 += freq[0] == s; base5 += s in freq
fillr = dict(trials=total, top1=round(hit1 / total, 3), top5=round(hit5 / total, 3),
             freq_top1=round(base1 / total, 3), freq_top5=round(base5 / total, 3))
out['fill_in_blank'] = fillr

# ── Classifier ray: positional behaviour (initial = first read, terminal = last read) ──
posn = {}
for s, c in uni.items():
    if c < 6: continue
    ini = sum(1 for t in clean if len(t) > 1 and t[0] == s)
    ter = sum(1 for t in clean if len(t) > 1 and t[-1] == s)
    posn[s] = dict(n=c, initial=ini, terminal=ter, desc=short(s))
terminal = sorted(posn.items(), key=lambda kv: -kv[1]['terminal'] / kv[1]['n'])[:6]
initial = sorted(posn.items(), key=lambda kv: -kv[1]['initial'] / kv[1]['n'])[:6]
out['position'] = dict(terminal=[[k, v] for k, v in terminal], initial=[[k, v] for k, v in initial])

# ── Abacus ray: stroke signs and what follows them ──────────────────────────────────────
strokes = [p for p in uni if re.search(r'adjacent .*(strokes|lines)|^A single small vertical line', desc(p), re.I) and not re.search(r'jar|U with|triangle|tree|fish', desc(p), re.I)]
after = collections.Counter(); before = collections.Counter()
for t in clean:
    for a, b in zip(t, t[1:]):
        if a in strokes and b not in strokes: after[b] += 1
        if b in strokes and a not in strokes: before[a] += 1
out['abacus'] = dict(stroke_signs=[[p, uni[p], short(p)] for p in sorted(strokes, key=lambda p: -uni[p])],
                     read_after=[[p, c, short(p)] for p, c in after.most_common(6)],
                     read_before=[[p, c, short(p)] for p, c in before.most_common(6)])

# ── This:That::That:This ray: signs that share contexts (distributional similarity) ────
ctx = collections.defaultdict(collections.Counter)
for t in clean:
    pad = ['<'] + t + ['>']
    for i in range(1, len(pad) - 1):
        ctx[pad[i]]['L' + pad[i - 1]] += 1; ctx[pad[i]]['R' + pad[i + 1]] += 1
cand = [s for s in uni if uni[s] >= 6]
def cos(a, b):
    k = set(ctx[a]) & set(ctx[b]); num = sum(ctx[a][x] * ctx[b][x] for x in k)
    return num / (math.sqrt(sum(v * v for v in ctx[a].values())) * math.sqrt(sum(v * v for v in ctx[b].values())))
pairs = sorted(((cos(a, b), a, b) for a, b in itertools.combinations(cand, 2)), reverse=True)[:8]
out['analogy'] = [[round(c, 3), a, b, short(a), short(b)] for c, a, b in pairs]

# ── Metas: 500 bootstrap resamples of the seals; which pairs survive? ──────────────────
top10 = [k for k, _ in bigr.most_common(10)]; keep = collections.Counter()
for _ in range(500):
    smp = [random.choice(clean) for _ in clean]
    b = collections.Counter((a, c) for t in smp for a, c in zip(t, t[1:]))
    for k, _ in b.most_common(10): keep[k] += 1
out['metas'] = dict(resamples=500, stable_pairs=[[list(k), keep[k] / 500, short(k[0]), short(k[1])] for k in top10])

# ── Dream Engine: sample “dream” seals from the learned model, compare with real ones ──
u, L = train(clean)
starts = collections.Counter(t[0] for t in clean if t)
ends = collections.Counter(t[-1] for t in clean if t)
def dream():
    s = random.choices(list(starts), weights=list(starts.values()))[0]; t = [s]
    while len(t) < 14:
        nxt = [(b, v) for (a, b), v in L.items() if a == t[-1]]
        stop = ends[t[-1]] / max(1, u[t[-1]])
        if not nxt or random.random() < stop: break
        t.append(random.choices([b for b, _ in nxt], weights=[v for _, v in nxt])[0])
    return t
dreams = [dream() for _ in range(2000)]
real_set = {tuple(t) for t in clean}
out['dream'] = dict(n=2000, mean_len=round(float(np.mean([len(d) for d in dreams])), 2), real_mean_len=out['corpus']['mean_len'],
                    copies_of_real=sum(1 for d in dreams if tuple(d) in real_set),
                    jar_terminal_dream=round(sum(1 for d in dreams if d[-1] == 'P324') / 2000, 3),
                    jar_terminal_real=round(sum(1 for t in clean if t and t[-1] == 'P324') / len(clean), 3),
                    samples=[d for d in dreams[:5]])

# ── The 419-sign "completed lexicon" (Feb 2025) checked against the real sign shapes ──
gpt = json.load(open('gpt_list.json'))
CAT = {'fish': r'fish', 'jar/vessel': r'\bjar|vessel|pot\b', 'stroke/line': r'stroke|vertical line|line', 'person': r'person|man\b|human|figure',
       'tree/plant': r'tree|branch|leaf|plant', 'bird': r'bird', 'animal': r'bull|elephant|tiger|deer|rhino|animal|crocodile|snake|scorpion|monkey|peacock',
       'wheel/circle': r'circle|wheel|ring|oval|dot', 'arrow/weapon': r'arrow|spear|bow|weapon', 'mountain/triangle': r'triangle|mountain|pincer'}
def cats(s): return {k for k, rx in CAT.items() if re.search(rx, s or '', re.I)}
M2P = {}
for p, v in SIGN.items():
    for m in v.get('M') or []: M2P.setdefault(m[1:].zfill(3), p)
checked = agree = 0; examples = []
for m, p in sorted(M2P.items()):
    if m not in gpt: continue
    real = cats(desc(p)); claim = cats(gpt[m])
    if not real: continue
    checked += 1; ok = bool(real & claim); agree += ok
    if m in ('342', '059', '087', '099', '161', '336', '015', '216', '267', '067', '065'):
        examples.append(dict(M='M' + m, real=short(p), lexicon=gpt[m].split('  ')[0]))
keys = [m for m in sorted(M2P) if m in gpt and cats(desc(M2P[m]))]
perm = []
for _ in range(1000):
    sh = random.sample(keys, len(keys))
    perm.append(sum(bool(cats(desc(M2P[a])) & cats(gpt[b])) for a, b in zip(keys, sh)) / len(keys))
out['gpt_lexicon_check'] = dict(entries=len(gpt), checked=checked, same_category=agree, rate=round(agree / checked, 3),
    chance_rate=round(float(np.mean(perm)), 3), chance_p95=round(float(np.percentile(perm, 95)), 3), examples=examples)

# ── Build the EVE: the Museum envelope and its Rays as NVEs ────────────────────────────
eve = EVE(n_slots=720)
ray_defs = [
 ("Old Indus Valley", "the seals themselves, in reading order", math.log2(len(texts))),
 ("Present-day Indus Valley", "modern languages of the region — no data loaded", 0.0),
 ("Lexicon", "signs on the core surface, 2–7-sign strings on the inner walls", math.log2(V)),
 ("Artifact Repository", "CISI files nested inside the Lexicon core", math.log2(len(toks))),
 ("Comparative", "Zipf slope and entropy against shuffled text", max(0.0, z_order)),
 ("Gyroscopic Core", "plug-and-play fill-in-the-blank", 10 * (fillr['top1'] - fillr['freq_top1'])),
 ("Abacus", "stroke signs and their neighbours", math.log2(1 + len(strokes))),
 ("Classifiers", "initial and terminal sign classes", sum(1 for k, v in posn.items() if v['terminal'] / v['n'] > .5)),
 ("This:That::That:This", "signs that share contexts", 10 * pairs[0][0]),
 ("Reverse-engineering IETF", "present day → past; needs language data not in hand", 0.0),
 ("Dream Engine", "samples new seals from the learned model", math.log2(len(dreams))),
]
for name, purpose, rr in ray_defs:
    n = eve.open(name, purpose); n.r = round(rr, 4)
    n.log(evidence=n.r)
lex = eve.nves['Lexicon']
for m in range(2, 8):
    lex.manifold_inward(f"wall-{m}", f"{m}-sign strings").r = math.log2(1 + combos[m])
S = eve.unified_state(k=0.5, t=1.0)
S_even = EVE(n_slots=720)
for name, purpose, rr in ray_defs: S_even.open(name, purpose).r = 1.0
out['eve'] = dict(rays=[dict(name=n.name, purpose=n.purpose, r=n.r, theta=round(n.theta, 4), phi=round(n.phi, 4),
                             u=[round(float(x), 4) for x in n.u]) for n in eve.nves.values()],
                  lexicon_walls={k: round(v.r, 3) for k, v in lex.children.items()},
                  min_separation_deg=round(eve.gyroscopic_check(), 2),
                  S=S, S_equal_weights=S_even.unified_state(k=0.5, t=1.0), note=null_model_note())
try:
    eve.unified_state(k=1.0)
except ValueError as e:
    out['eve']['k_ge_1'] = str(e)

json.dump(out, open('ep7_results.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ('corpus', 'entropy', 'fill_in_blank', 'gpt_lexicon_check', 'dream')}, ensure_ascii=False, indent=1))
print('zipf', round(zipf, 3)); out['zipf_slope'] = round(zipf, 3)
print('S', out['eve']['S']['magnitude'], 'equal', out['eve']['S_equal_weights']['magnitude'], 'sep', out['eve']['min_separation_deg'])
print('analogy', out['analogy'][:5]); print('position', [(k, v['terminal'], v['n']) for k, v in out['position']['terminal']])
print('abacus', out['abacus']['read_after'][:4]); print('metas', [(x[0], x[1]) for x in out['metas']['stable_pairs']])
json.dump(out, open('ep7_results.json', 'w'), ensure_ascii=False, indent=1)
