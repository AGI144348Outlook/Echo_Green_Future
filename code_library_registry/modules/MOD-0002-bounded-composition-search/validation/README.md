# Verification

Run the preserved source experiment:

```bash
python original/test_autonomous_agency_a1.py
```

Run the generalized suite:

```bash
PYTHONPATH=generalized python -m unittest discover -s validation -p 'test_*.py'
```

The source script's own assertion checks the experimental/control distinction and ordered provenance chain. The generalized tests additionally verify shortest replayable paths, zero-length goals, depth/expansion limits, rejected states, operation-error handling and duplicate-name rejection.

