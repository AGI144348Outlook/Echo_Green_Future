"""Synthetic event-ring causal checks, preregistered in Issue #316."""
import random, json, math
STEP=360/27
class Ring:
 def __init__(self,step=STEP,clear=True,wrong=False):
  self.seats=(None,)*27; self.occ={}; self.projections=[{} for _ in range(7)];self.ticks=0;self.step=step;self.clear=clear;self.wrong=wrong
 def phase(self):return (self.ticks*self.step)%360
 def enter(self,g,s):
  if self.occ.get(g)==s or s in self.occ.values():return False
  self.occ[g]=s;self.ticks+=1
  for p in self.projections:p[s]=(g+1)%27 if self.wrong else g
  return True
 def leave(self,g):
  if g not in self.occ:return False
  s=self.occ.pop(g)
  if self.clear:
   for p in self.projections:p.pop(s,None)
  return True
def events(schedule,seed=1106,invert=False):
 rng=random.Random(seed);return [i for i,e in enumerate(schedule) if rng.random() < max(0,min(1,1-e if invert else e))]
def run():
 c={};r=Ring();r.enter(0,0)
 c['angle_step']=math.isclose(r.phase(),STEP)
 z=Ring(step=0);z.enter(0,0);v=Ring(step=-STEP);v.enter(0,0)
 c['zero_reverse_mutants']=not math.isclose(z.phase(),STEP) and not math.isclose(v.phase(),STEP)
 r=Ring()
 for i in range(26):r.enter(i,i);r.leave(i)
 c['intermediate_phase']=math.isclose(r.phase(),26*STEP,abs_tol=1e-9)
 r.enter(26,26);c['27_cycle']=math.isclose(r.phase(),0,abs_tol=1e-9)
 r=Ring();r.enter(0,0);r.enter(0,0);c['hold_no_double_tick']=r.ticks==1
 r=Ring();r.enter(0,0);r.leave(0);stale=Ring(clear=False);stale.enter(0,0);stale.leave(0)
 c['seven_projection_clear']=all(not p for p in r.projections) and any(p for p in stale.projections)
 wrong=Ring(wrong=True);wrong.enter(0,0);c['wrong_glyph_detected']=all(p.get(0)!=0 for p in wrong.projections)
 low=events([.1]*270);high=events([.9]*270);c['entropy_direction']=len(high)>len(low)
 c['sign_flip_detected']=len(events([.9]*270,invert=True))<len(events([.1]*270,invert=True))
 c['zero_and_replay']=events([0]*270)==[] and events([.5]*270)==events([.5]*270)
 sched=[.2]*135+[.8]*135;shuffle=sched[:];random.Random(55).shuffle(shuffle)
 a=events(sched);b=events(shuffle);c['shuffle_temporal']=a!=b
 return {'issue':316,'checks':c,'passed':sum(c.values()),'total':len(c),'low_ticks':len(low),'high_ticks':len(high),'varying_ticks':len(a),'shuffled_ticks':len(b),'independent_target':'not evaluated; no claim'}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
