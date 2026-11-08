"""F-001 synthetic-only custody validator. No release authorization. Issue #356."""
import hashlib,re,json
SHA=re.compile(r'^[0-9a-f]{64}$')

def validate(unit,refs,source_bytes,expected_source_sha,rights='HOLD',editorial='HOLD',approval_basis=''):
    errors=[]
    if not SHA.fullmatch(expected_source_sha):errors.append('BAD_SHA256_FORMAT')
    elif hashlib.sha256(source_bytes).hexdigest()!=expected_source_sha:errors.append('SOURCE_HASH_MISMATCH')
    if not refs and not rights.startswith('HOLD'):errors.append('ZERO_REFS_WITHOUT_HOLD')
    seen=set()
    for ref in refs:
        key=(unit,ref['occurrence_id'])
        if key in seen:errors.append('DUPLICATE_JOIN')
        seen.add(key)
        a,b=ref['start'],ref['end']
        if not isinstance(a,int) or not isinstance(b,int) or a<0 or b<=a or b>len(source_bytes):errors.append('BAD_RANGE');continue
        quote=source_bytes[a:b]
        if hashlib.sha256(quote).hexdigest()!=ref['quote_sha256']:errors.append('QUOTE_HASH_MISMATCH')
    if editorial.startswith('APPROVED') and approval_basis=='overlap-only':errors.append('OVERLAP_PROMOTION_REJECTED')
    return {'errors':sorted(set(errors)),'release':'HOLD'}

def run():
    source='synthetic TAM fixture – no publication'.encode('utf-8'); digest=hashlib.sha256(source).hexdigest()
    ref={'occurrence_id':'O1','start':0,'end':9,'quote_sha256':hashlib.sha256(source[:9]).hexdigest()}
    tests={
      'positive':validate('SYN',[ref],source,digest)['errors']==[],
      'uppercase_sha': 'BAD_SHA256_FORMAT' in validate('SYN',[ref],source,digest.upper())['errors'],
      'reversed_range':'BAD_RANGE' in validate('SYN',[dict(ref,start=9,end=0)],source,digest)['errors'],
      'zero_hold':validate('SYN',[],source,digest,rights='HOLD')['errors']==[],
      'zero_approved':'ZERO_REFS_WITHOUT_HOLD' in validate('SYN',[],source,digest,rights='APPROVED')['errors'],
      'duplicate':'DUPLICATE_JOIN' in validate('SYN',[ref,ref],source,digest)['errors'],
      'overlap':'OVERLAP_PROMOTION_REJECTED' in validate('SYN',[ref],source,digest,editorial='APPROVED',approval_basis='overlap-only')['errors'],
      'source_mutation':'SOURCE_HASH_MISMATCH' in validate('SYN',[ref],source+b'x',digest)['errors']
    }
    return {'checks':tests,'passed':sum(tests.values()),'total':len(tests),'failed':[k for k,v in tests.items() if not v]}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
