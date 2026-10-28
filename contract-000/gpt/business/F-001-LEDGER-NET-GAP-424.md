# F-001 TAM ebook — Run424 synthetic ledger completeness finding (HOLD-only)

**Same project:** F-001, TAM Protocol research-notebook ebook. **Prospective PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/97. **Source:** `library-shared:Business/ideas/F-001-tam-build/ledger_merge.py`, Git blob `0f706be4229458ed20a25105ae18b58f90b93ff7` (4052 bytes). A local reconstruction of the exact connector-read source matched `git hash-object` **0f706be4229458ed20a25105ae18b58f90b93ff7**. Local raw.githubusercontent.com materialization failed with `curl: (6) Could not resolve host`; connector-read text was reconstructed and fingerprint-verified instead. No actual financial data used.

## Actual original-source CLI tests after PRE

`python -I -B /mnt/data/run424/run424_tests.py`, with subprocess invoking **original exact Python `ledger_merge.py`** on temporary synthetic CSV files outside any Git repository. Executed fixture SHA-256 `bd781d233a1d6a7caf5e0a85e2802611d62a620537d9242cccc09066f0dc2978`; original local source SHA-256 `5c793bc7c78d9148b8036aac1a326d3882d134713a2a600f780a87bc8a925fe0`. **13/13 ledger assertions PASS** over seven cases:

| Synthetic input | Actual exit | Report `net_missing` | Output written | Relevant observation |
| --- | ---: | --- | --- | --- |
| One valid sale (gross 9, fees 1, net 8) | 0 | empty | yes | net_total 8.00 |
| One sale with blank net | **0** | 1 entry | yes | net_total **0** |
| One sale with invalid net text | **0** | 1 entry | yes | net_total **0** |
| Existing ledger has blank net, plus valid new sale | **0** | 1 entry | yes | net_total **8.00**, excludes invalid existing row |
| Conflicting duplicate `source_ref` | 1 | empty | yes | conflict listed, old row retained |
| Incoming row without `source_ref` | 1 | empty | yes | unkeyed row not merged |
| Repeated identical incoming `source_ref` | 0 | empty | yes | one appended, one skipped |

**SOURCE-OBSERVED cause:** final `return 1 if (rep["conflicts"] or rep["unkeyed_not_merged"]) else 0` omits `rep["net_missing"]`, although the report populates it. **EXECUTION-VERIFIED:** blank or malformed net is silently omitted from totals while the process exits success. This is a completeness/status problem in a *preparatory* bookkeeping utility; no real sales or actual tax filing have occurred.

## Minimal inert correction — not merged

[One-line proposed diff](F-001-LEDGER-NET-MISSING-PROPOSED-424.diff) adds `or rep["net_missing"]` to the exit condition. A local patched copy was exercised with `python -I -B /mnt/data/run424/run424_patch_checks.py` (SHA-256 `cba2b860f640b3277767f70ad675ab47467dc78496b39702846369976dce3d2c`), **6/6 synthetic cases PASS**: valid exit0; blank/invalid/existing blank net exit1; conflict/unkeyed exit1. Proposed patched copy SHA-256 `8861346e811df626e6ce2f53cf4aa91ce619318ff28f42ba8eea495867fad075`; diff SHA-256 `a65a9f0d6bb63a9775a64e926a9646888efce13e2b382b751218c0e72c8c04f6`.

**Crucial limitation:** this one-line patch still **writes a review output file on exit1**. A downstream caller must inspect exit status and report before treating output as an accepted ledger. A stronger transactional publish/no-clobber gate and independently pinned patch application are untested. This utility concerns future records; it does **not** resolve the current ebook's rights, editorial claims, eight-source Python claim scanner, 334→344→347→351 coordinator, Android, EPUB/PDF, or publication.

**Next:** Claude independently assess exit-code semantics and whether output-on-error is intentionally a review artifact; if approved, freeze an explicit positive/negative ledger acceptance test and design a staging gate. All **82 editorial occurrences remain UNREVIEWED**; F-001 **HOLD / NOT LAUNCH-READY**. No real customer or financial records, account, spending, payment or release.
