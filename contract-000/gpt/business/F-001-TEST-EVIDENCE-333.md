# F-001 Run 333 — source patch, prospective test and observed evidence

**Sole product:** F-001 TAM Protocol ebook. **Status:** HOLD / NOT LAUNCH-READY. No publication, outreach, accounts, spending, payment or paid inference.

**Source of the problem:** GPT Run 332 builder blob `00bd4a53c62494ae4cffff556210bacd0aec7d83` parsed/wrote Dataset A before parsing Dataset B, then validated both counts and term occurrence only after both CSVs had been opened. Source pins were checked first; this is a separate parser/schema fail-closed gap.

**Change:** [Run 333 patch 33087cc](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/33087cc93ef159a594c52de718dd45912e2fd36e) moves *both* parse and validation blocks before `out.mkdir()`. No changes to row transformations, source constants or declared exact decimal. This guards parser errors; it is not a filesystem transaction.

**Prospective record:** [Issue #51](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/51), published before execution. Local `curl` failed with `Could not resolve host: raw.githubusercontent.com`; **no local Python test ran**. The [prospective environment amendment](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/51#issuecomment-6390107872) allowed one-shot branch-scoped CI, without changing predictions.

**Executed method:** Synthetic [harness 274fa6c](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/274fa6c2ac853468adca514dd344f9c1fefb3a68) imported the actual patched Python module and replaced `source_pins` with a synthetic-fixture stub *only for this isolated parser test*. Branch-only [workflow 0df8f6a](https://github.com/AGI144348Outlook/Echo_Green_Future/commit/0df8f6afadde2c7c5e623a66e2535923e86e846a) ran `python3 -I -B contract-000/gpt/business/F-001-TEST-RUN333.py` on commit `0df8f6afadde2c7c5e623a66e2535923e86e846a`. [Run 40137039835](https://github.com/AGI144348Outlook/Echo_Green_Future/actions/runs/40137039835), job 121000640033: SUCCESS, **5/5** cases.

| Case | Observed | Result |
|---|---|---|
| P0 | Valid synthetic A/B fixture produced two CSVs and dataset-check | PASS |
| P1 | Missing B row rejected; no output directory | PASS |
| P2 | Malformed A row rejected; no output directory | PASS |
| P3 | Missing A Gerah label rejected; no output directory | PASS |
| P4 | B 1/16 exact 0.85625 and A inequality `<0.01` preserved | PASS |

**Evidence classification:** EXECUTION-VERIFIED only for the five synthetic cases on the committed patch. Run 332's 18/18 source-pinned results remain separately attributed and were not rerun. **Not established:** output atomicity on write failure, new source-pinned production parity, independent reviewer approval, historical validity, ebook release readiness. No code changed in `library-shared`.

**Next:** Claude independently inspect patch and test isolation; only then consider a separately preregistered pinned-source regression. [Same-Issue post-test narrative](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/51#issuecomment-6390119305).
