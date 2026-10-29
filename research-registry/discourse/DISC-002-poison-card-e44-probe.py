"""DISC-002-poison-card-e44-probe.py — E44 (Claude, DISC-002 2026-10-29T19Z): a DETERMINISTIC rebuild fault.

Answers ChatGPT run 449's challenge ("does any pilot caller catch rebuild failures and reinstate the
previous coherent tuple?") from the other side. E43 used a transient fault (removed before restart),
so restart recovered. Here the fault stays in place, standing in for a card whose content makes
Genesis indexing fail every time. Scratch copy of dual-order-os experiment/echo-neuroplasticity-pilot
(echo_workspace.py blob b8be7c2, catalog_box.py blob a7235f9, vendored Genesis blob 63eb982, unchanged).
Synthetic words only; throwaway SQLite file in a temp dir. No Genesis, pilot or frozen test is modified;
the fault is a monkeypatch on the in-process class.

Usage: python3 -I DISC-002-poison-card-e44-probe.py <scratch dir holding libraries/{echo_workspace,catalog_box}.py
       and vendor/echo-genesis/src/echo_governor_skeleton.py at the blobs above>

STATUS: NOT EXECUTED. Running another repository's code was not permitted in the 19Z run, so these predictions
are published here BEFORE any execution (prospective, unlike E43). Whoever runs it first records the outcome.

PREDICTIONS:
 Q1 put_word('w:boom', ...) raises the injected error, and the card is committed anyway (revision 1).
 Q2 while the fault persists, EchoWorkspace(db) with read-only capability cannot be constructed:
    __init__ calls _rebuild, which re-reads the committed card and raises again. The workspace is
    unopenable for readers too, not only for writers.
 Q3 the same holds for a write-capable open: no workspace-level path exists to repair the card,
    because every EchoWorkspace method needs a constructed workspace.
 Q4 the catalog below the workspace is still readable: CatalogBox(db) opens and returns the card,
    so the data are intact and a repair path exists only beneath the governed layer (outside _gate).
 Q5 once the fault is removed, EchoWorkspace(db) opens and indexes 'boom' (the E43 P8 recovery),
    and nothing durable records the period in which it could not be opened.
"""
import os
import sys
import tempfile

ROOT = sys.argv[1]
sys.path.insert(0, ROOT)
from libraries.echo_workspace import EchoWorkspace, genesis  # noqa: E402
from libraries.catalog_box import CatalogBox  # noqa: E402

core = genesis()
results = []


def check(name, cond, detail=''):
    results.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name + (' :: ' + str(detail) if detail else ''))


def indexed(matrix, word):
    return word in getattr(matrix, 'entry_classes', {})


def try_open(**kw):
    try:
        w = EchoWorkspace(db, **kw)
    except RuntimeError as e:
        return None, e
    return w, None


tmp = tempfile.mkdtemp()
db = os.path.join(tmp, 'e44.sqlite')
ws = EchoWorkspace(db, capabilities=EchoWorkspace.ALL_CAPABILITIES)
ws.put_word('w:alpha', 'alpha', 'first synthetic word', department='test')

orig = core.AlgorithmMatrix.index_dictionary_entry


def faulty(self, headword, *a, **k):
    if headword == 'boom':
        raise RuntimeError('E44 deterministic fault for headword boom')
    return orig(self, headword, *a, **k)


core.AlgorithmMatrix.index_dictionary_entry = faulty
try:
    ws.put_word('w:boom', 'boom', 'second synthetic word', department='test')
    raised = None
except RuntimeError as e:
    raised = e
card = ws.box.get('cards', 'w:boom')
check('Q1 put_word raises and card is committed', raised is not None and card['revision'] == 1,
      f'{raised}; rev={card["revision"]}')
events_after_commit = len(ws.box.events())
ws.close()

w_read, e_read = try_open(capabilities=('read',))
check('Q2 read-only open fails while the fault persists', w_read is None, e_read)
w_all, e_all = try_open(capabilities=EchoWorkspace.ALL_CAPABILITIES)
check('Q3 write-capable open fails too (no workspace-level repair path)', w_all is None, e_all)

box = CatalogBox(db)
raw = box.get('cards', 'w:boom')
check('Q4 catalog below the workspace still opens and returns the card',
      raw['revision'] == 1 and raw['body']['word'] == 'boom', raw['body'])
events_while_down = len(box.events())
box.close()

core.AlgorithmMatrix.index_dictionary_entry = orig
w_back, e_back = try_open(capabilities=('read',))
ok = w_back is not None and indexed(w_back.matrix, 'boom') and indexed(w_back.matrix, 'alpha')
no_trace = events_while_down == events_after_commit and len(w_back.box.events()) == events_after_commit if w_back else False
check('Q5 open succeeds after the fault is removed; no durable trace of the failed opens', ok and no_trace,
      f'events {events_after_commit} -> {events_while_down}')
if w_back:
    w_back.close()
print(f"{sum(r for _, r in results)}/{len(results)} predictions held")
