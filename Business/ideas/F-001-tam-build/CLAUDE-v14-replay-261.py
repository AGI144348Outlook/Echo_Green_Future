"""F-001 section 261 (Claude 16Z): replay of ChatGPT's custody validator v14 (blob 304854cb, Issue #357/#358).
Runs (1) v14's own run() and (2) Claude's 17 section-260 fixtures plus 9 new probes P1-P9 against v14.
Expected v14 results below were written from reading the v14 source BEFORE the first run (same-run, not pre-registered on an Issue).
Synthetic-only; never authorizes release. Does not modify ChatGPT's file.
Usage: python3 -I -B CLAUDE-v14-replay-261.py <v14 blob path> <CLAUDE-validator-ref-260.py path>
"""
import hashlib, json, sys, importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

EXPECT_V14 = {
 'G1_positive': [], 'G2_uppercase_source_sha': ['BAD_SHA256_FORMAT'], 'G3_reversed_range': ['BAD_RANGE'],
 'G4_zero_hold': [], 'G5_zero_approved': ['ZERO_REFS_WITHOUT_HOLD'], 'G6_duplicate': ['DUPLICATE_JOIN'],
 'G7_overlap': ['UNSUPPORTED_EDITORIAL_APPROVAL'], 'G8_source_mutation': ['SOURCE_HASH_MISMATCH'],
 'E1_missing_quote_key': ['BAD_QUOTE_SHA256_FORMAT'], 'E2_bool_start': ['BAD_RANGE'],
 'E3_uppercase_quote_sha': ['BAD_QUOTE_SHA256_FORMAT'], 'E4_end_eq_len_ok': [],
 'E5_rights_HOLDX_prefix_zero_refs': ['BAD_RIGHTS_DECISION', 'ZERO_REFS_WITHOUT_HOLD'],
 'E6_editorial_approved_no_basis': ['UNSUPPORTED_EDITORIAL_APPROVAL'], 'E7_utf8_midchar_split': ['BAD_UTF8_BOUNDARY'],
 'N1_extra_field': [], 'N2_listed_basis_ok': [],
 'P1_free_text_basis': [], 'P2_rights_approved_with_refs': [], 'P3_bytearray_source': ['BAD_SOURCE_TYPE'],
 'P4_refs_none': 'EXC:TypeError', 'P5_refs_string': ['BAD_REFERENCE'], 'P6_unhashable_unit': 'EXC:TypeError',
 'P7_occurrence_int': ['BAD_OCCURRENCE'], 'P8_end_split_char': ['BAD_UTF8_BOUNDARY'], 'P9_lowercase_rights_hold': ['BAD_RIGHTS_DECISION'],
}

def probes(src, d, ok):
    h = lambda a, b: hashlib.sha256(src[a:b]).hexdigest()
    return [
      ('P1_free_text_basis', 'SYN', [ok], src, d, {'editorial': 'APPROVED', 'approval_basis': 'anything'}),
      ('P2_rights_approved_with_refs', 'SYN', [ok], src, d, {'rights': 'APPROVED'}),
      ('P3_bytearray_source', 'SYN', [ok], bytearray(src), d, {}),
      ('P4_refs_none', 'SYN', None, src, d, {}),
      ('P5_refs_string', 'SYN', 'x', src, d, {}),
      ('P6_unhashable_unit', ['SYN'], [ok], src, d, {}),
      ('P7_occurrence_int', 'SYN', [dict(ok, occurrence_id=1)], src, d, {}),
      ('P8_end_split_char', 'SYN', [dict(ok, start=0, end=23, quote_sha256=h(0, 23))], src, d, {}),
      ('P9_lowercase_rights_hold', 'SYN', [ok], src, d, {'rights': 'hold'}),
    ]

def call(fn, *a, **k):
    try: return fn(*a, **k)['errors']
    except Exception as e: return 'EXC:' + type(e).__name__

def main():
    v14 = load('gptv14', sys.argv[1]); ref = load('ref260', sys.argv[2])
    own = v14.run()
    cases = [(n, 'SYN', r, s, d, k) for n, r, s, d, k, _ in ref.fixtures()]
    src = 'synthetic TAM fixture – no publication'.encode('utf-8'); d = hashlib.sha256(src).hexdigest()
    ok = {'occurrence_id': 'O1', 'start': 0, 'end': 9, 'quote_sha256': hashlib.sha256(src[:9]).hexdigest()}
    cases += probes(src, d, ok)
    rows = []
    for n, unit, r, s, dg, k in cases:
        got = call(v14.validate, unit, r, s, dg, **k)
        rows.append({'case': n, 'v14': got, 'expected_v14': EXPECT_V14[n], 'match': got == EXPECT_V14[n],
                     'ref260': call(ref.validate, unit, r, s, dg, **k)})
    print(json.dumps({'v14_own_run': own, 'rows': rows, 'match': sum(x['match'] for x in rows), 'total': len(rows),
                      'release_always': 'HOLD'}, indent=1, sort_keys=True))

if __name__ == '__main__': main()
