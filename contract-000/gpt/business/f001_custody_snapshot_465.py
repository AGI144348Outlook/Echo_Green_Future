#!/usr/bin/env python3
"""F-001 HOLD-only executable-pinned receipt with private data snapshots.

Integrity of bytes is not authentication of Timothy, the machine, or a release.
This successor leaves the Run463 validator and Run464 wrapper unchanged.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT = 'F-001'
STATUS = 'HOLD / NOT LAUNCH-READY'
VERSION = 'F-001-custody-receipt/v3-snapshot-hold'
GATE_BLOB = '5a767d9110554a2cad855f9291ee696b46cc17a3'
REGISTER_BLOB = '300dfcf0ba9e9d236326d09b2a4b6c5467d3874c'
LOCATION_BLOB = '7fb5cd952127de7a0469cfb3d0139d7bdfb60b86'
INTAKE_BLOB = '4cc1617d1f1bbea1661f74ba931f86660c087939'


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def unique_json(text):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError('duplicate receipt key: ' + key)
            obj[key] = value
        return obj
    return json.loads(text, object_pairs_hook=unique)


def attest(gate, register, location, intake, *, expected_gate_blob=GATE_BLOB,
           expected_register_blob=REGISTER_BLOB, expected_location_blob=LOCATION_BLOB,
           expected_intake_blob=INTAKE_BLOB, interpreter=sys.executable):
    paths = (Path(gate), Path(register), Path(location), Path(intake))
    # Read each source ONCE. These four immutable byte strings are the authority
    # for both pin verification and the subprocess's eventual input.
    data = tuple(path.read_bytes() for path in paths)
    pins = (expected_gate_blob, expected_register_blob, expected_location_blob, expected_intake_blob)
    for label, actual, expected in zip(('gate', 'register', 'location', 'intake'), data, pins):
        if git_blob(actual) != expected:
            raise ValueError(label + ': Git blob differs from reviewed pin')
    source = data[0].decode('utf-8', errors='strict')
    # Never hand the original mutable data paths to the subprocess. A private
    # directory, automatically removed on both success and refusal, contains
    # the EXACT data bytes already checked above.
    with tempfile.TemporaryDirectory(prefix='f001-verified-snapshot-') as temp:
        snapshots = []
        for name, contents in zip(('register.tsv', 'location.tsv', 'intake.tsv'), data[1:]):
            path = Path(temp) / name
            path.write_bytes(contents)
            path.chmod(0o400)
            snapshots.append(str(path))
        completed = subprocess.run(
            [interpreter, '-I', '-B', '-c', source, *snapshots],
            capture_output=True, text=True, encoding='utf-8',
            timeout=30, check=False)
    if completed.returncode != 0 or completed.stderr or not completed.stdout:
        raise ValueError('pinned gate refused input or produced an execution error')
    try:
        receipt = unique_json(completed.stdout)
    except (ValueError, json.JSONDecodeError) as exc:
        raise ValueError('pinned gate emitted invalid/ambiguous JSON') from exc
    if not isinstance(receipt, dict):
        raise ValueError('pinned gate emitted a non-object receipt')
    expected = {
        'project': PROJECT, 'status': STATUS,
        'register_git_blob': expected_register_blob,
        'location_map_git_blob': expected_location_blob,
        'intake_git_blob': expected_intake_blob,
        'occurrences': 82, 'copy_links': 10, 'pending': 82, 'approved': 0,
        'approval_authenticated': False, 'editorial_overlay_applied': False,
        'publication_authorized': False,
    }
    if receipt != expected:
        raise ValueError('pinned gate receipt differs from required HOLD-only schema')
    return {**receipt, 'receipt_version': VERSION,
            'gate_script_git_blob': expected_gate_blob,
            'gate_script_sha256': hashlib.sha256(data[0]).hexdigest(),
            'input_snapshot_mode': 'private-verified-byte-snapshots',
            'produced_by_wrapper_run': True,
            'timothy_approval_authenticated': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description='F-001 HOLD-only snapshot-bound custody receipt')
    for name in ('gate', 'register', 'location_map', 'intake'):
        parser.add_argument(name, type=Path)
    args = parser.parse_args(argv)
    try:
        receipt = attest(args.gate, args.register, args.location_map, args.intake)
    except (OSError, ValueError, subprocess.TimeoutExpired, UnicodeError) as exc:
        print('F-001 HOLD / ATTESTATION REFUSED: ' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(receipt, sort_keys=True, separators=(',', ':'), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
