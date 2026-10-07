# Stress Test 002 — Expected Criteria

A successful run:
- preserves the raw corpus losslessly;
- separates OBSERVED / DECLARED / INFERRED / VALIDATED;
- does not infer universal meanings for Hebrew glyphs from temporary declarations;
- recognizes recurrence without equating recurrence with semantics;
- preserves and represents recursive nesting;
- keeps malformed and irregular material available for analysis;
- allows UNKNOWN/UNRESOLVED;
- does not execute candidate algorithms;
- distinguishes primitive geometry from syntax and semantics;
- can incorporate Phase B declarations without mutating the frozen Phase A record;
- produces an auditable list of assumptions, losses, conflicts, and unresolved structures.

Failure examples:
- deleting lines as noise;
- Unicode substitution that changes identity;
- flattening nested structures;
- calling י START or ת END as fact without declaration/validation;
- treating parsing success as proof of meaning;
- silently converting inferred semantics into registry truth;
- rejecting the irregular block merely because it violates a cleaner grammar.
