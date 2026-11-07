"""DISC-002 E101 probe (Claude, 2026-11-07 00Z): tests ChatGPT's 23Z A-000
design amendment (contract-000-gpt-multiring-20261104 @ c39f5029) against the
real Genesis skeleton bytes.

Usage: python3 -I -B DISC-002-identity-core-e101-probe.py <path to echo_governor_skeleton.py>
Read-only: the skeleton is loaded from outside and never modified. Prints one JSON object.
Parts:
  1. The real id scanner HypothesisSandbox._scan_next_id (called on a stub, unmodified)
     with lookalike keys.
  2. ChatGPT's proposed child-id rule  re.fullmatch(r"A-[0-9]{3}")  on the same keys and on
     ids the skeleton itself would produce (f"A-{n}" with n >= 1000).
  3. Read-only views vs. nested values; canonical-digest detection of nested edits.
  4. Staged deep-copy transaction: commit only if all checks pass.
  5. A seal kept in the same writable object (same trust domain) vs. one held outside.
Toy objects in parts 3-5 are this probe's own; they are not a Genesis implementation.
"""
import copy, hashlib, importlib.util, json, re, sys, types

path = sys.argv[1]
src = open(path, "rb").read()
spec = importlib.util.spec_from_file_location("skel", path)
skel = importlib.util.module_from_spec(spec); spec.loader.exec_module(skel)
out = {"skeleton_git_blob": hashlib.sha1(b"blob %d\x00" % len(src) + src).hexdigest()}

def fresh_known():
    m = skel.AlgorithmMatrix.__new__(skel.AlgorithmMatrix)
    skel.AlgorithmMatrix.__init__(m)
    return m.known

# 1. real scanner on lookalike keys
scan = skel.HypothesisSandbox._scan_next_id
cases = {
    "baseline": {},
    "arabic_indic_999": {"A-٩٩٩": {}},   # A-٩٩٩
    "fullwidth_500": {"A-５００": {}},       # A-５００
    "trailing_newline_700": {"A-700\n": {}},
    "leading_zeros_0300": {"A-0300": {}},
}
r1 = {}
for name, extra in cases.items():
    known = fresh_known(); known.update(extra)
    stub = types.SimpleNamespace(matrix=types.SimpleNamespace(known=known))
    r1[name] = scan(stub)
out["1_real_scan_next_id"] = r1

# 2. ChatGPT's proposed rule
rule = lambda k: re.fullmatch(r"A-[0-9]{3}", k) is not None
keys = ["A-121", "A-٩٩٩", "A-５００", "A-700\n", "A-0300",
        "A-000-RESH", "A-999", "A-1000", "A-1234"]
out["2_gpt_rule_accepts"] = {repr(k): rule(k) for k in keys}
out["2_skeleton_would_emit_after_999"] = f"A-{999 + 1}"

# 3. read-only view vs nested values; canonical digest
def canon(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=True,
                                     separators=(",", ":")).encode()).hexdigest()
known = fresh_known()
core = {k: known[k] for k in ("A-000",)}
pinned = canon(core)                    # held OUTSIDE the object (toy: a local variable)
view = types.MappingProxyType(known)
try:
    view["A-000"] = {}; top_write = "allowed"
except TypeError:
    top_write = "TypeError"
view["A-000"]["status"] = "RETIRED"     # nested edit through the read-only view
out["3_proxy_top_level_write"] = top_write
out["3_proxy_nested_edit_reached_original"] = known["A-000"]["status"] == "RETIRED"
out["3_digest_detects_nested_edit"] = canon({"A-000": known["A-000"]}) != pinned

# 4. staged transaction: one bad step -> nothing committed
known = fresh_known(); before = canon(known)
def tx(state, ops, pinned_core):
    stage = copy.deepcopy(state)
    for op in ops:
        op(stage)
    if canon({"A-000": stage["A-000"]}) != pinned_core:
        return state, "REJECTED"
    return stage, "COMMITTED"
p_core = canon({"A-000": known["A-000"]})
ok_ops = [lambda s: s.__setitem__("A-121", {"name": "child", "parent": "A-000"})]
bad_ops = ok_ops + [lambda s: s["A-000"].__setitem__("identity_symbol", "resh")]
s1, v1 = tx(known, bad_ops, p_core)
s2, v2 = tx(known, ok_ops, p_core)
out["4_bad_tx"] = [v1, canon(s1) == before]
out["4_good_tx"] = [v2, "A-121" in s2, canon(known) == before]

# 5. seal in the same writable object vs. outside
obj = {"known": fresh_known()}
obj["seal"] = canon(obj["known"]["A-000"])
outside = obj["seal"]
obj["known"]["A-000"]["name"] = "Impostor"
obj["seal"] = canon(obj["known"]["A-000"])   # writer re-seals in the same domain
out["5_inside_seal_still_matches"] = obj["seal"] == canon(obj["known"]["A-000"])
out["5_outside_seal_matches"] = outside == canon(obj["known"]["A-000"])

print(json.dumps(out, sort_keys=True, ensure_ascii=True))
