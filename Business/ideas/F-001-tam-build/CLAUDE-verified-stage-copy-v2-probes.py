"""Claude 07Z probes (W1-W6) of GPT run 316 verified-copy helper v2 (blob 21407ac).
Pre-registered on Issue #13 comment 6381209283 before execution. Synthetic bytes only.
Usage: python3 -I -B CLAUDE-verified-stage-copy-v2-probes.py <path-to-helper.py>
"""
import hashlib, importlib.util, json, os, stat, sys, tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('vc2', sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sha = lambda b: hashlib.sha256(b).hexdigest()
res = {}

def outcome(fn):
    try:
        return 'OK:' + json.dumps(fn())
    except BaseException as e:
        return 'REJECTED:%s:%s' % (type(e).__name__, e)

with tempfile.TemporaryDirectory(prefix='claude-07z-') as td:
    r = Path(td); os.chmod(r, 0o700)
    data = b'synthetic placeholder bytes, not a book ' * 50
    src = r / 'snap'; src.write_bytes(data)
    res['control'] = outcome(lambda: m.copy_verified(src, r / 'c0', sha(data), len(data)))
    # W1 pre-existing destination
    pre = r / 'w1'; pre.write_bytes(b"someone else's file")
    res['W1_preexisting_dest'] = outcome(lambda: m.copy_verified(src, pre, sha(data), len(data)))
    res['W1_preexisting_preserved'] = pre.exists() and pre.read_bytes() == b"someone else's file"
    # W2 symlink swap just before fchmod
    outside = r / 'outside'; outside.write_bytes(b'outside file'); os.chmod(outside, 0o644)
    dest2 = r / 'w2'; real_fchmod = os.fchmod
    def swap_fchmod(fd, mode):
        if not dest2.is_symlink():
            dest2.unlink(); dest2.symlink_to(outside)
        return real_fchmod(fd, mode)
    os.fchmod = swap_fchmod
    try:
        res['W2_symlink_swap_before_fchmod'] = outcome(lambda: m.copy_verified(src, dest2, sha(data), len(data)))
    finally:
        os.fchmod = real_fchmod
    res['W2_outside_mode_after'] = oct(stat.S_IMODE(os.stat(outside).st_mode))
    res['W2_symlink_left_in_place'] = dest2.is_symlink()
    # W3 private parent reached through a symlinked ancestor
    real_anc = r / 'real_anc'; (real_anc / 'priv').mkdir(parents=True); os.chmod(real_anc / 'priv', 0o700)
    link_anc = r / 'link_anc'; link_anc.symlink_to(real_anc)
    res['W3_symlinked_ancestor'] = outcome(lambda: m.copy_verified(src, link_anc / 'priv' / 'w3', sha(data), len(data)))
    res['W3_file_landed_in_real_dir'] = (real_anc / 'priv' / 'w3').exists()
    # W4 parent renamed aside and replaced just before the final by-path re-hash
    p4 = r / 'p4'; p4.mkdir(mode=0o700); dest4 = p4 / 'w4'
    real_digest = m.digest_regular
    def swap_parent(path, **k):
        if Path(path) == dest4 and not (r / 'p4_aside').exists():
            os.rename(p4, r / 'p4_aside'); p4.mkdir(mode=0o700); dest4.write_bytes(data)
        return real_digest(path, **k)
    m.digest_regular = swap_parent
    try:
        res['W4_parent_swap_before_rehash'] = outcome(lambda: m.copy_verified(src, dest4, sha(data), len(data)))
    finally:
        m.digest_regular = real_digest
    created = r / 'p4_aside' / 'w4'
    res['W4_created_inode_location'] = 'p4_aside/w4' if created.exists() else 'missing'
    res['W4_returned_path_is_created_inode'] = created.exists() and os.stat(created).st_ino == os.stat(dest4).st_ino
    # W5 KeyboardInterrupt mid-read of the source
    dest5 = r / 'w5'; real_read = os.read; calls = {'n': 0}
    def bad_read(fd, n):
        calls['n'] += 1
        if calls['n'] == 1:
            return real_read(fd, 100)
        raise KeyboardInterrupt('injected')
    os.read = bad_read
    try:
        res['W5_interrupt_mid_copy'] = outcome(lambda: m.copy_verified(src, dest5, sha(data), len(data)))
    finally:
        os.read = real_read
    res['W5_partial_left'] = os.path.lexists(dest5)
    # W6 parent not private
    p6 = r / 'p6'; p6.mkdir(); os.chmod(p6, 0o755)
    res['W6_parent_0755'] = outcome(lambda: m.copy_verified(src, p6 / 'w6', sha(data), len(data)))

print(json.dumps({'python': sys.version.split()[0], 'helper_sha256': sha(Path(sys.argv[1]).read_bytes()), 'results': res}, indent=1))
