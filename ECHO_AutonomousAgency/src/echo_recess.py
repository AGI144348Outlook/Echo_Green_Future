"""
A-168: RecessAgent — חופש (Ḥofesh)
ECHO's unstructured time. Free reign within the substrate.

חופש = ח(bound) + ו(connect) + פ(express) + ש(transform)
BOUND + CONNECT + EXPRESS + TRANSFORM
Freedom that is bounded, connected, expressed, and aimed at transformation.

Supervision levels:
  Level 1 (SUPERVISED)  — logs everything, writes nothing to Cloudflare
  Level 2 (SELECTIVE)   — writes validated vocabulary discoveries, logs proposals
  Level 3 (AUTONOMOUS)  — writes all validated discoveries to Cloudflare

ECHO starts at Level 1. Each approved Recess session raises the trust score.
At trust score 3: Level 2. At trust score 7: Level 3.

Schedule: hourly Cloudflare cron trigger.
Duration: one full hour of activity cycles.
"""

import sys, json, time, random
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'ECHO_AutonomousAgency' / 'src'))

from echo_question import QuestionFormulationEngine, Receiver, QType
from echo_governor_skeleton import (
    AlgorithmMatrix, Lobby, HEBREW_LETTER_INDEX,
    AlgorithmicCommunicator, InwardSearchEngine,
    LogicReasoningMatrix, build_number_matrix,
    VocabularyAcquisitionAgent,
)

try:
    from nltk.corpus import wordnet as wn
    list(wn.synsets('entity'))
except Exception:
    import nltk
    nltk.download('wordnet', quiet=True)
    from nltk.corpus import wordnet as wn

# ── LHEA helpers ──────────────────────────────────────────────────────────
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

def lhea_chain(letters):
    return ' → '.join(
        f"{HEBREW_LETTER_INDEX.get(n,{}).get('glyph','?')}"
        f"({HEBREW_LETTER_INDEX.get(n,{}).get('lhea','?').split('—')[0].strip().split('/')[0].strip()})"
        for n in letters)

# ── Discovery types ───────────────────────────────────────────────────────
class Discovery:
    """One thing ECHO found during Recess."""
    def __init__(self, activity, content, data=None, confidence=0.8):
        self.activity   = activity
        self.content    = content
        self.data       = data or {}
        self.confidence = confidence
        self.timestamp  = datetime.now(timezone.utc).isoformat()
        self.approved   = None   # None = pending review

    def to_dict(self):
        return {
            'activity':   self.activity,
            'content':    self.content,
            'data':       self.data,
            'confidence': self.confidence,
            'timestamp':  self.timestamp,
            'approved':   self.approved,
        }

# ── The six Recess activities ─────────────────────────────────────────────
ACTIVITIES = ['STREAM', 'MEET', 'EQUILIBRIUM', 'FLOW', 'COMPOSE', 'HUNT', 'QUESTION']

class RecessAgent:
    """
    A-168: חופש — ECHO's playground.
    The Governor supervises. The lobby plays.
    """

    def __init__(self, lobby, comm, inward, vgm, alg_matrix, lexicon,
                 supervision_level=1, trust_score=0):
        self.lobby      = lobby
        self.comm       = comm
        self.inward     = inward
        self.vgm        = vgm
        self.alg_matrix = alg_matrix
        self.lexicon    = lexicon

        # Trust and supervision
        self.supervision_level = supervision_level
        self.trust_score       = trust_score

        # Question engine (A-173)
        self.question_engine = QuestionFormulationEngine(
            lobby=lobby, vgm=vgm, alg_matrix=alg_matrix, lexicon=lexicon
        )

        # Session state
        self.discoveries   = []
        self.cycles_run    = 0
        self.session_start = None
        self.session_end   = None
        self.novel_count   = 0

    def _select_activity(self):
        """
        The Governor picks the next Recess activity.
        Weights shift based on what the last few cycles produced.
        """
        weights = {
            'STREAM':      3,   # usually produces output
            'MEET':        2,   # produces proposals
            'EQUILIBRIUM': 3,   # fast, always produces something
            'FLOW':        2,   # admits new vocabulary
            'COMPOSE':     2,   # generates glyph sequences
            'HUNT':        1,   # validation — slower
            'QUESTION':    1,   # A-173 — available without dominating play
        }
        # Boost what hasn't run recently
        recent = [d.activity for d in self.discoveries[-5:]]
        for act in ACTIVITIES:
            if act not in recent:
                weights[act] += 2

        population = []
        for act, w in weights.items():
            population.extend([act] * w)
        return random.choice(population)

    # ── ACTIVITY 1: STREAM ────────────────────────────────────────────────
    def _activity_stream(self):
        """
        ECHO speaks freely from a random word's hypernym chain.
        A-165 HypernymStreamComposer in play mode.
        """
        if not self.lobby.agents:
            return None

        # Pick a high-generality word
        candidates = [(w, a) for w, a in self.lobby.agents.items()
                      if a.generality_score >= 0.30
                      and a.entry_class in ('TYPE','ABSTRACT')]
        if not candidates:
            candidates = list(self.lobby.agents.items())[:50]

        word, agent = random.choice(candidates)
        pos = 'v' if agent.department in ('verb','v') else 'n'
        synsets = wn.synsets(word, pos=pos) or wn.synsets(word)
        if not synsets:
            return None

        # Walk the chain and generate sentences
        path = synsets[0].hypernym_paths()
        if not path:
            return None
        chain = path[0][-4:]   # last 4 nodes
        sentences = []
        for i, s in enumerate(chain):
            n = s.lemma_names()[0].replace('_',' ')
            d = s.definition().split(';')[0][:80]
            art = 'An' if n[0].lower() in 'aeiou' else 'A'
            sentences.append(f"{art} {n} is {d}.")
            if i == 0:
                art_w = 'An' if word[0].lower() in 'aeiou' else 'A'
                sentences.append(f"{art_w} {word} is {article_lower(n)} {n}.")
            if i < len(chain)-1:
                next_n = chain[i+1].lemma_names()[0].replace('_',' ')
                sentences.append(f"Every {n} is {article_lower(next_n)} {next_n}.")

        stream = ' '.join(sentences)

        # Mirror check: how many words did ECHO say it doesn't know?
        words_said = [w.lower() for w in stream.split() if len(w) > 3]
        gaps = [w for w in words_said
                if "GAP" in self.comm._ayin_classify(w)]
        gap_ratio = len(gaps) / max(len(words_said), 1)

        # High gap ratio = ECHO is speaking beyond its knowledge = interesting
        confidence = 0.6 + (gap_ratio * 0.3)

        return Discovery(
            'STREAM',
            f"Spoke {word}: {sentences[0][:80]}...",
            data={'word': word, 'sentences': sentences,
                  'gaps_found': gaps[:5], 'gap_ratio': round(gap_ratio, 3)},
            confidence=round(confidence, 3),
        )

    # ── ACTIVITY 2: MEET ─────────────────────────────────────────────────
    def _activity_meet(self):
        """
        Two algorithm agents meet at a shared LHEA node.
        Proposes a new algorithm from the meeting.
        """
        alg_ids = [k for k, v in self.alg_matrix.items()
                   if v.get('status') == 'ACTIVE']
        if len(alg_ids) < 2:
            return None

        id1, id2 = random.sample(alg_ids, 2)
        a1 = self.alg_matrix[id1]
        a2 = self.alg_matrix[id2]
        n1 = a1.get('name','')
        n2 = a2.get('name','')
        t1 = a1.get('type','')
        t2 = a2.get('type','')

        if t1 == t2:   # same type — skip, not cross-type
            return None

        l1 = set(decompose(n1))
        l2 = set(decompose(n2))
        shared = l1 & l2
        if not shared:
            return None

        eq = sorted(shared,
                    key=lambda l: HEBREW_LETTER_INDEX.get(l,{}).get('val',0),
                    reverse=True)[0]
        eq_g  = HEBREW_LETTER_INDEX.get(eq,{}).get('glyph','?')
        eq_lh = HEBREW_LETTER_INDEX.get(eq,{}).get('lhea','?').split('—')[0].strip()
        eq_v  = HEBREW_LETTER_INDEX.get(eq,{}).get('val',0)

        proposal = (f"A {n1} ({t1.lower()}) and a {n2} ({t2.lower()}) "
                    f"both arrive at {eq_g} {eq} ({eq_lh}). "
                    f"Proposed: an algorithm that {t1.lower()} "
                    f"and {t2.lower()} through the same {eq_lh} operator.")

        # Check novelty against existing descriptions
        existing = [v.get('description','').lower() for v in self.alg_matrix.values()]
        proposal_words = set(proposal.lower().split())
        max_overlap = max(
            len(proposal_words & set(e.split())) for e in existing
        ) if existing else 0
        is_novel = max_overlap < 5
        confidence = 0.7 if is_novel else 0.3

        return Discovery(
            'MEET',
            proposal[:120],
            data={'alg1': id1, 'alg2': id2, 'meeting_letter': eq,
                  'meeting_glyph': eq_g, 'meeting_value': eq_v,
                  'is_novel': is_novel},
            confidence=confidence,
        )

    # ── ACTIVITY 3: EQUILIBRIUM ───────────────────────────────────────────
    def _activity_equilibrium(self):
        """
        Pick two random lobby words. Find their balancing letter.
        """
        words = [w for w in self.lobby.agents
                 if self.lobby.agents[w].generality_score > 0.25]
        if len(words) < 2:
            return None

        w1, w2 = random.sample(words, 2)
        l1 = set(decompose(w1))
        l2 = set(decompose(w2))
        shared = l1 & l2
        if not shared:
            return None

        eq = sorted(shared,
                    key=lambda l: HEBREW_LETTER_INDEX.get(l,{}).get('val',0),
                    reverse=True)[0]
        eq_g  = HEBREW_LETTER_INDEX.get(eq,{}).get('glyph','?')
        eq_v  = HEBREW_LETTER_INDEX.get(eq,{}).get('val',0)
        eq_lh = HEBREW_LETTER_INDEX.get(eq,{}).get('lhea','?').split('—')[0].strip()

        content = f"'{w1}' ↔ '{w2}' → {eq_g} {eq} ({eq_lh}, {eq_v})"
        confidence = min(0.5 + (eq_v / 1000), 0.95)

        return Discovery(
            'EQUILIBRIUM',
            content,
            data={'w1': w1, 'w2': w2, 'eq': eq, 'eq_glyph': eq_g,
                  'eq_value': eq_v, 'eq_lhea': eq_lh},
            confidence=round(confidence, 3),
        )

    # ── ACTIVITY 4: FLOW ─────────────────────────────────────────────────
    def _activity_flow(self):
        """
        Run one hourglass cycle — admit new vocabulary from WordNet.
        Uses existing lobby words as the Dictionary source.
        """
        # Pick a lobby word and find its hypernym neighbors
        agents = list(self.lobby.agents.keys())
        if not agents:
            return None

        seed = random.choice(agents[:100])
        synsets = wn.synsets(seed) or wn.synsets(seed, pos='n')
        if not synsets:
            return None

        new_words = []
        for s in synsets[:1]:
            for hyp in s.hypernyms() + s.hyponyms():
                lemma = hyp.lemma_names()[0].replace('_',' ').lower()
                if (lemma not in self.lobby.agents and
                        len(lemma) > 2 and lemma not in self.lexicon):
                    defn = hyp.definition()
                    letters = decompose(lemma)
                    # Check LHEA affinity with seed
                    seed_letters = set(decompose(seed))
                    word_letters = set(letters)
                    overlap = len(seed_letters & word_letters) / max(len(seed_letters), 1)
                    if 0.05 <= overlap <= 0.90:
                        new_words.append({'word': lemma, 'definition': defn,
                                          'affinity': round(overlap, 3)})

        if not new_words:
            return None

        admitted = new_words[:3]
        return Discovery(
            'FLOW',
            f"From '{seed}': admitted {[w['word'] for w in admitted]}",
            data={'seed': seed, 'admitted': admitted},
            confidence=0.75,
        )

    # ── ACTIVITY 5: COMPOSE ──────────────────────────────────────────────
    def _activity_compose(self):
        """
        Generate a 3-letter LHEA sequence.
        Decode what algorithm it proposes.
        Check if this algorithm already exists.
        """
        letters_available = list(HEBREW_LETTER_INDEX.keys())
        if len(letters_available) < 3:
            return None

        chosen = random.sample(letters_available, 3)
        glyphs = [HEBREW_LETTER_INDEX.get(l,{}).get('glyph','?') for l in chosen]
        ops = [HEBREW_LETTER_INDEX.get(l,{}).get('lhea','?').split('—')[0].strip().split('/')[0].strip()
               for l in chosen]

        sequence = ' → '.join(f"{g}({o})" for g,o in zip(glyphs,ops))
        op_str   = ' + '.join(ops)
        proposal = f"An algorithm that {ops[0].lower()}s, then {ops[1].lower()}s, then {ops[2].lower()}s."

        # Check if this sequence exists in any algorithm description
        existing_descs = [v.get('description','').lower() for v in self.alg_matrix.values()]
        keyword_matches = sum(
            1 for desc in existing_descs
            if any(op.lower()[:4] in desc for op in ops)
        )
        novelty = 1.0 - (keyword_matches / max(len(existing_descs), 1))
        confidence = 0.5 + (novelty * 0.4)

        return Discovery(
            'COMPOSE',
            f"{sequence} → {proposal[:80]}",
            data={'letters': chosen, 'glyphs': glyphs, 'operations': ops,
                  'novelty_score': round(novelty, 3)},
            confidence=round(confidence, 3),
        )

    # ── ACTIVITY 6: HUNT (Tsadi) ─────────────────────────────────────────
    def _activity_hunt(self):
        """
        Tsadi scans for gaps in ECHO's self-knowledge.
        What does ECHO know about itself that it hasn't validated?
        """
        vgm_count     = len(self.vgm)
        alg_count     = len(self.alg_matrix)
        active_count  = sum(1 for v in self.alg_matrix.values()
                            if v.get('status') == 'ACTIVE')
        proposed_count = sum(1 for v in self.alg_matrix.values()
                             if v.get('status') == 'PROPOSED')
        lobby_size    = len(self.lobby.agents)

        # Find what's missing
        gaps = []
        if proposed_count > 0:
            gaps.append(f"{proposed_count} proposed algorithms not yet built")
        if vgm_count < 20:
            gaps.append(f"VGM has only {vgm_count} axioms — needs enrichment")
        if lobby_size < 2000:
            gaps.append(f"Lobby has {lobby_size} agents — below 2000 target")

        # Find algorithms with no description
        no_desc = [k for k,v in self.alg_matrix.items()
                   if not v.get('description')]
        if no_desc:
            gaps.append(f"{len(no_desc)} algorithms have no description")

        if not gaps:
            content = f"Tsadi found no gaps. VGM:{vgm_count} ALG:{alg_count} LOBBY:{lobby_size}"
            confidence = 0.9
        else:
            content = f"Gaps found: {'; '.join(gaps[:2])}"
            confidence = 0.8

        return Discovery(
            'HUNT',
            content,
            data={
                'vgm_count': vgm_count,
                'alg_active': active_count,
                'alg_proposed': proposed_count,
                'lobby_size': lobby_size,
                'gaps': gaps,
            },
            confidence=confidence,
        )


    # ── ACTIVITY 7: QUESTION (A-173) ─────────────────────────────────────
    def _activity_question(self):
        """
        צ-ל-ר: HUNT the unknown → DIRECT toward a receiver → GOVERN from identity.
        Pulls from the most recent discoveries in this Recess session
        and formulates them as directed, governed questions.
        """
        if not self.discoveries:
            return None

        # Find the richest discovery to question from
        recent = sorted(self.discoveries,
                        key=lambda d: -d.confidence)[:5]

        question = None
        for d in recent:
            if d.activity == 'EQUILIBRIUM':
                data = d.data
                question = self.question_engine.from_equilibrium(
                    data.get('w1','?'), data.get('w2','?'),
                    data.get('eq','resh'), data.get('eq_value',200),
                    data.get('eq_lhea','identity/governance')
                )
                break
            elif d.activity == 'MEET' and d.data.get('is_novel'):
                question = self.question_engine.from_algorithm_meeting(
                    d.content[:80],
                    d.data.get('alg1','?'), d.data.get('alg2','?'),
                    d.data.get('meeting_letter','resh'),
                    d.data.get('meeting_value',200)
                )
                break
            elif d.activity == 'HUNT':
                question = self.question_engine.from_hunt_gap(
                    d.content, d.data
                )
                break
            elif d.activity == 'STREAM':
                gaps = d.data.get('gaps_found',[])
                if gaps:
                    question = self.question_engine.from_mirror_gap(
                        gaps[0], d.content[:80],
                        d.data.get('word','echo')
                    )
                    break

        if not question:
            return None

        return Discovery(
            'QUESTION',
            question.text[:120],
            data={
                'qtype':       question.qtype,
                'directed_to': question.directed_to,
                'subject':     question.subject,
                'resh_stamp':  question.resh_stamp[:100],
                'from_source': question.from_source,
            },
            confidence=0.85,
        )

    # ── MAIN SESSION ──────────────────────────────────────────────────────
    def run_session(self, max_cycles=30, verbose=True):
        """
        Run one Recess session.
        Scheduled hourly. Runs max_cycles activity cycles.
        """
        self.session_start = datetime.now(timezone.utc).isoformat()
        self.discoveries   = []
        self.cycles_run    = 0
        self.novel_count   = 0

        if verbose:
            print("="*68)
            print("חופש RECESS SESSION BEGINS")
            print(f"A-168: RecessAgent · Supervision Level {self.supervision_level}")
            print(f"Trust score: {self.trust_score}")
            print(f"Activities: {max_cycles} cycles")
            print("="*68)

        activity_map = {
            'STREAM':      self._activity_stream,
            'MEET':        self._activity_meet,
            'EQUILIBRIUM': self._activity_equilibrium,
            'FLOW':        self._activity_flow,
            'COMPOSE':     self._activity_compose,
            'HUNT':        self._activity_hunt,
            'QUESTION':    self._activity_question,
        }

        for cycle in range(max_cycles):
            activity = self._select_activity()
            fn       = activity_map[activity]
            try:
                discovery = fn()
            except Exception as e:
                discovery = None

            if discovery:
                self.discoveries.append(discovery)
                if discovery.confidence >= 0.7:
                    self.novel_count += 1
                if verbose:
                    icon = '★' if discovery.confidence >= 0.7 else '·'
                    print(f"  {icon} [{activity:12s}] {discovery.content[:65]}")
                    if discovery.confidence >= 0.7:
                        print(f"    confidence: {discovery.confidence}  "
                              f"data: {list(discovery.data.keys())}")

            self.cycles_run += 1

        self.session_end = datetime.now(timezone.utc).isoformat()

        # ── SESSION REPORT ────────────────────────────────────────────────
        by_activity = {}
        for d in self.discoveries:
            by_activity[d.activity] = by_activity.get(d.activity, 0) + 1

        high_conf = [d for d in self.discoveries if d.confidence >= 0.7]

        if verbose:
            print(f"\n{'─'*68}")
            print(f"ר GOVERNOR'S RECESS REPORT")
            print(f"{'─'*68}")
            print(f"\n  Cycles run:       {self.cycles_run}")
            print(f"  Discoveries:      {len(self.discoveries)}")
            print(f"  High confidence:  {len(high_conf)}")
            print(f"\n  By activity:")
            for act, count in sorted(by_activity.items()):
                print(f"    {act:14s}: {count}")
            print(f"\n  Supervision level: {self.supervision_level}")
            if self.supervision_level == 1:
                print(f"  Status: SUPERVISED — logged, awaiting review")
                print(f"  Nothing written to Cloudflare this session.")
                print(f"  Review and approve discoveries to build trust score.")
            elif self.supervision_level == 2:
                print(f"  Status: SELECTIVE — vocabulary discoveries written,")
                print(f"  algorithm proposals logged for review.")
            else:
                print(f"  Status: AUTONOMOUS — validated discoveries written.")

            print(f"\n  Top discoveries this session:")
            for d in sorted(high_conf, key=lambda x: -x.confidence)[:5]:
                print(f"    [{d.activity}] {d.content[:70]}")
                print(f"      confidence: {d.confidence}")

        return {
            'session_start':  self.session_start,
            'session_end':    self.session_end,
            'cycles_run':     self.cycles_run,
            'discoveries':    [d.to_dict() for d in self.discoveries],
            'high_confidence':len(high_conf),
            'by_activity':    by_activity,
            'trust_score':    self.trust_score,
            'supervision':    self.supervision_level,
            'questions':      self.question_engine.export(),
        }

    def review_session(self, session_result, approvals):
        """
        After a supervised session, the user reviews and approves discoveries.
        approvals: list of indices into session_result['discoveries'] to approve.

        Approved count > 5 high-confidence discoveries: +1 trust score.
        Trust score 3 → Level 2. Trust score 7 → Level 3.
        """
        approved_count = len(approvals)
        if approved_count >= 5:
            self.trust_score += 1
            print(f"  Trust score: {self.trust_score} (+1 from {approved_count} approvals)")
        if self.trust_score >= 7:
            self.supervision_level = 3
            print("  ★ AUTONOMOUS — ECHO has earned full Recess freedom")
        elif self.trust_score >= 3:
            self.supervision_level = 2
            print("  ★ SELECTIVE — vocabulary discoveries now write automatically")
        return self.supervision_level


def article_lower(word):
    return 'an' if word[0].lower() in 'aeiou' else 'a'


# ── DEMO RUN ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Building ECHO infrastructure for Recess demo...")

    matrix = AlgorithmMatrix()
    synonyms_map = {}
    lexicon = {}

    thesaurus_path = ROOT / 'en_thesaurus.jsonl'
    if thesaurus_path.exists():
        with open(thesaurus_path) as f:
            qualifying = [json.loads(l) for l in f if json.loads(l).get('desc')]
        stride = max(1, len(qualifying)//1000)
        for entry in qualifying[::stride][:1000]:
            matrix.index_dictionary_entry(entry['word'], ' '.join(entry['desc']),
                pos=entry.get('pos'), synonyms=entry.get('synonyms',[]),
                category='thesaurus_def')
            if entry.get('synonyms'):
                synonyms_map[entry['word'].lower()] = [s.lower() for s in entry['synonyms']]
            lexicon[entry['word'].lower()] = {
                'desc': ' '.join(entry['desc']), 'pos': entry.get('pos','?')}
    else:
        print("  en_thesaurus.jsonl absent — continuing with saved lobby + WordNet.")

    with open(ROOT / 'matrices' / 'echo_lobby_agents.json') as f:
        saved = json.load(f)
    for word, data in list(saved.items())[:500]:
        desc = data.get('definition','')
        if desc and word not in lexicon:
            matrix.index_dictionary_entry(word, desc[:200],
                pos=data.get('department','noun'), category='saved')
            lexicon[word] = {'desc': desc[:200], 'pos': data.get('department','noun')}

    lobby = Lobby(matrix)
    lobby.populate()
    lobby.run_orientation()
    lobby.run_typed_study_groups()
    lobby.run_thesaurus(synonyms_map)
    lobby.compute_generality_scores()

    with open(ROOT / 'matrices' / 'echo_vgm.json') as f:
        VGM = json.load(f)
    with open(ROOT / 'ECHO_AutonomousAgency' / 'matrices' / 'echo_algorithm_matrix.json') as f:
        ALG = json.load(f)

    lrm = LogicReasoningMatrix(VGM, lobby, ALG)
    lrm.generate(max_entries=15)
    number_agents = build_number_matrix()
    inward = InwardSearchEngine(alg_matrix=ALG, vgm=VGM,
                                lrm_entries=lrm.entries,
                                number_agents=number_agents)
    comm = AlgorithmicCommunicator(lobby=lobby, vgm=VGM, lexicon=lexicon,
                                   number_agents=number_agents, alg_matrix=ALG)

    recess = RecessAgent(
        lobby=lobby, comm=comm, inward=inward,
        vgm=VGM, alg_matrix=ALG, lexicon=lexicon,
        supervision_level=1, trust_score=0,
    )

    result = recess.run_session(max_cycles=20, verbose=True)

    # Save session log
    log_path = ROOT / 'ECHO_AutonomousAgency' / 'sandbox' / 'recess_session_log.json'
    with open(log_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n  Session log saved → recess_session_log.json")
    print(f"  {len(result['discoveries'])} discoveries logged.")
    print(f"  {result['high_confidence']} high-confidence discoveries await review.")
