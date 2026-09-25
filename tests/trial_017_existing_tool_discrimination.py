#!/usr/bin/env python3
"""Trial 017 — Can ECHO's existing learning substrate discriminate tools?
No operator execution; no preferred answer encoded."""
import importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def govmod():
 p=ROOT/"src"/"echo_governor_skeleton.py"; s=importlib.util.spec_from_file_location("g",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def words(x): return " ".join(re.findall(r"[A-Za-z]+",str(x))).lower()
def main():
 g=govmod(); matrix=g.AlgorithmMatrix()
 goal="Create a new working object that preserves the information contained in both Notebook objects A and B. Do not alter A or B."
 glyphs=load("matrices/glyphs/hebrew_glyph_registry.json")["records"]
 manual=load("matrices/symbols/mashet_instruction_manual.json")["cards"]
 tools=[]
 for r in glyphs: tools.append({"kind":"HEBREW","id":r["glyph"],"text":words(r)})
 for r in manual: tools.append({"kind":"MASHET","id":r["id"],"text":words(r)})
 # Give every tool description and the goal to ECHO's existing A-102 substrate.
 goal_units=matrix.index_content(goal,"goal")
 rows=[]
 for t in tools:
  u=matrix.index_content(t["text"],"tool")
  rows.append({**t,"similarity":matrix.tfidf_similarity(goal_units,u)})
 rows.sort(key=lambda x:(-x["similarity"],x["kind"],x["id"]))
 nonzero=[r for r in rows if r["similarity"]>0]
 out={"trial":"017","question":"Can existing ECHO A-102 discriminate available operator descriptions relative to an unseen goal?",
      "status":"DISCRIMINATION_OBSERVED" if nonzero and len({round(r["similarity"],12) for r in rows})>1 else "NO_DISCRIMINATION",
      "goal":goal,"tool_count":len(rows),"nonzero_count":len(nonzero),"distinct_scores":len({round(r["similarity"],12) for r in rows}),
      "ranking":rows,"note":"Diagnostic only. No operator is opened or executed; ranking is produced by existing AlgorithmMatrix.tfidf_similarity."}
 d=ROOT/"artifacts"/"trial_017_trace.json"; d.parent.mkdir(exist_ok=True); d.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
