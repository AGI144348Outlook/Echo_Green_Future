"""GPT-only experimental 27-seat warehouse ring; preregistered Issue #319.
Run: python contract-000/gpt/experiments/warehouse_ring_e86_07z.py
Synthetic offline; no canonical Echo, live Neon or private inputs.
"""
import json, math, random
N=27
class Ring:
 def __init__(self):
  self.seats=(None,)*N;self.occupied={};self.views=[{} for _ in range(7)];self.ticks=0
 def enter(self,g,s):
  if g not in range(N) or s not in range(N):return False
  if g in self.occupied or s in self.occupied.values():return False
  self.occupied[g]=s;self.ticks+=1
  for v in self.views:v[s]=g
  return True
 def leave(self,g):
  if g not in self.occupied:return False
  s=self.occupied.pop(g)
  for v in self.views:v.pop(s,None)
  return True
 def phase(self):return (self.ticks%N)*360/N
def events(schedule,seed=1106):
 rng=random.Random(seed)
 return [i for i,e in enumerate(schedule) if rng.random()<max(0,min(1,e))]
def dynamics(entries,coupling=.15):
 phases=[0.0]*7
 for t in entries:
  k=t%7;prior=phases[k]
  phases[k]=(prior+360/N)%360
  j=(k+1)%7
  phases[j]=(phases[j]+coupling*math.sin(math.radians(prior-phases[j])))%360
 return phases
def checks():
 o={}
 r=Ring()
 o["01_seats_cube"]=len(r.seats)==27 and all(x is None for x in r.seats) and len({(i%3,i//3%3,i//9) for i in range(27)})==27
 r.enter(0,0);snap=(r.ticks,dict(r.occupied),[dict(v) for v in r.views])
 o["02_glyph_guard"]=not r.enter(0,1) and snap==(r.ticks,r.occupied,r.views)
 o["03_seat_guard"]=not r.enter(1,0) and snap==(r.ticks,r.occupied,r.views)
 o["04_range_leave"]=not r.enter(27,2) and not r.enter(1,-1) and not r.leave(1) and snap==(r.ticks,r.occupied,r.views)
 o["05_projection_exit"]=len(r.views)==7 and all(v=={0:0} for v in r.views) and r.leave(0) and all(not v for v in r.views) and not r.occupied
 q=Ring();phases=[]
 for i in range(27):
  assert q.enter(i,i);phases.append(q.phase());q.leave(i)
 o["06_phase"]=all(math.isclose(phases[i-1],i*360/N if i<27 else 0,abs_tol=1e-9) for i in (1,13,26,27))
 p=dynamics([0]);a=dynamics([1,0]);expected=360/N+.15*math.sin(math.radians(-360/N))
 o["07_dynamics"]=len(p)==7 and math.isclose(p[0],360/N,abs_tol=1e-9) and all(math.isclose(v,0,abs_tol=1e-9) for v in p[1:]) and math.isclose(a[0],360/N,abs_tol=1e-9) and math.isclose(a[1],expected,abs_tol=1e-9) and all(math.isclose(v,0,abs_tol=1e-9) for v in a[2:])
 lo=events([.1]*270);hi=events([.9]*270);zero=events([0]*270);schedule=[.2]*135+[.8]*135;sh=schedule[:];random.Random(55).shuffle(sh);v=events(schedule);s=events(sh)
 o["08_rate_seed"]=len(lo)==22 and len(hi)==242 and len(v)==129 and len(s)==125 and not zero and events(schedule)==v and v!=s
 target=[(i*7+3)%27 for i in range(270)]
 def loss(ts):
  st=set(ts);return sum(min(abs(((i%27) if i in st else 0)-target[i]),27-abs(((i%27) if i in st else 0)-target[i])) for i in range(270))/270
 # independent expected value for circular distance, 26 to 0 is one
 o["10_exogenous"]=min(abs(26-0),27-abs(26-0))==1 and math.isfinite(loss(v)) and math.isfinite(loss(s)) and math.isfinite(loss([]))
 return o,{"low":len(lo),"high":len(hi),"varying":len(v),"shuffled":len(s),"event_loss":loss(v),"shuffled_loss":loss(s),"noop_loss":loss([]),"dynamics_1_0":a}
def run():
 base,metrics=checks()
 import pathlib
 source=pathlib.Path(__file__).read_text(encoding="utf8")
 mutants={
 "glyph_guard":("if g in self.occupied or s in self.occupied.values():return False","if s in self.occupied.values():return False",False),
 "seat_guard":("if g in self.occupied or s in self.occupied.values():return False","if g in self.occupied:return False",False),
 "range_guard":("if g not in range(N) or s not in range(N):return False","if False:return False",False),
 "leave_guard":("if g not in self.occupied:return False","if False:return False",False),
 "coupling_sign":("prior-phases[j]","phases[j]-prior",False),
 "coupling_target":("j=(k+1)%7","j=(k+3)%7",False),
 "domain_step":("prior+360/N","prior+360/7",False),
 "domain_key":("k=t%7;prior=phases[k]","k=(t//7)%7;prior=phases[k]",False),
 "phase_zero":("return (self.ticks%N)*360/N","return (self.ticks%N)*0",False),
 "seed_flip":("def events(schedule,seed=1106):","def events(schedule,seed=1107):",False),
 "equiv_step":("return (self.ticks%N)*360/N","return (self.ticks%N)*360.0/N",True),
 "equiv_guard":("if g not in range(N) or s not in range(N):return False","if not (0<=g<N and 0<=s<N):return False",True)
 }
 prefix,sep,suffix=source.partition("def run():");results={}
 for name,(old,new,equivalent) in mutants.items():
  if prefix.count(old)!=1:results[name]={"error":"anchor_count","count":prefix.count(old)};continue
  ns={"__name__":"injected_module","__file__":__file__}
  try:
   exec(compile(prefix.replace(old,new,1)+sep+suffix,__file__,"exec"),ns)
   test,_=ns["checks"]();failed=[k for k,v in test.items() if not v]
   results[name]={"equivalent":equivalent,"caught":bool(failed),"failed":failed}
  except Exception as exc:results[name]={"equivalent":equivalent,"caught":True,"exception":type(exc).__name__}
 base["09_mutation_table"]=all(("error" not in x and x["caught"]!=x["equivalent"]) for x in results.values())
 return {"issue":319,"seed":1106,"checks":base,"passed":sum(base.values()),"total":len(base),"metrics":metrics,"mutants":results}
if __name__=="__main__":print(json.dumps(run(),sort_keys=True,indent=2))
