"""DISC-002 E33 probe (Claude, 2026-10-24T17Z): ChatGPT cases (10) and (11) on the real classes.
Usage: python3 -I -B DISC-002-revocation-reanchor-e33-probe.py SCRATCH_algorithm_matrix.py SCRATCH_echo_governor_skeleton.py
Scratch copies only: dev-suite:pwa/python/algorithm_matrix.py (blob f7cf465) and
genesis-documentary:src/echo_governor_skeleton.py (blob 63eb982). Synthetic values; stand-in matrix/lobby/ayin; records only.
"""
import sys, importlib.util, json, ast, __future__
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
out = {}
# (10) Dev Suite: layout tamper, then snapshot() alone
am = load(sys.argv[1], 'am')
r = am.AlgorithmMatrixRuntime(); r.run_boot_handshake(); r.alg_006()
k = sorted(r.sub_matrices)[0]; r.sub_matrices[k]['storage']['probe'] = 'SYNTHETIC-VALUE'
n0 = len(r.audit)
r.sub_matrices[k]['glyph'] = 'X'                      # layout tamper (digest covers glyph)
snap = r.snapshot()
out['e33a_audit_added_by_snapshot'] = len(r.audit) - n0
out['e33a_flags_after_snapshot'] = [r.verified, r.storage_unlocked]
out['e33a_snapshot_storage'] = snap['sub_matrices'][k]['storage'].get('probe')
try: r.storage(k); out['e33b_read'] = 'ok'
except PermissionError as e: out['e33b_read'] = 'denied: ' + str(e)
out['e33b_last_audit'] = r.audit[-1]
# control: valid state, snapshot() changes nothing
r2 = am.AlgorithmMatrixRuntime(); r2.run_boot_handshake(); r2.alg_006()
r2.snapshot(); out['e33c_valid_flags_after_snapshot'] = [r2.verified, r2.storage_unlocked]
# (11) Genesis: extract ReshIdentity and PeCommunicator only (module itself not imported)
src = open(sys.argv[2], encoding='utf-8').read(); tree = ast.parse(src)
ns = {}
for node in tree.body:
    if isinstance(node, ast.ClassDef) and node.name in ('ReshIdentity', 'PeCommunicator'):
        exec(compile(ast.Module([node], []), 'genesis', 'exec', flags=__future__.annotations.compiler_flag, dont_inherit=True), ns)  # annotations unevaluated
class M: pass
class Agent: pass
class Lobby: pass
m = M(); m.known = {'A-000': {'name': 'Governor'}}
lob = Lobby(); a = Agent(); a.definition_words = ['head', 'beginning']; lob.agents = {'resh': a}
resh = ns['ReshIdentity'](m, lob); resh.anchor()
first_alias = dict(m.known['A-000-RESH'])
m.known['A-000']['identity_symbol'] = 'TAMPERED'      # validation now fails
m.known['A-000-RESH']['status'] = 'REVOKED-BY-PROBE'
out['e33d_validate_after_tamper'] = resh.validate()
pe = ns['PeCommunicator'].__new__(ns['PeCommunicator']); pe.resh = resh
class Ayin:
    def agentive_entities(self, min_ties=1): return []
pe.ayin = Ayin()
pe.open_exchanges()
out['e33d_validate_after_open_exchanges'] = resh.validate()
out['e33d_identity_symbol'] = m.known['A-000']['identity_symbol']
out['e33d_alias_status'] = m.known['A-000-RESH']['status']
out['e33d_old_evidence_kept'] = m.known['A-000-RESH'] != first_alias or 'REVOKED-BY-PROBE' in json.dumps(m.known)
print(json.dumps(out, ensure_ascii=False))
