#!/usr/bin/env python3
"""NVE-D-029: finite source-identity and frozen-root comparator controls.
No signatures or independent custody are tested by this small reproducer.
"""
import hashlib
import json

def digest(record):
    payload=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(payload).hexdigest()

source={'path':'pwa/python/algorithm_matrix.py',
        'commit':'bd6d48b894d5f433951c3eb5d0e14fab4010c24f',
        'source_blob':'f7cf46584a7c787367196ec0d1aae7178dd976e3'}
frozen=digest(source)
cases={'pristine':dict(source),
       'relocated_same_blob':dict(source,path='different/algorithm_matrix.py'),
       'changed_blob':dict(source,source_blob='0'*40)}
for name,candidate in cases.items():
    digest_only='=' if candidate['source_blob']==source['source_blob'] else '0'
    tuple_equal='=' if candidate==source else '0'
    frozen_equal='=' if digest(candidate)==frozen else '0'
    print(json.dumps({'case':name,'digest_only':digest_only,
                      'source_tuple':tuple_equal,'frozen_root':frozen_equal}))
assert cases['relocated_same_blob']['source_blob']==source['source_blob']
assert digest(cases['relocated_same_blob'])!=frozen
