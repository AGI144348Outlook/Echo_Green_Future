import sys,csv,re
tsv,manu=sys.argv[1],sys.argv[2]
M=open(manu,encoding='utf-8').read()
rows=list(csv.reader(open(tsv,encoding='utf-8'),delimiter='\t',quoting=csv.QUOTE_NONE))
h=rows[0];rows=rows[1:]
ok=miss=0;bad=[]
for r in rows:
    d=dict(zip(h,r))
    p=d['claude_proposed_state'].strip()
    s=d['short_text'].strip().strip('"').rstrip('…').strip()
    pin = p in M
    sin = s[:60] in M
    if pin and sin: ok+=1
    else: bad.append((d['occurrence_id'],d['proposal_section'],pin,sin,p[:70]))
print('rows',len(rows),'proposal+short verbatim in manuscript',ok)
for b in bad: print('NOT-VERBATIM',b)
