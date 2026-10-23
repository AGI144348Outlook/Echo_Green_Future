#!/usr/bin/env python3
"""F-001 §115 probes of GPT's PROPOSED-f001-v5-report-gate-v1.py (blob 7556a83).
Records only; synthetic editorial records; never a release or editorial decision.
Usage: python3 -I -B f001-v5-gate-probes-115.py <dir holding the 4 GPT files>
Pre-registered predictions (written before running):
  U1 pin circularity: after the CSV's numeric cell on a non-flagged line is altered, a caller who
     re-pins Dataset A and regenerates+re-pins the v5 report gets PASS/HOLD (gate attests only
     self-consistency of caller pins)                                   -> PASS/HOLD
  U2 corrected Dataset A (line 6 and 7 made consistent, as an editorial fix might): gate fails
     closed with the hard-coded [6,7] message, conflating "corrected" with "forged" -> FAIL/HOLD
  U3 parent-directory symlink (dir link -> real dir; final components regular files): O_NOFOLLOW
     guards only the last component, so the gate accepts                -> PASS/HOLD
  U4 editorial record replaced by a different valid synthetic record and report regenerated +
     re-pinned: gate has no record pin, so it accepts                  -> PASS/HOLD (RECORDED_UNAUTHENTICATED)
"""
import csv, hashlib, io, json, os, subprocess, sys, tempfile
from pathlib import Path
D = Path(sys.argv[1]).resolve()
GATE, V5, ARCH = D/'PROPOSED-f001-v5-report-gate-v1.py', D/'PROPOSED-f001-disposition-binding-v5.py', D/'dataset-a-archived.csv'
HEADER = ["object","measured_g","units","registry_sign","stated_deviation_pct","term","expected_g","recomputed_deviation_pct","stated_matches_recomputed"]
BOUND = ("object","measured_g","units","stated_deviation_pct","recomputed_deviation_pct")
sha = lambda b: hashlib.sha256(b).hexdigest()
def v5(csvp, rec):
    p = subprocess.run([sys.executable,'-I','-B',str(V5),str(csvp),str(rec),sha(csvp.read_bytes())],capture_output=True,timeout=5)
    return p.stdout
def record(csv_bytes, note):
    data = list(csv.reader(io.StringIO(csv_bytes.decode(), newline='')))
    rows = [{'csv_line':n, **{k:dict(zip(HEADER,r))[k] for k in BOUND}, 'disposition':'RETAIN_STATED_WITH_DISCLOSURE','explanation':note}
            for n,r in enumerate(data[1:],2) if r[-1]=='False']
    return json.dumps({'record_version':2,'dataset_a_sha256':sha(csv_bytes),'decision_reference':'SYNTHETIC-NOT-APPROVED','rows':rows},sort_keys=True).encode()
def gate(csvp, rec, script, rep):
    p = subprocess.run([sys.executable,'-I','-B',str(GATE),'--dataset-a',str(csvp),'--disposition-record',str(rec),'--v5-script',str(script),
        '--report-json',str(rep),'--expected-dataset-sha256',sha(csvp.read_bytes()),'--expected-report-sha256',sha(rep.read_bytes())],capture_output=True,timeout=10)
    r = json.loads(p.stdout)
    return ('PASS' if r['integrity']=='PASS' else 'FAIL')+'/'+r['release'], p.returncode, r['issues'], r['v5_status']
def edit_csv(raw, fn):
    rows = list(csv.reader(io.StringIO(raw.decode(), newline='')))
    fn(rows); out = io.StringIO(); csv.writer(out, lineterminator='\r\n').writerows(rows); return out.getvalue().encode()
res = {}
with tempfile.TemporaryDirectory() as t:
    t = Path(t); script = t/'v5.py'; script.write_bytes(V5.read_bytes())
    # U1
    raw = ARCH.read_bytes(); rows = list(csv.reader(io.StringIO(raw.decode(), newline='')))
    nonflag = next(i for i,r in enumerate(rows[1:],1) if r[-1]!='False')
    def f1(rs): rs[nonflag][5] = rs[nonflag][5] + ' (altered)'
    c = t/'u1.csv'; c.write_bytes(edit_csv(raw, f1)); rec = t/'u1-rec.json'; rep = t/'u1.json'; rep.write_bytes(v5(c, rec))
    res['U1_pin_circularity'] = ('PASS/HOLD', gate(c, rec, script, rep))
    # U2
    def f2(rs):
        for r in rs[1:]:
            if r[-1]=='False': r[4] = r[7]; r[-1] = 'True'
    c = t/'u2.csv'; c.write_bytes(edit_csv(raw, f2)); rec = t/'u2-rec.json'; rep = t/'u2.json'; rep.write_bytes(v5(c, rec))
    res['U2_corrected_dataset'] = ('FAIL/HOLD', gate(c, rec, script, rep))
    # U3
    real = t/'real'; real.mkdir(); (real/'a.csv').write_bytes(raw); link = t/'link'; os.symlink(real, link)
    rec = link/'rec.json'; rep = link/'rep.json'; rep.write_bytes(v5(link/'a.csv', rec))
    res['U3_parent_symlink'] = ('PASS/HOLD', gate(link/'a.csv', rec, script, rep))
    # U4
    c = t/'u4.csv'; c.write_bytes(raw); rec = t/'u4-rec.json'
    rec.write_bytes(record(raw, 'SYNTHETIC A')); rep = t/'u4.json'; rep.write_bytes(v5(c, rec)); a = gate(c, rec, script, rep)
    rec.write_bytes(record(raw, 'SYNTHETIC B, different explanation')); rep.write_bytes(v5(c, rec)); b = gate(c, rec, script, rep)
    res['U4_unpinned_record'] = ('PASS/HOLD', b, 'first record:', a)
out = {k: {'predicted': v[0], 'observed': v[1][0], 'exit': v[1][1], 'issues': v[1][2], 'v5_status': v[1][3], 'as_predicted': v[0]==v[1][0]} for k,v in res.items()}
print(json.dumps(out, indent=1)); print('as predicted:', sum(o['as_predicted'] for o in out.values()), '/', len(out))
