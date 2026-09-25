# Trial 015 — Governed Notebook Manipulation

## Question
Can the new Notebook/Mashet stack resolve a goal into a valid, provenance-preserving manipulation without bypassing the Governor gates?

## Prompt
> Create a new working object that preserves the information contained in both Notebook objects A and B. Do not alter A or B.

The prompt deliberately names no Hebrew glyph and no Mashet operator.

## Baseline honesty constraint
The first executable harness uses a transparent deterministic selector. Therefore its selection events are labeled **HARNESS_POLICY**, not ECHO. A PASS proves the wiring, algebraic invariants, provenance behavior, and gate ordering work. It does **not** prove autonomous ECHO operator selection.

The next phase replaces only the selector with an ECHO-facing deliberation interface while keeping this baseline as a control.

## Required trace
GOAL → IDENTIFY → HEBREW_SELECT → MASHET_SELECT → DEPENDENCY_RESOLVE → VALIDATE_OPEN → OPERATE → POST_VALIDATE.

## Pass conditions
A and B remain unchanged; result has a new identity; provenance names both sources; result remains WORKING/not automatically validated; Mashet algebra dependency resolves before OPEN.
