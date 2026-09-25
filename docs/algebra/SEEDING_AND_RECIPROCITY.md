# Algebra branch — seeding, licensing, and reciprocity

This branch is project-authored. No third-party source code is copied by this seed commit. External repositories were studied for architectural enrichment only.

## Internal architectural seed
- AGI144348Outlook/dual-order-os — informed separation of matrices, indices, and libraries; its by-glyph/bidirectional indexing work motivated keeping address/index structures distinct from source matrices.

## External repositories reviewed
- sympy/sympy — symbolic-expression and computer-algebra reference. License file permits redistribution/modification under BSD-style conditions. Current use here: conceptual reference only; no SymPy code copied. Candidate reciprocal contribution: reusable tests/examples for independent verification of externally-produced symbolic/glyph-abacus expressions, if shaped to SymPy contribution standards.
- networkx/networkx — graph/index relation reference. 3-clause BSD. Current use here: conceptual reference only; no NetworkX code copied. Candidate reciprocal contribution: if ECHO develops a generally useful provenance-preserving bidirectional relation/index example or test case, prepare it separately against NetworkX contribution requirements rather than injecting project-specific semantics upstream.
- lark-parser/lark — grammar/parser architecture reference. MIT. Current use here: conceptual reference only; no Lark code copied. Candidate reciprocal contribution: a small Unicode symbolic-grammar example/test, only if it demonstrates a generally useful parser behavior and follows upstream contribution rules.
- spdx/tools and SPDX specifications — license/provenance metadata reference. Apache-2.0 for spdx/tools. Current use here: conceptual reference only; no code copied. Candidate reciprocal contribution: report/test any concrete interoperability issue discovered while representing branch-level provenance and SPDX identifiers.

## Reciprocity rule
Before importing code/data: (1) fetch and record exact upstream license at the revision used; (2) determine compatibility with this repository's licensing; (3) preserve required copyright/NOTICE/attribution; (4) record upstream repo + revision + files + local branch + local paths; (5) identify a plausible upstream-beneficial contribution; (6) do not claim contribution until an upstream issue/PR is actually submitted and linked.

## Branch seeded
All references above assisted the `algebra` branch. A main-branch attribution ledger records this relationship without merging experimental algebra code into main.
