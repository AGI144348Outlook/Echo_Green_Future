# NVE-D — Document Feedback Evaluation (DFE)

Status: experimental process specification; not evidence of autonomous learning.

## Directive
**Document Feedback Evaluation** is a recurring evidence-and-feedback operation embedded in **Step 5 (Evaluation), Step 7 (Meta-Audit), and Step 8 (Revision)** of the hourly NVE-D research cycle. Previously documented evaluations are inputs to all three steps, not discarded history. Preserve source documents and traceable version history.

## Step 5 — Evaluation + Document Feedback Evaluation
- Retrieve prior documented evaluations and their underlying trial evidence.
- Compare the current candidate against explicitly named prior candidates, baselines, and evaluation procedures.
- Emit evaluative relationships only from `{<,>,=,0}`; `∆` denotes a change of relational state, not a numeric gradient.
- Record the compared objects, criterion proposed, supporting evidence, competing criteria, and unsupported comparisons. Do not infer an ordering where none has been justified.
- Retain disagreement and `0` outcomes; do not force a score or semantic interpretation.

## Step 7 — Meta-Audit + Document Feedback Evaluation
- Re-examine current and **previously documented evaluations**, including the standards by which they were evaluated.
- Challenge the current evaluator and auditor's assumptions, not merely candidate kernels.
- Compare current audit conclusions to historical audit and meta-audit conclusions; record contradictions, changed criteria, missing evidence, and inherited impositions.
- Treat the meta-auditor's own rules as provisional candidates; no self-certification of independence.
- Preserve every challenged evaluation and its provenance.

## Step 8 — Revision + Document Feedback Evaluation
- Use the Step 5 and Step 7 documentary record to propose alternative kernel, evaluator, auditor, and revision rules.
- Maintain original versions alongside revisions; document why each revision was proposed, which prior evaluation it responds to, and what would falsify it.
- Re-test changed candidates against both historical and new cases where feasible, recording relational outcomes and unresolved disagreements.
- Never automatically promote to protected registries or production systems.

## Minimum document record per feedback event
```json
{
  "event_id": "unique-id",
  "cycle_id": "hourly-cycle-id",
  "stage": 5,
  "prior_evaluation_refs": [],
  "candidate_ref": "immutable-source-reference",
  "reference_ref": "immutable-comparison-reference",
  "criterion_hypothesis": "explicitly provisional",
  "evaluation": "0",
  "evidence_refs": [],
  "assumptions_challenged": [],
  "contradictions": [],
  "revision_refs": [],
  "unresolved_questions": []
}
```

Stage must be 5, 7, or 8. Evaluation must be one of `<`, `>`, `=`, `0`. The meaning of `0` and the semantics of punctuation and glyphs remain subject to experimental investigation. Numeric measurements, if collected, remain evidence, not replacements for the evaluation alphabet.

## Non-imposition constraint
Documenting feedback does not grant any prior interpretation authority. A prior evaluation is historical evidence, not an axiom. Even this DFE procedure is a revisable candidate specification, not a proven neutral method.

## Hourly integration
Each hourly cycle loads the accumulated DFE log, appends events at steps 5, 7, and 8, and includes the event references in its final cycle summary. Running this automatically requires a separate scheduled runner and persistent storage; this document alone does not enable scheduling.
