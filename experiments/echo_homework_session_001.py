"""ECHO Homework Session 001 — canonical starting state + first dictionary study."""

import json
from hashlib import sha256
from pathlib import Path

from src.echo_homework import HomeworkGovernor
from src.echo_dictionary import EchoDictionary
from src.echo_homework_audit import HomeworkAudit

# Small basic-child/basic-concept Lobby. Freeze before any dictionary study.
SEEDS = [
    "I","you","we","this","that","who","what","one","two",
    "person","mother","father","child","man","woman",
    "dog","bird","fish","tree","seed","water","fire","sun","moon","earth",
    "head","eye","ear","nose","mouth","hand","foot","heart","blood",
    "eat","drink","see","hear","sleep","walk","come","go","give","take",
    "big","small","good","bad","hot","cold","red","black","white",
    "here","there","not"
]

governor = HomeworkGovernor(SEEDS, max_turns=100, max_new_words_per_turn=3)
audit = HomeworkAudit()
for word in sorted(governor.lobby):
    audit.record_seed(word)

start = governor.snapshot()
start_json = json.dumps(start, sort_keys=True)
print("# ECHO Homework Session 001")
print("Initial Lobby size:", len(start["lobby"]))
print("Initial Lobby SHA256:", sha256(start_json.encode()).hexdigest())
print("Study budget:", governor.max_turns)
print("Max new words per instantiation:", governor.max_new_words_per_turn)

dictionary = EchoDictionary(governor)

# First permitted dictionary encounter. No candidate is automatically admitted.
result = dictionary.study("water")
audit.record_definition(
    "water",
    result["sense"]["definition"] if result["sense"] else "",
    result["candidates"],
)

print("\nFirst study word: water")
print("Sense:", result["sense"]["synset"] if result["sense"] else None)
print("Definition:", result["sense"]["definition"] if result["sense"] else None)
print("Candidates discovered:", result["candidates"])
print("Lobby size after reading:", len(governor.lobby))
print("Candidate frontier size:", len(governor.candidates))
print("Turns spent:", governor.turn)
print("\nNo candidates admitted automatically.")
print("STATUS: HOMEWORK_SESSION_001_STARTED")
