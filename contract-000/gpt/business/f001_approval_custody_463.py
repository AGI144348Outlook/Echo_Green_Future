#!/usr/bin/env python3
"""F-001 HOLD-only approval intake custody. Never authenticates approval or edits text."""
import argparse
import hashlib
import json
import re
from pathlib import Path

PROJECT = "F-001"
STATUS = "HOLD / NOT LAUNCH-READY"
SOURCE_COMMIT = "d46456a18fe412398d0ae37ec5a8c4eebb44e0c9"
REGISTER_BLOB = "300dfcf0ba9e9d236326d09b2a4b6c5467d3874c"
LOCATION_BLOB = "7fb5cd952127de7a0469cfb3d0139d7bdfb60b86"
REGISTER_COLS = ["project", "occurrence_id", "proposal_section", "short_text", "claude_proposed_state", "same_text_as", "editorial_approval", "publication_status", "tam_source_commit", "manuscript_git_blob"]
LOCATION_COLS = ["occurrence_id", "source_file", "sentence_no", "source_git_blob", "quote_match_class", "copy_target", "source_sentence_preview"]
INTAKE_COLS = ["project", "occurrence_id", "proposal_register_blob", "location_map_blob", "source_git_blob", "decision", "replacement_text", "approved_by", "decision_evidence", "release_authorized"]
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def parse_tsv(data, columns, label):
    if not isinstance(data, bytes):
        raise ValueError(label + ": expected bytes")
    if not data or data.startswith(b"\xef\xbb\xbf") or b"\r" in data or b"\x00" in data or not data.endswith(b"\n"):
        raise ValueError(label + ": noncanonical bytes/BOM/CRLF/missing final LF")
    try:
        lines = data.decode("utf-8", errors="strict").split("\n")[:-1]
    except UnicodeError as exc:
        raise ValueError(label + ": invalid UTF-8") from exc
    if not lines or lines[0].split("\t") != columns:
        raise ValueError(label + ": unexpected TSV header")
    rows = []
    for i, line in enumerate(lines[1:], 2):
        cells = line.split("\t")
        if len(cells) != len(columns):
            raise ValueError(f"{label}: line {i} has {len(cells)} fields; expected {len(columns)}")
        rows.append(dict(zip(columns, cells)))
    return rows


def validate(register_bytes, location_bytes, intake_bytes, register_pin=REGISTER_BLOB, location_pin=LOCATION_BLOB):
    if git_blob(register_bytes) != register_pin:
        raise ValueError("register: complete Git blob differs from reviewed pin")
    if git_blob(location_bytes) != location_pin:
        raise ValueError("location map: complete Git blob differs from reviewed pin")
    reg = parse_tsv(register_bytes, REGISTER_COLS, "register")
    loc = parse_tsv(location_bytes, LOCATION_COLS, "location map")
    intake = parse_tsv(intake_bytes, INTAKE_COLS, "intake")
    if not (len(reg) == len(loc) == len(intake) == 82):
        raise ValueError("all three inputs must contain exactly 82 rows")
    seen = set()
    copies = 0
    for index, (r, m, d) in enumerate(zip(reg, loc, intake), 1):
        ident = r["occurrence_id"]
        if not ident or ident in seen:
            raise ValueError(f"register: duplicate or blank occurrence at row {index}")
        seen.add(ident)
        if r["project"] != PROJECT or r["editorial_approval"] != "PROPOSED_NOT_APPROVED" or r["publication_status"] != STATUS or r["tam_source_commit"] != SOURCE_COMMIT:
            raise ValueError(f"register: unexpected project/approval/status/source at {ident}")
        if not r["short_text"] or not r["claude_proposed_state"]:
            raise ValueError(f"register: missing editorial evidence at {ident}")
        if m["occurrence_id"] != ident or m["source_file"] + "#S" + m["sentence_no"] != ident or not HEX40.fullmatch(m["source_git_blob"]):
            raise ValueError(f"location: mismatch at {ident}")
        if m["copy_target"] != r["same_text_as"]:
            raise ValueError(f"location: copy link mismatch at {ident}")
        if r["same_text_as"]:
            copies += 1
        if (d["project"] != PROJECT or d["occurrence_id"] != ident or d["proposal_register_blob"] != register_pin or d["location_map_blob"] != location_pin or d["source_git_blob"] != m["source_git_blob"]):
            raise ValueError(f"intake: source binding mismatch at {ident}")
        if (d["decision"] != "PENDING" or d["replacement_text"] or d["approved_by"] or d["decision_evidence"] or d["release_authorized"] != "false"):
            raise ValueError(f"intake: unauthorized decision or release assertion at {ident}")
    if copies != 10:
        raise ValueError(f"register: expected 10 exact-copy links, got {copies}")
    return {
        "project": PROJECT, "status": STATUS, "register_git_blob": register_pin,
        "location_map_git_blob": location_pin, "intake_git_blob": git_blob(intake_bytes),
        "occurrences": 82, "copy_links": copies, "pending": 82, "approved": 0,
        "approval_authenticated": False, "editorial_overlay_applied": False,
        "publication_authorized": False
    }


def make_pending(register_bytes, location_bytes, register_pin=REGISTER_BLOB, location_pin=LOCATION_BLOB):
    if git_blob(register_bytes) != register_pin or git_blob(location_bytes) != location_pin:
        raise ValueError("cannot prepare intake from unpinned sources")
    reg = parse_tsv(register_bytes, REGISTER_COLS, "register")
    loc = parse_tsv(location_bytes, LOCATION_COLS, "location map")
    if len(reg) != 82 or len(loc) != 82:
        raise ValueError("expected 82 source-bound rows")
    lines = ["\t".join(INTAKE_COLS)]
    for r, m in zip(reg, loc):
        lines.append("\t".join([PROJECT, r["occurrence_id"], register_pin, location_pin, m["source_git_blob"], "PENDING", "", "", "", "false"]))
    data = ("\n".join(lines) + "\n").encode("utf-8")
    validate(register_bytes, location_bytes, data, register_pin, location_pin)
    return data


def main():
    parser = argparse.ArgumentParser(description="F-001 HOLD-only pending review intake; never imports approval")
    parser.add_argument("register", type=Path)
    parser.add_argument("location_map", type=Path)
    parser.add_argument("intake", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.register.read_bytes(), args.location_map.read_bytes(), args.intake.read_bytes())
    except (OSError, ValueError) as exc:
        print("F-001 HOLD / INTAKE REFUSED: " + str(exc))
        raise SystemExit(2)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
