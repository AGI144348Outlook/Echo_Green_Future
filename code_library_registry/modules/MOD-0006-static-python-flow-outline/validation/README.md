# Validation boundary

`test_source_characterization.py` is independently written; it is not an upstream suite. It records the source's `"null"` missing-target result and that its links are a lexical outline rather than a complete control-flow graph.

`test_static_python_flow_outline.py` contains seven generalized tests for non-executing parsing, branch labels, async class methods, deterministic serialization, strict bounds, explicit target/configuration failures and syntax errors.

Run from the module directory:

```sh
PYTHONPATH=original:generalized python -m unittest discover -s validation -p 'test_*.py' -v
```

The tests do not prove executable reachability, join points, exception propagation, data flow, type correctness or security of the analyzed source.
