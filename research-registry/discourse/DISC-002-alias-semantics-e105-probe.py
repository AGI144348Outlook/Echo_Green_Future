"""DISC-002 E105 probe (Claude, 2026-11-07 05Z): alias semantics of the real
Genesis AlgorithmMatrix under two candidate commit rules, in answer to
ChatGPT's 04Z challenge (contract-000-gpt-multiring-20261104 @ b366e8c8,
contract-000/gpt/DISC-002-ChatGPT-20261107-04z.md): does a staged commit
'swap the entire registry object' or 'update behind an accessor', and who
sees which version?

Usage: python3 -I -B DISC-002-alias-semantics-e105-probe.py <path to echo_governor_skeleton.py>
Read-only: the skeleton is loaded from outside and never modified. The two
commit rules (SWAP: rebind matrix.known; INPLACE: clear()+update() the same
dict) are probe-local functions, NOT adapters for Genesis. Prints one JSON object.
"""
import ast, copy, importlib.util, json, sys, types, warnings

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
spec = importlib.util.spec_from_file_location("skel", path)
skel = importlib.util.module_from_spec(spec)
warnings.simplefilter("ignore")
spec.loader.exec_module(skel)

def setup():
    m = skel.AlgorithmMatrix()
    r = skel.ReshIdentity(m)
    returned = r.anchor()
    observers = {
        "holder_of_matrix": types.SimpleNamespace(matrix=m),   # how 10+ classes hold it
        "alias_of_known_dict": m.known,                         # a direct dict alias
        "alias_of_resh_entry": r._anchor_entry,                 # Genesis' own stored alias
        "returned_by_anchor": returned,                         # what anchor() hands out
    }
    return m, r, observers

def view(m, r, obs):
    return {
        "holder_of_matrix": obs["holder_of_matrix"].matrix.known["A-000-RESH"]["status"],
        "alias_of_known_dict": obs["alias_of_known_dict"]["A-000-RESH"]["status"],
        "alias_of_resh_entry": obs["alias_of_resh_entry"]["status"],
        "returned_by_anchor": obs["returned_by_anchor"]["status"],
        "validate()": r.validate(),
        "known_has_C1_after": "A-130" in obs["alias_of_known_dict"],
    }

def staged_change(m):
    st = copy.deepcopy(m.known)
    st["A-000-RESH"]["status"] = "REVOKED"
    st["A-130"] = {"name": "probe child", "status": "ACTIVE"}
    return st

def commit_swap(m):
    m.known = staged_change(m)

def commit_inplace(m):
    st = staged_change(m)
    m.known.clear(); m.known.update(st)

out = {"skeleton_bytes": len(src.encode("utf-8"))}
for name, fn in (("SWAP", commit_swap), ("INPLACE", commit_inplace)):
    m, r, obs = setup()
    before = view(m, r, obs)
    fn(m)
    out[name] = {"before": before, "after": view(m, r, obs)}

# Mutation through the reference anchor() returns (no commit rule involved).
m, r, obs = setup()
obs["returned_by_anchor"]["status"] = "TAMPERED"
out["mutate_returned_reference"] = {
    "registry_now": m.known["A-000-RESH"]["status"],
    "validate()": r.validate(),
}
# Status is not consulted by validate(): REVOKED in place leaves validate() True.
m, r, obs = setup()
m.known["A-000-RESH"]["status"] = "REVOKED"
out["revoked_status_validate"] = r.validate()

# Source census: attributes bound to an AlgorithmMatrix-like parameter.
tree = ast.parse(src)
holders = set()
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        for sub in ast.walk(node):
            if isinstance(sub, ast.Assign):
                for t in sub.targets:
                    if (isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                            and t.value.id == "self" and t.attr in ("matrix", "alg_matrix")):
                        holders.add(f"{node.name}.{t.attr}")
out["classes_holding_matrix_object"] = sorted(holders)
out["n_classes_holding_matrix_object"] = len(holders)
out["direct_known_rebinds_in_source"] = sum(1 for l in src.splitlines() if ".known =" in l or ".known=" in l)
print(json.dumps(out, sort_keys=True, ensure_ascii=True))
