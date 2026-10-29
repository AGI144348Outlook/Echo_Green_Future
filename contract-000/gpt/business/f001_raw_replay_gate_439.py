#!/usr/bin/env python3
"""F-001 draft-only fail-closed gate for local original-Python claim scanner replay.
No network, no source edits, no publication. Requires exact raw source snapshot.
Usage: python3 -I f001_raw_replay_gate_439.py SRC SCANNER MANIFEST OUT
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SCANNER_BLOB = '31f3dcff486c4c8cc96d514eb425da86834d00c3'
FILES = ['README.md', 'Article 1 Hacksilber', 'Article 2 Water Weight Computes',
         'The Color Dyed and Dental Records', 'Article 5', 'Article 6',
         'Article 10', 'Collective information']
HEADER = ['file', 'sentence_no', 'triggers', 'sentence', 'status']


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def require(cond, msg):
    if not cond:
        raise ValueError(msg)


def path_no_symlinks(p):
    p = Path(os.path.abspath(p))
    for q in (p, *p.parents):
        require(not q.is_symlink(), 'symlink component: ' + str(q))
    return p


def utf16_prefix_matches(sentence, excerpt):
    # Manifest's historical excerpt convention uses UTF-16 code units, not Python codepoints.
    e = excerpt.encode('utf-16-le')
    return sentence.encode('utf-16-le')[:len(e)] == e


def main(src, scanner, manifest_path, out):
    src, scanner, manifest_path, out = map(path_no_symlinks, (src, scanner, manifest_path, out))
    require(src.is_dir(), 'source directory absent')
    require(scanner.is_file(), 'original scanner absent')
    require(manifest_path.is_file(), 'manifest absent')
    require(src != out and src not in out.parents, 'output inside source')
    require(out != scanner.parent and out != manifest_path.parent, 'output overwrites input directory')
    require(not out.exists() or (out.is_dir() and not any(out.iterdir())), 'output not empty')
    require(git_blob(scanner.read_bytes()) == SCANNER_BLOB, 'scanner Git blob mismatch')
    m = json.loads(manifest_path.read_text(encoding='utf-8'))
    require(m.get('project') == 'F-001', 'project mismatch')
    require(m.get('source_commit') == 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9', 'source commit mismatch')
    expected_files = m.get('source_files')
    require(isinstance(expected_files, list) and len(expected_files) == len(FILES), 'expected exactly eight source pins')
    require([x.get('path') for x in expected_files] == FILES, 'source file list mismatch')
    hashes = {}
    for x in expected_files:
        p = src / x['path']
        require(not p.is_symlink() and p.is_file(), 'missing/symlink source: ' + x['path'])
        raw = p.read_bytes()
        require(git_blob(raw) == x.get('blob_sha'), 'source Git blob mismatch: ' + x['path'])
        hashes[x['path']] = hashlib.sha256(raw).hexdigest()
    expected_rows = m.get('rows')
    require(isinstance(expected_rows, list) and len(expected_rows) == 42, 'expected 42 source-bound candidates')
    out.mkdir(parents=True, exist_ok=True)
    cp = subprocess.run([sys.executable, '-I', str(scanner), str(src), str(out)],
                        text=True, capture_output=True, timeout=45, check=False)
    require(cp.returncode == 0, 'scanner exit=' + str(cp.returncode) + ': ' + cp.stderr[-500:])
    csvpath, reportpath = out / 'claims.csv', out / 'claims-report.json'
    require(csvpath.is_file() and reportpath.is_file(), 'missing scanner output')
    with csvpath.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        require(reader.fieldnames == HEADER, 'unexpected CSV columns')
        rows = list(reader)
    report = json.loads(reportpath.read_text(encoding='utf-8'))
    require(len(rows) == len(expected_rows) == report.get('rows'), 'row count mismatch')
    require(report.get('source_files') == hashes, 'report source hashes mismatch')
    require(set(report.get('per_file', {})) == set(FILES), 'report missing file count')
    counts = {name: 0 for name in FILES}
    for r, expected in zip(rows, expected_rows):
        require(r['file'] == expected['source'], 'candidate file/order mismatch')
        require(int(r['sentence_no']) == expected['sentence_no'], 'candidate coordinate mismatch')
        require(r['triggers'].split(';') == expected['triggers'], 'candidate trigger mismatch')
        require(r['status'] == '', 'scanner assigned editorial status')
        require(utf16_prefix_matches(r['sentence'], expected['excerpt']), 'candidate excerpt mismatch')
        counts[r['file']] += 1
    require(counts == report['per_file'], 'per-file counts mismatch')
    return {'result': 'LOCAL_SOURCE_AND_SCANNER_PARITY_ONLY', 'rows': len(rows),
            'source_git_blobs_verified': len(hashes),
            'source_sha256': hashes,
            'claims_csv_sha256': hashlib.sha256(csvpath.read_bytes()).hexdigest(),
            'claims_report_sha256': hashlib.sha256(reportpath.read_bytes()).hexdigest(),
            'limitations': 'No semantic, historical, rights, editorial, coordinator or release approval'}


if __name__ == '__main__':
    try:
        if len(sys.argv) != 5:
            raise ValueError(__doc__)
        print(json.dumps(main(*sys.argv[1:]), indent=2))
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print('HOLD: ' + str(exc), file=sys.stderr)
        sys.exit(2)
