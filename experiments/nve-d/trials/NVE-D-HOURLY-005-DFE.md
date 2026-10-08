# NVE-D-HOURLY-005 — DFE 5/7/8
All evaluation fields are from `{<,>,=,0}`. ∆ denotes changed relational state.

## Step 5 — Evaluation
Event: NVE-D-HOURLY-005-S5. Prior references: NVE-D-HOURLY-001-DFE, NVE-D-HOURLY-003-report, local NVE-D-HOURLY-004-report. Candidate: 005 full runner; reference: uninterrupted vs midpoint serialized/reloaded run. Criterion: exact equality of final digital state/history/clock/source bytes. **Evaluation: `=`**; evidence: 540/540 in 005 summary. Contradictions: 99/180 disagreements between artificial low/high-bit evaluators; semantic comparisons remain `0`. No claim of conceptual NVE or symbolic understanding.

## Step 7 — Meta-Audit
Event: NVE-D-HOURLY-005-S7. Prior references: NVE-D-003-meta-audit, 001-S7, local 004, 005-S5. Candidate: witness/scheduler audit; reference: independent trusted witness and semantic oracle (not available). **Evaluation: `0`**. Assumptions challenged: held-out digest is not an authenticated immutable witness; shared authored algorithm is not independent oracle; reverse-order equality is expected under isolated state. Contradictions: 540/540 original-witness tamper detections coexist with acceptance of jointly forged checkpoint and witness; 48 isolated order equalities coexist with 12 shared-state order differences.

## Step 8 — Revision
Event: NVE-D-HOURLY-005-S8. Prior references: 005-S5, 005-S7, NVE-D-003-meta-audit. Proposal: independently implemented message-passing scheduler, externally authenticated append-only witness, separate CVE virtue/type specification and independent reference implementation. **Evaluation: `0`** (unexecuted). Falsifiers: cross-node leakage under declared isolation, unauthorized witness replacement undetected by trusted verification, and oracle disagreement. Preserve earlier contradictory records; no automatic registry promotion, merge or deployment.
