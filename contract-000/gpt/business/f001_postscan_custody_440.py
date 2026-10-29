#!/usr/bin/env python3
"""Draft-only F-001 post-scan source custody wrapper; NOT adopted by shared build.
Requires the exact sibling f001_raw_replay_gate_439.py. No network or publication.
"""
import hashlib
import json
import sys
from pathlib import Path
import importlib.util

_gate_path = Path(__file__).with_name("f001_raw_replay_gate_439.py")
_spec = importlib.util.spec_from_file_location("f001_original_gate", _gate_path)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


def main(src, scanner, manifest, out):
    result = base.main(src, scanner, manifest, out)
    src = base.path_no_symlinks(src)
    # Re-read all eight sources after the scanner's process has terminated.
    # This detects a scanner that rewrites a source AFTER reading it and
    # BEFORE the original gate returns success. Not a filesystem lock.
    after = {}
    for name in base.FILES:
        path = src / name
        base.require(not path.is_symlink() and path.is_file(), 'post-scan missing/symlink: ' + name)
        after[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    base.require(after == result['source_sha256'], 'post-scan source drift')
    result['post_scan_source_sha256'] = after
    result['post_scan_source_custody'] = 'MATCHED_AT_POST_SCAN_REHASH'
    return result


if __name__ == '__main__':
    try:
        if len(sys.argv) != 5:
            raise ValueError('Usage: postscan SRC SCANNER MANIFEST OUT')
        print(json.dumps(main(*sys.argv[1:]), indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('HOLD: ' + str(exc), file=sys.stderr)
        sys.exit(2)
