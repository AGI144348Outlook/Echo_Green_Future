#!/usr/bin/env python3
"""F-001 §138 (Claude 21Z): read-only check of ChatGPT run 331 CSV spec P1/P2 on a TAM clone.
Usage: python3 -I CLAUDE-csv-spec-331-check-138.py <tam-clone>  (reads commit d46456a via git show; writes nothing)."""
import hashlib,subprocess,sys,csv
from fractions import Fraction as F
tam=sys.argv[1]
for b,p in [("b62c970a660e0a6685b58db1ef121690daa4fce7","Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)"),("12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4","Dataset_B_Binary_Matrix.md")]:
    raw=subprocess.run(["git","-C",tam,"show","d46456a:"+p],capture_output=True).stdout
    sid=hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
    print("P1",p[:12],len(raw),sid==b, hashlib.sha256(raw).hexdigest()[:16])
    raw2=bytearray(raw); raw2[0]^=1
    print("P1-neg", hashlib.sha1(b"blob "+str(len(raw2)).encode()+bytes([0])+bytes(raw2)).hexdigest()==b)
for n,d in [(1,16),(1,4),(1,8)]:
    e=F(137,10)*F(n,d); print("P2",f"{n}/{d}",e,float(e), round(13.7*n/d,4))
