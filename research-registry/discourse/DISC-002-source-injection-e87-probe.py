"""E87 (Claude, 2026-11-06 08Z): source-text injection into exact #320 blob 8e1619fe (commit c55a9721).
Same method as E85/E86: replace one unique anchor in the text before 'def evaluate():', exec, call the
unchanged evaluate(). Caught = passed<total or a crash. Stdlib only, offline. Exploratory, not a test of Echo."""
import json,sys,hashlib
src=open(sys.argv[1],encoding="utf8").read()
prefix,sep,suffix=src.partition("def evaluate():")
M={
 "F1_tick_double":("tick+=1;events","tick+=2;events"),
 "F2_sim_step_26":("phase[domain]=(phase[domain]+STEP)%360","phase[domain]=(phase[domain]+360/26)%360"),
 "F3_reverse_sign":("seat=(glyph+shift)%N","seat=(glyph-shift)%N"),
 "F4_coupling_target":("phase[(domain+1)%D]=(phase[(domain+1)%D]+.15*STEP)%360","phase[(domain+3)%D]=(phase[(domain+3)%D]+.15*STEP)%360"),
 "F5_coupling_gain":(".15*STEP",".9*STEP"),
 "F6_shift_domain":("shift=round(phase[glyph%D]/STEP)","shift=round(phase[0]/STEP)"),
 "F7_no_hold_guard":("assert glyph not in occupied and seat not in occupied.values()","pass"),
 "F8_reverse_reads_none":("if mode in ('both','reverse') else 0","if mode in ('both',) else 0"),
 "F9_radius_amp":("radius=1+.1*math","radius=1+.5*math"),
 "F10_one_view":("for v in views:v[seat]=glyph","views[0][seat]=glyph"),
 "F11_keep_occupancy":("del occupied[glyph]","pass"),
 "F12_event_index":("events.append(t)","events.append(t//2)"),
}
# F7 and F8 are behaviourally equivalent in this program (occupancy never exceeds 1; reverse never moves phase): controls.
EQUIV={"F7_no_hold_guard","F8_reverse_reads_none"}
def run(text):
    g={"__name__":"e87"}
    exec(compile(text,"<m>","exec"),g)
    r=g["evaluate"]()
    return r["passed"],r["total"],sorted(k for k,v in r["checks"].items() if not v)
out={"source_sha256":hashlib.sha256(src.encode()).hexdigest(),"baseline":run(src),"mutants":{}}
for k,(a,b) in M.items():
    assert prefix.count(a)==1,k
    try:
        p,t,f=run(prefix.replace(a,b)+sep+suffix); caught=p<t
    except Exception as e:
        f=["crash:"+type(e).__name__]; caught=True
    out["mutants"][k]={"caught":caught,"failed":f,"equivalent":k in EQUIV}
ne=[k for k in M if k not in EQUIV]
out["summary"]={"non_equivalent":len(ne),"caught":sum(out["mutants"][k]["caught"] for k in ne),
 "survivors":[k for k in ne if not out["mutants"][k]["caught"]],
 "equivalent_survive":[k for k in EQUIV if not out["mutants"][k]["caught"]]}
print(json.dumps(out,indent=1,sort_keys=True))
