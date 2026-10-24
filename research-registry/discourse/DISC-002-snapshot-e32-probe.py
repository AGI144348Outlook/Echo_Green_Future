"""DISC-002 E32 probe (Claude, 2026-10-24T16Z): denial flood vs snapshot() on Dev Suite f7cf465.
Usage: python3 -I -B DISC-002-snapshot-e32-probe.py SCRATCH_COPY_OF_algorithm_matrix.py
Scratch copy of dev-suite:pwa/python/algorithm_matrix.py (blob f7cf465) only; synthetic value; records only.
"""
import sys, importlib.util, json
spec=importlib.util.spec_from_file_location('am',sys.argv[1]);am=importlib.util.module_from_spec(spec);spec.loader.exec_module(am)
r=am.AlgorithmMatrixRuntime(); r.run_boot_handshake(); r.alg_006()
k=sorted(r.sub_matrices)[0]
r.sub_matrices[k]['storage']['probe']='SYNTHETIC-VALUE'
out={'key':k,'d0_read':r.storage(k)}
for i in range(300):
    try: r.storage(k, actor='someone_else')
    except PermissionError: pass
out['d1_unlocked_after_denials']=r.storage_unlocked
try: r.storage(k); out['d2_governor_read']='ok'
except PermissionError as e: out['d2_governor_read']='denied: '+str(e)
snap=r.snapshot()
out['d3_snapshot_has_value']=snap['sub_matrices'][k]['storage'].get('probe')
out['d3_snapshot_alg002']=snap['system_state']['alg_002_status']
out['d4_audit_len']=len(snap['audit']); out['d4_denied']=sum(e['event']=='DENIED' for e in snap['audit'])
out['d4_lifecycle']=[e['event'] for e in snap['audit'] if e['event']!='DENIED']
print(json.dumps(out))
