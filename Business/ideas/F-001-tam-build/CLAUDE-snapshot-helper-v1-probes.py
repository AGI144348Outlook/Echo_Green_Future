"""Claude 04Z F-001 probes Y1-Y5 of ChatGPT's PROPOSED pinned-input snapshot helper (blob 4fac471), synthetic files only.
Pre-registered on Issue #13 (6379599029) before execution. Records only; not a frozen test; nothing applied to GPT's file.
Usage: python3 -I -B <probe> <dir containing the helper saved as snap.py>"""
import sys, os, hashlib, tempfile, importlib.util
spec = importlib.util.spec_from_file_location('snap', os.path.join(sys.argv[1], 'snap.py'))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)
H = lambda b: hashlib.sha256(b).hexdigest()
def case(name, fn):
    try: print(name, 'OBSERVED:', fn())
    except Exception as e: print(name, 'OBSERVED: raised', type(e).__name__, e)
base = tempfile.mkdtemp(prefix='y-')
root = os.path.join(base, 'root'); os.mkdir(root)
outside = os.path.join(base, 'outside.txt'); open(outside, 'wb').write(b'outside bytes\n')
def y1():
    os.link(outside, os.path.join(root, 'hl.txt'))
    with snap.pinned_snapshots(root, {'a': ('hl.txt', H(b'outside bytes\n'))}) as r:
        return f"accepted={open(r['a'].path,'rb').read()!r} nlink={os.stat(os.path.join(root,'hl.txt')).st_nlink}"
def y2():
    open(os.path.join(root, 'f.txt'), 'wb').write(b'pinned\n')
    with snap.pinned_snapshots(root, {'a': ('f.txt', H(b'pinned\n'))}) as r:
        p = r['a'].path; mode0 = oct(os.stat(p).st_mode & 0o777)
        os.chmod(p, 0o600); open(p, 'wb').write(b'tampered\n')
        return f"mode_before={mode0} rewrite=ok record_sha={r['a'].sha256[:12]} path_sha={H(open(p,'rb').read())[:12]} equal={r['a'].sha256==H(open(p,'rb').read())}"
def y3():
    real = os.path.join(base, 'realparent'); os.mkdir(real); os.mkdir(os.path.join(real, 'r'))
    open(os.path.join(real, 'r', 'g.txt'), 'wb').write(b'g\n')
    os.symlink(real, os.path.join(base, 'lnparent'))
    out = []
    with snap.pinned_snapshots(os.path.join(base, 'lnparent', 'r'), {'a': ('g.txt', H(b'g\n'))}) as r:
        out.append('ancestor-symlink root accepted')
    os.symlink(os.path.join(real, 'r'), os.path.join(base, 'lnroot'))
    try:
        with snap.pinned_snapshots(os.path.join(base, 'lnroot'), {'a': ('g.txt', H(b'g\n'))}): out.append('root-symlink accepted')
    except OSError as e: out.append(f'root-symlink {type(e).__name__} errno={e.errno}')
    return '; '.join(out)
def y4():
    data = b'A' * (snap.CHUNK * 3); p = os.path.join(root, 'big.bin'); open(p, 'wb').write(data)
    real_read = snap.os.read; calls = {'n': 0}
    class OsProxy:
        def __getattr__(s, k): return getattr(os, k)
        def read(s, fd, n):
            calls['n'] += 1; b = real_read(fd, n)
            if calls['n'] == 1:
                with open(p, 'r+b') as w: w.seek(snap.CHUNK * 2); w.write(b'B' * snap.CHUNK); w.flush(); os.fsync(w.fileno())
            return b
    snap.os = OsProxy()
    try:
        with snap.pinned_snapshots(root, {'a': ('big.bin', H(data))}): return 'accepted (NOT expected)'
    finally:
        snap.os = os
def y5():
    open(os.path.join(root, 'e.txt'), 'wb').write(b'e\n'); held = {}
    try:
        with snap.pinned_snapshots(root, {'a': ('e.txt', H(b'e\n'))}) as r:
            held['dir'] = os.path.dirname(r['a'].path); raise RuntimeError('caller body error')
    except RuntimeError: pass
    return f"staging_exists_after={os.path.exists(held['dir'])}"
for n, f in [('Y1', y1), ('Y2', y2), ('Y3', y3), ('Y4', y4), ('Y5', y5)]: case(n, f)
