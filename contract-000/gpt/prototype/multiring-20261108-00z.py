"""Standalone synthetic 27-slot multiring controls; no Echo canonical imports."""
import json, math, random
SEEDS=(3301,3302,3303,3304)
GLYPHS=list('אבגדהוזחטיכלמנסעפצקרשת')+list('ךםןףץ')
assert len(GLYPHS)==27
GEM=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90]
XYZ=[(i//9,(i//3)%3,i%3) for i in range(27)]
def neighbors(i):
 return [j for j,p in enumerate(XYZ) if sum(abs(a-b) for a,b in zip(XYZ[i],p))==1]
def step(a,k=.2):
 return [a[i]*(1-k)+k*sum(a[j] for j in neighbors(i))/len(neighbors(i)) for i in range(27)]
def rings(seed,n=2,coupled=True,shuffle=False,reverse=False):
 rng=random.Random(seed); weights=GEM[:]
 if shuffle:rng.shuffle(weights)
 phases=[rng.uniform(-math.pi,math.pi) for _ in range(n)]
 if reverse:phases=[-p for p in phases]
 values=[];radii=[]
 for t in range(12):
  rad=[1+.08*math.sin(.3*t+p) for p in phases];radii.extend(rad)
  for i in range(27):
   v=sum(math.sin(.27*t+p+(.001*weights[(i+k)%27] if coupled else 0))*rad[k] for k,p in enumerate(phases))/n
   values.append(v)
 return values,radii
def mse(a,b):return sum((x-y)**2 for x,y in zip(a,b))/len(a)
def evaluate(seed):
 a=[0.]*27;a[13]=1
 b=step(a); bb=step([0.]*27)
 base,rad=rings(seed);same,_=rings(seed)
 shuffled,_=rings(seed,shuffle=True); reversed_,_=rings(seed,reverse=True)
 uncoupled,_=rings(seed,coupled=False);triple,_=rings(seed,n=3)
 target=[.7*math.sin(.27*t+.19)+.3*math.cos(.11*t+.33) for t in range(12) for i in range(27)]
 checks={
 'identity_bijection':len(set(GLYPHS))==27 and len(set(XYZ))==27,
 'neighbor_degree':len(neighbors(13))==6 and len(neighbors(0))==3,
 'causal_neighbor':all(b[j]>0 for j in neighbors(13)),
 'nonneighbor_exclusion':all(b[j]==0 for j in range(27) if j!=13 and j not in neighbors(13)),
 'no_op':bb==[0.]*27,
 'deterministic_replay':base==same,
 'gematria_shuffle_sensitivity':base!=shuffled,
 'phase_reversal_sensitivity':base!=reversed_,
 'deformation_bound':all(.92-1e-12<=r<=1.08+1e-12 for r in rad),
 'independent_target_control':all(math.isfinite(mse(x,target)) for x in (base,uncoupled,shuffled,triple))
 }
 return {'seed':seed,'checks':checks,'mse':{'coupled':mse(base,target),'uncoupled':mse(uncoupled,target),'shuffled':mse(shuffled,target),'three_ring':mse(triple,target)},'neighbor_effect':sum(b[j] for j in neighbors(13))}
if __name__=='__main__':
 data=[evaluate(s) for s in SEEDS]
 print(json.dumps({'protocol':'issue-342','seeds':SEEDS,'results':data,'passed':sum(sum(v for v in x['checks'].values()) for x in data),'total':40},indent=2,sort_keys=True))
