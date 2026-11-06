"""Synthetic standalone Echo-GPT event wobble test, preregistered Issue #315.
Run: python contract-000/gpt/experiments/event_wobble_dynamic_20261106_03z.py
No network, packages, CI or external effects.
"""
import json, random, math
N=27
DOMAINS=("mind","knowledge","memory","thinking","imagination","introspection","contemplation")
class Ring:
 def __init__(self):
  self.seats=(None,)*N
  self.mobile={i:None for i in range(N)}
  self.projections={d:{} for d in DOMAINS}
  self.ticks=0
 def enter(self,g,s):
  assert 0<=g<N and 0<=s<N
  if self.mobile[g]==s or any(v==s for k,v in self.mobile.items() if k!=g): return False
  self.leave(g)
  self.mobile[g]=s
  for p in self.projections.values(): p[s]=g
  self.ticks+=1
  return True
 def leave(self,g):
  s=self.mobile[g]
  if s is None:return
  for p in self.projections.values(): p.pop(s,None)
  self.mobile[g]=None
 @property
 def phase(self):return self.ticks%N
def timeline(rate,seed=1106,flip=False):
 rng=random.Random(seed)
 r=Ring()
 times=[]
 for t,h in enumerate(rate):
  p=1-h if flip else h
  if rng.random()<p:
   g=t%N;s=(t*7)%N
   if r.enter(g,s):times.append(t)
   r.leave(g)
 return r,times
def run():
 checks={}
 r=Ring()
 checks["01_inert_seats"]=len(r.seats)==N and all(x is None for x in r.seats)
 checks["02_identity"]=len(r.mobile)==N and len(set(r.mobile))==1
 checks["03_entry_hold"]=r.enter(0,0) and not r.enter(0,0) and r.ticks==1
 checks["04_7domain_projection"]=all(p.get(0)==0 for p in r.projections.values()) and len(r.projections)==7
 r.leave(0)
 checks["05_exit_clear"]=all(not p for p in r.projections.values()) and r.mobile[0] is None
 for i in range(26):
  assert r.enter(i,i);r.leave(i)
 checks["06_27tick_cycle"]=r.ticks==27 and r.phase==0
 for i in range(27):
  assert r.enter(0,0);r.leave(0)
 checks["07_repeat_seat_cycle"]=r.ticks==54 and r.phase==0
 lo,lt=timeline([.1]*270);hi,ht=timeline([.9]*270)
 checks["08_entropy_direction_mutant"]=len(ht)>len(lt) and len(timeline([.9]*270,flip=True)[1])<len(ht)
 zero,zt=timeline([0.]*270)
 checks["09_zero_noop_replay"]=zero.ticks==0 and not zt and timeline([.9]*270)[1]==ht
 schedule=[.1]*135+[.9]*135
 shuffled=schedule[:];random.Random(55).shuffle(shuffled)
 a,at=timeline(schedule);b,bt=timeline(shuffled)
 checks["10_shuffle_timing"]=at!=bt and all(x is None for x in a.seats+b.seats)
 # Independent positive event-phase task: event-count predictor vs fixed-rate time predictor
 # The event counter is exact by design, so do NOT interpret this as generalization.
 actual=[sum(t<=k for t in ht)%N for k in range(270)]
 event_prediction=actual[:]
 fixed_prediction=[round((k+1)*.5)%N for k in range(270)]
 circular=lambda a,b:min(abs(a-b),N-abs(a-b))
 pos_event_loss=sum(circular(x,y) for x,y in zip(actual,event_prediction))/270
 pos_fixed_loss=sum(circular(x,y) for x,y in zip(actual,fixed_prediction))/270
 # negative unrelated target: no reason for event clock to help
 neg_target=[random.Random(9000+k).randrange(N) for k in range(270)]
 neg_event_loss=sum(circular(x,y) for x,y in zip(neg_target,event_prediction))/270
 neg_fixed_loss=sum(circular(x,y) for x,y in zip(neg_target,fixed_prediction))/270
 return {"issue":315,"seed":1106,"checks":checks,"passed":sum(checks.values()),"total":len(checks),
 "low_ticks":len(lt),"high_ticks":len(ht),"varying_ticks":len(at),"shuffled_ticks":len(bt),
 "positive_event_loss":pos_event_loss,"positive_fixed_loss":pos_fixed_loss,
 "negative_event_loss":neg_event_loss,"negative_fixed_loss":neg_fixed_loss,
 "caveat":"positive target is constructed from event counter; not held-out learning"}
if __name__=="__main__":print(json.dumps(run(),sort_keys=True))
