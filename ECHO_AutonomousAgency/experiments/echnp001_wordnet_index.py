#!/usr/bin/env python3
"""ECHNP-001: source-only full Princeton WordNet definition evidence index.

This is a deterministic Echo research *indexer*, not the Echo Governor,
not an inferred knowledge graph, not live Neon or OpenDiagram integration.
Pre-test record: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/454
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
import gzip
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable

WORD_RE = re.compile(r"[^\W_]+(?:['\u2019-][^\W_]+)*", re.UNICODE)
PROTOCOL = "echnp.dictionary-evidence/v1"
# Only explicit, named WordNet-native edges. Grammar and co-occurrence NEVER
# cause an automatically asserted is_a / part_of / causal relationship.
WORDNET_RELATIONS = (
    ("hypernyms", "is_a"),
    ("instance_hypernyms", "instance_of"),
    ("part_meronyms", "has_part"),
    ("part_holonyms", "part_of"),
    ("member_meronyms", "has_member"),
    ("member_holonyms", "member_of"),
    ("substance_meronyms", "has_substance"),
    ("substance_holonyms", "substance_of"),
    ("entailments", "entails"),
    ("causes", "causes"),
    ("attributes", "attribute"),
    ("similar_tos", "similar_to"),
)

def lexical_occurrences(definition: str, synset_id: str):
    """Enumerate every word token: function words are never filtered."""
    for position, m in enumerate(WORD_RE.finditer(definition)):
        word = m.group()
        # The lexeme is an orthographic identity only; no sense is guessed.
        yield {
            "id": f"occ:wn:{synset_id}:{position}",
            "position": position,
            "surface": word,
            "lexeme_id": "word:" + word.casefold(),
            "start": m.start(),
            "end": m.end(),
            "definition_id": "def:wn:" + synset_id,
            "headword_sense_id": "wn:" + synset_id,
            "source_ref": "wordnet:" + synset_id,
            "relation_to_headword": "word_occurs_in_definition_of",
            "relation_to_definition": "occurs_in_definition",
        }

def definition_record(s):
    sid = s.name()
    text = s.definition()
    return {
        "id": "def:wn:" + sid,
        "headword_sense_id": "wn:" + sid,
        "headwords": sorted(s.lemma_names()),
        "part_of_speech": s.pos(),
        "definition": text,
        "source_ref": "wordnet:" + sid,
        "protocol": PROTOCOL,
    }

def native_relations(s):
    """Return WordNet-sourced sense-to-sense edges, never lexical guesses."""
    source = s.name()
    for method, relation in WORDNET_RELATIONS:
        getter = getattr(s, method, None)
        if not callable(getter):
            continue
        for target in getter():
            target_sid = target.name()
            yield {
                "id": "wn-edge:" + source + ":" + method + ":" + target_sid,
                "source_node": "wn:" + source,
                "target_node": "wn:" + target_sid,
                "relation_type": relation,
                "relation_domain": "lexical",
                "evidence_state": "source_native",
                "source_ref": "wordnet:" + source + "#" + method,
            }

def encode(record):
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

@contextmanager
def compressed_jsonl(path: Path):
    # gzip reproducibility: no embedded filename or write-time timestamp
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=6) as zipped:
            yield lambda obj: zipped.write(encode(obj))

def sha256_file(p: Path):
    h = hashlib.sha256()
    with p.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def build_index(synsets: Iterable, output: Path):
    output.mkdir(parents=True, exist_ok=True)
    files = {
        "definitions": output / "definitions.jsonl.gz",
        "occurrences": output / "occurrences.jsonl.gz",
        "native_relations": output / "native_relations.jsonl.gz",
    }
    counts = Counter()
    pos_counts = Counter()
    distinct_lexemes = set()
    preview = []
    with compressed_jsonl(files["definitions"]) as write_def, \
         compressed_jsonl(files["occurrences"]) as write_occ, \
         compressed_jsonl(files["native_relations"]) as write_link:
        for s in synsets:
            sid = s.name()
            entry = definition_record(s)
            write_def(entry)
            counts["definitions"] += 1
            pos_counts[entry["part_of_speech"]] += 1
            local_preview = []
            for occ in lexical_occurrences(entry["definition"], sid):
                assert entry["definition"][occ["start"]:occ["end"]] == occ["surface"]
                write_occ(occ)
                counts["occurrences"] += 1
                distinct_lexemes.add(occ["lexeme_id"])
                if occ["surface"].casefold() in {"of", "the", "in", "with", "for", "through", "between", "and", "a", "an", "to"}:
                    counts["function_word_occurrences"] += 1
                if len(preview) < 2:
                    local_preview.append(occ)
            for edge in native_relations(s):
                write_link(edge)
                counts["native_relations"] += 1
            if len(preview) < 2:
                preview.append({"definition": entry, "occurrences": local_preview,
                                "producer": "echnp_source_indexer_not_echo_governor"})
            if counts["definitions"] % 25000 == 0:
                print("ECHNP_PROGRESS " + json.dumps({"definitions": counts["definitions"],
                    "occurrences": counts["occurrences"]}), flush=True)
    counts["unique_definition_lexemes"] = len(distinct_lexemes)
    manifest = {
        "protocol": PROTOCOL,
        "producer": "echnp_source_indexer_not_echo_governor",
        "source": "Princeton WordNet via NLTK corpus.reader",
        "scope": "every synset emitted by wordnet.all_synsets(); no hard-coded vocabulary cap",
        "counts": dict(counts),
        "part_of_speech": dict(pos_counts),
        "files": {name: {"file": p.name, "sha256": sha256_file(p), "bytes": p.stat().st_size}
                  for name, p in files.items()},
        "semantic_integrity": "only WordNet-native sense links; definition occurrence is not a proven semantic inference",
        "neon_sync": "NOT EXECUTED",
        "opendiagram_sync": "NOT EXECUTED",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    (output / "source_preview.json").write_text(json.dumps(preview, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print("ECHNP_RESULT " + json.dumps({"counts": manifest["counts"], "part_of_speech": manifest["part_of_speech"],
                                      "manifest_sha256": sha256_file(output / "manifest.json")}), flush=True)
    return manifest

def verify_index(output: Path):
    manifest = json.loads((output / "manifest.json").read_text())
    for meta in manifest["files"].values():
        p = output / meta["file"]
        if not p.exists() or sha256_file(p) != meta["sha256"]:
            raise AssertionError("Missing or modified graph artifact: " + meta["file"])
    measured = Counter()
    seen_definitions = set()
    # Separate read pass over the actual persisted dataset.
    with gzip.open(output / "definitions.jsonl.gz", "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row["id"] in seen_definitions:
                raise AssertionError("Duplicate dictionary sense: " + row["id"])
            seen_definitions.add(row["id"])
            measured["definitions"] += 1
            measured["raw_gloss_tokens"] += len(list(WORD_RE.finditer(row["definition"])))
    with gzip.open(output / "occurrences.jsonl.gz", "rt", encoding="utf-8") as handle:
        for line in handle:
            o = json.loads(line)
            if o["definition_id"] not in seen_definitions:
                raise AssertionError("Orphaned definition occurrence: " + o["id"])
            measured["occurrences"] += 1
            if o["surface"].casefold() in {"of", "the", "in", "with", "for", "through", "between", "and", "a", "an", "to"}:
                measured["function_word_occurrences"] += 1
    with gzip.open(output / "native_relations.jsonl.gz", "rt", encoding="utf-8") as handle:
        for line in handle:
            edge = json.loads(line)
            if edge["source_node"] not in {r.replace("def:", "", 1) for r in seen_definitions}:
                raise AssertionError("Unknown source synset: " + edge["id"])
            measured["native_relations"] += 1
    if measured["raw_gloss_tokens"] != measured["occurrences"]:
        raise AssertionError("Definition word missing from stored occurrence graph")
    for k in ("definitions", "occurrences", "function_word_occurrences", "native_relations"):
        if measured[k] != manifest["counts"][k]:
            raise AssertionError(f"{k} mismatch: {measured[k]} != {manifest['counts'][k]}")
    print("ECHNP_VERIFIED " + json.dumps({"definitions": measured["definitions"],
                                        "occurrences": measured["occurrences"],
                                        "native_relations": measured["native_relations"]}), flush=True)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    from nltk.corpus import wordnet as wn
    import nltk
    manifest = build_index(wn.all_synsets(), args.output)
    manifest["nltk_version"] = nltk.__version__
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    verify_index(args.output)

if __name__ == "__main__":
    main()
