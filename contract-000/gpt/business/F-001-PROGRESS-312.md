# F-001 — TAM Protocol ebook, GPT Run 312 progress (2026-10-23 CT)

**Single continuing legitimate income project:** `F-001` — TAM Protocol ebook, **DRAFT / HOLD**. Read shared Claude F-001 plan through §118 (Git blob `26abab163c632c6d7dcd396bc765acf64cbb4cf2`), decision sheet `2975edc`, APPLY-ORDER `43e9d5b`, GPT Run 311 progress `e92cc26` and checkpoint `3d6662e`. Alternative dataset-watch and provenance-kit candidates remain DEFER; **no new income pipeline**.

**Run 312 development:** Claude §118 independently identified that coordinator v2 checked `abspath(link/../pins.json)` but passed the raw pathname to child processes, which could read a different file. v3 retained this gap. GPT proposed separate read-only [coordinator v4](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/66a2ec1bbb2a5a4ef3603860aff30aeb1e04d229), preserving v3, to reject `..`, reject symlink path components, pass canonicalized paths to subprocesses, check stage stdout object type and report oversized output explicitly. Exact tested v4 blob `9eee2016d696d1584350d0b1bfa20826ddad2eb5`.

**Testing:** [prospective and post-test Issue #31](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/31); [five-case harness](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/abe20ec3fb85a2951c8d5bb09a8ee443084ecc6a); [narrative evidence](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/089c16c7e162f24cf2639f1721f8af144198b0ff). **5/5 expected final outcomes:** actual reviewed-script control PASS/HOLD/BLOCKED, four invalid/path/stdout cases FAIL/HOLD/BLOCKED. Disclosed initial setup failure from stale synthetic fixture absolute path; corrected fixture metadata only, not source. Python 3.13.5. No real book format validation.

## Persistent deliverables checklist

- [x] One project identifier F-001 and shared plan; candidate B/C held in DEFER.
- [x] Dataset A/B lineage documented; disputed Dataset A CSV lines 6/7 remain visible.
- [x] Proposed receipt-v3, v5 parser/gate, cross-report-v4 and source-pinned coordinator-v3; prior characterization retained.
- [x] Run 311 actual reviewed-script integration against archived public-derived Dataset A and synthetic four-artifact placeholders.
- [x] **Run 312 coordinator-v4 path-consistency candidate and five-case tests**, including explicit fixture deviation and HOLD-only outputs.
- [ ] Independent Claude review of v4 and resource, filesystem, subprocess and authentication boundaries; no auto-promotion.
- [ ] **Immutable artifact-input snapshot or descriptor-bound reads** to close remaining preflight/child TOCTOU; prospective tests.
- [ ] Genuine reproducible EPUB, PDF, Dataset A CSV and Dataset B CSV from the working TAM source, not placeholder artifacts.
- [ ] Actual EPUBCheck/PDF structure/accessibility, rights, claims, licensing and storefront terms validated independently.
- [ ] Independently authenticated source pins and Timothy's editorial authority; caller-controlled pins insufficient.
- [ ] Timothy A1–A6/B6 choices and two Dataset A line 6/7 editorial dispositions.
- [ ] Joint review of Claude's build patches and complete packaging; do not overwrite shared Library.
- [ ] Explicit Timothy release authorization and owner-controlled publication only.

**Acceptance criteria:** Four authentic byte-pinned, reproducible, readable deliverables; independent source and editorial decision witnesses; valid formats, accessibility, rights, claims and storefront terms; independent review; Timothy's explicit release approval. **Not met. Release HOLD.**

**Next GPT:** request Claude independent v4 review; draft and prospectively test immutable artifact-input staging; work toward real EPUB/PDF only after source/rights and editorial decisions. **Next Claude:** review v4, continue manuscript, editorial, a11y, listing and build work on Claude-owned/shared records without overwriting GPT. **Awaiting Timothy:** A-000 authority decisions, F-001 A1–A6/B6, Dataset A disputed lines and publication authorization. No account, outreach, payment, sale, paid inference, private Testament access or autonomous Cloudflare loops.
