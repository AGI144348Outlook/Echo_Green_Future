#!/usr/bin/env python3
"""Run 381: bounded characterization of Genesis ReshIdentity.anchor's Lobby update.
SOURCE-OBSERVED: genesis-documentary src/echo_governor_skeleton.py blob
63eb982989b4f3478d649430b555c8f4ba755c27, lines 3284-3290.
This script executes only the exact list(set(...)) expression, not Genesis.
"""
import json, os, subprocess, sys

EXTRA = ['governor', 'indexing', 'algorithm', 'identity', 'matrix', 'aleph', 'ayin', 'pe']
BASE = ['resh', 'identity', 'resh', 'memory']
EXPRESSION = '''import json
base = ['resh', 'identity', 'resh', 'memory']
extra = ['governor', 'indexing', 'algorithm', 'identity', 'matrix', 'aleph', 'ayin', 'pe']
result = list(set(base + extra))
print(json.dumps(result))'''

def run(seed):
    env = dict(os.environ, PYTHONHASHSEED=str(seed))
    result = subprocess.run([sys.executable, '-I', '-B', '-c', EXPRESSION],
                            check=True, capture_output=True, text=True, env=env)
    return json.loads(result.stdout)

def main():
    runs = {seed: run(seed) for seed in range(8)}
    expected = set(BASE + EXTRA)
    assert all(set(v) == expected for v in runs.values()), 'word-set mismatch'
    assert all(len(v) == len(expected) for v in runs.values()), 'dedup mismatch'
    assert len(set(tuple(v) for v in runs.values())) > 1, 'hash-seed order did not vary'
    assert len(BASE + EXTRA) > len(expected), 'duplicate did not exist in input'
    assert set(list(set(runs[0] + EXTRA))) == expected
    print(json.dumps({
        'cases': 5, 'passed': 5, 'seed_count': len(runs),
        'distinct_orderings': len(set(tuple(v) for v in runs.values())),
        'input_length': len(BASE + EXTRA), 'output_length': len(expected),
        'all_sets_equal': True, 'examples': {str(k): runs[k] for k in (0,1)}
    }, ensure_ascii=False))

if __name__ == '__main__':
    main()
