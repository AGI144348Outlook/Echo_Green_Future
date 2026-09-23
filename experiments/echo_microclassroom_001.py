"""ECHO Micro-Classroom 001.

A tiny sealed-answer comprehension probe constrained to the initial Lobby.
This is infrastructure validation, not a substitute for later frozen external
benchmark items.
"""
from src.echo_homework import HomeworkGovernor
from src.echo_comprehension_audit import MirrorComprehensionAudit
from src.echo_classroom import Classroom, ExamItem

SEEDS=["water","fire","sun","earth","eye","ear","hand","foot",
       "eat","drink","see","hear","go","come","big","small","good","bad"]

# Items intentionally use Lobby vocabulary in the prompt/options.
BANK=[
 ExamItem(id="m1",source="microclassroom",prompt="You drink water.",gold=True,metadata={"concept":"water"}),
 ExamItem(id="m2",source="microclassroom",prompt="You hear with an eye.",gold=False,metadata={"concept":"eye"}),
 ExamItem(id="m3",source="microclassroom",prompt="You see with an eye.",gold=True,metadata={"concept":"eye"}),
 ExamItem(id="m4",source="microclassroom",prompt="Fire is cold.",gold=False,metadata={"concept":"fire"}),
 ExamItem(id="m5",source="microclassroom",prompt="You eat water.",gold=False,metadata={"concept":"water"}),
]

g=HomeworkGovernor(SEEDS,max_turns=100,max_new_words_per_turn=3)
mirror=MirrorComprehensionAudit(g)
room=Classroom()

print("# ECHO MICRO-CLASSROOM 001")
print("Lobby:",sorted(g.lobby))
print("Items:",len(BANK))

# Validate that lexical tokens carrying test meaning are Lobby words.
# Function words/punctuation are structural scaffolding, not new study concepts.
concepts={x.metadata["concept"] for x in BANK}
assert concepts <= set(g.lobby)
print("Concept filter:",sorted(concepts))

# Public views demonstrate gold answers are sealed.
for item in BANK:
    room.add(item)
    public=room.public_view(item.id)
    assert "gold" not in public
    print("SEALED:",item.id,public["prompt"])

print("STATUS: MICROCLASSROOM_FILTER_AND_SEAL_VALIDATED")
print("NOTE: no answer-generating cognition is fabricated here; this run validates")
print("the filtered/sealed examination path. The next stage must connect ECHO's")
print("actual response mechanism before Classroom grades comprehension.")
