"""Build the Dev Suite and the Canvas Keyboard and Terminal.

    npm install            (fetches pyodide 0.26.4 into node_modules)
    python build.py        (writes dist/canvas-keyboard-terminal.html and dist/dev-suite.html)

1. Keyboard: keyboard/src/page.html + keyboard/src/substrate_data.py + keyboard/src/app.js
   -> dist/canvas-keyboard-terminal.html (standalone; loads Python from the jsDelivr CDN).
2. The same keyboard, adapted to borrow the Dev Suite's Python, is embedded (base64) into
   suite/src/app_part.html as KB_DOC_B64.
3. Suite: head_part + loader_part + app_part, with Pyodide packed in from node_modules
   -> dist/dev-suite.html (self-contained, works offline, about 10 MB).
"""
import base64, gzip, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda *p: os.path.join(ROOT, *p)
read = lambda *p: open(P(*p), encoding="utf-8").read()
def write(text, *p):
    os.makedirs(os.path.dirname(P(*p)), exist_ok=True)
    open(P(*p), "w", encoding="utf-8").write(text)

# 1. standalone keyboard
page = read("keyboard", "src", "page.html").replace("__KEYBOARDS3__", read("keyboard", "src", "substrate_data.py"))
app = read("keyboard", "src", "app.js")
write(page + app, "dist", "canvas-keyboard-terminal.html")

# 2. embedded keyboard: no CDN; run the substrate in the Suite's Python, in its own namespace
emb = app.replace('<script src="https://cdn.jsdelivr.net/npm/pyodide@0.26.4/pyodide.js"></script>\n', "")
old = '''    py=await loadPyodide(); py.runPython($("substrate").textContent);
    const c=JSON.parse(py.runPython("config()")); KB=c.keyboards; USES=c.uses; EXAMPLES=c.examples;'''
new = '''    const host=window.parent&&window.parent!==window?window.parent:null;
    for(let i=0;i<300&&!(host&&host.devPy);i++) await new Promise(r=>setTimeout(r,100));
    if(!(host&&host.devPy)) throw new Error("Dev Suite Python not available");
    const P=host.devPy, ns=P.globals.get("dict")();
    py={ runPython:(code)=>P.runPython(code,{globals:ns}), globals:{ set:(k,v)=>ns.set(k,v) } };
    py.runPython($("substrate").textContent);
    const c=JSON.parse(py.runPython("config()")); KB=c.keyboards; USES=c.uses; EXAMPLES=c.examples;'''
assert old in emb, "keyboard boot block not found"
emb = emb.replace(old, new).replace('''$("st").textContent="Python "+py.runPython("import sys; sys.version.split()[0]");''',
                                    '''$("st").textContent="Python "+py.runPython("import sys; sys.version.split()[0]")+" (Dev Suite)";''')
b64 = base64.b64encode((page + emb).encode()).decode()
app_part = read("suite", "src", "app_part.html")
app_part = re.sub(r'const KB_DOC_B64="[A-Za-z0-9+/=]*";', 'const KB_DOC_B64="' + b64 + '";', app_part, count=1)
write(app_part, "suite", "src", "app_part.html")

# 3. the Suite, with Pyodide packed in
tpl = read("suite", "src", "head_part.html") + read("suite", "src", "loader_part.html") + app_part
PY = P("node_modules", "pyodide") + os.sep
pack = lambda f, gz: base64.b64encode(gzip.compress(open(PY + f, "rb").read(), 9, mtime=0) if gz else open(PY + f, "rb").read()).decode()
out = (tpl.replace("__WASM_GZ__", pack("pyodide.asm.wasm", True))
          .replace("__STDLIB__", pack("python_stdlib.zip", False))
          .replace("__LOCK_GZ__", pack("pyodide-lock.json", True))
          .replace("__LOADER_JS__", open(PY + "pyodide.js", encoding="utf-8").read().replace("//# sourceMappingURL=pyodide.js.map", ""))
          .replace("__ASM_JS__", open(PY + "pyodide.asm.js", encoding="utf-8").read()))
write(out, "dist", "dev-suite.html")
print("dist/canvas-keyboard-terminal.html", len(page + app) // 1024, "KB")
print("dist/dev-suite.html", len(out) // 1024 // 1024, "MB")
