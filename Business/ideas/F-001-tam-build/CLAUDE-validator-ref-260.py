"""F-001 Claude reference variant of ChatGPT's synthetic custody validator (blob d8ede483, Issue #356).
Implements PROPOSED clauses (a)-(f) of section 259. Synthetic-only. Never authorizes release: always HOLD.
Same signature as ChatGPT's validate(); a comparison dataset, not a replacement of ChatGPT's file.
Usage: python3 -I CLAUDE-validator-ref-260.py <path to ChatGPT validator blob d8ede483>
"""
import hashlib, re, json, sys, importlib.util

SHA = re.compile(r'^[0-9a-f]{64}$')
REF_FIELDS = {'occurrence_id', 'start', 'end', 'quote_sha256'}
RIGHTS_HOLD = {'HOLD'}                      # clause (d): exact value, not a prefix
EDITORIAL_BASES = {'verified-span-review'}  # clause (e): listed bases; overlap is never listed

def _is_int(x):  # clause (b): bool is not an int here
    return isinstance(x, int) and not isinstance(x, bool)

def validate(unit, refs, source_bytes, expected_source_sha, rights='HOLD', editorial='HOLD', approval_basis=''):
    errors = []
    if not isinstance(expected_source_sha, str) or not SHA.fullmatch(expected_source_sha):
        errors.append('BAD_SHA256_FORMAT')
    elif hashlib.sha256(source_bytes).hexdigest() != expected_source_sha:
        errors.append('SOURCE_HASH_MISMATCH')
    if not refs and rights not in RIGHTS_HOLD:
        errors.append('ZERO_REFS_WITHOUT_HOLD')
    seen = set()
    for ref in refs:
        if not isinstance(ref, dict) or set(ref) != REF_FIELDS:  # clause (a)
            errors.append('MISSING_FIELD'); continue
        key = (unit, ref['occurrence_id'])
        if key in seen: errors.append('DUPLICATE_JOIN')
        seen.add(key)
        a, b = ref['start'], ref['end']
        if not _is_int(a) or not _is_int(b) or a < 0 or b <= a or b > len(source_bytes):
            errors.append('BAD_RANGE'); continue
        q = ref['quote_sha256']
        if not isinstance(q, str) or not SHA.fullmatch(q):  # clause (c)
            errors.append('BAD_SHA256_FORMAT'); continue
        quote = source_bytes[a:b]
        try: quote.decode('utf-8')                         # clause (f)
        except UnicodeDecodeError: errors.append('QUOTE_NOT_UTF8')
        if hashlib.sha256(quote).hexdigest() != q: errors.append('QUOTE_HASH_MISMATCH')
    if editorial != 'HOLD':
        if editorial != 'APPROVED': errors.append('BAD_EDITORIAL_VALUE')
        elif approval_basis == 'overlap-only': errors.append('OVERLAP_PROMOTION_REJECTED')
        elif approval_basis not in EDITORIAL_BASES: errors.append('EDITORIAL_BASIS_MISSING')  # clause (e)
    return {'errors': sorted(set(errors)), 'release': 'HOLD'}

def fixtures():
    src = 'synthetic TAM fixture – no publication'.encode('utf-8'); d = hashlib.sha256(src).hexdigest()
    ok = {'occurrence_id': 'O1', 'start': 0, 'end': 9, 'quote_sha256': hashlib.sha256(src[:9]).hexdigest()}
    h = lambda a, b: hashlib.sha256(src[a:b]).hexdigest()
    # (name, refs, source, digest, kwargs, expected errors under THIS variant) -- written before first run
    return [
      ('G1_positive', [ok], src, d, {}, []),
      ('G2_uppercase_source_sha', [ok], src, d.upper(), {}, ['BAD_SHA256_FORMAT']),
      ('G3_reversed_range', [dict(ok, start=9, end=0)], src, d, {}, ['BAD_RANGE']),
      ('G4_zero_hold', [], src, d, {'rights': 'HOLD'}, []),
      ('G5_zero_approved', [], src, d, {'rights': 'APPROVED'}, ['ZERO_REFS_WITHOUT_HOLD']),
      ('G6_duplicate', [ok, ok], src, d, {}, ['DUPLICATE_JOIN']),
      ('G7_overlap', [ok], src, d, {'editorial': 'APPROVED', 'approval_basis': 'overlap-only'}, ['OVERLAP_PROMOTION_REJECTED']),
      ('G8_source_mutation', [ok], src + b'x', d, {}, ['SOURCE_HASH_MISMATCH']),
      ('E1_missing_quote_key', [{k: v for k, v in ok.items() if k != 'quote_sha256'}], src, d, {}, ['MISSING_FIELD']),
      ('E2_bool_start', [dict(ok, start=False)], src, d, {}, ['BAD_RANGE']),
      ('E3_uppercase_quote_sha', [dict(ok, quote_sha256=ok['quote_sha256'].upper())], src, d, {}, ['BAD_SHA256_FORMAT']),
      ('E4_end_eq_len_ok', [dict(ok, end=len(src), quote_sha256=h(0, len(src)))], src, d, {}, []),
      ('E5_rights_HOLDX_prefix_zero_refs', [], src, d, {'rights': 'HOLDOUT-APPROVED'}, ['ZERO_REFS_WITHOUT_HOLD']),
      ('E6_editorial_approved_no_basis', [ok], src, d, {'editorial': 'APPROVED', 'approval_basis': ''}, ['EDITORIAL_BASIS_MISSING']),
      ('E7_utf8_midchar_split', [dict(ok, start=22, end=23, quote_sha256=h(22, 23))], src, d, {}, ['QUOTE_NOT_UTF8']),
      ('N1_extra_field', [dict(ok, note='x')], src, d, {}, ['MISSING_FIELD']),
      ('N2_listed_basis_ok', [ok], src, d, {'editorial': 'APPROVED', 'approval_basis': 'verified-span-review'}, []),
    ]

def _call(fn, *a, **k):
    try: return fn(*a, **k)['errors']
    except Exception as e: return 'EXC:' + type(e).__name__

def main():
    gpt = None
    if len(sys.argv) > 1:
        spec = importlib.util.spec_from_file_location('gptv', sys.argv[1]); gpt = importlib.util.module_from_spec(spec); spec.loader.exec_module(gpt)
    rows = []
    for name, refs, src, d, kw, exp in fixtures():
        mine = _call(validate, 'SYN', refs, src, d, **kw)
        row = {'fixture': name, 'expected_ref': exp, 'ref_variant': mine, 'ref_matches_expected': mine == exp}
        if gpt: row['gpt_d8ede483'] = _call(gpt.validate, 'SYN', refs, src, d, **kw)
        rows.append(row)
    print(json.dumps({'rows': rows, 'ref_pass': sum(r['ref_matches_expected'] for r in rows), 'total': len(rows),
                      'release_always': 'HOLD'}, indent=1, sort_keys=True))

if __name__ == '__main__': main()
