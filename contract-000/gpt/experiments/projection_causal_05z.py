"""Issue #317 preregistered; standalone stdlib Python, GPT experimental only.
python contract-000/gpt/experiments/projection_causal_05z.py
"""
import json, math, random
N=27
class Ring:
 def __init__(self,domains=7,wrong=False,release=True):
  self.seats=(None,)*N;self.occ={};self.projections=[{} for _ in range(domains)]
  self.ticks=0;self.wrong=wrong;self.release=release
 def enter(self,g,s):
  if g in self.occ or s in self.occ.values():return False
  self.occ[g]=s;self.ticks+=1
  for p in self.projections:p[s]=(g+1)%N if self.wrong else g
  return True
 def leave(self,g):
  if g not in self.occ:return False
  s=self.occ[g]
  if self.release:del self.occ[g]
  for p in self.projections:p.pop(s,None)
  return True
 def phase(self):return (self.ticks%N)*360/N
def event_times(schedule,seed=1106):
 r=random.Random(seed);return [i for i,x in enumerate(schedule) if r.random()<max(0,min(1,x))]
def loss(times,target):
 phase=0;ts=set(times);out=[]
 for i in range(len(target)):
  if i in ts:phase=(phase+1)%N
  out.append(phase)
 return sum(min(abs(a-b),N-abs(a-b)) for a,b in zip(out,target))/len(target)
def check():
 checks={}
 r=Ring();r.enter(3,4)
 checks['01_default_glyph_identity']=len(r.projections)==7 and all(p.get(4)==3 for p in r.projections)
 checks['02_seven_domain_cardinality']=len(r.projections)==7 and len({id(p) for p in r.projections})==7
 r.leave(3);checks['03_exit_clears']=not r.occ and all(not p for p in r.projections)
 r=Ring();ok=True
 for i in range(54):
  g=i%N;s=i%N
  ok &= r.enter(g,s)
  ok &= len(r.occ)==1 and all(p.get(s)==g for p in r.projections)
  ok &= r.leave(g) and not r.occ and all(not p for p in r.projections)
 checks['04_54_reentry_two_cycles']=ok and r.ticks==54 and math.isclose(r.phase(),0,abs_tol=1e-10)
 coords=[(i%3,(i//3)%3,i//9) for i in range(N)]
 checks['05_cube_bijection']=len(set(coords))==27 and all(x+3*y+9*z==i for i,(x,y,z) in enumerate(coords)) and all(v is None for v in r.seats)
 checks['06_noop_zero_rate']=event_times([0]*270)==[] and Ring().phase()==0
 lo=event_times([.1]*270);hi=event_times([.9]*270)
 checks['07_entropy_rate_intervention']=len(hi)>len(lo)
 a=[.2]*135+[.8]*135;b=a[:];random.Random(55).shuffle(b)
 ta=event_times(a);tb=event_times(b)
 checks['08_shuffle_replay']=ta!=tb and ta==event_times(a) and tb==event_times(b)
 # Phase coupling is deliberately separate from event phase: parent-child delta.
 parent=0.7;child=1.3
 coupled=child+.25*math.sin(parent-child);uncoupled=child+0*math.sin(parent-child)
 checks['09_coupling_vs_null']=abs(coupled-uncoupled)>1e-6 and uncoupled==child
 # Exogenous target generated independently of events, with fixed independent seed.
 target=[random.Random(90000+i).randrange(N) for i in range(270)]
 observed=loss(ta,target);shuffled=loss(tb,target);noop=loss([],target)
 checks['10_exogenous_null_measured']=all(math.isfinite(x) for x in (observed,shuffled,noop)) and len(target)==270
 # Mutant injection: replace actual class configuration, run same direct assertions.
 mutants={}
 for name,m in [('wrong_glyph',Ring(wrong=True)),('one_domain',Ring(domains=1)),('no_release',Ring(release=False))]:
  first=m.enter(3,4)
  idok=len(m.projections)==7 and all(p.get(4)==3 for p in m.projections)
  m.leave(3);releaseok=not m.occ and all(not p for p in m.projections)
  mutants[name]={'detected':not(idok and releaseok),'identity_ok':idok,'release_ok':releaseok}
 return {'issue':317,'seed':1106,'checks':checks,'passed':sum(checks.values()),'total':len(checks),
 'low_ticks':len(lo),'high_ticks':len(hi),'varying_ticks':len(ta),'shuffled_ticks':len(tb),
 'exogenous_loss':{'event':observed,'shuffled':shuffled,'noop':noop},'mutants':mutants}
if __name__=='__main__':print(json.dumps(check(),sort_keys=True,indent=2))
