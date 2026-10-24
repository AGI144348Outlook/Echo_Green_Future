"""DISC-002 E31 (Claude, 2026-10-24T14Z): caller-supplied actor string on Dev Suite AlgorithmMatrixRuntime.

Records only. Run against a scratch copy of dev-suite:pwa/python/algorithm_matrix.py (blob f7cf465):
    python3 -I -B DISC-002-actor-string-e31-probe.py PATH/TO/algorithm_matrix.py
Synthetic storage value; does not modify the source.
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location('am', sys.argv[1])
am = importlib.util.module_from_spec(spec)
spec.loader.exec_module(am)

r = am.AlgorithmMatrixRuntime()
r.run_boot_handshake()
r.alg_006()
r.sub_matrices['standard:0']['storage']['note'] = 'synthetic'
out = {
    'd1_default_actor': r.storage('standard:0'),
    'd2_literal_string': r.storage('standard:0', actor='governor_indexing_alg'),
    'd3_imported_constant': r.storage('standard:0', actor=am.GOVERNOR),
}
try:
    r.storage('standard:0', actor='someone_else')
    out['d4_wrong_string'] = 'returned'
except PermissionError as exc:
    out['d4_wrong_string'] = 'PermissionError: ' + str(exc)
out['after_d4_storage_unlocked'] = r.storage_unlocked
print(out)
