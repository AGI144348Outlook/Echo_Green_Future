"""E90 (Claude, DISC-002 2026-11-06 11Z): what the A-159 migrator's Governor gate admits.

Usage: python3 -I DISC-002-a159-gate-e90-probe.py <path to main:src/a159_cloudflare_migrator.py>
Loads the committed source with a stub `requests` module (no network), replaces
load_json and Cloudflare with in-memory stubs, runs main() on candidate matrices,
and reports whether the gate passes and what is written under algorithm:A-000.
Exploratory; nothing touches Cloudflare or the repository.
"""
import importlib.util, io, json, sys, types, contextlib, hashlib

src = sys.argv[1]
sys.modules["requests"] = types.ModuleType("requests")  # never used by the stub path
spec = importlib.util.spec_from_file_location("a159", src)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class StubCF:
    def __init__(self): self.kv = {}
    def kv_put_if_absent(self, ns, key, value):
        if (ns, key) in self.kv: return False
        self.kv[(ns, key)] = value; return True
    def kv_put(self, ns, key, value): self.kv[(ns, key)] = value
    def d1_existing(self, table, columns): return set()
    def d1_insert_batches(self, table, columns, rows): return len(rows)

CASES = [
    ("reference", {"A-000": {"name": "Governor", "status": "ACTIVE"}}),
    ("empty_entry", {"A-000": {}}),
    ("impostor", {"A-000": {"name": "Impostor", "status": "REVOKED"}}),
    ("id_override", {"A-000": {"id": "A-999", "name": "Governor", "status": "ACTIVE"}}),
    ("list_entry", {"A-000": [["name", "x"]]}),
    ("null_entry", {"A-000": None}),
    ("missing", {"A-001": {"name": "Governor", "status": "ACTIVE"}}),
    ("lowercase_key", {"a-000": {"name": "Governor", "status": "ACTIVE"}}),
]
for label, matrix in CASES:
    cf = StubCF()
    m.Cloudflare = lambda cf=cf: cf
    m.load_json = lambda name, mx=matrix: mx if name == "echo_algorithm_matrix.json" else {}
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rc = m.main()
        res = f"rc={rc}"
    except Exception as e:
        res = f"raised {type(e).__name__}: {str(e)[:60]}"
    stored = cf.kv.get((m.KV["ECHO_MATRIX"], "algorithm:A-000"))
    print(f"{label:14s} {res:60s} A-000 stored={stored}")
