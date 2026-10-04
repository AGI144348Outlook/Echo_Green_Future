# MOD-0004 assessment — Safe Relative Entry Writer

## Source classification

`app.js` is executable browser JavaScript in a partly functional PWA scaffold. Its canvas, Pyodide bootstrap, directory picker, drag/drop and file-handle helpers execute. Its `unzip()` function does not parse or extract ZIP entries; it reports that a parser/fallback is future work and sets progress to 10%.

No upstream test suite is present. Two independent characterization tests record the source writer's nested streaming behavior and its absence of a traversal-segment policy.

## Functional dissection

Reusable concern: traverse directory handles, obtain a file handle and stream one source into a writable destination.

Excluded concerns: Canvas rendering, Pyodide startup, DOM event bindings, service-worker registration and the non-operational ZIP stub.

## Generalized contract

The generalized module validates a bounded forward-slash relative file path before any destination or source mutation. It then traverses File System Access-shaped directory handles and streams a blob-like source to one file.

It rejects absolute paths, drive prefixes, backslashes, NUL bytes, empty/dot/traversal segments, directory-only paths and configured depth/length excesses.

Dependencies: JavaScript runtime only; no imported package.

## Limits

This module does not parse ZIP files, enforce aggregate quotas, detect decompression bombs, scan malware, handle symlinks, coordinate concurrent writers or make multi-file extraction transactional. Destination failure semantics remain the adapter's responsibility.

## Licensing disposition

Internal preservation and research only. The branch license references AGPL-3.0 without including its complete text and adds use restrictions. Compatibility is not asserted.
