#!/usr/bin/env python3
"""Read-only F-001 dataset release characterization gate (GPT run 295).

Checks delivered CSVs against hashes independently rebuilt earlier from the
pinned TAM source blobs using the pinned shared builder. Does not claim source
truth, license approval, editorial approval, or independent trust.
Exit 0: integrity check ran and passed; editorial HOLD may still be present.
Exit 1: integrity fails.
Exit 3: integrity passes but editorial HOLD, only with --release-gate.
Exit 64: usage error.
This is an unintegrated characterization draft; no output authorizes launch.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

SOURCE_COMMIT = 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9'  # provenance record; not verified by this script
PINS = {
    'Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)': 'b62c970a660e0a6685b58db1ef121690daa4fce7',
    'Dataset_B_Binary_Matrix.md': '12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4',
    'rebuild_datasets.py': 'fa3a62f76549ecaea6e226ba5cca41597000d790',
}
DATA = {
    'A': {'name': 'dataset-a.csv', 'rows': 6, 'sha256': 'd3c176b9d2ff8041b093f46f28c7b56619d1e1cc3b3ea4841b12027e5ec826f2',
          'header': ['object', 'measured_g', 'units', 'registry_sign', 'stated_deviation_pct', 'term', 'expected_g', 'recomputed_deviation_pct', 'stated_matches_recomputed'],
          'source': 'Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)'},
    'B': {'name': 'dataset-b.csv', 'rows': 8, 'sha256': 'fecd151b5b7393fc69975a0b323e02c5f306eb1fd49bedc2901f849001e8afc5',
          'header': ['ratio', 'mass_g', 'registry_sign', 'units', 'relation_to_dataset_a', 'expected_g_from_units', 'deviation_pct', 'ratio_over_16_equals_units'],
          'source': 'Dataset_B_Binary_Matrix.md'},
}
REPORT_SHA256 = '036a85e5fe3b372c6ada0e0851f3463fd6da3e5d6ab825972cb454085f85dde4'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def verify(source_dir, builder, delivery_dir, release_gate=False):
    errors, review = [], []
    for name, expected in PINS.items():
        p = builder if name == 'rebuild_datasets.py' else source_dir / name
        try:
            actual = blob_sha(p.read_bytes())
        except OSError as exc:
            errors.append(f'{name}: missing/unreadable: {exc}'); continue
        if actual != expected:
            errors.append(f'{name}: Git blob mismatch {actual} != {expected}')

    report_file = delivery_dir / 'dataset-check.json'
    try:
        raw = report_file.read_bytes()
        report = json.loads(raw)
        if digest(raw) != REPORT_SHA256:
            errors.append('dataset-check.json: output digest mismatch')
    except (OSError, ValueError) as exc:
        errors.append(f'dataset-check.json: missing/invalid: {exc}')
        report = {}

    for label, spec in DATA.items():
        path = delivery_dir / spec['name']
        try:
            raw = path.read_bytes()
            if digest(raw) != spec['sha256']:
                errors.append(f'{spec["name"]}: full-byte output digest mismatch')
            with path.open(newline='', encoding='utf-8') as fh:
                rows = list(csv.reader(fh))
            if not rows or rows[0] != spec['header']:
                errors.append(f'{spec["name"]}: header mismatch')
                continue
            if len(rows) - 1 != spec['rows']:
                errors.append(f'{spec["name"]}: row count mismatch {len(rows)-1} != {spec["rows"]}')
            if any(len(row) != len(spec['header']) for row in rows[1:]):
                errors.append(f'{spec["name"]}: malformed row width')
            if label == 'A':
                for row_num, row in enumerate(rows[1:], 2):
                    if len(row) == len(spec['header']) and row[-1] != 'True':
                        review.append(f'{spec["name"]} row {row_num}: stated_matches_recomputed={row[-1]}')
        except (OSError, UnicodeError, csv.Error) as exc:
            errors.append(f'{spec["name"]}: missing/unreadable: {exc}')
        try:
            entry = report['files'][label]
            source_bytes = (source_dir / spec['source']).read_bytes()
            if entry['sha256'] != digest(source_bytes):
                errors.append(f'{label}: source digest mismatch in dataset-check.json')
            if entry['rows'] != spec['rows'] or entry['rejected'] != []:
                errors.append(f'{label}: row count/rejected rows in dataset-check.json')
        except (KeyError, TypeError, OSError) as exc:
            errors.append(f'{label}: missing/invalid report fields: {exc}')

    result = {'source_commit_recorded': SOURCE_COMMIT,
              'source_pin_authenticated': False,
              'integrity': 'FAIL' if errors else 'PASS',
              'editorial': 'HOLD' if review else 'NO_FLAGGED_ROWS',
              'release': 'HOLD' if errors or review else 'OTHER_GATES_PENDING',
              'errors': errors, 'editorial_review': review,
              'gate_mode': 'release' if release_gate else 'integrity'}
    print(json.dumps(result, indent=2))
    return 1 if errors else (3 if review and release_gate else 0)


if __name__ == '__main__':
    args = sys.argv[1:]
    release_gate = bool(args and args[0] == '--release-gate')
    if release_gate:
        args = args[1:]
    if len(args) != 3 or any(x.startswith('--') for x in args):
        print('usage: python3 -I -B PROPOSED-f001-dataset-receipt-gate-v2.py [--release-gate] <source-dir> <builder.py> <delivery-dir>', file=sys.stderr)
        sys.exit(64)
    sys.exit(verify(Path(args[0]), Path(args[1]), Path(args[2]), release_gate))
