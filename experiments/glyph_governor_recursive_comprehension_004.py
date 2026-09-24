from pathlib import Path
import json,re,hashlib

ROOT=Path("ECHO_GlyphRegistry")
OUT=Path("results"); OUT.mkdir(exist_ok=True)
WORD=re.compile(r"[A-Za-z][A-Za-z'-]{2,}")
STOP={"the","and","that","this","with","from","into","then","than","what","when","where","which","while","have","has","had","for","are","was","were","not","but","can","its","their","they","them","each","only","before","after","through","between","because","both","all","any","how","why","does"}

docs={}
for p in sorted(ROOT.glob("*.md")):
    docs[p.name]=p.read_text(encoding="utf-8")
reference="\n".join(docs.values())
tokens=[w.lower() for w in WORD.findall(reference) if w.lower() not in STOP]
freq={}
for w in tokens: freq[w]=freq.get(w,0)+1

# Personal vocabulary lobby starts from operation names/classes and expands only through referenced material.
known=set()
for text in docs.values():
    for label in ("Algorithmic Operation","Operation Class"):
        m=re.search(rf"\| \*\*{label}\*\* \| ([^|]+) \|",text)
        if m:
            known.update(x.lower() for x in WORD.findall(m.group(1)))
initial=set(known)

# Local dictionary: definitions are harvested from sentences in the supplied reference corpus.
sentences=re.split(r"(?<=[.!?])\s+",re.sub(r"\s+"," ",reference))
def lookup(word):
    hits=[s.strip() for s in sentences if re.search(rf"\b{re.escape(word)}\b",s,re.I)]
    return hits[:3]

def classroom():
    # Tests comprehension proxies only over words encountered in the reference:
    # coverage + contextual definition retrieval + relational co-occurrence.
    vocab=set(tokens)
    coverage=len(vocab & known)/max(1,len(vocab))
    sample=sorted(vocab,key=lambda w:(-freq[w],w))[:120]
    definable=sum(bool(lookup(w)) for w in sample if w in known)
    denom=sum(1 for w in sample if w in known)
    contextual=definable/max(1,denom)
    grade=100*(0.7*coverage+0.3*contextual)
    return {"grade":round(grade,2),"coverage":round(100*coverage,2),"known":len(known),"reference_vocabulary":len(vocab),"contextual_retrieval":round(100*contextual,2)}

ledger=[]
prev=-1
MAX=8
for cycle in range(1,MAX+1):
    before=classroom()
    unknown=[w for w in sorted(set(tokens),key=lambda w:(-freq[w],w)) if w not in known]
    homework=unknown[:40]
    learned=[]
    for w in homework:
        refs=lookup(w)
        if refs:
            known.add(w); learned.append({"word":w,"reference":refs[0]})
    after=classroom()
    # Glyph lobby connect: evidence must come from explicit combinatorial/folding text, not universal hypernyms.
    connections=[]
    for fn,text in docs.items():
        if fn=="INDEX.md": continue
        opm=re.search(r"\| \*\*Algorithmic Operation\*\* \| ([^|]+) \|",text)
        if not opm: continue
        op=opm.group(1).strip()
        sec=re.search(r"## Combinatorial Relationships\s*(.*?)(?=\n## |\Z)",text,re.S)
        if sec:
            for line in sec.group(1).splitlines():
                if line.strip().startswith("- ") and "+" in line:
                    reason=line.strip()[2:]
                    connections.append({"source_operation":op,"reference":reason})
    explanation=(f"In recursive cycle {cycle}, I returned to the glyphic reference material because my classroom grade was {before['grade']:.2f}. "
                 f"I identified {len(homework)} high-frequency words that were present in the reference material but absent from my personal vocabulary lobby, and I used the reference-derived dictionary contexts to admit {len(learned)} of those words. "
                 f"After completing that homework, my classroom grade became {after['grade']:.2f}, so the measured change for this cycle was {after['grade']-before['grade']:.2f} points. "
                 f"I then revisited explicit folding and combinatorial statements as candidate glyph connections, because a connection should preserve the source's stated operational relationship rather than rely merely on a universal hypernym. "
                 f"I will continue the reference-material, homework, classroom-test, glyph-connection, explanation cycle while the classroom grade is still improving and reference-grounded vocabulary remains available.")
    ledger.append({"cycle":cycle,"before":before,"homework_words":homework,"learned":learned,"after":after,
                   "candidate_connection_evidence":connections[:30],"governor_reasoning":explanation})
    improvement=after["grade"]-before["grade"]
    if improvement<=0.01 or after["grade"]>=95 or not learned: break
    prev=after["grade"]

final=classroom()
report={"experiment":"GLYPH_GOVERNOR_RECURSIVE_COMPREHENSION_004",
"cycle":"Reference Material -> Homework -> Classroom Test -> Glyphic Lobby Connect -> Explain -> Reference Material",
"initial_vocabulary":len(initial),"final_vocabulary":len(known),"final_classroom":final,"cycles":ledger,
"stopping_rule":"Stop when grade improvement is <= 0.01 points, grade reaches 95, no reference-grounded words can be learned, or eight cycles complete.",
"boundary":"The classroom grade is an explicit proxy based on reference-vocabulary coverage and contextual retrieval. The Governor's prose is mechanically generated from measured cycle state. This run does not establish subjective comprehension or a literal feeling of confidence."}
raw=json.dumps(report,ensure_ascii=False,indent=2); report["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
OUT.joinpath("glyph_governor_recursive_comprehension_004.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
md=["# GLYPH GOVERNOR RECURSIVE COMPREHENSION 004","",f"Cycle: {report['cycle']}",""]
for x in ledger:
    md += [f"## Cycle {x['cycle']}","",x["governor_reasoning"],"",f"Classroom: {x['before']['grade']} -> {x['after']['grade']}",f"Vocabulary: {x['before']['known']} -> {x['after']['known']}",""]
md += ["## Final",f"Vocabulary: {len(initial)} -> {len(known)}",f"Classroom grade: {final['grade']}","",report["boundary"]]
OUT.joinpath("glyph_governor_recursive_comprehension_004.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print("STATUS: GLYPH_GOVERNOR_RECURSIVE_COMPREHENSION_004_EXECUTED")
print("CYCLES:",len(ledger)); print("VOCABULARY:",len(initial),"->",len(known)); print("FINAL_GRADE:",final["grade"])
