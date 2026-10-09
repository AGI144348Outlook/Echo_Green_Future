# Conditions Registry (Contract 000 §27)

| ID | Trigger | Condition | Action | Route | Level | Approved | Disable by |
|---|---|---|---|---|---|---|---|
| C-001 | Push to `bridge/ops/*.json` or the bridge workflow on `bridge-experiment` | Always | Run bridge **inventory only** (never deploys) | 1 | 0 | Timothy, 2026-10-08 (bridge split) | Remove the `push` trigger from the bridge workflow |
| C-002 | Timothy adds `run:approved` to an Issue titled `[RUN] bridge <participant>` | Sender is the repository owner; title matches exactly | Start the bridge for that participant; it runs the participant's current operation file after re-validating it | 3 | 1 | Timothy, 2026-10-09 | Delete `.github/workflows/label-dispatcher.yml` from `main` (Timothy's approval) |

Proposed conditions are added below with level and justification, labeled `awaiting:timothy` on `[C-000]`, and move into the table only once approved.
