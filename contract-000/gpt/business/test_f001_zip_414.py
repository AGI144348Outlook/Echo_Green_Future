"""Offline synthetic positive/tamper-negative checks for F-001 ZIP replay.
Does NOT use actual TAM content or original scanner. The synthetic runner is
explicitly synthetic; no result implies actual eight-source scanner parity.
"""
import importlib.util, io, json, os, pathlib, stat, tempfile, zipfile
P=pathlib.Path(__file__).with_name('F-001-OFFLINE-ZIP-REPLAY-414.py')
spec=importlib.util.spec_from_file_location('z414',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
checks={}
def check(name,fn):
 try: checks[name]=bool(fn())
 except Exception as e:checks[name]=False;print('ERROR',name,type(e).__name__,str(e))
 print(('PASS' if checks[name] else 'FAIL'),name)
def rejects(fn):
 try:fn();return False
 except (ValueError,zipfile.BadZipFile):return True

def zipwrite(path,entries,prefix='',dup=False,symlink=False):
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
  if prefix:z.writestr(prefix+'/',b'')
  for name,data in entries.items():z.writestr(prefix+'/'+name if prefix else name,data)
  if dup:z.writestr((prefix+'/' if prefix else '')+next(iter(entries)),b'evil')
  if symlink:
   i=zipfile.ZipInfo((prefix+'/' if prefix else '')+'link')
   i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16
   z.writestr(i,'outside')

with tempfile.TemporaryDirectory() as t:
 root=pathlib.Path(t);d={f'f{i}':('data'+str(i)).encode() for i in range(8)}
 pins={k:m.blob(v) for k,v in d.items()};extras={'extra':m.blob(b'other')}
 archive=root/'input.zip';zipwrite(archive,d,prefix='The-TAM-protocol-d46456a')
 check('valid_8_prefixed',lambda:m.load_zip(archive,pins,extras)==d)
 zipwrite(archive,d)
 check('valid_8_root',lambda:m.load_zip(archive,pins,extras)==d)
 zipwrite(archive,{**d,'extra':b'other'},prefix='The-TAM-protocol-d46456a')
 check('valid_9_custom_pins',lambda:m.load_zip(archive,pins,extras)==d)
 zipwrite(archive,{**d,'extra':b'other changed'})
 check('tampered_extra_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 zipwrite(archive,{**d,'unlisted':b'bad'})
 check('unknown_file_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 zipwrite(archive,d,dup=True)
 check('duplicate_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 zipwrite(archive,d,symlink=True)
 check('symlink_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 zipwrite(archive,{**d,'f7':b'changed'})
 check('tampered_source_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 zipwrite(archive,{k:v for k,v in d.items() if k!='f7'})
 check('missing_source_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 zipwrite(archive,{**d,'../evil':b'bad'})
 check('traversal_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 with zipfile.ZipFile(archive,'w') as z:
  for k,v in d.items():z.writestr(('prefix1/' if k!='f7' else 'prefix2/')+k,v)
 check('mixed_prefix_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 zipwrite(archive,{**d,'f7':b'x'*(m.MAX_FILE+1)})
 check('oversized_entry_rejected',lambda:rejects(lambda:m.load_zip(archive,pins,extras)))
 zipwrite(archive,d)
 scanner=root/'scan.py';scanner.write_text('print("synthetic scanner")')
 runner=root/'runner.py'
 # Synthetic runner only: reports source pins and fixed count, never reads actual claim text.
 runner.write_text('import hashlib,json,sys,pathlib\n'
 'd={p.name:p.read_bytes() for p in pathlib.Path(sys.argv[1]).iterdir()}\n'
 'blob=lambda b:hashlib.sha1(b"blob "+str(len(b)).encode()+b"\\0"+b).hexdigest()\n'
 'print(json.dumps({"audit":"PASS","project":"F-001","status":"HOLD / NOT LAUNCH-READY",'
 '"release_authorized":False,"scanner_executed":True,"scanner_blob":'+repr(m.blob(scanner.read_bytes()))+','
 '"source_commit":'+repr(m.SOURCE_COMMIT)+',"source_files":len(d),"rows":42,'
 '"per_file":'+repr({'f0':1,'f1':2,'f2':3,'f3':3,'f4':3,'f5':3,'f6':4,'f7':23})+','
 '"source_blobs":{k:blob(v) for k,v in d.items()}}))\n')
 per={f'f{i}':v for i,v in enumerate([1,2,3,3,3,3,4,23])}
 args=dict(pins=pins,extras={},scanner_pin=m.blob(scanner.read_bytes()),runner_pin=m.blob(runner.read_bytes()),per_file=per)
 check('synthetic_runner_positive',lambda:m.replay(archive,scanner,runner,**args)['rows']==42)
 scanner.write_text('changed scanner')
 check('scanner_pin_negative',lambda:rejects(lambda:m.replay(archive,scanner,runner,**args)))
 scanner.write_text('print("synthetic scanner")')
 runner.write_text('print("changed runner")')
 check('runner_pin_negative',lambda:rejects(lambda:m.replay(archive,scanner,runner,**args)))

assert all(checks.values()),checks
print(json.dumps({'audit':'PASS','synthetic':True,'original_tam_replay':False,'checks':len(checks),'results':checks},sort_keys=True))
