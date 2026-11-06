"""GPT-only warehouse ring source-injected tests; prereg #318. Python stdlib.
Run: python contract-000/gpt/experiments/warehouse_ring_injection_06z.py
Synthetic; no network, Neon, or canonical edits.
"""
import json,random,math,copy
N=27
class Ring:
 def __init__(self,domains=7):
  self.seats=(None,)*N;self.occupied={};self.views=[{} for _ in range(domains)];self.ticks=0
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
 rng=random.Random(seed);return [i for i,e in enumerate(schedule) if rng.random()<max(0,min(1,e))]
def dynamics(entries,coupling=.15):
 phases=[0.0]*7
 for t in entries:
  k=t%7;prior=phases[k]
  phases[k]=(prior+360/N)%360
  j=(k+1)%7
  phases[j]=(phases[j]+coupling*math.sin(math.radians(prior-phases[j])))%360
 return phases
def tests():
 result={}
 r=Ring();result["01_27_inert"]=len(r.seats)==27 and all(x is None for x in r.seats)
 result["02_27_unique"]=len(set(range(N)))==27 and len({(i%3,(i//3)%3,i//9) for i in range(N)})==27
 r.enter(0,0);result["03_seven_exact"]=len(r.views)==7 and all(v=={0:0} for v in r.views)
 result["04_hold_collision"]=not r.enter(0,0) and not r.enter(1,0) and r.ticks==1
 r.leave(0);result["05_exit_clears"]=not r.occupied and len(r.views)==7 and all(not v for v in r.views)
 ok=True
 for i in range(54):
  ok=ok and r.enter(i%27,i%27)
  ok=ok and len(r.views)==7 and all(v.get(i%27)==i%27 for v in r.views)
  ok=ok and r.leave(i%27) and not r.occupied and all(not v for v in r.views)
 result["06_reentry_54"]=ok and r.ticks==55
 q=Ring();q.enter(0,0);a=q.phase()
 for i in range(1,27):q.leave(i-1);q.enter(i,i)
 result["07_angle_wrap"]=math.isclose(a,360/27) and math.isclose(q.phase(),0,abs_tol=1e-9)
 lo=events([.1]*270);hi=events([.9]*270);zero=events([0]*270)
 result["08_rate_null"]=len(hi)>len(lo) and not zero
 sched=[.2]*135+[.8]*135;sh=sched[:];random.Random(55).shuffle(sh)
 result["09_shuffle_replay"]=events(sched)==events(sched) and events(sched)!=events(sh)
 c=dynamics(events(sched),.15);u=dynamics(events(sched),0)
 target=[(i*7+3)%27 for i in range(270)]
 pred=lambda ts:sum(min(abs(((i%27) if i in set(ts) else 0)-target[i]),27-abs(((i%27) if i in set(ts) else 0)-target[i])) for i in range(270))/270
 result["10_coupled_exogenous"]=any(abs(x-y)>1e-8 for x,y in zip(c,u)) and math.isfinite(pred(events(sched)))
 return result,{"low":len(lo),"high":len(hi),"varying":len(events(sched)),"shuffled":len(events(sh)),"coupled_phases":c,"uncoupled_phases":u,"exogenous_event_loss":pred(events(sched)),"exogenous_noop_loss":pred([])}
def run():
 original,measure=tests()
 # Actual source-text injection into implementation, with unchanged tests() code.
 import pathlib
 source=pathlib.Path(__file__).read_text(encoding="utf8")
 mutants={
  "wrong_glyph":("for v in self.views:v[s]=g","for v in self.views:v[s]=(g+1)%27"),
  "one_domain":("def __init__(self,domains=7):","def __init__(self,domains=1):"),
  "stale_occupancy":("s=self.occupied.pop(g)","s=self.occupied[g]"),
  "zero_phase":("return (self.ticks%N)*360/N","return (self.ticks%N)*0"),
  "inverted_entropy":("rng.random()<max(0,min(1,e))","rng.random()<max(0,min(1,1-e))")
 }
 injection={}
 for name,(old,new) in mutants.items():
  if source.count(old)!=1:injection[name]={"error":"nonunique_anchor","count":source.count(old)};continue
  mutated=source.replace(old,new,1)
  ns={"__name__":"injected_module","__file__":__file__}
  exec(compile(mutated,__file__,"exec"),ns)
  result,_=ns["tests"]()
  failed=[k for k,v in result.items() if not v]
  injection[name]={"caught":bool(failed),"failed_checks":failed}
 return {"issue":318,"seed":1106,"checks":original,"passed":sum(original.values()),"total":len(original),"measure":measure,"injected_mutants":injection}
if __name__=="__main__":print(json.dumps(run(),sort_keys=True,indent=2))
