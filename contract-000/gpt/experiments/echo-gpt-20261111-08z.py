"""Echo-GPT 08Z independent synthetic multiring model. Preregistered Issue #414."""
import json, math, random, hashlib
SEEDS=(11,23,37,53)
N=27
def simulate(seed, rings=2, gain=.16, steps=12, phase_shift=0., relative_shift=0., freq_scale=1., shuffle=False):
    rng=random.Random(seed)
    mass=[[1.0+(.12*math.sin(i*1.3+j*.7)) for i in range(N)] for j in range(rings)]
    # Equal total initial mass for 2/3 rings; first two ring profiles same shape, but rescaled for 3.
    scale=2.0/rings
    mass=[[x*scale for x in row] for row in mass]
    initial=[row[:] for row in mass]
    freq=[.12+.015*j+.001*i for j in range(rings) for i in range(N)]
    perm=list(range(N))
    if shuffle:rng.shuffle(perm)
    for t in range(steps):
        for j in range(rings):
            k=(j+1)%rings
            if j>=k:continue
            for i in range(N):
                a=mass[j][i];c=mass[k][i]
                phase_j=(freq[j*N+i]*freq_scale*t+phase_shift+(relative_shift if j==0 else 0))
                phase_k=(freq[k*N+i]*freq_scale*t+phase_shift)
                affinity=.6+.4*math.cos((i-perm[i])*.11)
                coupling=gain*affinity*(.5+.5*math.cos(phase_j-phase_k))
                transfer=coupling*(a-c)
                mass[j][i]-=transfer
                mass[k][i]+=transfer
    return {"mass":mass,"initial":initial,"projection":[sum(row[i] for row in mass) for i in range(N)],"total":sum(map(sum,mass)),"ids":list(range(N))}
def l1(a,b):return sum(abs(x-y) for x,y in zip(a,b))
def flatten(a):return [x for row in a for x in row]
def evaluate(seed):
    base=simulate(seed)
    replay=simulate(seed)
    zero=simulate(seed,gain=0)
    uncoupled=simulate(seed,gain=0,steps=20,freq_scale=1.7)
    common=simulate(seed,phase_shift=.77)
    relative=simulate(seed,relative_shift=1.3)
    frequency=simulate(seed,freq_scale=1.8)
    shuffled=simulate(seed,shuffle=True)
    three=simulate(seed,rings=3)
    # ring resolved comparisons, topology uses aggregate only because dimensions differ
    drel=l1(flatten(base["mass"]),flatten(relative["mass"]))
    dfreq=l1(flatten(base["mass"]),flatten(frequency["mass"]))
    dshuf=l1(flatten(base["mass"]),flatten(shuffled["mass"]))
    dthree=l1(base["projection"],three["projection"])
    tests={
      "T1_replay":base==replay,
      "T2_conservation":abs(base["total"]-sum(map(sum,base["initial"])))<1e-9,
      "T3_nonnegative":min(flatten(base["mass"]))>=0,
      "T4_zero_gain":zero["mass"]==zero["initial"],
      "T5_uncoupled":uncoupled["mass"]==uncoupled["initial"],
      "T6_global_phase":l1(flatten(base["mass"]),flatten(common["mass"]))<1e-9,
      "T7_relative_phase":drel>1e-6,
      "T8_frequency":dfreq>1e-6,
      "T9_shuffled_affinity":dshuf>1e-6,
      "T10_three_ring_projection":dthree>1e-6
    }
    return {"seed":seed,"tests":tests,"metrics":{"relative_ring_l1":drel,"frequency_ring_l1":dfreq,"shuffled_ring_l1":dshuf,"three_ring_projected_l1":dthree,"common_phase_ring_l1":l1(flatten(base["mass"]),flatten(common["mass"])),"relative_projected_l1":l1(base["projection"],relative["projection"]),"conservation_error":abs(base["total"]-sum(map(sum,base["initial"]))) }}
if __name__=="__main__":
    rows=[evaluate(s) for s in SEEDS]
    print(json.dumps({"protocol":"Issue #414","seeds":SEEDS,"results":rows,"passed":sum(sum(r["tests"].values()) for r in rows),"total":len(rows)*10},indent=2,sort_keys=True))
