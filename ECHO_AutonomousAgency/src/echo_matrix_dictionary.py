#!/usr/bin/env python3
"""Recess Matrix Dictionary.

A thin environment around EchoDictionary. It gives ECHO an empty matrix
workspace in which dictionary observations and glyph blocks can be arranged
without prescribing semantic organization. ECHO chooses matrix names, cells,
relations, and glyph indexes. All writes are sandbox-local proposals.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
import json, uuid

@dataclass
class MatrixCell:
    id: str
    content: object
    source: str
    metadata: dict = field(default_factory=dict)

@dataclass
class CustomMatrix:
    id: str
    name: str
    purpose: str = ""
    cells: dict = field(default_factory=dict)
    relations: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class MatrixDictionary:
    """Dictionary whose cover opens into a blank, user/ECHO-constructed matrix space."""

    def __init__(self, dictionary=None, workspace="ECHO_AutonomousAgency/sandbox/recess_matrices"):
        self.dictionary = dictionary
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.matrices = {}
        self.indexes = []

    def lookup(self, word, limit=8):
        if self.dictionary is None:
            raise RuntimeError("No dictionary provider attached")
        return self.dictionary.senses(word, limit=limit)

    def new_matrix(self, name, purpose=""):
        mid = "MX-" + uuid.uuid4().hex[:10].upper()
        self.matrices[mid] = CustomMatrix(mid, str(name), str(purpose))
        return mid

    def add_cell(self, matrix_id, content, source="ECHO", metadata=None, cell_id=None):
        m = self.matrices[matrix_id]
        cid = cell_id or ("C-" + uuid.uuid4().hex[:8].upper())
        if cid in m.cells:
            raise ValueError("cell id already exists")
        m.cells[cid] = asdict(MatrixCell(cid, content, source, metadata or {}))
        return cid

    def add_dictionary_cell(self, matrix_id, word, sense_index=0):
        senses = self.lookup(word)
        if not senses:
            return self.add_cell(matrix_id, {"word": word, "sense": None}, "dictionary")
        if not 0 <= sense_index < len(senses):
            raise IndexError("sense_index outside available senses")
        return self.add_cell(matrix_id, {"word": word, "sense": senses[sense_index]}, "dictionary")

    def relate(self, matrix_id, source_cell, target_cell, relationship_type, evidence=None):
        m = self.matrices[matrix_id]
        if source_cell not in m.cells or target_cell not in m.cells:
            raise KeyError("both cells must exist")
        edge = {
            "source": source_cell,
            "target": target_cell,
            "relationship_type": str(relationship_type),
            "evidence": evidence,
            "proposed_by": "ECHO"
        }
        m.relations.append(edge)
        return len(m.relations) - 1

    def index_glyph(self, glyph, matrix_id, label="", relationship_type="custom_index"):
        if matrix_id not in self.matrices:
            raise KeyError("matrix does not exist")
        idx = {
            "id": "IDX-" + uuid.uuid4().hex[:10].upper(),
            "glyph": str(glyph),
            "relationship_type": str(relationship_type),
            "matrix_id": matrix_id,
            "label": str(label),
            "access_semantics": "index provides access, not instruction",
            "proposed_by": "ECHO",
            "status": "EXPERIMENTAL"
        }
        self.indexes.append(idx)
        return idx["id"]

    def view(self, matrix_id):
        return asdict(self.matrices[matrix_id])

    def save(self, matrix_id):
        data = self.view(matrix_id)
        data["indexes"] = [x for x in self.indexes if x["matrix_id"] == matrix_id]
        path = self.workspace / f"{matrix_id}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return str(path)

    def available_actions(self):
        return [
            "lookup(word)", "new_matrix(name,purpose)", "add_cell(matrix_id,content)",
            "add_dictionary_cell(matrix_id,word,sense_index)", "relate(source,target,type)",
            "index_glyph(glyph,matrix_id,label)", "view(matrix_id)", "save(matrix_id)"
        ]
