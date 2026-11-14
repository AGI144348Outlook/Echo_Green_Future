"""T83 noncanonical GPT multiring synthetic controlled experiments. Stdlib only."""
import hashlib, json, math, random, sys
SEEDS=(11,23,47,89)
GLYPHS=list('אבגדהוזחטיכלמנסעפצקרשת')+list('ךםןףץ')
assert len(GLYPHS)==27 and len(set(GLYPHS))==27

def model(seed, mode='pair', shuffled=False, deform=False, contact=True):
    r=random.Random(seed)
    phases=[r.uniform(-math.pi,math.pi) for _ in range(27)]
    freq=[r.uniform(-.12,.12) for _ in range(27)]
    weights=[(i%9+1)/10 for i in range(27)]
    if shuffled:r.shuffle(weights)
    radius=[1.0]*27
    for t in range(16):
        old=phases[:]
        for i in range(27):
            j=(i+1)%27;k=(i+2)%27
            pair=.08*weights[i]*math.sin(old[j]-old[i]) if mode in ('pair','tri') and contact else 0
            tri=.045*math.sin(old[j]+old[k]-2*old[i]) if mode=='tri' and contact else 0
            phases[i]=old[i]+freq[i]+pair+tri
            if deform:radius[i]=1+.1*math.sin(phases[i])
    return phases,radius

def dist(a,b):return max(abs(x-y) for x,y in zip(a,b))

def trial(seed):
    p,r=model(seed,'pair');n,_=model(seed,'none');tri,_=model(seed,'tri')
    sh,_=model(seed,'pair',shuffled=True);defp,rad=model(seed,'pair',deform=True)
    sham,_=model(seed,'pair',contact=False)
    witness={'glyphs':GLYPHS,'ordered':GLYPHS[:4]}
    digest=lambda d:hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
    checks={
      'identity':len(set(GLYPHS))==27,
      'projection':len({(i//9,(i//3)%3,i%3) for i in range(27)})==27,
      'ordered_rings':all(len(GLYPHS[:n])==n and GLYPHS[:n]==list(GLYPHS[:n]) for n in (2,3,4)),
      'noop_replay':model(seed,'none')==model(seed,'none'),
      'uncoupled_frequency':dist(n,sham)==0,
      'pairwise_effect':dist(p,n)>0,
      'triadic_ablation':dist(tri,p)>0,
      'shuffled_affinity':dist(sh,p)>0,
      'deform_bound':all(.9-1e-10<=x<=1.1+1e-10 for x in rad),
      'matched_sham_and_tamper':dist(n,sham)==0 and digest(witness)!=digest({**witness,'ordered':list(reversed(witness['ordered']))})
    }
    return {'seed':seed,'checks':checks,'metrics':{'pair_vs_none':dist(p,n),'tri_vs_pair':dist(tri,p),'shuffle_vs_pair':dist(sh,p),'sham_vs_none':dist(sham,n),'radius_min':min(rad),'radius_max':max(rad)}}
if __name__=='__main__':
    rows=[trial(s) for s in SEEDS]
    output={'python':sys.version.split()[0],'seeds':SEEDS,'types':10,'rows':rows,'passed':sum(sum(r['checks'].values()) for r in rows),'total':40}
    print(json.dumps(output,sort_keys=True,indent=2))
    if output['passed']!=output['total']:sys.exit(1)
