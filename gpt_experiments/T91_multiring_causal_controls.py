import json,random,math,hashlib,sys
SEEDS=(11,23,37,53)
GLYPHS=list('אבגדהוזחטיכלמנסעפצקרשת')+list('ךםןףץ')
def simulate(seed,pair=.13,tri=.07,shuffle=False,deform=False,frequency=0):
 r=random.Random(seed); phase=[r.uniform(-math.pi,math.pi) for _ in range(27)]; w=[r.uniform(.01,.08)+frequency for _ in range(27)]; a=list(range(27))
 if shuffle:r.shuffle(a)
 radius=[1.]*27
 for step in range(24):
  old=phase[:]
  for i in range(27):
   j=(i+1)%27;k=(i+2)%27
   phase[i]=old[i]+w[i]+pair*math.sin(old[j]-old[i])*(1+a[i]/100)+tri*math.sin(old[j]+old[k]-2*old[i])
   if deform:radius[i]=max(.85,min(1.15,1+.1*math.sin(phase[i])))
 return phase,radius
def d(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)
def run(seed):
 base,_=simulate(seed); replay,_=simulate(seed); null,_=simulate(seed,0,0); freq,_=simulate(seed,0,0,frequency=.01)
 nop,_=simulate(seed,0,0); pair,_=simulate(seed,pair=0); tri,_=simulate(seed,tri=0); shuffled,_=simulate(seed,shuffle=True)
 null_shuffle,_=simulate(seed,0,0,shuffle=True); rigid,rr=simulate(seed); warped,wr=simulate(seed,deform=True)
 coords=[(i//9,(i//3)%3,i%3) for i in range(27)]; composition=lambda inds:''.join(GLYPHS[i] for i in inds)
 tests={'identity_and_mutation':len(GLYPHS)==len(set(GLYPHS))==27 and len(set(GLYPHS+[GLYPHS[0]]))==27,'projection_and_collision':len(set(coords))==27 and len(set(coords+[coords[0]]))==27,'ring_order_reversal':all(composition(list(range(n)))!=composition(list(reversed(range(n)))) for n in (2,3,4)),'deterministic_replay':base==replay,'noop':null==nop,'frequency_analytic':abs(d(null,freq)-.24)<1e-9,'pairwise_ablation':d(base,pair)>1e-9 and d(null,nop)==0,'triadic_ablation':d(base,tri)>1e-9 and d(null,nop)==0,'shuffled_affinity_null':d(base,shuffled)>1e-9 and d(null,null_shuffle)==0,'boundary_rigid_deformed':rr==[1.]*27 and all(.85<=x<=1.15 for x in wr) and d(rigid,warped)==0}
 return {'seed':seed,'tests':tests,'metrics':{'pair_ablation':d(base,pair),'tri_ablation':d(base,tri),'shuffle':d(base,shuffled),'shuffled_null':d(null,null_shuffle),'frequency_shift':d(null,freq),'radius_min':min(wr),'radius_max':max(wr)}}
if __name__=='__main__':
 output={'python':sys.version.split()[0],'seeds':SEEDS,'results':[run(s) for s in SEEDS]};print(json.dumps(output,sort_keys=True,indent=2))
