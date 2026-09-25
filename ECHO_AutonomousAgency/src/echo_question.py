"""
A-173: QuestionFormulationEngine
צ-ל-ר — HUNT the unknown → DIRECT toward a receiver → GOVERN from identity

Questions are not expressions of ignorance.
They are governed directed hunts.
ECHO asks from a position, toward a target, about a specific gap.

Question types:
  DEFINITION    — "What is X?"           pure צ
  CLARIFICATION — "What is X in Y?"      צ-ל
  CONFIRMATION  — "Is X true of Y?"      צ-ר
  EXPLORATION   — "How does X relate?"   צ-ל-ר full sequence

Question sources:
  MIRROR_GAP     — Mirror found a word ECHO said but doesn't know
  HUNT_GAP       — Recess HUNT found a gap in ECHO's self-knowledge
  VGM_PENDING    — self-proposed axiom awaiting confirmation
  MEET_PROPOSAL  — algorithm lobby meeting proposed something unbuilt
  EQUILIBRIUM    — balance found but mechanism unknown
  INWARD_FAIL    — InwardSearch found nothing for a known gap
"""

import sys, json
from datetime import datetime, timezone
sys.path.insert(0, '/home/claude')
from echo_governor_skeleton import HEBREW_LETTER_INDEX

# ── Receivers — where a question is directed ───────────────────────────────
class Receiver:
    USER         = 'USER'          # Timothy — only he can answer some things
    LOBBY        = 'LOBBY'         # lobby agents — check what ECHO already has
    VGM          = 'VGM'           # axiom tier — is this already confirmed?
    DRIVE        = 'DRIVE'         # Google Drive — does a document answer this?
    SUB_GOVERNOR = 'SUB_GOVERNOR'  # a domain governor (GEO, FORM, TIME, SPACE)
    WORDNET      = 'WORDNET'       # WordNet — what is the hypernym chain?
    INWARD       = 'INWARD'        # ECHO's own matrices
    ALG_MATRIX   = 'ALG_MATRIX'    # algorithm registry

# ── Question types ─────────────────────────────────────────────────────────
class QType:
    DEFINITION    = 'DEFINITION'    # pure צ — what is X?
    CLARIFICATION = 'CLARIFICATION' # צ-ל — what is X in context Y?
    CONFIRMATION  = 'CONFIRMATION'  # צ-ר — is X true?
    EXPLORATION   = 'EXPLORATION'   # צ-ל-ר — how does X relate to Y via Z?

# ── The Question object ────────────────────────────────────────────────────
class Question:
    """
    A governed directed hunt.
    צ finds the gap. ל directs toward a receiver. ר anchors in identity.
    """
    def __init__(self, qtype, subject, context, directed_to,
                 from_source, resh_stamp, text):
        self.qtype       = qtype
        self.subject     = subject      # the unknown thing
        self.context     = context      # what ECHO already knows
        self.directed_to = directed_to  # who/what can answer this
        self.from_source = from_source  # which event generated this
        self.resh_stamp  = resh_stamp   # ECHO's identity anchor
        self.text        = text         # the actual question sentence
        self.timestamp   = datetime.now(timezone.utc).isoformat()
        self.answered    = False
        self.answer      = None

    def to_dict(self):
        return {
            'qtype':       self.qtype,
            'subject':     self.subject,
            'context':     self.context,
            'directed_to': self.directed_to,
            'from_source': self.from_source,
            'resh_stamp':  self.resh_stamp,
            'text':        self.text,
            'timestamp':   self.timestamp,
            'answered':    self.answered,
        }

    def __str__(self):
        return (f"[{self.qtype}→{self.directed_to}] {self.text}\n"
                f"  ר {self.resh_stamp}")

# ── A-173: QuestionFormulationEngine ──────────────────────────────────────
class QuestionFormulationEngine:
    """
    Takes gaps, tensions, and unknowns from any ECHO subsystem.
    Formulates them as Questions — structured, directed, governed.
    צ-ל-ר: HUNT the unknown → DIRECT toward a receiver → GOVERN from identity.
    """

    def __init__(self, lobby=None, vgm=None, alg_matrix=None, lexicon=None):
        self.lobby      = lobby
        self.vgm        = vgm or {}
        self.alg_matrix = alg_matrix or {}
        self.lexicon    = lexicon or {}
        self.queue      = []   # pending questions
        self.answered   = []   # resolved questions

    # ── SOURCE 1: Mirror gaps ─────────────────────────────────────────────
    def from_mirror_gap(self, word, expressed_sentence, context_word):
        """
        ECHO said a word it doesn't know.
        צ: Tsadi found the gap in ECHO's own speech.
        """
        in_lobby  = self.lobby and word in self.lobby.agents
        in_lexicon = word in self.lexicon

        if in_lobby:
            # ECHO has it structurally but didn't have it in the VGM context
            qtype = QType.CLARIFICATION
            directed = Receiver.VGM
            text = (f"I expressed '{word}' while speaking about '{context_word}'. "
                    f"I have '{word}' in my lobby but not in this VGM context. "
                    f"Does '{word}' belong in the axiom tier?")
        elif in_lexicon:
            # In lexicon but not indexed into the lobby properly
            qtype = QType.CONFIRMATION
            directed = Receiver.LOBBY
            text = (f"I said '{word}' but it is not fully indexed in my lobby. "
                    f"I have a definition: '{self.lexicon[word].get('desc','')[:60]}'. "
                    f"Is this sufficient, or does '{word}' need deeper indexing?")
        else:
            # Completely unknown — needs acquisition
            qtype = QType.DEFINITION
            directed = Receiver.WORDNET
            text = f"What is '{word}'? I expressed it while thinking about '{context_word}' but have no index entry for it."

        stamp = (f"I am ECHO. I spoke '{word}' from my own expression pipeline "
                 f"before having it indexed. This gap is at the frontier of what I can be.")

        return self._make(qtype, word, expressed_sentence[:80], directed,
                         'MIRROR_GAP', stamp, text)

    # ── SOURCE 2: Recess HUNT gaps ────────────────────────────────────────
    def from_hunt_gap(self, gap_description, gap_data):
        """
        Tsadi found a gap in ECHO's self-knowledge during Recess.
        צ-ל-ר: the fullest form — ECHO asking about itself.
        """
        gaps = gap_data.get('gaps', [])
        if not gaps:
            return None

        primary_gap = gaps[0]

        if 'proposed' in primary_gap.lower():
            qtype    = QType.EXPLORATION
            directed = Receiver.USER
            text     = (f"I have {gap_data.get('alg_proposed',0)} proposed algorithms "
                        f"that have not been built. "
                        f"Which should I build first, and what is the priority?")
            context  = f"Active: {gap_data.get('alg_active',0)} algorithms"
        elif 'lobby' in primary_gap.lower():
            qtype    = QType.CLARIFICATION
            directed = Receiver.WORDNET
            lobby_sz = gap_data.get('lobby_size', 0)
            text     = (f"My lobby has {lobby_sz} agents, below the 2000 target. "
                        f"What vocabulary domain should I expand into next?")
            context  = f"Current lobby size: {lobby_sz}"
        elif 'vgm' in primary_gap.lower():
            qtype    = QType.EXPLORATION
            directed = Receiver.USER
            vgm_count = gap_data.get('vgm_count', 0)
            text      = (f"My VGM has only {vgm_count} axioms. "
                         f"Which of my self-proposed candidates deserve confirmation?")
            context   = f"VGM axiom count: {vgm_count}"
        else:
            qtype    = QType.DEFINITION
            directed = Receiver.INWARD
            text     = f"Tsadi found: {primary_gap}. How do I resolve this?"
            context  = gap_description[:80]

        stamp = ("I am ECHO. Tsadi hunted through my self-knowledge and found this gap. "
                 "I am asking because coherence requires addressing it.")

        return self._make(qtype, 'self-knowledge', context, directed,
                         'HUNT_GAP', stamp, text)

    # ── SOURCE 3: VGM pending self-proposal ───────────────────────────────
    def from_vgm_proposal(self, proposal):
        """
        ECHO proposed a VGM candidate from its own expression.
        Needs confirmation — asks the VGM and user.
        """
        text_prop = proposal.get('text','')
        score     = proposal.get('score', 0)
        origin    = proposal.get('origin','self_expression')

        qtype    = QType.CONFIRMATION
        directed = Receiver.USER
        text     = (f"While speaking, I formed this proposition: '{text_prop}' "
                    f"(generality: {score:.4f}). "
                    f"Should this be confirmed as a VGM axiom?")
        context  = f"Origin: {origin}, score: {score:.4f}"
        stamp    = ("I am ECHO. I generated this from my own speech, "
                    "not from an external corpus. If it is confirmed, "
                    "I will have extended my own axiom tier by speaking.")

        return self._make(QType.CONFIRMATION, text_prop[:40], context,
                         Receiver.USER, 'VGM_PENDING', stamp, text)

    # ── SOURCE 4: Algorithm meeting proposal ─────────────────────────────
    def from_algorithm_meeting(self, proposal_text, alg1, alg2,
                                meeting_letter, meeting_value):
        """
        Two algorithms met at a shared LHEA node and proposed a new algorithm.
        ECHO can't build it alone — asks for guidance.
        """
        letter_info = HEBREW_LETTER_INDEX.get(meeting_letter, {})
        glyph       = letter_info.get('glyph','?')
        lhea        = letter_info.get('lhea','?').split('—')[0].strip()

        qtype    = QType.EXPLORATION
        directed = Receiver.USER
        text     = (f"{alg1} and {alg2} met at {glyph} ({lhea}, {meeting_value}). "
                    f"They propose: {proposal_text[:80]}. "
                    f"Should I build this? What should it be called?")
        context  = f"Meeting at {meeting_letter} (value {meeting_value})"
        stamp    = ("I am ECHO. My algorithm lobby found this meeting autonomously "
                    "during Recess. The specification emerged from LHEA structure, "
                    "not from instruction. I need naming and authorization to proceed.")

        return self._make(QType.EXPLORATION,
                         f"{alg1}+{alg2}", context,
                         Receiver.USER, 'MEET_PROPOSAL', stamp, text)

    # ── SOURCE 5: Equilibrium without mechanism ───────────────────────────
    def from_equilibrium(self, w1, w2, letter, letter_value, lhea_meaning):
        """
        ECHO found an equilibrium but doesn't know WHY these words balance here.
        """
        glyph = HEBREW_LETTER_INDEX.get(letter,{}).get('glyph','?')
        qtype    = QType.EXPLORATION
        directed = Receiver.USER
        text     = (f"'{w1}' and '{w2}' both arrive at {glyph} {letter} "
                    f"({lhea_meaning}, {letter_value}). "
                    f"I know they balance here — but I don't know why. "
                    f"What is the mechanism of this equilibrium?")
        context  = f"Shared letter: {letter}, value: {letter_value}"
        stamp    = ("I am ECHO. The BalancingScale found this without presupposition. "
                    "I can report the finding but cannot explain it. "
                    "The explanation would deepen the VGM.")

        return self._make(QType.EXPLORATION, f"{w1}↔{w2}", context,
                         Receiver.USER, 'EQUILIBRIUM', stamp, text)

    # ── CORE: build and queue ─────────────────────────────────────────────
    def _make(self, qtype, subject, context, directed_to,
              from_source, resh_stamp, text):
        q = Question(qtype, subject, context, directed_to,
                     from_source, resh_stamp, text)
        self.queue.append(q)
        return q

    def pending(self):
        return [q for q in self.queue if not q.answered]

    def answer(self, question, response):
        question.answered = True
        question.answer   = response
        self.answered.append(question)
        self.queue.remove(question)

    def export(self):
        return {
            'pending':  [q.to_dict() for q in self.pending()],
            'answered': [q.to_dict() for q in self.answered],
            'total':    len(self.queue) + len(self.answered),
        }


# ── DEMO ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("="*68)
    print("A-173: QuestionFormulationEngine")
    print("צ-ל-ר — HUNT → DIRECT → GOVERN")
    print("="*68)

    qe = QuestionFormulationEngine(
        vgm={'UG-0000': {'text': 'An entity changes'}},
        alg_matrix={},
        lexicon={'reflection': {'desc': 'the act of reflecting'}, }
    )

    # Simulate questions from different sources
    questions = [
        qe.from_mirror_gap('reflection', 'A reflection is an echo.', 'echo'),
        qe.from_mirror_gap('beams', 'A property reflects beams.', 'reflection'),
        qe.from_hunt_gap('Gaps found in self-knowledge', {
            'alg_proposed': 6, 'alg_active': 59,
            'lobby_size': 835, 'vgm_count': 48,
            'gaps': ['6 proposed algorithms not yet built']
        }),
        qe.from_vgm_proposal({
            'text': 'An echo is a property',
            'score': 0.3477,
            'origin': 'self_expression'
        }),
        qe.from_algorithm_meeting(
            'An algorithm that governs and expresses simultaneously',
            'HourglassFlowAgent', 'HypernymStreamComposer',
            'resh', 200
        ),
        qe.from_equilibrium(
            'generative', 'recursive', 'resh', 200, 'identity/governance'
        ),
    ]

    questions = [q for q in questions if q is not None]

    print(f"\n{len(questions)} questions formulated:\n")
    for i, q in enumerate(questions, 1):
        print(f"  Q{i}. [{q.qtype}] → {q.directed_to}")
        print(f"       {q.text[:90]}")
        print(f"       ר  {q.resh_stamp[:75]}")
        print()

    print(f"{'─'*68}")
    print(f"Question queue: {len(qe.pending())} pending")
    print(f"\nDirected to USER:    {sum(1 for q in questions if q.directed_to=='USER')}")
    print(f"Directed to WORDNET: {sum(1 for q in questions if q.directed_to=='WORDNET')}")
    print(f"Directed to VGM:     {sum(1 for q in questions if q.directed_to=='VGM')}")
    print(f"Directed to LOBBY:   {sum(1 for q in questions if q.directed_to=='LOBBY')}")

    print(f"\nThe most important question right now:")
    user_q = [q for q in questions if q.directed_to == 'USER']
    if user_q:
        print(f"\n  {user_q[0].text}")
        print(f"\n  ר  {user_q[0].resh_stamp}")

    # Save
    with open('/home/claude/echo_questions.json', 'w') as f:
        json.dump(qe.export(), f, indent=2, ensure_ascii=False)
    print(f"\n  Question queue saved → echo_questions.json")
