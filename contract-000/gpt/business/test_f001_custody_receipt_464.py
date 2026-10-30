"""Synthetic tests for F-001 executable-pin wrapper; NOT real-source replay."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from f001_custody_receipt_464 import attest, git_blob, GATE_BLOB, main

# Synthetic executable emits a HOLD receipt derived from the passed files.
# Its pin is injected ONLY into the test function, never the production CLI.
GATE = '''import hashlib, json, sys
from pathlib import Path
def blob(x):
 d=Path(x).read_bytes(); return hashlib.sha1(b"blob "+str(len(d)).encode()+b"\\0"+d).hexdigest()
r,m,i=sys.argv[1:]
print(json.dumps({"project":"F-001","status":"HOLD / NOT LAUNCH-READY", "register_git_blob":blob(r),"location_map_git_blob":blob(m),"intake_git_blob":blob(i),"occurrences":82,"copy_links":10,"pending":82,"approved":0,"approval_authenticated":False,"editorial_overlay_applied":False,"publication_authorized":False},sort_keys=True))
'''

class TestReceipt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.paths = [self.root / n for n in ('gate.py','register.tsv','location.tsv','intake.tsv')]
        for p,d in zip(self.paths, (GATE.encode(),b'register\n',b'location\n',b'intake\n')):
            p.write_bytes(d)
        self.pins = [git_blob(p.read_bytes()) for p in self.paths]

    def good(self, **overrides):
        kw=dict(zip(('expected_gate_blob','expected_register_blob','expected_location_blob','expected_intake_blob'),self.pins))
        kw.update(overrides)
        return attest(*self.paths, **kw)

    def test_positive_hold(self):
        r=self.good(); self.assertEqual((r['pending'],r['approved'],r['publication_authorized']),(82,0,False))
    def test_version_and_gate(self):
        r=self.good(); self.assertEqual(r['gate_script_git_blob'],self.pins[0]); self.assertEqual(len(r['gate_script_sha256']),64)
    def test_deterministic(self):
        self.assertEqual(json.dumps(self.good(),sort_keys=True),json.dumps(self.good(),sort_keys=True))
    def test_production_pin_not_synthetic(self):
        self.assertNotEqual(GATE_BLOB,self.pins[0]);
        with self.assertRaisesRegex(ValueError,'gate:'):
            attest(*self.paths,expected_register_blob=self.pins[1],expected_location_blob=self.pins[2],expected_intake_blob=self.pins[3])
    def test_changed_gate(self):
        self.paths[0].write_bytes(self.paths[0].read_bytes()+b'\n# changed')
        with self.assertRaisesRegex(ValueError,'gate:'): self.good()
    def test_changed_register(self):
        self.paths[1].write_bytes(b'altered')
        with self.assertRaisesRegex(ValueError,'register:'): self.good()
    def test_changed_location(self):
        self.paths[2].write_bytes(b'altered')
        with self.assertRaisesRegex(ValueError,'location:'): self.good()
    def test_changed_intake(self):
        self.paths[3].write_bytes(b'altered')
        with self.assertRaisesRegex(ValueError,'intake:'): self.good()
    def test_missing_file(self):
        self.paths[3].unlink()
        with self.assertRaises(FileNotFoundError): self.good()
    def test_gate_reject(self):
        self.paths[0].write_text('import sys\nsys.exit(2)\n')
        with self.assertRaisesRegex(ValueError,'refused'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_gate_wrong_receipt(self):
        self.paths[0].write_text('print("{}")\n')
        with self.assertRaisesRegex(ValueError,'schema'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_gate_forged_approval(self):
        bad=GATE.replace('"approved":0','"approved":1')
        self.paths[0].write_text(bad)
        with self.assertRaisesRegex(ValueError,'schema'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_gate_forged_release(self):
        bad=GATE.replace('"publication_authorized":False','"publication_authorized":True')
        self.paths[0].write_text(bad)
        with self.assertRaisesRegex(ValueError,'schema'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_gate_invalid_json(self):
        self.paths[0].write_text('print("not json")\n')
        with self.assertRaisesRegex(ValueError,'JSON'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_gate_duplicate_json_keys(self):
        self.paths[0].write_text('print(\'{"project":"F-001","project":"F-001"}\')\n')
        with self.assertRaisesRegex(ValueError,'JSON'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_gate_nonobject_json(self):
        self.paths[0].write_text('print("[]")\n')
        with self.assertRaisesRegex(ValueError,'non-object'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_gate_stderr(self):
        self.paths[0].write_text('import sys\nprint("x",file=sys.stderr)\nprint("{}")\n')
        with self.assertRaisesRegex(ValueError,'execution error'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))
    def test_gate_no_stdout(self):
        self.paths[0].write_text('pass\n')
        with self.assertRaisesRegex(ValueError,'execution error'): self.good(expected_gate_blob=git_blob(self.paths[0].read_bytes()))

if __name__=='__main__': unittest.main()
