from pathlib import Path
import json, hashlib, re
from collections import defaultdict

rows=json.loads(Path("lobbies/glyph/registry.json").read_text(encoding="utf-8"))
agents={f"glyph-{r['id']:02d}":r for r in rows}
universal={"COMPUTATIONAL PRIMITIVE","ALGORITHM COMPONENT","ALGORITHM","SYSTEM"}

# Governor may connect only from evidence present in both registry chains.
pair_records=[]
ids=sorted(agents)
for i,a_id in enumerate(ids):
    for b_id in ids[i+1:]:
        a,b=agents[a_id],agents[b_id]
        common=[n for n in a["hypernyms"] if n in set(b["hypernyms"])]
        if not common:
            continue
        discriminating=[n for n in common if n not in universal]
        evidence=discriminating if discriminating else common
        reason=("shared lower-level registry hypernym" if discriminating
                else "shared universal registry hypernym")
        # Sentence is assembled solely from fields visible to the Governor.
        sentence=(f"{a_id} ({a['operation']}) is connected to {b_id} "
                  f"({b['operation']}) because both registry chains contain "
                  f"{', '.join(evidence)} as a {reason}.")
        checks={
            "ends_as_sentence": bool(re.search(r"[.!?]$",sentence)),
            "names_agent_a": a_id in sentence,
            "names_agent_b": b_id in sentence,
            "states_reason": "because" in sentence.lower(),
            "cites_shared_evidence": all(n in sentence for n in evidence),
        }
        pair_records.append({
            "a":a_id,"b":b_id,
            "a_operation":a["operation"],"b_operation":b["operation"],
            "a_chain":a["hypernyms"],"b_chain":b["hypernyms"],
            "shared_nodes":common,
            "connection_evidence":evidence,
            "evidence_kind":reason,
            "governor_sentence":sentence,
            "sentence_audit":checks,
            "sentence_complete":all(checks.values()),
        })

report={
    "experiment":"GLYPH_GOVERNOR_HYPERNYM_002_SHOW_YOUR_WORK",
    "agents":len(agents),
    "lexical_lobby_members":0,
    "connections":len(pair_records),
    "complete_sentence_reports":sum(x["sentence_complete"] for x in pair_records),
    "lower_level_connections":sum(x["evidence_kind"].startswith("shared lower") for x in pair_records),
    "universal_only_connections":sum(x["evidence_kind"].startswith("shared universal") for x in pair_records),
    "records":pair_records,
    "boundary":"Every explanation is mechanically composed from registry-visible fields and shared hypernym evidence. Sentence completeness here measures audit-format compliance, not independent language comprehension."
}
payload=json.dumps(report,ensure_ascii=False,indent=2)
report["sha256"]=hashlib.sha256(payload.encode()).hexdigest()
Path("results/glyph_governor_hypernym_002.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

lines=["# GLYPH GOVERNOR HYPERNYM 002 — SHOW YOUR WORK","",
       f"Connections: {report['connections']}",
       f"Complete sentence reports: {report['complete_sentence_reports']}",
       f"Lower-level connections: {report['lower_level_connections']}",
       f"Universal-only connections: {report['universal_only_connections']}","",
       "## Governor connection ledger",""]
for n,x in enumerate(pair_records,1):
    lines += [f"### Connection {n}: {x['a']} ↔ {x['b']}",
              f"- A chain: {' → '.join(x['a_chain'])}",
              f"- B chain: {' → '.join(x['b_chain'])}",
              f"- Shared evidence: {'; '.join(x['connection_evidence'])}",
              f"- Governor report: {x['governor_sentence']}",
              f"- Sentence audit: {'PASS' if x['sentence_complete'] else 'FAIL'}",""]
Path("results/glyph_governor_hypernym_002.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("GLYPH_GOVERNOR_HYPERNYM_002_SHOW_YOUR_WORK")
print("Connections:",report["connections"])
print("Complete sentence reports:",report["complete_sentence_reports"])
print("Lower-level connections:",report["lower_level_connections"])
print("Universal-only connections:",report["universal_only_connections"])
print("STATUS: EXECUTED")
