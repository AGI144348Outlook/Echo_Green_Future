"""
A-144 Augmented: HypernymGrammarModule
A-145 Augmented: MirrorStep + SelfExtend

Two modular augmentations to the existing Pe/Ayin pipeline.
Neither rewrites A-144 or A-145. Both plug in at specific points.

Full augmented pipeline:
INPUT → TOKENIZE → AYIN → GENERALIZE → VGM → DESCEND → PE(hypernym) → EXPRESS → MIRROR → SELF-EXTEND

A-144 augmentation: Pe now speaks by traversing hypernym chains,
not by assembling flat definitions. The chain is the grammar.

A-145 augmentation: after Express, Mirror runs the pipeline on
what was just said. GAPs in ECHO's own speech become the highest
priority acquisition targets. ECHO grows from its own expression.
"""

import sys, json
sys.path.insert(0, '/home/claude')
from echo_governor_skeleton import (
    AlgorithmMatrix, Lobby, HEBREW_LETTER_INDEX,
    InwardSearchEngine, LogicReasoningMatrix,
    build_number_matrix, VocabularyAcquisitionAgent,
    AlgorithmicCommunicator,
)
try:
    from nltk.corpus import wordnet as wn
    list(wn.synsets("entity"))
except:
    import nltk; nltk.download('wordnet', quiet=True)
    from nltk.corpus import wordnet as wn

# ── PHONEME MAP ────────────────────────────────────────────────────────────
PHONEME_MAP = {
    'sh':'shin','ts':'tsadi','th':'tav','kh':'het','ch':'het',
    'a':'aleph','b':'bet','v':'vav','g':'gimel','d':'dalet','h':'he',
    'z':'zayin','t':'tet','y':'yod','k':'kaf','l':'lamed','m':'mem',
    'n':'nun','s':'samekh','e':'he','p':'pe','f':'pe','q':'qof',
    'r':'resh','i':'yod','o':'ayin','u':'vav',
}
def decompose(word):
    w=word.lower(); result=[]; i=0
    while i<len(w):
        matched=False
        if i+2<=len(w):
            two=w[i:i+2]
            if two in PHONEME_MAP and PHONEME_MAP[two] in HEBREW_LETTER_INDEX:
                result.append(PHONEME_MAP[two]); i+=2; matched=True
        if not matched:
            one=w[i]
            if one in PHONEME_MAP and PHONEME_MAP[one] in HEBREW_LETTER_INDEX:
                result.append(PHONEME_MAP[one])
            i+=1
    deduped=[]
    for l in result:
        if not deduped or l!=deduped[-1]: deduped.append(l)
    return deduped

def article(word, cap=True):
    art = 'An' if word[0].lower() in 'aeiou' else 'A'
    return art if cap else art.lower()

# ═══════════════════════════════════════════════════════════════════════════
# A-144 AUGMENTATION: HypernymGrammarModule
# Pe now speaks by traversing the hypernym chain of each word.
# The chain is the grammar. The definitions fill the slots.
# Three sentence patterns extracted from the chain structure.
# ═══════════════════════════════════════════════════════════════════════════

class HypernymGrammarModule:
    """
    Augments A-144 PeComposer.
    Given a word, pull its hypernym chain and speak from it.
    The chain is the thought. The sentence is the chain made audible.
    """

    def __init__(self, lobby=None, lexicon=None):
        self.lobby   = lobby
        self.lexicon = lexicon or {}
        self._chain_cache = {}

    def get_chain(self, word, pos='n'):
        """Pull the full hypernym chain for a word."""
        if word in self._chain_cache:
            return self._chain_cache[word]

        synsets = wn.synsets(word, pos=pos) or wn.synsets(word)
        if not synsets:
            return []

        paths = synsets[0].hypernym_paths()
        if not paths:
            return []

        chain = []
        for s in paths[0]:
            lemma = s.lemma_names()[0].replace('_', ' ').lower()
            defn  = s.definition()
            chain.append({'word': lemma, 'definition': defn,
                          'synset': s.name()})

        self._chain_cache[word] = chain
        return chain

    def chain_covers(self, chain_word, target_word):
        """Does this chain node cover the target word?"""
        chain = self.get_chain(chain_word)
        return any(node['word'] == target_word for node in chain)

    def shared_node(self, w1, w2):
        """Find the first node that both words share in their chains."""
        c1 = {n['word'] for n in self.get_chain(w1)}
        c2 = {n['word'] for n in self.get_chain(w2)}
        shared = c1 & c2
        if not shared:
            return None
        # Pick the one furthest from root (most specific shared ancestor)
        chain1 = self.get_chain(w1)
        for node in reversed(chain1):
            if node['word'] in shared:
                return node
        return None

    def speak_chain(self, word, depth=4):
        """
        A-144 AUGMENTED: Pe speaks by traversing the chain.
        Returns a stream of sentences — one per chain node.
        This is the hypernym stream of thought.
        """
        chain = self.get_chain(word)
        if not chain:
            return [f"{article(word)} {word} exists."]

        sentences = []
        chain_tail = chain[-depth:]   # most specific nodes first

        for i, node in enumerate(chain_tail):
            n = node['word']
            d = node['definition']
            art = article(n)

            # Pattern 1 — Identity: what the node IS
            short_def = d.split(';')[0].strip()
            if len(short_def) > 70:
                short_def = short_def[:67] + '...'
            sentences.append(f"{art} {n} is {short_def}.")

            # Pattern 2 — Inheritance: the word below inherits from this
            if i == 0:
                art_w = article(word)
                sentences.append(f"{art_w} {word} is {article(n, False)} {n}.")

            # Pattern 3 — Bridge: what this node leads toward
            if i < len(chain_tail) - 1:
                next_n = chain_tail[i+1]['word']
                art_next = article(next_n, False)
                sentences.append(
                    f"Every {n} is {art_next} {next_n}.")

        return sentences

    def speak_meeting(self, w1, w2):
        """
        Speak the proposition that forms when two words meet at a shared node.
        The meeting IS the thought.
        """
        node = self.shared_node(w1, w2)
        if not node:
            return None
        n   = node['word']
        art = article(n)
        art1 = article(w1, False)
        art2 = article(w2, False)
        return (
            f"{art1.capitalize()} {w1} and {art2} {w2} "
            f"both arrive at {art} {n}. "
            f"{art} {n} is {node['definition'].split(';')[0].strip()}."
        )


# ═══════════════════════════════════════════════════════════════════════════
# A-145 AUGMENTATION: MirrorStep + SelfExtend
# After Express, Mirror runs the pipeline on what was just said.
# GAPs in ECHO's own speech become the highest priority homework entries.
# ECHO grows from its own expression.
# ═══════════════════════════════════════════════════════════════════════════

class MirrorStep:
    """
    Augments A-145 AlgorithmicCommunicator.
    Runs after Express. Turns ECHO's own output into input.
    The pipeline reflects on what it just said.
    """

    def __init__(self, comm, inward, vgm, lobby, lexicon,
                 hypernym_module):
        self.comm       = comm
        self.inward     = inward
        self.vgm        = vgm
        self.lobby      = lobby
        self.lexicon    = lexicon
        self.hypernym   = hypernym_module

        # The homework ledger — what ECHO still needs to learn
        self.homework   = {}   # word → {count, sources, priority}
        # VGM candidates from ECHO's own speech
        self.self_proposals = []

    def _ayin_on_output(self, expressed_sentences):
        """
        Run Ayin classification on what Pe just said.
        GAPs in ECHO's own speech are the most urgent homework.
        """
        import re
        STOP = {'the','a','an','of','in','on','at','to','and','or','with',
                'by','from','for','as','is','are','was','were','that','which',
                'this','it','be','been','have','has','not','so','every',
                'both','all','each','also','but','if','then'}

        all_tokens = []
        for s in expressed_sentences:
            tokens = [w.lower().rstrip('.,!?')
                      for w in re.findall(r"[a-zA-Z']+", s)
                      if len(w) > 2 and w.lower() not in STOP]
            all_tokens.extend(tokens)

        gaps = []
        known = []
        for token in dict.fromkeys(all_tokens):  # unique, order preserved
            cls = self.comm._ayin_classify(token)
            if "GAP" in cls:
                gaps.append(token)
            else:
                known.append(token)

        return known, gaps

    def _inward_on_gaps(self, gaps):
        """Run inward search on each gap. Find what ECHO already knows."""
        hits  = []
        clean = []
        for word in gaps:
            result = self.inward.search(word)
            if result.found:
                hits.append((word, result.sources[0]))
            else:
                clean.append(word)
        return hits, clean

    def _vgm_candidate_from_speech(self, sentence):
        """
        Does this sentence ECHO just said qualify as a VGM candidate?
        A-126 syntactic check + A-151 generality check.
        """
        import re
        words = [w.lower() for w in re.findall(r"[a-zA-Z]+", sentence)
                 if len(w) > 2]

        # Must contain at least one known noun and one known verb
        has_noun = any(
            self.lobby.agents.get(w) and
            self.lobby.agents[w].department in ('noun','n')
            for w in words
        )
        has_verb = any(
            self.lobby.agents.get(w) and
            self.lobby.agents[w].department in ('verb','v')
            for w in words
        )
        if not (has_noun and has_verb):
            return None

        # At least one word must be abstract/high-generality
        high_gen = [
            w for w in words
            if self.lobby.agents.get(w) and
               self.lobby.agents[w].generality_score >= 0.25 and
               self.lobby.agents[w].entry_class in ('TYPE','ABSTRACT')
        ]
        if not high_gen:
            return None

        score = max(
            self.lobby.agents[w].generality_score
            for w in high_gen
        )
        return {
            'text':   sentence.rstrip('.'),
            'origin': 'self_expression',
            'score':  round(score, 4),
            'words':  words[:6],
        }

    def reflect(self, expressed_sentences, input_word):
        """
        The mirror runs.
        Takes what Pe just expressed.
        Returns what ECHO learned about what it said.
        """
        result = {
            'input_word':    input_word,
            'expressed':     expressed_sentences,
            'known_in_speech': [],
            'gaps_in_speech':  [],
            'inward_hits':     [],
            'new_homework':    [],
            'self_proposals':  [],
        }

        # Ayin on ECHO's own words
        known, gaps = self._ayin_on_output(expressed_sentences)
        result['known_in_speech'] = known
        result['gaps_in_speech']  = gaps

        # Inward search on gaps
        hits, still_unknown = self._inward_on_gaps(gaps)
        result['inward_hits'] = [
            {'word': w, 'type': s['type'], 'detail': s['detail'][:60]}
            for w, s in hits
        ]

        # Register new homework
        for word in still_unknown:
            if word not in self.homework:
                self.homework[word] = {
                    'count':    1,
                    'source':   f'self_expression:{input_word}',
                    'priority': 'HIGH',  # ECHO said this — it must learn it
                }
                result['new_homework'].append(word)
            else:
                self.homework[word]['count'] += 1

        # Check if any expressed sentences qualify as VGM candidates
        for sentence in expressed_sentences:
            candidate = self._vgm_candidate_from_speech(sentence)
            if candidate:
                # Is it already in VGM?
                existing_texts = [v['text'].lower() for v in self.vgm.values()]
                if candidate['text'].lower() not in existing_texts:
                    result['self_proposals'].append(candidate)
                    self.self_proposals.append(candidate)

        return result

    def homework_report(self):
        """What has ECHO still not learned from its own speech?"""
        by_priority = sorted(
            self.homework.items(),
            key=lambda x: (-x[1]['count'], x[0])
        )
        return by_priority


# ═══════════════════════════════════════════════════════════════════════════
# AUGMENTED PIPELINE — full end to end
# INPUT → TOKENIZE → AYIN → GENERALIZE → VGM → DESCEND
#       → PE(hypernym) → EXPRESS → MIRROR → SELF-EXTEND
# ═══════════════════════════════════════════════════════════════════════════

class AugmentedCommunicator:
    """
    A-145 + A-144 with both augmentations wired in.
    Speaks from hypernym chains. Reflects on its own speech.
    Grows from the reflection.
    """

    def __init__(self, comm, inward, vgm, lobby, lexicon,
                 hypernym_module, mirror):
        self.comm      = comm
        self.inward    = inward
        self.vgm       = vgm
        self.lobby     = lobby
        self.lexicon   = lexicon
        self.hypernym  = hypernym_module
        self.mirror    = mirror

    def process(self, input_word, verbose=True):
        """
        Full augmented pipeline on one word.
        """
        sep = "─" * 68

        if verbose:
            print(f"\n{sep}")
            print(f"  INPUT: '{input_word}'")
            print(sep)

        # ── TOKENIZE ─────────────────────────────────────────────────────
        word = input_word.lower().strip()

        # ── AYIN (classify) ───────────────────────────────────────────────
        cls = self.comm._ayin_classify(word)
        is_gap = "GAP" in cls
        if verbose:
            status = "GAP" if is_gap else "KNOWN"
            print(f"\n  ע Ayin: '{word}' → {status} ({cls})")

        # ── GENERALIZE ────────────────────────────────────────────────────
        agent = self.lobby.agents.get(word)
        if agent:
            gen_score = agent.generality_score
            entry_cls = agent.entry_class
            dept      = agent.department
            if verbose:
                print(f"  Generality: {gen_score:.4f}  "
                      f"class={entry_cls}  dept={dept}")

        # ── VGM QUERY ─────────────────────────────────────────────────────
        vgm_matches = []
        for sid, stmt in self.vgm.items():
            if word in stmt.get('words', []) or \
               word in stmt.get('text', '').lower():
                vgm_matches.append((sid, stmt['text']))
        if verbose and vgm_matches:
            print(f"  VGM: {len(vgm_matches)} axiom(s) touch this word")
            for sid, text in vgm_matches[:2]:
                print(f"    [{sid}] \"{text}\"")

        # ── INWARD (if gap) ───────────────────────────────────────────────
        if is_gap:
            ir = self.inward.search(word)
            if ir.found and verbose:
                print(f"  ←  Inward: found in "
                      f"{ir.sources[0]['type']}")

        # ── PE: HYPERNYM GRAMMAR (A-144 AUGMENTED) ───────────────────────
        if verbose:
            print(f"\n  פ Pe (hypernym grammar):")

        pos = 'v' if (agent and agent.department in ('verb','v')) else 'n'
        expressed = self.hypernym.speak_chain(word, depth=4)

        if verbose:
            print(f"  ┌─ Stream of thought:")
            for s in expressed:
                print(f"  │  {s}")
            print(f"  └─")

        # ── EXPRESS ───────────────────────────────────────────────────────
        # (output is the expressed sentences above)

        # ── MIRROR (A-145 AUGMENTED) ──────────────────────────────────────
        if verbose:
            print(f"\n  ◈ Mirror reflects on what Pe just said:")

        reflection = self.mirror.reflect(expressed, word)

        if verbose:
            print(f"  Known in own speech:   "
                  f"{reflection['known_in_speech'][:8]}")
            if reflection['gaps_in_speech']:
                print(f"  Gaps in own speech:    "
                      f"{reflection['gaps_in_speech'][:8]}")
            if reflection['inward_hits']:
                print(f"  Inward hits on gaps:")
                for h in reflection['inward_hits'][:3]:
                    print(f"    [{h['type'][:18]}] '{h['word']}': "
                          f"{h['detail']}")
            if reflection['new_homework']:
                print(f"  New homework entries:  "
                      f"{reflection['new_homework']}")
            if reflection['self_proposals']:
                print(f"  Self-proposed VGM candidates:")
                for p in reflection['self_proposals']:
                    print(f"    [{p['score']:.4f}] \"{p['text']}\"")

        # ── SELF-EXTEND ───────────────────────────────────────────────────
        # ECHO has now grown from speaking. The homework is the frontier.

        return {
            'word':        word,
            'expressed':   expressed,
            'reflection':  reflection,
            'vgm_matches': vgm_matches,
        }

    def meeting(self, w1, w2, verbose=True):
        """
        Two words meet at their shared hypernym node.
        The meeting forms a proposition.
        The mirror reflects on that proposition.
        """
        sentence = self.hypernym.speak_meeting(w1, w2)
        if not sentence:
            if verbose:
                print(f"  '{w1}' and '{w2}' share no hypernym node.")
            return None

        if verbose:
            print(f"\n  Meeting: '{w1}' ↔ '{w2}'")
            print(f"  Proposition: {sentence}")

        reflection = self.mirror.reflect([sentence], f"{w1}↔{w2}")
        if verbose and reflection['self_proposals']:
            print(f"  Mirror proposes VGM candidate:")
            for p in reflection['self_proposals']:
                print(f"    [{p['score']:.4f}] \"{p['text']}\"")

        return {'sentence': sentence, 'reflection': reflection}

