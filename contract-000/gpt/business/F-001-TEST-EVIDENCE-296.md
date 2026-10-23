# F-001 — GPT Run 296 v3 offline characterization evidence (2026-10-23)

**Pre-test notice:** Issue #13 comment [6362437264](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/13#issuecomment-6362437264), published before executing these exploratory tests. **Project:** F-001 TAM Protocol ebook, still ON HOLD.

**Method:** Read Claude §103 and the committed GPT v2 gate and harness first. In isolated local scratch (Linux, Python 3.13.5), extracted the archived public TAM source-derived Dataset A/B source files, pinned `rebuild_datasets.py`, `dataset-a.csv`, `dataset-b.csv`, and `dataset-check.json` from the previous Run 295 handoff. Modified a local GPT v3 copy to set `editorial=NOT_EVALUATED` unless Dataset A source/builder pins and CSV bytes/structure were checked. Reused the original 10 cases and added four A-specific corruptions. Invoked `python3 -I -B test_gate_v3.py` with fresh temporary copies per case; checked process exit and JSON `integrity/editorial/release` fields. No CI, external API, production EPUB build, Echo A-000 runtime, paid inference or Cloudflare loop. Local tested verifier logic (`def digest` through `verify`) was compared with the committed GPT v3 verifier and matched; local and committed files differ in nonexecuting header/usage text. The committed harness also retains the same 14 case definitions; fixture files are not committed.

**Observed: 14/14 expected outcomes.**

| Case | Exit | Integrity | Editorial | Release |
|---|---:|---|---|---|
| Baseline integrity | 0 | PASS | HOLD | HOLD |
| Baseline release | 3 | PASS | HOLD | HOLD |
| Truncated B | 1 | FAIL | HOLD | HOLD |
| Changed B ratio | 1 | FAIL | HOLD | HOLD |
| Changed B registry sign | 1 | FAIL | HOLD | HOLD |
| Missing B | 1 | FAIL | HOLD | HOLD |
| Tampered report | 1 | FAIL | HOLD | HOLD |
| Extra B row | 1 | FAIL | HOLD | HOLD |
| Changed B source | 1 | FAIL | HOLD | HOLD |
| Invalid invocation | 64 | — | — | — |
| Missing A | 1 | FAIL | NOT_EVALUATED | HOLD |
| Wrong A header | 1 | FAIL | NOT_EVALUATED | HOLD |
| Changed A bytes (valid header) | 1 | FAIL | NOT_EVALUATED | HOLD |
| Changed A source | 1 | FAIL | NOT_EVALUATED | HOLD |

**Observation vs interpretation:** Missing, header-corrupt, byte-altered, or source-altered Dataset A now returns `NOT_EVALUATED` rather than the misleading `NO_FLAGGED_ROWS` found by Claude §103. The intact pinned delivery still reports editorial HOLD because two pre-existing Dataset A `stated_matches_recomputed=False` rows have not been dispositioned. Exit 0 in integrity mode is not permission to publish; release mode exits 3 for intact but unresolved editorial rows.

**Deviations / setup failures:** An initial local preparation script had an unmatched triple quote and failed with SyntaxError before producing v3; a subsequent premature harness invocation failed with TypeError because the v3 script was not yet installed. These were local setup errors, not observed gate outcomes. After correcting the setup, the final 14-case suite ran and passed. The test expands the three promised A failure cases to four (including changed A source).

**Limitations:** Source commit pin is recorded but not independently authenticated; output hashes are from a previously rebuilt pinned fixture, not a new production build; test harness depends on uncommitted fixture copies; source claims, licensing, storefront terms, accessibility, EPUB/PDF and independent reviewer authorization were not tested. No release readiness is asserted.

**Next:** Claude independently reviews the v3 `NOT_EVALUATED` semantics and disposition-file schema. A future draft should distinguish `disposition recorded` from `editorial approved` and keep the four-artifact receipt fail-closed until Timothy's explicit decisions. No shared/Claude/main writes or deletions.
