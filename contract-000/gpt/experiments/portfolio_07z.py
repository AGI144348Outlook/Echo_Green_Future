"""Noncanonical Echo-GPT ten-type bounded portfolio, prereg Issue #330 comment 6703646876.
No Genesis import, no network, no filesystem writes. Python 3 stdlib only.
Run: python3 -I -B portfolio_07z.py > results_07z.json
"""
import copy, hashlib, json, math, random, sys
SEEDS=tuple(range(1106,1136))
GLYPHS=tuple("אבגדהוזחטיכלמנסעפצקרשתךםןףץ")
VALUES=(1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,20,40,50,80,90)
def sha(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
def arrivals(seed):
    rng=random.Random(seed)
    return [(t,2*t+j) for t in range(40) for j in range(2) if rng.random()<.54]
def ledger(seed,dwell=3):
    inp=arrivals(seed); queue=[]; events=[]; occupied=None; until=-1
    for t in range(40+dwell+12):
        if occupied is not None and t>=until:
            events.append((t,"release",occupied));occupied=None
        for at,ident in inp:
            if at==t:
                queue.append((at,ident));events.append((t,"arrival",ident))
        queue2=[]
        for at,ident in queue:
            if t-at>=6:
                events.append((t,"expire",ident))
            else:queue2.append((at,ident))
        queue=queue2
        if occupied is None and queue:
            at,ident=queue.pop(0);occupied=ident;until=t+dwell
            events.append((t,"admit",ident))
    for at,ident in queue:events.append((40+dwell+12,"expire",ident))
    return dict(inputs=inp,events=events,dwell=dwell)
def oracle(p,reference):
    inp=reference; events=p["events"]; seen=set(); terminal=set(); seated=None; errs=[]
    expected={ident for _,ident in inp}; order={ident:i for i,(_,ident) in enumerate(inp)}
    waiting=[]; admission_times={}
    for t,k,i in sorted(events,key=lambda e:(e[0],{"release":0,"arrival":1,"expire":2,"admit":3}.get(e[1],4))):
        if k=="arrival":
            if i in seen or i not in expected:errs.append("arrival_census")
            seen.add(i);waiting.append(i)
        elif k=="admit":
            if i in terminal or i in admission_times:errs.append("double_admit")
            if seated is not None:errs.append("seat_overlap")
            if not waiting or i!=waiting[0]:errs.append("fifo")
            if i in waiting:waiting.remove(i)
            seated=i;admission_times[i]=t
        elif k=="release":
            if seated!=i:errs.append("seat_release")
            if i in admission_times and t-admission_times[i]!=p["dwell"]:errs.append("dwell")
            seated=None
            if i in terminal:errs.append("double_terminal")
            terminal.add(i)
        elif k=="expire":
            if i in terminal:errs.append("double_terminal")
            at=dict((ident,at) for at,ident in inp).get(i)
            if at is None or t-at<6:errs.append("early_expiry")
            if i in waiting:waiting.remove(i)
            terminal.add(i)
    if seen!=expected:errs.append("missing_arrival")
    if terminal!=expected:errs.append("missing_terminal")
    if seated is not None:errs.append("open_seat")
    return sorted(set(errs))
def ring(seed,n,mode):
    rng=random.Random(seed);phase=[rng.random()*math.tau for _ in range(n)]
    initial=phase[:]; values=list(VALUES)
    if mode=="shuffled":random.Random(seed+900).shuffle(values)
    cells=tuple((i//9,(i//3)%3,i%3) for i in range(27))
    history=[]
    for t in range(64):
        ids=[min(range(27),key=lambda k:abs(math.atan2(math.sin(p-math.tau*k/27),math.cos(p-math.tau*k/27)))) for p in phase]
        target=(.137*t+math.sin(.21*t))%math.tau
        pred=math.atan2(sum(math.sin(p) for p in phase),sum(math.cos(p) for p in phase))
        history.append(dict(ids=ids,phase=phase[:],loss=1-math.cos(pred-target)))
        old=phase[:]
        if mode!="noop":
            for i in range(n):
                drift=.04*math.sin(.13*t+i)
                coupling=0 if mode=="uncoupled" else .08*math.sin(old[(i+1)%n]-old[i])*values[ids[i]]/400
                deformation=.015*math.sin(.17*t+i) if mode=="deformable" else 0
                if mode=="projected":
                    a,b,c=cells[ids[i]]; deformation+=.002*(a-b+c-1)
                phase[i]=(old[i]+drift+coupling+deformation)%math.tau
    return dict(initial=initial,cells=cells,history=history,loss=sum(h["loss"] for h in history[32:])/32)
def run():
    rows=[]
    def row(kind,seed,ok,detail):rows.append(dict(type=kind,seed=seed,pass_=bool(ok),detail=detail))
    for seed in SEEDS:
        base=ledger(seed); ref=arrivals(seed); clean=oracle(base,ref)
        row("T1-conservation",seed,not clean,clean)
        row("T8-replay",seed,sha(base)==sha(ledger(seed)),sha(base))
        def mutate(name,operation,code):
            p=copy.deepcopy(base);changed=operation(p);errors=oracle(p,ref)
            activated=bool(changed and sha(p["events"])!=sha(base["events"]))
            row(name,seed,not clean and activated and code in errors,dict(activated=activated,errors=errors))
        def duplicate(p):
            e=next((e for e in p["events"] if e[1] in ("release","expire")),None)
            if not e:return False
            p["events"].append(e);return True
        mutate("T2-duplicate-terminal",duplicate,"double_terminal")
        def missing(p):
            e=next((e for e in p["events"] if e[1] in ("release","expire")),None)
            if not e:return False
            p["events"].remove(e);return True
        mutate("T3-missing-terminal",missing,"missing_terminal")
        def double(p):
            e=next((e for e in p["events"] if e[1]=="admit"),None)
            if not e:return False
            p["events"].append(e);return True
        mutate("T4-double-admission",double,"double_admit")
        def fifo(p):
            e=next((e for e in p["events"] if e[1]=="admit"),None)
            if not e:return False
            j=next((ident for _,ident in ref if ident!=e[2]),None)
            if j is None:return False
            p["events"][p["events"].index(e)]=(e[0],e[1],j);return True
        mutate("T5-fifo",fifo,"fifo")
        def dwell(p):
            e=next((e for e in p["events"] if e[1]=="release"),None)
            if not e:return False
            p["events"][p["events"].index(e)]=(e[0]+1,e[1],e[2]);return True
        mutate("T6-dwell",dwell,"dwell")
        def expiry(p):
            e=next((e for e in p["events"] if e[1]=="expire"),None)
            if not e:return False
            p["events"][p["events"].index(e)]=(e[0]-1,e[1],e[2]);return True
        mutate("T7-expiry",expiry,"early_expiry")
        other=ledger(seed,5)
        def counts(p):
            return {k:sum(e[1]==k for e in p["events"]) for k in ("admit","expire")}
        c1,c2=counts(base),counts(other)
        row("T9-dwell-intervention",seed,base["inputs"]==other["inputs"] and sha(base)==sha(ledger(seed)) and bool(c1!=c2),dict(base=c1,intervention=c2,delta={k:c2[k]-c1[k] for k in c1}))
        for n in (2,3,4):
            modes=("noop","uncoupled","coupled","shuffled","deformable","projected")
            rs={m:ring(seed,n,m) for m in modes}
            noop=rs["noop"]; frozen=all(h["phase"]==noop["initial"] for h in noop["history"])
            bijective=len(set(rs["projected"]["cells"]))==27
            valid=all(len(h["ids"])==n and all(0<=i<27 for i in h["ids"]) for r in rs.values() for h in r["history"])
            row("T10-ring-controls",seed,frozen and bijective and valid and all(math.isfinite(r["loss"]) for r in rs.values()),dict(n=n,losses={m:round(rs[m]["loss"],8) for m in modes},frozen=frozen,bijective=bijective))
    return rows
if __name__=="__main__":
    out=run()
    print(json.dumps(dict(schema="echo-gpt-07z",seeds=SEEDS,python=sys.version,counts={t:dict(total=sum(x["type"]==t for x in out),passed=sum(x["type"]==t and x["pass_"] for x in out)) for t in sorted({x["type"] for x in out})},rows=out),ensure_ascii=False,sort_keys=True,indent=2))
