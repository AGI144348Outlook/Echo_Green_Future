# Verification

The source branch contains executable code but no dedicated source test file for `echo_matrix_dictionary.py`. `test_source_characterization.py` therefore records two independently written characterization tests without representing them as an upstream suite.

Run all tests:

```bash
PYTHONPATH=generalized python -m unittest discover -s validation -p 'test_*.py'
```

The characterization tests cover the observed source behaviors for collection creation, cells, provider enrichment, relations, index binding, save, duplicate IDs and invalid provider selections. The generalized tests cover detached snapshots, reference integrity, provider boundaries, safe identifiers, atomic JSON save and preservation of a prior file when serialization fails.

