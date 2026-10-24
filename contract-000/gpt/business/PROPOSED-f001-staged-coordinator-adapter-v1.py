#!/usr/bin/env python3
"""F-001 HOLD-only research adapter: stage all four artifacts and JSON inputs.

Requires reviewed pinned-input-snapshot-v1 and coordinator-v4 Git blobs.
Creates a DERIVED receipt with rewritten staged paths/root, not a source-authenticated
receipt. No publication authority, process containment, or production security claim.
"""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from types import ModuleType, SimpleNamespace

ARTIFACTS = ('epub', 'pdf', 'dataset_a_csv', 'dataset_b_csv')
META = {'pins': 'pins.json', 'receipt': 'receipt.json',
        'binding': 'binding.json', 'v5': 'v5-report.json'}
HELPER_BLOB = '4fac471658d36ed71bec707cb9803150064ec894'
COORDINATOR_BLOB = '9eee2016d696d1584350d0b1bfa20826ddad2eb5'
MAX_JSON = 1024 * 1024
MAX_TOTAL = 120 * 1024 * 1024


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def reviewed_module(path, expected, name):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError('reviewed source not regular')
        data = os.read(fd, 1024 * 1024 + 1)
    finally:
        os.close(fd)
    if len(data) > 1024 * 1024 or git_blob(data) != expected:
        raise ValueError('reviewed source Git blob mismatch: ' + name)
    mod = ModuleType(name)
    sys.modules[name] = mod
    exec(compile(data, '<reviewed-' + name + '>', 'exec'), mod.__dict__)
    return mod


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key: ' + key)
        out[key] = value
    return out


def parse_json(data):
    obj = json.loads(data.decode('utf-8'), object_pairs_hook=no_duplicates,
                     parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    if not isinstance(obj, dict):
        raise ValueError('JSON input must be object')
    return obj


def read_beneath(root_fd, parts, helper, limit=MAX_JSON):
    fd = helper._open_beneath(root_fd, parts)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > limit:
            raise ValueError('metadata not bounded regular file')
        data = os.read(fd, limit + 1)
        if len(data) > limit or len(data) != st.st_size:
            raise ValueError('metadata size changed or exceeds bound')
        return data
    finally:
        os.close(fd)


def safe_root(value):
    root = Path(os.path.abspath(os.fspath(value)))
    if not root.is_dir() or any(p.is_symlink() for p in (root, *root.parents)):
        raise ValueError('root absent or symlink ancestor')
    return root


def write_private(path, data):
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'wb') as out:
        out.write(data)
    os.chmod(path, 0o400)


@contextmanager
def staged_inputs(source_root, tool_root, *, _after_open=None, _before_snapshot=None):
    """Yield (v4 arguments, provenance). Private callbacks are test-only.

    JSON hashes from first read are used only for consistency, NOT trust.
    Four artifact hashes are read from unauthenticated caller pins; HOLD forever.
    """
    root, toolroot = safe_root(source_root), safe_root(tool_root)
    helper = reviewed_module(toolroot / 'PROPOSED-f001-pinned-input-snapshot-v1.py',
                             HELPER_BLOB, 'f001_reviewed_snapshot_v1')
    root_fd = os.open(root, helper.DIR_FLAGS)
    try:
        raw = {k: read_beneath(root_fd, helper._relative_parts(v), helper)
               for k, v in META.items()}
        optional = 'disposition.json'
        try:
            raw['disposition'] = read_beneath(root_fd, [optional], helper)
        except FileNotFoundError:
            pass
    finally:
        os.close(root_fd)
    objects = {k: parse_json(v) for k, v in raw.items()}
    pins, receipt = objects['pins'], objects['receipt']
    if pins.get('schema') != 'f001-pins/v1' or receipt.get('schema') != 'f001-receipt/v1':
        raise ValueError('unsupported pin/receipt schema')
    pa, ra = pins.get('artifacts'), receipt.get('artifacts')
    if not isinstance(pa, dict) or not isinstance(ra, dict) or set(pa) != set(ARTIFACTS) or set(ra) != set(ARTIFACTS):
        raise ValueError('exact four-artifact maps required')
    items = {'meta_' + k: (META[k] if k in META else optional, hashlib.sha256(v).hexdigest())
             for k, v in raw.items()}
    seen = set()
    total = 0
    for name in ARTIFACTS:
        p, r = pa[name], ra[name]
        if not isinstance(p, dict) or not isinstance(r, dict):
            raise ValueError('artifact entry must be object')
        rel = r.get('path')
        helper._relative_parts(rel)
        if rel in seen or rel in META.values() or rel == optional:
            raise ValueError('duplicate or metadata-overlapping artifact path')
        seen.add(rel)
        if type(p.get('size')) is not int or p['size'] < 0 or type(r.get('size')) is not int or r['size'] != p['size'] or r.get('sha256') != p.get('sha256'):
            raise ValueError('inconsistent artifact pin and receipt')
        total += p['size']
        items['artifact_' + name] = (rel, p['sha256'])
    if total > MAX_TOTAL:
        raise ValueError('aggregate artifact size exceeds bound')
    if _before_snapshot:
        _before_snapshot()
    with helper.pinned_snapshots(root, items, max_bytes=MAX_TOTAL, _after_open=_after_open) as copies:
        with tempfile.TemporaryDirectory(prefix='f001-stage-all-') as tmp:
            stage = Path(tmp)
            (stage / 'artifacts').mkdir(mode=0o700)
            for name in ARTIFACTS:
                rec = copies['artifact_' + name]
                if rec.size != pa[name]['size']:
                    raise ValueError('staged artifact size mismatch')
                write_private(stage / 'artifacts' / name, Path(rec.path).read_bytes())
                ra[name]['path'] = 'artifacts/' + name
            for k, filename in META.items():
                if k != 'receipt':
                    write_private(stage / filename, Path(copies['meta_' + k].path).read_bytes())
            if 'disposition' in raw:
                write_private(stage / optional, Path(copies['meta_disposition'].path).read_bytes())
            env = receipt.get('environment')
            if not isinstance(env, dict) or not isinstance(env.get('build_output_realpath'), str):
                raise ValueError('receipt environment missing')
            if env['build_output_realpath'] != str(root):
                raise ValueError('original build_output_realpath does not match source root')
            env['build_output_realpath'] = str(stage)
            derived = (json.dumps(receipt, sort_keys=True, indent=2) + '\n').encode('utf-8')
            write_private(stage / 'receipt.json', derived)
            provenance = {'original_receipt_sha256': hashlib.sha256(raw['receipt']).hexdigest(),
                          'derived_receipt_sha256': hashlib.sha256(derived).hexdigest(),
                          'derivation': 'staged path and build_output_realpath rewrite',
                          'source_pin_authenticated': False,
                          'publication_authorization': 'ABSENT',
                          'artifact_sha256': {k: copies['artifact_' + k].sha256 for k in ARTIFACTS}}
            a = SimpleNamespace(artifact_root=str(stage), tool_root=str(toolroot),
                                pins=str(stage / 'pins.json'), receipt=str(stage / 'receipt.json'),
                                binding_manifest=str(stage / 'binding.json'),
                                v5_report=str(stage / 'v5-report.json'),
                                disposition_record=str(stage / optional),
                                **{k: str(toolroot / v) for k, v in {
                                    'receipt_v3': 'PROPOSED-f001-receipt-verify-v3.py',
                                    'v5_gate': 'PROPOSED-f001-v5-report-gate-v1.py',
                                    'v4_binding': 'PROPOSED-f001-receipt-v4-binding.py',
                                    'v5_parser': 'PROPOSED-f001-disposition-binding-v5.py'}.items()})
            yield a, provenance


def coordinate_staged(source_root, tool_root, **test_hooks):
    try:
        with staged_inputs(source_root, tool_root, **test_hooks) as (args, provenance):
            coordinator = reviewed_module(Path(tool_root) / 'PROPOSED-f001-source-pinned-coordinator-v4.py',
                                          COORDINATOR_BLOB, 'f001_reviewed_coordinator_v4')
            result = coordinator.coordinate(args)
            result['staging_provenance'] = provenance
            return result
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, json.JSONDecodeError) as exc:
        return {'schema': 'f001-staged-adapter/v1', 'integrity': 'FAIL', 'release': 'HOLD',
                'readiness': 'BLOCKED', 'source_pin_authenticated': False,
                'approval_authenticated': False, 'publication_authorization': 'ABSENT',
                'issues': [str(exc)], 'stages': []}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: staged-adapter.py SOURCE_ROOT TOOL_ROOT')
    output = coordinate_staged(sys.argv[1], sys.argv[2])
    print(json.dumps(output, sort_keys=True))
    raise SystemExit(0 if output['integrity'] == 'PASS' else 1)
