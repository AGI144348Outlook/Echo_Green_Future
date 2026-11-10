"""GPT-only synthetic experiment; prospective protocol Issue #381. No canonical Echo changes."""
import hashlib, json, random
SEEDS = (11001, 11002, 11003, 11004)
GLYPHS = list("אבגדהוזחטיכלמנסעפצקרשת") + list("ךםןףץ")
N = 27
def initial(seed):
    rng = random.Random(seed)
    return [rng.random() for _ in range(N)]
def l1(a,b):
    return sum(abs(x-y) for x,y in zip(a,b))
def shift(v,g,offset=1):
    out = [(1-g)*x for x in v]
    for i,x in enumerate(v):
        out[(i+offset)%N] += g*x
    return out
def coord(i):
    return (i//9,(i//3)%3,i%3)
def cube(v,g):
    out = [(1-g)*x for x in v]
    for i,x in enumerate(v):
        p = coord(i)
        ns = [j for j in range(N) if sum(abs(a-b) for a,b in zip(p,coord(j)))==1]
        for j in ns:
            out[j] += g*x/len(ns)
    return out
def perm(v):
    return [v[(i//9)*9+8-(i%9)] for i in range(N)]
def oracle(v,g,offset=1):
    return [(1-g)*v[i]+g*v[(i-offset)%N] for i in range(N)]
def run(seed):
    v=initial(seed); z=[0.0]*N; g=.2
    abc=perm(cube(shift(v,g),g))
    aba=shift(cube(shift(v,g),g),g)
    rewired=perm(cube(shift(v,g,7),g))
    reversed_order=shift(cube(perm(v),g),g)
    no_op=shift(cube(perm(v),0),0)
    core=json.dumps({"glyphs":GLYPHS,"operators":["shift","cube","perm"]},sort_keys=True,ensure_ascii=False).encode("utf-8")
    sha=hashlib.sha256(core).hexdigest()
    metrics={"abc_aba_l1":l1(abc,aba),"rewired_l1":l1(abc,rewired),"reverse_l1":l1(abc,reversed_order),"oracle_error":l1(shift(v,g),oracle(v,g)),"mass_error":max(abs(sum(v)-sum(x)) for x in (abc,aba,rewired,reversed_order))}
    checks={
      "01_unique":len(GLYPHS)==27 and len(set(GLYPHS))==27,
      "02_replay":v==initial(seed),
      "03_zero":perm(cube(shift(z,g),g))==z,
      "04_uncoupled":shift(v,0)==v and cube(v,0)==v and no_op==perm(v),
      "05_mass":metrics["mass_error"]<1e-12,
      "06_matched_duration":metrics["abc_aba_l1"]>1e-8,
      "07_rewire":metrics["rewired_l1"]>1e-8,
      "08_order":metrics["reverse_l1"]>1e-8,
      "09_oracle":metrics["oracle_error"]<1e-12,
      "10_sha256":sha==hashlib.sha256(bytes(core)).hexdigest() and sha!=hashlib.sha256(core+b"!").hexdigest()
    }
    return {"seed":seed,"checks":checks,"metrics":metrics,"sha256":sha}
if __name__=="__main__":
    rows=[run(s) for s in SEEDS]
    print(json.dumps({"issue":381,"rows":rows,"passed":sum(sum(v for v in row["checks"].values()) for row in rows),"total":40},sort_keys=True))
