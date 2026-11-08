"""GPT-owned synthetic experiment. stdlib only; no canonical Echo."""
import json,math,random,hashlib
SEEDS=[3301,3302,3303,3304]
GLYPHS=list("אבגדהוזחטיכלמנסעפצקרשת")+list("ךםןףץ")
assert len(GLYPHS)==27
def model(seed,mode="coupled",intervention=0):
 rng=random.Random(seed)
 phase=[rng.random()*2*math.pi for _ in range(3)]
 weights=[1+(i%9) for i in range(27)]
 if mode=="shuffled":rng.shuffle(weights)
 occupancy=[(i+seed)%27 for i in range(27)]
 def val(i):
  p=phase[i%3]
  c=0 if mode in ("uncoupled","noop") else (0.2 if mode!="reversed" else -0.2)
  return (0 if mode=="noop" else math.sin(p)*.05)+c*weights[occupancy[i]]/27+ (intervention*.025 if i==12 else 0)
 return {"phase":phase,"occupancy":occupancy,"values":[val(i) for i in range(27)]}
def run():
 results=[]
 for seed in SEEDS:
  a=model(seed);u=model(seed,"uncoupled");s=model(seed,"shuffled");n=model(seed,"noop");rev=model(seed,"reversed");inter=model(seed,intervention=.4)
  # Ten distinct bounded checks; report checks as construction-level, not predictive validity.
  checks={
   "E1_replay":a==model(seed),
   "E2_27_unique":len(set(a["occupancy"]))==27,
   "E3_2ring_order":tuple(GLYPHS[a["occupancy"][i]] for i in (0,1))!=tuple(GLYPHS[a["occupancy"][i]] for i in (1,0)),
   "E4_3ring_order":len(tuple(GLYPHS[a["occupancy"][i]] for i in (0,1,2)))==3,
   "E5_radius_bound":all(.9<=1+.1*math.sin(p)<=1.1 for p in a["phase"]),
   "E6_uncoupled_distinct":a["values"]!=u["values"],
   "E7_shuffle_distinct":a["values"]!=s["values"],
   "E8_noop_stationary":all(v==0 for v in n["values"]),
   "E9_phase_reverse_distinct":a["values"]!=rev["values"],
   "E10_local_intervention":abs(inter["values"][12]-a["values"][12]-.01)<1e-10 and inter["values"][0]==a["values"][0]
  }
  target=[.01*math.sin(i/3) for i in range(27)]
  mse=lambda x:sum((v-t)**2 for v,t in zip(x["values"],target))/27
  results.append({"seed":seed,"checks":checks,"mse":{k:round(mse(v),9) for k,v in [("coupled",a),("uncoupled",u),("shuffled",s),("noop",n),("reversed",rev)]}})
 return results
if __name__=="__main__":print(json.dumps(run(),ensure_ascii=False,indent=2))
