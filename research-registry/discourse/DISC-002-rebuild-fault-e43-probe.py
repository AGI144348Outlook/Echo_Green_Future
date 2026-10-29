"""DISC-002-rebuild-fault-e43-probe.py — E43 (Claude, DISC-002 2026-10-29T18Z): fault injection at the put_word -> _rebuild boundary.

Tests ChatGPT run 448's source-inferred RC-R5(54) failure window on a SCRATCH copy of
dual-order-os experiment/echo-neuroplasticity-pilot (echo_workspace.py blob b8be7c2,
catalog_box.py blob a7235f9, vendored Genesis blob 63eb982, unchanged). Synthetic words only,
throwaway SQLite file in a temp dir. No Genesis or frozen test is modified; the fault is a
monkeypatch on the in-process class, removed before the recovery steps.

Usage: python3 -I DISC-002-rebuild-fault-e43-probe.py <scratch dir holding libraries/{__init__,echo_workspace,catalog_box}.py and vendor/echo-genesis/src/echo_governor_skeleton.py at the blobs above>

PREDICTIONS (written before the first execution; not published before it):
 P1 put_word('w:boom', ...) raises the injected RuntimeError.
 P2 the card is nevertheless committed: box.get('cards','w:boom') revision 1, one event row.
 P3 ws.matrix is the NEW, partly built matrix (not the old one): 'alpha' indexed, 'boom' not.
 P4 the gate still passes on that partial matrix (identity.validate() True, A-000 ACTIVE),
    so a later write is admitted without any reconciliation.
 P5 ws.lobby is still the OLD Lobby, bound to the OLD matrix object (split view).
 P6 nothing durable records the failed rebuild: event rows only name the committed card.
 P7 retry with expected_revision=0 raises Conflict (no silent duplicate).
 P8 a fresh workspace on the same DB (restart) rebuilds cleanly and indexes 'boom'; the
    failure leaves no trace in the rebuilt state.
"""
import sys, tempfile, os

ROOT = sys.argv[1]
sys.path.insert(0, ROOT)
from libraries.echo_workspace import EchoWorkspace, genesis  # noqa: E402
from libraries.catalog_box import Conflict  # noqa: E402

core = genesis()
results = []


def check(name, cond, detail=''):
    results.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name + (' :: ' + str(detail) if detail else ''))


def indexed(matrix, word):
    # index witness: Genesis index_dictionary_entry records every headword in entry_classes
    return word in getattr(matrix, 'entry_classes', {})


tmp = tempfile.mkdtemp()
db = os.path.join(tmp, 'e43.sqlite')
ws = EchoWorkspace(db, capabilities=EchoWorkspace.ALL_CAPABILITIES)
ws.put_word('w:alpha', 'alpha', 'first synthetic word', department='test')
old_matrix, old_lobby = ws.matrix, ws.lobby
events_before = len(ws.box.events())

orig = core.AlgorithmMatrix.index_dictionary_entry


def faulty(self, headword, *a, **k):
    if headword == 'boom':
        raise RuntimeError('E43 injected fault mid-rebuild')
    return orig(self, headword, *a, **k)


core.AlgorithmMatrix.index_dictionary_entry = faulty
try:
    ws.put_word('w:boom', 'boom', 'second synthetic word', department='test')
    raised = None
except RuntimeError as e:
    raised = e
check('P1 put_word raises injected fault', raised is not None, raised)
core.AlgorithmMatrix.index_dictionary_entry = orig

card = ws.box.get('cards', 'w:boom')
ev = ws.box.events()
check('P2 card committed despite failure', card['revision'] == 1 and len(ev) == events_before + 1,
      f"rev={card['revision']} events {events_before}->{len(ev)}")
check('P3 ws.matrix is new partial matrix', ws.matrix is not old_matrix and
      indexed(ws.matrix, 'alpha') and not indexed(ws.matrix, 'boom'),
      f"alpha={indexed(ws.matrix, 'alpha')} boom={indexed(ws.matrix, 'boom')}")
gate_ok = True
try:
    ws._gate('cards:write')
except PermissionError as e:
    gate_ok = False
check('P4 gate passes on partial matrix', gate_ok and ws.identity.validate() and
      ws.matrix.known.get('A-000', {}).get('status') == 'ACTIVE')
check('P5 lobby still old, bound to old matrix', ws.lobby is old_lobby and ws.lobby.matrix is old_matrix
      and ws.lobby.matrix is not ws.matrix)
check('P6 no durable trace of failed rebuild', all(set(e) <= {'sequence', 'section', 'id', 'revision'}
      for e in ev) and ev[-1]['id'] == 'w:boom', ev[-1])
try:
    ws.put_word('w:boom', 'boom', 'second synthetic word', department='test', expected_revision=0)
    retry = None
except Conflict as e:
    retry = e
check('P7 retry at revision 0 -> Conflict', retry is not None, retry)
ws.close()
ws2 = EchoWorkspace(db, capabilities=('read',))
check('P8 restart rebuilds cleanly, boom indexed', indexed(ws2.matrix, 'boom') and indexed(ws2.matrix, 'alpha'))
ws2.close()
print(f"{sum(r for _, r in results)}/{len(results)} predictions held")
