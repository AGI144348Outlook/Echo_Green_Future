#!/usr/bin/env python3
"""F-001 HOLD-only, no-network, exact-Git-blob scanner snapshot verification.

Usage: python3 -I -B f001_scanner_snapshot_412.py <TAM-directory> <claim_scan.py>
Runs ONLY the pinned original scanner on an ephemeral copy of eight pinned sources.
Returns a JSON verification receipt; does not persist worksheets or approve claims.
"""
import csv
import hashlib
import json
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE_COMMIT = 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9'
SCANNER_PIN = '31f3dcff486c4c8cc96d514eb425da86834d00c3'
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
MAX_BYTES = 2 * 1024 * 1024


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def read_pinned(path, expected):
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_BYTES:
        raise ValueError('not bounded regular file: ' + path.name)
    data = path.read_bytes()
    if len(data) != st.st_size or len(data) > MAX_BYTES or path.lstat().st_size != st.st_size:
        raise ValueError('file changed during read: ' + path.name)
    if git_blob(data) != expected:
        raise ValueError('Git blob mismatch: ' + path.name)
    return data


def verify(src, scanner, pins=PINS, scanner_pin=SCANNER_PIN, expected_rows=42):
    src, scanner = Path(src), Path(scanner)
    if not src.is_dir() or src.is_symlink():
        raise ValueError('source must be a real directory')
    originals = {name: read_pinned(src / name, pin) for name, pin in pins.items()}
    scanner_bytes = read_pinned(scanner, scanner_pin)
    with tempfile.TemporaryDirectory(prefix='f001-hold-') as temp:
        root = Path(temp)
        input_dir = root / 'source'
        output_dir = root / 'output'
        input_dir.mkdir()
        for name, data in originals.items():
            (input_dir / name).write_bytes(data)
        scanner_path = root / 'claim_scan.py'
        scanner_path.write_bytes(scanner_bytes)
        proc = subprocess.run([sys.executable, '-I', '-B', str(scanner_path), str(input_dir), str(output_dir)],
                              cwd=root, capture_output=True, text=True, timeout=30)
        if proc.returncode:
            raise ValueError('scanner nonzero exit: ' + str(proc.returncode))
        report = json.loads((output_dir / 'claims-report.json').read_text(encoding='utf-8'))
        with (output_dir / 'claims.csv').open(encoding='utf-8', newline='') as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != ['file', 'sentence_no', 'triggers', 'sentence', 'status']:
                raise ValueError('invalid worksheet schema')
            rows = list(reader)
        if len(rows) != expected_rows or report.get('rows') != expected_rows:
            raise ValueError('unexpected claim row count')
        if set(report.get('source_files', {})) != set(pins):
            raise ValueError('missing/extra report source keys')
        for name, data in originals.items():
            if report['source_files'][name] != hashlib.sha256(data).hexdigest():
                raise ValueError('scanner report source mismatch: ' + name)
        if sum(report.get('per_file', {}).values()) != expected_rows:
            raise ValueError('per-file totals mismatch')
        if any(row['file'] not in pins or row['status'] or not row['triggers'] for row in rows):
            raise ValueError('invalid source/status/trigger row')
        return {'project': 'F-001', 'status': 'HOLD / NOT LAUNCH-READY',
                'source_commit': SOURCE_COMMIT, 'scanner_blob': scanner_pin,
                'source_blobs': {name: git_blob(data) for name, data in originals.items()},
                'source_files': len(pins), 'rows': len(rows), 'per_file': report['per_file'],
                'scanner_executed': True, 'release_authorized': False}


def main(args):
    if len(args) != 3:
        print('usage: f001_scanner_snapshot_412.py <TAM-directory> <claim_scan.py>', file=sys.stderr)
        return 2
    try:
        print(json.dumps({'audit': 'PASS', **verify(args[1], args[2])}, sort_keys=True))
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print(json.dumps({'audit': 'FAIL', 'project': 'F-001', 'status': 'HOLD / NOT LAUNCH-READY',
                          'reason': str(exc), 'release_authorized': False}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
