#!/usr/bin/env python3
"""F-001 synthetic package-evidence *shape* gate; never authorizes release.

Reads at most 64 KiB of JSON and checks syntax, exact schema and pinned
source/dataset identities. It does NOT read EPUB/PDF bytes, validate signatures,
prove rights, verify editorial approvals, or grant publication permission.
Usage: python3 -I -B F-001-PACKAGE-EVIDENCE-GATE-353.py manifest.json
"""
import json
import re
import sys
import uuid
from pathlib import Path

SOURCE = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
CSV = {
    "dataset-a.csv": "989d83c16568f23a97251d93919068f3a5e726c738644625af909b278f395fdb",
    "dataset-b.csv": "ff442e48acaf00900a3bc3d7900bf987995355a34226b749dbd5b81878e2f7c0",
}
EVIDENCE = ("editorial", "rights", "attribution", "independent_rebuild",
            "epubcheck", "ace", "pdf_review", "listing_parity")
HEX = re.compile(r"[0-9a-f]{64}\Z")


def reject(message):
    raise ValueError(message)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            reject("duplicate JSON key: " + key)
        result[key] = value
    return result


def exact(obj, keys, label):
    if not isinstance(obj, dict) or set(obj) != set(keys):
        reject(label + " has missing or unexpected keys")


def digest(value, label):
    if not isinstance(value, str) or HEX.fullmatch(value) is None:
        reject(label + " is not lowercase SHA-256")


def size(value, label):
    if type(value) is not int or not 0 < value <= 100_000_000:
        reject(label + " size invalid")


def validate(obj):
    exact(obj, ("schema", "project", "release", "authorization", "book_id",
                "stage", "artifacts", "evidence"), "manifest")
    if (obj["schema"] != "F-001-PACKAGE-EVIDENCE-v1" or
            obj["project"] != "F-001" or obj["release"] != "HOLD" or
            obj["authorization"] != "NOT_GRANTED"):
        reject("manifest must remain F-001 / HOLD / NOT_GRANTED")
    try:
        ident = uuid.UUID(obj["book_id"].removeprefix("urn:uuid:"))
        if obj["book_id"] != "urn:uuid:" + str(ident):
            reject("book_id must be canonical urn:uuid")
    except (TypeError, ValueError, AttributeError):
        reject("book_id invalid")
    stage = obj["stage"]
    exact(stage, ("receipt_sha256", "source_commit", "release",
                  "receipt_type", "csv_sha256"), "stage")
    digest(stage["receipt_sha256"], "stage receipt")
    if (stage["source_commit"] != SOURCE or stage["release"] != "HOLD" or
            stage["receipt_type"] != "STAGING_ONLY" or
            stage["csv_sha256"] != CSV):
        reject("stage source, dataset pins or HOLD boundary mismatch")
    exact(obj["artifacts"], ("epub", "pdf"), "artifacts")
    for kind, record in obj["artifacts"].items():
        exact(record, ("sha256", "bytes"), kind)
        digest(record["sha256"], kind)
        size(record["bytes"], kind)
    exact(obj["evidence"], EVIDENCE, "evidence")
    for kind, value in obj["evidence"].items():
        digest(value, kind)
    return {"project": "F-001", "result": "STRUCTURE_VALID_ONLY",
            "release": "HOLD", "publication_authorized": False,
            "warning": "Evidence references are unverified; independent byte checks and Timothy approval required"}


def load(path):
    with open(path, "rb") as stream:
        raw = stream.read(65_537)
    if len(raw) > 65_536:
        reject("manifest exceeds 64 KiB")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                      parse_constant=lambda x: reject("nonfinite JSON: " + x))


def main(argv):
    try:
        if len(argv) != 2:
            reject("usage: gate.py manifest.json")
        result = validate(load(Path(argv[1])))
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, UnicodeError) as exc:
        print(json.dumps({"project": "F-001", "result": "REJECTED", "release": "HOLD",
                          "publication_authorized": False, "reason": str(exc)[:240]},
                         sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
