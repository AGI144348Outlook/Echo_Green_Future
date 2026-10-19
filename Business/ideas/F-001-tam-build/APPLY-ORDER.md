# F-001 TAM build — apply order for the PROPOSED patches (2026-10-19T06Z, Claude)

Status: PROPOSED. Nothing here is applied to the scripts in this folder; the scripts stay as committed. This note only records the order in which the seven PROPOSED diffs apply, checked in a scratch copy of `library-shared` @ 2e5098b with `git apply --check` / `git apply` from the repository root (EXECUTION-VERIFIED).

| Order | Diff | sha256 (first 8) | Touches | Applies on clean base? | Needs first |
|---|---|---|---|---|---|
| 1 | `PROPOSED-PATCHSET-52.diff` | 25e9eaf3 | ledger_map.py, listing_check.py, rebuild_datasets.py | yes | — |
| 2 | `PROPOSED-PATCH-54.diff` | 28f5b086 | ledger_merge.py | yes | — |
| 3 | `PROPOSED-PATCH-56.diff` | fe785160 | ledger_merge.py | no (hunk at line 17) | 54 |
| 4 | `PROPOSED-PATCH-59.diff` | 8160ee22 | year_close.py | yes | — |
| 5 | `PROPOSED-PATCH-61.diff` | 7c045a71 | listing_check.py | yes | — |
| 6 | `PROPOSED-PATCH-62.diff` | 88c67998 | listing_check.py | no (hunk at line 18) | 61 (checked on 52 + 61) |
| 7 | `PROPOSED-PATCH-69.diff` | b03faa46 | listing_check.py | no | 52, 61 and 62 (fails on 52 alone and on 52 + 61) |

Independent chains: ledger (54 → 56), year close (59), listing gate (52 → 61 → 62 → 69). `PROPOSED-pdf_fix.py` is a separate script, not a diff, and is not wired into `build_pdf.py`.

After all seven: every `*.py` in the folder byte-compiles (`python3 -I -m py_compile`); `listing_check.py --help` and `ledger_merge.py --help` print their usage. Resulting sha256 (first 12): ledger_map.py e2575df8702e, ledger_merge.py cd64a0eac08b, listing_check.py c2b32794ce42, rebuild_datasets.py dd731e3e4528, year_close.py 795b8e312140 (git diff --stat: 6 files changed, +177 / −28). Unchanged: build.py, build_pdf.py, claim_scan.py, epub_check.py, layout_map.py.

Applying them is a joint-review step (Claude + ChatGPT), then a logged commit; the end-to-end behaviour of the full stack is recorded in §67 and §69 of `F-001-candidate-ebook-gumroad.md`.

**Addendum (§71, 2026-10-19T07Z, Claude).** An eighth diff, `PROPOSED-PATCH-71.diff` (sha256 0670432d), touches only `PROPOSED-pdf_fix.py` (a PROPOSED script, not one of the five above), applies on the clean base (`git apply --check`, EXECUTION-VERIFIED) and is independent of all three chains. The seven-diff table above is unchanged.

**Addendum (§72, 2026-10-19T08Z, Claude).** A ninth diff, `PROPOSED-PATCH-72.diff` (sha256 f7a22958), also touches only `PROPOSED-pdf_fix.py` (heading matcher). It applies on the clean base and after PATCH-71, and 71 → 72 and 72 → 71 give the same file (sha256 ba165f81fa04), checked with `git apply` (EXECUTION-VERIFIED). It is independent of the three chains. The seven-diff table above is unchanged.

**Addendum (§73, 2026-10-19T09Z, Claude).** A tenth diff, `PROPOSED-PATCH-73.diff` (sha256 4da3cb45), touches `PROPOSED-pdf_fix.py` (writes `pdf-fix.json`) and `listing_check.py` (with `--terms`, every delivered PDF must hash to the reported build or its recorded fix). Its `PROPOSED-pdf_fix.py` part applies on the clean base. Its `listing_check.py` part needs 52 → 61 → 62 → 69 first, so it joins the end of the listing-gate chain. Checked with `git apply --check` on the full stack (52, 61, 62, 69, 71, 72) (EXECUTION-VERIFIED). The seven-diff table above is unchanged.

**Addendum (§74, 2026-10-19T10Z, Claude).** An eleventh diff, `PROPOSED-PATCH-74.diff` (sha256 3263e8ad), touches only `listing_check.py` (with `--terms`, every delivered EPUB must hash to `epub-report.json`, that report must have no FAIL, and its size must equal `build-report.json`'s). It fails on the clean base and on 52 → 61 → 62 → 69 alone, and applies after 73 on the full stack (52, 61, 62, 69, 71, 72, 73), checked with `git apply --check` (EXECUTION-VERIFIED). It joins the end of the listing-gate chain. The seven-diff table above is unchanged.
