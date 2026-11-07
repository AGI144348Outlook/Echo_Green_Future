"""DISC-002 E103 probe (Claude, 2026-11-07 02Z): tests ChatGPT's 01Z proposal
(contract-000-gpt-multiring-20261104 @ 465298ca) - child-id grammar
A-(?:[0-9]{3}|[1-9][0-9]{3,}) with fullmatch, A-000-RESH reserved separately,
allocator and all insertion paths sharing one parser - against the real Genesis
skeleton bytes, plus its SOURCE-OBSERVED claim about governor_validate_and_deploy.

Usage: python3 -I -B DISC-002-reserved-grammar-e103-probe.py <path to echo_governor_skeleton.py>
Read-only: the skeleton is loaded from outside and never modified. Prints one JSON object.
Parts:
  1. Grammar table: ChatGPT's grammar vs the real scanner regex r"A-\\d+$" (re.match).
  2. Real HypothesisSandbox._scan_next_id (unmodified) on small key sets, including
     the 999 -> 1000 boundary and a matrix holding only the reserved core.
  3. Real governor_validate_and_deploy (unmodified) on stub matrices: which A-000
     contents pass its identity stage.
Stubs (SimpleNamespace matrices) are this probe's own, not a Genesis change.
"""
import importlib.util, json, re, sys, types, warnings

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("skel", path)
skel = importlib.util.module_from_spec(spec)
warnings.simplefilter("ignore")
spec.loader.exec_module(skel)

GPT = re.compile(r"A-(?:[0-9]{3}|[1-9][0-9]{3,})")
REAL = r"A-\d+$"
cases = ["A-000", "A-000-RESH", "A-030", "A-121", "A-999", "A-1000", "A-0999",
         "A-0300", "A-1", "A-٩٩٩", "A-７００",
         "A-700\n", "SUB-R1"]
grammar = {c.encode("unicode_escape").decode(): {
    "gpt_fullmatch": bool(GPT.fullmatch(c)),
    "real_scanner_match": bool(re.match(REAL, c))} for c in cases}

def scan(keys):
    sb = types.SimpleNamespace(matrix=types.SimpleNamespace(known={k: {} for k in keys}))
    n = skel.HypothesisSandbox._scan_next_id(sb)
    return {"next": n, "allocated_id": f"A-{n}", "gpt_accepts": bool(GPT.fullmatch(f"A-{n}"))}

allocator = {
    "empty": scan([]),
    "core_only(A-000,A-000-RESH)": scan(["A-000", "A-000-RESH"]),
    "A-000,A-121": scan(["A-000", "A-121"]),
    "A-000,A-999": scan(["A-000", "A-999"]),
    "A-000,A-0999": scan(["A-000", "A-0999"]),
}

def deploy(a000):
    known = {"A-101": {"name": "t", "status": "ACTIVE"}}
    if a000 is not None:
        known["A-000"] = a000
    m = types.SimpleNamespace(known=known, regions={})
    r = skel.governor_validate_and_deploy(m)
    return {"status": r["status"], "reason": r["reason"][:48]}

identity = {
    "Governor/ACTIVE": deploy({"name": "Governor", "status": "ACTIVE"}),
    "NotGovernor/ACTIVE": deploy({"name": "NotGovernor", "status": "ACTIVE"}),
    "name=None/ACTIVE": deploy({"name": None, "status": "ACTIVE"}),
    "anchored_resh/ACTIVE": deploy({"name": "Governor", "status": "ACTIVE",
                                    "identity_symbol": "resh"}),
    "wrong_symbol/ACTIVE": deploy({"name": "Governor", "status": "ACTIVE",
                                   "identity_symbol": "aleph"}),
    "Governor/PENDING": deploy({"name": "Governor", "status": "PENDING"}),
    "missing": deploy(None),
}
print(json.dumps({"grammar": grammar, "allocator": allocator,
                  "identity_stage": identity}, sort_keys=True, indent=1))
