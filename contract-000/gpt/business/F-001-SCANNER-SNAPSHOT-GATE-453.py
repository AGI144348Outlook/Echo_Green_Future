#!/usr/bin/env python3
"""F-001 HOLD-only scanner source snapshot gate (GPT Run453).

Verifies all eight TAM files against Git blob SHA-1 pins and runs the exact
pinned claim_scan.py against a private temporary snapshot. Never approves a
claim or release. Local/offline preparation only. No security guarantee against
malicious concurrent directory swaps or forged Git references.
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

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
SCANNER_BLOB = '31f3dcff486c4c8cc96d514eb425da86834d00c3'
MAX_BYTES = 5 * 1024 * 1024


def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def checked_bytes(path, expected):
    """No-follow final file component; verify bytes from one open descriptor."""
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    fd = os.open(path, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
            raise ValueError('nonregular or oversized input: ' + path.name)
        with os.fdopen(os.dup(fd), 'rb') as f:
            data = f.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES or blob_sha(data) != expected:
            raise ValueError('source blob mismatch: ' + path.name)
        return data
    finally:
        os.close(fd)


def snapshot(root, target, pins=None):
    pins = PINS if pins is None else pins
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('source directory must be real and existing')
    if set(pins) != set(PINS):
        raise ValueError('all eight expected source names are required')
    evidence = {}
    for name, expected in pins.items():
        if not isinstance(expected, str) or len(expected) != 40:
            raise ValueError('invalid source pin: ' + name)
        data = checked_bytes(root / name, expected)
        (target / name).write_bytes(data)
        evidence[name] = {'git_blob': expected, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
    return evidence


def run(root, out, scanner):
    root, out, scanner = Path(root).absolute(), Path(out).absolute(), Path(scanner)
    if out.resolve() == root.resolve() or root.resolve() in out.resolve().parents:
        raise ValueError('output must be outside source')
    if out.exists():
        raise ValueError('refusing to overwrite an existing output path')
    checked_bytes(scanner, SCANNER_BLOB)
    with tempfile.TemporaryDirectory(prefix='f001-scanner-snapshot-') as d:
        snap = Path(d)
        evidence = snapshot(root, snap)
        proc = subprocess.run([sys.executable, '-I', str(scanner.resolve()), str(snap), str(out)],
                              text=True, capture_output=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError('scanner failed: ' + proc.stderr[:400])
        rep = json.loads((out / 'claims-report.json').read_text(encoding='utf-8'))
        if set(rep.get('source_files', {})) != set(PINS) or any(
            rep['source_files'].get(name) != evidence[name]['sha256'] for name in PINS):
            raise ValueError('scanner source report does not match snapshot')
        return {'status': 'HOLD', 'source_files': evidence, 'rows': rep.get('rows'),
                'per_file': rep.get('per_file'), 'per_trigger': rep.get('per_trigger'),
                'claims_csv_sha256': hashlib.sha256((out / 'claims.csv').read_bytes()).hexdigest(),
                'claims_report_sha256': hashlib.sha256((out / 'claims-report.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit('usage: python -I F-001-SCANNER-SNAPSHOT-GATE-453.py SOURCE_DIR NEW_OUTPUT_DIR PINNED_SCANNER')
    try:
        print(json.dumps(run(*sys.argv[1:]), sort_keys=True))
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as e:
        print('HOLD / FAIL CLOSED: ' + str(e), file=sys.stderr)
        sys.exit(2)
