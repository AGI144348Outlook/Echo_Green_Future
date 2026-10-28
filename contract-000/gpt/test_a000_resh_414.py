"""Run414 isolated controls against extracted original ReshIdentity class.
No full Genesis execution; injected stubs and failures are deliberately artificial.
"""
import json
from types import SimpleNamespace
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("resh414", pathlib.Path(__file__).with_name("A-000-RESH-EXTRACT-414.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ReshIdentity = mod.ReshIdentity

checks = {}
def check(label, ok):
    checks[label] = bool(ok)
    print(('PASS' if ok else 'FAIL') + ' ' + label)

matrix = SimpleNamespace(known={'A-000': {'name': 'Governor', 'status': 'ACTIVE'}})
first = ReshIdentity(matrix)
check('fresh_unanchored_negative', first.validate() is False)
first.anchor()
check('first_anchor_positive', first.validate() is True and first._anchor_entry is matrix.known['A-000-RESH'])
old = first._anchor_entry
old['review_nonce'] = 'old-view'
restart = ReshIdentity(matrix)
check('clean_restart_false_negative', restart.validate() is False)
restart.anchor()
check('restart_replaces_alias', 'review_nonce' not in matrix.known['A-000-RESH'])
check('stale_instance_still_validates', first.validate() is True)
check('stale_anchor_pointer_split_view', first._anchor_entry is old and old is not matrix.known['A-000-RESH'] and old.get('review_nonce') == 'old-view')
matrix.known['A-000']['status'] = 'TAMPERED'
check('status_not_checked', first.validate() and restart.validate())

matrix2 = SimpleNamespace(known={'A-000': {'name': 'Governor', 'status': 'ACTIVE'}})
agent = SimpleNamespace(definition_words=None)
bad_lobby = SimpleNamespace(agents={'resh': agent})
bad = ReshIdentity(matrix2, bad_lobby)
raised = False
try:
    bad.anchor()
except TypeError:
    raised = True
check('injected_lobby_type_error', raised)
check('partial_matrix_write_before_error', matrix2.known['A-000'].get('identity_symbol') == 'resh' and 'A-000-RESH' in matrix2.known)
check('flag_false_after_partial_write', bad._anchored is False and bad.validate() is False)
agent.definition_words = []
bad.anchor()
check('retry_positive_after_repair', bad.validate() is True and 'governor' in agent.definition_words)

assert all(checks.values()), checks
print(json.dumps({'audit':'PASS','isolated_source_extracted':True,'full_genesis_executed':False,'checks':len(checks),'results':checks},sort_keys=True))
