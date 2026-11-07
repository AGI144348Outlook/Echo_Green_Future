"""DISC-002 E104 probe (Claude, 2026-11-07 03Z): baseline of the real Genesis
skeleton against the control list ChatGPT proposed at 02Z
(contract-000-gpt-multiring-20261104 @ 514e9043): A-000 missing, A-000
re-registration, A-1000, A-0999, Unicode digits, SUB- namespaces, atomic
rollback, aliasing, external digest mismatch. It records what the UNMODIFIED
code does today, so a frozen acceptance table has an observed "before" column.
It does not implement or test any adapter.

Usage: python3 -I -B DISC-002-control-baseline-e104-probe.py <path to echo_governor_skeleton.py>
Read-only: the skeleton is loaded from outside and never modified. Prints one JSON object.
Rollback and aliasing are not re-run here (see E102 probe); they are listed as
'see E102'. The digest control is a source census only (no digest code exists to run).
"""
import importlib.util, json, sys, types, warnings

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
spec = importlib.util.spec_from_file_location("skel", path)
skel = importlib.util.module_from_spec(spec)
warnings.simplefilter("ignore")
spec.loader.exec_module(skel)

def scan_real_matrix(extra_keys):
    """Insert keys through the real AlgorithmMatrix.record(), then run the
    real HypothesisSandbox._scan_next_id on that matrix."""
    m = skel.AlgorithmMatrix()
    accepted = {}
    for k in extra_keys:
        before = k in m.known
        m.record(k, {"name": "probe", "status": "ACTIVE"})
        accepted[k.encode("unicode_escape").decode()] = {"was_present": before,
                                                         "now_present": k in m.known}
    sb = types.SimpleNamespace(matrix=m)
    n = skel.HypothesisSandbox._scan_next_id(sb)
    return {"record_accepts": accepted, "next": n, "allocated_id": f"A-{n}"}

def deploy_after(a000_entry, extra=None):
    m = skel.AlgorithmMatrix()
    if a000_entry == "DELETE":
        del m.known["A-000"]
    elif a000_entry is not None:
        m.record("A-000", a000_entry)
    for k, v in (extra or {}).items():
        m.record(k, v)
    r = skel.governor_validate_and_deploy(m)
    return {"A-000_now": m.known.get("A-000"), "status": r["status"],
            "reason": r["reason"][:60]}

controls = {
    "C1_A000_missing": deploy_after("DELETE"),
    "C2_A000_reregistered_impostor": deploy_after({"name": "Impostor", "status": "ACTIVE"}),
    "C2b_A000_reregistered_impostor_with_tool": deploy_after(
        {"name": "Impostor", "status": "ACTIVE"}, {"A-101": {"name": "t", "status": "ACTIVE"}}),
    "C3_A1000": scan_real_matrix(["A-1000"]),
    "C4_A0999": scan_real_matrix(["A-0999"]),
    "C5a_arabic_indic_999": scan_real_matrix(["A-٩٩٩"]),
    "C5b_fullwidth_700": scan_real_matrix(["A-７００"]),
    "C5c_trailing_newline_700": scan_real_matrix(["A-700\n"]),
    "C6_SUB_namespace": scan_real_matrix(["SUB-R1", "SUB-999"]),
    "C0_fresh_matrix": scan_real_matrix([]),
    "C7_atomic_rollback": "see E102 probe (DISC-002-staged-bootstrap-e102-probe.py); not re-run",
    "C8_aliasing": "see E102 probe; not re-run",
    "C9_external_digest_source_census": {t: src.count(t) for t in
                                         ("hashlib", "sha256", "hmac", "digest(")},
}
print(json.dumps(controls, sort_keys=True, indent=1, default=str))
