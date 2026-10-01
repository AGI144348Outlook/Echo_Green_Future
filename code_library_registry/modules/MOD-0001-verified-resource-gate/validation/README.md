# Validation

From the module directory:

```sh
PYTHONPATH=generalized python -m unittest discover -s validation -p 'test_*.py' -v
PYTHONPATH=original python -m unittest discover -s original -p 'test_*.py' -v
```

The first command validates the generalized contract. The second confirms that the preserved source and its tests remain executable without editing.
