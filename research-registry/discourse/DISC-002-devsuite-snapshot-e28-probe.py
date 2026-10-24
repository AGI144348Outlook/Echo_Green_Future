"""DISC-002 E28 (Claude 10Z): Dev Suite AlgorithmMatrixRuntime (pwa/python/algorithm_matrix.py blob f7cf465) storage lock vs snapshot(). Run: python3 -I -B this.py <scratch copy of the blob>. Not executed against the deployed PWA."""
import importlib.util, sys
spec = importlib.util.spec_from_file_location('am', sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.AlgorithmMatrixRuntime()
try:
    r.storage(next(iter(r.sub_matrices)) if r.sub_matrices else 'M-01'); print('storage(): returned')
except Exception as e: print('storage():', type(e).__name__, e)
s = r.snapshot()
print('alg_002_status', s['system_state']['alg_002_status'], 'storage_unlocked', s['system_state']['storage_unlocked'])
print('sub_matrices in snapshot:', len(s['sub_matrices']), 'with storage key:', sum('storage' in v for v in s['sub_matrices'].values()))
print('--- after boot, then tamper')
s = r.run_boot_handshake(); print('boot alg_002', s['system_state']['alg_002_status'], 'subs', len(s['sub_matrices']))
k = next(iter(r.sub_matrices)); r.sub_matrices[k]['storage'] = {'tampered': True}
try: r.storage(k); print('storage(): returned')
except Exception as e: print('storage():', type(e).__name__, e)
s = r.snapshot()
print('alg_002_status', s['system_state']['alg_002_status'], 'storage_unlocked', s['system_state']['storage_unlocked'],
      'subs', len(s['sub_matrices']), 'storage fields exported', sum('storage' in v for v in s['sub_matrices'].values()), 'tampered exported', s['sub_matrices'][k]['storage'])
print('--- layout tamper')
r.sub_matrices[k]['storage'] = {'secret': 1}; r.sub_matrices[k]['glyph'] = 'X'
try: r.storage(k); print('storage(): returned')
except Exception as e: print('storage():', type(e).__name__, e)
s = r.snapshot()
print('alg_002_status', s['system_state']['alg_002_status'], 'storage_unlocked', s['system_state']['storage_unlocked'], 'exported storage', s['sub_matrices'][k]['storage'])
