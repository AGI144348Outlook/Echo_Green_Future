# F-001 §210 (Claude, 2026-11-06 10Z): multi-line span and NFC/NFD column fixtures for source_range (synthetic text only, no manuscript text). Stdlib, offline.
# Run: python3 -I CLAUDE-multiline-nfc-fixtures-210.py
import hashlib,re,unicodedata
RX=re.compile(r"([1-9][0-9]*):([1-9][0-9]*)-([1-9][0-9]*):([1-9][0-9]*)")
def span(rng,text):
    m=RX.fullmatch(rng)
    if not m: return "noncanonical_source_range"
    l1,c1,l2,c2=map(int,m.groups())
    if (l2,c2)<(l1,c1): return "noncanonical_source_range"
    lines=text.split("\n")
    if l2>len(lines) or c1>len(lines[l1-1]) or c2>len(lines[l2-1]): return "source_range_out_of_bounds"
    if l1==l2: return c2-c1+1
    return len(lines[l1-1])-c1+1+1+sum(len(x)+1 for x in lines[l1:l2-1])+c2
def band(n): return "B0" if n<40 else "B1" if n<100 else "B2" if n<200 else "B3" if n<300 else "B4"
nfc=unicodedata.normalize("NFC","Écho synthetic line one\nline two\nthree\n")
nfd=unicodedata.normalize("NFD",nfc)
for name,src in (("nfc",nfc),("nfd",nfd)):
    b=src.encode()
    print(name,len(b),hashlib.sha256(b).hexdigest(),"is_nfc=",unicodedata.is_normalized("NFC",src))
    for rng in ("1:1-1:4","1:1-2:4","1:6-3:5","2:1-2:8","3:1-3:6","1:24-2:1"):
        s=span(rng,src); print(" ",rng,s,band(s) if isinstance(s,int) else "-")
