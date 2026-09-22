#!/usr/bin/env python3
"""
generate_matrices.py — ECHO Matrix Generator
Regenerates matrices/echo_lobby_agents.json and matrices/echo_lhea_chains.json
from the project's source data.

Run from the repo root:
    pip install nltk --break-system-packages -q
    python generate_matrices.py

Requires: src/echo_governor_skeleton.py, src/alphabet_data.py,
          corpus/mashet_parsed.json, matrices/echo_mashet_corpus.json
"""

import sys, json, re, os

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO_ROOT, 'src'))

print("ECHO Matrix Generator")
print("="*60)

try:
    from nltk.corpus import wordnet as wn
    list(wn.synsets("entity"))
    print("WordNet: already available")
except Exception:
    print("WordNet: downloading...")
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'nltk',
                    '--break-system-packages', '-q'], check=False)
    import nltk
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    from nltk.corpus import wordnet as wn
    print("WordNet: ready")

print("Loading ECHO infrastructure...")
from echo_governor_skeleton import (
    AlgorithmMatrix, Lobby, HEBREW_LETTER_INDEX,
    VocabularyAcquisitionAgent,
)

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

print("Building vocabulary matrix...")
matrix = AlgorithmMatrix()
synonyms_map = {}
lexicon = {}

thesaurus_path = os.path.join(REPO_ROOT, 'corpus', 'en_thesaurus.jsonl')
if not os.path.exists(thesaurus_path):
    thesaurus_path = os.path.join(REPO_ROOT, 'en_thesaurus.jsonl')
if not os.path.exists(thesaurus_path):
    thesaurus_path = os.path.expanduser('~/en_thesaurus.jsonl')

if os.path.exists(thesaurus_path):
    print(f"Thesaurus: {thesaurus_path}")
    with open(thesaurus_path) as f:
        qualifying = [json.loads(l) for l in f if json.loads(l).get('desc')]
    stride = max(1, len(qualifying) // 1000)
    for entry in qualifying[::stride][:1000]:
        matrix.index_dictionary_entry(
            entry['word'], ' '.join(entry['desc']),
            pos=entry.get('pos'), synonyms=entry.get('synonyms', []),
            category='thesaurus_def')
        if entry.get('synonyms'):
            synonyms_map[entry['word'].lower()] = [s.lower() for s in entry['synonyms']]
        lexicon[entry['word'].lower()] = {
            'desc': ' '.join(entry['desc']), 'pos': entry.get('pos', '?')}
    print(f"Thesaurus: {len(qualifying)} entries loaded")
else:
    print("WARNING: en_thesaurus.jsonl not found — lobby will be smaller")

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
    'invariant':'property preserved under transformation unchanging permanent',
    'potential':'capacity to receive and become latent unrealized possibility',
    'stewardship':'creator obligation responsibility wellbeing flourishing protection',
    'jurisdiction':'perimeter triangular planar semantic region latin root constrain',
    'matrix':'content-first table elemental parts rows structure',
    'index':'lookup-first key resolving to matrix or row bidirectional traversal',
}
for word, desc in PRIOR.items():
    matrix.index_dictionary_entry(word, desc, pos='noun', category='prior_session')
    lexicon[word] = {'desc': desc, 'pos': 'noun'}

mashet_path = os.path.join(REPO_ROOT, 'corpus', 'mashet_parsed.json')
if not os.path.exists(mashet_path):
    mashet_path = os.path.join(REPO_ROOT, 'matrices', 'echo_mashet_corpus.json')
if os.path.exists(mashet_path):
    with open(mashet_path) as f:
        mashet = json.load(f)
    entries = mashet if isinstance(mashet, list) else list(mashet.values())
    for entry in entries:
        word = entry.get('word', entry.get('mashet', ''))
        desc = entry.get('definition', entry.get('desc', ''))
        if word and desc:
            matrix.index_dictionary_entry(word, desc[:200], pos='noun',
                                           category='mashet_corpus')
            lexicon[word.lower()] = {'desc': desc[:200], 'pos': 'noun'}
    print(f"Mashet corpus: {len(entries)} entries loaded")

print("Running orientation pipeline...")
lobby = Lobby(matrix)
lobby.populate()
lobby.run_orientation()
lobby.run_typed_study_groups()
if synonyms_map:
    lobby.run_thesaurus(synonyms_map)
lobby.compute_generality_scores()
print(f"Lobby agents: {len(lobby.agents)}")

print("Enriching with WordNet hypernym chains...")
acq = VocabularyAcquisitionAgent(lobby=lobby, lexicon=lexicon, alg_matrix=matrix)
wn_result = acq.enrich_lobby_with_wordnet(max_words=500)
print(f"WordNet: +{wn_result.get('new_genus_links', 0)} genus terms added")
print(f"Total lobby agents: {len(lobby.agents)}")

print("\nGenerating echo_lobby_agents.json...")
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

out_dir = os.path.join(REPO_ROOT, 'matrices')
os.makedirs(out_dir, exist_ok=True)

agents_path = os.path.join(out_dir, 'echo_lobby_agents.json')
with open(agents_path, 'w') as f:
    json.dump(agents_export, f, indent=2, ensure_ascii=False)
kb = os.path.getsize(agents_path) // 1024
print(f"echo_lobby_agents.json: {len(agents_export)} agents, {kb} KB")

print("\nGenerating echo_lhea_chains.json...")
STOP = {'the','a','an','of','in','on','at','to','and','or','with','by',
        'from','for','as','is','are','was','were','that','which','this',
        'it','be','been','have','has','not','so','if','then','but','also'}

all_lhea = {}

for word in lobby.agents:
    letters = decompose(word)
    if len(letters) >= 2:
        chain = lhea_chain(letters)
        gematria = sum(HEBREW_LETTER_INDEX.get(l,{}).get('val',0) for l in letters)
        all_lhea[word] = {'letters': letters, 'chain': chain, 'gematria': gematria}

extra_terms = [
    'perception','environment','reality','experience','semiotics','topology',
    'consciousness','stewardship','flourishing','suffering','authentic','emergent',
    'causality','nominalization','actualization','instantiation','operative',
    'traversal','substrate','bedrock','generative','metacontroller','recursive',
    'executable','descriptive','emergence','consent','intrinsic','instrumental',
    'precautionary','complementarity','processual','hexagram','trigram',
    'invariant','potentiality','receptive','tetrahedron','configuration',
    'transformation','manifestation','polarity','combinatorial','eigenvalue',
    'myelination','ossification','propagational','inhabitant','opcode',
    'lexical','ontological','zatamsen','jurisdiction','bidirectional',
    'being','effecting','becoming','being','effecting','yang','yin',
]
for word in extra_terms:
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
print(f"echo_lhea_chains.json: {len(all_lhea)} chains, {kb} KB")

print("\n" + "="*60)
print("GENERATION COMPLETE")
print("="*60)
print(f"\nFiles written to {out_dir}/")
print("  echo_lobby_agents.json")
print("  echo_lhea_chains.json")
print("\nNext steps in terminal:")
print("  git add matrices/echo_lobby_agents.json")
print("  git add matrices/echo_lhea_chains.json")
print('  git commit -m "feat: add generated lobby agents and LHEA chains"')
print("  git push origin genesis-documentary")
