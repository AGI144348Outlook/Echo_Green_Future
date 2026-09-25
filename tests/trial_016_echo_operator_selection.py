# Trial 016 execution marker
#!/usr/bin/env python3
"""Trial 016 — ECHO Operator Selection.

Tests the currently implemented Governor Propose→Validate→Govern→Select path
without supplying a Hebrew/Mashet answer in the harness.
Expected first-run outcome may be NO_SELECTION: that is an experimental result.
"""
from __future__ import annotations
import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def load_governor():
    p=ROOT/"src"/"echo_governor_skeleton.py"
    spec=importlib.util.spec_from_file_location("echo_governor_skeleton",p)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

GOAL="Create a new working object that preserves the information contained in both Notebook objects A and B. Do not alter A or B."
A={"handle":"N::X::A","value":["alpha"],"status":"WORKING"}
B={"handle":"N::X::B","value":["beta"],"status":"WORKING"}

def main():
    gov=load_governor()
    glyphs=load("matrices/glyphs/hebrew_glyph_registry.json")
    manual=load("matrices/symbols/mashet_instruction_manual.json")
    algebra=load("matrices/symbols/algebra_mashet.json")

    # Expose the available tool space as data. The harness does not rank it.
    primitives=[{"kind":"HEBREW","glyph":r["glyph"],"operation":r["operation"]} for r in glyphs["records"]]
    primitives += [{"kind":"MASHET","id":r["id"],"symbol":r["symbol"],"role":r["source_role"],
                    "execution":r["execution"]} for r in manual["cards"]]
    primitives += [{"kind":"ALGEBRA_MASHET","id":r["id"],"mashet":r["mashet"],
                    "signature":r["signature"],"law_status":r["law_status"]} for r in algebra["records"]]

    deficiency={"id":"T016-GOAL","type":"GOAL","observed":GOAL,"magnitude":1.0,"status":"CONFIRMED",
                "operands":[A["handle"],B["handle"]]}
    theta={"goal":GOAL,"operands":[A["handle"],B["handle"]]}
    trace=[{"stage":"GOAL","actor":"HARNESS","value":GOAL},
           {"stage":"TOOLSPACE","actor":"NOTEBOOK","count":len(primitives)}]

    candidates=gov.propose([deficiency],theta,primitives)
    trace.append({"stage":"PROPOSE","actor":"ECHO_GOVERNOR_CODE","candidates":candidates})

    validated=[]
    for c in candidates:
        ok,margin=gov.validate(c,[])
        governed=gov.govern(c,{}, {})
        validated.append({"candidate":c,"valid":ok,"margin":margin,"governed":governed})
    trace.append({"stage":"VALIDATE_GOVERN","actor":"ECHO_GOVERNOR_CODE","candidates":validated})

    eligible=[x["candidate"] for x in validated if x["valid"] and x["governed"]]
    selected=gov.select(eligible) if eligible else None
    trace.append({"stage":"SELECT","actor":"ECHO_GOVERNOR_CODE","selected":selected})

    # Selection counts only if ECHO's returned candidate actually names a
    # Hebrew operation and Mashet dependency from the exposed tool space.
    operational=bool(selected and
        (selected.get("hebrew") or selected.get("glyph") or selected.get("hebrew_operation")) and
        (selected.get("mashet") or selected.get("mashet_id") or selected.get("algebra_handle")))
    noop=bool(selected and selected.get("m_id")=="M-000-NOOP")
    status="OPERATOR_SELECTION_OBSERVED" if operational else "NO_OPERATIONAL_SELECTION"
    if noop: status="NOOP_STUB_SELECTED"

    out={"trial":"016","name":"ECHO Operator Selection","status":status,
         "research_label":"OBSERVED_CURRENT_GOVERNOR_IMPLEMENTATION",
         "goal":GOAL,"inputs":[A,B],"toolspace_count":len(primitives),
         "candidate_count":len(candidates),"selected":selected,
         "operational_selection":operational,"noop_stub_selected":noop,"trace":trace}
    dest=ROOT/"artifacts"/"trial_016_trace.json"; dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,indent=2))
    # A scientifically meaningful NO_SELECTION is not a CI failure.
    return 0

if __name__=="__main__": raise SystemExit(main())
