"""F-001 §161: content-word check of ChatGPT 462's 43 MANUAL source locations.
Usage: python3 -I manual_review.py REGISTER.tsv LOCATIONS.tsv TAM_DIR OUT.tsv
Read-only. For each MANUAL row: recall of the quote's content words in the mapped
sentence, and the best-scoring sentence in the same file (mis-mapping check)."""
import sys, re, unicodedata, csv, json
reg, loc, tam, out = sys.argv[1:5]
def sentences(t):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n{2,}', t) if s.strip()]
STOP=set("the a an of and or to in on is are was were be it its this that with as by for at from into than then".split())
def words(t):
    t=unicodedata.normalize("NFKC",t).replace("\\%","%").replace("\\","").lower()
    return [w for w in re.findall(r"[a-z0-9֐-׿.]+(?:'[a-z]+)?",t) if w.strip(".") and w.strip(".") not in STOP]
def recall(q,s):
    qs=[w.strip(".") for w in words(q)]; ss=set(w.strip(".") for w in words(s))
    return (sum(1 for w in qs if w in ss)/len(qs)) if qs else 0.0
R={r["occurrence_id"]:r for r in csv.DictReader(open(reg,encoding="utf-8"),delimiter="\t",quoting=csv.QUOTE_NONE)}
L=list(csv.DictReader(open(loc,encoding="utf-8"),delimiter="\t",quoting=csv.QUOTE_NONE))
rows=[]; cache={}
for l in L:
    if l["quote_match_class"]!="MANUAL": continue
    oid=l["occurrence_id"]; f,n=re.match(r"^(.*)#S(\d+)$",oid).groups(); n=int(n)
    ss=cache.setdefault(f,sentences(open(f"{tam}/{f}",encoding="utf-8").read()))
    q=R[oid]["short_text"].strip('"\'… ')
    sc=[recall(q,s) for s in ss]; mapped=sc[n-1]; best=max(range(len(ss)),key=lambda i:sc[i])
    if mapped>=0.8 and sc[best]<=mapped: v="CONFIRMED"
    elif mapped>=0.5 and sc[best]<=mapped: v="PROBABLE"
    else: v="CHECK"
    rows.append([oid,f"{mapped:.2f}",best+1,f"{sc[best]:.2f}",v,q[:90]])
with open(out,"w",encoding="utf-8",newline="\n") as fh:
    fh.write("occurrence_id\tmapped_recall\tbest_sentence_no\tbest_recall\tverdict\tquote_excerpt\n")
    for r in rows: fh.write("\t".join(map(str,r))+"\n")
from collections import Counter
print(json.dumps({"manual_rows":len(rows),"verdicts":Counter(r[4] for r in rows)}))
