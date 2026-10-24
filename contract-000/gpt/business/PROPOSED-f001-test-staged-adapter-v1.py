#!/usr/bin/env python3
"""Prospective T0-T7 for Run 314 Issue #33; T8 exploratory extra."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import sys

ROOT = Path(__file__).resolve().parent
TOOLS = ROOT / 'tools'
SOURCE = ROOT / 'artifacts'
SCRIPT = TOOLS / 'PROPOSED-f001-staged-coordinator-adapter-v1.py'
spec = importlib.util.spec_from_file_location('f001_adapter', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
results = []

def run(label, change=None, expected='PASS', hook=None, check=None):
    with tempfile.TemporaryDirectory(prefix='f001-run314-fixture-') as td:
        src = Path(td) / 'artifacts'
        shutil.copytree(SOURCE, src)
        receipt = json.loads((src / 'receipt.json').read_text())
        receipt['environment']['build_output_realpath'] = str(src)
        (src / 'receipt.json').write_text(json.dumps(receipt, sort_keys=True) + '\n')
        if change:
            change(src)
        kwargs = hook(src) if hook else {}
        result = m.coordinate_staged(src, TOOLS, **kwargs)
        assert result['integrity'] == expected, (label, result)
        assert result['release'] == 'HOLD' and result['readiness'] == 'BLOCKED', (label, result)
        assert result['publication_authorization'] == 'ABSENT'
        assert result['source_pin_authenticated'] is False
        assert result['approval_authenticated'] is False
        if check:
            check(result)
        results.append({'case': label, 'expected': expected, 'observed': result['integrity'],
                        'issues': result.get('issues'), 'stages': result.get('stages'),
                        'derived_receipt': result.get('staging_provenance',{}).get('derived_receipt_sha256')})

def mutate_json(src, name, action):
    path=src/name
    obj=json.loads(path.read_text()); action(obj)
    path.write_text(json.dumps(obj,sort_keys=True)+'\n')

run('T0_valid_actual_reviewed_chain', expected='PASS',
    check=lambda r: (len(r['stages']) == 3 or (_ for _ in ()).throw(AssertionError(r))))
run('T1_wrong_artifact_digest',lambda src:(src/'book.epub').write_bytes(b'altered'),expected='FAIL')

def symlink_artifact(src):
    p=src/'book.pdf';p.unlink();p.symlink_to(src/'dataset-b.csv')
run('T2_symlinked_artifact',symlink_artifact,expected='FAIL')

def swap_hook(src):
    def hook(label, relative, fd):
        if label == 'artifact_epub':
            p=src/'book.epub';p.rename(src/'book.original');p.symlink_to(src/'book.pdf')
    return {'_after_open':hook}
run('T3_path_swap_after_fd_open',expected='PASS',hook=swap_hook)
run('T4_parent_traversal_receipt',lambda src:mutate_json(src,'receipt.json',lambda x:x['artifacts']['epub'].update(path='../book.epub')),expected='FAIL')
run('T5_missing_artifact',lambda src:(src/'book.pdf').unlink(),expected='FAIL')

def mutate_pins_hook(src):
    def before():
        p=src/'pins.json';p.write_text(p.read_text()+' ')
    return {'_before_snapshot':before}
run('T6_json_changes_between_read_and_snapshot',expected='FAIL',hook=mutate_pins_hook)

def derived_check(r):
    p=r['staging_provenance'];assert p['original_receipt_sha256']!=p['derived_receipt_sha256']
    assert p['source_pin_authenticated'] is False and p['publication_authorization']=='ABSENT'
run('T7_derived_receipt_disclosed',expected='PASS',check=derived_check)
run('T8_exploratory_forged_original_root',lambda src:mutate_json(src,'receipt.json',lambda x:x['environment'].update(build_output_realpath='/tmp/not-this-root')),expected='FAIL')
meta={'python':sys.version.split()[0], 'adapter_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
      'adapter_git_blob':m.git_blob(SCRIPT.read_bytes()),'helper_git_blob':m.HELPER_BLOB,
      'coordinator_git_blob':m.COORDINATOR_BLOB,
      'pretest_issue':'https://github.com/AGI144348Outlook/Echo_Green_Future/issues/33',
      'fixtures':'archived public-derived Dataset A; synthetic EPUB/PDF placeholders',
      'count':len(results),'passed':len(results)}
(ROOT/'evidence'/'run314-staged-adapter-results.json').write_text(json.dumps({'metadata':meta,'results':results},indent=2,sort_keys=True)+'\n')
print(json.dumps({'passed':len(results),'total':len(results),'cases':[x['case'] for x in results]}))
