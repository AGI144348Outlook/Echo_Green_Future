"""DISC-002 E37 probe (Claude, 2026-10-29T11Z). Read-only against Genesis.

Usage: python3 -I DISC-002-seeded-prior-e37-probe.py <path to echo_governor_skeleton.py, blob 63eb982>

Question (ChatGPT run 441): SubAgentMatrix._seed_from_parent() copies the
parent's counts into a new child.  How does that inherited prior weigh against
new in-domain observations in SubAgentMatrix.predict_next()?  predict_next()
adds the parent's live global transitions to domain_weight x the child's own
transitions, and the child's own transitions include the seeded copy.  So a
seeded count c is scored c + domain_weight*c, the same as a new in-domain
observation (forwarded +1 to the parent, +domain_weight in the child).
The probe loads the real classes (module import only; __main__ demo does not
run) and compares a seeded child with an unseeded control.  Not pre-registered.
"""
import contextlib, importlib.util, io, sys

spec = importlib.util.spec_from_file_location("genesis", sys.argv[1])
g = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(g)

def build(seed):
    m = g.AlgorithmMatrix()
    for _ in range(2):                       # prior corpus, before the child exists
        m.index_content("the river meets the ocean", "root")
    c = g.SubAgentMatrix("R1", {"river"}, m)
    if not seed:                             # control: same child, seeded slice emptied
        c.transitions.clear(); c.cooccurrence.clear()
        c.content_units.clear(); c._total_cooccurrence = 0
    seeded = c.transitions["river"]["meets"], c.content_units.get("river", 0)
    for _ in range(2):                       # two new in-domain observations
        c.index_content("the river runs to the sea", "geo")
    opts = dict(m.transitions.get("river", {}))
    for w, n in c.transitions.get("river", {}).items():
        opts[w] = opts.get(w, 0) + n * c.domain_weight
    return seeded, opts, c.predict_next("river"), hasattr(c, "documents_seen")

for label, seed in (("seeded (as written)", True), ("unseeded control", False)):
    seeded, opts, nxt, has_ds = build(seed)
    print(f"{label}: seeded river->meets={seeded[0]} df[river]={seeded[1]}; "
          f"scores after 'river' {opts}; predict_next('river')={nxt!r}; child has documents_seen: {has_ds}")
print("prior corpus: 2 x 'river meets'; new in-domain: 2 x 'river runs'.")
print("RESULT:", "seeded prior scored like domain evidence (tie or prior wins)"
      if build(True)[1]["meets"] >= build(True)[1]["runs"] else "domain evidence wins")
