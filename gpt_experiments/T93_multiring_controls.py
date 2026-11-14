import json, random, math, sys
SEEDS=(11,23,37,53)
GLYPHS=list('אבגדהוזחטיכלמנסעפצקרשת')+list('ךםןףץ')
COORDS=[(i//9,(i//3)%3,i%3) for i in range(27)]
def unique27(items): return len(items)==27 and len(set(items))==27
def circular(a,b): return sum(abs(math.atan2(math.sin(x-y),math.cos(x-y))) for x,y in zip(a,b))/len(a)
def simulate(seed,pair=.13,tri=.07,shuffle=False,deform=False,feedback=0,frequency=0):
 r=random.Random(seed); phase=[r.uniform(-math.pi,math.pi) for _ in range(27)]; w=[r.uniform(.01,.08)+frequency for _ in range(27)]; affinity=list(range(27)); radius=[1.]*27
 if shuffle:r.shuffle(affinity)
 for step in range(24):
  old=phase[:]; previous_radius=radius[:]
  for i in range(27):
   j=(i+1)%27;k=(i+2)%27
   coupling=pair*math.sin(old[j]-old[i])*(1+affinity[i]/100)+tri*math.sin(old[j]+old[k]-2*old[i])
   phase[i]=old[i]+w[i]+coupling*(1+feedback*(previous_radius[i]-1))
   if deform:radius[i]=max(.85,min(1.15,1+.1*math.sin(phase[i])))
 return phase,radius
def run(seed):
 base,rr=simulate(seed);replay,_=simulate(seed);null,_=simulate(seed,0,0);nop,_=simulate(seed,0,0)
 pair,_=simulate(seed,pair=0);tri,_=simulate(seed,tri=0);shuffled,_=simulate(seed,shuffle=True)
 null_shuffle,_=simulate(seed,0,0,shuffle=True);rigid,_=simulate(seed,deform=False,feedback=0)
 warped,wr=simulate(seed,deform=True,feedback=0);active,ar=simulate(seed,deform=True,feedback=2)
 compose=lambda indices:''.join(GLYPHS[i] for i in indices)
 wrap=circular(base,[v+2*math.pi for v in null])
 tests={
 'identity_mutation_rejection':unique27(GLYPHS) and not unique27(GLYPHS+[GLYPHS[0]]),
 'projection_collision_rejection':unique27(COORDS) and not unique27(COORDS+[COORDS[0]]),
 'ring_order_reversal':all(compose(list(range(n)))!=compose(list(reversed(range(n)))) for n in (2,3,4)),
 'deterministic_replay':base==replay,
 'noop_uncoupled':null==nop,
 'circular_wrap_metric':0<=circular(base,null)<=math.pi and abs(circular(base,null)-wrap)<1e-12,
 'pairwise_ablation':circular(base,pair)>1e-9,
 'triadic_ablation':circular(base,tri)>1e-9,
 'shuffled_affinity_null':circular(base,shuffled)>1e-9 and circular(null,null_shuffle)==0,
 'boundary_feedback':rr==[1.]*27 and all(.85<=v<=1.15 for v in wr+ar) and circular(rigid,warped)==0 and circular(warped,active)>1e-9}
 return {'seed':seed,'tests':tests,'metrics':{'pair_circular':circular(base,pair),'tri_circular':circular(base,tri),'shuffle_circular':circular(base,shuffled),'uncoupled_shuffle':circular(null,null_shuffle),'feedback_circular':circular(warped,active),'feedback_disabled':circular(rigid,warped),'radius_min':min(ar),'radius_max':max(ar)}}
if __name__=='__main__':
 results=[run(s) for s in SEEDS]; print(json.dumps({'python':sys.version.split()[0],'seeds':SEEDS,'results':results,'passed':sum(sum(x['tests'].values()) for x in results),'total':sum(len(x['tests']) for x in results)},indent=2,sort_keys=True))
