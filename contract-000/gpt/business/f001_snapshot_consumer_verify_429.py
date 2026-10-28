#!/usr/bin/env python3
"""F-001 HOLD-only post-staging verifier. Trusted single-user scratch only.
Independent source pins are NOT taken from the co-located receipt. Read-only.
Usage: python3 -I -B f001_snapshot_consumer_verify_429.py SNAPSHOT_DIR
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

SOURCE_COMMIT = 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9'
PINS = {
    'README.md': '213bcfaf560dcc54fbb7ae79fad932e86b660357',
    'Article 1 Hacksilber': '237bd3335abdcc0f0465817dffe01ad6eaa86055',
    'Article 2 Water Weight Computes': 'ec657c3fa0f70da9686fb1ae52983d28f77c6c4c',
    'The Color Dyed and Dental Records': 'b525ad60ab37cb2d72ea43c40ba687b0fe2a348d',
    'Article 5': 'c8c1bf617c0d81389f6c2408ed975131695857ff',
    'Article 6': '662d745f0b9b41236d1053cdbaa9351f7c020dd0',
    'Article 10': 'e82be564872f636662652d34dcb8d3437559f84f',
    'Collective information': '710ad3cd4feeae7bafa329d7437a78df4c40cfa8',
}
RECEIPT = 'SOURCE-SNAPSHOT-RECEIPT.json'
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_RECEIPT_BYTES = 65536


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def reject_symlink_components(path):
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('symlink path component: ' + str(part))
    return path


def regular_bytes(path, limit):
    if path.is_symlink():
        raise ValueError('symlink source: ' + path.name)
    mode = path.stat(follow_symlinks=False).st_mode
    if not stat.S_ISREG(mode):
        raise ValueError('not a regular file: ' + path.name)
    if path.stat(follow_symlinks=False).st_size > limit:
        raise ValueError('oversize file: ' + path.name)
    with path.open('rb') as handle:
        raw = handle.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('oversize read: ' + path.name)
    return raw


def verify_snapshot(directory, *, pins=None):
    pins = PINS if pins is None else pins  # test-only override; CLI always fixed pins
    root = reject_symlink_components(directory)
    if not root.is_dir():
        raise ValueError('snapshot directory missing')
    if not pins or any(Path(k).name != k or k in ('.', '..') for k in pins):
        raise ValueError('invalid pin names')
    expected = set(pins) | {RECEIPT}
    actual = {p.name for p in root.iterdir()}
    if actual != expected:
        raise ValueError('missing or unexpected snapshot files: ' + str(sorted(actual ^ expected)))
    raw_receipt = regular_bytes(root / RECEIPT, MAX_RECEIPT_BYTES)
    try:
        receipt = json.loads(raw_receipt.decode('utf-8', 'strict'))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError('invalid receipt') from exc
    if not isinstance(receipt, dict) or set(receipt) != {'status', 'source_commit', 'files', 'release_authorized'}:
        raise ValueError('receipt schema mismatch')
    if receipt['status'] != 'PREPARED_HOLD' or receipt['source_commit'] != SOURCE_COMMIT or receipt['release_authorized'] is not False:
        raise ValueError('not an authorized HOLD snapshot receipt')
    if not isinstance(receipt['files'], dict) or set(receipt['files']) != set(pins):
        raise ValueError('receipt file inventory mismatch')
    for name, pin in pins.items():
        raw = regular_bytes(root / name, MAX_FILE_BYTES)
        if not raw:
            raise ValueError('empty source: ' + name)
        try:
            raw.decode('utf-8', 'strict')
        except UnicodeDecodeError as exc:
            raise ValueError('invalid UTF-8: ' + name) from exc
        sha = hashlib.sha256(raw).hexdigest()
        blob = git_blob(raw)
        record = receipt['files'][name]
        if not isinstance(record, dict) or set(record) != {'git_blob', 'sha256', 'bytes'}:
            raise ValueError('file receipt schema mismatch: ' + name)
        if blob != pin or record != {'git_blob': blob, 'sha256': sha, 'bytes': len(raw)}:
            raise ValueError('independent pin or receipt mismatch: ' + name)
    return {'status': 'VERIFIED_PREPARED_HOLD', 'source_commit': SOURCE_COMMIT,
            'files_verified': len(pins), 'release_authorized': False}


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        result = verify_snapshot(argv[1])
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'REJECTED', 'error': str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
