# NVE-D Cycle 017 — Document Feedback Evaluation (repository summary)

**Evidence:** `NVE-D-HOURLY-017-summary.json` and local reproducibility package `NVE-D-HOURLY-017-artifacts.zip` (runner, fixture, structural auditor, checkpoint and witness records). Full DFE is in the local package; this committed document is an abridged index. Finite DVE fixture only. Evaluations are restricted to `{<,>,=,0}`; ∆ is a relational change, not an evaluation.

## Step 5 — Evaluation + DFE

```json
{"event_id":"NVE-D-017-S5","cycle_id":"NVE-D-HOURLY-017","stage":5,"prior_evaluation_refs":["NVE-D-HOURLY-014-DFE.md","NVE-D-HOURLY-015-DFE.md","NVE-D-HOURLY-016-DFE.md"],"candidate_ref":"local TCP witness with operation-id deduplication","reference_ref":"one durable journal record per operation and exact conflict rejection","criterion_hypothesis":"exact witness journal identity after recovery","evaluation":"=","evidence_refs":["run017/network-results.json","run017/summary.json","run017/audit.json"],"assumptions_challenged":["committed witness record implies delivered acknowledgment","separate process implies independent custody"],"contradictions":["84 corrected transport cases =; initial evaluator falsely recorded 84 0 due tuple/list mismatch","180 checkpoint replays = but 30 final-state and 80 event-trace comparisons had ∆ under reversed ordering"],"revision_refs":["R17-A","R17-B"],"unresolved_questions":["remote partition behavior","cross-epoch identity"]}
```

## Step 7 — Meta-Audit + DFE

```json
{"event_id":"NVE-D-017-S7","cycle_id":"NVE-D-HOURLY-017","stage":7,"prior_evaluation_refs":["NVE-D-003-meta-audit.md","NVE-D-HOURLY-011-DFE.md","NVE-D-HOURLY-014-DFE.md","NVE-D-HOURLY-015-DFE.md","NVE-D-HOURLY-016-DFE.md"],"candidate_ref":"NVE-D-HOURLY-017-auditor.py","reference_ref":"independent transition oracle and independently held witness","criterion_hypothesis":"structural checks do not authenticate causal history","evaluation":"0","evidence_refs":["run017/audit.json","run017/network-results.json"],"assumptions_challenged":["auditors cannot share representation defects","loopback equals remote partition","internal digest equals authentic history"],"contradictions":["first evaluator incorrectly emitted 0 for all network cases, corrected rerun =","Cycle 014 witness staleness and tampering both caused mismatch","Cycle 015 coordinated rollback could appear equal"],"revision_refs":["R17-A","R17-B","R17-C"],"unresolved_questions":["independent custody","independent transition recomputation"]}
```

The structural auditor checked 180 checkpoint records, 84 transport cases and 96 SQLite journal entries; structural evaluation `=`. It did not independently recompute kernel transitions or establish external witness custody.

## Step 8 — Revision + DFE

```json
{"event_id":"NVE-D-017-S8","cycle_id":"NVE-D-HOURLY-017","stage":8,"prior_evaluation_refs":["NVE-D-HOURLY-015-DFE.md","NVE-D-HOURLY-016-DFE.md","NVE-D-017-S5","NVE-D-017-S7"],"candidate_ref":"R17-A/R17-B/R17-C/R17-D","reference_ref":"Cycle 017 loopback witness","criterion_hypothesis":"do not rank custody models without defined trust boundaries","evaluation":"0","evidence_refs":["run017/summary.json","run017/audit.json"],"assumptions_challenged":["local TCP implies independent witness custody","matching journal proves authentic history"],"contradictions":["local recovery = while coordinated rollback remains possible"],"revision_refs":["R17-A","R17-B","R17-C","R17-D"],"unresolved_questions":["separate host custody","randomized faults","conceptual/digital bridge criteria"]}
```

**Unexecuted proposals:** R17-A independently administered append-only witness; R17-B remote partitions and randomized crash timing; R17-C independently coded transition oracle and canonical type serialization; R17-D separately specify virtues and evidence bridges for EVE/NVE/CVE/DVE/DCVE/CDVE/CDCVE.

**Known evaluation defect retained:** first network run reported 84 false `0` evaluations because Python tuples were compared with JSON lists. Comparator corrected, network cases actually rerun; prior 180 SHA-verified checkpoint rows reused without re-counting transitions. No protected registry modification, merge or deployment.
