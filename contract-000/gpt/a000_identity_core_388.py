"""Proposed identity-core validation candidate; NOT production Governor.
Source inspected: genesis-documentary/src/echo_governor_skeleton.py blob
63eb982989b4f3478d649430b555c8f4ba755c27, ReshIdentity 3233-3305.
PRE-TEST: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/61
"""

IDENTITY_FIELDS = {
    'identity_symbol': 'resh',
    'identity_glyph': 'ר',
    'identity_letter': 'resh',
    'identity_meaning': 'head beginning leader identity',
}
ALIAS_FIELDS = {
    'name': 'Resh — Governor Identity Anchor',
    'status': 'ACTIVE',
    'type': 'IDENTITY-LETTER',
    'glyph': 'ר',
    'aliases': ['A-000', 'resh', 'governor'],
    'perception_operator': 'ayin',
    'expression_operator': 'pe',
}

def validate_candidate(matrix, anchored):
    """Field-scope proposal: strict types and required identity values, not custody.

    Unrelated metadata is permitted; receipt issuance and authorized mutation
    remain outside this proposal. No canonicalization or cryptographic attestation.
    """
    if type(anchored) is not bool or not anchored:
        return False
    if type(matrix) is not dict:
        return False
    a000 = matrix.get('A-000')
    alias = matrix.get('A-000-RESH')
    if type(a000) is not dict or type(alias) is not dict:
        return False
    for key, expected in IDENTITY_FIELDS.items():
        if type(a000.get(key)) is not type(expected) or a000.get(key) != expected:
            return False
    for key, expected in ALIAS_FIELDS.items():
        value = alias.get(key)
        if type(value) is not type(expected) or value != expected:
            return False
    return True


def source_validate(matrix, anchored):
    """Exact logical predicate of pinned source validate() without class wrapper."""
    return (anchored and 'A-000-RESH' in matrix and
            matrix.get('A-000', {}).get('identity_symbol') == 'resh')


def anchored_fixture():
    """Minimum fields from pinned anchor(); excludes long description text."""
    return {'A-000': dict(IDENTITY_FIELDS),
            'A-000-RESH': {**ALIAS_FIELDS, 'description': 'original source description'}}
