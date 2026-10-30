#!/usr/bin/env python3
"""F-001 HOLD-only gate-code attestation. No approval or publication capability.

Runs only the byte-pinned Run463 gate, and binds the emitted HOLD receipt to
that executable and its three exact data inputs. A hash is an integrity check,
not an authentication of Timothy or of the executing environment.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PROJECT = 'F-001'
STATUS = 'HOLD / NOT LAUNCH-READY'
VERSION = 'F-001-custody-receipt/v2-hold'
GATE_BLOB = '5a767d9110554a2cad855f9291ee696b46cc17a3'
REGISTER_BLOB = '300dfcf0ba9e9d236326d09b2a4b6c5467d3874c'
LOCATION_BLOB = '7fb5cd952127de7a0469cfb3d0139d7bdfb60b86'
INTAKE_BLOB = '4cc1617d1f1bbea1661f74ba931f86660c087939'


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def unique_json(text):
    def unique(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError('duplicate receipt key: ' + k)
            d[k] = v
        return d
    return json.loads(text, object_pairs_hook=unique)


def attest(gate, register, location, intake, *, expected_gate_blob=GATE_BLOB,
           expected_register_blob=REGISTER_BLOB, expected_location_blob=LOCATION_BLOB,
           expected_intake_blob=INTAKE_BLOB, interpreter=sys.executable):
    paths = (Path(gate), Path(register), Path(location), Path(intake))
    data = [p.read_bytes() for p in paths]
    pins = (expected_gate_blob, expected_register_blob, expected_location_blob, expected_intake_blob)
    for label, actual, expected in zip(('gate', 'register', 'location', 'intake'), data, pins):
        if git_blob(actual) != expected:
            raise ValueError(label + ': Git blob differs from reviewed pin')
    # Execute the EXACT verified bytes, not a path that could change after hashing.
    # The pinned Run463 gate does not depend on __file__. No shell or file writes.
    source = data[0].decode('utf-8', errors='strict')
    completed = subprocess.run([interpreter, '-I', '-B', '-c', source,
                                str(paths[1].resolve()), str(paths[2].resolve()),
                                str(paths[3].resolve())], capture_output=True, text=True,
                               encoding='utf-8', timeout=30, check=False)
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
    # Explicitly bind to gate bytes; receipt remains evidence of this local run,
    # NOT an independently signed or trusted execution attestation.
    return {**receipt, 'receipt_version': VERSION,
            'gate_script_git_blob': expected_gate_blob,
            'gate_script_sha256': hashlib.sha256(data[0]).hexdigest(),
            'execution_verified_locally': True,
            'timothy_approval_authenticated': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description='F-001 HOLD-only executable-pinned custody receipt')
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
