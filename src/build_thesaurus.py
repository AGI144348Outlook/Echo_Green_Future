#!/usr/bin/env python3
"""
build_thesaurus.py — Regenerates en_thesaurus.jsonl from NLTK WordNet.
Run once in the Codespace before generate_matrices.py.

Usage:
    pip install nltk --break-system-packages -q
    python build_thesaurus.py
"""
import json, sys

print("Building en_thesaurus.jsonl from WordNet...")

try:
    from nltk.corpus import wordnet as wn
    list(wn.synsets("entity"))
except Exception:
    import nltk
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    from nltk.corpus import wordnet as wn

pos_map = {
    wn.NOUN: 'noun', wn.VERB: 'verb',
    wn.ADJ:  'adj',  wn.ADV:  'adv',
}

count = 0
with open('en_thesaurus.jsonl', 'w') as f:
    for synset in wn.all_synsets():
        pos = pos_map.get(synset.pos(), 'noun')
        lemmas = synset.lemma_names()
        definitions = [synset.definition()]
        examples = synset.examples()
        if examples:
            definitions.extend([f'"{e}"' for e in examples[:1]])

        for i, lemma in enumerate(lemmas):
            word = lemma.replace('_', ' ')
            synonyms = [l.replace('_', ' ') for l in lemmas if l != lemma]
            entry = {
                'pos':        pos,
                'wordnet_id': synset.offset(),
                'word':       word,
                'key':        f'{lemma}_{i+1}',
                'synonyms':   synonyms,
                'desc':       definitions,
            }
            f.write(json.dumps(entry) + '\n')
            count += 1

        if count % 10000 == 0:
            print(f"  {count:,} entries written...")

print(f"\nen_thesaurus.jsonl complete: {count:,} entries")
print("Now run: python generate_matrices.py")
