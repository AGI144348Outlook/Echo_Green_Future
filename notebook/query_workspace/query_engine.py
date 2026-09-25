#!/usr/bin/env python3
"""ECHO Notebook registry query workspace.

Read-only resolver over permanent registries. Queries create temporary matrices
in memory; persistence is explicit and never implies VGM validation.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "notebook" / "manifest.json"

def _load(path: str) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as f:
        return json.load(f)

def manifest() -> dict:
    return _load("notebook/manifest.json")

def resolve(handle: str) -> Any:
    section = manifest()["sections"].get(handle)
    if section is None:
        raise KeyError(f"Unknown notebook handle: {handle}")
    if section.get("kind") not in {"registry", "registry-source", "matrix"}:
        raise ValueError(f"Handle {handle} is not a queryable data source")
    return _load(section["target"])

def sources() -> list[dict]:
    return _load("notebook/registry_catalog.json")["sources"]

def _rows(obj: Any) -> list[Any]:
    if isinstance(obj, list):
        return obj
    if not isinstance(obj, dict):
        return [obj]
    for key in ("records", "entries", "rules", "substrates", "symbols", "formulas", "algorithms"):
        value = obj.get(key)
        if isinstance(value, list):
            return value
    # Map-shaped registries (e.g. geosensory) become keyed rows.
    meta = {"schema","status","principle","purpose","version","constraints","interfaces","domains","resolver","rule","recursive_lift","record_shape"}
    return [{"key": k, "value": v} for k, v in obj.items() if k not in meta]

def query(handles: str | Iterable[str], predicate: Callable[[Any], bool] | None = None,
          projection: Iterable[str] | None = None) -> dict:
    if isinstance(handles, str):
        handles = [handles]
    rows=[]
    for handle in handles:
        for row in _rows(resolve(handle)):
            if predicate is None or predicate(row):
                if projection and isinstance(row, dict):
                    row={k: row.get(k) for k in projection}
                rows.append({"source":handle,"row":row})
    return {"kind":"temporary_matrix","sources":list(handles),"rows":rows,"validated":False}

def retain(matrix: dict, name: str) -> Path:
    safe="".join(c for c in name if c.isalnum() or c in "-_").strip("_-")
    if not safe:
        raise ValueError("A non-empty safe name is required")
    path=ROOT/"notebook"/"retained"/f"{safe}.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8") as f:
        json.dump(matrix,f,ensure_ascii=False,indent=2)
        f.write("\n")
    return path

def save_view(name: str, handles: Iterable[str], predicate_spec: dict | None = None,
              projection: Iterable[str] | None = None) -> Path:
    safe="".join(c for c in name if c.isalnum() or c in "-_").strip("_-")
    if not safe:
        raise ValueError("A non-empty safe name is required")
    view={"kind":"saved_view","sources":list(handles),"predicate_spec":predicate_spec or {},
          "projection":list(projection or []),"validated":False}
    path=ROOT/"notebook"/"views"/f"{safe}.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8") as f:
        json.dump(view,f,ensure_ascii=False,indent=2); f.write("\n")
    return path
