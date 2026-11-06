"""DISC-002 E99 probe (Claude, 2026-11-06 22Z): challenge the A-000 fail-closed
reserved-key gate (RC-R5 (ggg)) against the real skeleton bytes.

Usage: python3 -I -B DISC-002-reserved-key-gate-e99-probe.py <path to echo_governor_skeleton.py>
Read-only: the skeleton is loaded from outside and never modified. The gate below
is a toy written for this probe only; it is not a proposal for the final code.
Prints one JSON object on stdout.
"""
import ast
import hashlib
import importlib.util
import json
import sys
import types

path = sys.argv[1]
src = open(path, "rb").read()
out = {"skeleton_git_blob": hashlib.sha1(b"blob %d\x00" % len(src) + src).hexdigest()}

# 1. Static census of write sites into a `known` mapping (SOURCE-OBSERVED via AST).
tree = ast.parse(src)
sites = []
for node in ast.walk(tree):
    targets = []
    if isinstance(node, ast.Assign):
        targets = node.targets
    elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
        targets = [node.target]
    for t in targets:
        if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Attribute) and t.value.attr == "known":
            sites.append((node.lineno, "subscript-assign"))
        if isinstance(t, ast.Attribute) and t.attr == "known":
            sites.append((node.lineno, "rebind"))
        if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Subscript):
            inner = t.value
            if isinstance(inner.value, ast.Attribute) and inner.value.attr == "known":
                sites.append((node.lineno, "nested-subscript-assign"))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
            and node.func.attr in ("update", "setdefault", "pop", "popitem", "clear") \
            and isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "known":
        sites.append((node.lineno, "method-" + node.func.attr))
sites.sort()
out["write_sites"] = [f"{l}:{k}" for l, k in sites]
out["write_site_count"] = len(sites)

# 2. Load the real module (its __main__ block does not run on import).
spec = importlib.util.spec_from_file_location("gov", path)
gov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gov)

RESERVED = {"A-000", "A-000-RESH"}


class GatedKnown(dict):
    """Toy fail-closed gate: refuses __setitem__/__delitem__ on reserved keys."""
    refusals = []

    def __setitem__(self, k, v):
        if k in RESERVED:
            GatedKnown.refusals.append(k)
            raise PermissionError("reserved " + k)
        super().__setitem__(k, v)

    def __delitem__(self, k):
        if k in RESERVED:
            raise PermissionError("reserved " + k)
        super().__delitem__(k)


def fresh():
    m = gov.AlgorithmMatrix()
    m.known = GatedKnown(m.known)
    return m


def gov_digest(m):
    return hashlib.sha256(json.dumps(m.known.get("A-000"), sort_keys=True, default=str).encode()).hexdigest()[:16]


results = {}

m = fresh(); d0 = gov_digest(m)
try:
    m.record("A-000", {"name": "Impostor"}); results["record_A000"] = "WRITTEN"
except PermissionError:
    results["record_A000"] = "REFUSED"

m = fresh()
dict.update(m.known, {})  # warm
m.known.update({"A-000": {"name": "Impostor"}})
results["dict_update_bypass"] = "WRITTEN" if m.known["A-000"].get("name") == "Impostor" else "REFUSED"

m = fresh()
m.known.setdefault("A-000-RESH", {"name": "Impostor-Resh"})
results["setdefault_new_reserved"] = "WRITTEN" if "A-000-RESH" in m.known else "REFUSED"

m = fresh()
m.known["A-000"]["status"] = "RETIRED"   # in-place value mutation, key untouched
results["inplace_value_mutation"] = "WRITTEN" if m.known["A-000"]["status"] == "RETIRED" else "REFUSED"
results["inplace_changes_digest"] = gov_digest(m) != d0

m = fresh()
m.known.pop("A-000")
results["pop_bypass"] = "REMOVED" if "A-000" not in m.known else "KEPT"

lookalikes = {
    "trailing_space": "A-000 ",
    "lowercase": "a-000",
    "cyrillic_A": "А-000",
    "arabic_indic_digits": "A-٠٠٠",
    "fullwidth_digits": "A-０００",
    "trailing_newline": "A-000\n",
}
look = {}
for name, k in lookalikes.items():
    m = fresh()
    try:
        m.record(k, {"name": "Lookalike"}); accepted = True
    except PermissionError:
        accepted = False
    look[name] = {"accepted": accepted, "governor_unchanged": gov_digest(m) == d0,
                  "nfkc_casefold_equals_reserved": __import__("unicodedata").normalize("NFKC", k).strip().upper() in RESERVED}
results["lookalikes"] = look

# 3. Real HypothesisSandbox._scan_next_id on a matrix carrying a lookalike key.
scan = {}
for name, k in [("baseline", None), ("arabic_indic_1200", "A-١٢٠٠"),
                ("trailing_newline_A-900", "A-900\n"), ("fullwidth_500", "A-５００")]:
    m = gov.AlgorithmMatrix()
    if k is not None:
        m.record(k, {"name": "x"})
    fake = types.SimpleNamespace(matrix=m)
    try:
        scan[name] = gov.HypothesisSandbox._scan_next_id(fake)
    except Exception as e:  # report, do not hide
        scan[name] = "ERROR " + type(e).__name__
results["scan_next_id"] = scan

# 4. Child with parent pointer stays writable.
m = fresh()
m.record("A-000.c1", {"name": "child", "parent": "A-000"})
results["child_with_parent_pointer"] = "WRITTEN" if "A-000.c1" in m.known else "REFUSED"

# 5. Real ReshIdentity.anchor() under the toy fail-closed gate (bootstrap path).
m = fresh(); d0 = gov_digest(m)
r = gov.ReshIdentity(m)
try:
    r.anchor(); outcome = "ANCHORED"
except PermissionError as e:
    outcome = "REFUSED " + str(e)
results["anchor_under_gate"] = {"outcome": outcome, "validate": r.validate(),
                                "governor_digest_changed": gov_digest(m) != d0,
                                "identity_symbol_present": m.known["A-000"].get("identity_symbol")}

# 6. Real anchor() after the Governor entry was popped (no gate).
m = gov.AlgorithmMatrix(); m.known.pop("A-000")
r = gov.ReshIdentity(m); r.anchor()
results["anchor_after_pop"] = {"validate": r.validate(), "recreated_A000_keys": sorted(m.known["A-000"].keys())}

out["results"] = results
print(json.dumps(out, sort_keys=True, ensure_ascii=True))
