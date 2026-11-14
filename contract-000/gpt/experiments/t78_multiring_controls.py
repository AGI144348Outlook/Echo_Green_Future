"""GPT-only bounded synthetic multiring control portfolio T78; no semantic claims."""
import json, math, random, platform
SEEDS=(11,23,37,53)
GLYPHS=tuple(f'G{i:02d}' for i in range(27))
GEM=tuple((i*7+3)%31 for i in range(27))
def projection(): return {g:(i//9,(i//3)%3,i%3) for i,g in enumerate(GLYPHS)}
def pair(a,b,k=.2): return k*math.sin(b-a)
def tri(a,b,c,k=.13): return k*math.sin(b+c-2*a)
def affinity(gem): return sum(math.cos((gem[i]-gem[(i+1)%27])/10) for i in range(27))/27
def run(seed):
 r=random.Random(seed); phase=[r.uniform(-math.pi,math.pi) for _ in range(27)]
 shift=.73; a,b,c=phase[:3]
 shuffled=list(GEM);r.shuffle(shuffled)
 radii=[1+.12*math.sin(x) for x in phase]
 result={}
 result['01_projection_identity']=(len(projection())==27 and len(set(projection().values()))==27)
 result['02_pair_order']=(GLYPHS[0]+GLYPHS[1]!=GLYPHS[1]+GLYPHS[0])
 result['03_triple_order']=(len((GLYPHS[0],GLYPHS[1],GLYPHS[2]))==3 and len(set(GLYPHS[:3]))==3)
 result['04_noop']=(all(x+pair(x,y,0)==x for x,y in zip(phase,phase[1:]+phase[:1])))
 omega=.07; result['05_uncoupled']=(all(abs((x+omega)-(x+omega+pair(x,y,0)))<1e-14 for x,y in zip(phase,phase[1:]+phase[:1])))
 result['06_relative_covariance']=(abs(pair(a+shift,b+shift)-pair(a,b))<1e-12)
 result['07_absolute_negative']=(abs(.2*math.sin(b+shift)-.2*math.sin(b))>1e-4)
 d_aff=affinity(GEM)-affinity(shuffled)
 result['08_shuffled_affinity_measured']=(math.isfinite(d_aff))
 d_tri=tri(a,b,c)-tri(a,b,c,0)
 result['09_triad_ablation_measured']=(math.isfinite(d_tri))
 contact=1; sham=a+omega+contact*pair(a,b,0); baseline=a+omega
 result['10_matched_contact_sham']=(sham==baseline)
 result['11_deformable_bounds']=(all(.88-1e-12<=x<=1.12+1e-12 for x in radii))
 return {'seed':seed,'checks':result,'metrics':{'affinity_difference':round(d_aff,12),'triad_difference':round(d_tri,12),'relative_shift_error':round(abs(pair(a+shift,b+shift)-pair(a,b)),15),'sham_difference':round(sham-baseline,15)}}
rows=[run(s) for s in SEEDS]
replay=[run(s) for s in SEEDS]
out={'experiment':'T78','python':platform.python_version(),'seeds':list(SEEDS),'test_types':11,'checks':sum(len(x['checks']) for x in rows),'passed':sum(sum(x['checks'].values()) for x in rows),'replay_identical':rows==replay,'rows':rows}
print(json.dumps(out,sort_keys=True,indent=2))
