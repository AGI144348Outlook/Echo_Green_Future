#!/usr/bin/env python3
"""F-001 HOLD-only public-source fetch + exact pinned original Python scanner replay.

Usage: python3 -I -B f001_public_fetch_replay_413.py
Fetches only fixed public GitHub raw URLs, verifies exact Git blob bytes, runs
Run412's pinned offline snapshot runner in a temporary directory, and discards
all source files and worksheets. No credentials, publication or account actions.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

TAM_REPO = 'AGI144348Outlook/The-TAM-protocol'
TAM_COMMIT = 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9'
ECHO_REPO = 'AGI144348Outlook/Echo_Green_Future'
GPT_COMMIT = '986590b058d7a847eeaeb43523815717687f91ef'
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
MAX_BYTES = 2 * 1024 * 1024

def blob_hash(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()

def raw_url(repo, commit, path):
    return ('https://raw.githubusercontent.com/' + repo + '/' + commit + '/' +
            '/'.join(urllib.parse.quote(segment, safe='') for segment in path.split('/')))

def fetch_verified(url, pin, opener=urllib.request.urlopen):
    if not url.startswith('https://raw.githubusercontent.com/'):
        raise ValueError('disallowed source host')
    with opener(url, timeout=20) as response:
        final = response.geturl()
        if final != url:
            raise ValueError('redirected source URL rejected')
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('source exceeds size cap')
    if blob_hash(data) != pin:
        raise ValueError('Git blob pin mismatch')
    return data

def main():
    with tempfile.TemporaryDirectory(prefix='f001-public-hold-') as td:
        root = Path(td)
        tam = root / 'tam'
        tam.mkdir()
        for path, pin in PINS.items():
            data = fetch_verified(raw_url(TAM_REPO, TAM_COMMIT, path), pin)
            (tam / path).write_bytes(data)
        # Pin the scanner by content hash; the branch ref is not trusted.
        scanner = root / 'claim_scan.py'
        scanner.write_bytes(fetch_verified(raw_url(ECHO_REPO, 'library-shared',
                          'Business/ideas/F-001-tam-build/claim_scan.py'), SCANNER_BLOB))
        runner = root / 'f001_scanner_snapshot_412.py'
        runner.write_bytes(fetch_verified(raw_url(ECHO_REPO, GPT_COMMIT,
                          'contract-000/gpt/business/F-001-SCANNER-SNAPSHOT-412.py'), RUNNER_BLOB))
        proc = subprocess.run([sys.executable, '-I', '-B', str(runner), str(tam), str(scanner)],
                              cwd=root, capture_output=True, text=True, timeout=90)
        try:
            receipt = json.loads(proc.stdout.strip())
        except json.JSONDecodeError:
            raise ValueError('snapshot runner returned invalid JSON')
        if proc.returncode or receipt.get('audit') != 'PASS' or receipt.get('rows') != 42 or receipt.get('source_files') != 8 or receipt.get('status') != 'HOLD / NOT LAUNCH-READY' or receipt.get('release_authorized') is not False:
            raise ValueError('snapshot runner failed or receipt incomplete: ' + str(receipt))
        return receipt

if __name__ == '__main__':
    try:
        print(json.dumps(main(), sort_keys=True))
    except (OSError, ValueError, TimeoutError, urllib.error.URLError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'audit': 'FAIL', 'project': 'F-001', 'status': 'HOLD / NOT LAUNCH-READY',
                          'reason': str(exc), 'release_authorized': False}, sort_keys=True))
        sys.exit(1)
