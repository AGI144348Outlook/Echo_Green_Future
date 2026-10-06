# Applications and limits

## Meaningful applications

- generate a bounded structural outline for a Python function before showing it in a browser or notebook;
- inspect direct class methods without importing or executing the module;
- inventory statement kinds and visible call names for documentation or review triage;
- provide deterministic nodes and edges to a UI renderer;
- cap output from large functions while stating that truncation occurred.

## Contract

Input is Python source text, a top-level function name or direct class/method pair, and positive node/call-name bounds. Output is an immutable `FlowOutline` with stable node identifiers, lexical nesting/order edges and an explicit truncation flag.

Parsing never imports the supplied module. Syntax errors, missing targets and invalid limits fail explicitly. Dependencies are Python's standard library only.

## Assumptions and non-applications

The source must parse under the running Python grammar. Only a top-level function or direct member of a top-level class is selected. This is not an executable control-flow graph, call graph, data-flow analysis, reachability proof, type checker, security scanner or sandbox. It does not follow imports or resolve dynamic dispatch.
