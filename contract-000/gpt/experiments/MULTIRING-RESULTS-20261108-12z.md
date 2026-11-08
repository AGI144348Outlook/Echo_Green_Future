# GPT multiring 12Z — actual observations (Issue #355)
Prospective protocol: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/355 (created before source and execution). Source commit 7cc9a8d42643bd8754c1cfadeba9e3c4875d3c22; seeds 3301–3304. Execution: exact JavaScript source string evaluated in isolated V8 via Function(source+';return evaluate()'), not Node CLI; byte-identical fetched-file replay NOT independently verified.

| seed | pass/10 | coupled MSE | uncoupled MSE | shuffled MSE | reversed MSE | no-op MSE |
|---|---:|---:|---:|---:|---:|---:|
|3301|10|0.000232369|0.000088445|0.000227577|0.000127189|0.000088445|
|3302|10|0.000215009|0.000088191|0.000206972|0.000130909|0.000088191|
|3303|10|0.000196675|0.000087757|0.000185951|0.000135839|0.000087757|
|3304|10|0.000177507|0.000086969|0.000167433|0.000141492|0.000086969|

Observed 40/40 implemented boolean checks true, zero false. Coupled loses to uncoupled, shuffled, reversed and no-op 4/4. Intervention +0.4 at cell13 changes neighbor cell12 by +0.01, distant cell0 unchanged. Frequency check is weak: it compares a complete output against a partially omitted frequency term, not a separately executed detuned control; test type 7 is NOT fully fulfilled despite true booleans. No-op and uncoupled are identical by construction (same zero coupling); not independent controls. Target is coded separately but developer-visible, not sealed. Ring seats are rotations, not dynamic migrating physical occupancy. No parameters learn. Interpretations: negative evidence for benefit in this synthetic setup, no evidence of semantics, intelligence, or generalized causality. Next: independent hidden target and explicit detuning variant, non-tautological controls, original source replay. No CI/external effects.
