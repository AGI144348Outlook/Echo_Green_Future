# F-001 §209 (Claude, 2026-11-06 09Z): source_range grammar, bounds and length_band check on synthetic fixtures only (no manuscript text). Stdlib, offline. Run: python3 -I CLAUDE-range-band-fixtures-209.py
import hashlib,re
b="26bb461648789ad095fe64891f0cd838a935e928"
src="F-001 synthetic fixture source, no manuscript text\n"
H="passage_id\tsource_blob_sha\tsource_range\tlength_band\trights_basis\tdecision\tscope\treviewed_at\trights_evidence_ref"
RX=re.compile(r"([1-9][0-9]*):([1-9][0-9]*)-([1-9][0-9]*):([1-9][0-9]*)")
def span(rng,text):
    m=RX.fullmatch(rng)
    if not m: return "noncanonical_source_range"
    l1,c1,l2,c2=map(int,m.groups())
    if (l2,c2)<(l1,c1): return "noncanonical_source_range"
    lines=text.split("\n")
    if l2>len(lines) or c1>len(lines[l1-1])+0 or c2>len(lines[l2-1]): return "source_range_out_of_bounds"
    if l1==l2: return c2-c1+1
    return len(lines[l1-1])-c1+1+1+sum(len(x)+1 for x in lines[l1:l2-1])+c2
def band(n): return "B0" if n<40 else "B1" if n<100 else "B2" if n<200 else "B3" if n<300 else "B4"
def ws(rows): return (H+"\n"+"".join("\t".join(r)+"\n" for r in rows)).encode()
def row(pid,rng,bd,dec,ref): return [pid,b,rng,bd,"own",dec,"ebook-v1","2026-11-06T00:00Z",ref]
V={"fixture10_corrected":[row("SYN-001","1:1-1:5","B0","ALLOW","ATTEST"),row("SYN-002","1:7-1:15","B0","DENY","-")],
   "range_out_of_bounds":[row("SYN-001","1:1-1:5","B0","ALLOW","ATTEST"),row("SYN-002","1:7-1:60","B1","DENY","-")],
   "range_reversed":[row("SYN-001","1:1-1:5","B0","ALLOW","ATTEST"),row("SYN-002","1:15-1:7","B0","DENY","-")],
   "range_leading_zero":[row("SYN-001","1:01-1:5","B0","ALLOW","ATTEST"),row("SYN-002","1:7-1:15","B0","DENY","-")],
   "band_mismatch":[row("SYN-001","1:1-1:5","B1","ALLOW","ATTEST"),row("SYN-002","1:7-1:15","B0","DENY","-")],
   "s208_band_S":[row("SYN-001","1:1-1:5","S","ALLOW","ATTEST"),row("SYN-002","1:7-1:15","S","DENY","-")]}
for k,rows in V.items():
    w=ws(rows); codes=set()
    for r in rows:
        s=span(r[2],src)
        if isinstance(s,str): codes.add(s)
        elif r[3]!=band(s): codes.add("length_band_mismatch")
    print(k,len(w),hashlib.sha256(w).hexdigest(),sorted(codes) or ["ok"],[span(r[2],src) for r in rows])
