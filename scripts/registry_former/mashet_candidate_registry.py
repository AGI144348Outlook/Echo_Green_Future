#!/usr/bin/env python3
"""Form a provenance-preserving *candidate* registry from the Mashet source transcript.
Runs offline with Python stdlib. No inference or semantic promotion.
"""
import hashlib, json, pathlib, re, sys, unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[2]
SRC=ROOT/"source-transcriptions/mashet-control-surface"
OUT=ROOT/"registries/mashet-candidates"
CATEGORIES={"A":(1,12),"B":(13,24),"C":(25,36),"D":(37,60),"E":(61,80),"F":(81,96)}
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    paths=sorted(SRC.glob("part-*.txt"))
    if not paths: raise SystemExit("No Mashet transcript parts found")
    full="\n".join(p.read_text(encoding="utf-8") for p in paths)
    # Scope to FIRST 'Bedrock Style' legend; later legends are competing proposals.
    start=full.find("Category A – Core Dynamics")
    end=full.find("Key Principles for Glyph Design",start)
    if start<0 or end<0:raise SystemExit("First legend boundaries not found; no candidates promoted")
    segment=full[start:end]
    candidates=[];active=None;index_by_category={k:0 for k in CATEGORIES};headings=[]
    for line_no,line in enumerate(segment.splitlines(),1):
        line=line.strip()
        m=re.match(r"Category ([A-F])\s*[–-]",line)
        if m:active=m.group(1);headings.append({"category":active,"heading":line});continue
        if not active or not line or line in ("Concept Glyph",):continue
        # A candidate is a concept followed by its terminal glyph token.
        # Whitespace is significant inside glyph clusters, so only split on last whitespace.
        m=re.match(r"^(.+?)\s+(\S+)$",line)
        if not m:continue
        label,glyph=m.groups()
        if len(glyph)>12 or len(label)<3:continue
        index_by_category[active]+=1
        n=index_by_category[active]
        candidate={"id":f"MASHET-{active}-{n:02d}","category":active,
            "claimed_slot":CATEGORIES[active][0]+n-1,
            "concept_as_written":label,"glyph_as_written":glyph,
            "codepoints":[f"U+{ord(c):04X}" for c in glyph],
            "unicode_names":[unicodedata.name(c,"UNASSIGNED") for c in glyph],
            "source":"source-transcriptions/mashet-control-surface/part-01.txt",
            "source_legend":"Mashet Glyph Legend (96 Symbols, Bedrock Style)",
            "status":"unverified_candidate","executable":False}
        candidates.append(candidate)
    glyph_to_ids={}
    for c in candidates:glyph_to_ids.setdefault(c["glyph_as_written"],[]).append(c["id"])
    report={"source_sha256":hashlib.sha256(full.encode()).hexdigest(),
        "legend_claimed_count":96,"actual_candidate_count":len(candidates),
        "per_category_counts":index_by_category,
        "declared_category_slot_ranges":{k:list(v) for k,v in CATEGORIES.items()},
        "duplicate_glyphs":{g:ids for g,ids in glyph_to_ids.items() if len(ids)>1},
        "cautions":["Multiple different legends appear in the source; this is the first one only.",
        "Candidate positions are sequential within their categories, not authoritative global identities.",
        "No candidate has been validated as a DSL operator, matrix, or codex.",
        "Missing positions and conflicting claims are retained, not silently repaired."]}
    (OUT/"candidate_registry.json").write_text(json.dumps(candidates,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
