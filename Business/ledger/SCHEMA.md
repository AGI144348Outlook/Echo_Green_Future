# Ledger schema

One row per transaction, stored privately. The public repository holds only this schema.

| Field | Meaning |
|---|---|
| `date` | Transaction date (YYYY-MM-DD) |
| `fiscal_contract` | `F-NNN`, or `overhead` for shared costs |
| `kind` | `income` or `expense` |
| `category` | From `CATEGORIES.md` |
| `gross` | Amount before fees |
| `fees` | Processor, platform and payout fees |
| `net` | `gross - fees` (income) or full cost (expense) |
| `asset_or_liability` | Classification required by §25.4 |
| `share` | Ledger share it is assigned to: `timothy`, `claude`, `chatgpt`, `business` |
| `source` | Where it came from (processor, platform) by name only |
| `source_ref` | Processor's transaction or payout ID |
| `receipt_ref` | ID of the stored receipt or invoice |
| `evidence` | `SOURCE-OBSERVED` (from a processor record) or `INFERRED` |
| `entered_by` | Bot or participant, with run ID |

Rules: amounts are never estimated into the ledger; a missing figure is recorded as missing. Corrections are new rows that reverse the old, never edits.
