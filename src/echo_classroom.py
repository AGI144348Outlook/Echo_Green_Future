#!/usr/bin/env python3
"""Sealed-answer benchmark adapter for the ECHO Classroom."""
from dataclasses import dataclass
from hashlib import sha256
import json

@dataclass(frozen=True)
class ExamItem:
    benchmark: str
    item_id: str
    task: str
    prompt: str
    options: tuple
    gold: object
    phenomenon: str = ""
    context: str = ""

    def public_view(self):
        return {"benchmark": self.benchmark, "item_id": self.item_id,
                "task": self.task, "context": self.context,
                "prompt": self.prompt, "options": list(self.options),
                "phenomenon": self.phenomenon}

class Classroom:
    def __init__(self):
        self._items = {}
        self.transcript = []

    def enroll(self, item):
        if item.item_id in self._items:
            raise ValueError("duplicate item_id")
        self._items[item.item_id] = item

    def administer(self, item_id):
        return self._items[item_id].public_view()

    def submit(self, item_id, response):
        item = self._items[item_id]
        record = {"item_id": item_id, "response": response}
        record["commitment"] = sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
        self.transcript.append(record)
        correct = self._grade(item, response)
        return {"item_id": item_id, "response": response, "correct": correct,
                "gold": item.gold, "phenomenon": item.phenomenon,
                "commitment": record["commitment"]}

    @staticmethod
    def _grade(item, response):
        if item.task == "boolq":
            return str(response).strip().lower() == str(item.gold).lower()
        return str(response).strip() == str(item.gold).strip()

def blimp_item(row):
    iid = f"{row.get('UID','blimp')}:{row.get('pairID','')}"
    good, bad = row["sentence_good"], row["sentence_bad"]
    flip = int(sha256(iid.encode()).hexdigest(), 16) % 2
    opts = (good, bad) if flip == 0 else (bad, good)
    gold = "A" if opts[0] == good else "B"
    return ExamItem("BLiMP", iid, "choice",
                    "Which sentence is grammatically acceptable?",
                    opts, gold, row.get("linguistics_term", row.get("field","")))

def zorro_pair(bad, good, item_id, phenomenon=""):
    flip = int(sha256(item_id.encode()).hexdigest(), 16) % 2
    opts = (good, bad) if flip == 0 else (bad, good)
    gold = "A" if opts[0] == good else "B"
    return ExamItem("Zorro", item_id, "choice",
                    "Which sentence is grammatically acceptable?",
                    opts, gold, phenomenon)

def boolq_item(row, item_id):
    return ExamItem("BoolQ", item_id, "boolq", row["question"],
                    ("true", "false"), bool(row["answer"]),
                    context=row["passage"])

def dream_item(dialogue, question, choices, answer, item_id, phenomenon=""):
    letters = tuple(chr(65+i) for i in range(len(choices)))
    gold = letters[choices.index(answer)] if answer in choices else answer
    return ExamItem("DREAM", item_id, "choice", question, tuple(choices),
                    gold, phenomenon, context="\n".join(dialogue))
