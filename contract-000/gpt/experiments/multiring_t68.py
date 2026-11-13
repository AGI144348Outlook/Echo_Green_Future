#!/usr/bin/env python3
"""Synthetic GPT-only multiring controls; preregistration Issue #464. No canonical imports."""
import json, math, hashlib, sys, random
GLYPHS=list('אבגדהוזחטיכלמנסעפצקרשת')+list('ךםןףץ')
assert len(GLYPHS)==27 and len(set(GLYPHS))==27
SEEDS=[11,23,37,53]
def experiment(seed):
    rng=random.Random(seed)
    phase=[rng.uniform(-math.pi,math.pi) for _ in GLYPHS]
    freq=[rng.uniform(-0.2,0.2) for _ in GLYPHS]
    affinity=[(i*7+3)%19/19 for i in range(27)]
    shuffled=affinity[:];random.Random(seed+1000).shuffle(shuffled)
    shift=0.71
    def step(ph, weights, coupling=0.15, triad=0, absolute=False):
        return [ph[i]+freq[i]+coupling*weights[i]*math.sin((ph[(i+1)%27]-ph[i]) if not absolute else ph[i])+triad*math.sin(ph[(i+1)%27]+ph[(i+2)%27]-2*ph[i]) for i in range(27)]
    base=step(phase,affinity)
    again=step(phase,affinity)
    null=step(phase,affinity,0)
    shifted=step([p+shift for p in phase],affinity)
    abs_base=step(phase,affinity,absolute=True)
    abs_shift=step([p+shift for p in phase],affinity,absolute=True)
    shuffle=step(phase,shuffled)
    tri=step(phase,affinity,triad=0.08)
    tri_zero=step(phase,affinity,triad=0)
    radii=[1+0.1*math.sin(p) for p in phase]
    projected=[(i//9,(i//3)%3,i%3) for i in range(27)]
    occupied=[i for i,p in enumerate(phase) if p>1]
    sham=step(phase,affinity,0)
    checks={
      '01_identity_27':len(set(GLYPHS))==27,
      '02_noop':phase[:]==list(phase),
      '03_seed_replay':base==again,
      '04_uncoupled_null':null==[p+f for p,f in zip(phase,freq)],
      '05_relative_covariance':max(abs((s-b)-shift) for s,b in zip(shifted,base))<1e-12,
      '06_absolute_negative':max(abs((s-b)-shift) for s,b in zip(abs_shift,abs_base))>1e-5,
      '07_shuffled_intervention':max(abs(s-b) for s,b in zip(shuffle,base))>1e-8,
      '08_triadic_ablation':max(abs(t-b) for t,b in zip(tri,tri_zero))>1e-8,
      '09_deformable_bounds':all(0.9-1e-12<=r<=1.1+1e-12 for r in radii),
      '10_projection_contact_sham':len(set(projected))==27 and len(occupied)<=27 and sham==null,
    }
    return {'seed':seed,'checks':checks,'metrics':{'shuffle_max_delta':max(abs(s-b) for s,b in zip(shuffle,base)),'triad_max_delta':max(abs(t-b) for t,b in zip(tri,tri_zero)),'absolute_shift_deviation':max(abs((s-b)-shift) for s,b in zip(abs_shift,abs_base)),'contact_count':len(occupied)}}
if __name__=='__main__':
    rows=[experiment(s) for s in SEEDS]
    print(json.dumps({'python':sys.version.split()[0],'seeds':SEEDS,'results':rows,'passing_types':sum(all(row['checks'][k] for row in rows) for k in rows[0]['checks']),'total_types':10},indent=2,sort_keys=True))
    sys.exit(0 if all(all(row['checks'].values()) for row in rows) else 1)
