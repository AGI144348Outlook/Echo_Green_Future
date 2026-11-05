# Echo GPT Round 5 — executable glyph DSL

Pre-test Issue: #274. This is an isolated GPT-only research branch, not a canonical Genesis update.

## Canonical role alignment

22 base glyphs: א INITIALIZE; ב CONTAIN; ג TRAVERSE; ד FILTER; ה REVEAL; ו CONNECT; ז TIMESTAMP; ח BOUND; ט COIL; י SEED; כ CAPACITY; ל DIRECT; מ FLOW; נ INDIVIDUATE; ס CYCLE; ע PERCEIVE; פ EXPRESS; צ HUNT; ק SCAN_PERIPHERY; ר GOVERN; ש TRANSFORM; ת SEAL. Final forms ך ם ן ף ץ are contextual specializations of כ מ נ פ צ, not independent conceptual primitives.

## Prototype design

The 3×3×3 registry assigns 27 unique glyph addresses. Each glyph has a Python execution branch over a typed packet carrying `data`, `state`, `trace`, `sealed`; interpreter enforces program budget and execution traces. Examples: ד filters list using an injected predicate; מ buffers a list; ו creates connection with trace provenance; ר checks budget; ת seals packet; ם closes flow. The DSL is currently a sequential glyph string interpreter; not yet a dynamic graph or independent learning agent.

## Observations

16 unittest cases passed locally: 27 unique addresses; all 27 executable on a list input; canonical role mapping; filter correctness; invalid type rejection; program budget; bounded cycle; connection provenance; sealing; governor budget; multi-glyph DSL composition (`עדמפ`); unknown glyph rejection; final-form variants; recipe replay and tamper rejection; candidate hunt; ordered trace. The tested composition `עדמפ` applied a supplied `x>0` filter to `[0,1,2]`, buffered and expressed `[1,2]`. No autonomous task discovery was tested. The source, tests and full stdout are in the conversation artifact `echo_round5` and need uploading to this branch for independent reproduction.

## Research rationale

Algebraic effects separate operation syntax from effect interpretation: https://www.eff-lang.org/handlers-tutorial.pdf ; scoped effects demand special handling: https://lmcs.episciences.org/14832 ; modular higher-order effects: https://doi.org/10.1145/3571255 . Our interpreter is only inspired by these designs; it does not implement a formal effect calculus.

## Limitations and next steps

Current operations are deliberately minimal, not algorithmically mature: for instance, צ uses a supplied predicate and selects first match; ש applies an injected transform. No proof of formal correctness, concurrency, adaptive edges, robust identity/provenance or generalization. Next: full contract schema per glyph; implement bounded algorithm families and typed effect handlers; test compositional laws and error recovery; enable packet exchange on graph; assess discovered recipes against unseen task families.
