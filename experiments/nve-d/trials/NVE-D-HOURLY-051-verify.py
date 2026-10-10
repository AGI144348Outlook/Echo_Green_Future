"""Cycle 051 archive verifier. Run beside extracted Cycle 051 ledger/checkpoints.
This is an integrity verifier, not the complete experiment runner.
"""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
ledger = root / "ledger051.jsonl"
lines = ledger.read_bytes().splitlines(keepends=True)
assert len(lines) == 120
rows = [json.loads(line) for line in lines]
assert sum(row["model_fits"] for row in rows) == 480
assert sum(row["depth_loss_values"] for row in rows) == 23040
assert sum(row["arm_training_draw_applications"] for row in rows) == 1800000
assert sum(row["training_token_occurrences"] for row in rows) == 11423488
for n in range(10, 121, 10):
    checkpoint = json.loads((root / f"checkpoint_{n:04d}.json").read_text())
    assert checkpoint["completed_records"] == n
    digest = hashlib.sha256(b"".join(lines[:n])).hexdigest()
    assert checkpoint["ledger_prefix_sha256"] == digest
print(json.dumps({"cycle":"051","ledger_records":120,"verified_sha256_checkpoints":12,"evaluation":"="}))
