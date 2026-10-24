import importlib.util, hashlib, json, pathlib, tempfile, os
P = pathlib.Path(__file__).with_name('PROPOSED-f001-verified-stage-copy-v1.py')
spec = importlib.util.spec_from_file_location('verified_copy', P)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sha = lambda x: hashlib.sha256(x).hexdigest()
results = []

def run(name, fn, expected):
    try:
        outcome = fn()
    except Exception as e:
        outcome = 'REJECTED:'+type(e).__name__
    results.append({'case':name, 'observed':outcome, 'expected':expected, 'pass':outcome==expected})

with tempfile.TemporaryDirectory(prefix='f001-315-') as td:
    root = pathlib.Path(td)
    src=root/'snapshot'; dst=root/'staged'; data=b'PDF placeholder only, not a real book'
    src.write_bytes(data)
    run('T0_consistent', lambda: 'ACCEPTED' if m.copy_verified(src,dst,sha(data),len(data))['sha256']==sha(data) else 'WRONG', 'ACCEPTED')
    run('T1_metadata_snapshot_changed', lambda: (src.write_bytes(b'FORGED'+data), m.copy_verified(src,root/'meta',sha(data),len(data)))[1], 'REJECTED:ValueError')
    src.write_bytes(data)
    run('T2_epub_snapshot_changed', lambda: (src.write_bytes(b'EPUB swapped'+data), m.copy_verified(src,root/'epub',sha(data),len(data)))[1], 'REJECTED:ValueError')
    src.write_bytes(data)
    run('T3_staged_binding_changed', lambda: (os.chmod(dst,0o600), dst.write_bytes(b'forged'), m.verify_staged({dst:{'sha256':sha(data),'size':len(data)}}))[2], 'REJECTED:ValueError')
    dst.unlink(); m.copy_verified(src,dst,sha(data),len(data))
    run('T4_staged_epub_changed', lambda: (os.chmod(dst,0o600), dst.write_bytes(b'epub modified'), m.verify_staged({dst:{'sha256':sha(data),'size':len(data)}}))[2], 'REJECTED:ValueError')
    run('T5_wrong_pin', lambda: m.copy_verified(src,root/'bad','0'*64,len(data)), 'REJECTED:ValueError')
    run('T6_optional_disposition', lambda: 'NOT_RUN_NOT_IN_HELPER', 'NOT_RUN_NOT_IN_HELPER')
    run('T7_duplicate_json', lambda: 'NOT_RUN_NOT_IN_HELPER', 'NOT_RUN_NOT_IN_HELPER')
print(json.dumps({'scope':'isolated verified-copy helper, NOT full adapter or actual verifier chain', 'results':results, 'executed':6, 'passed':sum(x['pass'] for x in results[:6]), 'not_executed':['T6','T7']},indent=2))
