"""Synthetic characterization for F-001 pinned snapshots. Issue #32 pre-registered."""
import hashlib
import importlib.util
import os
from pathlib import Path
import stat
import tempfile

spec = importlib.util.spec_from_file_location('snapshot', Path(__file__).with_name('PROPOSED-f001-pinned-input-snapshot-v1.py'))
mod = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

outcomes = []
def check(name, func, expect_failure=False):
    try:
        result = func()
        ok = not expect_failure and bool(result)
        info = str(result)
    except (OSError, ValueError) as exc:
        ok = expect_failure
        info = f'{type(exc).__name__}: {exc}'
    outcomes.append((name, ok, info[:160]))
    print(('PASS' if ok else 'FAIL') + ' ' + name + ' -> ' + info[:160])

def attempt(root, items, **kwargs):
    with mod.pinned_snapshots(root, items, **kwargs):
        return True

with tempfile.TemporaryDirectory() as td:
    root = Path(td)/'root'; root.mkdir()
    outside = Path(td)/'outside'; outside.mkdir()
    original = b'original source bytes\n'
    digest = hashlib.sha256(original).hexdigest()
    (root/'a.txt').write_bytes(original)
    (outside/'evil.txt').write_bytes(b'forged')
    def control():
        with mod.pinned_snapshots(root, {'source':('a.txt', digest)}) as r:
            x=r['source']; return Path(x.path).read_bytes()==original and x.sha256==digest and x.size==len(original)
    check('S0_valid_digest_pinned', control)
    (root/'link.txt').symlink_to(outside/'evil.txt')
    check('S1_final_symlink', lambda: attempt(root, {'x':('link.txt',digest)}), True)
    (root/'linkdir').symlink_to(outside, target_is_directory=True)
    check('S2_ancestor_symlink', lambda: attempt(root, {'x':('linkdir/evil.txt',digest)}), True)
    check('S3_parent_traversal', lambda: attempt(root, {'x':('sub/../a.txt',digest)}), True)
    check('S4_wrong_digest', lambda: attempt(root, {'x':('a.txt','0'*64)}), True)
    check('S5_oversized', lambda: attempt(root, {'x':('a.txt',digest)},max_bytes=5), True)
    os.mkfifo(root/'fifo')
    check('S6_fifo_nonregular', lambda: attempt(root, {'x':('fifo',digest)}), True)
    def swap(label, rel, fd):
        (root/'a.txt').rename(root/'saved.txt')
        (root/'a.txt').symlink_to(outside/'evil.txt')
    def swap_case():
        with mod.pinned_snapshots(root, {'x':('a.txt',digest)},_after_open=swap) as r:
            return Path(r['x'].path).read_bytes()==original and (root/'a.txt').is_symlink()
    check('S7_swap_after_fd_open',swap_case)
    (root/'a.txt').unlink(); (root/'saved.txt').rename(root/'a.txt')
    def mutate(label, rel, fd):
        with open(root/'a.txt','wb') as f: f.write(b'mutated after open')
    check('S8_mutation_after_open', lambda: attempt(root, {'x':('a.txt',digest)},_after_open=mutate), True)
    (root/'a.txt').write_bytes(original)
    check('S9_missing_input', lambda: attempt(root, {'x':('missing.txt',digest)}), True)
    check('S10_invalid_label', lambda: attempt(root, {'../x':('a.txt',digest)}), True)
    def modes():
        with mod.pinned_snapshots(root, {'x':('a.txt',digest)}) as r:
            x=Path(r['x'].path)
            return stat.S_IMODE(x.stat().st_mode)==0o400 and stat.S_IMODE(x.parent.stat().st_mode)==0o700
    check('S11_private_modes', modes)
    def batch():
        with mod.pinned_snapshots(root, {'one':('a.txt',digest),'two':('a.txt',digest)}) as r:
            return len(r)==2 and all(Path(v.path).read_bytes()==original for v in r.values())
    check('S12_two_item_batch', batch)
print(f'FINAL {sum(o[1] for o in outcomes)}/{len(outcomes)} expected outcomes')
if not all(o[1] for o in outcomes):
    raise SystemExit(1)
