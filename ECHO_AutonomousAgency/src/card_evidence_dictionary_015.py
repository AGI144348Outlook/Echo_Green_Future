#!/usr/bin/env python3
"""Experiment 015: Echo dictionary + upstream CatalogBox + source-linked evidence graph.

Algorithmic, frozen WordNet-chain input. No model calls, no Neon credentials,
no production edits, and no automatic vocabulary admission.
Pre-test plan: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/435

Offline local run:
  DUAL_ORDER_OS_PATH=/path/to/dual-order-os python ECHO_AutonomousAgency/src/card_evidence_dictionary_015.py
"""
import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ECHO_AutonomousAgency" / "src"))
DUAL_ORDER = os.getenv("DUAL_ORDER_OS_PATH")
if not DUAL_ORDER:
    raise RuntimeError("DUAL_ORDER_OS_PATH must point to a pinned Dual Order OS checkout")
sys.path.insert(0, str(Path(DUAL_ORDER) / "libraries"))
from catalog_box import CatalogBox


def load_dictionary(path=None):
    source = Path(path) if path else ROOT / "matrices" / "echo_wordnet_chains.json"
    raw = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not raw:
        raise ValueError("dictionary must be a populated object")
    for word, entry in raw.items():
        if not isinstance(word, str) or not isinstance(entry, dict):
            raise ValueError("dictionary word and entry must be typed")
        chain = entry.get("chain")
        if (not isinstance(chain, list) or not chain or
            any(not isinstance(c, str) or not c.strip() for c in chain)):
            raise ValueError("every dictionary entry needs a nonempty lexical path")
        if not isinstance(entry.get("synset"), str):
            raise ValueError("every entry needs a recorded WordNet synset")
    return raw


def baseline(dictionary, left, right):
    """A-165-style chain intersection, including uninformative root nodes."""
    a, b = dictionary[left]["chain"], dictionary[right]["chain"]
    shared = sorted(set(a) & set(b))
    return {"decision": "associated" if shared else "abstain",
            "shared": shared, "has_source_witness": False}


class EvidenceDictionary:
    """No relation is accepted as empirically verified by this structure."""

    def __init__(self, dictionary, box=None, max_ancestor_frequency=0.25):
        self.data = dictionary
        self.box = box or CatalogBox(":memory:")
        self.cap = max_ancestor_frequency
        self.refs = {}
        self.graph = {}
        self.df = Counter()
        for entry in dictionary.values():
            self.df.update(set(entry["chain"]))
        for word, entry in dictionary.items():
            record = self.box.put_card(
                f"wordnet:{word}", f"Lexical context: {word}",
                {"word": word, "synset": entry["synset"],
                 "definition": entry.get("definition"),
                 "chain": list(entry["chain"]),
                 "epistemic_status": "provisional",
                 "admission_status": "source_observation_only"},
                provenance={"source": "Echo_Green_Future:matrices/echo_wordnet_chains.json",
                            "origin": f"genesis.wordnet_chain:{word}",
                            "source_claim_status": "source_assertion_unverified"},
            )
            self.refs[word] = {"id": record["id"], "revision": record["revision"]}
            path = list(reversed(entry["chain"]))
            self.graph[word] = [
                {"from": word if i == 0 else path[i-1],
                 "to": ancestor, "relation": "lexical_path",
                 "domain": "lexical", "review_state": "proposed",
                 "evidence_card": dict(self.refs[word]),
                 "source": f"genesis.wordnet_chain:{word}"}
                for i, ancestor in enumerate(path)]
        self.box.put_template(
            "echo-lexical-evidence-v1", "Frozen lexical evidence context",
            {"network": "provisional", "execution": False, "auto_admit": False},
            list(self.refs.values()))

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.box.close()

    def _witness(self, word, candidate, omit_edges):
        card = self.box.get("cards", self.refs[word]["id"], self.refs[word]["revision"])
        if card["body"]["chain"] != self.data[word]["chain"]:
            return None
        needed = []
        for edge in self.graph[word]:
            if (word, edge["from"], edge["to"]) in omit_edges:
                return None
            needed.append(edge)
            if edge["to"] == candidate:
                return {"word": word, "synset": card["body"]["synset"],
                        "source_card": dict(self.refs[word]),
                        "edges": needed, "origin": card["provenance"]["source"]}
        return None

    def relate(self, left, right, *, omit_edges=(), card_refs=None):
        if left not in self.data or right not in self.data:
            return {"decision": "abstain", "reason": "unknown dictionary entry"}
        if left == right:
            return {"decision": "abstain", "reason": "self-comparison is not evidence"}
        for word in (left, right):
            if card_refs is not None and card_refs.get(word) != self.refs[word]:
                return {"decision": "abstain", "reason": "missing or stale exact card revision"}
        if self.data[left]["synset"] == self.data[right]["synset"]:
            candidates = [self.data[left]["chain"][-1]]
            reason = "exact recorded synset"
        else:
            common = set(self.data[left]["chain"]) & set(self.data[right]["chain"])
            limit = max(2, int(len(self.data) * self.cap))
            candidates = sorted(
                (c for c in common if self.df[c] <= limit and c != "entity"),
                key=lambda c: (self.df[c], -min(
                    self.data[left]["chain"].index(c),
                    self.data[right]["chain"].index(c)), c))
            reason = "shared discriminating lexical ancestor"
        if not candidates:
            return {"decision": "abstain", "reason": "generic-only or no shared relation"}
        candidate = candidates[0]
        witnesses = [self._witness(word, candidate, set(omit_edges)) for word in (left, right)]
        if not all(witnesses):
            return {"decision": "abstain", "reason": "incomplete evidence path"}
        return {"decision": "supported_provisional", "reason": reason,
                "ancestor": candidate, "document_frequency": self.df[candidate],
                "witnesses": witnesses, "source_linked": True,
                "not_empirical_truth": True, "vocabulary_admitted": 0}

    def candidate_words(self):
        """Observed ancestors not already among the 22 seed words; never admitted."""
        seeds = set(self.data)
        return sorted({word for entry in self.data.values()
                       for word in entry["chain"] if word not in seeds})


PAIR_CASES = [
    ("being", "existence"),
    ("change", "emergence"),
    ("experience", "reality"),
    ("condition", "consciousness"),
    ("boundary", "state"),
    ("structure", "boundary"),
    ("cause", "change"),
    ("relation", "being"),
    ("entity", "relation"),
    ("identity", "structure"),
    ("actual", "identity"),
    ("effect", "process"),
    ("condition", "state"),
    ("potential", "being"),
]


def run_comparison(dictionary):
    cases = []
    with EvidenceDictionary(dictionary) as network:
        for left, right in PAIR_CASES:
            b = baseline(dictionary, left, right)
            t = network.relate(left, right)
            cases.append({
                "left": left, "right": right, "baseline": b,
                "treatment": {k: v for k, v in t.items() if k != "witnesses"},
                "evidence_witnesses": (
                    [{"word": w["word"], "source_card": w["source_card"],
                      "path_length": len(w["edges"]), "origin": w["origin"]}
                     for w in t["witnesses"]] if "witnesses" in t else []),
            })
        positive_baseline = sum(c["baseline"]["decision"] == "associated" for c in cases)
        support = sum(c["treatment"]["decision"] == "supported_provisional" for c in cases)
        citations = sum(bool(c["evidence_witnesses"]) for c in cases)
        candidate_words = network.candidate_words()
        return {
            "experiment": "ECHO-CARD-EVIDENCE-DICTIONARY-015",
            "dictionary": "frozen Echo_Green_Future autonomous-agency wordnet-chain fixture",
            "source_words": len(dictionary),
            "source_revision": "pinned by branch checkout; capture Git SHA in CI log",
            "baseline": "A-165-style any-shared-ancestor, includes universal roots",
            "treatment": "revisioned CatalogBox + candidate lexical evidence graph + specificity threshold",
            "same_lexical_inputs": True,
            "comparison_pairs": len(cases),
            "baseline_associations": positive_baseline,
            "treatment_provisional_supports": support,
            "treatment_abstentions": len(cases)-support,
            "source_witness_coverage_of_supported": (citations/support if support else None),
            "candidate_new_lexical_terms_not_admitted": len(candidate_words),
            "vocabulary_actually_admitted": 0,
            "epistemic_limit": ("This tests explainability and generic-link filtering on an existing"
                " frozen lexical graph. It does not test new factual knowledge, new vocabulary"
                " admission, independently learned language, or subjective comprehension."),
            "cases": cases,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_comparison(load_dictionary())
    data = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf-8")
    print(data)
