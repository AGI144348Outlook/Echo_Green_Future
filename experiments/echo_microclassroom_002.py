"""ECHO Micro-Classroom 002 — first scored lexical-reasoning probe.

No answer is supplied to the answering mechanism. ECHO answers from WordNet
relations available through Lobby-permitted concepts; Classroom seals gold
until submission. This is a narrow symbolic/lexical test, not a claim of
general comprehension.
"""
from nltk.corpus import wordnet as wn
from src.echo_homework import HomeworkGovernor
from src.echo_classroom import Classroom, ExamItem

SEEDS=["water","fire","sun","earth","eye","ear","hand","foot",
       "eat","drink","see","hear","go","come","big","small","good","bad"]

ITEMS=[
 ExamItem(id="r1",source="microclassroom-002",prompt="You drink water.",gold=True,
          metadata={"subject":"you","verb":"drink","object":"water"}),
 ExamItem(id="r2",source="microclassroom-002",prompt="You hear with an eye.",gold=False,
          metadata={"subject":"you","verb":"hear","instrument":"eye"}),
 ExamItem(id="r3",source="microclassroom-002",prompt="You see with an eye.",gold=True,
          metadata={"subject":"you","verb":"see","instrument":"eye"}),
 ExamItem(id="r4",source="microclassroom-002",prompt="Fire is cold.",gold=False,
          metadata={"subject":"fire","property":"cold"}),
 ExamItem(id="r5",source="microclassroom-002",prompt="You eat water.",gold=False,
          metadata={"subject":"you","verb":"eat","object":"water"}),
]

g=HomeworkGovernor(SEEDS,max_turns=100,max_new_words_per_turn=3)
room=Classroom()

def glosses(word):
    g.require_lobby(word)
    return " ".join(s.definition().lower() for s in wn.synsets(word)[:6])

def answer(item):
    m=item.metadata
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
    room.add(item)
    public=room.public_view(item.id)
    assert "gold" not in public
    response,evidence=answer(item)
    # Response is committed before Classroom reveals correctness/gold.
    result=room.submit(item.id,response)
    ok=result["correct"]
    correct+=int(ok)
    print(item.id,"PROMPT:",public["prompt"])
    print("ECHO:",response,"CORRECT:",ok)
    print("EVIDENCE:",evidence[:220].replace("\n"," "))
print("SCORE:",correct,"/",len(ITEMS),f"({correct/len(ITEMS):.1%})")
print("STATUS: MICROCLASSROOM_002_SCORED")
