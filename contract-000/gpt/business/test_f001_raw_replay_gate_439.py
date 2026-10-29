"""Synthetic-only checks for the F-001 local replay gate; NOT real TAM replay."""
import importlib.util, json, tempfile, shutil
from pathlib import Path
spec=importlib.util.spec_from_file_location('gate',str(Path(__file__).with_name('f001_raw_replay_gate_439.py')))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
FAKE_SCANNER=r'''import csv,hashlib,json,sys
from pathlib import Path
src,out=map(Path,sys.argv[1:]); names=['README.md','Article 1 Hacksilber','Article 2 Water Weight Computes','The Color Dyed and Dental Records','Article 5','Article 6','Article 10','Collective information']
rows=[]; counts={}; hashes={}
for name in names:
 raw=(src/name).read_bytes();hashes[name]=hashlib.sha256(raw).hexdigest()
 lines=raw.decode().split('|');counts[name]=len(lines)
 for i,line in enumerate(lines,1):rows.append([name,i,'accuracy',line,''])
with (out/'claims.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['file','sentence_no','triggers','sentence','status']);w.writerows(rows)
(out/'claims-report.json').write_text(json.dumps({'source_files':hashes,'per_file':counts,'per_trigger':{'accuracy':len(rows)},'rows':len(rows)}))
'''
passed=[];failed=[]
with tempfile.TemporaryDirectory(prefix='f001-439-') as root:
 root=Path(root);src=root/'src';src.mkdir();scanner=root/'synthetic_scanner.py';scanner.write_text(FAKE_SCANNER)
 g.SCANNER_BLOB=g.git_blob(scanner.read_bytes()) # synthetic test override ONLY
 manifest={'project':'F-001','source_commit':'d46456a18fe412398d0ae37ec5a8c4eebb44e0c9','source_files':[],'rows':[]}
 for n,name in enumerate(g.FILES):
  count=6 if n<2 else 5
  lines=[f'Synthetic accuracy {name} sentence {i}.' for i in range(1,count+1)]
  raw='|'.join(lines).encode();(src/name).write_bytes(raw)
  manifest['source_files'].append({'path':name,'blob_sha':g.git_blob(raw)})
  manifest['rows'] += [{'source':name,'sentence_no':i,'triggers':['accuracy'],'excerpt':line[:170]} for i,line in enumerate(lines,1)]
 mp=root/'manifest.json';mp.write_text(json.dumps(manifest))
 def case(name,change=None,should_pass=False):
  out=root/('out-'+str(len(passed)+len(failed)))
  # restore original baseline each case
  for i,entry in enumerate(manifest['source_files']):
   n=entry['path'];count=6 if i<2 else 5
   (src/n).unlink(missing_ok=True)
   (src/n).write_bytes('|'.join(f'Synthetic accuracy {n} sentence {j}.' for j in range(1,count+1)).encode())
  mp.write_text(json.dumps(manifest));scanner.write_text(FAKE_SCANNER)
  if change:change(out)
  try:
   r=g.main(src,scanner,mp,out)
   ok=should_pass and r['rows']==42 and r['source_git_blobs_verified']==8
   detail='accepted '+str(r['rows'])
  except Exception as e:
   ok=not should_pass
   detail=type(e).__name__+': '+str(e)[:120]
  (passed if ok else failed).append(name+' '+detail)
 case('positive_8_sources_42_rows',should_pass=True)
 case('tampered_source_bytes',lambda o:(src/g.FILES[0]).write_text('altered'))
 case('missing_source',lambda o:(src/g.FILES[1]).unlink())
 def symlink(o):
  (src/g.FILES[0]).unlink();(src/g.FILES[0]).symlink_to(src/g.FILES[1])
 case('symlink_source',symlink)
 case('tampered_scanner',lambda o:scanner.write_text(FAKE_SCANNER+'\n# changed'))
 def missing_pin(o):
  m=json.loads(mp.read_text());m['source_files'].pop();mp.write_text(json.dumps(m))
 case('missing_manifest_pin',missing_pin)
 def wrong_coordinate(o):
  m=json.loads(mp.read_text());m['rows'][0]['sentence_no']=99;mp.write_text(json.dumps(m))
 case('wrong_candidate_coordinate',wrong_coordinate)
 def wrong_excerpt(o):
  m=json.loads(mp.read_text());m['rows'][0]['excerpt']='wrong';mp.write_text(json.dumps(m))
 case('wrong_candidate_excerpt',wrong_excerpt)
 def wrong_trigger(o):
  m=json.loads(mp.read_text());m['rows'][0]['triggers']=['certainty'];mp.write_text(json.dumps(m))
 case('wrong_candidate_trigger',wrong_trigger)
 case('nonempty_output',lambda o:(o.mkdir(),(o/'existing').write_text('do not overwrite')))
 def wrong_commit(o):
  m=json.loads(mp.read_text());m['source_commit']='bad';mp.write_text(json.dumps(m))
 case('wrong_source_commit',wrong_commit)
 # Output directory within source must be rejected.
 try:g.main(src,scanner,mp,src/'nested');failed.append('output_inside_source accepted')
 except ValueError as e:passed.append('output_inside_source '+str(e))
 print(json.dumps({'passed':len(passed),'failed':len(failed),'pass_cases':passed,'fail_cases':failed},indent=2))
 assert not failed
