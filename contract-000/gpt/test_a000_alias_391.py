#!/usr/bin/env python3
"""HOLD-only isolated source-transcribed ReshIdentity tests.

Source: Echo_Green_Future genesis-documentary:src/echo_governor_skeleton.py
Git blob 63eb982989b4f3478d649430b555c8f4ba755c27, lines 3233-3305.
Pre-test: Issue #64. Not a full Governor import, race, or production fix.
"""
import copy
import hashlib
import json


class MatrixStub:
    def __init__(self):
        self.known = {'A-000': {'name': 'Governor', 'status': 'ACTIVE'}}


class ReshIdentity:
    # Methods transcribed from pinned Genesis source; Lobby=None in all tests.
    def __init__(self, matrix, hebrew_lobby=None):
        self.matrix = matrix
        self.hebrew_lobby = hebrew_lobby
        self._anchored = False
        self._anchor_entry = None

    def anchor(self):
        a000 = self.matrix.known.get('A-000', {})
        a000['identity_symbol'] = 'resh'
        a000['identity_glyph'] = 'ר'
        a000['identity_letter'] = 'resh'
        a000['identity_meaning'] = 'head beginning leader identity'
        self.matrix.known['A-000'] = a000
        self.matrix.known['A-000-RESH'] = {
            'name': 'Resh — Governor Identity Anchor',
            'status': 'ACTIVE',
            'type': 'IDENTITY-LETTER',
            'glyph': 'ר',
            'aliases': ['A-000', 'resh', 'governor'],
            'description': (
                'The Governor and Resh are one and the same — '
                'Resh is head, beginning, identity; the Governor '
                'reads Resh when it reads itself in the matrix. '
                'Identity validation (IDENTIFY→VALIDATE→OPEN) '
                'runs through this entry.'),
            'perception_operator': 'ayin',
            'expression_operator': 'pe',
        }
        if self.hebrew_lobby:
            resh_agent = self.hebrew_lobby.agents.get('resh')
            if resh_agent:
                resh_agent.definition_words = list(set(
                    resh_agent.definition_words +
                    ['governor', 'indexing', 'algorithm', 'identity',
                     'matrix', 'aleph', 'ayin', 'pe']))
        self._anchored = True
        self._anchor_entry = self.matrix.known['A-000-RESH']
        return self._anchor_entry

    def validate(self):
        return (self._anchored
                and 'A-000-RESH' in self.matrix.known
                and self.matrix.known.get('A-000', {}).get(
                    'identity_symbol') == 'resh')


def digest(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def snapshot(matrix):
    return copy.deepcopy({k: matrix.known[k] for k in ('A-000', 'A-000-RESH')})


def check(name, fn):
    fn()
    print('PASS', name)


def main():
    m = MatrixStub()
    r = ReshIdentity(m)
    check('unanchored_false', lambda: assert_equal(bool(r.validate()), False))
    alias = r.anchor()
    snap = snapshot(m)
    frozen = digest(snap)
    check('anchored_true', lambda: assert_equal(bool(r.validate()), True))
    check('returned_alias_is_shared_reference', lambda: assert_equal(alias is m.known['A-000-RESH'], True))
    alias['status'] = 'TAMPERED'
    check('alias_mutation_validation_still_true', lambda: assert_equal(bool(r.validate()), True))
    check('detached_full_snapshot_detects_alias_mutation', lambda: assert_equal(digest(snapshot(m)) != frozen, True))
    alias['status'] = 'ACTIVE'
    m.known['A-000']['status'] = 'RETIRED'
    check('a000_status_mutation_validation_still_true', lambda: assert_equal(bool(r.validate()), True))
    check('detached_full_snapshot_detects_a000_status_mutation', lambda: assert_equal(digest(snapshot(m)) != frozen, True))
    # Core-only design would permit status metadata to evolve, subject to Timothy's ruling.
    m.known['A-000']['status'] = 'ACTIVE'
    m.known['A-000']['identity_symbol'] = 'foreign'
    check('symbol_mutation_validation_false', lambda: assert_equal(bool(r.validate()), False))
    m.known['A-000']['identity_symbol'] = 'resh'
    m.known['A-000-RESH'] = None
    check('alias_none_presence_only_validation_true', lambda: assert_equal(bool(r.validate()), True))
    del m.known['A-000-RESH']
    check('alias_absent_validation_false', lambda: assert_equal(bool(r.validate()), False))
    print('PASS: 10/10 isolated assertions; not complete Genesis execution')


def assert_equal(a, b):
    assert a == b, f'{a!r} != {b!r}'


if __name__ == '__main__':
    main()
