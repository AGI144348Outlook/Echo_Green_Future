#!/usr/bin/env python3
"""F-001 HOLD-only offline original-Python-scanner replay from a verified TAM ZIP.

Usage: python3 -I -B F-001-OFFLINE-ZIP-REPLAY-414.py <tam-archive.zip> <claim_scan.py> <F-001-SCANNER-SNAPSHOT-412.py>

Accepts either exactly eight pinned public TAM files or the eleven-file public
GitHub source archive at d46456a, with or without one common root directory.
Rejects unknown, duplicated, symlink, oversized or altered entries. Copies only
pinned sources and exact pinned scanner/runner to a temporary directory, runs
only the pinned runner in a subprocess, verifies its HOLD receipt, and discards
all temporary data. No network, credentials, sales, publishing or approvals.
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

PROJECT = 'F-001'
HOLD = 'HOLD / NOT LAUNCH-READY'
SOURCE_COMMIT = 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9'
SCANNER_BLOB = '31f3dcff486c4c8cc96d514eb425da86834d00c3'
RUNNER_BLOB = 'c099d3e524f7dd879dfaed97e4896cb018844b1e'
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
EXTRA_PINS = {
    'Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)': 'b62c970a660e0a6685b58db1ef121690daa4fce7',
    'Dataset_B_Binary_Matrix.md': '12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4',
    'URLs to storedNotebookLM Diagramed Infographics': '127cca3d0eb99054b6088ac31f0f8d4bcbe2179a',
}
PER_FILE = {
    'README.md': 1, 'Article 1 Hacksilber': 2, 'Article 2 Water Weight Computes': 3,
    'The Color Dyed and Dental Records': 3, 'Article 5': 3, 'Article 6': 3,
    'Article 10': 4, 'Collective information': 23,
}
MAX_FILE = 2 * 1024 * 1024
MAX_ARCHIVE = 8 * 1024 * 1024
MAX_TOTAL = 8 * 1024 * 1024


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def pinned_regular(path, pin):
    path = Path(path)
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_FILE:
        raise ValueError('not a bounded regular file: ' + path.name)
    data = path.read_bytes()
    if len(data) != st.st_size or path.lstat().st_size != st.st_size or blob(data) != pin:
        raise ValueError('source or tool pin mismatch: ' + path.name)
    return data


def load_zip(archive, pins=PINS, extras=EXTRA_PINS):
    archive = Path(archive)
    st = archive.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_ARCHIVE:
        raise ValueError('not a bounded regular archive')
    all_allowed = {**pins, **extras}
    seen = {}
    prefixes = set()
    total = 0
    with zipfile.ZipFile(archive, 'r') as z:
        for info in z.infolist():
            name = info.filename
            if not name or name.startswith('/') or '\\' in name or '\x00' in name or ':' in name:
                raise ValueError('unsafe ZIP entry name')
            parts = name.rstrip('/').split('/')
            if any(p in ('', '.', '..') for p in parts):
                raise ValueError('unsafe ZIP entry path')
            kind = stat.S_IFMT(info.external_attr >> 16)
            if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError('nonregular ZIP entry')
            if info.is_dir():
                if len(parts) != 1:
                    raise ValueError('unexpected nested ZIP directory')
                prefixes.add(parts[0])
                continue
            if kind == stat.S_IFDIR:
                raise ValueError('directory disguised as ZIP file')
            if len(parts) not in (1, 2):
                raise ValueError('nested ZIP entry refused')
            prefix = parts[0] if len(parts) == 2 else ''
            prefixes.add(prefix)
            key = parts[-1]
            if key not in all_allowed or key in seen:
                raise ValueError('unknown or duplicate ZIP entry: ' + key)
            if info.flag_bits & 1 or info.file_size > MAX_FILE:
                raise ValueError('encrypted or oversized ZIP entry')
            total += info.file_size
            if total > MAX_TOTAL:
                raise ValueError('ZIP exceeds total size cap')
            with z.open(info, 'r') as stream:
                data = stream.read(MAX_FILE + 1)
                if len(data) > MAX_FILE or stream.read(1):
                    raise ValueError('ZIP extraction exceeds size cap')
            if blob(data) != all_allowed[key]:
                raise ValueError('Git blob mismatch in ZIP: ' + key)
            seen[key] = data
    if len(prefixes) != 1:
        raise ValueError('mixed ZIP prefixes')
    keys = set(seen)
    if keys != set(pins) and keys != set(all_allowed):
        raise ValueError('ZIP must contain exactly 8 or all 11 pinned public files')
    return {key: seen[key] for key in pins}


def replay(archive, scanner, runner, pins=PINS, extras=EXTRA_PINS,
           scanner_pin=SCANNER_BLOB, runner_pin=RUNNER_BLOB,
           per_file=PER_FILE):
    sources = load_zip(archive, pins, extras)
    scanner_bytes = pinned_regular(scanner, scanner_pin)
    runner_bytes = pinned_regular(runner, runner_pin)
    with tempfile.TemporaryDirectory(prefix='f001-offline-hold-') as td:
        root = Path(td)
        src = root / 'tam'
        src.mkdir()
        for name, data in sources.items():
            (src / name).write_bytes(data)
        scanner_file = root / 'claim_scan.py'
        runner_file = root / 'f001_scanner_snapshot_412.py'
        scanner_file.write_bytes(scanner_bytes)
        runner_file.write_bytes(runner_bytes)
        proc = subprocess.run([sys.executable, '-I', '-B', str(runner_file), str(src), str(scanner_file)],
                              cwd=root, capture_output=True, text=True, timeout=90)
        try:
            receipt = json.loads(proc.stdout.strip())
        except json.JSONDecodeError as exc:
            raise ValueError('runner returned non-JSON receipt') from exc
        if (proc.returncode != 0 or receipt.get('audit') != 'PASS' or
            receipt.get('project') != PROJECT or receipt.get('status') != HOLD or
            receipt.get('release_authorized') is not False or
            receipt.get('scanner_executed') is not True or
            receipt.get('scanner_blob') != scanner_pin or
            receipt.get('source_commit') != SOURCE_COMMIT or
            receipt.get('source_files') != len(pins) or
            receipt.get('rows') != sum(per_file.values()) or
            receipt.get('per_file') != per_file or
            receipt.get('source_blobs') != {name: blob(data) for name, data in sources.items()}):
            raise ValueError('runner failed or source-bound HOLD receipt mismatch')
        return {'audit': 'PASS', 'project': PROJECT, 'status': HOLD,
                'source_commit': SOURCE_COMMIT, 'source_files': len(pins),
                'scanner_executed': True, 'rows': receipt['rows'],
                'per_file': receipt['per_file'], 'release_authorized': False}


def main(args):
    if len(args) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        print(json.dumps(replay(*args[1:]), sort_keys=True))
        return 0
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'audit': 'FAIL', 'project': PROJECT, 'status': HOLD,
                          'reason': str(exc), 'release_authorized': False}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
