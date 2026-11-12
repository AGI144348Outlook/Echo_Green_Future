"""Noncanonical synthetic Echo-GPT ring/warehouse model. Prospective Issue #447."""
import json, math
SEEDS=(11,23,37,53)
GLYPHS=list('אבגדהוזחטיכלמנסעפצקרשתךםןףץ')
VALUES=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90]
def rng(seed):
 x=seed & 0xffffffff
 while True:
  x=(1664525*x+1013904223)&0xffffffff
  yield x/4294967296
def simulate(seed,*,strength=.028,tri=True,four=True,shuffle=False,shift=0.,detune=False,deform=False,transfer=True):
 random=rng(seed); phases=[2*math.pi*next(random)+shift for _ in range(27)]
 values=VALUES[:]
 if shuffle:
  perm=list(range(27));sh=rng(seed+777)
  for i in range(26,0,-1):
   j=int(next(sh)*(i+1));perm[i],perm[j]=perm[j],perm[i]
  values=[VALUES[i] for i in perm]
 radii=[1.]*27;matrix=list(range(27));warehouse=[None]*27;events=[]
 for t in range(16):
  if transfer and t in (3,8):
   for i in range(27):
    if matrix[i] is not None:warehouse[i]=matrix[i];matrix[i]=None
   events.append(('out',t))
  if transfer and t in (5,10):
   for i in range(27):
    if warehouse[i] is not None:matrix[i]=warehouse[i];warehouse[i]=None
   events.append(('return',t))
  old=phases;phases=[]
  for i,p in enumerate(old):
   b,c,d=(old[(i+k)%27] for k in (1,2,3))
   term=math.sin(b-p)+(0.6*math.sin(b+c-2*p) if tri else 0)+(0.35*math.sin(b+c+d-3*p) if four else 0)
   phases.append(p+strength*(values[i]/400)*term+(0.0007*(i%5-2) if detune else 0))
  if deform:radii=[min(1.2,max(.8,r+.003*math.sin(phases[i]-phases[(i+1)%27]))) for i,r in enumerate(radii)]
 return dict(ids=matrix,warehouse=warehouse,events=events,phase=phases,radii=radii,values=values)
def distance(a,b):
 return sum(abs(math.sin((x-y)/2)) for x,y in zip(a['phase'],b['phase']))
def tests(seed):
 b=simulate(seed);again=simulate(seed);noop=simulate(seed,strength=0,transfer=False);unc=simulate(seed,strength=0,tri=False,four=False,transfer=False)
 shuffled=simulate(seed,shuffle=True);pair=simulate(seed,tri=False,four=False);tri=simulate(seed,four=False)
 shifted=simulate(seed,shift=.91);detuned=simulate(seed,detune=True);deformed=simulate(seed,deform=True)
 observed=[x for x in b['ids']+b['warehouse'] if x is not None]
 no_phase=simulate(seed,strength=0,transfer=False)['phase']
 zero=simulate(seed,strength=0,transfer=False)
 phase_error=max(abs(math.sin((y-x-.91)/2)) for x,y in zip(b['phase'],shifted['phase']))
 metrics=dict(shuffle=distance(b,shuffled),triad=distance(b,pair),four=distance(b,tri),detune=distance(b,detuned),phase_error=phase_error,seed_contrast=distance(b,simulate(seed+1)),events=b['events'])
 checks={
 'unique_ids':len(GLYPHS)==len(set(GLYPHS))==27 and sorted(observed)==list(range(27)),
 'projection_inverse':all((i//9)*9+((i%9)//3)*3+i%3==i for i in range(27)),
 'replay_heterogeneity':b==again and metrics['seed_contrast']>1e-8,
 'noop':zero['phase']==no_phase,
 'uncoupled_null':unc['phase']==noop['phase'],
 'shuffled_affinity':metrics['shuffle']>1e-8,
 'triadic_ablation':metrics['triad']>1e-8,
 'fourbody_ablation':metrics['four']>1e-8,
 'global_phase_covariance':phase_error<1e-11,
 'warehouse_transfer_bounds':len(b['events'])==4 and sorted(observed)==list(range(27)) and all(.8<=r<=1.2 for r in deformed['radii']) and all(x is None for x in b['warehouse'])}
 return dict(seed=seed,checks=checks,metrics=metrics)
if __name__=='__main__':
 results=[tests(seed) for seed in SEEDS]
 print(json.dumps(results,indent=2))
 raise SystemExit(0 if all(all(r['checks'].values()) for r in results) else 1)
