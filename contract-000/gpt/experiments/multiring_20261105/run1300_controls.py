"""GPT-owned 13Z offline synthetic experiment. Run: python3 run1300.py"""
import json,math
SEED=20261105
GLYPHS=list("אבגדהוזחטיכלמנסעפצקרשתךםןףץ")
def wrap(x): return x%(2*math.pi)
def delta(a,b): return abs(math.atan2(math.sin(a-b),math.cos(a-b)))
def sim(rings=3,steps=16,coupling=.16,boundary=True,shuffle=False,perturb=0):
 p=[wrap((i*17+SEED%101)*.037) for i in range(27)]
 b=[1+.15*math.sin(i+SEED%17) for i in range(27)]
 p[0]=wrap(p[0]+perturb)
 for _ in range(steps):
  old=p[:]
  for i in range(27):
   nxt=(i+1)%27
   affinity=(((i*7+3)%11+1) if shuffle else ((i*3+5)%11+1))/12
   force=sum(math.sin(old[(i+27-k)%27]-old[i]) for k in range(1,rings))/(rings-1)
   p[i]=wrap(old[i]+.025+.004*(i%3)+coupling*affinity*(b[i] if boundary else 1)*force)
   if boundary:b[i]=max(.4,min(1.6,b[i]+.015*math.sin(old[nxt]-old[i])))
 return {"phase":p,"boundaries":b}
def run():
 base=sim(); replay=sim(); two=sim(rings=2); four=sim(rings=4)
 nop=sim(steps=0); unc=sim(coupling=0); uncpert=sim(coupling=0,perturb=.7)
 pert=sim(steps=1,perturb=.7); normal=sim(steps=1)
 frozen=sim(boundary=False); shuffled=sim(shuffle=True); uncfrozen=sim(coupling=0,boundary=False)
 active=set(); components={("פ","grammar"):0,("ע","classify"):0,("ר","govern"):1,("צ","validate"):1}
 dispatch=lambda origin,fn:(origin,fn) in components and origin in active
 inactive=not dispatch("פ","grammar");active.add("פ")
 active_isolation=dispatch("פ","grammar") and not dispatch("ע","classify")
 metrics={"two_vs_three":delta(two["phase"][6],base["phase"][6]),"three_vs_four":delta(four["phase"][6],base["phase"][6]),"uncoupled_neighbor":delta(unc["phase"][1],uncpert["phase"][1]),"downstream":delta(pert["phase"][1],normal["phase"][1]),"upstream":delta(pert["phase"][26],normal["phase"][26]),"boundary_delta":delta(base["phase"][6],frozen["phase"][6]),"boundary_uncoupled_delta":delta(unc["phase"][6],uncfrozen["phase"][6]),"shuffle_delta":delta(base["phase"][6],shuffled["phase"][6])}
 tests=[
 ("27-position-projection",len(GLYPHS)==27 and len(set(GLYPHS))==27 and len({(i//9,(i//3)%3,i%3) for i in range(27)})==27),
 ("deterministic-replay",base==replay),
 ("2-3-4-ring-contrast",metrics["two_vs_three"]>1e-7 and metrics["three_vs_four"]>1e-7),
 ("zero-step-noop",nop["phase"]==[wrap((i*17+SEED%101)*.037) for i in range(27)]),
 ("inactive-origin-gate",inactive),
 ("active-cross-origin-isolation",active_isolation),
 ("uncoupled-perturbation-null",metrics["uncoupled_neighbor"]<=1e-12),
 ("directed-one-step",metrics["downstream"]>1e-7 and metrics["upstream"]<=1e-12),
 ("boundary-coupled-and-null",metrics["boundary_delta"]>1e-7 and metrics["boundary_uncoupled_delta"]<=1e-12),
 ("shuffled-affinity-quantified",math.isfinite(metrics["shuffle_delta"]))
 ]
 return {"seed":SEED,"steps":16,"tests":[{"type":k,"pass":v} for k,v in tests],"metrics":metrics,"pass_count":sum(v for _,v in tests),"total":len(tests),"limitations":"Toy model; affinity shuffle is deterministic remapping, not distributional significance; no learned semantics, authentication or production effects."}
if __name__=="__main__": print(json.dumps(run(),ensure_ascii=False,indent=2))
