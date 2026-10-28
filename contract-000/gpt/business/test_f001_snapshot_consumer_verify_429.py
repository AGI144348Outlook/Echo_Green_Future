#!/usr/bin/env python3
"""Synthetic-only Run429 tests for HOLD snapshot consumer verifier.
No real TAM text, payment data, publication or network calls.
"""
import importlib.util
import json
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location('v429', Path(__file__).with_name('f001_snapshot_consumer_verify_429.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
checks = []


def check(label, result):
    checks.append([label, bool(result)])
    assert result, label


def fixture(root):
    root.mkdir()
    pins = {}
    files = {}
    for i, name in enumerate(v.PINS):
        raw = ('Synthetic public placeholder ' + str(i) + ' — ר\n').encode('utf-8')
        (root / name).write_bytes(raw)
        pins[name] = v.git_blob(raw)
        files[name] = {'git_blob': pins[name], 'sha256': v.hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    receipt = {'status': 'PREPARED_HOLD', 'source_commit': v.SOURCE_COMMIT,
               'files': files, 'release_authorized': False}
    (root / v.RECEIPT).write_text(json.dumps(receipt), encoding='utf-8')
    return pins


def negative(label, mutate):
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'snap'
        pins = fixture(root)
        mutate(root, pins)
        try:
            v.verify_snapshot(root, pins=pins)
        except (OSError, ValueError):
            check(label, True)
        else:
            check(label, False)

with tempfile.TemporaryDirectory() as td:
    root = Path(td) / 'snap'
    pins = fixture(root)
    result = v.verify_snapshot(root, pins=pins)
    check('positive 8-file verified HOLD', result['files_verified'] == 8 and result['status'] == 'VERIFIED_PREPARED_HOLD')
    check('positive no release flag', result['release_authorized'] is False)
    check('positive source commit pin', result['source_commit'] == v.SOURCE_COMMIT)

first = next(iter(v.PINS))
negative('reject altered source bytes', lambda r,p: (r / first).write_text('tamper'))
negative('reject missing source', lambda r,p: (r / first).unlink())
negative('reject extra file', lambda r,p: (r / 'extra.txt').write_text('unexpected'))
negative('reject invalid UTF-8', lambda r,p: (r / first).write_bytes(b'\xff'))
negative('reject empty source', lambda r,p: (r / first).write_bytes(b''))
negative('reject wrong independent pin', lambda r,p: p.__setitem__(first, '0' * 40))
negative('reject missing receipt', lambda r,p: (r / v.RECEIPT).unlink())
negative('reject malformed receipt', lambda r,p: (r / v.RECEIPT).write_text('{'))

def change_receipt(r, field, value):
    p = r / v.RECEIPT
    rec = json.loads(p.read_text())
    rec[field] = value
    p.write_text(json.dumps(rec))

negative('reject changed release flag', lambda r,p: change_receipt(r,'release_authorized',True))
negative('reject altered source commit', lambda r,p: change_receipt(r,'source_commit','0'*40))
negative('reject status flip', lambda r,p: change_receipt(r,'status','APPROVED'))
negative('reject extra receipt field', lambda r,p: change_receipt(r,'unknown','yes'))
negative('reject receipt source inventory', lambda r,p: change_receipt(r,'files',{}))

def swap_link(r,p):
    (r / first).unlink()
    (r / first).symlink_to(v.RECEIPT)
negative('reject source symlink', swap_link)
with tempfile.TemporaryDirectory() as td:
    real = Path(td) / 'real'
    pins = fixture(real)
    link = Path(td) / 'link'
    link.symlink_to(real, target_is_directory=True)
    try:
        v.verify_snapshot(link, pins=pins)
    except ValueError:
        check('reject snapshot root symlink', True)
    else:
        check('reject snapshot root symlink', False)

print(json.dumps({'passed': sum(x[1] for x in checks), 'total': len(checks), 'checks': checks}, indent=2))
