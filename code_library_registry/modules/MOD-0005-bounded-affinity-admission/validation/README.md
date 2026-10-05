# Validation boundary

`test_source_characterization.py` contains two independently written tests. They are not an upstream suite. They record the source ledger's undirected aggregation/endpoint-count behavior and the fact that rejected candidates stay at the front of its queue.

`test_bounded_affinity_admission.py` contains seven generalized tests covering unambiguous undirected accounting, invalid ties, threshold/capacity decisions, starvation avoidance, transactional scorer failure, deterministic sampling/tie order and configuration/score validation.

Run from the module directory:

```sh
PYTHONPATH=generalized python -m unittest discover -s validation -p 'test_*.py' -v
```

The tests demonstrate deterministic bounded mechanics. They do not validate any real-world affinity function, threshold, recommendation quality or fairness claim.
