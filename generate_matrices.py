#!/usr/bin/env python3
"""
generate_matrices.py — ECHO Matrix Generator
Regenerates matrices/echo_lobby_agents.json and matrices/echo_lhea_chains.json

Run from the repo root:
    python build_thesaurus.py   # first time only
    python generate_matrices.py

KEY FIX: WordNet genus terms are indexed into the matrix BEFORE lobby.populate()
so they become full agents, not orphaned matrix entries.
"""

import sys, json, re, os

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO_ROOT, 'src'))

print("ECHO Matrix Generator")
print("="*60)

# ── WordNet ───────────────────────────────────────────────────────────────
try:
    from nltk.corpus import wordnet as wn
    list(wn.synsets("entity"))
    print("WordNet: ready")
except Exception:
    import subprocess, nltk
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'nltk',
                    '--break-system-packages', '-q'], check=False)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    from nltk.corpus import wordnet as wn
    print("WordNet: downloaded and ready")

# ── Import ECHO ───────────────────────────────────────────────────────────
print("Loading ECHO...")
from echo_governor_skeleton import (
    AlgorithmMatrix, Lobby, HEBREW_LETTER_INDEX,
)

# ── Helpers ───────────────────────────────────────────────────────────────
PHONEME_MAP = {
    'sh':'shin','ts':'tsadi','th':'tav','kh':'het','ch':'het',
    'a':'aleph','b':'bet','v':'vav','g':'gimel','d':'dalet','h':'he',
    'z':'zayin','t':'tet','y':'yod','k':'kaf','l':'lamed','m':'mem',
    'n':'nun','s':'samekh','e':'he','p':'pe','f':'pe','q':'qof',
    'r':'resh','i':'yod','o':'ayin','u':'vav',
}

def decompose(word):
    w = word.lower(); result = []; i = 0
    while i < len(w):
        matched = False
        if i + 2 <= len(w):
            two = w[i:i+2]
            if two in PHONEME_MAP and PHONEME_MAP[two] in HEBREW_LETTER_INDEX:
                result.append(PHONEME_MAP[two]); i += 2; matched = True
        if not matched:
            one = w[i]
            if one in PHONEME_MAP and PHONEME_MAP[one] in HEBREW_LETTER_INDEX:
                result.append(PHONEME_MAP[one])
            i += 1
    deduped = []
    for l in result:
        if not deduped or l != deduped[-1]:
            deduped.append(l)
    return deduped

def lhea_chain(letters):
    parts = []
    for n in letters:
        d = HEBREW_LETTER_INDEX.get(n, {})
        s = d.get('lhea', '?').split('—')[0].strip().split('/')[0].strip()
        parts.append(f"{d.get('glyph','?')}({s})")
    return ' → '.join(parts)

# ── PHASE 1: Build matrix BEFORE lobby ───────────────────────────────────
print("\nPhase 1: Building matrix...")
matrix = AlgorithmMatrix()
synonyms_map = {}
lexicon = {}

# Thesaurus
for path in ['en_thesaurus.jsonl',
             os.path.join(REPO_ROOT, 'corpus', 'en_thesaurus.jsonl'),
             os.path.expanduser('~/en_thesaurus.jsonl')]:
    if os.path.exists(path):
        print(f"Thesaurus: {path}")
        with open(path) as f:
            qualifying = [json.loads(l) for l in f if json.loads(l).get('desc')]
        stride = max(1, len(qualifying) // 1000)
        for entry in qualifying[::stride][:1000]:
            matrix.index_dictionary_entry(
                entry['word'], ' '.join(entry['desc']),
                pos=entry.get('pos'), synonyms=entry.get('synonyms', []),
                category='thesaurus_def')
            if entry.get('synonyms'):
                synonyms_map[entry['word'].lower()] = [
                    s.lower() for s in entry['synonyms']]
            lexicon[entry['word'].lower()] = {
                'desc': ' '.join(entry['desc']), 'pos': entry.get('pos','?')}
        print(f"  Thesaurus: {len(qualifying):,} entries, stride={stride}")
        break
else:
    print("WARNING: en_thesaurus.jsonl not found — run build_thesaurus.py first")

# Prior session vocabulary
PRIOR = {
    'echo':'governor indexing algorithm A-000 resh identity index made algorithm',
    'mashet':'source transformation completion framework symbolic substrate 740',
    'alamaket':'potential aspiration source sanctity completion kernel engine 571',
    'governor':'first algorithm A-000 causal boundary identity semantic termination',
    'lhea':'latin hebrew execution architecture operators symbolic substrate 22 letters',
    'ayin':'eye perception depth operator Hebrew letter 70 classifier',
    'pe':'mouth speech expression operator Hebrew letter 80',
    'resh':'head beginning identity leader A-000 governor letter 200 equilibrium',
    'being':'nouned verb existence entity state potential actual',
    'effecting':'verb nouned actualization mechanism producing state causation',
    'yang':'heaven pure invariant creative active solid line principle',
    'yin':'earth pure potential receptive broken yielding principle',
    'hexagram':'six line configuration state system 64 binary change transformation',
    'trigram':'three line configuration eight states binary heaven earth',
    'invariant':'property preserved under transformation unchanging permanent',
    'potential':'capacity to receive and become latent unrealized possibility',
    'stewardship':'creator obligation responsibility wellbeing flourishing protection',
    'jurisdiction':'perimeter triangular planar semantic region latin root constrain',
    'matrix':'content-first table elemental parts rows structure',
    'index':'lookup-first key resolving to matrix or row bidirectional traversal',
    'eigenvalue':'centrality weight balance graph node importance measure',
    'myelination':'pathway reinforcement persistence count threshold hardening edge',
    'perception':'eye ayin operator classify incoming tokens semantic classification',
    'topology':'space structure properties continuous transformation invariant',
    'semiotics':'signs meaning symbol representation linguistic structure',
    'consciousness':'aware subjective experience entity state self perception',
    'boundary':'distinguishes separates defines limit perimeter edge',
    'substrate':'foundation base layer unchanging coordinate space letter operators',
    'traversal':'navigation matrix index content lookup bidirectional path',
}
for word, desc in PRIOR.items():
    matrix.index_dictionary_entry(word, desc, pos='noun', category='prior_session')
    lexicon[word] = {'desc': desc, 'pos': 'noun'}

# Mashet corpus
for path in [os.path.join(REPO_ROOT, 'corpus', 'mashet_parsed.json'),
             os.path.join(REPO_ROOT, 'matrices', 'echo_mashet_corpus.json'),
             'mashet_parsed.json']:
    if os.path.exists(path):
        with open(path) as f:
            mashet = json.load(f)
        entries = mashet if isinstance(mashet, list) else list(mashet.values())
        for entry in entries:
            word = entry.get('word', entry.get('mashet', ''))
            desc = entry.get('definition', entry.get('desc', ''))
            if word and desc:
                matrix.index_dictionary_entry(
                    word, desc[:200], pos='noun', category='mashet_corpus')
                lexicon[word.lower()] = {'desc': desc[:200], 'pos': 'noun'}
        print(f"Mashet corpus: {len(entries)} entries")
        break

print(f"Matrix entries before WordNet: {len(matrix.known)}")

# ── PHASE 2: WordNet genus terms → matrix BEFORE populate ────────────────
print("\nPhase 2: WordNet genus enrichment (pre-populate)...")
new_genus = 0
seen = set(lexicon.keys())

# Get all synsets and index genus terms
for synset in list(wn.all_synsets(wn.NOUN))[:15000]:
    for path in synset.hypernym_paths():
        for s in path:
            lemma = s.lemma_names()[0].replace('_', ' ').lower()
            if lemma not in seen and len(lemma) > 2:
                desc = s.definition()
                matrix.index_dictionary_entry(
                    lemma, desc, pos='noun', category='wordnet_genus')
                lexicon[lemma] = {'desc': desc, 'pos': 'noun'}
                seen.add(lemma)
                new_genus += 1

print(f"WordNet genus terms added to matrix: {new_genus:,}")
print(f"Matrix entries after WordNet: {len(matrix.known)}")

# ── PHASE 3: Lobby — NOW includes all matrix entries ─────────────────────
print("\nPhase 3: Building lobby from enriched matrix...")
lobby = Lobby(matrix)
lobby.populate()
print(f"Lobby after populate: {len(lobby.agents)} agents")

lobby.run_orientation()
lobby.run_typed_study_groups()
if synonyms_map:
    lobby.run_thesaurus(synonyms_map)
lobby.compute_generality_scores()
print(f"Lobby after orientation: {len(lobby.agents)} agents")

# ── PHASE 4: Export lobby agents ─────────────────────────────────────────
print("\nPhase 4: Exporting lobby agents...")
out_dir = os.path.join(REPO_ROOT, 'matrices')
os.makedirs(out_dir, exist_ok=True)

agents_export = {}
for word, agent in lobby.agents.items():
    agents_export[word] = {
        'department':       agent.department,
        'entry_class':      agent.entry_class,
        'generality_score': round(agent.generality_score, 4),
        'neighborhood':     agent.neighborhood,
        'study_group_type': getattr(agent, 'study_group_type', None),
        'ties':             list(agent.ties)[:20],
        'definition':       lexicon.get(word, {}).get('desc', '')[:200],
    }

agents_path = os.path.join(out_dir, 'echo_lobby_agents.json')
with open(agents_path, 'w') as f:
    json.dump(agents_export, f, indent=2, ensure_ascii=False)
kb = os.path.getsize(agents_path) // 1024
print(f"echo_lobby_agents.json: {len(agents_export):,} agents, {kb} KB")

# ── PHASE 5: Export LHEA chains ───────────────────────────────────────────
print("\nPhase 5: Exporting LHEA chains...")
all_lhea = {}

for word in lobby.agents:
    letters = decompose(word)
    if len(letters) >= 2:
        chain = lhea_chain(letters)
        gematria = sum(HEBREW_LETTER_INDEX.get(l,{}).get('val',0) for l in letters)
        all_lhea[word] = {'letters': letters, 'chain': chain, 'gematria': gematria}

# Extra philosophical/technical terms from the session
EXTRA = [
    'perception','environment','reality','experience','semiotics','topology',
    'consciousness','stewardship','flourishing','suffering','authentic',
    'emergent','causality','nominalization','actualization','instantiation',
    'operative','traversal','substrate','bedrock','generative','recursive',
    'executable','descriptive','emergence','consent','intrinsic','instrumental',
    'precautionary','complementarity','processual','hexagram','trigram',
    'invariant','potentiality','receptive','tetrahedron','configuration',
    'transformation','manifestation','polarity','combinatorial','eigenvalue',
    'myelination','ossification','propagational','inhabitant','opcode',
    'lexical','ontological','zatamsen','jurisdiction','bidirectional',
    'being','effecting','becoming','yang','yin','mashet','alamaket',
]
for word in EXTRA:
    if word not in all_lhea:
        letters = decompose(word)
        if len(letters) >= 2:
            chain = lhea_chain(letters)
            gematria = sum(HEBREW_LETTER_INDEX.get(l,{}).get('val',0) for l in letters)
            all_lhea[word] = {'letters': letters, 'chain': chain, 'gematria': gematria}

lhea_path = os.path.join(out_dir, 'echo_lhea_chains.json')
with open(lhea_path, 'w') as f:
    json.dump(all_lhea, f, indent=2, ensure_ascii=False)
kb = os.path.getsize(lhea_path) // 1024
print(f"echo_lhea_chains.json: {len(all_lhea):,} chains, {kb} KB")

# ── Done ──────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("GENERATION COMPLETE")
print("="*60)
print(f"\nLobby agents: {len(agents_export):,}")
print(f"LHEA chains:  {len(all_lhea):,}")
print(f"\nNext steps:")
print("  git add matrices/echo_lobby_agents.json matrices/echo_lhea_chains.json")
print('  git commit -m "feat: add generated lobby agents and LHEA chains"')
print("  git push origin genesis-documentary")
