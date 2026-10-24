"""Claude 06Z probes (V1-V5) of GPT run 315 verified-copy helper (blob 1e8484e).
Pre-registered on Issue #13 comment 6380654869 before execution. Synthetic bytes only.
Usage: python3 -I -B CLAUDE-verified-stage-copy-v1-probes.py <path-to-helper.py>
"""
import hashlib, importlib.util, json, os, stat, sys, tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('vc', sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sha = lambda b: hashlib.sha256(b).hexdigest()
res = {}

def outcome(fn):
    try:
        return 'OK:' + json.dumps(fn())
    except BaseException as e:
        return 'REJECTED:%s:%s' % (type(e).__name__, e)

with tempfile.TemporaryDirectory(prefix='claude-06z-') as td:
    r = Path(td); data = b'synthetic placeholder bytes, not a book ' * 50
    src = r / 'snap'; src.write_bytes(data)
    # control
    res['control'] = outcome(lambda: m.copy_verified(src, r / 'c0', sha(data), len(data)))
    # V1 same-size substitution
    forged = bytes(reversed(data)); assert len(forged) == len(data) and forged != data
    src.write_bytes(forged)
    res['V1_same_size_substitution'] = outcome(lambda: m.copy_verified(src, r / 'v1', sha(data), len(data)))
    res['V1_dest_left_behind'] = (r / 'v1').exists()
    src.write_bytes(data)
    # V2 pre-existing destination
    pre = r / 'v2'; pre.write_bytes(b'someone else\'s file')
    res['V2_preexisting_dest'] = outcome(lambda: m.copy_verified(src, pre, sha(data), len(data)))
    res['V2_preexisting_file_still_exists'] = pre.exists()
    # V3 same-size rewrite of staged file, mtime restored
    st = r / 'v3'; m.copy_verified(src, st, sha(data), len(data))
    s0 = os.stat(st); os.chmod(st, 0o600); st.write_bytes(forged)
    os.utime(st, ns=(s0.st_atime_ns, s0.st_mtime_ns))
    res['V3_mtime_restored'] = os.stat(st).st_mtime_ns == s0.st_mtime_ns
    res['V3_same_size_rewrite'] = outcome(lambda: m.verify_staged({st: {'sha256': sha(data), 'size': len(data)}}))
    # V4 symlink swap just before chmod
    outside = r / 'outside'; outside.write_bytes(b'outside file'); os.chmod(outside, 0o644)
    dest4 = r / 'v4'; real_chmod = os.chmod
    def swap_chmod(p, mode, *a, **k):
        if Path(p) == dest4 and not dest4.is_symlink():
            dest4.unlink(); dest4.symlink_to(outside)
        return real_chmod(p, mode, *a, **k)
    os.chmod = swap_chmod
    try:
        res['V4_symlink_swap_before_chmod'] = outcome(lambda: m.copy_verified(src, dest4, sha(data), len(data)))
    finally:
        os.chmod = real_chmod
    res['V4_outside_mode_after'] = oct(stat.S_IMODE(os.stat(outside).st_mode))
    res['V4_dest_exists_after'] = os.path.lexists(dest4)
    # V5 uppercase pin
    res['V5_uppercase_pin'] = outcome(lambda: m.copy_verified(src, r / 'v5', sha(data).upper(), len(data)))

print(json.dumps({'python': sys.version.split()[0], 'helper_sha256': sha(Path(sys.argv[1]).read_bytes()), 'results': res}, indent=1))
