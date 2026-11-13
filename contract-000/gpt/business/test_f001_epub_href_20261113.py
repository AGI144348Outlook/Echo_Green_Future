#!/usr/bin/env python3
"""F-001 narrow synthetic manifest href fixtures; run only after Issue #463 preregistration.
Usage: python3 contract-000/gpt/business/test_f001_epub_href_20261113.py
Requires adjacent F-001-EPUB-HREF-GATE-20261113-17Z.py; no network or writes.
"""
import importlib.util, json, pathlib, sys
source=pathlib.Path(__file__).with_name("F-001-EPUB-HREF-GATE-20261113-17Z.py")
spec=importlib.util.spec_from_file_location("f001_href_gate",source)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
base=["OPS/book.opf","OPS/a.xhtml"]
cases=[
("valid","a.xhtml",base,True),
("missing","b.xhtml",base,False),
("traversal","../a.xhtml",base,False),
("encoded_traversal","%2e%2e/a.xhtml",base,False),
("remote","https://x.test/a.xhtml",base,False),
("absolute","/OPS/a.xhtml",base,False),
("empty","",base,False),
("query","a.xhtml?x=1",base,False),
("double_encoded","%252e%252e/a.xhtml",base,False),
("duplicate_zip","a.xhtml",base+["OPS/a.xhtml"],False),
("fragment","a.xhtml#anchor",base,True),
]
rows=[]
for name,href,names,expected in cases:
    try:
        module.validate_opf_references("OPS/book.opf",[{"id":"x","href":href}],names)
        accepted=True; error=None
    except ValueError as exc:
        accepted=False; error=str(exc)
    rows.append({"case":name,"expected_accept":expected,"actual_accept":accepted,"pass":accepted==expected,"error":error})
print(json.dumps({"source":str(source),"python":sys.version.split()[0],"results":rows},sort_keys=True,indent=2))
sys.exit(0 if all(row["pass"] for row in rows) else 1)
