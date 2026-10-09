"""NVE-D configuration-testing prototype (Steps 1-4). Standard library only.

All interpretations and move semantics are PROPOSED, never registry authority.
No semantic conclusions or E3/E4 evidence are produced by this module.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import re
from collections import Counter
from dataclasses import dataclass, field

ALPHABET = ("<", ">", "=", "0")
ENTITIES = tuple(f"MS-{i:03d}" for i in range(1, 17))
MOVES = {"ו": "JUNGERE", "ז": "SCINDERE", "ט": "VERTERE",
         "ס": "STARE", "מ": "FLUERE", "ק": "MUTARE",
         "ת": "FINIS", "י": "RADIX"}
# These are candidate operators, not declared meanings.
PROPOSAL_STATUS = "PROPOSED/INFERRED"


def pairs(entities=ENTITIES):
    return tuple((a, b) for a in entities for b in entities if a != b)


def canonical_relations(relations, entities=ENTITIES):
    expected = {f"{a}|{b}" for a, b in pairs(entities)}
    if set(relations) != expected:
        raise ValueError("missing, extra or invalid ordered-pair keys")
    if any(value not in ALPHABET for value in relations.values()):
        raise ValueError("relation outside provisional alphabet")
    return [[key, relations[key]] for key in sorted(expected)]


def configuration(relations=None, *, entities=ENTITIES, registry_ref, parent=None, move=None):
    if not registry_ref or registry_ref == "unverified":
        raise ValueError("pin a real registry commit/ref; never invent provenance")
    if len(set(entities)) != len(entities) or len(entities) < 2:
        raise ValueError("entity IDs must be unique")
    if relations is None:
        relations = {f"{a}|{b}": "0" for a, b in pairs(entities)}
    canon = canonical_relations(relations, entities)
    identity = {"entity_registry": registry_ref, "entities": list(entities),
                "alphabet": list(ALPHABET), "relations": canon}
    raw = json.dumps(identity, sort_keys=True, ensure_ascii=False,
                     separators=(",", ":")).encode("utf-8")
    return {"config_id": "sha256:" + hashlib.sha256(raw).hexdigest(),
            **identity, "parent_config_id": parent, "move": move,
            "status": PROPOSAL_STATUS}


def verify_config(config):
    rel = dict(config["relations"])
    rebuilt = configuration(rel, entities=tuple(config["entities"]),
                            registry_ref=config["entity_registry"])
    if rebuilt["config_id"] != config["config_id"]:
        raise ValueError("configuration digest mismatch")
    return True


def judge_b(config, bindings):
    """J-B: independent four ordered-pair relations; no proportional semantics.

    Token '=' iff all four are observed and identical; '0' otherwise.
    This is a candidate aggregation rule, not the user's declared formula.
    """
    if len(bindings) != 4 or len(set(bindings)) != 4:
        return {"judge": "J-B-v0", "token": "0", "reason": "invalid_bindings"}
    r = dict(config["relations"])
    try:
        values = [r[f"{bindings[i]}|{bindings[(i+1)%4]}"] for i in range(4)]
    except KeyError:
        return {"judge": "J-B-v0", "token": "0", "reason": "unregistered_entity"}
    token = "=" if "0" not in values and len(set(values)) == 1 else "0"
    return {"judge": "J-B-v0", "token": token, "evidence": values,
            "status": PROPOSAL_STATUS}


def judge_b_independent(config, bindings):
    """Independently structured oracle: scan ordered pair table, not judge_b."""
    if len(bindings) != 4 or len(set(bindings)) != 4:
        return "0"
    found = []
    for i, left in enumerate(bindings):
        right = bindings[(i + 1) % 4]
        matches = [value for key, value in config["relations"]
                   if key == left + "|" + right]
        if len(matches) != 1 or matches[0] == "0":
            return "0"
        found.extend(matches)
    return "=" if all(value == found[0] for value in found) else "0"


@dataclass
class Node:
    config: dict
    status: str = "active"
    provenance: dict = field(default_factory=dict)


@dataclass
class Link:
    a: str
    b: str
    w: float = 0.5
    H: int = 0
    wins: int = 0
    losses: int = 0
    protect: float = 0.0


@dataclass
class Budget:
    max_tests: int
    tests: int = 0

    def spend(self):
        if self.tests >= self.max_tests:
            return False
        self.tests += 1
        return True


@dataclass
class Clock:
    tick: int = 0
    rest: int = 0


class TestedSet:
    def __init__(self, ids=()):
        self.ids = set(ids)

    def add(self, config):
        ident = config["config_id"]
        if ident in self.ids:
            return False
        self.ids.add(ident)
        return True

    def dump(self):
        return {"schema": "nve-d-tested-set-v1", "config_ids": sorted(self.ids)}

    @classmethod
    def load(cls, data):
        if data.get("schema") != "nve-d-tested-set-v1":
            raise ValueError("tested-set schema mismatch")
        return cls(data["config_ids"])


def apply_move(config, letter, rng, *, protected=None, recent=None):
    """Return proposed child config; no mutation of parent.

    'ו' and 'ז' are disallowed on the same pair in one step.
    Protections are per-run only. 'ת' is terminal; 'י' resets to a seed.
    """
    if letter not in MOVES:
        raise ValueError("unknown proposed move")
    protected = protected if protected is not None else {}
    recent = recent if recent is not None else {}
    rel = dict(config["relations"])
    eligible = [k for k in sorted(rel) if protected.get(k, 0) <= 0]
    if not eligible and letter not in ("ת",):
        return None
    key = rng.choice(eligible) if eligible else None
    old = rel.get(key)
    if letter == "ו":
        if recent.get(key) == "ז":
            return None
        if old != "0":
            return None
        rel[key] = rng.choice(("<", ">", "="))
    elif letter == "ז":
        if recent.get(key) == "ו" or old == "0":
            return None
        rel[key] = "0"
    elif letter == "ט":
        if old not in ("<", ">"):
            return None
        rel[key] = ">" if old == "<" else "<"
    elif letter == "ס":
        if old == "0":
            return None
        protected[key] = 2
    elif letter == "מ":
        a, b = key.split("|")
        options = [k for k in sorted(rel) if k.startswith(b + "|")
                   and rel[k] == "0" and rel[key] != "0"]
        if not options:
            return None
        rel[rng.choice(options)] = rel[key]
    elif letter == "ק":
        if old == "0":
            return None
        rel[key] = rng.choice([v for v in ("<", ">", "=") if v != old])
    elif letter == "ת":
        return None
    elif letter == "י":
        rel = {k: "0" for k in rel}
        rel[key] = rng.choice(("<", ">", "="))
    if rel == dict(config["relations"]):
        return None
    if letter in ("ו", "ז"):
        recent[key] = letter
    return configuration(rel, entities=tuple(config["entities"]),
                         registry_ref=config["entity_registry"],
                         parent=config["config_id"], move=letter + " " + MOVES[letter])


def score(config):
    """Synthetic proxy ONLY: non-open pairs; never evidence of symbol meaning."""
    return sum(value != "0" for _, value in config["relations"])


def run_arm(*, arm, seed, budget, registry_ref, prior=()):
    if arm not in ("random", "sparse", "adaptive"):
        raise ValueError("unknown arm")
    if budget < 1:
        raise ValueError("budget must be positive")
    rng = random.Random(seed)
    seen = TestedSet(prior)
    current = configuration(registry_ref=registry_ref)
    clock = Clock()
    cap = Budget(budget)
    history = []
    links = {}
    move_counts = Counter()
    best = score(current)
    duplicates = 0
    attempts = 0
    protected = {}
    # One transition per attempted configuration; hard ceiling prevents endless retries.
    while cap.tests < cap.max_tests and attempts < budget * 50:
        attempts += 1
        if arm == "random":
            letter = rng.choice(tuple(MOVES))
        elif arm == "sparse":
            letter = rng.choice(("ו", "ז", "ט", "ק", "י"))
        else:
            weights = [(links.get(x, Link(x, x)).wins + 1) /
                       (links.get(x, Link(x, x)).wins +
                        links.get(x, Link(x, x)).losses + 2)
                       for x in MOVES]
            letter = rng.choices(tuple(MOVES), weights=weights)[0]
        # Step-local locks; no false cross-step exclusion.
        candidate = apply_move(current, letter, rng, protected=protected, recent={})
        for key in list(protected):
            protected[key] -= 1
            if protected[key] <= 0:
                del protected[key]
        if candidate is None:
            continue
        if not seen.add(candidate):
            duplicates += 1
            continue
        cap.spend()
        clock.tick += 1
        improved = score(candidate) > best
        link = links.setdefault(letter, Link(letter, letter))
        link.H += 1
        link.w = min(1.0, link.w + (0.02 if improved else -0.005))
        link.w = max(0.0, link.w)
        if improved:
            link.wins += 1
        else:
            link.losses += 1
        if improved or arm == "random" or rng.random() < 0.15:
            current = candidate
        best = max(best, score(candidate))
        move_counts[letter] += 1
        history.append({"config_id": candidate["config_id"], "parent": candidate["parent_config_id"],
                        "move": candidate["move"], "proxy": score(candidate)})
    return {"schema": "nve-d-arm-v1", "arm": arm, "seed": seed,
            "budget": budget, "tested_new": cap.tests, "attempts": attempts,
            "duplicates": duplicates, "clock": vars(clock),
            "best_synthetic_proxy": best, "move_counts": dict(move_counts),
            "history": history, "tested_set": seen.dump(),
            "evidence_level": "NONE", "semantic_conclusion": False,
            "note": "Scaffold only: synthetic proxy is not a finding."}



def validate_registry_manifest(manifest, *, expected=ENTITIES):
    """Validate a locally supplied source-pinned registry manifest.

    This verifies structure and provenance shape, NOT canonical authority or
    authenticity of the claimed upstream commit. Caller must independently
    verify source bytes against the GitHub commit.
    """
    if manifest.get("schema") != "nve-d-registry-manifest-v1":
        raise ValueError("registry manifest schema mismatch")
    commit = manifest.get("commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("registry manifest needs a full 40-hex commit")
    if not manifest.get("repository") or not manifest.get("source_path"):
        raise ValueError("registry source repository and path required")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise ValueError("registry entries missing")
    ids = [e.get("id") for e in entries if isinstance(e, dict)]
    if len(ids) != len(entries) or len(set(ids)) != len(ids):
        raise ValueError("registry IDs duplicate or malformed")
    if set(ids) != set(expected):
        raise ValueError("registry IDs do not match declared trial entity set")
    if any(not e.get("source_locator") for e in entries):
        raise ValueError("each registry entry needs source locator")
    return manifest["repository"] + "@" + commit + ":" + manifest["source_path"]



def main():
    p = argparse.ArgumentParser()
    p.add_argument("--registry-ref", required=True,
                   help="Pinned commit containing verified MS-001..016 IDs")
    p.add_argument("--registry-manifest", required=True,\n                   help="Locally supplied, source-pinned manifest of MS-001..016")\n    p.add_argument("--budget", type=int, default=100)
    p.add_argument("--seed", type=int, default=21)
    p.add_argument("--output", default="-")
    args = p.parse_args()
    with open(args.registry_manifest, encoding="utf-8") as f:
        manifest = json.load(f)
    pinned_ref = validate_registry_manifest(manifest)
    if args.registry_ref != pinned_ref:
        p.error("--registry-ref must match the validated manifest reference")
    output = {"trial": "NVE-D-021-PREPARATION", "status": "PROTOTYPE_NOT_021",
              "registry_ref": args.registry_ref, "arms": [
                  run_arm(arm=arm, seed=args.seed, budget=args.budget,
                          registry_ref=args.registry_ref)
                  for arm in ("random", "sparse", "adaptive")]}
    data = json.dumps(output, indent=2, ensure_ascii=False)
    if args.output == "-":
        print(data)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(data + "\n")


if __name__ == "__main__":
    main()
