#!/usr/bin/env python3
"""F-001 Run441 bounded original-Python scanner source-pin and Article10 replay.
Draft-only; tests ONE public source, NOT the full eight-source product parity.
Usage: python -I f001_article10_original_scanner_probe_441.py SCANNER ARTICLE10
Source files are never modified; only scratch output is created and removed.
"""
import csv, hashlib, json, subprocess, sys, tempfile
from pathlib import Path

SCANNER_BLOB = '31f3dcff486c4c8cc96d514eb425da86834d00c3'
ARTICLE10_BLOB = 'e82be564872f636662652d34dcb8d3437559f84f'
SOURCE_COMMIT = 'd46456a18fe412398d0ae37ec5a8c4eebb44e0c9'
EXPECTED = [(3,'certainty;accuracy'),(4,'certainty'),(5,'percent;accuracy'),(8,'superlative')]
FILES = ['README.md','Article 1 Hacksilber','Article 2 Water Weight Computes',
         'The Color Dyed and Dental Records','Article 5','Article 6','Article 10','Collective information']

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def verify_raw(scanner, article):
    assert git_blob(scanner) == SCANNER_BLOB, 'scanner pin mismatch'
    assert git_blob(article) == ARTICLE10_BLOB, 'Article10 pin mismatch'

def main(scanner_path, article_path):
    scanner_path, article_path = Path(scanner_path), Path(article_path)
    original_scanner, original_article = scanner_path.read_bytes(), article_path.read_bytes()
    verify_raw(original_scanner, original_article)
    with tempfile.TemporaryDirectory(prefix='f001-run441-') as d:
        root=Path(d);src=root/'src';out=root/'out';src.mkdir()
        (src/'Article 10').write_bytes(original_article)
        p=subprocess.run([sys.executable,'-I',str(scanner_path.resolve()),str(src),str(out)],
                         capture_output=True,text=True,timeout=20)
        assert p.returncode==0, 'original scanner failed: '+p.stderr[-500:]
        with (out/'claims.csv').open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
        report=json.loads((out/'claims-report.json').read_text(encoding='utf-8'))
        assert [(int(x['sentence_no']),x['triggers']) for x in rows]==EXPECTED, 'Article10 rows differ'
        assert all(x['file']=='Article 10' and x['status']=='' for x in rows)
        assert report['rows']==4 and report['per_file']=={'Article 10':4}
        assert report['source_files']['Article 10']==hashlib.sha256(original_article).hexdigest()
        assert sum(v is None for v in report['source_files'].values())==7, 'not a one-file pilot'
        assert set(report['source_files'])==set(FILES)
        # Negative: one-byte mutation is rejected by pinned-byte verification.
        mutated=original_article.replace(b'99.9%',b'99.8%',1)
        assert mutated!=original_article
        negative_rejected=False
        try:verify_raw(original_scanner,mutated)
        except AssertionError:negative_rejected=True
        assert negative_rejected, 'tamper-negative unexpectedly accepted'
        assert scanner_path.read_bytes()==original_scanner and article_path.read_bytes()==original_article
        return {'project':'F-001','source_commit':SOURCE_COMMIT,'scanner_blob':SCANNER_BLOB,
                'article10_blob':ARTICLE10_BLOB,'original_python_executed':True,
                'verified_source_files':1,'required_source_files':8,
                'article10_rows':len(rows),'article10_candidate_coordinates':EXPECTED,
                'missing_source_files':7,'tamper_negative_rejected':negative_rejected,
                'full_eight_source_parity':'NOT_TESTED','editorial_status':'UNREVIEWED',
                'release':'HOLD / NOT LAUNCH-READY'}

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: probe SCANNER ARTICLE10')
    try: print(json.dumps(main(*sys.argv[1:]),indent=2))
    except (AssertionError,ValueError,OSError,subprocess.TimeoutExpired) as e:
        print('FAIL / HOLD: '+str(e),file=sys.stderr);raise SystemExit(2)
