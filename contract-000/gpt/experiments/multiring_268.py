"""Inert deterministic multi-ring geometry prototype. Pretest: Issue #268.
No semantic interpretation, real-world physics, external effects or AI inference.
"""
import json, math, random, hashlib, sys
GLYPHS = tuple("אבגדהוזחטיכלמנסעפצקרשתךםןףץ")
VALUES = (1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90)
assert len(GLYPHS)==len(VALUES)==len(set(GLYPHS))==27
TAU=2*math.pi

def affinity(a,b):
    lo,hi=sorted((a,b))
    return 1.0 if hi%lo==0 else math.gcd(lo,hi)/hi

def simulate(variant, n, seed=173, steps=32, shuffle=False):
    if variant not in ("independent","coupled","deformable","matrix"): raise ValueError(variant)
    if n not in (2,3,4): raise ValueError(n)
    rng=random.Random(seed)
    values=list(VALUES)
    if shuffle: rng.shuffle(values)
    # Each ring contains all 27 glyphs; ring slots are ordered composition positions.
    angles=[[TAU*j/27+rng.uniform(-.08,.08) for j in range(27)] for _ in range(n)]
    centers=[0.0]*n
    radii=[1.0]*n
    for t in range(steps):
        new=[]
        for r in range(n):
            current=[]
            for j in range(27):
                theta=angles[r][j]
                # Baseline drift depends only on ring and glyph index.
                delta=.014*(r+1)+.002*math.sin(t*.13+j)
                if variant in ("coupled","deformable","matrix"):
                    other=(r+1)%n
                    k=(j+3)%27
                    delta+=.03*affinity(values[j],values[k])*math.sin(angles[other][k]-theta)
                current.append((theta+delta)%TAU)
            new.append(current)
        angles=new
        if variant=="deformable":
            radii=[1+.12*math.sin(.1*t+r) for r in range(n)]
        elif variant=="matrix":
            radii=[1+.04*math.sin(.07*t+r) for r in range(n)]
    # Selection is angular proximity to a common readout ray; not learned language.
    chosen=[min(range(27),key=lambda j:abs(math.atan2(math.sin(angles[r][j]-centers[r]),math.cos(angles[r][j]-centers[r])))) for r in range(n)]
    word="".join(GLYPHS[j] for j in chosen)
    # Circular coherence of selected phases, not linguistic quality.
    coherence=abs(sum(complex(math.cos(angles[r][chosen[r]]),math.sin(angles[r][chosen[r]])) for r in range(n)))/n
    # The matrix variant uses fixed 3x3x3 addresses; movement is only a projection.
    addresses={GLYPHS[j]:(j//9,(j//3)%3,j%3) for j in range(27)}
    return dict(variant=variant,n=n,word=word,selected=chosen,coherence=round(coherence,9),
                radii=[round(x,9) for x in radii],addresses=addresses,
                unique_ids=len(addresses),bounds_ok=all(.8<=x<=1.2 for x in radii))

def run():
    cases=[]
    for variant in ("independent","coupled","deformable","matrix"):
        for n in (2,3,4):
            a=simulate(variant,n)
            assert a==simulate(variant,n), "replay differs"
            assert len(a["word"])==n and a["unique_ids"]==27 and a["bounds_ok"]
            assert len(set(a["addresses"].values()))==27
            cases.append({k:v for k,v in a.items() if k!="addresses"})
    controls={}
    for variant in ("independent","coupled","deformable","matrix"):
        base=simulate(variant,3)
        shuffled=simulate(variant,3,shuffle=True)
        controls[variant]=dict(base_word=base["word"],shuffled_word=shuffled["word"],
                               base_coherence=base["coherence"],shuffled_coherence=shuffled["coherence"])
    print(json.dumps({"python":sys.version.split()[0],"cases":cases,"controls":controls,
                      "passed":len(cases),"claims":"geometry only; no meaning or emergence inferred"},ensure_ascii=False,sort_keys=True,indent=2))
if __name__=="__main__": run()
