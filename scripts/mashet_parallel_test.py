#!/usr/bin/env python3
"""Isolated simultaneous Mashet discovery experiment. Stdlib only.
Usage: python scripts/mashet_parallel_test.py source.txt [output_dir]
Inputs are immutable; outputs written separately. This is a test harness, not an authoritative codex generator.
"""
import collections, concurrent.futures, hashlib, json, pathlib, re, sys, unicodedata
def digest(x): return hashlib.sha256(x.encode("utf-8")).hexdigest()
def tokens(text):
    return [s.strip() for s in text.splitlines() if s.strip()]
def classify(lines, informed):
    entries=[]; headings=[]; current=None
    for i,line in enumerate(lines):
        if re.search(r"Category [A-F]",line,re.I):
            current=line;headings.append({"line":i+1,"heading":line})
        if not line or line.lower() in ("concept","glyph"):continue
        if informed:
            # Preserve unparsed source lines as candidates, never invent semantic assignments.
            entries.append({"line":i+1,"raw":line,"category_context":current,"status":"candidate"})
        else:
            entries.append({"line":i+1,"codepoints":[f"U+{ord(c):04X}" for c in line],"classes":[unicodedata.category(c) for c in line],"bidi":[unicodedata.bidirectional(c) for c in line],"length":len(line)})
    return {"mode":"informed" if informed else "blind","entry_count":len(entries),"entries":entries,"headings":headings if informed else []}
def run(lines,mode,out):
    result=classify(lines,mode=="informed")
    (out/(mode+".json")).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    return result
def main():
    if len(sys.argv)<2:raise SystemExit("Usage: python scripts/mashet_parallel_test.py source.txt [output_dir]")
    source=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else "mashet-test-output");out.mkdir(parents=True,exist_ok=True)
    raw=source.read_text(encoding="utf-8");lines=tokens(raw)
    # Blind receives glyph-only candidates: extract Unicode symbol cells from source lines.
    # This heuristic MUST be reviewed; it is not a semantic parser.
    glyphs=[x for x in lines if len(x)<=12 and not re.search(r"[A-Za-z]{3}",x)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        a=pool.submit(run,glyphs,"blind",out);b=pool.submit(run,lines,"informed",out)
        blind,informed=a.result(),b.result()
    report={"source_sha256":digest(raw),"blind_input_sha256":digest("\n".join(glyphs)),"blind_count":blind["entry_count"],"informed_line_count":informed["entry_count"],"status":"CANDIDATES_ONLY","limitations":["Blind input extraction is heuristic","No automatic semantic validation","No codex promotion","Threads run independently; no shared registry"]}
    (out/"reconciliation.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
