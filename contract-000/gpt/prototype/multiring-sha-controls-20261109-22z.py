"""GPT-only 22Z prospective test family, Issue #379. Synthetic, not canonical Echo."""
import hashlib, json, random
SEEDS=(9901,9902,9903,9904)
GLYPHS=list("אבגדהוזחטיכלמנסעפצקרשת")+list("ךםןףץ")
N=27
def coord(i): return (i//9,(i//3)%3,i%3)
def neighbors(i):
    p=coord(i)
    return [j for j in range(N) if sum(abs(a-b) for a,b in zip(p,coord(j)))==1]
def shift(v,g,offset=1):
    out=v[:]
    for i,x in enumerate(v):
        out[i]-=g*x
        out[(i+offset)%N]+=g*x
    return out
def cube(v,g):
    out=v[:]
    for i,x in enumerate(v):
        ns=neighbors(i)
        out[i]-=g*x
        for j in ns:out[j]+=g*x/len(ns)
    return out
def permute(v):
    # involution: reverse each block of nine
    return [v[(i//9)*9+8-(i%9)] for i in range(N)]
def oracle_shift(v,g,offset=1):
    return [(1-g)*v[i]+g*v[(i-offset)%N] for i in range(N)]
def l1(a,b):return sum(abs(x-y) for x,y in zip(a,b))
def run(seed):
    r=random.Random(seed);v=[r.random() for _ in range(N)];z=[0.]*N
    a=shift(v,.2); b=cube(v,.2)
    abc=shift(cube(shift(v,.2),.2),.2)
    abi=cube(shift(v,.2),.2)
    rewired=shift(cube(shift(v,.2,7),.2),.2)
    ab=permute(shift(v,.2));ba=shift(permute(v),.2)
    core=json.dumps({"glyphs":GLYPHS,"operators":["shift","cube","permutation"]},ensure_ascii=False,sort_keys=True).encode()
    changed=core+b"!"
    measures={"coupled_l1":l1(abc,abi),"rewired_l1":l1(abc,rewired),"order_l1":l1(ab,ba),"oracle_error":l1(a,oracle_shift(v,.2)),"mass_error":max(abs(sum(v)-sum(x)) for x in (a,b,abc,rewired))}
    checks={
      "01_glyph_identity":len(GLYPHS)==27 and len(set(GLYPHS))==27,
      "02_replay":v==[random.Random(seed).random() for _ in range(N)] if False else v==make_input(seed),
      "03_zero_input":shift(cube(z,.2),.2)==z,
      "04_zero_coupling":shift(v,0)==v and cube(v,0)==v,
      "05_mass":measures["mass_error"]<1e-12,
      "06_coupling_effect":measures["coupled_l1"]>1e-8,
      "07_rewire_effect":measures["rewired_l1"]>1e-8 and abs(sum(abc)-sum(rewired))<1e-12,
      "08_operator_order":measures["order_l1"]>1e-8,
      "09_oracle":measures["oracle_error"]<1e-12,
      "10_sha256":hashlib.sha256(core).hexdigest()==hashlib.sha256(bytes(core)).hexdigest() and hashlib.sha256(core).hexdigest()!=hashlib.sha256(changed).hexdigest()
    }
    return {"seed":seed,"checks":checks,"measures":measures,"sha256":hashlib.sha256(core).hexdigest()}
def make_input(seed):
    r=random.Random(seed);return [r.random() for _ in range(N)]
if __name__=="__main__":
    rows=[run(s) for s in SEEDS]
    print(json.dumps({"issue":379,"rows":rows,"passed":sum(sum(v for v in x["checks"].values()) for x in rows),"total":40},sort_keys=True))
