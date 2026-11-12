#!/usr/bin/env python3
"""ECHO-021 diagram-expression port for source-attributed Echo study outputs.

Does not answer questions, solve arithmetic, invent reasons, or translate
curriculum prompts into solved examples. Only represents:
  1) arithmetic results ALREADY returned by Echo's study algorithm; or
  2) a source-fragment lookup as such, never a causal proof.
A refusal remains a refusal.

OpenDiagram validates and renders this interchange without any AI model.
The producer claim is an experimental process attribution, not a signature.
"""
from __future__ import annotations

import json
import re
from typing import Any

PROTOCOL = "echo.diagram/v1"

def emit_from_echo_answer(
    *,
    run_id: str,
    stimulus_id: str,
    prompt: str,
    echo_answer: dict[str, Any],
    title: str,
) -> dict[str, Any]:
    if not run_id or not stimulus_id:
        raise ValueError("Source run/stimulus identity required")
    raw_answer = echo_answer.get("raw_answer")
    response = raw_answer if isinstance(raw_answer, str) and raw_answer.strip() else None
    reasons = echo_answer.get("reason")
    source_refs = [s for s in (echo_answer.get("source_refs") or []) if isinstance(s, str) and s]
    source_refs = list(dict.fromkeys(source_refs + ["stimulus:" + stimulus_id]))
    result = {
        "protocol": PROTOCOL,
        "producer": "echo_algorithm",
        "agent_run_id": run_id,
        "stimulus_id": stimulus_id,
        "title": title,
        "status": "abstained" if response is None else "partial",
        "utterance": response,
        "nodes": [],
        "relations": [],
        "source_refs": source_refs,
    }
    if response is None:
        return result

    # Echo's *own* observed_math_operator/structure outcome is the only
    # condition permitting a numeric computation trace. We copy its output
    # and original operands; there is NO calculation in this adapter.
    if reasons in ("observed_math_operator", "observed_math_structure"):
        numbers = [int(n) for n in re.findall(r"\d+", prompt)]
        if len(numbers) >= 2 and re.fullmatch(r"-?\d+", response.strip()):
            operation = "addition" if (
                "+" in prompt or any(x in prompt.lower() for x in ("altogether", "more", "total", "finds"))
            ) else "subtraction" if (
                "-" in prompt or "−" in prompt or any(x in prompt.lower() for x in ("left", "gave", "remaining"))
            ) else None
            if operation is not None:
                n1, n2 = numbers[:2]
                a = {"id": "given-a", "label": "given", "kind": "quantity",
                     "quantity": n1, "source_refs": ["stimulus:" + stimulus_id]}
                b = {"id": "given-b", "label": "given", "kind": "quantity",
                     "quantity": n2, "source_refs": ["stimulus:" + stimulus_id]}
                o = {"id": "observed-result", "label": "Echo reported", "kind": "quantity",
                     "quantity": int(response), "source_refs": source_refs}
                result["nodes"] = [a, b, o]
                result["relations"] = [
                    {"id": "applied-a", "from": "given-a", "to": "observed-result",
                     "predicate": "reported_" + operation, "source_refs": source_refs},
                    {"id": "applied-b", "from": "given-b", "to": "observed-result",
                     "predicate": "reported_" + operation, "source_refs": source_refs},
                ]
                result["status"] = "expressed"
                return result

    # A retrieved source passage is a *retrieval provenance* diagram.
    # We do not turn words such as "because" into a proven causal edge.
    if reasons == "source_retrieval_fragment" and source_refs:
        result["nodes"] = [
            {"id": "question", "label": prompt, "kind": "observation",
             "source_refs": ["stimulus:" + stimulus_id]},
            {"id": "retrieved", "label": response, "kind": "observation",
             "source_refs": source_refs},
        ]
        result["relations"] = [
            {"id": "retrieval", "from": "question", "to": "retrieved",
             "predicate": "retrieved_text_for", "source_refs": source_refs},
        ]
    return result

def emit_many(
    answers: list[dict[str, Any]], run_id: str
) -> list[dict[str, Any]]:
    return [
        emit_from_echo_answer(
            run_id=run_id,
            stimulus_id=str(a["id"]),
            prompt=str(a["question"]),
            echo_answer=a,
            title="Echo source expression / " + str(a["id"]),
        )
        for a in answers
    ]

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", type=str, required=True)
    args = parser.parse_args()
    original = json.loads(args.input.read_text())
    if not isinstance(original, list):
        raise RuntimeError("Expected actual recorded Echo response list")
    traces = emit_many(original, args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(traces, indent=2, ensure_ascii=False) + "\n")
    counts = {
        "total": len(traces),
        "abstained": sum(t["status"] == "abstained" for t in traces),
        "asserted_relations": sum(len(t["relations"]) for t in traces),
        "reported_calculations": sum(any(e["predicate"].startswith("reported_") for e in t["relations"]) for t in traces),
        "source_retrieval_diagrams": sum(any(e["predicate"] == "retrieved_text_for" for e in t["relations"]) for t in traces),
        "authorship": "ECHO-020 algorithm output only, rendered by ECHO-021; no newly computed answers",
    }
    print("ECHO021_DIAGRAM_BASELINE " + json.dumps(counts))
