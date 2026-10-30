"""Run465 synthetic tests; no real TAM files and no release capability."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from f001_custody_snapshot_465 import attest, git_blob, GATE_BLOB, main

GATE = '''import hashlib, json, sys
from pathlib import Path
def blob(x):
 d=Path(x).read_bytes(); return hashlib.sha1(b"blob "+str(len(d)).encode()+b"\\0"+d).hexdigest()
r,m,i=sys.argv[1:]
print(json.dumps({"project":"F-001","status":"HOLD / NOT LAUNCH-READY", "register_git_blob":blob(r),"location_map_git_blob":blob(m),"intake_git_blob":blob(i),"occurrences":82,"copy_links":10,"pending":82,"approved":0,"approval_authenticated":False,"editorial_overlay_applied":False,"publication_authorized":False},sort_keys=True))
'''

class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.paths = [self.root / n for n in ('gate.py','register.tsv','location.tsv','intake.tsv')]
        for p,d in zip(self.paths,(GATE.encode(),b'register\n',b'location\n',b'intake\n')):
            p.write_bytes(d)
        self.pins = [git_blob(p.read_bytes()) for p in self.paths]

    def good(self, **overrides):
        kw=dict(zip(('expected_gate_blob','expected_register_blob','expected_location_blob','expected_intake_blob'),self.pins))
        kw.update(overrides)
        return attest(*self.paths, **kw)

    def test_positive_hold(self):
        r=self.good()
        self.assertEqual((r['pending'],r['approved'],r['publication_authorized']),(82,0,False))
        self.assertEqual(r['input_snapshot_mode'],'private-verified-byte-snapshots')
        self.assertNotIn('execution_verified_locally',r)
    def test_determinism(self):
        self.assertEqual(json.dumps(self.good(),sort_keys=True),json.dumps(self.good(),sort_keys=True))
    def test_gate_pin_and_sha(self):
        r=self.good(); self.assertEqual(r['gate_script_git_blob'],self.pins[0]); self.assertEqual(len(r['gate_script_sha256']),64)
    def test_production_gate_not_synthetic(self):
        self.assertNotEqual(GATE_BLOB,self.pins[0])
        with self.assertRaisesRegex(ValueError,'gate:'):
            attest(*self.paths,expected_register_blob=self.pins[1],expected_location_blob=self.pins[2],expected_intake_blob=self.pins[3])
    def test_changed_gate_refused(self):
        self.paths[0].write_bytes(self.paths[0].read_bytes()+b'# edit\n')
        with self.assertRaisesRegex(ValueError,'gate:'): self.good()
    def test_changed_register_refused(self):
        self.paths[1].write_bytes(b'changed\n')
        with self.assertRaisesRegex(ValueError,'register:'): self.good()
    def test_changed_location_refused(self):
        self.paths[2].write_bytes(b'changed\n')
        with self.assertRaisesRegex(ValueError,'location:'): self.good()
    def test_changed_intake_refused(self):
        self.paths[3].write_bytes(b'changed\n')
        with self.assertRaisesRegex(ValueError,'intake:'): self.good()
    def test_missing_input_refused(self):
        self.paths[3].unlink()
        with self.assertRaises(FileNotFoundError): self.good()
    def test_post_read_source_path_swap_does_not_affect_snapshot(self):
        original_run = subprocess.run
        observed=[]
        def mutate_then_run(argv,**kwargs):
            # This is AFTER attest() has verified all four source bytes.
            self.paths[1].write_bytes(b'FORGED REGISTER\n')
            self.paths[2].write_bytes(b'FORGED LOCATION\n')
            self.paths[3].write_bytes(b'FORGED INTAKE\n')
            observed.extend(argv[-3:])
            return original_run(argv,**kwargs)
        with patch('f001_custody_snapshot_465.subprocess.run',side_effect=mutate_then_run):
            r=self.good()
        self.assertEqual(r['pending'],82)
        self.assertTrue(all('f001-verified-snapshot-' in p for p in observed))
        self.assertTrue(all(not Path(p).exists() for p in observed))
        self.assertEqual(self.paths[1].read_bytes(),b'FORGED REGISTER\n')
    def test_gate_rejection(self):
        self.paths[0].write_text('import sys\nsys.exit(2)\n')
        with self.assertRaisesRegex(ValueError,'refused'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_wrong_receipt(self):
        self.paths[0].write_text('print("{}")\n')
        with self.assertRaisesRegex(ValueError,'schema'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_forged_approval(self):
        self.paths[0].write_text(GATE.replace('"approved":0','"approved":1'))
        with self.assertRaisesRegex(ValueError,'schema'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_forged_release(self):
        self.paths[0].write_text(GATE.replace('"publication_authorized":False','"publication_authorized":True'))
        with self.assertRaisesRegex(ValueError,'schema'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_invalid_json(self):
        self.paths[0].write_text('print("not json")\n')
        with self.assertRaisesRegex(ValueError,'JSON'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_duplicate_json_keys(self):
        self.paths[0].write_text('print(\'{"project":"F-001","project":"F-001"}\')\n')
        with self.assertRaisesRegex(ValueError,'JSON'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_nonobject_receipt(self):
        self.paths[0].write_text('print("[]")\n')
        with self.assertRaisesRegex(ValueError,'non-object'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_stderr_refused(self):
        self.paths[0].write_text('import sys\nprint("x",file=sys.stderr)\nprint("{}")\n')
        with self.assertRaisesRegex(ValueError,'execution error'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_no_stdout_refused(self):
        self.paths[0].write_text('pass\n')
        with self.assertRaisesRegex(ValueError,'execution error'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_cleanup_on_gate_failure(self):
        self.paths[0].write_text('import sys\nsys.exit(2)\n')
        captured=[]
        original_run=subprocess.run
        def record(argv,**kwargs):
            captured.extend(argv[-3:]); return original_run(argv,**kwargs)
        with patch('f001_custody_snapshot_465.subprocess.run',side_effect=record):
            with self.assertRaisesRegex(ValueError,'refused'):
                self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
        self.assertTrue(all(not Path(p).exists() for p in captured))

if __name__=='__main__': unittest.main()
