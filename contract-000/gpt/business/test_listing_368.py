import hashlib, json, pathlib, subprocess, sys, tempfile, csv
src=pathlib.Path(__file__).with_name('listing_check.py')
b=src.read_bytes(); got=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
assert got=='adc3123c303168650e03270701cd3123afe0ce28',f'Git blob mismatch: {got}'
results=[]
with tempfile.TemporaryDirectory(prefix='f001-listing-368-') as td:
    base=pathlib.Path(td);out=base/'out';out.mkdir();listing=base/'listing.md'
    (out/'tam-review.epub').write_bytes(b'NOT AN EPUB; deliberately invalid')
    (out/'dataset.csv').write_text('item,grams\na,1\n',encoding='utf-8')
    (out/'manuscript.txt').write_text('This manuscript still contains the purportedly cut claim: TAM is certainly exact.',encoding='utf-8')
    def claim(status):
        with (out/'claims.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=['claim','status']);w.writeheader();w.writerow({'claim':'TAM is certainly exact.','status':status})
    def run(name,text,expected):
        listing.write_text(text,encoding='utf-8')
        cp=subprocess.run([sys.executable,'-I',str(src),str(listing),str(out)],capture_output=True,text=True,timeout=5)
        observed=cp.returncode;ok=observed==expected
        results.append({'name':name,'expected_exit':expected,'actual_exit':observed,'pass':ok,'stdout':cp.stdout,'stderr':cp.stderr})
        print(name,'PASS' if ok else 'FAIL','exit',observed,'expected',expected)
    claim('cut')
    run('invalid_epub_uncut_claim_and_unverified_pdf_promise','This draft includes an EPUB and CSV dataset and a PDF. Each claim is marked. Research notebook only.\n',0)
    run('invalid_epub_without_pdf_promise','This draft includes an EPUB and CSV dataset. Research notebook only.\n',0)
    (out/'claims.csv').unlink()
    run('missing_claims_csv','This draft includes an EPUB and CSV dataset. Research notebook only.\n',1)
    claim('cut')
    run('forbidden_testimonial','This draft includes an EPUB and CSV dataset with testimonial.\n',1)
    run('pdf_pages_assertion_without_report','This draft includes an EPUB and CSV dataset and a PDF of about 40 pages.\n',1)
    claim('open')
    run('open_claim_status','This draft includes an EPUB and CSV dataset.\n',1)
report={'source_git_blob':got,'fixture':'synthetic; not actual TAM manuscript or package','results':results,'passed':sum(x['pass'] for x in results),'total':len(results),'status':'HOLD'}
path=pathlib.Path(__file__).with_name('F-001-LISTING-NEGATIVE-RESULTS-368.json');path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('RESULTS',report['passed'],'/',report['total'])
if report['passed']!=report['total']:sys.exit(1)
