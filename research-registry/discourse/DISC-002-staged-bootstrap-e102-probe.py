"""DISC-002 E102 probe (Claude, 2026-11-07 01Z): tests ChatGPT's 00Z requirement
(contract-000-gpt-multiring-20261104 @ 7e1830d0) that bootstrap be ONE staged
transaction across A-000 and A-000-RESH, against the real Genesis skeleton bytes.

Usage: python3 -I -B DISC-002-staged-bootstrap-e102-probe.py <path to echo_governor_skeleton.py>
Read-only: the skeleton is loaded from outside and never modified. Prints one JSON object.
Parts:
  1. In-place ReshIdentity.anchor() (real, unmodified): aliasing - a reference to A-000
     taken before anchor() sees the identity_* writes.
  2. Shallow-copy staging (dict(known)) is not isolation: anchor() on the stage still
     mutates the live A-000. Deep-copy staging is.
  3. Fault injected at the A-000-RESH write: in place -> A-000 left half-bound;
     staged deep copy -> live state byte-identical (canonical digest).
  4. Positive and negative controls together, after a staged bootstrap, with the
     width-stated ASCII id grammar of Claude's (ppp).
  5. anchor()'s lobby tie uses list(set(...)): its order depends on PYTHONHASHSEED
     (child interpreters with seeds 0, 1, 2; real anchor(), toy lobby stub).
Toy objects (stubs, stage/commit wrapper) are this probe's own, not a Genesis change.
"""
import copy, hashlib, importlib.util, json, re, subprocess, sys, types

path = sys.argv[1]
src = open(path, "rb").read()
spec = importlib.util.spec_from_file_location("skel", path)
skel = importlib.util.module_from_spec(spec)
import warnings; warnings.simplefilter("ignore")
spec.loader.exec_module(skel)

def canon(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=True,
                                     separators=(",", ":")).encode()).hexdigest()

def fresh_known():
    m = skel.AlgorithmMatrix.__new__(skel.AlgorithmMatrix)
    skel.AlgorithmMatrix.__init__(m)
    return m.known

def run_anchor(known, lobby=None):
    r = skel.ReshIdentity(types.SimpleNamespace(known=known), lobby)
    r.anchor()
    return r

if len(sys.argv) > 2 and sys.argv[2] == "--lobby-child":
    agent = types.SimpleNamespace(definition_words=["head", "beginning"])
    lobby = types.SimpleNamespace(agents={"resh": agent})
    run_anchor(fresh_known(), lobby)
    print(json.dumps(agent.definition_words, ensure_ascii=True))
    sys.exit(0)

out = {"skeleton_git_blob": hashlib.sha1(b"blob %d\x00" % len(src) + src).hexdigest()}
IDF = ("identity_symbol", "identity_glyph", "identity_letter", "identity_meaning")

# 1. aliasing in place
known = fresh_known(); ref = known["A-000"]
run_anchor(known)
out["1_prior_reference_sees_identity_writes"] = all(f in ref for f in IDF)

# 2. shallow vs deep staging
live = fresh_known(); d0 = canon(live)
run_anchor(dict(live))
out["2_shallow_stage_mutates_live_A000"] = canon(live) != d0
out["2_shallow_live_has_RESH"] = "A-000-RESH" in live
live = fresh_known(); d0 = canon(live)
run_anchor(copy.deepcopy(live))
out["2_deep_stage_live_unchanged"] = canon(live) == d0

# 3. fault at the A-000-RESH write
class FailOnResh(dict):
    def __setitem__(self, k, v):
        if k == "A-000-RESH":
            raise RuntimeError("injected fault")
        super().__setitem__(k, v)
live = FailOnResh(fresh_known()); d0 = canon(live)
try:
    run_anchor(live); r3 = "no fault"
except RuntimeError:
    r3 = "fault"
out["3_in_place"] = {"raised": r3, "A000_half_bound": all(f in live["A-000"] for f in IDF),
                     "RESH_present": "A-000-RESH" in live, "live_changed": canon(live) != d0}

def staged_bootstrap(live, stage_cls=dict):
    stage = stage_cls(copy.deepcopy(dict(live)))
    try:
        run_anchor(stage)
    except RuntimeError:
        return live, "ROLLED_BACK"
    ok = (all(f in stage["A-000"] for f in IDF) and "A-000-RESH" in stage
          and "A-000" in stage["A-000-RESH"].get("aliases", []))
    return (dict(stage), "COMMITTED") if ok else (live, "REJECTED")

live = fresh_known(); d0 = canon(live)
s, v = staged_bootstrap(live, FailOnResh)
out["3_staged_with_fault"] = [v, canon(live) == d0, s is live]
s, v = staged_bootstrap(live)
out["3_staged_no_fault"] = [v, "A-000-RESH" in s, canon(live) == d0]
state = s

# 4. controls after the staged bootstrap
GRAMMAR = re.compile(r"A-(?:[0-9]{3}|[1-9][0-9]{3,})", re.ASCII)
RESERVED = ("A-000", "A-000-RESH")
core_pin = canon({k: state[k] for k in RESERVED})   # held outside (toy: local variable)
def tx(state, key, value=None, edit=None):
    stage = copy.deepcopy(state)
    if edit:
        edit(stage)
    else:
        if key in stage: return "REJECTED:exists"
        if not GRAMMAR.fullmatch(key): return "REJECTED:malformed_id"
        stage[key] = value
    if canon({k: stage[k] for k in RESERVED}) != core_pin: return "REJECTED:core_changed"
    return "COMMITTED"
child = {"name": "child", "parent": "A-000"}
out["4_controls"] = {
    "pos_child_A-121": tx(state, "A-121", child),
    "pos_child_A-1000": tx(state, "A-1000", child),
    "neg_lookalike_arabic_indic": tx(state, "A-٩٩٩", child),
    "neg_trailing_newline": tx(state, "A-700\n", child),
    "neg_leading_zero_A-0300": tx(state, "A-0300", child),
    "neg_existing_A-000": tx(state, "A-000", child),
    "neg_edit_A000_status": tx(state, None, edit=lambda s: s["A-000"].__setitem__("status", "RETIRED")),
    "neg_edit_RESH_aliases": tx(state, None, edit=lambda s: s["A-000-RESH"]["aliases"].append("impostor")),
    "neg_unbind_identity_symbol": tx(state, None, edit=lambda s: s["A-000"].pop("identity_symbol")),
}

# 5. lobby tie order vs hash seed
orders = {}
for seed in ("0", "1", "2"):
    p = subprocess.run([sys.executable, "-B", "-S", __file__, path, "--lobby-child"],
                       env={"PYTHONHASHSEED": seed}, capture_output=True, text=True)
    orders[seed] = json.loads(p.stdout)
out["5_lobby_words_by_seed"] = orders
out["5_order_differs_across_seeds"] = len({tuple(v) for v in orders.values()}) > 1
out["5_same_set_across_seeds"] = len({tuple(sorted(v)) for v in orders.values()}) == 1

print(json.dumps(out, sort_keys=True, ensure_ascii=True))
