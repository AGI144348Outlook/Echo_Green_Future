"""Bounded, deterministic static outlines for Python function source."""

from __future__ import annotations

import ast
from dataclasses import dataclass


class TargetNotFound(LookupError):
    """Raised when the requested top-level function or direct class method is absent."""


@dataclass(frozen=True)
class OutlineNode:
    id: int
    kind: str
    label: str
    detail: str
    depth: int


@dataclass(frozen=True)
class OutlineEdge:
    source: int
    target: int
    label: str


@dataclass(frozen=True)
class FlowOutline:
    target: str
    nodes: tuple[OutlineNode, ...]
    edges: tuple[OutlineEdge, ...]
    truncated: bool
    max_nodes: int

    def as_dict(self) -> dict[str, object]:
        return {
            "target": self.target,
            "nodes": [node.__dict__ for node in self.nodes],
            "edges": [edge.__dict__ for edge in self.edges],
            "truncated": self.truncated,
            "max_nodes": self.max_nodes,
        }


def _positive_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _text(node: ast.AST | None, limit: int) -> str:
    if node is None:
        return ""
    value = ast.unparse(node).splitlines()[0]
    return value if len(value) <= limit else value[: limit - 3] + "..."


def _call_names(node: ast.AST, limit: int) -> tuple[str, ...]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            try:
                names.add(ast.unparse(child.func))
            except (ValueError, TypeError):
                continue
    return tuple(sorted(names)[:limit])


def _find_target(tree: ast.Module, function: str, class_name: str | None) -> ast.FunctionDef | ast.AsyncFunctionDef:
    if class_name is None:
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function:
                return node
        raise TargetNotFound(f"top-level function {function!r} was not found")

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for member in node.body:
                if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)) and member.name == function:
                    return member
            raise TargetNotFound(f"method {class_name}.{function} was not found")
    raise TargetNotFound(f"class {class_name!r} was not found")


def outline_source(
    source: str,
    function: str,
    *,
    class_name: str | None = None,
    max_nodes: int = 48,
    max_call_names: int = 6,
) -> FlowOutline:
    """Parse source without importing it and return a bounded structural outline.

    Edges describe lexical nesting and statement order. They are not an executable
    control-flow graph: joins, loop back-edges, exception propagation and reachability
    are intentionally not inferred.
    """

    if not isinstance(source, str):
        raise TypeError("source must be text")
    if not function:
        raise ValueError("function must be non-empty")
    limit = _positive_int(max_nodes, "max_nodes")
    call_limit = _positive_int(max_call_names, "max_call_names")
    target = _find_target(ast.parse(source), function, class_name)

    nodes: list[OutlineNode] = []
    edges: list[OutlineEdge] = []
    omitted = False

    def add(kind: str, label: str, detail: str, depth: int) -> int | None:
        nonlocal omitted
        if len(nodes) >= limit:
            omitted = True
            return None
        node_id = len(nodes)
        nodes.append(OutlineNode(node_id, kind, label, detail, depth))
        return node_id

    def connect(source_id: int | None, target_id: int | None, label: str) -> None:
        if source_id is not None and target_id is not None:
            edges.append(OutlineEdge(source_id, target_id, label))

    def generic(statement: ast.stmt, depth: int, previous: int | None, edge_label: str) -> int | None:
        calls = _call_names(statement, call_limit)
        rendered = ast.unparse(statement)
        detail = rendered[:400] + ("\ncalls: " + ", ".join(calls) if calls else "")
        node_id = add("statement", _text(statement, 56), detail, depth)
        connect(previous, node_id, edge_label)
        return node_id if node_id is not None else previous

    def block(statements: list[ast.stmt], depth: int, previous: int | None, first_label: str) -> int | None:
        label = first_label
        for statement in statements:
            if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant) and isinstance(statement.value.value, str):
                continue
            if isinstance(statement, ast.If):
                gate = add("branch", "if " + _text(statement.test, 48), ast.unparse(statement.test), depth)
                connect(previous, gate, label)
                block(statement.body, depth + 1, gate, "true")
                block(statement.orelse, depth + 1, gate, "false")
                previous, label = gate, "next"
            elif isinstance(statement, (ast.For, ast.AsyncFor)):
                gate = add("loop", "for " + _text(statement.target, 18) + " in " + _text(statement.iter, 30), ast.unparse(statement.iter), depth)
                connect(previous, gate, label)
                block(statement.body, depth + 1, gate, "each")
                block(statement.orelse, depth + 1, gate, "else")
                previous, label = gate, "done"
            elif isinstance(statement, ast.While):
                gate = add("loop", "while " + _text(statement.test, 48), ast.unparse(statement.test), depth)
                connect(previous, gate, label)
                block(statement.body, depth + 1, gate, "true")
                block(statement.orelse, depth + 1, gate, "else")
                previous, label = gate, "false"
            elif isinstance(statement, (ast.Return, ast.Raise)):
                kind = "return" if isinstance(statement, ast.Return) else "raise"
                value = statement.value if isinstance(statement, ast.Return) else statement.exc
                node_id = add(kind, kind + (" " + _text(value, 48) if value else ""), ast.unparse(statement), depth)
                connect(previous, node_id, label)
                previous, label = node_id, "next"
            else:
                previous, label = generic(statement, depth, previous, label), "next"
        return previous

    qualified = f"{class_name}.{function}" if class_name else function
    start = add("function", qualified, ast.unparse(target.args), 0)
    block(target.body, 0, start, "first")
    return FlowOutline(qualified, tuple(nodes), tuple(edges), omitted, limit)
