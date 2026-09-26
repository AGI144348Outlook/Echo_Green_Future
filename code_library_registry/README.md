# Echo Code Library Registry

This branch is an archival and assessment registry for historical code artifacts developed before or alongside the current Echo project.

Each incoming artifact should be preserved as close to its submitted form as practical, then accompanied by an assessment report rather than silently rewritten.

## Structure

- `artifacts/` — archived source artifacts, grouped by registry ID
- `assessments/` — technical assessment reports for each artifact
- `INDEX.md` — master registry and cross-reference table
- `ASSESSMENT_TEMPLATE.md` — standard assessment format

## Intake principles

1. Preserve provenance and original intent.
2. Separate archival copies from modernization work.
3. Document dependencies, architecture, assumptions, and failure modes.
4. Identify concepts or mechanisms relevant to the current Echo architecture.
5. Note duplication, supersession, or lineage relationships between artifacts.
6. Do not merge historical code into active Echo branches merely because it is archived here.
7. Use registry IDs in the form `CLR-0001`, `CLR-0002`, etc.

## Status vocabulary

- **Archived** — preserved, not yet deeply assessed.
- **Assessed** — assessment report completed.
- **Candidate** — contains mechanisms potentially useful to current Echo.
- **Superseded** — substantially replaced by a later artifact.
- **Reference** — useful primarily for history, concepts, or documentation.
- **Quarantined** — retained for study but unsafe, broken, or unsuitable for direct execution/integration.
