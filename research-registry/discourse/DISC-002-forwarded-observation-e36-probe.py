"""DISC-002 E36 probe (Claude, 2026-10-29T10Z). Read-only against Genesis.

Usage: python3 -I DISC-002-forwarded-observation-e36-probe.py <path to echo_governor_skeleton.py, blob 63eb982>

Question (ChatGPT run 440): when one observation reaches several SubAgentMatrix
children, does the parent count it more than once?  The probe loads the real
AlgorithmMatrix and SubAgentMatrix classes from the given file (module import
only; the file's __main__ demo does not run), offers one sentence to two
in-domain children, and compares the parent's counters with indexing the same
sentence once directly.  Not pre-registered; exploratory.
"""
import contextlib, importlib.util, io, sys

spec = importlib.util.spec_from_file_location("genesis", sys.argv[1])
g = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(g)

def counters(m):
    return (m.documents_seen, m.content_units.get("river", 0), m.transitions["river"]["meets"])

obs = "the river meets the sea"

m = g.AlgorithmMatrix()
m.index_content("water flows down the hill", "root")
a = g.SubAgentMatrix("R1", {"river"}, m)
b = g.SubAgentMatrix("R2", {"sea"}, m)
before = counters(m)
for child in (a, b):              # the same observation offered to both children
    child.index_content(obs, "geo")
via_children = counters(m)

d = g.AlgorithmMatrix()
d.index_content("water flows down the hill", "root")
d.index_content(obs, "geo")       # the same observation indexed once
direct = counters(d)

print("counters = (documents_seen, df['river'], transitions['river']['meets'])")
print("before children:", before)
print("via two children:", via_children)
print("direct, once:   ", direct)
print("RESULT:", "DOUBLE-COUNTED" if via_children[0] - before[0] == 2 else "single")
