"""GPT-only independent-phase event-ring trial; preregistered Issue #321.
No network, canonical modifications, or real entropy. Python 3 stdlib.
"""
import json, math, random
N=27
D=7
STEP=360/N
class Ring:
    def __init__(self,seed=1106,mode="both",dwell=3):
        self.rng=random.Random(seed+909)
        self.phase=[self.rng.uniform(1,15) for _ in range(D)]
        self.mode=mode
        self.dwell=dwell
        self.seats=(None,)*N
        self.occupied={}
        self.views=[{} for _ in range(D)]
        self.tick=0
        self.events=[]
    def angle(self):
        return (self.tick%N)*STEP
    def enter(self,g,s,t):
        if not (isinstance(g,int) and isinstance(s,int) and 0<=g<N and 0<=s<N):
            return False
        if g in self.occupied or any(item[0]==s for item in self.occupied.values()):
            return False
        self.occupied[g]=(s,t+self.dwell)
        for v in self.views:v[s]=g
        self.tick+=1
        self.events.append((t,g,s,self.tick,self.angle()))
        if self.mode in ("both","forward"):
            d=g%D
            self.phase[d]=(self.phase[d]+STEP)%360
            self.phase[(d+1)%D]=(self.phase[(d+1)%D]+0.15*STEP)%360
        return True
    def leave(self,g):
        if g not in self.occupied:return False
        s,_=self.occupied.pop(g)
        for v in self.views:v.pop(s,None)
        return True
    def expire(self,t):
        for g,(s,until) in list(self.occupied.items()):
            if t>=until:self.leave(g)
    def choose(self,g):
        shift=round(self.phase[g%D]/STEP) if self.mode in ("both","reverse") else 0
        return (g+shift)%N

def simulate(seed,mode="both",schedule=None):
    if schedule is None:schedule=[.2]*135+[.8]*135
    schedule=tuple(schedule)
    rng=random.Random(seed)
    r=Ring(seed,mode)
    for t,e in enumerate(schedule):
        r.expire(t)
        if rng.random()<max(0,min(1,e)):
            g=t%N
            r.enter(g,r.choose(g),t)
    return {"ticks":r.tick,"events":r.events,"phase":r.angle(),
            "warehouse_phase":r.phase,"views":r.views,"occupied":r.occupied,
            "entropy_unchanged":schedule==tuple(schedule),"seats":r.seats}

def evaluate():
    checks={}
    r=Ring()
    checks["01_glyph_guard"]=r.enter(0,0,0) and not r.enter(0,1,1) and r.tick==1
    checks["02_seat_guard"]=not r.enter(1,0,1) and r.tick==1
    checks["03_invalid_inputs"]=all(not r.enter(g,s,1) for g,s in [(27,2),(-1,2),(2,27),(2,-1)])
    checks["04_leave_absent"]=not r.leave(5) and r.tick==1
    checks["05_projection_dwell"]=all(v.get(0)==0 for v in r.views) and (r.expire(2) is None) and all(v.get(0)==0 for v in r.views) and (r.expire(3) is None) and all(not v for v in r.views)
    q=Ring()
    for t in range(26):
        assert q.enter(t,t,t)
        q.leave(t)
    before=q.angle()
    assert q.enter(26,26,26)
    checks["06_trajectory_closure"]=abs(before-26*STEP)<1e-8 and abs(q.angle())<1e-8 and q.tick==27 and len(q.events)==27
    zero=simulate(1106,schedule=[0]*270)
    checks["07_zero_rate"]=zero["ticks"]==0
    low=simulate(1106,schedule=[.1]*270)
    high=simulate(1106,schedule=[.9]*270)
    checks["08_entropy_rate"]=high["ticks"]>low["ticks"] and low["entropy_unchanged"] and high["entropy_unchanged"]
    none=simulate(1106,"none")
    reverse=simulate(1106,"reverse")
    forward=simulate(1106,"forward")
    both=simulate(1106,"both")
    checks["09_reverse_intervention"]=reverse["events"]!=none["events"] and reverse["ticks"]==none["ticks"]
    checks["10_forward_bidirectional"]=forward["warehouse_phase"]!=none["warehouse_phase"] and both["events"]!=forward["events"] and both["ticks"]==forward["ticks"]
    shuffled=[.2]*135+[.8]*135
    random.Random(55).shuffle(shuffled)
    sh=simulate(1106,"both",shuffled)
    return {"issue":321,"seed":1106,"checks":checks,"passed":sum(checks.values()),"total":len(checks),
            "ticks":{"zero":zero["ticks"],"low":low["ticks"],"high":high["ticks"],"none":none["ticks"],"forward":forward["ticks"],"reverse":reverse["ticks"],"both":both["ticks"],"shuffled":sh["ticks"]},
            "phase":{"both":both["phase"],"reverse":reverse["phase"]},
            "choice_differences":{"reverse_vs_none":reverse["events"]!=none["events"],"both_vs_forward":both["events"]!=forward["events"]},
            "replay":simulate(1106,"both")["events"]==both["events"],
            "limitations":"Synthetic entropy; independent phase is seeded; no semantic learning, real Neon entropy or independent task gain."}
if __name__=="__main__":print(json.dumps(evaluate(),sort_keys=True,indent=2))
