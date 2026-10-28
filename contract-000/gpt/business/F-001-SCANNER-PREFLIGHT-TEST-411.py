import importlib.util, tempfile, pathlib, json, subprocess, sys
p=pathlib.Path(__file__).with_name('F-001-SCANNER-PREFLIGHT-411.py')
spec=importlib.util.spec_from_file_location('f001',p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
passes=0

def check(name, fn):
    global passes
    fn()
    passes += 1
    print('PASS', name)

def raises(fn):
    try: fn()
    except (OSError, ValueError): return
    raise AssertionError('expected fail')

def assert_good(r):
    assert r['source_file_count']==8 and r['scanner_execution']=='NOT RUN'

def assert_hash(h):
    assert h=='b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0'

with tempfile.TemporaryDirectory() as d:
    root=pathlib.Path(d); src=root/'src'; src.mkdir(); scanner=root/'scan.py'
    scanner.write_text('original scanner stand-in for synthetic tests')
    pins={k:m.git_blob(k.encode()) for k in m.PINS}
    for k in pins: (src/k).write_bytes(k.encode())
    scanner_pin=m.git_blob(scanner.read_bytes())
    check('valid eight-source synthetic pins',lambda: assert_good(m.audit_sources(src,scanner,pins,scanner_pin)))
    (src/'Article 10').unlink()
    check('missing source fails',lambda: raises(lambda:m.audit_sources(src,scanner,pins,scanner_pin)))
    (src/'Article 10').write_bytes(b'Article 10')
    (src/'Article 5').write_bytes(b'Article 5x')
    check('one-byte tamper fails',lambda: raises(lambda:m.audit_sources(src,scanner,pins,scanner_pin)))
    (src/'Article 5').write_bytes(b'Article 5')
    scanner.write_text('changed')
    check('scanner tamper fails',lambda: raises(lambda:m.audit_sources(src,scanner,pins,scanner_pin)))
    scanner.write_text('original scanner stand-in for synthetic tests')
    (src/'Article 6').unlink(); (src/'Article 6').symlink_to('Article 5')
    check('symlink source fails',lambda: raises(lambda:m.audit_sources(src,scanner,pins,scanner_pin)))
    (src/'Article 6').unlink(); (src/'Article 6').write_bytes(b'Article 6')
    (src/'Article 2 Water Weight Computes').unlink(); (src/'Article 2 Water Weight Computes').mkdir()
    check('directory instead of source fails',lambda: raises(lambda:m.audit_sources(src,scanner,pins,scanner_pin)))
    (src/'Article 2 Water Weight Computes').rmdir(); (src/'Article 2 Water Weight Computes').write_bytes(b'Article 2 Water Weight Computes')
    (src/'README.md').write_bytes(b'x'*(m.MAX_FILE_BYTES+1))
    check('oversize source fails',lambda: raises(lambda:m.audit_sources(src,scanner,pins,scanner_pin)))
    (src/'README.md').write_bytes(b'README.md')
    def check_cli():
        r=subprocess.run([sys.executable,'-I','-B',str(p),str(src),str(scanner)],capture_output=True,text=True)
        assert r.returncode==1 and json.loads(r.stdout)['audit']=='FAIL', (r.returncode,r.stdout,r.stderr)
    check('CLI fails with synthetic unpinned sources',check_cli)
    check('blob hashing uses Git frame',lambda: assert_hash(m.git_blob(b'hello')))
print(f'{passes}/{passes} controls passed')
