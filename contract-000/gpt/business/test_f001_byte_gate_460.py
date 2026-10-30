#!/usr/bin/env python3
"""Run460 synthetic-only tests. No source manuscript or real approval used."""
import hashlib
import importlib.util
import io
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent
FILE = HERE / 'F-001-EDITORIAL-BYTE-GATE-460.py'
spec = importlib.util.spec_from_file_location('f001_byte_gate_460', FILE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def fixture():
    lines = ['\t'.join(gate.COLUMNS)]
    for i in range(1, 83):
        d = dict(zip(gate.COLUMNS, [gate.PROJECT, 'Synthetic#S'+str(i), '§156',
               'quote '+str(i), 'proposal '+str(i),
               ('Synthetic#S'+str(i-10)) if 73 <= i <= 82 else '',
               'PROPOSED_NOT_APPROVED', gate.STATUS, gate.SOURCE_COMMIT,
               gate.MANUSCRIPT_BLOB]))
        lines.append('\t'.join(d[k] for k in gate.COLUMNS))
    return ('\n'.join(lines)+'\n').encode('utf-8')


def rep(raw, needle, replacement):
    assert needle in raw
    return raw.replace(needle, replacement, 1)

class ByteGateTests(unittest.TestCase):
    def setUp(self):
        self.good = fixture()
        self.pin = gate.git_blob(self.good)
        self.copies = {'Synthetic#S'+str(i): 'Synthetic#S'+str(i-10) for i in range(73,83)}

    def accept(self, raw):
        return gate.audit_bytes(raw, expected_blob=gate.git_blob(raw), expected_copies=self.copies)

    def reject_with_old_pin(self, raw):
        with self.assertRaises(gate.Refused):
            gate.audit_bytes(raw, expected_blob=self.pin, expected_copies=self.copies)

    def reject_with_new_pin(self, raw):
        with self.assertRaises(gate.Refused):
            self.accept(raw)

    def test_valid_synthetic(self):
        x = gate.audit_bytes(self.good, expected_blob=self.pin, expected_copies=self.copies)
        self.assertEqual((x['rows'], x['copies'], x['approved']), (82,10,0))
        self.assertFalse(x['publication_authorized'])
        self.assertEqual(x['sha256'], hashlib.sha256(self.good).hexdigest())

    def test_production_pin_rejects_synthetic(self):
        with self.assertRaises(gate.Refused): gate.audit_bytes(self.good)

    def test_proposal_mutation(self): self.reject_with_old_pin(rep(self.good,b'proposal 3',b'proposal X'))
    def test_quote_mutation(self): self.reject_with_old_pin(rep(self.good,b'quote 4',b'quote X'))
    def test_reorder(self):
        s=self.good.splitlines(keepends=True);s[1],s[2]=s[2],s[1];self.reject_with_old_pin(b''.join(s))
    def test_append(self): self.reject_with_old_pin(self.good+b'bad\n')
    def test_truncate(self): self.reject_with_old_pin(self.good[:-9])
    def test_approval_forgery(self): self.reject_with_old_pin(rep(self.good,b'PROPOSED_NOT_APPROVED',b'APPROVED_BY_TIMOTHY'))
    def test_release_forgery(self): self.reject_with_old_pin(rep(self.good,b'HOLD / NOT LAUNCH-READY',b'LAUNCH-READY'))
    def test_wrong_source(self): self.reject_with_old_pin(rep(self.good,gate.SOURCE_COMMIT.encode(),b'0'*40))
    def test_wrong_manuscript(self): self.reject_with_old_pin(rep(self.good,gate.MANUSCRIPT_BLOB.encode(),b'0'*40))
    def test_changed_copy(self): self.reject_with_old_pin(rep(self.good,b'Synthetic#S63\tPROPOSED',b'Synthetic#S62\tPROPOSED'))
    def test_missing_quote(self): self.reject_with_old_pin(rep(self.good,b'quote 1',b''))
    def test_duplicate_id(self): self.reject_with_old_pin(rep(self.good,'Synthetic#S2\t§'.encode(),'Synthetic#S1\t§'.encode()))
    def test_invalid_utf8(self): self.reject_with_old_pin(self.good+b'\xff')
    def test_wrong_pin(self):
        with self.assertRaises(gate.Refused): gate.audit_bytes(self.good, expected_blob='0'*40)
    def test_bad_header_even_if_rehashed(self): self.reject_with_new_pin(rep(self.good,b'project\t',b'projectX\t'))
    def test_bad_copy_even_if_rehashed(self): self.reject_with_new_pin(rep(self.good,b'Synthetic#S63\tPROPOSED',b'Synthetic#S82\tPROPOSED'))
    def test_duplicate_id_even_if_rehashed(self): self.reject_with_new_pin(rep(self.good,'Synthetic#S2\t§'.encode(),'Synthetic#S1\t§'.encode()))
    def test_noncanonical_crlf_even_if_rehashed(self): self.reject_with_new_pin(self.good.replace(b'\n',b'\r\n'))
    def test_missing_final_newline_even_if_rehashed(self): self.reject_with_new_pin(self.good[:-1])
    def test_cli_refuses_synthetic(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'synthetic.tsv';p.write_bytes(self.good)
            r=subprocess.run([sys.executable,'-I',str(FILE),str(p)],capture_output=True,text=True)
            self.assertEqual(r.returncode,2)
            self.assertIn('REGISTER REFUSED',r.stderr)

if __name__ == '__main__': unittest.main(verbosity=2)
