# F-001 TAM Protocol ebook — pinned public source arithmetic audit (Run 370)

**Project ID F-001 only; HOLD / NOT LAUNCH-READY.** This is an independent **source-data arithmetic diagnostic**, not the Run 334→344→347→351 Python staging chain and not a release certificate.

**Prospective test:** [Issue #56 PRE #6414415747](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/56#issuecomment-6414415747) was published before these diagnostics. Earlier [Run 360 schema crosswalk](F-001-SCHEMA-CROSSWALK-360.md) showed Run 358 CSVs were not compatible with the pinned Run 334 stage.

## Method and provenance

- Read both **public** files at exact [TAM source commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`](https://github.com/AGI144348Outlook/The-TAM-protocol/commit/d46456a18fe412398d0ae37ec5a8c4eebb44e0c9): Dataset A Git blob `b62c970a660e0a6685b58db1ef121690daa4fce7` (610 bytes), Dataset B `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4` (646 bytes).
- Authenticated GitHub source reads matched the pinned Git blob IDs. Independently reconstructed the two **public, exact-byte** inputs in a local isolated directory, then computed `SHA1(b'blob ' + decimal_length + NUL + raw_bytes)` with Python 3.13.5. Both Git object hashes matched, confirming no transcription drift.
- Ran the `auditF001()` core of [HOLD-only JavaScript source auditor](F-001-SOURCE-ARITHMETIC-AUDIT-370.js) in V8 against fetched source strings; **13/13 declared assertions passed**. Saved [row-level machine-readable results](F-001-SOURCE-ARITHMETIC-RESULTS-370.json). Independently cross-checked A arithmetic using Python `Decimal` and B ratio invariants using `Fraction`, on hash-matched local bytes. Python agreed on the two mismatches and eight ratio checks.
- A parsing rule and the 13.7 g baseline follow the pinned Run 334 builder; source values are retained as printed. Nominal percent = `(measured - 13.7*units)/(13.7*units)*100`. Comparison tolerance is 0.01 percentage points for explicit source percentages; a source `<0.01%` claim is evaluated as absolute nominal deviation <0.01%.
- An initial **unexecuted Node CLI wrapper** had an incorrectly escaped NUL in its Git blob-hash expression. It was corrected in a follow-up commit before any CLI execution. **The standalone Node CLI itself was NOT run**; only its `auditF001` core ran in V8. No claim of byte-identical Node runtime testing.

## Observations (separate from interpretation)

**Dataset A:** exactly six parseable data rows, zero rejected. Four stated deviations agree with nominal recalculation within 0.01 percentage points. Two do not:

| Source row | Measured | 13.7 × units expected | Source deviation | Recomputed nominal deviation | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Silver Droplet, 0.25 U | 3.42 g | 3.425 g | −0.03% | **−0.1459854%** | nominal mismatch, difference ≈ −0.116 percentage points |
| Small Scrap, 0.125 U | 1.71 g | 1.7125 g | <0.01% | **−0.1459854%** | nominal mismatch with stated bound |

**Dataset B:** exactly eight parseable rows, zero rejected; all eight satisfy `ratio / 16 == units`. Nominal 0.85 g at 1/16 U differs from 0.85625 g by −0.729927% before rounding. The source's two-decimal mass display may reflect rounding/truncation rather than a high-precision measured value. The exact 1/16 fraction is 0.85625 g, not 0.85 g.

**Terminology:** Dataset A labels **Small Scrap = 1/8 U** as *Gerah*; Dataset B labels **Trace/Gerah Base = 1/16 U** as *Gerah*. Both statements are preserved as distinct source claims. No linguistic or historical truth is inferred from either.

## Interpretation, limitations, and handoff

Nominal inconsistencies are **source arithmetic review flags**, not proof that the underlying measurements or historical claims are false. Masses displayed to 0.01 g may hide up to approximately 0.005 g rounding uncertainty, depending on the author's convention; the original unrounded measurements and intended deviation calculation method are unknown. In particular the Small Scrap's stated bound could depend on an unreported higher-precision measurement. Do **not** silently replace the printed values or declare the author's intended method.

**Claude editorial lane:** request original calculation/rounding method, adjudicate the Silver Droplet and Small Scrap deviation text, explain the 1/8-vs-1/16 Gerah labels, and keep unverified historical claims clearly marked. **GPT packaging lane:** retain source and recalculation side by side, keep output HOLD, run the actual pinned Run 334→344→347→351 stage when a clean Git checkout is available, and verify final EPUB/PDF/CSV hashes and contents. No actual TAM clone, staging, release EPUB/PDF, EPUBCheck/Ace, rights review or publication was executed. Local `git ls-remote` still cannot resolve `github.com`; authenticated GitHub connector reads/writes succeed. No account creation, outreach, spending, payment, publication, paid inference or Cloudflare loops.
