#!/usr/bin/env python3
"""Run 316 prospective T0-T9 (GitHub Issue #35), synthetic fixtures only."""
import hashlib, importlib.util, json, os, pathlib, shutil, stat, sys, tempfile

BASE=pathlib.Path(__file__).resolve().parent
TOOLS=BASE/'contract314'/'tools'
SOURCE=BASE/'contract314'/'artifacts'

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod
v=load(TOOLS/'PROPOSED-f001-verified-stage-copy-v2.py','f001_vcopy_v2')
a=load(TOOLS/'PROPOSED-f001-staged-coordinator-adapter-v2.py','f001_adapter_v2')
sha=lambda b:hashlib.sha256(b).hexdigest()
results=[]

def run(label,fn,expected):
    try: observed=fn()
    except BaseException as e: observed='REJECTED:'+type(e).__name__
    results.append({'case':label,'expected':expected,'observed':observed,'pass':expected==observed})

def fixture_case(change=None,hook=None):
    with tempfile.TemporaryDirectory(prefix='f001-run316-') as td:
        src=pathlib.Path(td)/'artifacts';shutil.copytree(SOURCE,src)
        receipt=json.loads((src/'receipt.json').read_text())
        receipt['environment']['build_output_realpath']=str(src)
        (src/'receipt.json').write_text(json.dumps(receipt,sort_keys=True)+'\n')
        if change:change(src)
        return a.coordinate_staged(src,TOOLS,**(hook(src) if hook else {}))

with tempfile.TemporaryDirectory(prefix='f001-v2-copy-') as td:
    root=pathlib.Path(td);data=b'F001 SYNTHETIC NOT A BOOK';src=root/'src';src.write_bytes(data)
    def t0():
        r=v.copy_verified(src,root/'valid',sha(data),len(data));return 'ACCEPTED' if r=={'sha256':sha(data),'size':len(data)} else 'BAD'
    run('T0_valid_copy',t0,'ACCEPTED')
    def t1():
        dest=root/'existing';dest.write_bytes(b'PRESERVE ME')
        try:v.copy_verified(src,dest,sha(data),len(data))
        except FileExistsError:return 'PRESERVED' if dest.read_bytes()==b'PRESERVE ME' else 'DELETED'
        return 'NOT_REJECTED'
    run('T1_V2_existing_dest_preserved',t1,'PRESERVED')
    def t2():
        dest=root/'swap';outside=root/'outside';outside.write_bytes(b'EXTERNAL')
        outside.chmod(0o644);original=os.fchmod;state={'done':False}
        def inject(fd,mode):
            if not state['done']:
                state['done']=True
                dest.rename(root/'moved');dest.symlink_to(outside)
            return original(fd,mode)
        os.fchmod=inject
        try:
            try:v.copy_verified(src,dest,sha(data),len(data))
            except OSError:pass
        finally:os.fchmod=original
        return 'OUTSIDE_UNCHANGED' if stat.S_IMODE(outside.stat().st_mode)==0o644 and state['done'] else 'OUTSIDE_CHANGED'
    run('T2_V4_symlink_swap_no_external_chmod',t2,'OUTSIDE_UNCHANGED')
    def t3():
        src.write_bytes(b'X'+data[1:])
        try:v.copy_verified(src,root/'tampered',sha(data),len(data))
        finally:src.write_bytes(data)
    run('T3_same_size_changed_source',t3,'REJECTED:ValueError')
    def t4():
        p=root/'valid';p.chmod(0o600);p.write_bytes(b'Z'+data[1:]);v.verify_staged({p:{'sha256':sha(data),'size':len(data)}})
    run('T4_changed_staged_bytes',t4,'REJECTED:ValueError')
    run('T5_wrong_sha',lambda:v.copy_verified(src,root/'wrong','0'*64,len(data)),'REJECTED:ValueError')

def check_integrity(result,expected):
    assert result['release']=='HOLD' and result['readiness']=='BLOCKED',result
    assert result['publication_authorization']=='ABSENT' and result['source_pin_authenticated'] is False,result
    assert result['approval_authenticated'] is False,result
    return result['integrity']

def t6():
    control=fixture_case()
    assert check_integrity(control,'PASS')=='PASS',control
    def bad(src):(src/'disposition.json').write_text('{"schema":"x","schema":"y"}')
    invalid=fixture_case(change=bad)
    assert check_integrity(invalid,'FAIL')=='FAIL',invalid
    return 'VALID_PASS_INVALID_FAIL'
run('T6_optional_disposition_bounded_json',t6,'VALID_PASS_INVALID_FAIL')

def t7():
    def bad(src):
        path=src/'binding.json';text=path.read_text();path.write_text('{"x":1,"x":2}')
    return check_integrity(fixture_case(change=bad),'FAIL')
run('T7_duplicate_json_rejected',t7,'FAIL')

def t8():
    r=fixture_case();assert check_integrity(r,'PASS')=='PASS',r
    p=r.get('staging_provenance',{})
    assert p.get('staged_copy_verified') is True and p.get('original_receipt_sha256')!=p.get('derived_receipt_sha256'),r
    assert len(r.get('stages',[]))==3,r
    assert set(p.get('metadata_sha256',{}))=={'pins','binding','v5'},r
    return 'PASS/HOLD/BLOCKED'
run('T8_actual_reviewed_chain_synthetic_files',t8,'PASS/HOLD/BLOCKED')

def t9():
    original=a.reviewed_module
    def intercepted(path,expected,name):
        module=original(path,expected,name)
        if name=='f001_verified_copy_v2':
            base=module.copy_verified
            def corrupt(source,destination,*args,**kwargs):
                result=base(source,destination,*args,**kwargs)
                if pathlib.Path(destination).name=='binding.json':
                    p=pathlib.Path(destination);p.chmod(0o600)
                    b=p.read_bytes();p.write_bytes(b'Z'+b[1:])
                return result
            module.copy_verified=corrupt
        return module
    a.reviewed_module=intercepted
    try:return check_integrity(fixture_case(),'FAIL')
    finally:a.reviewed_module=original
run('T9_staged_binding_tamper_rejected',t9,'FAIL')

out={'scope':'GPT Run 316, synthetic fixtures, actual archived reviewed verification scripts, not production release',
     'pretest_issue':'https://github.com/AGI144348Outlook/Echo_Green_Future/issues/35',
     'python':sys.version.split()[0],
     'helper_git_blob':a.git_blob((TOOLS/'PROPOSED-f001-verified-stage-copy-v2.py').read_bytes()),
     'adapter_git_blob':a.git_blob((TOOLS/'PROPOSED-f001-staged-coordinator-adapter-v2.py').read_bytes()),
     'executed':len(results),'passed':sum(x['pass'] for x in results),'results':results}
(BASE/'run316-results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['passed']==out['executed'] else 1)
