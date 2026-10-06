# MOD-0006 assessment — Static Python Flow Outline

## Source classification

`libmap.py` is executable Python used by the Dev Suite. It has no upstream test suite. It combines source AST outlining with runtime module import/introspection and contains a `gen_flow` path that depends on an externally injected `GENESIS_SRC` global.

Two independent characterization tests record source behavior: a missing target returns the JSON string `"null"`, and branch bodies are presented as an outline without join edges. The latter means the result must not be represented as a complete executable control-flow graph.

## Generalized contract

The generalized module accepts source text and a top-level function or direct class-method target. It parses without importing or executing the module, emits immutable deterministic nodes/edges, strictly bounds output and reports truncation. Syntax errors, absent targets and invalid limits fail explicitly.

Dependencies: Python standard library only.

## Limits

This is a structural outline, not a control-flow graph, call graph, data-flow engine, reachability proof, type checker, security scanner or sandbox. It does not resolve imports, decorators or dynamic dispatch.

## Licensing disposition

Internal preservation and research only. The source-branch license references AGPL-3.0 without including the complete text and adds use restrictions. Compatibility is not asserted.
