"""F-001 read-only full-text queue verifier; PRE-TEST Issue #61.
Use: python3 -I f001_full_sentence_verify_388.py QUEUE.json TAM_SOURCE_DIR
Only validates provenance and HOLD; not a fact checker or release authority.
"""
import hashlib, json, re, sys
from collections import Counter
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

def git_blob_sha(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def sentences(raw):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n{2,}', raw.decode('utf-8')) if s.strip()]

def normalize(s):
    return re.sub(r'\s+', ' ', re.sub('[\u200b-\u200d\ufeff]', '', s)).strip()

def verify(queue, src, pins=None, expected_count=45):
    pins = PINS if pins is None else pins
    errors, data = [], {}
    if queue.get('status') != 'HOLD' or queue.get('release_authorized') is not False:
        errors.append('release-state')
    cards = queue.get('cards', [])
    if len(cards) != expected_count or queue.get('card_count') != expected_count:
        errors.append('card-count')
    for name, pin in pins.items():
        path = src / name
        if '/' in name or '\\' in name or name.startswith('.') or path.is_symlink() or not path.is_file():
            errors.append('missing-or-unsafe:'+name); continue
        raw = path.read_bytes()
        if git_blob_sha(raw) != pin:
            errors.append('blob-mismatch:'+name); continue
        data[name] = sentences(raw)
    seen, texts, counts = set(), Counter(), Counter()
    for card in cards:
        cid, name, n = card.get('id'), card.get('source_file'), card.get('sentence_no')
        if cid in seen: errors.append('duplicate-id:'+str(cid))
        seen.add(cid)
        counts[name] += 1
        if card.get('review_status') != 'UNREVIEWED' or any(card.get(k) is not None for k in ('editorial_disposition','evidence_reference','rights_clearance')):
            errors.append('review-state:'+str(cid))
        if name not in data or type(n) is not int or n < 1 or n > len(data[name]):
            errors.append('missing-sentence:'+str(cid)); continue
        full = data[name][n-1]
        if cid != name+'#S'+str(n) or card.get('source_blob_sha') != pins[name]:
            errors.append('source-reference:'+str(cid))
        if card.get('full_sentence') != full or not full.startswith(card.get('excerpt','')):
            errors.append('text-binding:'+str(cid))
        if card.get('was_truncated') is not (full != card.get('excerpt')):
            errors.append('truncation:'+str(cid))
        if card.get('previous_sentence') != (data[name][n-2] if n>1 else None):
            errors.append('previous-context:'+str(cid))
        if card.get('next_sentence') != (data[name][n] if n<len(data[name]) else None):
            errors.append('next-context:'+str(cid))
        texts[normalize(full)] += 1
    if dict(counts) != queue.get('source_counts'): errors.append('source-counts')
    if queue.get('unique_normalized_sentence_count') != len(texts): errors.append('unique-count')
    if queue.get('duplicate_group_count') != sum(x>1 for x in texts.values()): errors.append('duplicate-groups')
    return errors

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    errors = verify(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')), Path(sys.argv[2]))
    print(json.dumps({'status':'HOLD','release_authorized':False,'errors':errors},indent=2))
    sys.exit(bool(errors))
