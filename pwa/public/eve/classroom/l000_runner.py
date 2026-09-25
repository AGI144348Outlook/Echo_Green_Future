"""L000 deterministic execution harness.

This is ECHO's first executable classroom loop, not a language model.
It may organize only from observable properties already present in the lobby
and glyph registry. It cannot invent semantic facts about words.

The loop searches candidate structural views, validates Dual-Order
reachability, retains improvements, and records every round.
"""
from collections import defaultdict
import json

def _view(words, mode):
    out = defaultdict(list)
    for word in words:
        if mode == "initial":
            key = word[0]
        elif mode == "terminal":
            key = word[-1]
        elif mode == "length":
            key = str(len(word))
        elif mode == "contains":
            # observable character-membership; intentionally non-semantic
            for ch in sorted(set(word)):
                out[ch].append(word)
            continue
        else:
            raise ValueError(mode)
        out[key].append(word)
    return {k: sorted(v) for k, v in sorted(out.items())}

def _validate(words, views):
    universe=set(words)
    referenced=set()
    missing=set()
    typed=True
    for view_name, buckets in views.items():
        if not isinstance(view_name,str) or not isinstance(buckets,dict):
            typed=False
        for members in buckets.values():
            referenced.update(members)
            missing.update(set(members)-universe)
    unreachable=universe-referenced
    return {
        "reachable": len(universe)-len(unreachable),
        "total": len(universe),
        "unreachable": sorted(unreachable),
        "missing_references": sorted(missing),
        "relationship_types_distinguishable": typed,
        "pass": not unreachable and not missing and typed,
    }

def run_l000(lobby, glyph_registry, assignment):
    words=list(lobby.neighbors)
    modes=("initial","terminal","length","contains")
    accepted={}
    history=[]
    stable=0
    previous_signature=None
    budget=int(assignment.get("round_budget",50))

    # Glyph sequence is a structural candidate justified from registry:
    # Resh leading/self-reference -> Vav joining -> Samech stabilize -> Tav terminal seal.
    names={g["name"]:g for g in glyph_registry["glyphs"]}
    glyph_sequence=[names[n]["glyph"] for n in ("Resh","Vav","Samech","Tav")]

    for rnd in range(1,budget+1):
        candidate_mode=modes[min(rnd-1,len(modes)-1)]
        candidate={candidate_mode:_view(words,candidate_mode)}
        trial={**accepted,**candidate}
        validation=_validate(words,trial)
        decision="retain" if validation["pass"] else "revise"
        if validation["pass"]:
            accepted=trial

        signature=json.dumps(accepted,sort_keys=True,ensure_ascii=False)
        stable=stable+1 if signature==previous_signature else 0
        previous_signature=signature
        history.append({
            "round":rnd,
            "candidate":candidate_mode,
            "decision":decision,
            "validation":validation,
            "accepted_views":list(accepted),
            "stable_rounds":stable,
        })
        if validation["pass"] and stable>=5:
            break

    final=_validate(words,accepted)
    return {
        "assignment":"L000",
        "engine":"deterministic-structural-harness-v1",
        "epistemic_boundary":"No semantic facts inferred; indexes use observable string structure only.",
        "glyph_sequence":glyph_sequence,
        "glyph_rationale":{
            "ר":"leading/self-reference: initiate organization from ECHO's governing reference",
            "ו":"joining: establish relations between addressable neighbors and index buckets",
            "ס":"stability: retain a validated organizational view",
            "ת":"terminal: mark validated completion"
        },
        "mathematical_representation":"I_k: W -> P(B_k); validate union(range(I_k)) = W and range(I_k) subset W",
        "rounds_executed":len(history),
        "history":history,
        "accepted_indexes":accepted,
        "final_validation":final,
        "status":"PASS" if final["pass"] else "INCOMPLETE",
        "semantic_organization":"UNRESOLVED",
        "next_need":"Acquire evidence/definitions before proposing semantic relationship indexes."
    }

def run_l000_json(lobby, glyph_registry_json, assignment_json):
    glyph_registry=json.loads(glyph_registry_json)
    assignment=json.loads(assignment_json)
    return json.dumps(run_l000(lobby,glyph_registry,assignment),ensure_ascii=False,sort_keys=True)
