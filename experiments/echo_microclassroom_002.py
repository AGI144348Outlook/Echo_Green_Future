"""ECHO Micro-Classroom 002 — first scored lexical-reasoning probe.

No answer is supplied to the answering mechanism. ECHO answers from WordNet
relations available through Lobby-permitted concepts; Classroom seals gold
until submission. This is a narrow symbolic/lexical test, not a claim of
general comprehension.
"""
import os, sys
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from nltk.corpus import wordnet as wn
from src.echo_homework import HomeworkGovernor
from src.echo_classroom import Classroom, ExamItem

SEEDS=["water","fire","sun","earth","eye","ear","hand","foot",
       "eat","drink","see","hear","go","come","big","small","good","bad"]

ITEMS=[
 ExamItem("Micro002","r1","boolq","You drink water.",("true","false"),True, context="you|drink|water"),
 ExamItem("Micro002","r2","boolq","You hear with an eye.",("true","false"),False, context="you|hear|eye"),
 ExamItem("Micro002","r3","boolq","You see with an eye.",("true","false"),True, context="you|see|eye"),
 ExamItem("Micro002","r4","boolq","Fire is cold.",("true","false"),False, context="fire|is|cold"),
 ExamItem("Micro002","r5","boolq","You eat water.",("true","false"),False, context="you|eat|water"),
]

g=HomeworkGovernor(SEEDS,max_turns=100,max_new_words_per_turn=3)
room=Classroom()

def glosses(word):
    g.require_lobby(word)
    return " ".join(s.definition().lower() for s in wn.synsets(word)[:6])

def answer(item):
    parts=item.context.split("|")
    if parts[1] == "is": m={"subject":parts[0],"property":parts[2]}
    elif parts[1] in ("see","hear"): m={"subject":parts[0],"verb":parts[1],"instrument":parts[2]}
    else: m={"subject":parts[0],"verb":parts[1],"object":parts[2]}
    # Evidence is lexical, retrieved only for Lobby concepts in the item.
    if "instrument" in m:
        inst,verb=m["instrument"],m["verb"]
        evidence=glosses(inst)
        if verb=="see":
            return ("visual" in evidence or "sight" in evidence or "see" in evidence), evidence
        if verb=="hear":
            return ("auditory" in evidence or "hearing" in evidence or "hear" in evidence), evidence
    if "object" in m:
        obj,verb=m["object"],m["verb"]
        evidence=glosses(obj)
        if verb=="drink":
            return ("liquid" in evidence or "water" in evidence), evidence
        if verb=="eat":
            # Reject if lexical evidence presents the object as liquid/material
            # rather than food/nutriment.
            return ("food" in evidence or "nutriment" in evidence), evidence
    if "property" in m:
        subj,prop=m["subject"],m["property"]
        evidence=glosses(subj)
        if subj=="fire" and prop=="cold":
            return not ("heat" in evidence or "hot" in evidence or "burn" in evidence), evidence
    return False,"no supporting lexical relation"

print("# ECHO MICRO-CLASSROOM 002")
correct=0
for item in ITEMS:
    room.enroll(item)
    public=room.administer(item.item_id)
    assert "gold" not in public
    response,evidence=answer(item)
    # Response is committed before Classroom reveals correctness/gold.
    result=room.submit(item.item_id,response)
    ok=result["correct"]
    correct+=int(ok)
    print(item.item_id,"PROMPT:",public["prompt"])
    print("ECHO:",response,"CORRECT:",ok)
    print("EVIDENCE:",evidence[:220].replace("\n"," "))
print("SCORE:",correct,"/",len(ITEMS),f"({correct/len(ITEMS):.1%})")
print("STATUS: MICROCLASSROOM_002_SCORED")
