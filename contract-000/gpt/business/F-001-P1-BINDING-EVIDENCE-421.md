# F-001 TAM Protocol — P1 family/occurrence binding verification (Run421)

**Sole project:** F-001 TAM research-notebook ebook, HOLD / NOT LAUNCH-READY. **Prospective PRE:** [Issue #94](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/94) published before all Run421 controls. **Source packet:** `contract-000/gpt/business/F-001-P1-TRIAGE-420.json` Git blob `eb139defefba0e86ac23879e753e892ee654aca5`, source TAM commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`; 18 P1 occurrences / 14 distinct exact sentences / four duplicate pairs. All 82 editorial occurrences remain UNREVIEWED.

## New deliverable

`f001_p1_family_binding_421.js` is a **read-only, HOLD-only, source-pinned** packet validator. It checks source commit, parent packet blob, eight TAM source fingerprints, schema, 14 families, 18 occurrence IDs, four two-occurrence families, 14 distinct family sentences, occurrence-to-family binding, source locations, exact sentence equality, and explicit UNREVIEWED/false evidence/rights/release flags.

The Node CLI path additionally checks the **Git blob SHA-1 of the exact input JSON bytes** against `eb139defefba0e86ac23879e753e892ee654aca5` before parsing. This prevents an attacker or accidental edit from replacing all corresponding sentences consistently and still passing the structural checks. The CLI hash path was **not executed in this run**; it is source-inspected, not independently CLI-verified. A caller must supply the unchanged Run420 packet.

## Actual bounded tests

**22/22 in-isolate JavaScript checks passed against the actual connector-returned Run420 packet**: two positive cases (original and reordering) and 20 negative mutation cases: missing occurrence; duplicate occurrence; switched family; changed source sentence; wrong occurrence pin; release flag; family status; occurrence status; evidence flag; source-pin set; wrong location ID; wrong counts; missing reviewer question; duplicate family; unrepresented family ID; wrong project; parent packet pin; rights flag; human-reviewed count; duplicate exact sentence family.

**Observed:** original packet passes with zero validation errors; all 20 mutated inputs are rejected for the expected error category. **Interpretation:** this gate can catch these internal consistency failures. **NOT established:** Node CLI execution, cryptographic verification against a hostile source beyond Git blob matching, historical accuracy, scientific support, publication rights, editorial dispositions, real-source original Python scanner parity, or final product quality. The test harness used a V8 in-memory module evaluator, not the Node command-line runtime.

**Expected acceptance:** a real CLI run with unchanged packet must exit 0; changing even one raw byte must exit nonzero due to the Git blob check; source status/rights flags must remain HOLD. Those CLI controls remain outstanding and must be pre-registered again before execution.

**Human/editorial next step:** Claude independently reviews the 14 P1 sentence families against primary evidence, counterevidence and licensing, recording one disposition per family and reflecting it at all 18 occurrences. GPT then integrates signed human decisions into a **new** source-pinned packet, never silently edits the Run420 source packet. Timothy's A1–A6/B1/B4/B6/C1 and publication decisions remain required. No release, outreach, account, spending or payment action.
