#!/usr/bin/env python3
"""F-001 §140 (Claude, read-only review aid; NOT a release script).
X4: a good run into OUT, then a failing run (one Dataset B row removed, pins stubbed as in
GPT run 333 harness) into the SAME OUT. Shows the earlier files stay and look complete.
Usage: python3 -I -B CLAUDE-csv-preflight-333-review-140.py <builder.py> <tam-clone@d46456a>
Runs on temp copies only; never writes to the clone.
"""
import importlib.util, sys, shutil, tempfile, subprocess
from pathlib import Path
code, tam = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("c", code); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
td = Path(tempfile.mkdtemp())
out = td/"deliv"
m.main(tam, out)  # good run first (real pins)
before = sorted(p.name for p in out.iterdir())
# now a failing run on a mutated copy into the SAME out dir (pins stubbed like the harness)
src = td/"src"; shutil.copytree(tam, src, ignore=shutil.ignore_patterns('.git'))
b = (src/m.B_FILE).read_text().splitlines(); (src/m.B_FILE).write_text("\n".join(b[:-1])+"\n")
m.source_pins = lambda s: {m.A_FILE: m.PIN_A_BLOB, m.B_FILE: m.PIN_B_BLOB}
try: m.main(src, out); err=None
except Exception as e: err=repr(e)
after = sorted(p.name for p in out.iterdir())
print({"error": err, "stale_files_left": after, "same_as_before": before==after})
