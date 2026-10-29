"""Synthetic-only controls; does not claim an original TAM source replay."""
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from collections import Counter
import f001_claim_output_gate_437 as gate

class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"; self.source.mkdir()
        self.out = self.root / "out"; self.out.mkdir()
        self.receipt = self.out / "receipt.json"
        self.report = self.out / "claims-report.json"
        self.csv = self.out / "claims.csv"
        src = {}; files = []; per = {}; triggers = Counter(); rows = []
        for j, name in enumerate(gate.FILES):
            text = ("The precision is exactly 95%. This is proposed.\n\n"
                    "Another sentence always confirms a result." if j % 2 else
                    "The only proof is here.\n\nWe measure 95% accuracy.")
            raw = text.encode(); (self.source / name).write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            files.append({"name":name,"bytes":len(raw),"sha256":digest,"git_blob_sha1":"0"*40})
            src[name] = digest; per[name] = 0
            for i, s in enumerate(gate.sentences(text),1):
                hits=[k for k,rx in gate.TRIGGERS.items() if gate.re.search(rx,s,gate.re.I)]
                if hits:
                    per[name]+=1;triggers.update(hits)
                    rows.append({"file":name,"sentence_no":str(i),"triggers":";".join(hits),"sentence":s,"status":""})
        self.receipt.write_text(json.dumps({"schema":"f001-verified-git-pins/v1","status":"HOLD_SOURCE_PIN_MATCH_NOT_EDITORIAL_APPROVAL","source_count":8,"repository":"AGI144348Outlook/The-TAM-protocol","source_ref":"1"*40,"files":files}))
        self.report.write_text(json.dumps({"source_files":src,"per_file":per,"per_trigger":dict(triggers),"rows":len(rows)}))
        with self.csv.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=gate.HEADER);w.writeheader();w.writerows(rows)
    def mutate(self, name, fn):
        p=getattr(self,name);p.write_text(fn(p.read_text()))
    def fails(self):
        with self.assertRaises((gate.GateError, OSError, ValueError)):
            gate.verify(self.source,self.receipt,self.csv,self.report)
    def test_01_positive(self):
        self.assertEqual(gate.verify(self.source,self.receipt,self.csv,self.report)["source_count"],8)
    def test_02_missing(self):
        (self.source / gate.FILES[0]).unlink();self.fails()
    def test_03_tampered_source(self):
        with (self.source/gate.FILES[0]).open("ab") as f:f.write(b"changed")
        self.fails()
    def test_04_source_symlink(self):
        p=self.source/gate.FILES[0];p.unlink();p.symlink_to(self.source/gate.FILES[1]);self.fails()
    def test_05_csv_truncated(self):
        lines=self.csv.read_text().splitlines();self.csv.write_text("\n".join(lines[:-1])+"\n");self.fails()
    def test_06_csv_status_promoted(self):
        self.mutate("csv",lambda s:s.replace(",\n",",approved\n",1));self.fails()
    def test_07_report_count(self):
        self.mutate("report",lambda s:s.replace('"rows": 16','"rows": 15'));self.fails()
    def test_08_report_missing_source(self):
        data=json.loads(self.report.read_text());del data['source_files'][gate.FILES[0]];self.report.write_text(json.dumps(data));self.fails()
    def test_09_receipt_invalid(self):
        self.mutate("receipt",lambda s:s.replace('"source_count": 8','"source_count": 7'));self.fails()
    def test_10_duplicate_json_key(self):
        self.mutate("receipt",lambda s:s.replace('"source_count": 8','"source_count": 8, "source_count": 8'));self.fails()
    def test_11_csv_symlink(self):
        self.csv.unlink();self.csv.symlink_to(self.report);self.fails()
    def test_12_wrong_repo(self):
        self.mutate("receipt",lambda s:s.replace('AGI144348Outlook/The-TAM-protocol','other/repo'));self.fails()

if __name__=='__main__':unittest.main(verbosity=2)
