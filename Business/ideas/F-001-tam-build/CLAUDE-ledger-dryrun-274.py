# F-001 §274 (Claude 05Z): checks K1-K3 on LEDGER-DRYRUN-274.json with the symbolic params.
# Synthetic arithmetic only; proves the row shapes are self-consistent, not any real fee.
import json, sys
d = json.load(open(sys.argv[1]))
p = d["params_for_check_only"]; P = p["P"]
fee = p["platform_rate"]*P + p["platform_fixed"] + p["r"]*P + p["f"]
sale = {"gross": P, "fees": fee}; sale["net"] = sale["gross"] - sale["fees"]
out = {}
for returned in (True, False):
    ref = {"gross": -P, "fees": -fee if returned else 0.0}; ref["net"] = ref["gross"] - ref["fees"]
    out["fees_returned" if returned else "fees_kept"] = round(sale["net"] + ref["net"], 2)
rows = {r["id"]: r for r in d["rows"]}
out["K1_net_formula_all_rows"] = all(r["net"] in ("gross - fees", r["gross"]) for r in d["rows"])
out["K2_refund_names_reversed_row"] = rows["R2"]["proposed_reverses_row"] == "R1" and rows["R2"]["gross"] == "-" + rows["R1"]["gross"]
out["K3_full_refund_fees_returned_sums_zero"] = out["fees_returned"] == 0.0
out["K3_fees_kept_residual_equals_minus_fee"] = out["fees_kept"] == round(-fee, 2)
print(json.dumps(out, sort_keys=True))
