# ECHO work queue — 2026-09-30
Status: queued; this document does not claim implementation or review completion.

## Today's sequence
- [ ] 1. New ZIP intake: receive the new attachment, inspect its manifest, dependencies, code and overlap with existing branches; recommend an exact branch/path before repository placement. Preserve original archive and provenance. No new ZIP was attached to this request.
- [ ] 2. Licensing follow-up: resolve PR #2's competing LICENSE addition, AGPL/commercial-policy contradictions, complete license text, branch-aware scope, third-party exclusions, source notices and README/CLA consistency. Prepare concrete revisions; do not merge or invent a licensing decision.
- [ ] 3A. Inventory executable code across all repository branches at pinned commit SHAs. Deduplicate identical blobs while preserving every branch/path lineage. Reuse existing CLR assessments; distinguish available source, missing source, specifications and placeholders.
- [ ] 3B. Dissect source into independently usable functional modules, then generalize by abstraction BEFORE searching external repositories. Record input/output contracts, assumptions, dependencies, failure modes and meaningful validation. Freeze a dated abstraction revision before discovery to preserve independence from search bias.
- [ ] 3C. Preserve original/unabstracted code and generalized equivalents in their own folders under code_library_registry/modules/<module-id>/. Retain original copyright, licenses and provenance. Document functional applications and demonstrated limitations.
- [ ] 3D. After abstraction, inspect issues in 1,000 distinct GitHub repositories; track reviewed counts, pinned evidence, incomplete reviews and resume cursors. Identify issue-fit first, then license compatibility, then apply filters for correctness, maintenance, contribution guidelines, duplication, feasibility and demonstrable value. Select 0–2 repositories per module; zero is valid. Do not substitute 1,000 search hits for 1,000 repository reviews.
- [ ] 3E. Write each proposed contribution under that generalized module's proposals/<owner>--<repo>/ folder. Include issue URLs, how/why the code helps, adaptation and verification plan, license/notices, and possible benefit to Echo's agency. Otherwise explain strategic attention value or classify as purely open-source philanthropy. Do not claim upstream contribution before an actual linked contribution exists.
- [ ] 3F. Evaluate code-library-registry for merge to main: inspect full branch diff, archive size, source availability, tests, license/provenance, and deployment/workflow effects. Prepare recommendation; merge is not authorized by consideration alone.
- [ ] 4. Dev Suite: use dev-suite as an isolated branch from pwa-hosting-environment. Review Notebook-to-Canvas WidgetSpec contracts, responsive Echo widget creation, Registry references and capability boundaries. Investigate actual Pyodide-compatible drag/drop development features from primary documentation. Prototype a fresh PWA workspace with separate practice state; do not treat Pyodide itself as a drag/drop IDE.
- [ ] 5. Geo-Sensory visualization: continue geosensory-crawler-experiment; inspect actual sensed endpoint records and their units, timestamps, coordinates, provenance and coverage. Design visual models from measured data, clearly separating observations, derived values, missing/stale data and conceptual models.

## Daily review
One scheduled daily morning run repeats 3A–3E, reviews existing generalized modules for new functional applications, and updates source/generalized folders, application notes and proposal records. Reuse prior evidence and only recompute when changes or gaps warrant it.
Continue the tracked 1,000-repository discovery in honest resumable batches. Record progress and limitations, never claim completion from search result counts.
No automatic merge, deployment, upstream PR submission or outreach is included.

## Module layout
code_library_registry/modules/<module-id>/
  provenance.json
  original/                 # preserved source + notices
  generalized/              # independent functional code + documentation
    APPLICATIONS.md
    proposals/<owner>--<repo>/PROPOSAL.md
  validation/
  ASSESSMENT.md

## Discovery/review records
code_library_registry/reviews/ contains dated branch snapshots, changed-module assessments, verified repository counts, evidence and resume state. Existing assessments and artifacts retain their identities.


## Checkpoint — 2026-10-01

- Branch snapshot recorded for all 15 current branches.
- MOD-0001 (`verified-resource-gate`) preserved, generalized, validated and abstraction-locked before discovery. Preserved source tests: 3/3 passing; generalized tests: 5/5 passing.
- Frozen abstraction commit: `f27de97fd6e65ed57e7e8c27f60982abbea93be2`.
- External discovery: 5 distinct repositories reviewed; 0 selected; cumulative progress 5/1,000.
- License compatibility remains unasserted. Four candidates lacked a retrievable root project license; the fifth uses path-sensitive mixed licensing.
- Resume at repository ordinal 6. Continue narrower issue-first searches for staged initialization and fail-closed resource exposure. See `reviews/MOD-0001_DISCOVERY_BATCH_2026-10-01.md` and `reviews/PROGRESS_2026-10-01.md`.
