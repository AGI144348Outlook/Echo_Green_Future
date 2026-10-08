# NVE-D evaluation alphabet constraint — candidate protocol v0.1

User directive: **Use `{<,>,=,0}` for evaluation only.**

## Boundary
These four tokens are **evaluation outputs**, not Mashet execution operators, not numerical scores, not optimization instructions, and not symbol identities. Keep execution traces, candidate configurations, and evidence separately. No automatic Registry 0 promotion.

## Provisional comparator interpretation (must be user-confirmed)
For an explicit comparison of candidate A against reference B, with a named metric and declared direction:
- `<`: A evaluates below B on that metric.
- `>`: A evaluates above B on that metric.
- `=`: A and B evaluate equally on that metric under a declared tolerance.
- `0`: evaluation is absent, invalid, or insufficient to make a supported comparison. **This is a proposal, not a confirmed user definition.**

No automatic conversion of `<` or `>` to “good” or “bad”; meaning depends on the metric and orientation. `0` is not numeric zero and is not an automatic rejection. For missing metric orientation, missing baseline, incompatible evidence, or failed audit, emit `0` provisionally.

## Application
Each experiment, audit, meta-audit, and review emits only one of the four tokens as its **evaluation field**. Other fields may hold explanation, trace IDs, measurements, and queue items but must not substitute scores, pass/fail, or retain/reject labels for the evaluation token. Review disposition is a distinct decision field.

## Trial comparison example
```json
{"candidate":"selection","reference":"frozen","metric":"held_out_loss","orientation":"lower_is_better","evaluation":"<","evidence_ref":"NVE-D-004-summary.json"}
```

This is a representation of a recorded numeric comparison, not a new experiment. `<` here means the candidate's measured loss was lower.

## Meta-audit
An audit of an audit must also use the same four-token evaluation alphabet, with the evaluated property named explicitly. Missing audit evidence maps provisionally to `0` and creates a gap queue item.

## Pending clarification
Confirm whether `0` means *no comparison / unknown* or a different intended concept. Do not silently reinterpret it.
