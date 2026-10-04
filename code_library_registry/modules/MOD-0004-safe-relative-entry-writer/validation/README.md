# Validation boundary

`test_source_characterization.mjs` contains two independently written tests for the preserved browser script. They are not an upstream test suite. One records its intended nested streaming behavior; the other records that the source passes `..` through to the directory adapter without a path-policy check.

`test_safe_relative_entry_writer.mjs` contains six tests for the generalized module: canonical relative paths, rejected path classes, configurable budgets, fail-before-mutation behavior, ordered streaming writes and failure propagation.

Run from the module directory:

```sh
node --test validation/*.mjs
```

These tests do not claim ZIP parsing, decompression, quota enforcement, browser permission behavior or transactionality.
