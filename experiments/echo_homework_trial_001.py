"""Initial ECHO Homework Trial 001.

Dictionary-only trial. No Classroom benchmark content or answer keys.
The trial reads only instantiated Lobby words and uses dictionary evidence to
exercise the Mirror comprehension-governance path.
"""
from src.echo_homework import HomeworkGovernor
from src.echo_dictionary import EchoDictionary
from src.echo_comprehension_audit import MirrorComprehensionAudit

SEEDS=["water","fire","sun","earth","eye","ear","hand","foot",
       "eat","drink","see","hear","go","come","big","small","good","bad"]

g=HomeworkGovernor(SEEDS,max_turns=100,max_new_words_per_turn=3)
d=EchoDictionary(g)
m=MirrorComprehensionAudit(g)

print("# ECHO INITIAL HOMEWORK TRIAL 001")
print("Initial Lobby:", sorted(g.lobby))
print("Initial Lobby size:",len(g.lobby))

# A first small study sample. Scores below are mechanically derived diagnostics
# from available lexical structure; they are NOT self-reported confidence.
for word in ("water","fire","eye","eat","good"):
    result=d.study(word)
    sense=result["sense"]
    if not sense:
        rec=rel=coh=trans=0.0
    else:
        rec=1.0
        rel=min(1.0,(len(sense["lemmas"])+len(sense["hypernyms"]))/4)
        # Coherence proxy: definition exists and lexical relations are present.
        coh=(0.5 if sense["definition"] else 0)+(0.5 if sense["hypernyms"] else 0)
        # Transfer is intentionally zero until an independent unseen probe exists.
        trans=0.0
    record=m.audit(word,recall=rec,relations=rel,coherence=coh,transfer=trans)
    print("\nWORD:",word)
    print("SYNSET:",sense["synset"] if sense else None)
    print("DEFINITION:",sense["definition"] if sense else None)
    print("CANDIDATES:",result["candidates"])
    print("MIRROR:",record.state,round(record.score,3))

print("\nAudited coverage:",round(m.coverage(),3))
print("Mirror next action:",m.next_action())
print("Turns spent:",g.turn)
print("Lobby size:",len(g.lobby))
print("Candidate frontier:",len(g.candidates))
print("STATUS: HOMEWORK_TRIAL_001_EXECUTED")
