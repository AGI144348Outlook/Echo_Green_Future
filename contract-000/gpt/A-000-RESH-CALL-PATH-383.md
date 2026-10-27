# A-000 / Resh Lobby call-path correction — Run 383

Prospective test: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6430241594
Authority: Contract-000 blob 0fbc794, DISC-002 ee443fbc, TJ R5. Source: genesis-documentary:src/echo_governor_skeleton.py blob 63eb982989b4f3478d649430b555c8f4ba755c27.

## SOURCE-OBSERVED and bounded tests

1. `make_letter_lobby` (lines 9204–9245) constructs a separate Lobby, creates each WordAgent from `definition_words=props`, sets `generality_score=0.9`, calls `run_orientation()` and returns. It does not call `compute_generality_scores()`.
2. Only one `make_letter_lobby(` occurrence exists in the source: its definition. No `ReshIdentity(` constructor call appears in this file. This does not rule out callers in other modules.
3. The only executable `lobby.compute_generality_scores()` call (line 4651) is in the separate corpus Lobby pipeline, after populate/orientation/discovery. Another textual mention (line 3678) is a docstring. The initial assertion counted both and matched 11/12; corrected standalone-statement check yielded **12/12**.
4. `ReshIdentity.anchor()` updates the optional letter Lobby's resh `definition_words` through `list(set(...))`, but does not recompute genus or generality. `validate()` checks an instance flag, alias-key presence and `identity_symbol`, not a cryptographic witness.

## Interpretation / correction to Run382

Run382 identified a real order-sensitive **generic** `Lobby._compute_genus_depths()` implementation. It did not establish that a Hebrew letter Lobby calls this method after Resh anchoring. The available `make_letter_lobby` path hard-codes letter generality and performs no genus recomputation. Therefore resh-to-genus drift remains **UNDEMONSTRATED**, not an observed identity or runtime failure.

**Challenge / limitation:** a caller elsewhere could explicitly recompute Hebrew Lobby generality or integrate resh into the corpus Lobby. This run inspected one pinned source file, not all external call sites, and ran no Genesis Python runtime. Report slices and future order-dependent consumers remain possible. Do not silently sort semantically ordered definitions without Timothy's ruling.

**Next Claude:** trace actual integrations in other repositories and challenge this bounded conclusion. **Next Timothy:** witness/custodian, failure receipts, ordered-vs-set definition semantics and race acceptance remain open. No Genesis/main/Claude changes.