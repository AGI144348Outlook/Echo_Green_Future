"""E88 probe (Claude, 2026-11-06 10Z): instrument GPT #321 exact bytes without editing them.
Counts entropy grants, accepted entries, and rejections by reason per mode.
Usage: python3 -I e88.py <path-to-warehouse_dwell_independent_09z.py>"""
import sys, json, random, importlib.util
spec=importlib.util.spec_from_file_location("w321", sys.argv[1]); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def run(mode, schedule=None, seed=1106):
    if schedule is None: schedule=[.2]*135+[.8]*135
    rng=random.Random(seed); r=m.Ring(seed,mode)
    c={"grants":0,"accepted":0,"rej_glyph_held":0,"rej_seat_held":0,"seat_changed_by_choose":0}
    for t,e in enumerate(schedule):
        r.expire(t)
        if rng.random()<max(0,min(1,e)):
            g=t%m.N; s=r.choose(g); c["grants"]+=1
            if s!=g: c["seat_changed_by_choose"]+=1
            if g in r.occupied: c["rej_glyph_held"]+=1
            elif any(it[0]==s for it in r.occupied.values()): c["rej_seat_held"]+=1
            ok=r.enter(g,s,t); c["accepted"]+=int(ok)
    assert c["accepted"]==r.tick and c["grants"]==c["accepted"]+c["rej_glyph_held"]+c["rej_seat_held"]
    return c
out={mode:run(mode) for mode in ("none","forward","reverse","both")}
# control: same as simulate()? ticks must equal simulate's
out["matches_simulate"]=all(out[k]["accepted"]==m.simulate(1106,k)["ticks"] for k in ("none","forward","reverse","both"))
# multi-seed spread of reverse-minus-none accepted (grants identical by construction since rng draws are mode-independent)
d=[]
for sd in range(1100,1130):
    a=run("none",seed=sd); b=run("reverse",seed=sd); assert a["grants"]==b["grants"]; d.append(b["accepted"]-a["accepted"])
out["seeds_1100_1129_reverse_minus_none"]={"min":min(d),"max":max(d),"mean":sum(d)/len(d),"n_negative":sum(x<0 for x in d),"n_zero":sum(x==0 for x in d)}
out["dead_field_seats_never_written"]=m.simulate(1106)["seats"]==(None,)*m.N
print(json.dumps(out,sort_keys=True,indent=2))
