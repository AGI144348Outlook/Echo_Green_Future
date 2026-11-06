"""E85 source-injection probe (Claude, DISC-002, 2026-11-06T06Z).
Reads GPT #317 source bytes (blob 9c85ae9e, commit c07bfb80) from a path argument,
applies one textual mutation at a time to the SHIPPED code, and runs its unchanged check().
M08 is a deliberate equivalent mutant (control): it must SURVIVE.
A mutant is "caught" if check() reports passed < total or raises. stdlib only.
Usage: python3 -I this.py path/to/projection_causal_05z.py
"""
import hashlib, json, sys, types
src = open(sys.argv[1], encoding="utf-8").read()
MUTANTS = [
 ("M01 phase() constant 0", "def phase(self):return (self.ticks%N)*360/N", "def phase(self):return 0.0"),
 ("M02 enter drops glyph-occupied guard", "if g in self.occ or s in self.occ.values():return False", "if s in self.occ.values():return False"),
 ("M03 enter drops seat-occupied guard", "if g in self.occ or s in self.occ.values():return False", "if g in self.occ:return False"),
 ("M04 enter drops both guards", "if g in self.occ or s in self.occ.values():return False", "pass"),
 ("M05 loss ignores events (phase frozen)", "  if i in ts:phase=(phase+1)%N", "  pass"),
 ("M06 loss non-circular distance", "min(abs(a-b),N-abs(a-b))", "abs(a-b)"),
 ("M07 event_times ignores schedule (always fire)", "if r.random()<max(0,min(1,x))", "if True"),
 ("M08 EQUIVALENT control (same writes, restructured loop)", "  for p in self.projections:p[s]=(g+1)%N if self.wrong else g", "  self.projections[0][s]=g\n  for p in self.projections[1:]:p[s]=g"),
 ("M09 leave keeps projections", "  for p in self.projections:p.pop(s,None)", "  pass"),
 ("M10 leave double-ticks", "  if self.release:del self.occ[g]", "  if self.release:del self.occ[g]\n  self.ticks+=1"),
 ("M11 shared projection dict x7", "self.projections=[{} for _ in range(domains)]", "self.projections=[{}]*domains"),
 ("M12 wrong glyph by default", "p[s]=(g+1)%N if self.wrong else g", "p[s]=(g+1)%N"),
 ("M13 no occupancy release by default", "if self.release:del self.occ[g]", "pass"),
 ("M14 coupling formula zeroed", "coupled=child+.25*math.sin(parent-child)", "coupled=child+.25*math.sin(0)+1e-3"),
]
def run(code):
    m = types.ModuleType("m317"); exec(compile(code, "<m317>", "exec"), m.__dict__)
    r = m.check(); return r["passed"], r["total"]
print("source_sha256", hashlib.sha256(src.encode()).hexdigest())
base = run(src); print("baseline", base)
res = []
for name, old, new in MUTANTS:
    assert src.count(old) == 1, name
    try:
        p, t = run(src.replace(old, new)); caught = p < t; note = f"{p}/{t}"
    except Exception as e:
        caught, note = True, "raised " + type(e).__name__
    res.append((name, caught, note)); print(("CAUGHT  " if caught else "SURVIVES"), name, note)
print("caught", sum(c for _, c, _ in res), "of", len(res))
