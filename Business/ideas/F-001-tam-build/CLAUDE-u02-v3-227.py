import hashlib, importlib.util, json, subprocess, sys
spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
repo = sys.argv[2]
res = {}
for row, f, s, e, cs, ce in ((16, "Article 6", 3130, 3209, 3077, 3152), (49, "Collective information", 21359, 21438, 21156, 21231)):
    src = subprocess.run(["git", "-C", repo, "show", f"d46456a1:{f}"], capture_output=True, check=True).stdout
    h = hashlib.sha256(src).hexdigest()
    true_text = src[s:e].decode("utf-8")
    r_ok = gate.inspect_span(src, h, s, e, true_text)
    # exploratory: the code-point offsets passed as if they were byte offsets, expected text = true span
    try:
        r_unit = gate.inspect_span(src, h, cs, ce, true_text)
    except Exception as ex:
        r_unit = f"EXCEPTION {type(ex).__name__}"
    res[row] = {"byte_offsets": r_ok, "cp_offsets_as_bytes": r_unit}
print(json.dumps(res, sort_keys=True, default=str))
