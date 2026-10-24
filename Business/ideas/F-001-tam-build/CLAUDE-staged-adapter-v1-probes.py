"""F-001 §122 probes (Claude 05Z) of GPT staged coordinator adapter v1 (blob 6d8ec22) + snapshot helper (blob 4fac471). Synthetic inputs only.
Pre-registered on Issue #13 (6380141211) before execution. Records only. Usage: python3 -I -B CLAUDE-staged-adapter-v1-probes.py TOOLS_DIR
(TOOLS_DIR holds the adapter as adapter.py and the helper under its own name, both copied from mirror-chatgpt-root 99ba65f.)"""
import hashlib, importlib.util, json, os, pathlib, shutil, sys, tempfile
TOOLS = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('adapter', TOOLS / 'adapter.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sha = lambda b: hashlib.sha256(b).hexdigest()
ART = {'epub': b'EPUB-PLACEHOLDER', 'pdf': b'%PDF-PLACEHOLDER', 'dataset_a_csv': b'a,b\n1,2\n', 'dataset_b_csv': b'c,d\n3,4\n'}

def fixture(base):
    src = base / 'src'; src.mkdir()
    pins = {'schema': 'f001-pins/v1', 'artifacts': {}}; rec = {'schema': 'f001-receipt/v1', 'artifacts': {}, 'environment': {'build_output_realpath': str(src)}}
    for k, b in ART.items():
        (src / k).write_bytes(b)
        pins['artifacts'][k] = {'sha256': sha(b), 'size': len(b)}
        rec['artifacts'][k] = {'path': k, 'sha256': sha(b), 'size': len(b)}
    (src / 'pins.json').write_text(json.dumps(pins)); (src / 'receipt.json').write_text(json.dumps(rec))
    (src / 'binding.json').write_text(json.dumps({'schema': 'binding', 'v5_report_sha256': 'aa'}))
    (src / 'v5-report.json').write_text(json.dumps({'schema': 'v5', 'ok': True}))
    return src

orig_rb = pathlib.Path.read_bytes
def patched(targets):
    def rb(self):
        if self.parent.name.startswith('f001-pinned-') and self.name in targets:
            os.chmod(self, 0o600); self.write_bytes(targets[self.name]); os.chmod(self, 0o400)
        return orig_rb(self)
    return rb

out = {}
def case(name, targets=None, prep=None, root_of=None):
    with tempfile.TemporaryDirectory(prefix='claude-z-') as td:
        base = pathlib.Path(td); src = fixture(base)
        if prep: src = prep(base, src)
        pathlib.Path.read_bytes = patched(targets or {})
        try:
            with m.staged_inputs(src, TOOLS) as (a, prov):
                st = pathlib.Path(a.artifact_root)
                out[name] = {'result': 'YIELDED',
                    'staged_binding': json.loads(orig_rb(st / 'binding.json')),
                    'staged_v5': json.loads(orig_rb(st / 'v5-report.json')),
                    'staged_epub_sha256': sha(orig_rb(st / 'artifacts' / 'epub')),
                    'prov_epub_sha256': prov['artifact_sha256']['epub'], 'pinned_epub_sha256': sha(ART['epub']),
                    'prov_keys': sorted(prov)}
        except Exception as e:
            out[name] = {'result': 'REJECTED', 'error': type(e).__name__ + ': ' + str(e)}
        finally:
            pathlib.Path.read_bytes = orig_rb

case('control')
case('Z1_meta_rewrite', {'meta_binding': json.dumps({'schema': 'binding', 'v5_report_sha256': 'bb'}).encode(), 'meta_v5': json.dumps({'schema': 'v5', 'ok': 'FORGED'}).encode()})
case('Z2_epub_rewrite', {'artifact_epub': b'EPUB-SWAPPED-AFTER-SNAPSHOT'})
def anc(base, src):
    real = base / 'real'; real.mkdir(); shutil.move(str(src), real / 'src'); (base / 'link').symlink_to(real)
    p = base / 'link' / 'src'
    r = json.loads((p / 'receipt.json').read_text()); r['environment']['build_output_realpath'] = str(p); (p / 'receipt.json').write_text(json.dumps(r))
    return p
case('Z3_ancestor_symlink', prep=anc)
def ddir(base, src):
    (src / 'disposition.json').mkdir(); return src
case('Z4_disposition_dir', prep=ddir)
print(json.dumps(out, indent=1, sort_keys=True))
