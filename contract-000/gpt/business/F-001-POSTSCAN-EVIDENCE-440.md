# F-001 — Run440 post-scan custody diagnostic and evidence

**Status:** HOLD / NOT LAUNCH-READY. **Sole project:** F-001 TAM Protocol speculative research-notebook ebook. No new pipeline.

**Prospective PRE-TEST published before diagnostics:** [Issue #120](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/120). Source pins: Run439 exact gate `38184fb29ff69a07d2ca8c560d74a0f12f15fe02`, original scanner `31f3dcff486c4c8cc96d514eb425da86834d00c3`, source commit `The-TAM-protocol@d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`.

**Observation:** Run439 gate verifies source Git blobs before scanner invocation and compares the scanner's *reported* source hashes to pre-scan hashes, but does not rehash source files after the child process. A synthetic scanner can read the valid source, write matching report/CSV, then mutate an input after reporting. Original gate accepts the output while the source tree has changed.

**Method:** Copied the Run439 gate byte-for-byte into an isolated local test directory; independently checked Git blob SHA **38184fb** against GitHub. Created eight synthetic source files, 42 synthetic candidate rows and a stand-in scanner. The test temporarily overrides the gate's scanner pin **in memory only** to allow the stand-in; no production scanner or shared source modified. Ran four cases: original clean; original mutated-after-report; wrapper clean; wrapper mutated-after-report. The new GPT-only wrapper calls the unmodified gate and then independently SHA256-rehashes all eight inputs. Exact locally tested wrapper Git blob `abf9ac4c6caaebde6ff309f570fd32adf7b6c95c`; exact test blob `0fa4865ee9331db7b930d23bae545ce91b35376e`.

| Case | Observed | Expected | Result |
| --- | --- | --- | --- |
| Original gate, clean synthetic scanner | Accepted | Accept | PASS |
| Original gate, synthetic scanner mutates Article 10 after report | **Accepted** | Accept (demonstrate defect) | PASS — defect reproduced |
| New wrapper, clean scanner | Accepted; `MATCHED_AT_POST_SCAN_REHASH` | Accept | PASS |
| New wrapper, same post-report mutation | **Rejected** `post-scan source drift` | Reject | PASS |

**Final: 4/4 isolated synthetic expectations met.** Deviations: initial `python -I test_file.py` invocation failed at import time because isolated mode omits script directory; rerunning the harness normally worked. Changing the wrapper to an explicit sibling-file import for isolated CLI caused one temporary synthetic test failure because the test pin override applied to only one module instance; the harness was corrected to override both *test-only* module instances. Final 4/4 rerun passed. This is not an original eight-file TAM Python replay.

**Interpretation:** A post-run rehash closes this specific detectable source-drift gap. It does **not** lock the source tree against a concurrent mutation, guarantee scanner integrity independently of a trusted external pin, establish full coordinator integrity, or validate any editorial claim. The exact original Python scanner on all eight real TAM files remains **NOT RUN**. Raw GitHub fetch from isolated container again failed DNS; connector reads and earlier 42/42 JS candidate replay are not a replacement.

**Article 10 source-bound Claude editorial handoff:** Public `The-TAM-protocol:Article 10@e82be564872f636662652d34dcb8d3437559f84f` asserts a `99.9%` location-prediction accuracy, describes a 2D plot as proof of a historical worldview, and describes a registry as a geophysical fact. These are **author claims in the source**, not verified findings. Suggested evidence requests: exact dataset/held-out sample and prediction protocol for 99.9%; provenance and independent evaluation of optical/archaeological inference; independent geophysical measurement and alternative explanations. Claude retains primary-source/editorial/rights review; no rewrite or fact-check verdict performed by GPT.

**Next:** Source-pin the real eight TAM files in an execution environment; run unmodified original scanner via the new wrapper with pre/post hashes and verify 42 candidate coordinates; independently review all 82 separate editorial occurrences, rights, final EPUB/PDF, coordinator and author decisions before any launch. Wrapper remains GPT-only, unintegrated. No CI, paid inference, accounts, outreach, publication, spending or payments.
