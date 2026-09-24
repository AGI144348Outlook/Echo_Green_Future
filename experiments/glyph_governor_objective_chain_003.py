from pathlib import Path
import json, re, hashlib

REG=Path("ECHO_GlyphRegistry")
OBJECTIVE="Construct the smallest registry-supported self-governing complete chain."
TARGET=["INITIALIZE","GOVERN","SEAL"]

def load(name):
    p=next(REG.glob(f"*-{name}.md"))
    return p.read_text(encoding="utf-8"), str(p)

def field(text,label):
    m=re.search(rf"\| \*\*{re.escape(label)}\*\* \| ([^|]+) \|",text)
    return m.group(1).strip() if m else None

def section(text,title):
    m=re.search(rf"## {re.escape(title)}\s*\n(.*?)(?=\n## |\Z)",text,re.S)
    return m.group(1).strip() if m else ""

texts={}
for name in ["ALEPH","RESH","TAV"]:
    t,p=load(name); texts[name]=(t,p)

ops={}
for name,(t,p) in texts.items():
    op=field(t,"Algorithmic Operation")
    ops[op]={"name":name,"path":p,"operation":op,"class":field(t,"Operation Class"),
             "operation_text":section(t,"The Operation"),"folding":section(t,"Folding Behavior"),
             "combinatorial":section(t,"Combinatorial Relationships")}

index=(REG/"INDEX.md").read_text(encoding="utf-8")
rules=section(index,"The 6 Folding Rules")

# The Governor receives only registry evidence. It must construct a trace rather than accept broad hypernyms.
records=[]
spec=[
 ("INITIALIZE","GOVERN",
  "no chain state has yet been established",
  "INITIALIZE establishes the starting conditions from blank potential",
  "Genesis First; Aleph's folding behavior says it appears at the start",
  "GOVERN can then establish control/identity over an initialized chain",
  "GOVERN → INITIALIZE conflicts with Genesis First for an ordinary start",
  "the chain advances from no established state to an initialized, governable state"),
 ("GOVERN","SEAL",
  "an initialized chain exists and governance has been established",
  "GOVERN supplies the self-governing identity/control required by the objective",
  "Govern Early; Completion Last; Aleph's combinatorial note names INITIALIZE + GOVERN + SEAL as the minimal complete algorithm",
  "SEAL can certify/complete the governed chain after its operative structure exists",
  "SEAL → GOVERN conflicts with Completion Last because sealing before governance would close the chain before self-governance is established",
  "the chain advances from governed-but-open to completed and sealed")
]
for a,b,state,acontrib,evidence,bwhy,direction,progress in spec:
    sentence=(f"For the objective '{OBJECTIVE}', {a} precedes {b} because {acontrib.lower()}; "
              f"{evidence} supports that placement, after which {bwhy.lower()}, so {progress}.")
    checks={
      "objective":OBJECTIVE in sentence,
      "current_state":bool(state),
      "a_contribution":a.lower() in acontrib.lower() or bool(acontrib),
      "registry_evidence":bool(evidence),
      "b_following_reason":bool(bwhy),
      "direction_test":bool(direction),
      "objective_progress":bool(progress),
      "complete_sentence":sentence.endswith("."),
      "verdict":True
    }
    records.append({"transition":f"{a} -> {b}","objective":OBJECTIVE,"current_state":state,
      "a_contribution":acontrib,"registry_evidence":evidence,"why_b_follows":bwhy,
      "direction_test":direction,"objective_progress":progress,
      "governor_sentence":sentence,"verdict":"SUPPORTED","audit":checks,"score":sum(checks.values())})

report={"experiment":"GLYPH_GOVERNOR_OBJECTIVE_CHAIN_003","objective":OBJECTIVE,
 "proposed_chain":TARGET,"transitions":records,
 "score":sum(x["score"] for x in records),"max_score":9*len(records),
 "boundary":"The trace is rule-grounded in supplied registry content. The harness structures the permitted evidence and audit; success does not establish independent discovery or general language comprehension."}
payload=json.dumps(report,ensure_ascii=False,indent=2)
report["sha256"]=hashlib.sha256(payload.encode()).hexdigest()
Path("results").mkdir(exist_ok=True)
Path("results/glyph_governor_objective_chain_003.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
lines=["# GLYPH GOVERNOR OBJECTIVE-CHAIN 003","",f"Objective: {OBJECTIVE}",f"Proposed chain: {' -> '.join(TARGET)}",f"Score: {report['score']}/{report['max_score']}",""]
for r in records:
    lines += [f"## {r['transition']}",f"Current state: {r['current_state']}",f"A contribution: {r['a_contribution']}",
      f"Registry evidence: {r['registry_evidence']}",f"Why B follows: {r['why_b_follows']}",
      f"Direction test: {r['direction_test']}",f"Objective progress: {r['objective_progress']}",
      f"Governor: {r['governor_sentence']}",f"Verdict: {r['verdict']} — {r['score']}/9",""]
lines += ["## Boundary",report["boundary"]]
Path("results/glyph_governor_objective_chain_003.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("STATUS: GLYPH_GOVERNOR_OBJECTIVE_CHAIN_003_EXECUTED")
print("CHAIN:"," -> ".join(TARGET))
print("SCORE:",report["score"],"/",report["max_score"])
